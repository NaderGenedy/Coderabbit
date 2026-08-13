#!/usr/bin/env python3
"""Grey-zone risk enhancers: Lp(a) and log(apoB/LDL-C) on top of the CALON base.

RATIONALE
The base model (age, sex, hypertension, T2DM, smoking, cumulative non-HDL-C,
TG/HDL-C) sorts most people clearly. The clinical question is not whether an
enhancer improves discrimination on average - averaged over people already
classified confidently, almost nothing does - but whether it resolves the
INTERMEDIATE band, where the treatment decision is genuinely uncertain.

DESIGN
1. Fit the base model with the same repeated, cluster-aware cross-validation
   used by code/15, and convert each out-of-fold linear predictor to a 10-year
   predicted risk through a Breslow baseline estimated in the training folds.
2. Define the GREY ZONE as 5-20% predicted 10-year risk - the intermediate band
   used by prevention guidelines, fixed before any enhancer is examined.
3. Within the grey zone only, refit base vs base+enhancers out-of-fold and
   compare discrimination, with a cluster bootstrap on the paired difference.
4. Report each enhancer's hazard ratio per SD inside the grey zone, and how many
   people the enhancers move out of it.

Enhancers are NOT in the base model and are not published-score inputs, so the
binding rule is respected: they are raw measured variables.

Wales carries Lp(a) on a different assay scale and has no apoB, so this panel is
UK Biobank only. Stated as a limitation rather than papered over.

Governance: aggregate output only; strata with <10 events are suppressed.
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

ROOT = Path(os.environ.get("CALON_PROJECT_ROOT",
            "${CALON_PROJECT_ROOT}"))
_s = importlib.util.spec_from_file_location("cf", ROOT / "code" / "15_CALON_FINAL.py")
cf = importlib.util.module_from_spec(_s)
sys.modules["cf"] = cf
_s.loader.exec_module(cf)

HORIZON = 10.0
GREY_LO, GREY_HI = 0.05, 0.20
ENHANCERS = ["log_lpa", "log_apob_ldl"]
MIN_EVENTS = 10


def oof_risk(d, feats, horizon=HORIZON, repeats=cf.REPEATS, seed=cf.SEED):
    """Out-of-fold 10-year predicted risk via a training-fold Breslow baseline."""
    y, t = d.E.to_numpy(int), d["T"].to_numpy(float)
    feats = [f for f in feats if f in d and d[f].nunique(dropna=True) >= 2]
    acc, cnt = np.zeros(len(d)), np.zeros(len(d))
    for r in range(repeats):
        rng = np.random.default_rng(seed + r)
        fold = rng.integers(0, 5, len(d))
        for k in range(5):
            tr, te = np.flatnonzero(fold != k), np.flatnonzero(fold == k)
            if y[tr].sum() < MIN_EVENTS or len(te) == 0:
                continue
            X = d.reindex(columns=feats).astype(float)
            X = X.fillna(X.iloc[tr].median())
            for c in feats:
                if X[c].nunique() > 2:
                    mu, sd = X[c].iloc[tr].mean(), X[c].iloc[tr].std()
                    if sd > 1e-9:
                        X[c] = (X[c] - mu) / sd
            td = X.iloc[tr].copy()
            td["T"], td["E"] = t[tr], y[tr]
            try:
                f = CoxPHFitter(penalizer=0.05).fit(td, "T", "E")
                s = f.predict_survival_function(X.iloc[te], times=[horizon])
                acc[te] += 1.0 - s.values[0]
                cnt[te] += 1
            except Exception:
                continue
    ok = cnt > 0
    return np.divide(acc, np.maximum(cnt, 1)), ok


def boot_delta(t, y, a, b, grp, n=cf.BOOT, seed=cf.SEED):
    rng = np.random.default_rng(seed)
    u = pd.unique(pd.Series(grp))
    idx = {g: np.flatnonzero(grp == g) for g in u}
    try:
        pt = concordance_index(t, -a, y) - concordance_index(t, -b, y)
    except Exception:
        return None
    v = []
    for _ in range(n):
        tk = np.concatenate([idx[g] for g in rng.choice(u, len(u), replace=True)])
        if y[tk].sum() < MIN_EVENTS:
            continue
        try:
            v.append(concordance_index(t[tk], -a[tk], y[tk])
                     - concordance_index(t[tk], -b[tk], y[tk]))
        except Exception:
            continue
    return (pt, float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))) if len(v) >= 200 else None


def main():
    d = cf.build_ukb()
    base = cf.usable(d, cf.SPEC)
    print("=" * 96)
    print("GREY-ZONE RISK ENHANCERS - UK Biobank LDLR carriers, incident ASCVD")
    print("=" * 96)
    print("  base model : %s" % " + ".join(base))
    print("  enhancers  : %s" % " + ".join(ENHANCERS))
    print("  grey zone  : %.0f-%.0f%% predicted %.0f-year risk (fixed before testing)"
          % (100 * GREY_LO, 100 * GREY_HI, HORIZON))
    for e, lbl in [("lpa", "Lp(a)"), ("apob", "apoB")]:
        print("  %-6s observed in %.1f%% of the cohort" % (lbl, 100 * d[e].notna().mean()))

    risk, ok = oof_risk(d, base)
    grey = ok & (risk >= GREY_LO) & (risk <= GREY_HI)
    y, t, g = d.E.to_numpy(int), d["T"].to_numpy(float), d["cluster"].to_numpy()
    print("\n  RISK DISTRIBUTION (out-of-fold, %d scored)" % ok.sum())
    for lo, hi, lbl in [(0, GREY_LO, "low   <5%"), (GREY_LO, GREY_HI, "GREY  5-20%"),
                        (GREY_HI, 1.01, "high  >20%")]:
        m = ok & (risk >= lo) & (risk < hi)
        ev = int(y[m].sum())
        print("    %-12s n=%-5d events=%-5s  observed rate %.1f%%"
              % (lbl, m.sum(), ev if ev >= MIN_EVENTS else "<10", 100 * y[m].mean() if m.sum() else 0))

    res = {"horizon_years": HORIZON, "grey_zone": [GREY_LO, GREY_HI],
           "base_terms": base, "enhancers": ENHANCERS,
           "n_scored": int(ok.sum()), "grey_n": int(grey.sum()),
           "grey_events": int(y[grey].sum()), "participant_level_outputs": False}

    if y[grey].sum() < MIN_EVENTS:
        print("\n  grey zone holds <10 events - non-estimable")
        (ROOT / "outputs" / "grey_zone_enhancers.json").write_text(json.dumps(res, indent=2))
        return

    s = d.loc[grey].reset_index(drop=True)
    ys, ts, gs = s.E.to_numpy(int), s["T"].to_numpy(float), s["cluster"].to_numpy()
    print("\n  WITHIN THE GREY ZONE  n=%d  events=%d" % (len(s), ys.sum()))

    lp_b, ok_b, c_b, sd_b, _, _ = cf.cv(s, base, resolve=False)
    print("    base model                       C=%.4f (repeat SD %.4f)" % (c_b, sd_b))
    rows = {}
    for add, lbl in [(["log_lpa"], "+ Lp(a)"),
                     (["log_apob_ldl"], "+ log(apoB/LDL-C)"),
                     (ENHANCERS, "+ BOTH enhancers")]:
        spec = base + [a for a in add if a in s and s[a].nunique(dropna=True) >= 2]
        lp_e, ok_e, c_e, sd_e, _, _ = cf.cv(s, spec, resolve=False)
        both = ok_b & ok_e
        r = boot_delta(ts[both], ys[both], lp_e[both], lp_b[both], gs[both])
        if r is None:
            print("    %-32s C=%.4f  delta non-estimable" % (lbl, c_e)); continue
        dd, lo, hi = r
        verdict = "ADDS" if lo > 0 else ("HARMS" if hi < 0 else "no gain")
        rows[lbl] = {"c_index": c_e, "delta": dd, "ci": [lo, hi], "verdict": verdict}
        print("    %-32s C=%.4f  delta %+.4f (%+.4f, %+.4f)  %s"
              % (lbl, c_e, dd, lo, hi, verdict))
    res["grey_zone_models"] = rows

    print("\n  ENHANCER EFFECT SIZES INSIDE THE GREY ZONE (HR per SD, adjusted for base)")
    hrs = {}
    for e in ENHANCERS:
        if e not in s or s[e].nunique(dropna=True) < 2:
            continue
        X = s.reindex(columns=base + [e]).astype(float)
        X = X.fillna(X.median())
        for c in X.columns:
            if X[c].nunique() > 2:
                mu, sdv = X[c].mean(), X[c].std()
                if sdv > 1e-9:
                    X[c] = (X[c] - mu) / sdv
        X["T"], X["E"] = ts, ys
        try:
            f = CoxPHFitter(penalizer=0.05).fit(X, "T", "E")
            hr = float(f.summary.loc[e, "exp(coef)"])
            lo = float(f.summary.loc[e, "exp(coef) lower 95%"])
            hi = float(f.summary.loc[e, "exp(coef) upper 95%"])
            hrs[e] = {"hr_per_sd": hr, "ci": [lo, hi],
                      "observed_pct": float(100 * s[e].notna().mean())}
            print("    %-16s HR %.3f (%.3f, %.3f)   observed in %.1f%% of the grey zone"
                  % (e, hr, lo, hi, 100 * s[e].notna().mean()))
        except Exception as exc:
            print("    %-16s not estimable (%s)" % (e, str(exc)[:40]))
    res["hazard_ratios"] = hrs

    (ROOT / "outputs" / "grey_zone_enhancers.json").write_text(json.dumps(res, indent=2))
    print("\nwritten:", ROOT / "outputs" / "grey_zone_enhancers.json")


if __name__ == "__main__":
    main()
