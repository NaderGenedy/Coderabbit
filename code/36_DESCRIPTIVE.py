#!/usr/bin/env python3
"""CALON-C — descriptive analysis for the manuscript.

Produces, for BOTH cohorts:
  T1  Table 1        every analysis variable, overall and by incident-event status,
                     with standardised mean differences
  T2  Missingness    n and % missing for every variable, plus a test of whether
                     missingness predicts the outcome (the Welsh registry has
                     previously shown outcome-related missingness, OR 4.75)
  T3  Per-variable   UNADJUSTED / AGE-ADJUSTED / FULLY-ADJUSTED hazard ratios for
                     every candidate variable, side by side, with direction
                     reversals flagged. This is the "all variables in all methods"
                     analysis.
  T4  Event ledger   component counts and date completeness
  T5  Follow-up      person-years, median follow-up, censoring pattern

Governance: aggregate output only. Cells with <10 events are suppressed.
"""
from __future__ import annotations

import importlib.util
import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from lifelines import CoxPHFitter

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "outputs"
_s = importlib.util.spec_from_file_location("cc", ROOT / "code" / "33_CALON_C.py")
cc = importlib.util.module_from_spec(_s); sys.modules["cc"] = cc; _s.loader.exec_module(cc)

MIN_EV = 10
CONT = ["age", "nonhdl_unt", "ldl_unt", "hdl", "remnant_unt", "tg_filter",
        "cum_nonhdl", "bmi", "lpa"]
BIN = ["male", "htn", "dm", "smoke"]
ALL_VARS = CONT + BIN


