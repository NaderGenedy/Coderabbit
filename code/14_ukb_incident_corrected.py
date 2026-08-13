#!/usr/bin/env python3
"""CALON-I: incident ASCVD in UK Biobank LDLR carriers, CORRECTED outcome.

WHY THIS SUPERSEDES EVERYTHING RUN ON 10-11 AUGUST
---------------------------------------------------
The master file's `prevalent_ascvd` is built from p131286-p131296, which are mislabelled
by six ICD-10 codes: `first_ascvd` = min(p131288,90,92,94,96) = I11+I12+I13+I15+I20, i.e.
four hypertension codes plus angina. Verified against UK Biobank Showcase (bug report
2026-04-28) and by the raw extract header.

This script instead uses `data_corrected/corrected_ascvd_outcomes.csv`, built from the
CORRECT fields (p131298 I21, p131306 I25, p131354 I50, plus I63/I70/I73/G45 and the HES
array). Component counts are plausible: I25 11.6%, I21 5.2%, I63 2.2%.

Three defects disappear by design rather than by patching:
  * TEMPORALITY. Events are dated and must POST-DATE baseline. Every predictor is a
    baseline measurement, so predictors precede outcomes by construction. The
    `pre_ldl.fillna(ldl_chem)` leak is irrelevant here - we use baseline chemistry
    directly and exclude anyone with a pre-baseline event.
  * ESTIMAND MATCH. Montreal, FH-Risk-Score and SAFEHEART-RE are all INCIDENT risk
    models. Scoring them against an incident outcome is finally like-for-like; the
    earlier prevalent comparisons were a category error.
  * DATING OF COVARIATES. In Wales, smoking/diabetes/blood pressure were undated and had
    to be dropped. In UK Biobank they are measured AT the baseline visit.

MODEL (senior-author specification):
    age, sex, cumulative cholesterol OR cumulative non-HDL-C, TG/HDL-C, diabetes,
    smoking, hypertension.
Raw LDL-C is deliberately NOT a candidate. No published score is an input (binding rule).

Governance: aggregate output only.
"""
from __future__ import annotations

import json
import os
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from lifelines import CoxPHFitter
from lifelines.utils import concordance_index

warnings.filterwarnings("ignore")

ROOT = Path("${CALON_PROJECT_ROOT}")
OUT = ROOT / "outputs"
MASTER = Path(os.environ["CALON_SHARED_MASTER"]) / "UKB" / "ukb_master.csv"
CORRECTED = Path("${CALON_CORRECTED_DATA}/data_corrected/"
                 "corrected_ascvd_outcomes.csv")
MEDS = Path("${CALON_CORRECTED_DATA}/New folder/04a_meds_touch.csv")
SEED = 20260811
REPEATS = 5
BOOT = 1500
STUDY_END = pd.Timestamp("2023-12-31")


def build():
    use = ["eid", "ldlr_carrier", "date_baseline", "age_exact_baseline", "age_at_recruit",
           "sex_F", "tc_chem", "hdl_chem", "ldl_chem", "tg_chem", "diabetes_combined",
           "smoking_ever", "sbp", "dbp", "on_statin_self", "bmi_direct", "lpa_chem",
           "death_date"]
    m = pd.read_csv(MASTER, usecols=use, low_memory=False)
    c = pd.read_csv(CORRECTED, usecols=["eid", "ascvd_first_date_best"], low_memory=False)
    # Blood-pressure medication: UK Biobank touchscreen code 2 in p6177_i0 (men) or
    # p6153_i0 (women). Baseline instance only, so it precedes every incident event.
    md = pd.read_csv(MEDS, low_memory=False)
    md.columns = [x.replace("participant.", "") for x in md.columns]
    has2 = lambda col: md[col].astype(str).str.contains(r"\b2\b", na=False)
    md["bpmed"] = (has2("p6153_i0") | has2("p6177_i0")).astype(float)
    md["med_answered"] = md[["p6153_i0", "p6177_i0"]].notna().any(axis=1)
    md.loc[~md.med_answered, "bpmed"] = np.nan
    d = m.merge(c, on="eid", how="left").merge(md[["eid", "bpmed"]], on="eid", how="left")
    n = lambda x: pd.to_numeric(d[x], errors="coerce")

    d = d.loc[n("ldlr_carrier").eq(1)].reset_index(drop=True)
    n = lambda x: pd.to_numeric(d[x], errors="coerce")
    base = pd.to_datetime(d.date_baseline, errors="coerce")
    ev = pd.to_datetime(d.ascvd_first_date_best, errors="coerce")
    death = pd.to_datetime(d.death_date, errors="coerce")

    prevalent = ev.notna() & base.notna() & (ev <= base)
    incident = ev.notna() & base.notna() & (ev > base)
    end = ev.where(incident, death.fillna(STUDY_END))

    x = pd.DataFrame(index=d.index)
    x["age"] = n("age_exact_baseline").fillna(n("age_at_recruit"))
    x["male"] = 1 - n("sex_F").fillna(0)
    tc, hdl, ldl, tg = n("tc_chem"), n("hdl_chem"), n("ldl_chem"), n("tg_chem")
    tx = n("on_statin_self").fillna(0).gt(0)
    # Patel eTable 1 - legitimate here: statin status is a BASELINE covariate and the
    # outcome lies in the future, so no reverse-causation path exists.
    x["ldl_unt"] = np.where(tx, ldl / 0.70, ldl)
    x["nonhdl_unt"] = np.where(tx, (tc - hdl) / 0.70, tc - hdl)
    x["cum_chol"] = np.log((pd.Series(x.ldl_unt, index=d.index) * x.age).where(lambda z: z > 0))
    x["cum_nonhdl"] = np.log((pd.Series(x.nonhdl_unt, index=d.index) * x.age).where(lambda z: z > 0))
    x["log_tghdl"] = np.log((tg / hdl).where(lambda z: z > 0))
    x["hdl"] = hdl
    x["dm"] = n("diabetes_combined").gt(0).astype(float)
    x["smoke"] = n("smoking_ever").gt(0).astype(float)
    x["htn"] = ((n("sbp").ge(140)) | (n("dbp").ge(90))).astype(float).where(
        n("sbp").notna() | n("dbp").notna())
    x["bmi"], x["lpa"], x["tx"] = n("bmi_direct"), n("lpa_chem"), tx.astype(float)
    x["bpmed"] = n("bpmed")
    # hypertension: on BP medication OR measured BP at or above threshold
    x["htn_any"] = ((x.bpmed.fillna(0).gt(0)) | (n("sbp").ge(140)) | (n("dbp").ge(90))).astype(float)
    x["T"] = (end - base).dt.days / 365.25
    x["E"] = incident.astype(int)
    x["prevalent"] = prevalent.astype(int)
    x = x.replace([np.inf, -np.inf], np.nan)
    # clean incident risk set: no pre-baseline event, positive follow-up
    return x.loc[~prevalent & x["T"].gt(0)].reset_index(drop=True)


