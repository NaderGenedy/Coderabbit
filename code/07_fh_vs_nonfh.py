#!/usr/bin/env python3
"""Why an FH-specific model is needed: FH vs matched non-FH, UK Biobank and Wales.

Design
------
UK Biobank arm (primary, full CALON-N variable set available):
    FH      = strict coordinate-verified LDLR P/LP carriers (n=890)
    non-FH  = UK Biobank participants with no LDLR variant call, matched to the
              carriers on sex (exact) and age (calliper +/-1 year), 5:1, seeded.

Wales arm (secondary, reduced variable set - registry has no apoB/apoA1):
    FH      = All-Wales specialist clinic, genetic test performed, mutation reported
    non-FH  = same clinic, same referral pathway, genetic test performed, no mutation
              reported; matched on sex (exact) and age (calliper +/-2 years), 1:1.
    Ascertainment is therefore held constant and only genotype differs.

Four questions
--------------
Q1  Risk level: does ASCVD prevalence differ between FH and matched non-FH?
Q2  FH -> non-FH: does a model developed in FH transport to matched non-FH?
Q3  non-FH -> FH: does a model developed in matched non-FH transport to FH?
Q4  Coefficients: do the predictor-outcome relationships differ between the two?

Governance: aggregate output only. No participant rows, identifiers, family
identifiers, variant coordinates or participant-level predictions are written.
"""
from __future__ import annotations

import os

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

ROOT = Path(os.environ["CALON_PROJECT_ROOT"])
BASE = ROOT / "code" / "01_calon_disc_analysis.py"
OUT = ROOT / "outputs"
UKB = Path(os.environ["CALON_SHARED_MASTER"]) / "UKB/ukb_master.csv"
WALES = Path(os.environ["CALON_WALES_DATA"]) / "WALES_FH_CLEANED.csv"
SEED = 20260810
BOOT = 2000

spec = importlib.util.spec_from_file_location("calon_base", BASE)
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)

CALON_N = ["age", "male", "hdl", "hypertension", "smoke_ever", "log_ratio", "log_apoa1"]
REDUCED = ["age", "male", "hdl", "smoke_ever"]


# ----------------------------------------------------------------- helpers
def num(frame, name):
    return pd.to_numeric(frame[name], errors="coerce") if name in frame else pd.Series(np.nan, index=frame.index)


def bounded(s, lo, hi):
    return s.where(s.between(lo, hi))


def match(case_age, case_sex, ctrl, ratio, calliper, seed):
    """Sex-exact, age-callipered nearest matching without replacement.

    Returns (matched case positions, matched control frame). Cases for which no
    control is available inside the calliper are dropped, so the two returned
    groups are balanced by construction.
    """
    rng = np.random.default_rng(seed)
    taken = np.zeros(len(ctrl), dtype=bool)
    c_age = ctrl["age"].to_numpy()
    c_sex = ctrl["male"].to_numpy()
    picked, kept_cases = [], []
    order = rng.permutation(len(case_age))
    for i in order:
        a, s = case_age[i], case_sex[i]
        ok = (~taken) & (c_sex == s) & (np.abs(c_age - a) <= calliper)
        idx = np.flatnonzero(ok)
        if idx.size < ratio:
            continue
        idx = idx[np.argsort(np.abs(c_age[idx] - a), kind="stable")][:ratio]
        taken[idx] = True
        picked.extend(idx.tolist())
        kept_cases.append(int(i))
    return sorted(kept_cases), ctrl.iloc[sorted(picked)].reset_index(drop=True)


def complete(frame, feats):
    q = frame.copy()
    for c in feats:
        q[c] = pd.to_numeric(q[c], errors="coerce")
        q[c] = q[c].fillna(q[c].median())
    return q


def fit(frame, feats, penalty=0.3):
    q = complete(frame, feats)
    X = q[feats].to_numpy(float)
    mu, sd = X.mean(0), X.std(0)
    sd[sd < 1e-9] = 1.0
    model = LogisticRegression(C=penalty, max_iter=5000)
    model.fit((X - mu) / sd, q["y"].to_numpy(int))
    return {"feats": feats, "mu": mu, "sd": sd, "model": model}


def predict(bundle, frame):
    q = complete(frame, bundle["feats"])
    X = q[bundle["feats"]].to_numpy(float)
    return bundle["model"].predict_proba((X - bundle["mu"]) / bundle["sd"])[:, 1]


