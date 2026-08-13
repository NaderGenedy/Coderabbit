#!/usr/bin/env python3
"""CALON-S13: the model that survives every defect found on 10-11 August 2026.

DESIGN RULES, each traceable to a specific defect
-------------------------------------------------
R1  UK Biobank is EXCLUDED. Its outcome fields p131286-p131296 are mislabelled by six
    ICD-10 codes; `first_ascvd` = min(p131288,90,92,94,96) = I11+I12+I13+I15+I20, i.e.
    four hypertension codes plus angina. `prevalent_ascvd` is not ASCVD.
R2  TIME-TO-EVENT IS CORRECT. Cases get (event age - baseline age); non-cases get
    (censor age - baseline age). The previous script gave cases their censoring time,
    inflating case follow-up by a median 3.7 years and discarding half the usable pairs.
R3  ONLY DATED PRE-BASELINE PREDICTORS. Hypertension (8.1% dated on/before baseline),
    smoking (undated) and diabetes (DiabetesYear 2.5%) are EXCLUDED. Baseline-visit
    lipids qualify because MeasurementDate.1 IS the baseline.
R4  NO SPLINE KNOT WITHOUT A COLLINEARITY CHECK. age_sp18 is admitted only if it is not
    a linear duplicate of age in this cohort.
R5  LEAK DETECTOR RUN EXPLICITLY. If treatment status alone out-discriminates the model,
    the model is a treatment marker. This one test would have caught the UKB failure.
R6  REPRODUCIBLE. Everything is in this file; nothing computed in an ad-hoc shell.
R7  Cluster count reported as Kish effective N, not the nominal family count.

Published comparators are NOT scored: Montreal needs hypertension and smoking, FH-RS adds
Lp(a), SAFEHEART adds BMI - none available with pre-baseline dating. That no published FH
score can be honestly evaluated on clean prospective data is itself a finding, not a gap
to paper over.

Governance: aggregate output only.
"""
from __future__ import annotations

import os

import importlib.util
import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from lifelines import CoxPHFitter
from lifelines.utils import concordance_index

warnings.filterwarnings("ignore")

ROOT = Path(os.environ["CALON_PROJECT_ROOT"])
OUT = ROOT / "outputs"
SEED = 20260811
REPEATS = 10
BOOT = 2000

spec = importlib.util.spec_from_file_location(
    "vw", ROOT / "code" / "audit_2026_08_10" / "07_verify_welsh_prospective.py")
vw = importlib.util.module_from_spec(spec)
sys.modules["vw"] = vw
spec.loader.exec_module(vw)


def build():
    raw = pd.read_csv(vw.WALES, low_memory=False)
    _, active, incident, bage = vw.reconstruct_wales(raw)

    def num(c):
        if c not in raw:
            return pd.Series(np.nan, index=raw.index)
        s = raw[c].astype(str).str.strip().replace(
            {"": np.nan, "Unknown": np.nan, "NoValue": np.nan, "nan": np.nan})
        return pd.to_numeric(s, errors="coerce")

    dob = vw.date(raw, "DOB").fillna(vw.date(raw, "DOB_1"))
    age_at = lambda c: (vw.date(raw, c) - dob).dt.total_seconds() / (365.25 * 86400.0)

    # ---- R2: event age for cases, censor age for everyone else -------------
    event_age = pd.concat([num(c) for c in ["MIACSAge", "PCIStentsAge", "CABGAge",
                                            "ANGINAAge", "TIAAge", "PVDAge"]],
                          axis=1).min(axis=1)
    last = pd.concat([age_at("MeasurementDate.%d" % i) for i in (1, 2, 3, 4)]
                     + [age_at("BMIDate")], axis=1).max(axis=1)
    censor_age = num("AGE_AT_DECEASED").fillna(last)
    exit_age = event_age.where(incident, censor_age)

    ldl, hdl, tg, tc = num("LDL.1"), num("HDL.1"), num("TRG.1"), num("TC.1")
    bdate, tdate = vw.date(raw, "MeasurementDate.1"), vw.date(raw, "Treatmentdate1")
    treated = (tdate.notna() & bdate.notna() & (tdate <= bdate)).astype(float)
    ldl_unt = np.where(treated.gt(0), ldl / 0.70, ldl)
    nonhdl = (tc - hdl).where(lambda z: z.between(0.3, 20))

    d = pd.DataFrame(index=raw.index)
    d["age"] = bage
    d["age_sp18"] = (bage - 18).clip(lower=0)
    d["male"] = raw["Gender"].astype(str).str[0].str.upper().eq("M").astype(float)
    d["ldl_unt"] = ldl_unt
    d["hdl"] = hdl
    d["log_tghdl"] = np.log((tg / hdl).where(lambda z: z > 0))
    d["nonhdl"] = nonhdl
    d["tx"] = treated
    d["T"] = (exit_age - bage)
    d["E"] = incident.astype(int)
    d["fam"] = raw["FamilyNumber"].astype(str)
    d["stratum"] = np.where(num("Proband").eq(1), "proband", "cascade")
    d = d.replace([np.inf, -np.inf], np.nan)
    return d.loc[active & d["T"].gt(0)].reset_index(drop=True)


