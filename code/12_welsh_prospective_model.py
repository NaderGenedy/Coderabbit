#!/usr/bin/env python3
"""CALON-W: senior-author 7-variable incident model, clean Welsh prospective cohort.

Specification requested 10 Aug 2026:
    age, sex, cumulative cholesterol, TG/HDL-C, smoking, diabetes, hypertension

Fixes applied to the previous run, all of which materially changed the answer
-----------------------------------------------------------------------------
1. NO SILENT FOLD FAILURES. The earlier run wrapped the Cox fit in a bare
   `except: lp = 0`, which zeroed the linear predictor whenever the model failed to
   converge and dragged the C-index toward 0.5 (it reported 0.5613). Failures are now
   counted, reported, and the affected rows are EXCLUDED from the C-index rather than
   silently scored as zero.
2. MULTIPLE IMPUTATION, not median fill. Risk factors here are recorded preferentially
   in participants who had events (diabetes present in 58% of the cohort but covering
   77% of events; smoking 74% covering 87%). Median filling encodes that pattern.
   IterativeImputer is fitted on the training fold only and applied to the held-out fold.
3. ASCERTAINMENT STRATIFICATION restored. The baseline hazard is stratified by
   proband/cascade, as in CALON-A, so results are comparable with prior work.
4. GENUINELY RE-RANDOMISED REPEATS. Families are permuted per repeat before fold
   assignment; GroupKFold alone is deterministic and produced a repeat SD of exactly 0.
5. Paired differences carry family-cluster bootstrap intervals.

Governance: aggregate output only.
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
from lifelines.utils import concordance_index
from sklearn.experimental import enable_iterative_imputer  # noqa: F401
from sklearn.impute import IterativeImputer

warnings.filterwarnings("ignore")

ROOT = Path("${CALON_PROJECT_ROOT}")
OUT = ROOT / "outputs"
SEED = 20260810
REPEATS = 5
BOOT = 1000

spec = importlib.util.spec_from_file_location(
    "vw", ROOT / "code" / "audit_2026_08_10" / "07_verify_welsh_prospective.py")
vw = importlib.util.module_from_spec(spec)
sys.modules["vw"] = vw
spec.loader.exec_module(vw)

MODELS = {
    "age + sex": ["age", "male"],
    "age spline + sex": ["age", "age_sp18", "male"],
    "CALON-W (7 variable)": ["age", "age_sp18", "male", "chol_yrs", "log_tghdl",
                             "smoke", "dm", "htn"],
    "CALON-W, cumulative non-HDL": ["age", "age_sp18", "male", "cum_nonhdl", "log_tghdl",
                                    "smoke", "dm", "htn"],
    "CALON-W minus cumulative term": ["age", "age_sp18", "male", "log_tghdl",
                                      "smoke", "dm", "htn"],
    "CALON-W minus diabetes": ["age", "age_sp18", "male", "chol_yrs", "log_tghdl",
                               "smoke", "htn"],
    "Montreal variable set": ["age", "male", "hdl", "htn", "smoke"],
    "FH-RS variable set": ["age", "male", "ldl_unt", "hdl", "htn", "smoke"],
    "CALON-W + dated treatment": ["age", "age_sp18", "male", "chol_yrs", "log_tghdl",
                                 "smoke", "dm", "htn", "tx_base"],
}


def build():
    raw = pd.read_csv(vw.WALES, low_memory=False)
    _, active, incident, bage = vw.reconstruct_wales(raw)

    def num(c):
        if c not in raw:
            return pd.Series(np.nan, index=raw.index)
        s = raw[c].astype(str).str.strip().replace(
            {"": np.nan, "Unknown": np.nan, "NoValue": np.nan, "nan": np.nan})
        return pd.to_numeric(s, errors="coerce")

    ldl, hdl, tg = num("LDL.1"), num("HDL.1"), num("TRG.1")
    # Treated at baseline: ONLY a dated treatment start on/before the baseline measurement.
    # `OnTreatment` is undated (85.8% positive here) and would inflate untreated LDL-C to a
    # median of 8.29 mmol/L; the dated rule gives 7.1% treated and a median of 6.10, against
    # the archived 11% / 6.30. The archive's producing script is lost, so this is a documented
    # near-reproduction, not an exact one.
    bdate = vw.date(raw, "MeasurementDate.1")
    tdate = vw.date(raw, "Treatmentdate1")
    treated_baseline = (tdate.notna() & bdate.notna() & (tdate <= bdate)).astype(float)
    ldl_unt = np.where(treated_baseline.gt(0), ldl / 0.70, ldl)
    d = pd.DataFrame(index=raw.index)
    d["age"] = bage
    d["age_sp18"] = (bage - 18).clip(lower=0)
    d["male"] = raw["Gender"].astype(str).str[0].str.upper().eq("M").astype(float)
    d["ldl"], d["hdl"] = ldl, hdl
    d["log_tghdl"] = np.log((tg / hdl).where(lambda z: z > 0))
    d["ldl_unt"] = ldl_unt
    d["tx_base"] = treated_baseline
    # cholesterol-years on the UNTREATED scale, matching the archived construction
    d["chol_yrs"] = np.log((pd.Series(ldl_unt, index=raw.index) * bage).where(lambda z: z > 0))
    # cumulative non-HDL-C: (total cholesterol - HDL-C), back-calculated then x age
    tc = num("TC.1")
    nonhdl = (tc - hdl).where(lambda z: z.between(0.3, 20))
    nonhdl_unt = np.where(treated_baseline.gt(0), nonhdl / 0.70, nonhdl)
    d["nonhdl_unt"] = nonhdl_unt
    d["cum_nonhdl"] = np.log((pd.Series(nonhdl_unt, index=raw.index) * bage).where(lambda z: z > 0))
    sm, dm = num("Smoking"), num("Diabetes")
    d["smoke"] = sm.where(sm.isin([0, 1]))
    d["dm"] = dm.where(dm.isin([0, 1]))
    bpm, sbp, dbp = num("BloodPressureMedication"), num("BloodPressureSystolic"), num("BloodPressureDiastolic")
    d["htn"] = ((bpm.eq(1)) | (sbp.ge(140)) | (dbp.ge(90))).astype(float).where(
        bpm.notna() | sbp.notna() | dbp.notna())

    dob = vw.date(raw, "DOB").fillna(vw.date(raw, "DOB_1"))
    age_at = lambda c: (vw.date(raw, c) - dob).dt.total_seconds() / (365.25 * 86400.0)
    last = pd.concat([age_at("MeasurementDate.%d" % i) for i in (1, 2, 3, 4)]
                     + [age_at("BMIDate")], axis=1).max(axis=1)
    d["T"] = (num("AGE_AT_DECEASED").fillna(last) - bage).clip(lower=1 / 365.25)
    d["E"] = incident.astype(int)
    d["fam"] = raw["FamilyNumber"].astype(str)
    d["stratum"] = np.where(num("Proband").eq(1), "proband", "cascade")
    d = d.replace([np.inf, -np.inf], np.nan)
    return d.loc[active].reset_index(drop=True)


def cv(df, feats, strat=True, repeats=REPEATS, seed=SEED):
    """Out-of-fold linear predictor with MICE-style imputation; failures are counted."""
    y = df["E"].to_numpy(int)
    t = df["T"].to_numpy(float)
    fam = df["fam"].to_numpy()
    st = df["stratum"].to_numpy()
    n = len(df)
    acc = np.zeros(n)
    valid_acc = np.zeros(n, dtype=bool)
    cs, fails = [], 0
    for r in range(repeats):
        rng = np.random.default_rng(seed + r)
        uniq = pd.unique(pd.Series(fam))
        mp = dict(zip(uniq[rng.permutation(len(uniq))], range(len(uniq))))
        fold = np.array([mp[f] % 10 for f in fam])
        lp = np.full(n, np.nan)
        for k in range(10):
            tr, te = np.flatnonzero(fold != k), np.flatnonzero(fold == k)
            if y[tr].sum() < 5 or len(te) == 0:
                continue
            X = df.reindex(columns=feats).astype(float)
            imp = IterativeImputer(random_state=seed + r, sample_posterior=True,
                                   max_iter=10).fit(X.iloc[tr])
            Xtr = pd.DataFrame(imp.transform(X.iloc[tr]), columns=feats)
            Xte = pd.DataFrame(imp.transform(X.iloc[te]), columns=feats)
            for c in feats:
                if Xtr[c].nunique() > 2:
                    mu, sd = Xtr[c].mean(), Xtr[c].std()
                    Xtr[c] = (Xtr[c] - mu) / (sd if sd > 1e-9 else 1.0)
                    Xte[c] = (Xte[c] - mu) / (sd if sd > 1e-9 else 1.0)
            td = Xtr.copy()
            td["T"], td["E"] = t[tr], y[tr]
            use = strat and len(set(st[tr])) > 1
            if use:
                td["S"] = st[tr]
                Xte = Xte.copy()
                Xte["S"] = st[te]
            try:
                f = CoxPHFitter(penalizer=0.05).fit(td, "T", "E", strata=["S"] if use else None)
                lp[te] = np.log(f.predict_partial_hazard(Xte).to_numpy() + 1e-12)
            except Exception:
                fails += 1                      # counted, NOT zero-filled
        ok = ~np.isnan(lp)
        if ok.sum() > 50 and y[ok].sum() >= 10:
            cs.append(concordance_index(t[ok], -lp[ok], y[ok]))
            acc[ok] += lp[ok]
            valid_acc |= ok
    return (acc / max(repeats, 1), valid_acc, float(np.mean(cs)) if cs else np.nan,
            float(np.std(cs)) if cs else np.nan, fails)


def boot_delta(t, y, a, b, ok, fam, n=BOOT, seed=SEED):
    rng = np.random.default_rng(seed)
    t, y, a, b, fam = t[ok], y[ok], a[ok], b[ok], fam[ok]
    uniq = pd.unique(pd.Series(fam))
    idx = {f: np.flatnonzero(fam == f) for f in uniq}
    point = concordance_index(t, -a, y) - concordance_index(t, -b, y)
    vals = []
    for _ in range(n):
        take = np.concatenate([idx[f] for f in rng.choice(uniq, len(uniq), replace=True)])
        if y[take].sum() < 10:
            continue
        try:
            vals.append(concordance_index(t[take], -a[take], y[take])
                        - concordance_index(t[take], -b[take], y[take]))
        except Exception:
            continue
    return point, float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))


def run(df, label):
    y, t, fam = df["E"].to_numpy(int), df["T"].to_numpy(float), df["fam"].to_numpy()
    print("\n" + "=" * 96)
    print("%s   n=%d  events=%d  families=%d  median follow-up %.2f y"
          % (label, len(df), y.sum(), df["fam"].nunique(), np.median(t)))
    store, out = {}, {}
    for name, feats in MODELS.items():
        lp, ok, c, sd, fails = cv(df, feats)
        store[name] = (lp, ok)
        out[name] = {"features": feats, "c_index": c, "repeat_sd": sd,
                     "fold_failures": fails, "scored": int(ok.sum())}
    ref = "age + sex"
    print("%-34s %8s %7s %7s  %s" % ("model", "C-index", "repSD", "fails", "vs age+sex (95% CI)"))
    for name in MODELS:
        lp, ok = store[name]
        both = ok & store[ref][1]
        if name == ref:
            d = lo = hi = 0.0
        else:
            d, lo, hi = boot_delta(t, y, lp, store[ref][0], both, fam)
        out[name].update({"delta_vs_age_sex": d, "delta_ci": [lo, hi]})
        mark = "  WIN" if lo > 0 else ("  LOSS" if hi < 0 else "")
        print("%-34s %8.4f %7.4f %7d  %+0.4f (%+0.4f, %+0.4f)%s"
              % (name, out[name]["c_index"], out[name]["repeat_sd"],
                 out[name]["fold_failures"], d, lo, hi, mark))
    return out


def main():
    A = build()
    full = MODELS["CALON-W (7 variable)"]
    cc = A.dropna(subset=full).reset_index(drop=True)
    res = {"seed": SEED, "repeats": REPEATS, "participant_level_outputs": False,
           "full_cohort": run(A, "FULL COHORT (MICE inside folds)"),
           "complete_case": run(cc, "COMPLETE CASES for the 7-variable model")}
    (OUT / "welsh_prospective_model.json").write_text(json.dumps(res, indent=2))
    print("\nwritten:", OUT / "welsh_prospective_model.json")


if __name__ == "__main__":
    main()
