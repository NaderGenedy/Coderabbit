#!/usr/bin/env python3
"""QC addendum to 15_CALON_FINAL.py: coefficient signs, fold failures,
covariate missingness, and calibration. Aggregate output only."""
from __future__ import annotations

import os

import importlib.util
import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from lifelines import CoxPHFitter

warnings.filterwarnings("ignore")
ROOT = Path(os.environ["CALON_PROJECT_ROOT"])

_s = importlib.util.spec_from_file_location("cf", ROOT / "code" / "15_CALON_FINAL.py")
cf = importlib.util.module_from_spec(_s)
_s.loader.exec_module(cf)

EXPECT = {"age": "+", "sp18": "?", "sp30": "?", "sp50": "?", "male": "+",
          "cum_nonhdl": "+", "log_tghdl": "+", "hdl": "-", "dm": "+",
          "smoke": "+", "htn_any": "+", "bmi": "+"}


def report(name, d):
    print("\n" + "=" * 92)
    print(name)
    print("=" * 92)
    feats = cf.usable(d, cf.SPEC)

    print("\nCOVARIATE COMPLETENESS (%% non-missing, n=%d)" % len(d))
    for f in cf.SPEC:
        if f in d:
            pct = 100 * d[f].notna().mean()
            flag = "  <-- SPARSE" if pct < 70 else ""
            print("  %-12s %6.1f%%%s" % (f, pct, flag))

    print("\nEVENTS BY STRATUM (governance: <10 suppressed)")
    for f in ("dm", "smoke", "htn_any", "tx", "male"):
        if f not in d:
            continue
        for v, lbl in ((1, "=1"), (0, "=0")):
            e = int(d.loc[d[f].eq(v), "E"].sum())
            print("  %-8s%-3s  n=%-5d events=%s"
                  % (f, lbl, int(d[f].eq(v).sum()), e if e >= 10 else "<10"))

    X = d.reindex(columns=feats).astype(float)
    X = X.fillna(X.median())
    sds = {c: (X[c].std() if X[c].nunique() > 2 else 1.0) for c in feats}
    for c in feats:
        if X[c].nunique() > 2:
            X[c] = (X[c] - X[c].mean()) / (sds[c] if sds[c] > 1e-9 else 1.0)
    X["T"], X["E"] = d["T"].to_numpy(float), d["E"].to_numpy(int)
    f = CoxPHFitter(penalizer=0.05).fit(X, "T", "E")
    s = f.summary

    print("\nCOEFFICIENT SIGNS (full-cohort refit, penalised; per SD or per unit)")
    print("  %-12s %8s %8s %-18s %s" % ("term", "coef", "HR", "95% CI", "sign vs expected"))
    bad = []
    for c in feats:
        b, hr = s.loc[c, "coef"], s.loc[c, "exp(coef)"]
        lo, hi = s.loc[c, "exp(coef) lower 95%"], s.loc[c, "exp(coef) upper 95%"]
        got = "+" if b > 0 else "-"
        exp = EXPECT.get(c, "?")
        ok = "ok" if exp == "?" or got == exp else "UNEXPECTED (%s)" % exp
        if ok != "ok":
            bad.append(c)
        print("  %-12s %8.4f %8.3f (%5.3f, %5.3f)  %s" % (c, b, hr, lo, hi, ok))

    # calibration of the cross-validated linear predictor
    lp, ok_m, cidx, sd, fails, _ = cf.cv(d, cf.SPEC)
    cal = CoxPHFitter().fit(pd.DataFrame({"lp": lp[ok_m], "T": d["T"].to_numpy()[ok_m],
                                          "E": d["E"].to_numpy()[ok_m]}), "T", "E")
    slope = float(cal.summary.loc["lp", "coef"])
    slo, shi = (float(cal.summary.loc["lp", "coef lower 95%"]),
                float(cal.summary.loc["lp", "coef upper 95%"]))
    print("\n  cross-validated C           %.4f  (repeat SD %.4f)" % (cidx, sd))
    print("  Cox convergence failures    %d" % fails)
    print("  calibration slope           %.3f (%.3f, %.3f)  [1.00 = no over/under-fit]"
          % (slope, slo, shi))
    print("  unexpected coefficient signs: %s" % (bad or "none"))
    return {"features": feats, "c_index": cidx, "repeat_sd": sd, "fold_failures": fails,
            "calibration_slope": [slope, slo, shi], "unexpected_signs": bad,
            "completeness": {f: float(d[f].notna().mean()) for f in cf.SPEC if f in d}}


def main():
    out = {"ukb": report("UK BIOBANK", cf.build_ukb()),
           "wales": report("WALES / PASS", cf.build_wales())}
    (ROOT / "outputs" / "calon_final_qc.json").write_text(json.dumps(out, indent=2))
    print("\nwritten:", ROOT / "outputs" / "calon_final_qc.json")


if __name__ == "__main__":
    main()