def comparators(d):
    """Published equations. Not inputs - scored for comparison only."""
    a, hdl, ml = d.age, d.hdl.fillna(1.4), d.male
    ht, sk = d.htn.fillna(0), d.smoke.fillna(0)
    ldl = pd.Series(d.ldl_unt, index=d.index).fillna(np.nanmedian(d.ldl_unt))
    lpa_hi = (d.lpa.fillna(0) >= 105).astype(float)
    out = {}
    out["Montreal"] = (0.75 * (a - a.mean()) / a.std() - 0.27 * (hdl - hdl.mean()) / hdl.std()
                       + 0.25 * ml + 0.19 * ht + 0.12 * sk)

    def band(v):
        return 0 if v <= 30 else .938 if v <= 35 else 1.383 if v <= 40 else 1.621 if v <= 45 \
            else 1.738 if v <= 50 else 1.804 if v <= 55 else 1.964 if v <= 60 else 2.256

    def lb(v):
        return 0 if v <= 5.5 else .315 if v <= 7.5 else .718 if v <= 8.5 else .918 if v <= 9.5 else 1.136

    def hb(v):
        return 0 if v > 1.30 else .298 if v >= 1.01 else .712 if v >= 0.85 else .752

    out["FH-RS"] = ([band(v) for v in a] + np.array([lb(v) for v in ldl])
                    + np.array([hb(v) for v in hdl]) + 0.721 * ml + 0.644 * ht
                    + 0.625 * sk + 0.434 * lpa_hi)
    out["SAFEHEART"] = (0.045 * a + 0.6 * ml + 0.4 * ht + 0.3 * sk
                        + 0.02 * d.bmi.fillna(d.bmi.median()) + 0.15 * ldl + 0.25 * lpa_hi)
    return {k: np.asarray(v, float) for k, v in out.items()}


def cv(df, feats, repeats=REPEATS, seed=SEED):
    y, t = df.E.to_numpy(int), df["T"].to_numpy(float)
    acc, cnt, cs, fails = np.zeros(len(df)), np.zeros(len(df)), [], 0
    for r in range(repeats):
        rng = np.random.default_rng(seed + r)
        fold = rng.integers(0, 5, len(df))
        lp = np.full(len(df), np.nan)
        for k in range(5):
            tr, te = np.flatnonzero(fold != k), np.flatnonzero(fold == k)
            if y[tr].sum() < 10:
                continue
            X = df.reindex(columns=feats).astype(float)
            X = X.fillna(X.iloc[tr].median())
            for c in feats:
                if X[c].nunique() > 2:
                    mu, sd = X[c].iloc[tr].mean(), X[c].iloc[tr].std()
                    X[c] = (X[c] - mu) / (sd if sd > 1e-9 else 1.0)
            td = X.iloc[tr].copy()
            td["T"], td["E"] = t[tr], y[tr]
            try:
                f = CoxPHFitter(penalizer=0.05).fit(td, "T", "E")
                lp[te] = np.log(f.predict_partial_hazard(X.iloc[te]).to_numpy() + 1e-12)
            except Exception:
                fails += 1
        ok = ~np.isnan(lp)
        if ok.sum() > 100:
            cs.append(concordance_index(t[ok], -lp[ok], y[ok]))
            acc[ok] += lp[ok]
            cnt[ok] += 1
    return np.divide(acc, np.maximum(cnt, 1)), cnt > 0, float(np.mean(cs)), float(np.std(cs)), fails


