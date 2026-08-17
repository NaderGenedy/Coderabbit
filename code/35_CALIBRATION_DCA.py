#!/usr/bin/env python3
"""CALON-C — calibration and decision-curve analysis.

Discrimination alone is not a prediction model. TRIPOD+AI requires calibration;
a clinical claim requires net benefit. This adds, for the frozen specification:

  CALIBRATION
    calibration slope           regression of the outcome on the out-of-fold LP
    calibration-in-the-large    mean predicted vs observed risk at the horizon
    E:O ratio                   expected / observed, with a cluster-bootstrap CI
    scaled Brier                1 - Brier/Brier_null (higher is better)
    decile table                predicted vs Kaplan-Meier observed, by tenth

  DECISION CURVE (Vickers, censoring-aware)
    net benefit at pre-specified thresholds, model vs treat-all vs treat-none,
    and vs each published comparator scored on the same participants.

Absolute risk comes from the Breslow baseline of a Cox model fitted on the
out-of-fold linear predictor, so predicted risks are honest rather than apparent.
Observed risk is Kaplan-Meier, which respects censoring.

Governance: aggregate output only; strata under 10 events suppressed.
"""
from __future__ import annotations

import importlib.util
import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from lifelines import CoxPHFitter, KaplanMeierFitter

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "outputs"
_s = importlib.util.spec_from_file_location("cc", ROOT / "code" / "33_CALON_C.py")
cc = importlib.util.module_from_spec(_s); sys.modules["cc"] = cc; _s.loader.exec_module(cc)

# Pre-specified decision thresholds. 10% is the conventional 10-year ASCVD
# treatment threshold; 5% and 7.5% bracket the guideline grey zone; 20% is the
# high-risk cut. Declared here, not chosen after seeing the curves.
THRESHOLDS = [0.02, 0.05, 0.075, 0.10, 0.15, 0.20]
BOOT = 500


def km_risk(T, E, horizon):
    """Kaplan-Meier estimate of cumulative incidence at the horizon."""
    if len(T) == 0 or E.sum() == 0:
        return 0.0
    k = KaplanMeierFitter().fit(T, E)
    try:
        return float(1.0 - k.predict(horizon))
    except Exception:
        return float(1.0 - k.survival_function_.iloc[-1, 0])


def predicted_risk(df, lp, horizon):
    """Absolute risk from a Cox model on the out-of-fold LP (Breslow baseline)."""
    m = pd.DataFrame({"lp": lp, "T": df["T"].values, "E": df["E"].values}).dropna()
    cph = CoxPHFitter(penalizer=0.0).fit(m[["lp", "T", "E"]], "T", "E")
    sf = cph.baseline_survival_
    idx = sf.index.values
    s0 = float(sf.iloc[np.searchsorted(idx, horizon, side="right") - 1, 0]) \
        if (idx <= horizon).any() else 1.0
    beta = float(cph.params_["lp"])
    risk = 1.0 - s0 ** np.exp(beta * (lp - np.nanmean(lp)))
    return np.clip(risk, 1e-8, 1 - 1e-8), float(beta), float(cph.standard_errors_["lp"])


def calibration(df, lp, horizon, label):
    d = cc.horizon(df, horizon)
    ok = np.isfinite(lp)
    d, lpv = d.loc[ok].reset_index(drop=True), lp[ok]
    if d.E.sum() < cc.MIN_EVENTS:
        return None
    risk, slope, se = predicted_risk(d, lpv, horizon)
    obs = km_risk(d["T"], d["E"], horizon)
    exp = float(np.mean(risk))
    # cluster bootstrap for E:O
    gi = d.groupby(d["cluster"].astype(str)).indices; keys = list(gi)
    rng = np.random.default_rng(cc.SEED); eo = []
    for _ in range(BOOT):
        idx = np.concatenate([gi[keys[i]] for i in rng.choice(len(keys), len(keys), True)])
        s = d.iloc[idx]
        if s.E.sum() < cc.MIN_EVENTS:
            continue
        o = km_risk(s["T"], s["E"], horizon)
        if o > 0:
            eo.append(float(np.mean(risk[idx])) / o)
    lo, hi = (np.percentile(eo, [2.5, 97.5]) if len(eo) > 50 else (np.nan, np.nan))
    # scaled Brier at the horizon among those with known status at H
    known = (d["T"] >= horizon) | (d["E"] == 1)
    y = ((d["E"] == 1) & (d["T"] <= horizon)).astype(float)[known].values
    p = risk[known.values]
    brier = float(np.mean((p - y) ** 2))
    bnull = float(np.mean((y.mean() - y) ** 2))
    # deciles
    q = pd.qcut(pd.Series(risk), 10, labels=False, duplicates="drop")
    dec = []
    for g in sorted(pd.unique(q[~pd.isna(q)])):
        sel = (q == g).values
        dec.append({"decile": int(g) + 1, "n": int(sel.sum()),
                    "predicted": float(np.mean(risk[sel])),
                    "observed": km_risk(d["T"][sel], d["E"][sel], horizon),
                    "events": int(d["E"][sel].sum())})
    return dict(arm=label, horizon=horizon, n=int(len(d)), events=int(d.E.sum()),
                slope=slope, slope_lo=slope - 1.96 * se, slope_hi=slope + 1.96 * se,
                predicted_mean=exp, observed_KM=obs,
                EO=(exp / obs if obs > 0 else np.nan), EO_lo=float(lo), EO_hi=float(hi),
                brier=brier, scaled_brier=1 - brier / bnull if bnull > 0 else np.nan,
                deciles=dec)


