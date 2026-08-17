#!/usr/bin/env python3
"""Does CALON-N work once it is updated to the setting it is used in?

Transporting a frozen equation to a new setting and reporting its raw
probabilities is the hardest possible test, and it is the one the manuscript
currently reports. Standard practice for deployment is model UPDATING: keep the
transported linear predictor, re-estimate the intercept (recalibration-in-the-
large), and optionally the slope, in the receiving setting.

This quantifies what updating buys. To avoid crediting the model with in-sample
optimism, the updating parameters are estimated by grouped cross-validation
inside the target: the intercept/slope are fitted on k-1 folds of clusters and
applied to the held-out fold, so every reported probability is out-of-fold.

Discrimination is invariant to these monotone transforms, so AUC is unchanged by
construction; the question is entirely whether calibration can be restored.

Governance: aggregate output only.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GroupKFold

ROOT = Path("/Users/nader85/Documents/CALON/calon_discordance_model_2026_08_09")
OUT = ROOT / "outputs"
SEED = 20260810
SPEC = ["age", "male", "hdl", "hypertension", "smoke_ever", "log_ratio", "log_apoa1"]

spec = importlib.util.spec_from_file_location("calon_base", ROOT / "code" / "01_calon_disc_analysis.py")
m = importlib.util.module_from_spec(spec)
sys.modules["calon_base"] = m
spec.loader.exec_module(m)


def logit(p):
    p = np.clip(p, 1e-6, 1 - 1e-6)
    return np.log(p / (1 - p))


def metrics(y, p):
    y = np.asarray(y, int)
    p = np.clip(np.asarray(p, float), 1e-6, 1 - 1e-6)
    obs = y.mean()
    brier = float(np.mean((p - y) ** 2))
    null = float(np.mean((obs - y) ** 2))
    return {"auc": float(roc_auc_score(y, p)), "brier": brier,
            "scaled_brier_pct": float(100 * (1 - brier / null)) if null > 0 else float("nan"),
            "expected_pct": float(100 * p.mean()), "observed_pct": float(100 * obs),
            "E_O": float(p.mean() / obs) if obs > 0 else float("nan")}


def cv_update(lp, y, groups, mode, n_splits=5):
    """Out-of-fold updated probabilities. mode: 'intercept' or 'intercept_slope'."""
    lp, y, groups = np.asarray(lp, float), np.asarray(y, int), np.asarray(groups)
    out = np.full(len(y), np.nan)
    uniq = pd.unique(pd.Series(groups))
    k = min(n_splits, len(uniq))
    if k < 2:
        return out
    for tr, te in GroupKFold(n_splits=k).split(lp.reshape(-1, 1), y, groups):
        if len(np.unique(y[tr])) < 2:
            continue
        if mode == "intercept":
            # slope fixed at 1: fit only an offset, by 1-D search on the log-likelihood
            a = np.linspace(-8, 8, 4001)
            ll = [(y[tr] * (lp[tr] + ai) - np.log1p(np.exp(lp[tr] + ai))).sum() for ai in a]
            out[te] = 1 / (1 + np.exp(-(lp[te] + a[int(np.argmax(ll))])))
        else:
            mdl = LogisticRegression(C=1e6, max_iter=5000).fit(lp[tr].reshape(-1, 1), y[tr])
            out[te] = mdl.predict_proba(lp[te].reshape(-1, 1))[:, 1]
    return out


def main():
    c = m.prepare_cohorts()
    for d in c.values():
        d["log_ratio"] = np.log((d["apob"] / d["ldl"]).where(lambda z: z.gt(0)))
        d["log_apoa1"] = np.log(d["apoa1"])
    m.CANDIDATES = {"calon_n": SPEC}

    res = {"seed": SEED, "spec": SPEC, "participant_level_outputs": False,
           "note": "updating parameters estimated out-of-fold within the target",
           "transports": []}

    for tag, src, tgt in [("DRAGON -> UKB strict", c["dragon"], c["ukb_strict"]),
                          ("UKB strict -> DRAGON", c["ukb_strict"], c["dragon"]),
                          ("DRAGON -> UKB union", c["dragon"], c["ukb_union"])]:
        pen, _ = m.choose_penalty(src, "calon_n", SEED)
        bundle = m.fit_candidate(src, "calon_n", pen)
        p_raw = m.predict_candidate(bundle, tgt)
        y = tgt["y"].to_numpy(int)
        g = tgt["cluster"].to_numpy()
        lp = logit(p_raw)

        block = {"transport": tag, "n": int(len(tgt)), "events": int(y.sum()),
                 "penalty": float(pen),
                 "as_transported": metrics(y, p_raw)}
        for mode, label in [("intercept", "after_intercept_update"),
                            ("intercept_slope", "after_intercept_and_slope_update")]:
            pu = cv_update(lp, y, g, mode)
            ok = ~np.isnan(pu)
            block[label] = metrics(y[ok], pu[ok]) if ok.sum() > 20 else {"status": "not_estimable"}
        res["transports"].append(block)

    (OUT / "recalibration.json").write_text(json.dumps(res, indent=2))

    print("%-22s %-32s %7s %7s %8s %8s" % ("transport", "state", "AUC", "E:O", "Brier", "scaled%"))
    for b in res["transports"]:
        print("-" * 92)
        for key, lbl in [("as_transported", "as transported (current paper)"),
                         ("after_intercept_update", "+ intercept update (1 param)"),
                         ("after_intercept_and_slope_update", "+ intercept & slope (2 param)")]:
            r = b.get(key, {})
            if "auc" not in r:
                print("%-22s %-32s %s" % (b["transport"][:22], lbl, r.get("status", "-")))
                continue
            print("%-22s %-32s %7.3f %7.2f %8.4f %+8.1f"
                  % (b["transport"][:22], lbl, r["auc"], r["E_O"], r["brier"], r["scaled_brier_pct"]))
    print("\nwritten:", OUT / "recalibration.json")


if __name__ == "__main__":
    main()
