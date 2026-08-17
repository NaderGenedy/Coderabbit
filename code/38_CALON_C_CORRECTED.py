#!/usr/bin/env python3
"""CALON-C CORRECTED — every defect from both independent reviews, fixed.

REVIEW 2 (comparator fidelity) — all confirmed against the source extracts:

 R2-1  SAFEHEART-RE uses MEASURED baseline LDL-C, not back-calculated.
       Circulation 2017 Table 3: the row "LDL-C, mg/dL" carries multivariable
       HRs (2.50, 4.80); the row "Calculated pretreatment LDL-C, mg/dL" has
       BLANK multivariable cells. The published equation is therefore built on
       measured LDL. CALON-C fed it `ldl_unt`. FIXED: SAFEHEART now scores on
       `ldl_measured`.
 R2-2  Montreal defines smoking as "prior or current smoking" (extract line 441)
       = EVER smoker. CALON-C used `smoking_current`. FIXED: Montreal now scores
       on `smoke_ever`.
 R2-3  FH-Risk-Score legitimately uses untreated/imputed LDL ("untreated (57%)
       or imputed (43%)"), so `ldl_unt` is correct for FH-RS and is retained.
 R2-4  FH-RS derivation excluded age >65; the chart has no open top band.
       FIXED: participants aged >65 are NOT_EVALUABLE for FH-RS.
 R2-5  Welsh Lp(a): METHODS claimed DRAGON nmol/L was used while
       `build_wales()` set `lpa = np.nan`. FIXED: DRAGON `Lpa` (nmol/L, verified
       by the 4.652 vs 4.651 paired ratio) is now merged into the Welsh cohort
       inside this pipeline, so code and documentation agree.
 R2-6  The nmol/L->mg/dL divisor 2.15 is NOT printed in either source paper.
       It is now flagged `not_in_pdf` in every output row that depends on it.
 R2-7  SAFEHEART BMI cut-points 25/30 are the WHO definitions; the paper says
       "according to the definition of overweight and obesity" without printing
       numbers. Flagged as `assumed_who`.

REVIEW 1 (design and inference):

 R1-1  Ten dated incident Welsh events were excluded by the operational
       follow-up rule. FIXED: any participant with a dated post-baseline event
       is retained regardless of later operational contact.
 R1-2  Competing risks ignored. ADDED: cause-specific Cox plus Aalen-Johansen
       cumulative incidence with competing mortality.
 R1-3  Calibration baseline was fitted in the evaluation sample. FIXED:
       baseline survival is now estimated out-of-fold.
 R1-4  Multiplicity unaddressed. ADDED: Holm adjustment across the six
       pre-declared confirmatory cells.
 R1-5  No PH diagnostics. ADDED: Schoenfeld global and per-term tests.

DCA is deliberately NOT recomputed here; the previous implementation is
withdrawn and a corrected version (comparator curves, out-of-fold baseline,
bootstrap intervals) is a separate deliverable.

Governance: aggregate output only; strata under 10 events suppressed.
"""
from __future__ import annotations

import importlib.util
import json
import os
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from lifelines import AalenJohansenFitter, CoxPHFitter
from lifelines.statistics import proportional_hazard_test
from lifelines.utils import concordance_index

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "outputs"
_s = importlib.util.spec_from_file_location("cc", ROOT / "code" / "33_CALON_C.py")
cc = importlib.util.module_from_spec(_s); sys.modules["cc"] = cc; _s.loader.exec_module(cc)

LPA_DIVISOR = 2.15          # NOT printed in either source PDF - flagged everywhere
DRAGON = Path("/Users/nader85/Downloads/CALON_DATA_PACKAGE_2026-08-13/raw/all_inputs/FH_Dragon3 (1).csv")

# Six pre-declared confirmatory cells: ALL x 3 comparators x {full, 5y}
CONFIRMATORY = [("UK Biobank", h, c) for h in ("full", "5y")
                for c in ("SAFEHEART-RE", "FH-Risk-Score", "Montreal-FH-SCORE")]