def cv(df, feats, repeats=REPEATS, seed=SEED):
    y, t = df["E"].to_numpy(int), df["T"].to_numpy(float)
    fam, st = df["fam"].to_numpy(), df["stratum"].to_numpy()
    acc, cnt, cs, fails = np.zeros(len(df)), np.zeros(len(df)), [], 0
    for r in range(repeats):
        rng = np.random.default_rng(seed + r)
        u = pd.unique(pd.Series(fam))
        mp = dict(zip(u[rng.permutation(len(u))], range(len(u))))
        fold = np.array([mp[f] % 10 for f in fam])
        lp = np.full(len(df), np.nan)
        for k in range(10):
            tr, te = np.flatnonzero(fold != k), np.flatnonzero(fold == k)
            if y[tr].sum() < 5 or len(te) == 0:
                continue
            X = df.reindex(columns=feats).astype(float)
            X = X.fillna(X.iloc[tr].median())
            for c in feats:
                if X[c].nunique() > 2:
                    mu, sd = X[c].iloc[tr].mean(), X[c].iloc[tr].std()
                    X[c] = (X[c] - mu) / (sd if sd > 1e-9 else 1.0)
            td = X.iloc[tr].copy()
            td["T"], td["E"], td["S"] = t[tr], y[tr], st[tr]
            xe = X.iloc[te].copy()
            xe["S"] = st[te]
            try:
                f = CoxPHFitter(penalizer=0.05).fit(td, "T", "E", strata=["S"])
                lp[te] = np.log(f.predict_partial_hazard(xe).to_numpy() + 1e-12)
            except Exception:
                fails += 1
        ok = ~np.isnan(lp)
        if ok.sum() > 50:
            cs.append(concordance_index(t[ok], -lp[ok], y[ok]))
            acc[ok] += lp[ok]
            cnt[ok] += 1
    return np.divide(acc, np.maximum(cnt, 1)), cnt > 0, float(np.mean(cs)), float(np.std(cs)), fails


def boot(t, y, a, b, ok, fam, n=BOOT, seed=SEED):
    rng = np.random.default_rng(seed)
    t_, y_, a_, b_, f_ = t[ok], y[ok], a[ok], b[ok], fam[ok]
    u = pd.unique(pd.Series(f_))
    idx = {f: np.flatnonzero(f_ == f) for f in u}
    pt = concordance_index(t_, -a_, y_) - concordance_index(t_, -b_, y_)
    v = []
    for _ in range(n):
        tk = np.concatenate([idx[f] for f in rng.choice(u, len(u), replace=True)])
        if y_[tk].sum() < 8:
            continue
        try:
            v.append(concordance_index(t_[tk], -a_[tk], y_[tk])
                     - concordance_index(t_[tk], -b_[tk], y_[tk]))
        except Exception:
            continue
    return pt, float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))