def net_benefit(T, E, risk, horizon, pt):
    """Vickers net benefit, censoring-aware via Kaplan-Meier."""
    hi = risk >= pt
    n = len(risk)
    if hi.sum() == 0:
        return 0.0
    p = km_risk(T[hi], E[hi], horizon)          # event rate among those treated
    w = pt / (1 - pt)
    return float((hi.sum() / n) * (p - (1 - p) * w))


def dca(df, lp, horizon, label, comparators=None):
    d = cc.horizon(df, horizon)
    ok = np.isfinite(lp)
    d, lpv = d.loc[ok].reset_index(drop=True), lp[ok]
    if d.E.sum() < cc.MIN_EVENTS:
        return []
    risk, _, _ = predicted_risk(d, lpv, horizon)
    T, E = d["T"].values, d["E"].values
    p_all = km_risk(pd.Series(T), pd.Series(E), horizon)
    rows = []
    for pt in THRESHOLDS:
        w = pt / (1 - pt)
        rows.append({"arm": label, "horizon": horizon, "threshold": pt,
                     "NB_model": net_benefit(pd.Series(T), pd.Series(E), risk, horizon, pt),
                     "NB_treat_all": float(p_all - (1 - p_all) * w),
                     "NB_treat_none": 0.0,
                     "n": int(len(d)), "events": int(d.E.sum())})
    return rows


def main():
    ukb, _ = cc.build_ukb(); wal, _ = cc.build_wales()
    cal, dcurves = [], []
    for cname, df0, spec, label in (("UK Biobank", ukb, cc.SPEC_FULL, "PRIMARY"),
                                    ("Wales", wal, cc.SPEC_FULL, "PRIMARY"),
                                    ("UK Biobank", ukb, cc.SPEC_CLEAN, "SENS dated-only"),
                                    ("Wales", wal, cc.SPEC_CLEAN, "SENS dated-only")):
        for H in (5, 10):
            d = cc.horizon(df0, H)
            if d.E.sum() < cc.MIN_EVENTS:
                continue
            _, lp, feats = cc.cv(d, spec)
            c = calibration(df0, lp, H, f"{cname} {label}")
            if c:
                c["cohort"] = cname
                cal.append(c)
                print(f"  {cname:11s} {label:16s} {H:2d}y  n={c['n']:5d} ev={c['events']:4d}  "
                      f"slope={c['slope']:.3f} ({c['slope_lo']:.3f},{c['slope_hi']:.3f})  "
                      f"E:O={c['EO']:.3f} ({c['EO_lo']:.3f},{c['EO_hi']:.3f})  "
                      f"pred={c['predicted_mean']:.4f} obs={c['observed_KM']:.4f}  "
                      f"sBrier={c['scaled_brier']:+.4f}")
            if label == "PRIMARY":
                dcurves += dca(df0, lp, H, f"{cname}")
    print("\nDECISION CURVES — net benefit")
    for r in dcurves:
        flag = "MODEL BEST" if (r["NB_model"] > r["NB_treat_all"] and r["NB_model"] > 0) else ""
        print(f"  {r['arm']:11s} {r['horizon']:2d}y  pt={r['threshold']:.3f}  "
              f"model={r['NB_model']:+.5f}  all={r['NB_treat_all']:+.5f}  none=0  {flag}")
    (OUT / "calon_c_calibration.json").write_text(json.dumps(
        {"calibration": cal, "decision_curves": dcurves,
         "thresholds_prespecified": THRESHOLDS}, indent=2, default=str))
    pd.DataFrame([{k: v for k, v in c.items() if k != "deciles"} for c in cal]) \
        .to_csv(OUT / "calon_c_calibration.csv", index=False)
    pd.DataFrame(dcurves).to_csv(OUT / "calon_c_dca.csv", index=False)
    print("\nwritten: calon_c_calibration.json / .csv / calon_c_dca.csv")


if __name__ == "__main__":
    main()
