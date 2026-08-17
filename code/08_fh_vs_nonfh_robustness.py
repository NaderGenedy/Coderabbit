#!/usr/bin/env python3
"""Robustness of the FH vs matched non-FH result (UK Biobank arm).

Checks
------
R1  Bootstrap confidence intervals on the expected:observed ratios, so the
    calibration reversal is reported with uncertainty rather than as a point.
R2  Matching sensitivity: ratio 1:1 / 1:3 / 1:5 and calliper 0.5 / 1 / 2 years,
    plus an alternative seed, to confirm the direction is not a matching artefact.
R3  Do the published FH-specific scores discriminate in non-FH? If Montreal-FH-
    SCORE and the FH-Risk-Score work equally well in matched non-carriers, their
    discrimination is not FH-specific either.
R4  Complete-case restriction, to confirm median completion is not driving it.

Governance: aggregate output only.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

ROOT = Path("/Users/nader85/Documents/CALON/calon_discordance_model_2026_08_09")
OUT = ROOT / "outputs"
SEED = 20260810

spec = importlib.util.spec_from_file_location("fhnf", ROOT / "code" / "07_fh_vs_nonfh.py")
f = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = f
spec.loader.exec_module(f)

CALON_N = f.CALON_N


def eo_ci(y, p, b=2000, seed=SEED):
    y, p = np.asarray(y, float), np.asarray(p, float)
    rng = np.random.default_rng(seed)
    vals = []
    for _ in range(b):
        take = rng.integers(0, len(y), len(y))
        obs = y[take].mean()
        if obs > 0:
            vals.append(p[take].mean() / obs)
    return float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))


def build():
    """Rebuild the UK Biobank FH frame and the non-carrier pool once."""
    cohorts = f.m.prepare_cohorts()
    fh = cohorts["ukb_strict"].copy()
    fh["log_ratio"] = np.log((fh["apob"] / fh["ldl"]).where(lambda z: z.gt(0)))
    fh["log_apoa1"] = np.log(fh["apoa1"])

    use = ["eid", "ldlr_carrier", "prevalent_ascvd", "age_exact_baseline", "age_at_recruit",
           "sex_F", "diabetes_combined", "smoking_ever", "sbp", "dbp", "pre_tc", "tc_chem",
           "pre_ldl", "ldl_chem", "pre_hdl", "hdl_chem", "pre_tg", "tg_chem", "apob",
           "apob_chem", "apo_a1", "pre_lpa", "lpa_chem", "on_statin_self", "bmi_direct"]
    raw = pd.read_csv(f.UKB, usecols=use, low_memory=False)
    raw = raw.loc[f.num(raw, "ldlr_carrier").fillna(0).ne(1)].reset_index(drop=True)
    n = f.num
    b = f.bounded
    x = pd.DataFrame(index=raw.index)
    x["age"] = b(n(raw, "age_exact_baseline").fillna(n(raw, "age_at_recruit")), 5, 105)
    x["male"] = 1 - n(raw, "sex_F").fillna(0)
    dia, smk = n(raw, "diabetes_combined"), n(raw, "smoking_ever")
    x["diabetes"] = dia.gt(0).astype(float).where(dia.notna())
    x["smoke_ever"] = smk.gt(0).astype(float).where(smk.notna())
    sbp, dbp = b(n(raw, "sbp"), 70, 260), b(n(raw, "dbp"), 35, 160)
    x["hypertension"] = (sbp.ge(140) | dbp.ge(90)).astype(float).where(sbp.notna() | dbp.notna())
    x["sbp10"] = sbp / 10.0
    x["tc"] = b(n(raw, "pre_tc").fillna(n(raw, "tc_chem")), 1.5, 25)
    x["ldl"] = b(n(raw, "pre_ldl").fillna(n(raw, "ldl_chem")), 0.3, 20)
    x["hdl"] = b(n(raw, "pre_hdl").fillna(n(raw, "hdl_chem")), 0.2, 5)
    x["tg"] = b(n(raw, "pre_tg").fillna(n(raw, "tg_chem")), 0.2, 25)
    x["apob"] = b(n(raw, "apob").fillna(n(raw, "apob_chem")), 0.2, 4)
    x["apoa1"] = b(n(raw, "apo_a1"), 0.3, 4)
    x["lpa"] = b(n(raw, "pre_lpa").fillna(n(raw, "lpa_chem")), 0, 1000)
    x["log_ratio"] = np.log((x["apob"] / x["ldl"]).where(lambda z: z.gt(0)))
    x["log_apoa1"] = np.log(x["apoa1"])
    x["log_lpa"] = np.log1p(x["lpa"])
    x["treatment"] = n(raw, "on_statin_self").fillna(0).gt(0).astype(float)
    x["y"] = n(raw, "prevalent_ascvd").fillna(0).gt(0).astype(int)
    x = x.loc[x["age"].notna()].reset_index(drop=True)
    return fh, x


def _terms(d):
    g = lambda c, fb: (pd.to_numeric(d[c], errors="coerce") if c in d
                       else pd.Series(fb, index=d.index))
    age = g("age", np.nan)
    hdl = g("hdl", np.nan).fillna(1.35)
    ldl = g("ldl", np.nan)
    return (age.fillna(age.median()), hdl, ldl.fillna(ldl.median()),
            g("male", 0).fillna(0), g("hypertension", 0).fillna(0),
            g("smoke_ever", 0).fillna(0), g("lpa", 0).fillna(0))


def montreal(d):
    """Montreal-FH-SCORE, published coefficients (Paquette 2017).

    CORRECTED 13 August 2026. This function previously used invented weights
    (age + 10*male - 10*HDL + 5*hypertension + 5*smoking) while its docstring
    claimed an Lp(a) term it never contained. Montreal has no Lp(a) term; the
    published model is age and HDL-C standardised, plus sex, hypertension and
    smoking. code/16_R3_comparator_recheck.py scores both versions side by side:
    the correction moved AUC by <=0.007 and left the R3 verdict unchanged.
    """
    age, hdl, _, male, htn, smoke, _ = _terms(d)
    return np.asarray(0.75 * (age - age.mean()) / age.std()
                      - 0.27 * (hdl - hdl.mean()) / hdl.std()
                      + 0.25 * male + 0.19 * htn + 0.12 * smoke, float)


def fhrs(d):
    """FH-Risk-Score, published banded coefficients (Paquette 2021).

    CORRECTED 13 August 2026; the previous form used invented linear weights.
    Age, LDL-C and HDL-C enter as published bands, not linear terms, and Lp(a)
    enters as a threshold indicator at 105 nmol/L.
    """
    age, hdl, ldl, male, htn, smoke, lpa = _terms(d)
    ab = lambda v: (0 if v <= 30 else .938 if v <= 35 else 1.383 if v <= 40 else 1.621 if v <= 45
                    else 1.738 if v <= 50 else 1.804 if v <= 55 else 1.964 if v <= 60 else 2.256)
    lb = lambda v: (0 if v <= 5.5 else .315 if v <= 7.5 else .718 if v <= 8.5
                    else .918 if v <= 9.5 else 1.136)
    hb = lambda v: (0 if v > 1.30 else .298 if v >= 1.01 else .712 if v >= 0.85 else .752)
    return np.asarray(np.array([ab(v) for v in age]) + np.array([lb(v) for v in ldl])
                      + np.array([hb(v) for v in hdl]) + 0.721 * male + 0.644 * htn
                      + 0.625 * smoke + 0.434 * (lpa >= 105).astype(float), float)


def main():
    fh, pool = build()
    out = {"seed": SEED, "participant_level_outputs": False}

    # ---------------- R1 primary matched sets with E:O intervals -------------
    keep, ctrl = f.match(fh["age"].to_numpy(float), fh["male"].to_numpy(float), pool, 5, 1.0, SEED)
    fh_m = fh.iloc[keep].reset_index(drop=True)
    b_fh, b_nf = f.fit(fh_m, CALON_N), f.fit(ctrl, CALON_N)

    p_nf = f.predict(b_fh, ctrl)
    p_fh = f.predict(b_nf, fh_m)
    r1 = {}
    for tag, y, p in [("fh_to_nonfh", ctrl["y"].to_numpy(int), p_nf),
                      ("nonfh_to_fh", fh_m["y"].to_numpy(int), p_fh)]:
        c = f.calib(y, p)
        lo, hi = eo_ci(y, p)
        r1[tag] = {"auc": float(roc_auc_score(y, p)), "E_O": c["E_O"], "E_O_ci": [lo, hi],
                   "expected_pct": 100 * c["expected"], "observed_pct": 100 * c["observed"]}
    out["R1_calibration_with_intervals"] = r1

    # ---------------- R2 matching sensitivity -------------------------------
    r2 = []
    for ratio in (1, 3, 5):
        for cal in (0.5, 1.0, 2.0):
            for seed in (SEED, SEED + 7):
                k, c = f.match(fh["age"].to_numpy(float), fh["male"].to_numpy(float),
                               pool, ratio, cal, seed)
                fm = fh.iloc[k].reset_index(drop=True)
                if len(fm) < 200 or c["y"].sum() < 20:
                    continue
                bf, bn = f.fit(fm, CALON_N), f.fit(c, CALON_N)
                cal_nf = f.calib(c["y"].to_numpy(int), f.predict(bf, c))
                cal_fh = f.calib(fm["y"].to_numpy(int), f.predict(bn, fm))
                a, b_ = fm["y"].sum(), len(fm) - fm["y"].sum()
                cc, d = c["y"].sum(), len(c) - c["y"].sum()
                r2.append({"ratio": ratio, "calliper": cal, "seed": seed,
                           "n_fh": int(len(fm)), "n_nonfh": int(len(c)),
                           "prev_fh_pct": float(100 * fm["y"].mean()),
                           "prev_nonfh_pct": float(100 * c["y"].mean()),
                           "or_fh": float((a * d) / (b_ * cc)) if b_ * cc else None,
                           "EO_fh_to_nonfh": cal_nf["E_O"], "EO_nonfh_to_fh": cal_fh["E_O"]})
    out["R2_matching_sensitivity"] = r2

    # ---------------- R3 do FH-specific scores work in non-FH? --------------
    r3 = {}
    for lbl, fn in [("Montreal_adapted", montreal), ("FH_Risk_Score_adapted", fhrs)]:
        r3[lbl] = {"auc_in_FH": float(roc_auc_score(fh_m["y"].to_numpy(int), fn(fh_m))),
                   "auc_in_matched_nonFH": float(roc_auc_score(ctrl["y"].to_numpy(int), fn(ctrl)))}
    r3["CALON_N_developed_in_FH"] = {
        "auc_in_FH": float(roc_auc_score(fh_m["y"].to_numpy(int), f.predict(b_fh, fh_m))),
        "auc_in_matched_nonFH": float(roc_auc_score(ctrl["y"].to_numpy(int), p_nf))}
    out["R3_score_discrimination_by_genotype"] = r3

    # ---------------- R4 complete cases -------------------------------------
    need = ["age", "male", "hdl", "hypertension", "smoke_ever", "apob", "ldl", "apoa1"]
    cfh = fh_m.dropna(subset=[c for c in need if c in fh_m]).reset_index(drop=True)
    cnf = ctrl.dropna(subset=[c for c in need if c in ctrl]).reset_index(drop=True)
    if len(cfh) > 100 and cnf["y"].sum() > 20:
        bf, bn = f.fit(cfh, CALON_N), f.fit(cnf, CALON_N)
        out["R4_complete_case"] = {
            "n_fh": int(len(cfh)), "events_fh": int(cfh["y"].sum()),
            "n_nonfh": int(len(cnf)), "events_nonfh": int(cnf["y"].sum()),
            "fh_to_nonfh": {"auc": float(roc_auc_score(cnf["y"], f.predict(bf, cnf))),
                            **f.calib(cnf["y"].to_numpy(int), f.predict(bf, cnf))},
            "nonfh_to_fh": {"auc": float(roc_auc_score(cfh["y"], f.predict(bn, cfh))),
                            **f.calib(cfh["y"].to_numpy(int), f.predict(bn, cfh))}}

    (OUT / "fh_vs_nonfh_robustness.json").write_text(json.dumps(out, indent=1))

    print("R1  calibration with 95% intervals")
    for k, v in r1.items():
        print("   %-12s AUC %.3f  expected %.2f%% vs observed %.2f%%  E:O %.2f (%.2f-%.2f)"
              % (k, v["auc"], v["expected_pct"], v["observed_pct"], v["E_O"], *v["E_O_ci"]))
    print("\nR2  matching sensitivity (%d configurations)" % len(r2))
    print("   ratio call seed   n_FH  n_nonFH  prevFH  prevNF    OR   EO_FH>NF  EO_NF>FH")
    for r in r2:
        print("   1:%-3d %.1f  %d %5d %8d  %5.1f%%  %5.1f%%  %5.2f    %5.2f     %5.2f"
              % (r["ratio"], r["calliper"], r["seed"] % 10, r["n_fh"], r["n_nonfh"],
                 r["prev_fh_pct"], r["prev_nonfh_pct"], r["or_fh"],
                 r["EO_fh_to_nonfh"], r["EO_nonfh_to_fh"]))
    print("\nR3  discrimination of each score by genotype")
    for k, v in r3.items():
        print("   %-26s in FH %.3f   in matched non-FH %.3f   difference %+.3f"
              % (k, v["auc_in_FH"], v["auc_in_matched_nonFH"],
                 v["auc_in_FH"] - v["auc_in_matched_nonFH"]))
    if "R4_complete_case" in out:
        c4 = out["R4_complete_case"]
        print("\nR4  complete cases  FH %d/%d, non-FH %d/%d"
              % (c4["n_fh"], c4["events_fh"], c4["n_nonfh"], c4["events_nonfh"]))
        print("   FH -> non-FH  AUC %.3f  E:O %.2f" % (c4["fh_to_nonfh"]["auc"], c4["fh_to_nonfh"]["E_O"]))
        print("   non-FH -> FH  AUC %.3f  E:O %.2f" % (c4["nonfh_to_fh"]["auc"], c4["nonfh_to_fh"]["E_O"]))
    print("\nwritten:", OUT / "fh_vs_nonfh_robustness.json")


if __name__ == "__main__":
    main()