def auc_ci(y, p, groups, seed=SEED, b=BOOT):
    y, p = np.asarray(y), np.asarray(p)
    point = roc_auc_score(y, p)
    rng = np.random.default_rng(seed)
    uniq = pd.unique(pd.Series(groups))
    index = {g: np.flatnonzero(np.asarray(groups) == g) for g in uniq}
    vals = []
    for _ in range(b):
        take = np.concatenate([index[g] for g in rng.choice(uniq, len(uniq), replace=True)])
        if len(np.unique(y[take])) < 2:
            continue
        vals.append(roc_auc_score(y[take], p[take]))
    lo, hi = (np.percentile(vals, [2.5, 97.5]) if vals else (np.nan, np.nan))
    return float(point), float(lo), float(hi)


def calib(y, p):
    y, p = np.asarray(y, float), np.clip(np.asarray(p, float), 1e-6, 1 - 1e-6)
    obs = y.mean()
    return {"expected": float(p.mean()), "observed": float(obs),
            "E_O": float(p.mean() / obs) if obs > 0 else float("nan"),
            "brier": float(np.mean((p - y) ** 2))}


def coef_table(bundle):
    return {f: float(c / s) for f, c, s in
            zip(bundle["feats"], bundle["model"].coef_[0], bundle["sd"])}


def arm(name, fh, nonfh, feats, cl_fh, cl_nf):
    """Run Q1-Q4 for one arm and return an aggregate result block."""
    res = {"arm": name, "n_fh": int(len(fh)), "events_fh": int(fh["y"].sum()),
           "n_nonfh": int(len(nonfh)), "events_nonfh": int(nonfh["y"].sum()),
           "prevalence_fh_pct": float(100 * fh["y"].mean()),
           "prevalence_nonfh_pct": float(100 * nonfh["y"].mean()),
           "age_mean_fh": float(fh["age"].mean()), "age_mean_nonfh": float(nonfh["age"].mean()),
           "male_pct_fh": float(100 * fh["male"].mean()), "male_pct_nonfh": float(100 * nonfh["male"].mean()),
           "features": feats}

    # Q1 unadjusted prevalence ratio / odds ratio for FH status
    a, b_ = fh["y"].sum(), len(fh) - fh["y"].sum()
    c, d = nonfh["y"].sum(), len(nonfh) - nonfh["y"].sum()
    res["odds_ratio_fh_vs_nonfh"] = float((a * d) / (b_ * c)) if b_ * c else float("nan")
    se = np.sqrt(1 / max(a, .5) + 1 / max(b_, .5) + 1 / max(c, .5) + 1 / max(d, .5))
    res["or_ci"] = [float(np.exp(np.log(res["odds_ratio_fh_vs_nonfh"]) - 1.96 * se)),
                    float(np.exp(np.log(res["odds_ratio_fh_vs_nonfh"]) + 1.96 * se))]

    # FH status adjusted for the risk-factor profile: pool both groups, fit the
    # same feature set plus an FH indicator, and read off its coefficient.
    pooled = pd.concat([fh.assign(fh=1), nonfh.assign(fh=0)], ignore_index=True)
    f_pool = fit(pooled, feats + ["fh"])
    j = f_pool["feats"].index("fh")
    beta = float(f_pool["model"].coef_[0][j] / f_pool["sd"][j])
    res["adjusted_or_fh"] = float(np.exp(beta))

    f_fh, f_nf = fit(fh, feats), fit(nonfh, feats)

    # Q2/Q3 reciprocal transport between FH and matched non-FH
    for tag, src, tgt, cl in [("fh_to_nonfh", f_fh, nonfh, cl_nf),
                              ("nonfh_to_fh", f_nf, fh, cl_fh),
                              ("fh_internal", f_fh, fh, cl_fh),
                              ("nonfh_internal", f_nf, nonfh, cl_nf)]:
        p = predict(src, tgt)
        pt, lo, hi = auc_ci(tgt["y"].to_numpy(int), p, cl)
        res[tag] = {"auc": pt, "auc_ci": [lo, hi], **calib(tgt["y"].to_numpy(int), p)}

    # Q4 coefficients on the raw scale, fitted separately in each population
    res["coefficients"] = {"fh": coef_table(f_fh), "nonfh": coef_table(f_nf)}
    return res


