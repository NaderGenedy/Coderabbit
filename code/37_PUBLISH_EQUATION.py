#!/usr/bin/env python3
"""CALON-C — publish the model equation. TRIPOD+AI item 17.

Without this, nobody can apply the model. This emits:

  * raw-unit coefficients (log hazard ratio per natural unit, NOT per SD)
  * hazard ratios with 95% CIs, both per unit and per SD
  * the mean of each predictor in the development cohort (needed for centring)
  * baseline survival S0 at 5 and 10 years
  * the complete risk equation as a copy-pasteable formula
  * WORKED EXAMPLES with expected outputs, so an independent implementer can
    unit-test their code the way SAFEHEART-RE's published worked examples let
    this project unit-test its own SAFEHEART implementation

Fitted on the FULL development cohort (this is the deployment equation).
Performance figures elsewhere are out-of-fold and remain the honest estimates.

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

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "outputs"
_s = importlib.util.spec_from_file_location("cc", ROOT / "code" / "33_CALON_C.py")
cc = importlib.util.module_from_spec(_s); sys.modules["cc"] = cc; _s.loader.exec_module(cc)


def publish(df, cohort, spec):
    feats = cc.usable(df, spec)
    m = df[feats + ["T", "E"]].copy()
    med = {}
    for f in feats:
        m[f] = pd.to_numeric(m[f], errors="coerce")
        med[f] = float(m[f].median())
        m[f] = m[f].fillna(med[f])
    cph = CoxPHFitter(penalizer=cc.PENALTY).fit(m, "T", "E")
    sf = cph.baseline_survival_
    idx = sf.index.values
    s0 = {}
    for H in (5, 10):
        s0[H] = float(sf.iloc[np.searchsorted(idx, H, side="right") - 1, 0]) \
            if (idx <= H).any() else 1.0
    means = {f: float(m[f].mean()) for f in feats}
    sds = {f: float(m[f].std(ddof=1)) for f in feats}
    coef = []
    for f in feats:
        b = float(cph.params_[f]); se = float(cph.standard_errors_[f])
        coef.append({"term": f, "beta_per_unit": b,
                     "HR_per_unit": float(np.exp(b)),
                     "lo_per_unit": float(np.exp(b - 1.96 * se)),
                     "hi_per_unit": float(np.exp(b + 1.96 * se)),
                     "HR_per_SD": float(np.exp(b * sds[f])) if f not in ("male", "htn", "dm", "smoke") else None,
                     "mean_dev_cohort": means[f], "sd_dev_cohort": sds[f],
                     "median_for_imputation": med[f],
                     "p": float(cph.summary.loc[f, "p"])})
    lp_mean = float(sum(cph.params_[f] * means[f] for f in feats))
    return {"cohort": cohort, "terms": feats, "n": int(len(m)), "events": int(m.E.sum()),
            "penalizer": cc.PENALTY, "coefficients": coef,
            "lp_mean_dev_cohort": lp_mean, "S0_5y": s0[5], "S0_10y": s0[10],
            "equation": ("risk(t) = 1 - S0(t) ** exp( SUM(beta_i * x_i) - lp_mean )   "
                         "with S0(5y)=%.6f, S0(10y)=%.6f, lp_mean=%.6f"
                         % (s0[5], s0[10], lp_mean))}, cph, feats, means, med, s0, lp_mean


def worked(pub, cph, feats, means, med, s0, lp_mean, profiles):
    out = []
    for name, prof in profiles:
        x = {f: prof.get(f, med[f]) for f in feats}
        lp = float(sum(float(cph.params_[f]) * x[f] for f in feats))
        r5 = 1 - s0[5] ** np.exp(lp - lp_mean)
        r10 = 1 - s0[10] ** np.exp(lp - lp_mean)
        out.append({"profile": name, "inputs": {k: round(v, 4) for k, v in x.items()},
                    "linear_predictor": lp, "lp_minus_mean": lp - lp_mean,
                    "risk_5y_pct": 100 * float(r5), "risk_10y_pct": 100 * float(r10)})
    return out


def main():
    ukb, _ = cc.build_ukb(); wal, _ = cc.build_wales()
    res = {}
    for cohort, df in (("UK Biobank", ukb), ("Wales", wal)):
        pub, cph, feats, means, med, s0, lpm = publish(df, cohort, cc.SPEC_FULL)
        # Worked profiles: a low-risk and a high-risk carrier, defined on raw units.
        lowrisk = {"age": 45, "sp50": 0, "male": 0, "htn": 0, "dm": 0, "smoke": 0}
        highrisk = {"age": 65, "sp50": 15, "male": 1, "htn": 1, "dm": 1, "smoke": 1}
        # lipid terms set to cohort 25th / 75th centile so the example is reproducible
        for k, q in (("cum_nonhdl", .25), ("tg_filter", .75), ("remnant_unt", .25)):
            if k in feats:
                lowrisk[k] = float(pd.to_numeric(df[k], errors="coerce").quantile(q))
        for k, q in (("cum_nonhdl", .75), ("tg_filter", .25), ("remnant_unt", .75)):
            if k in feats:
                highrisk[k] = float(pd.to_numeric(df[k], errors="coerce").quantile(q))
        pub["worked_examples"] = worked(pub, cph, feats, means, med, s0, lpm,
                                        [("low-risk carrier", lowrisk),
                                         ("high-risk carrier", highrisk)])
        res[cohort] = pub
        print(f"\n{'='*88}\n{cohort}  n={pub['n']} events={pub['events']}  "
              f"S0(5y)={pub['S0_5y']:.6f}  S0(10y)={pub['S0_10y']:.6f}  lp_mean={lpm:.6f}")
        print(f"{'term':14s} {'beta/unit':>12s} {'HR/unit':>9s} {'95% CI':>20s} {'HR/SD':>8s} {'p':>10s}")
        for c in pub["coefficients"]:
            sd = f"{c['HR_per_SD']:.3f}" if c["HR_per_SD"] else "   —"
            print(f"{c['term']:14s} {c['beta_per_unit']:>12.6f} {c['HR_per_unit']:>9.4f} "
                  f"({c['lo_per_unit']:.3f},{c['hi_per_unit']:.3f})".rjust(21)
                  + f" {sd:>8s} {c['p']:>10.2e}")
        for w in pub["worked_examples"]:
            print(f"  WORKED  {w['profile']:20s} LP={w['linear_predictor']:+.4f}  "
                  f"5y={w['risk_5y_pct']:6.2f}%  10y={w['risk_10y_pct']:6.2f}%")

    (OUT / "calon_c_equation.json").write_text(json.dumps(res, indent=2, default=str))
    rows = []
    for cohort, pub in res.items():
        for c in pub["coefficients"]:
            rows.append({"cohort": cohort, **c})
    pd.DataFrame(rows).to_csv(OUT / "calon_c_equation.csv", index=False)
    print(f"\nwritten: {OUT/'calon_c_equation.json'} and .csv")


if __name__ == "__main__":
    main()