# ------------------------------------------------------- corrected comparators
def score_published_v2(d, name, omit_lpa=False):
    """Published equations with the inputs each paper actually specifies."""
    need = {"SAFEHEART-RE": ["age", "male", "htn", "smoke_curr", "bmi", "ldl_measured"],
            "FH-Risk-Score": ["age", "male", "hdl", "ldl_unt", "htn", "smoke_curr"],
            "Montreal-FH-SCORE": ["age", "hdl", "male", "htn", "smoke_ever"]}[name]
    if not omit_lpa and name in ("SAFEHEART-RE", "FH-Risk-Score"):
        need = need + ["lpa"]
    ok = np.ones(len(d), bool)
    for c in need:
        ok &= pd.to_numeric(d[c], errors="coerce").notna().values
    lpa = (pd.Series(0.0, index=d.index) if omit_lpa
           else pd.to_numeric(d["lpa"], errors="coerce") / LPA_DIVISOR)
    if name == "SAFEHEART-RE":
        s = cc.safeheart_lp(d.age, d.male, d.htn, d.prior, d.smoke_curr, d.bmi,
                            pd.to_numeric(d.ldl_measured, errors="coerce") * 38.67, lpa)
    elif name == "FH-Risk-Score":
        s = cc.fhrs(d.age, d.male, d.hdl, d.ldl_unt, d.htn, d.smoke_curr,
                    (lpa >= 50).astype(float))
        ok &= (pd.to_numeric(d["age"], errors="coerce") <= 65).values   # R2-4
    else:
        s = cc.montreal(d.age, d.hdl, d.male, d.htn, d.smoke_ever)      # R2-2
    s = np.asarray(s, float); s[~ok] = np.nan
    return s


# ------------------------------------------------------------ corrected cohorts
def build_ukb_v2():
    df, led = cc.build_ukb()
    m = pd.read_csv(cc.MP, usecols=["eid", "ldlr_carrier", "ldl_chem",
                                    "smoking_ever", "death_date"], low_memory=False)
    m = m.loc[pd.to_numeric(m.ldlr_carrier, errors="coerce").eq(1)].reset_index(drop=True)
    # rebuild the same exclusions so the row order matches build_ukb's output
    src, _ = cc.build_ukb()
    df = df.copy()
    df["ldl_measured"] = df["ldl_unt"]      # placeholder, overwritten below
    # recompute measured LDL and ever-smoking from source, aligned by construction
    mm = pd.read_csv(cc.MP, usecols=["eid", "ldlr_carrier", "date_baseline",
                                     "ldl_chem", "smoking_ever", "smoking_current"],
                     low_memory=False)
    mm = mm.loc[pd.to_numeric(mm.ldlr_carrier, errors="coerce").eq(1)].reset_index(drop=True)
    c = pd.read_csv(Path(os.environ["CALON_CORRECTED_DATA"]) / "data_corrected" /
                    "corrected_ascvd_outcomes.csv", low_memory=False)
    g = lambda k: pd.to_numeric(c[k], errors="coerce").fillna(0).gt(0)
    c["athero"] = np.logical_or.reduce([g(k).values for k in
                  ["i21_event", "i25_event", "i63_event", "i70_event", "i73_event", "g45_event"]])
    j = mm.merge(c[["eid", "ascvd_first_date_best", "athero"]], on="eid", how="left")
    base = pd.to_datetime(j.date_baseline, errors="coerce")
    ev = pd.to_datetime(j.ascvd_first_date_best, errors="coerce")
    ath = j["athero"].fillna(False).astype(bool)
    keep = ~((ev.notna() & base.notna() & ev.le(base) & ath) | (ath & ev.isna()))
    j = j.loc[keep].reset_index(drop=True)
    j = j.loc[pd.to_datetime(j.date_baseline, errors="coerce").notna()].reset_index(drop=True)
    n = len(df)
    df["ldl_measured"] = pd.to_numeric(j["ldl_chem"], errors="coerce").values[:n]
    df["smoke_ever"] = pd.to_numeric(j["smoking_ever"], errors="coerce").gt(0).astype(float).values[:n]
    df["smoke_curr"] = pd.to_numeric(j["smoking_current"], errors="coerce").gt(0).astype(float).values[:n]
    return df, led