# ----------------------------------------------------------------- cohorts
def ukb_arm():
    cohorts = m.prepare_cohorts()
    fh = cohorts["ukb_strict"].copy()
    carrier_ids = set()  # rebuilt below from the master by carrier flag

    use = ["eid", "ldlr_carrier", "prevalent_ascvd", "age_exact_baseline", "age_at_recruit",
           "sex_F", "diabetes_combined", "smoking_ever", "sbp", "dbp", "pre_tc", "tc_chem",
           "pre_ldl", "ldl_chem", "pre_hdl", "hdl_chem", "pre_tg", "tg_chem", "apob",
           "apob_chem", "apo_a1", "pre_lpa", "lpa_chem", "on_statin_self", "bmi_direct"]
    raw = pd.read_csv(UKB, usecols=use, low_memory=False)
    raw = raw.loc[num(raw, "ldlr_carrier").fillna(0).ne(1)].reset_index(drop=True)

    x = pd.DataFrame(index=raw.index)
    x["age"] = bounded(num(raw, "age_exact_baseline").fillna(num(raw, "age_at_recruit")), 5, 105)
    x["male"] = 1 - num(raw, "sex_F").fillna(0)
    dia, smk = num(raw, "diabetes_combined"), num(raw, "smoking_ever")
    x["diabetes"] = dia.gt(0).astype(float).where(dia.notna())
    x["smoke_ever"] = smk.gt(0).astype(float).where(smk.notna())
    sbp, dbp = bounded(num(raw, "sbp"), 70, 260), bounded(num(raw, "dbp"), 35, 160)
    x["hypertension"] = (sbp.ge(140) | dbp.ge(90)).astype(float).where(sbp.notna() | dbp.notna())
    x["ldl"] = bounded(num(raw, "pre_ldl").fillna(num(raw, "ldl_chem")), 0.3, 20)
    x["hdl"] = bounded(num(raw, "pre_hdl").fillna(num(raw, "hdl_chem")), 0.2, 5)
    x["apob"] = bounded(num(raw, "apob").fillna(num(raw, "apob_chem")), 0.2, 4)
    x["apoa1"] = bounded(num(raw, "apo_a1"), 0.3, 4)
    x["log_ratio"] = np.log((x["apob"] / x["ldl"]).where(lambda z: z.gt(0)))
    x["log_apoa1"] = np.log(x["apoa1"])
    x["y"] = num(raw, "prevalent_ascvd").fillna(0).gt(0).astype(int)
    x = x.loc[x["age"].notna()].reset_index(drop=True)

    fh["log_ratio"] = np.log((fh["apob"] / fh["ldl"]).where(lambda z: z.gt(0)))
    fh["log_apoa1"] = np.log(fh["apoa1"])

    keep, ctrl = match(fh["age"].to_numpy(float), fh["male"].to_numpy(float), x, 5, 1.0, SEED)
    ctrl["cluster"] = np.arange(len(ctrl))          # unrelated participants
    fh_m = fh.iloc[keep].reset_index(drop=True)
    out = arm("UK Biobank", fh_m, ctrl, CALON_N,
              fh_m["cluster"].to_numpy(), ctrl["cluster"].to_numpy())
    out["fh_unmatched_dropped"] = int(len(fh) - len(fh_m))
    return out, len(x)


def wales_arm():
    w = pd.read_csv(WALES, low_memory=False)
    tested = w["ResultDate1"].notna()
    mut = w["Mutation1"].astype(str).str.strip()
    pos = mut.ne("") & mut.str.lower().ne("nan") & w["Mutation1"].notna()

    x = pd.DataFrame(index=w.index)
    x["age"] = bounded(num(w, "BMI_AGE"), 18, 100)
    x["male"] = w["Gender"].astype(str).str.upper().str[0].eq("M").astype(float)
    smk = w["Smoking"].astype(str).str.strip()
    x["smoke_ever"] = np.where(smk.eq("1"), 1.0, np.where(smk.eq("0"), 0.0, np.nan))
    x["hdl"] = bounded(num(w, "HDL.1"), 0.2, 5)
    x["ldl"] = bounded(num(w, "LDL.1"), 0.3, 20)
    x["y"] = num(w, "ascvd_combine").fillna(0).gt(0).astype(int)
    x["cluster"] = w["FamilyNumber"].astype(str).fillna("NA")
    x["fh"] = (tested & pos).astype(int)
    x["proband"] = num(w, "Proband")
    x = x.loc[tested & x["age"].notna()].reset_index(drop=True)

    fh = x.loc[x["fh"].eq(1)].reset_index(drop=True)
    nf = x.loc[x["fh"].eq(0)].reset_index(drop=True)
    keep, ctrl = match(fh["age"].to_numpy(float), fh["male"].to_numpy(float), nf, 1, 2.0, SEED)
    fh_m = fh.iloc[keep].reset_index(drop=True)
    out = arm("Wales specialist clinic", fh_m, ctrl, REDUCED,
              fh_m["cluster"].to_numpy(), ctrl["cluster"].to_numpy())
    out["fh_unmatched_dropped"] = int(len(fh) - len(fh_m))
    out["composition"] = {
        "genotype_positive_proband_pct": float(100 * fh["proband"].eq(1).mean()),
        "genotype_negative_proband_pct": float(100 * nf["proband"].eq(1).mean())}

    # Referral role is almost perfectly confounded with genotype in a specialist
    # clinic: a relative of a mutation-negative index is not cascade tested.
    # Repeat the contrast with both arms restricted to probands.
    pf = fh.loc[fh["proband"].eq(1)].reset_index(drop=True)
    pn = nf.loc[nf["proband"].eq(1)].reset_index(drop=True)
    k2, c2 = match(pf["age"].to_numpy(float), pf["male"].to_numpy(float), pn, 1, 2.0, SEED)
    pf_m = pf.iloc[k2].reset_index(drop=True)
    out["proband_only"] = arm("Wales, probands only", pf_m, c2, REDUCED,
                              pf_m["cluster"].to_numpy(), c2["cluster"].to_numpy())
    return out