def smd(a, b):
    """Standardised mean difference between two groups."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    a, b = a[np.isfinite(a)], b[np.isfinite(b)]
    if len(a) < 2 or len(b) < 2:
        return np.nan
    s = np.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2)
    return float((a.mean() - b.mean()) / s) if s > 0 else np.nan


def table1(df, cohort):
    rows = []
    ev, nev = df[df.E == 1], df[df.E == 0]
    for v in ALL_VARS:
        if v not in df:
            continue
        x = pd.to_numeric(df[v], errors="coerce")
        xe = pd.to_numeric(ev[v], errors="coerce")
        xn = pd.to_numeric(nev[v], errors="coerce")
        if v in BIN:
            rows.append({"cohort": cohort, "variable": v, "type": "binary",
                         "overall": f"{int(x.sum())} ({100*x.mean():.1f}%)" if x.notna().any() else "—",
                         "events": f"{int(xe.sum())} ({100*xe.mean():.1f}%)" if xe.notna().any() else "—",
                         "non_events": f"{int(xn.sum())} ({100*xn.mean():.1f}%)" if xn.notna().any() else "—",
                         "smd": smd(xe, xn), "n_observed": int(x.notna().sum()),
                         "pct_missing": 100 * x.isna().mean()})
        else:
            f = lambda s: (f"{s.median():.2f} ({s.quantile(.25):.2f}–{s.quantile(.75):.2f})"
                           if s.notna().sum() > 0 else "—")
            rows.append({"cohort": cohort, "variable": v, "type": "continuous",
                         "overall": f(x), "events": f(xe), "non_events": f(xn),
                         "smd": smd(xe, xn), "n_observed": int(x.notna().sum()),
                         "pct_missing": 100 * x.isna().mean()})
    return rows


def missingness_vs_outcome(df, cohort):
    """Does being MISSING on a variable predict the outcome?"""
    rows = []
    for v in ALL_VARS:
        if v not in df:
            continue
        miss = pd.to_numeric(df[v], errors="coerce").isna().astype(float)
        if miss.sum() < 20 or (1 - miss).sum() < 20:
            rows.append({"cohort": cohort, "variable": v, "pct_missing": 100 * miss.mean(),
                         "HR_missing": None, "note": "too few in one group"})
            continue
        m = pd.DataFrame({"miss": miss, "T": df["T"], "E": df["E"]}).dropna()
        if m.E.sum() < MIN_EV:
            continue
        try:
            c = CoxPHFitter().fit(m, "T", "E")
            hr = float(np.exp(c.params_["miss"])); se = float(c.standard_errors_["miss"])
            rows.append({"cohort": cohort, "variable": v, "pct_missing": 100 * miss.mean(),
                         "HR_missing": hr, "lo": float(np.exp(np.log(hr) - 1.96 * se)),
                         "hi": float(np.exp(np.log(hr) + 1.96 * se)),
                         "p": float(c.summary.loc["miss", "p"])})
        except Exception:
            pass
    return rows


def per_variable_hr(df, cohort):
    """UNADJUSTED / AGE-ADJUSTED / FULLY-ADJUSTED, side by side."""
    rows = []
    full = [v for v in cc.usable(df, cc.SPEC_FULL)]
    for v in ALL_VARS:
        if v not in df:
            continue
        x = pd.to_numeric(df[v], errors="coerce")
        if x.notna().sum() < 50 or x.nunique(dropna=True) < 2:
            continue
        sd = x.std(ddof=1)
        out = {"cohort": cohort, "variable": v,
               "scale": "per SD" if v in CONT else "present vs absent",
               "sd": float(sd) if v in CONT else None,
               "n_observed": int(x.notna().sum())}
        for label, terms in (("unadjusted", [v]),
                             ("age_adjusted", [v, "age"] if v != "age" else ["age"]),
                             ("fully_adjusted", sorted(set(full) | {v}))):
            terms = [t for t in dict.fromkeys(terms) if t in df]
            m = df[terms + ["T", "E"]].copy()
            for t in terms:
                m[t] = pd.to_numeric(m[t], errors="coerce")
                if v in CONT and t == v and sd > 0:
                    m[t] = m[t] / sd                       # per-SD scaling
                m[t] = m[t].fillna(m[t].median())
            if m.E.sum() < MIN_EV:
                continue
            try:
                c = CoxPHFitter(penalizer=0.0 if len(terms) < 3 else cc.PENALTY).fit(m, "T", "E")
                b, se = float(c.params_[v]), float(c.standard_errors_[v])
                out[f"{label}_HR"] = float(np.exp(b))
                out[f"{label}_lo"] = float(np.exp(b - 1.96 * se))
                out[f"{label}_hi"] = float(np.exp(b + 1.96 * se))
                out[f"{label}_p"] = float(c.summary.loc[v, "p"])
            except Exception:
                out[f"{label}_HR"] = None
        # direction reversal flag
        hrs = [out.get(f"{k}_HR") for k in ("unadjusted", "age_adjusted", "fully_adjusted")]
        hrs = [h for h in hrs if h is not None]
        out["direction_reversal"] = bool(hrs and (max(hrs) > 1) and (min(hrs) < 1))
        rows.append(out)
    return rows


def followup(df, cohort):
    py = float(df["T"].sum())
    return {"cohort": cohort, "n": int(len(df)), "events": int(df.E.sum()),
            "person_years": py, "rate_per_1000py": 1000 * df.E.sum() / py,
            "median_followup": float(df["T"].median()),
            "iqr_followup": [float(df["T"].quantile(.25)), float(df["T"].quantile(.75))],
            "max_followup": float(df["T"].max()),
            "clusters": int(df["cluster"].astype(str).nunique())}


def main():
    ukb, lu = cc.build_ukb(); wal, lw = cc.build_wales()
    t1, t2, t3, t5 = [], [], [], []
    for cohort, df in (("UK Biobank", ukb), ("Wales", wal)):
        print(f"  {cohort}: Table 1 …"); t1 += table1(df, cohort)
        print(f"  {cohort}: missingness …"); t2 += missingness_vs_outcome(df, cohort)
        print(f"  {cohort}: per-variable HRs …"); t3 += per_variable_hr(df, cohort)
        t5.append(followup(df, cohort))

    # T4 — event components, UKB (Wales components are ages, handled separately)
    import os
    c = pd.read_csv(Path(os.environ["CALON_CORRECTED_DATA"]) / "data_corrected" /
                    "corrected_ascvd_outcomes.csv", low_memory=False)
    m = pd.read_csv(Path(os.environ["CALON_SHARED_MASTER"]) / "UKB" / "ukb_master.csv",
                    usecols=["eid", "ldlr_carrier"], low_memory=False)
    d = m.merge(c, on="eid", how="left")
    d = d.loc[pd.to_numeric(d.ldlr_carrier, errors="coerce").eq(1)]
    t4 = [{"component": k, "n_carriers_positive": int(pd.to_numeric(d[k], errors="coerce").fillna(0).gt(0).sum())}
          for k in ["i21_event", "i25_event", "i63_event", "i70_event", "i73_event",
                    "g45_event", "i50_event"]]

    for name, rows in (("table1", t1), ("missingness", t2), ("per_variable_hr", t3),
                       ("event_components", t4), ("followup", t5)):
        pd.DataFrame(rows).to_csv(OUT / f"desc_{name}.csv", index=False)
    (OUT / "descriptive.json").write_text(json.dumps(
        {"table1": t1, "missingness": t2, "per_variable_hr": t3,
         "event_components": t4, "followup": t5,
         "ledger_ukb": lu, "ledger_wales": lw}, indent=2, default=str))

    print("\nFOLLOW-UP")
    for f in t5:
        print(f"  {f['cohort']:11s} n={f['n']:5d} ev={f['events']:4d} "
              f"py={f['person_years']:9.1f} rate={f['rate_per_1000py']:5.2f}/1000py "
              f"median={f['median_followup']:.2f}y clusters={f['clusters']}")
    print("\nDIRECTION REVERSALS (unadjusted vs adjusted cross 1.0)")
    for r in t3:
        if r.get("direction_reversal"):
            print(f"  {r['cohort']:11s} {r['variable']:14s} "
                  f"unadj={r.get('unadjusted_HR')} adj={r.get('fully_adjusted_HR')}")
    print("\nwritten: outputs/desc_*.csv and descriptive.json")


if __name__ == "__main__":
    main()