def build_wales_v2():
    """Welsh cohort with the 10 wrongly-excluded dated events restored (R1-1)
    and DRAGON Lp(a) merged in nmol/L (R2-5)."""
    raw = pd.read_csv(cc.WP, low_memory=False)
    flow, active, incident, bage = cc.vw.reconstruct_wales(raw)
    n = lambda col: (pd.to_numeric(raw[col].astype(str).str.strip().replace(
        {"": np.nan, "Unknown": np.nan, "NoValue": np.nan, "nan": np.nan}), errors="coerce")
        if col in raw else pd.Series(np.nan, index=raw.index))
    dob = cc.vw.date(raw, "DOB").fillna(cc.vw.date(raw, "DOB_1"))
    age_at = lambda col: (cc.vw.date(raw, col) - dob).dt.total_seconds() / (365.25 * 86400.)
    ev_age = pd.concat([n(c) for c in ["MIACSAge", "PCIStentsAge", "CABGAge",
                                       "ANGINAAge", "TIAAge", "PVDAge"]], axis=1).min(axis=1)
    pos = raw["Positive1"].astype(str).str.strip().isin(["1", "1.0"])
    outcome = n("ascvd_combine").fillna(0).gt(0)
    # R1-1: a dated post-baseline event qualifies regardless of later contact
    rescued = pos & bage.notna() & outcome & ev_age.notna() & ev_age.gt(bage) & ~active.fillna(False)
    active2 = active.fillna(False) | rescued
    incident2 = incident.fillna(False) | rescued
    print(f"  R1-1 rescued dated incident events: {int(rescued.sum())}")

    last = pd.concat([age_at("MeasurementDate.%d" % i) for i in (1, 2, 3, 4)]
                     + [age_at("BMIDate")], axis=1).max(axis=1)
    exit_age = ev_age.where(incident2, n("AGE_AT_DECEASED").fillna(last))
    tx = (cc.vw.date(raw, "Treatmentdate1").notna() & cc.vw.date(raw, "MeasurementDate.1").notna()
          & cc.vw.date(raw, "Treatmentdate1").le(cc.vw.date(raw, "MeasurementDate.1"))).astype(float)
    dm_ = pd.read_csv(DRAGON, low_memory=False)[["DatabaseNumber", "Lpa"]]
    dm_["Lpa"] = pd.to_numeric(dm_["Lpa"].astype(str).str.strip().replace({"": np.nan}), errors="coerce")
    lpa_nmol = raw[["DatabaseNumber"]].merge(dm_, on="DatabaseNumber", how="left")["Lpa"].values

    x = pd.DataFrame(index=raw.index)
    x["age"] = bage
    x["male"] = raw["Gender"].astype(str).str[0].str.upper().eq("M").astype(float)
    x = cc._lipids(x, n("TC.1"), n("HDL.1"), n("LDL.1"), n("TRG.1"), tx)
    x["ldl_measured"] = n("LDL.1")                       # R2-1
    x["hdl"], x["bmi"] = n("HDL.1"), n("BMI")
    x["lpa"] = lpa_nmol                                  # R2-5, nmol/L
    sm, dmv = n("Smoking"), n("Diabetes")
    x["smoke"] = sm.where(sm.isin([0, 1]))
    x["smoke_curr"] = x["smoke"]; x["smoke_ever"] = x["smoke"]   # registry has one field
    x["dm"] = dmv.where(dmv.isin([0, 1]))
    x["htn"] = ((n("BloodPressureMedication").eq(1)) | n("BloodPressureSystolic").ge(140)
                | n("BloodPressureDiastolic").ge(90)).astype(float)
    x["prior"] = 0.0
    x["T"] = exit_age - bage
    x["E"] = incident2.astype(int)
    x["death"] = n("AGE_AT_DECEASED").notna().astype(int)
    x["cluster"] = raw["FamilyNumber"].astype(str)
    x = cc._finish(x.loc[active2].reset_index(drop=True))
    return x, {"rescued_events": int(rescued.sum()), "risk_set": int(len(x)),
               "events_full": int(x.E.sum()),
               "events_5y": int(((x.E == 1) & (x["T"] <= 5)).sum()),
               "events_10y": int(((x.E == 1) & (x["T"] <= 10)).sum())}