def main():
    ukb, n_pool = ukb_arm()
    ukb["nonfh_pool_available"] = int(n_pool)
    wal = wales_arm()
    out = {"seed": SEED, "bootstrap": BOOT, "participant_level_outputs": False,
           "arms": [ukb, wal]}
    (OUT / "fh_vs_nonfh.json").write_text(json.dumps(out, indent=1))

    for a in out["arms"]:
        print("\n" + "=" * 78)
        print(a["arm"], "|", ", ".join(a["features"]))
        print("  FH      n=%-6d events=%-5d (%.1f%%)  age %.1f  male %.0f%%"
              % (a["n_fh"], a["events_fh"], a["prevalence_fh_pct"], a["age_mean_fh"], a["male_pct_fh"]))
        print("  non-FH  n=%-6d events=%-5d (%.1f%%)  age %.1f  male %.0f%%"
              % (a["n_nonfh"], a["events_nonfh"], a["prevalence_nonfh_pct"],
                 a["age_mean_nonfh"], a["male_pct_nonfh"]))
        print("  Q1 ASCVD odds ratio FH vs matched non-FH: %.2f (%.2f-%.2f)  |  adjusted for risk factors: %.2f"
              % (a["odds_ratio_fh_vs_nonfh"], *a["or_ci"], a["adjusted_or_fh"]))
        print("  matching: %d FH participants unmatched and dropped" % a.get("fh_unmatched_dropped", 0))
        for k, lbl in [("fh_internal", "Q0 FH model in FH        "),
                       ("nonfh_internal", "Q0 non-FH model in non-FH"),
                       ("fh_to_nonfh", "Q2 FH model -> non-FH    "),
                       ("nonfh_to_fh", "Q3 non-FH model -> FH    ")]:
            r = a[k]
            print("  %s AUC %.3f (%.3f-%.3f)  E:O %.2f  Brier %.4f"
                  % (lbl, r["auc"], r["auc_ci"][0], r["auc_ci"][1], r["E_O"], r["brier"]))
        if "composition" in a:
            print("  composition: probands are %.0f%% of the genotype-positive arm and %.0f%% of the genotype-negative arm"
                  % (a["composition"]["genotype_positive_proband_pct"],
                     a["composition"]["genotype_negative_proband_pct"]))
        if "proband_only" in a:
            q = a["proband_only"]
            print("  SENSITIVITY, both arms restricted to probands:")
            print("      FH n=%d (%.1f%%) vs non-FH n=%d (%.1f%%) | OR %.2f (%.2f-%.2f)"
                  % (q["n_fh"], q["prevalence_fh_pct"], q["n_nonfh"], q["prevalence_nonfh_pct"],
                     q["odds_ratio_fh_vs_nonfh"], *q["or_ci"]))
            print("      E:O  FH model -> non-FH %.2f    non-FH model -> FH %.2f"
                  % (q["fh_to_nonfh"]["E_O"], q["nonfh_to_fh"]["E_O"]))
        print("  Q4 coefficients (raw scale, per unit):")
        for f in a["features"]:
            print("      %-12s FH %+8.4f   non-FH %+8.4f"
                  % (f, a["coefficients"]["fh"][f], a["coefficients"]["nonfh"][f]))
    print("\nwritten:", OUT / "fh_vs_nonfh.json")


if __name__ == "__main__":
    main()