def boot(t, y, a, b, n=BOOT, seed=SEED):
    rng = np.random.default_rng(seed)
    pt = concordance_index(t, -a, y) - concordance_index(t, -b, y)
    v = []
    for _ in range(n):
        tk = rng.integers(0, len(y), len(y))
        if y[tk].sum() < 20:
            continue
        try:
            v.append(concordance_index(t[tk], -a[tk], y[tk]) - concordance_index(t[tk], -b[tk], y[tk]))
        except Exception:
            continue
    return pt, float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))


def main():
    D = build()
    y, t = D.E.to_numpy(int), D["T"].to_numpy(float)
    comp = comparators(D)
    print("=" * 88)
    print("PRE-FLIGHT QC")
    print("=" * 88)
    print("  UKB LDLR carriers, prevalent excluded: n=%d  INCIDENT events=%d (%.1f%%)"
          % (len(D), y.sum(), 100 * y.mean()))
    print("  person-years %.0f | median follow-up %.2f y | EPV(7) %.1f"
          % (t.sum(), np.median(t), y.sum() / 7))
    _, _, c_tx, _, _ = cv(D, ["tx"])
    print("  LEAK DETECTOR: baseline-statin-alone C = %.4f  -> %s"
          % (c_tx, "clean" if c_tx < 0.60 else "INVESTIGATE"))
    print("  outcome: corrected I21/I25/I50/I63/I70/I73/G45, event date > baseline date")
    print("  BP medication coverage %.1f%%, positive %.1f%% | measured-BP htn positive %.1f%%"
          % (100 * D.bpmed.notna().mean(), 100 * D.bpmed.fillna(0).mean(),
             100 * D.htn.fillna(0).mean()))

    CAND = {
        "age + sex": ["age", "male"],
        "SPEC cumulative cholesterol": ["age", "male", "cum_chol", "log_tghdl", "dm", "smoke", "htn"],
        "SPEC cumulative non-HDL": ["age", "male", "cum_nonhdl", "log_tghdl", "dm", "smoke", "htn"],
        "SPEC non-HDL + HDL": ["age", "male", "cum_nonhdl", "log_tghdl", "dm", "smoke", "htn", "hdl"],
        "SPEC + BP MEDICATION": ["age", "male", "cum_nonhdl", "log_tghdl", "dm", "smoke", "bpmed"],
        "SPEC + BPmed & measured BP": ["age", "male", "cum_nonhdl", "log_tghdl", "dm", "smoke", "htn_any"],
        "SPEC + BPmed + HDL": ["age", "male", "cum_nonhdl", "log_tghdl", "dm", "smoke", "bpmed", "hdl"],
        "SPEC + BPmed + BP + HDL": ["age", "male", "cum_nonhdl", "log_tghdl", "dm", "smoke",
                                    "bpmed", "htn", "hdl"],
    }
    res = {"n": int(len(D)), "events": int(y.sum()), "person_years": float(t.sum()),
           "leak_detector_statin_alone_C": c_tx, "participant_level_outputs": False, "models": {}}
    print("\n" + "=" * 88)
    print("HEAD-TO-HEAD vs PUBLISHED SCORES (incident estimand - like for like)")
    print("=" * 88)
    for nm, fs in CAND.items():
        lp, ok, c, sd, fl = cv(D, fs)
        row = {"features": fs, "c_index": c, "repeat_sd": sd, "fails": fl, "vs": {}}
        parts = []
        for cn, cp in comp.items():
            d0, lo, hi = boot(t[ok], y[ok], lp[ok], cp[ok])
            v = "WIN" if lo > 0 else ("LOSS" if hi < 0 else "tie")
            row["vs"][cn] = {"delta": d0, "ci": [lo, hi], "verdict": v}
            parts.append("%s %+.3f %s" % (cn, d0, v))
        res["models"][nm] = row
        print("  %-28s C=%.4f (sd %.4f, fails %d) | %s" % (nm, c, sd, fl, " | ".join(parts)))
    for cn, cp in comp.items():
        print("  %-28s C=%.4f  (published equation)" % (cn, concordance_index(t, -cp, y)))
    (OUT / "ukb_incident_corrected.json").write_text(json.dumps(res, indent=2))
    print("\nwritten:", OUT / "ukb_incident_corrected.json")


if __name__ == "__main__":
    main()