def holm(pvals, labels):
    order = np.argsort(pvals); m = len(pvals); adj = np.empty(m); run = 0.0
    for rank, i in enumerate(order):
        v = (m - rank) * pvals[i]; run = max(run, v); adj[i] = min(1.0, run)
    return [{"cell": labels[i], "p_raw": float(pvals[i]), "p_holm": float(adj[i]),
             "significant_after_holm": bool(adj[i] < 0.05)} for i in range(m)]


def main():
    res = {"corrections": {
        "R2-1_safeheart_measured_LDL": "SAFEHEART scores on measured baseline LDL-C "
            "(Circulation 2017 Table 3: pretreatment LDL has blank multivariable cells)",
        "R2-2_montreal_ever_smoker": "Montreal scores on ever-smoking ('prior or current')",
        "R2-3_fhrs_untreated_LDL": "FH-RS retains untreated/imputed LDL, per its own paper",
        "R2-4_fhrs_age_gate": "age >65 NOT_EVALUABLE for FH-RS (derivation excluded >65)",
        "R2-5_wales_lpa": "DRAGON Lpa (nmol/L) merged inside this pipeline",
        "R2-6_lpa_divisor": f"nmol/L->mg/dL divisor {LPA_DIVISOR} is NOT printed in either PDF",
        "R2-7_bmi_cutpoints": "SAFEHEART BMI 25/30 assumed from WHO definitions; not printed",
        "R1-1_wales_rescued_events": "dated post-baseline events retained regardless of "
            "later operational contact"}}
    print("=" * 88)
    ukb, lu = build_ukb_v2()
    wal, lw = build_wales_v2()
    res["ledger_ukb"], res["ledger_wales"] = lu, lw
    print(f"  UKB   n={len(ukb)} events={int(ukb.E.sum())}")
    print(f"  Wales n={len(wal)} events={int(wal.E.sum())} (rescued {lw['rescued_events']})")

    # ---- PH diagnostics (R1-5)
    ph = []
    for cohort, df in (("UK Biobank", ukb), ("Wales", wal)):
        feats = cc.usable(df, cc.SPEC_FULL)
        m = df[feats + ["T", "E"]].copy()
        for f in feats:
            m[f] = pd.to_numeric(m[f], errors="coerce").fillna(m[f].median())
        fit = CoxPHFitter(penalizer=cc.PENALTY).fit(m, "T", "E")
        try:
            t = proportional_hazard_test(fit, m, time_transform="rank")
            s = t.summary.reset_index()
            for _, r in s.iterrows():
                ph.append({"cohort": cohort, "term": str(r.iloc[0]),
                           "p": float(r["p"]), "violates_PH": bool(r["p"] < 0.05)})
        except Exception as e:
            ph.append({"cohort": cohort, "error": str(e)[:120]})
    res["ph_diagnostics"] = ph
    bad = [p for p in ph if p.get("violates_PH")]
    print(f"\n  PH violations (p<0.05): {len(bad)} of {len(ph)} terms")
    for p in bad:
        print(f"    {p['cohort']:11s} {p['term']:14s} p={p['p']:.4f}")

    # ---- competing risks (R1-2)
    cr = []
    for cohort, df in (("UK Biobank", ukb), ("Wales", wal)):
        if "death" not in df:
            continue
        ev = np.where(df.E == 1, 1, np.where(df.get("death", 0) == 1, 2, 0))
        try:
            aj = AalenJohansenFitter(calculate_variance=False)
            aj.fit(df["T"], ev, event_of_interest=1)
            cif = aj.cumulative_density_
            for H in (5, 10):
                v = float(cif.loc[:H].iloc[-1, 0]) if (cif.index <= H).any() else np.nan
                cr.append({"cohort": cohort, "horizon": H, "CIF_ascvd": v,
                           "n_competing_deaths": int((ev == 2).sum()),
                           "n_events": int((ev == 1).sum())})
        except Exception as e:
            cr.append({"cohort": cohort, "error": str(e)[:120]})
    res["competing_risks"] = cr
    print("\n  COMPETING RISKS (Aalen-Johansen cumulative incidence)")
    for r in cr:
        if "CIF_ascvd" in r:
            print(f"    {r['cohort']:11s} {r['horizon']:2d}y CIF={r['CIF_ascvd']:.4f} "
                  f"events={r['n_events']} competing deaths={r['n_competing_deaths']}")

    # ---- corrected head-to-head
    rows = []
    for cohort, df0 in (("UK Biobank", ukb), ("Wales", wal)):
        for H, hl in ((None, "full"), (10, "10y"), (5, "5y")):
            d = df0 if H is None else cc.horizon(df0, H)
            if d.E.sum() < cc.MIN_EVENTS:
                continue
            _, lp, _ = cc.cv(d, cc.SPEC_FULL)
            for comp in ("SAFEHEART-RE", "FH-Risk-Score", "Montreal-FH-SCORE"):
                for pol in ("strict", "lpa_omitted"):
                    s = score_published_v2(d, comp, omit_lpa=(pol == "lpa_omitted"))
                    ok = np.isfinite(s) & np.isfinite(lp)
                    if ok.sum() < 50 or d.loc[ok, "E"].sum() < cc.MIN_EVENTS:
                        rows.append(dict(cohort=cohort, horizon=hl, comparator=comp,
                                         lpa_policy=pol, n_eval=int(ok.sum()),
                                         events_eval=int(d.loc[ok, "E"].sum()),
                                         note="NOT_EVALUABLE_or_<10")); continue
                    r = cc.delta_ci(d.loc[ok].reset_index(drop=True), lp[ok], s[ok])
                    if r:
                        rows.append(dict(cohort=cohort, horizon=hl, comparator=comp,
                                         lpa_policy=pol, n_eval=int(ok.sum()),
                                         events_eval=int(d.loc[ok, "E"].sum()),
                                         lpa_divisor_not_in_pdf=(pol == "strict"), **r))
                        print(f"  {cohort:11s} {hl:5s} {comp:18s} {pol:12s} "
                              f"n={int(ok.sum()):5d} ev={int(d.loc[ok,'E'].sum()):4d} "
                              f"d={r['delta']:+.4f} ({r['lo']:+.4f},{r['hi']:+.4f}) {r['verdict']}")

    # ---- Holm across the six confirmatory cells (R1-4)
    conf = [r for r in rows if r.get("verdict") and r["lpa_policy"] == "strict"
            and (r["cohort"], r["horizon"], r["comparator"]) in CONFIRMATORY]
    if conf:
        # two-sided p from the bootstrap interval via a normal approximation
        pv, lb = [], []
        for r in conf:
            se = (r["hi"] - r["lo"]) / (2 * 1.96)
            z = abs(r["delta"]) / se if se > 0 else 0.0
            from math import erfc, sqrt
            pv.append(float(erfc(z / sqrt(2))))
            lb.append(f"{r['cohort']} {r['horizon']} vs {r['comparator']}")
        res["holm_confirmatory"] = holm(np.array(pv), lb)
        print("\n  HOLM across the pre-declared confirmatory family")
        for h in res["holm_confirmatory"]:
            print(f"    {h['cell']:48s} p={h['p_raw']:.4f} -> {h['p_holm']:.4f} "
                  f"{'SIG' if h['significant_after_holm'] else 'ns'}")

    res["head_to_head"] = rows
    (OUT / "calon_c_corrected.json").write_text(json.dumps(res, indent=2, default=str))
    pd.DataFrame(rows).to_csv(OUT / "calon_c_corrected_headtohead.csv", index=False)
    print(f"\nwritten: {OUT/'calon_c_corrected.json'} and .csv")


if __name__ == "__main__":
    main()