def main():
    D = build()
    y, t, fam = D["E"].to_numpy(int), D["T"].to_numpy(float), D["fam"].to_numpy()
    res = {"seed": SEED, "cohort": "All-Wales PASS, genotype-confirmed, incident ASCVD",
           "n": int(len(D)), "events": int(y.sum()), "families": int(D.fam.nunique()),
           "person_years": float(t.sum()), "median_followup": float(np.median(t)),
           "participant_level_outputs": False, "prechecks": {}, "models": {}}

    print("=" * 84)
    print("PRE-FLIGHT QC — the battery that would have caught today's failures")
    print("=" * 84)
    print("  n=%d  events=%d  families=%d  person-years=%.0f  median follow-up %.2f y"
          % (len(D), y.sum(), D.fam.nunique(), t.sum(), np.median(t)))
    # R2 evidence
    print("  R2 correct time: case median T %.2f y vs non-case %.2f y"
          % (np.median(t[y == 1]), np.median(t[y == 0])))
    # R7 Kish effective clusters
    sz = D.groupby("fam").size().to_numpy()
    kish = sz.sum() ** 2 / (sz ** 2).sum()
    res["prechecks"]["kish_effective_clusters"] = float(kish)
    print("  R7 clusters: nominal %d, Kish effective %.1f, largest holds %.1f%%"
          % (D.fam.nunique(), kish, 100 * sz.max() / sz.sum()))
    # R4 collinearity
    r = np.corrcoef(D.age, D.age_sp18)[0, 1]
    res["prechecks"]["corr_age_agesp18"] = float(r)
    keep_spline = abs(r) < 0.999
    print("  R4 corr(age, age_sp18) = %.6f -> spline %s"
          % (r, "ADMITTED" if keep_spline else "REJECTED as duplicate"))
    # R5 leak detector
    lp_tx, ok_tx, c_tx, _, _ = cv(D, ["tx"])
    res["prechecks"]["treatment_alone_C"] = c_tx
    print("  R5 leak detector: treatment-status-alone C = %.4f" % c_tx)
    # univariable
    print("\n  univariable C (age as covariate, ascertainment-stratified):")
    for f in ["age", "male", "ldl_unt", "hdl", "log_tghdl", "nonhdl", "tx"]:
        _, _, c1, _, _ = cv(D, [f])
        res["prechecks"]["univariable_C_%s" % f] = c1
        print("     %-10s %.4f" % (f, c1))

    BASE = ["age", "male"] + (["age_sp18"] if keep_spline else [])
    CAND = {
        "age + sex": BASE,
        "+ untreated LDL-C": BASE + ["ldl_unt"],
        "+ HDL-C": BASE + ["hdl"],
        "+ TG/HDL-C": BASE + ["log_tghdl"],
        "+ non-HDL-C": BASE + ["nonhdl"],
        "+ untreated LDL + HDL": BASE + ["ldl_unt", "hdl"],
        "+ LDL + HDL + TG/HDL": BASE + ["ldl_unt", "hdl", "log_tghdl"],
        "+ LDL + HDL + treatment": BASE + ["ldl_unt", "hdl", "tx"],
    }
    print("\n" + "=" * 84)
    print("MODELS — dated pre-baseline predictors only")
    print("=" * 84)
    print("  %-26s %8s %7s %6s  %s" % ("model", "C-index", "repSD", "fails", "vs age+sex (95% CI)"))
    store = {}
    for nm, fs in CAND.items():
        lp, ok, c, sd, fl = cv(D, fs)
        store[nm] = (lp, ok)
        d0 = lo = hi = 0.0
        if nm != "age + sex":
            both = ok & store["age + sex"][1]
            d0, lo, hi = boot(t, y, lp, store["age + sex"][0], both, fam)
        res["models"][nm] = {"features": fs, "c_index": c, "repeat_sd": sd,
                             "fold_failures": fl, "delta": d0, "ci": [lo, hi]}
        mark = "  WIN" if lo > 0 else ("  LOSS" if hi < 0 else "")
        print("  %-26s %8.4f %7.4f %6d  %+0.4f (%+0.4f, %+0.4f)%s"
              % (nm, c, sd, fl, d0, lo, hi, mark))

    # coefficient signs on the best lipid model
    best = max((k for k in CAND if k != "age + sex"), key=lambda k: res["models"][k]["c_index"])
    fs = CAND[best]
    X = D.reindex(columns=fs).astype(float)
    X = X.fillna(X.median())
    for c in fs:
        if X[c].nunique() > 2:
            X[c] = (X[c] - X[c].mean()) / max(X[c].std(), 1e-9)
    X["T"], X["E"], X["S"] = t, y, D.stratum.to_numpy()
    fit = CoxPHFitter(penalizer=0.05).fit(X, "T", "E", strata=["S"])
    print("\n  coefficient signs, best lipid model (%s):" % best)
    signs = {}
    for term in fit.params_.index:
        hr = float(np.exp(fit.params_[term]))
        signs[term] = hr
        print("     %-12s HR per SD %.3f %s" % (term, hr, "" if term in ("age", "age_sp18", "male") else
                                                ("<- expected direction" if
                                                 (term in ("ldl_unt", "log_tghdl", "nonhdl") and hr > 1)
                                                 or (term in ("hdl", "tx") and hr < 1) else "<- WRONG SIGN")))
    res["best_model_hr_per_sd"] = signs
    res["best_model"] = best
    (OUT / "survivable_model.json").write_text(json.dumps(res, indent=2))
    print("\nwritten:", OUT / "survivable_model.json")


if __name__ == "__main__":
    main()
