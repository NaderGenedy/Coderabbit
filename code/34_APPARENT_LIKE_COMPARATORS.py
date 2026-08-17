#!/usr/bin/env python3
"""Report CALON on the SAME validation footing the comparator papers used.

WHY THIS EXISTS
  The three comparators report, in their own words:

  SAFEHEART-RE (Circulation 2017;135) — Harrell C 0.85 (0.81 in primary
    prevention). Internal validation: "the degree of overoptimism resulting from
    model assessment ON THE SAME DATA ON WHICH IT WAS DEVELOPED was estimated
    with bootstrap resampling of the original set (100 randomized samples)".
    Reported overoptimism 0.003. No cross-validation. No external validation.

  FH-Risk-Score (ATVB 2021;41) — Harrell C 0.75. "The estimated optimism (or
    bias) obtained by the bootstrap ... with 100 bootstrap resampling was equal
    to 0.002", computed on DECILES of the score. LDL-C was "untreated (57%) or
    IMPUTED (43%)". No external validation; listed as a limitation.

  Montreal-FH-SCORE (J Clin Lipidol 2017;11) — AUC 0.840, from a STEPWISE
    logistic model (entry p<0.05) evaluated in the derivation sample. No
    internal validation of any kind is reported. Cross-sectional/prevalent.

  CALON has been reported as a 10x10 out-of-fold, family-clustered,
  cross-validated C. That is a materially harsher estimator than any of the
  above, so comparing our headline to theirs understates us. This script adds
  the like-for-like number: APPARENT C with Harrell bootstrap optimism
  correction, 100 resamples, matching SAFEHEART and FH-RS exactly.

  Both estimates are reported. Out-of-fold remains the conservative primary;
  apparent-minus-optimism is the figure directly comparable to 0.85 / 0.75 / 0.840.

Governance: aggregate output only.
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
from lifelines import CoxPHFitter
from lifelines.utils import concordance_index

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "outputs"
B_OPT = 100                       # exactly what SAFEHEART and FH-RS used
PENALTY = 0.02

_c = importlib.util.spec_from_file_location("cc", ROOT / "code" / "33_CALON_C.py")
cc = importlib.util.module_from_spec(_c); sys.modules["cc"] = cc; _c.loader.exec_module(cc)


def apparent_and_optimism(df, feats, B=B_OPT, seed=20260816):
    """Harrell optimism bootstrap, the comparator papers' own procedure.

    1. Fit on the full sample -> apparent C.
    2. For each of B bootstrap samples: fit on the resample, score the resample
       (C_boot) and score the ORIGINAL sample (C_orig). optimism = C_boot - C_orig.
    3. Corrected C = apparent - mean(optimism).
    """
    feats = cc.usable(df, feats)
    full = cc._fit(df, feats)
    med = {f: pd.to_numeric(df[f], errors="coerce").median() for f in feats}

    def lp_of(fit, frame, medians):
        m = frame[feats].copy()
        for f in feats:
            m[f] = pd.to_numeric(m[f], errors="coerce").fillna(medians[f])
        return np.log(np.asarray(fit.predict_partial_hazard(m), float))

    apparent = concordance_index(df["T"], -lp_of(full, df, med), df["E"])
    rng = np.random.default_rng(seed)
    opt = []
    for _ in range(B):
        idx = rng.choice(len(df), len(df), replace=True)
        bs = df.iloc[idx].reset_index(drop=True)
        if bs.E.sum() < 10:
            continue
        try:
            fb = cc._fit(bs, feats)
        except Exception:
            continue
        mb = {f: pd.to_numeric(bs[f], errors="coerce").median() for f in feats}
        try:
            c_boot = concordance_index(bs["T"], -lp_of(fb, bs, mb), bs["E"])
            c_orig = concordance_index(df["T"], -lp_of(fb, df, mb), df["E"])
        except Exception:
            continue
        opt.append(c_boot - c_orig)
    if not opt:
        return dict(apparent=float(apparent), optimism=None, corrected=None, B_eff=0)
    o = float(np.mean(opt))
    return dict(apparent=float(apparent), optimism=o, corrected=float(apparent - o),
                optimism_sd=float(np.std(opt, ddof=1)), B_eff=len(opt), terms=feats)


def main():
    ukb, lu = cc.build_ukb()
    wal, lw = cc.build_wales()
    res = {"procedure": "Harrell optimism bootstrap, 100 resamples — the identical "
                        "internal-validation method used by SAFEHEART-RE "
                        "(overoptimism 0.003) and FH-Risk-Score (0.002)",
           "published_benchmarks": {
               "SAFEHEART-RE": {"C": 0.85, "C_primary_prevention": 0.81,
                                "validation": "bootstrap x100, optimism 0.003",
                                "external_validation": False},
               "FH-Risk-Score": {"C": 0.75,
                                 "validation": "bootstrap x100 on deciles, optimism 0.002",
                                 "ldl": "untreated 57% / imputed 43%",
                                 "external_validation": False},
               "Montreal-FH-SCORE": {"AUC": 0.840,
                                     "validation": "none reported; stepwise p<0.05, "
                                                   "apparent in derivation sample",
                                     "design": "cross-sectional / prevalent",
                                     "external_validation": False}},
           "arms": []}

    print("=" * 82)
    print("CALON on the comparators' own validation footing")
    print("=" * 82)
    for cname, df0, spec, label in (
            ("UK Biobank", ukb, cc.SPEC_FULL, "PRIMARY 9-term"),
            ("Wales", wal, cc.SPEC_FULL, "PRIMARY 9-term"),
            ("UK Biobank", ukb, cc.SPEC_CLEAN, "SENS dated-only"),
            ("Wales", wal, cc.SPEC_CLEAN, "SENS dated-only")):
        for H, hl in ((None, "full"), (10, "10y"), (5, "5y")):
            d = df0 if H is None else cc.horizon(df0, H)
            if d.E.sum() < 10:
                continue
            a = apparent_and_optimism(d, spec)
            oof, _, feats = cc.cv(d, spec)
            row = dict(cohort=cname, arm=label, horizon=hl, n=int(len(d)),
                       events=int(d.E.sum()), out_of_fold_C=oof, **a)
            res["arms"].append(row)
            print(f"  {label:16s} {cname:11s} {hl:5s} "
                  f"apparent={a['apparent']:.4f}  optimism={a['optimism']:+.4f}  "
                  f"corrected={a['corrected']:.4f}  |  out-of-fold={oof:.4f}")

    (OUT / "calon_apparent.json").write_text(json.dumps(res, indent=2, default=str))
    pd.DataFrame(res["arms"]).to_csv(OUT / "calon_apparent.csv", index=False)
    print("=" * 82)
    print("written:", OUT / "calon_apparent.json")


if __name__ == "__main__":
    main()
