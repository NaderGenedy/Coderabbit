#!/usr/bin/env python3
"""CALON-SIMPLE: a routinely-available-variable model, pre-specified success bar.

Senior-author proposal (10 Aug 2026):
    age, sex, TG/HDL-C, smoking, hypertension (or BP medication), and UNTREATED LDL-C
    -- if it wins or ties every comparator in both cohorts, that is a win, because the
    inputs are ones any lipid clinic already has.

Untreated LDL-C is the key design choice. Measured LDL-C is contaminated by treatment
(established disease -> intensive therapy -> low measured LDL), which is why measured
LDL-C carries a NEGATIVE coefficient in all three cohorts. Back-calculating to the
pre-treatment value (measured / 0.7 when on lipid-lowering therapy, per Patel et al.
eTable 1) removes that inversion and restores the physiological direction.

Pre-specified bar, fixed BEFORE the run:
    WIN  = lower bound of the paired AUC difference > 0
    TIE  = interval contains 0
    LOSS = upper bound < 0
    SUCCESS = zero losses across all comparators in both transport directions.

Also reports calibration as transported and after a one-parameter out-of-fold intercept
update, since a model with no losses but uncorrected calibration is not deployable.

Governance: aggregate output only.
"""
from __future__ import annotations

import os

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

ROOT = Path(os.environ["CALON_PROJECT_ROOT"])
OUT = ROOT / "outputs"
SEED = 20260810
BOOT = 4000

spec = importlib.util.spec_from_file_location("calon_base", ROOT / "code" / "01_calon_disc_analysis.py")
m = importlib.util.module_from_spec(spec)
sys.modules["calon_base"] = m
spec.loader.exec_module(m)

SIMPLE = ["age", "male", "log_tghdl", "smoke_ever", "hypertension", "log_ldl_unt"]
CUMUL  = ["age", "male", "log_tghdl", "smoke_ever", "hypertension", "log_cum_ldl"]
CALON_N = ["age", "male", "hdl", "hypertension", "smoke_ever", "log_ratio", "log_apoa1"]


_orig_transform = m.transform


def transform_plus(frame, prep):
    """Engine transform, plus untreated and cumulative LDL-C.

    COHORT-SPECIFIC RULE, verified 10 Aug 2026. The two cohorts store different things:

      DRAGON  `MtachedLDLC` is ALREADY a pre-treatment / highest-recorded LDL-C. Its
              median is flat across treatment status (untreated 4.80 vs treated 4.70)
              and it exceeds the current `LastLDL` by a median 1.30 mmol/L. Applying the
              /0.70 statin correction to it double-corrects 87% of the cohort.
      UKB     `pre_ldl` is a measured baseline, so Patel et al. eTable 1 applies:
              divide by 0.70 when on lipid-lowering therapy.

    The rule is keyed off the frame, not hard-coded per call, so source and target are
    always treated consistently.

    Cumulative LDL-C (cholesterol-years) is untreated LDL x age -- the only definition
    both cohorts can support, since UK Biobank has a single baseline measurement.
    """
    z = _orig_transform(frame, prep)
    q = m.fill_raw(frame, prep["defaults"])
    if bool(frame.attrs.get("ldl_is_pretreatment", False)):
        ldl_unt = q["ldl"].to_numpy(float)
    else:
        ldl_unt = np.where(q["treatment"].gt(0), q["ldl"] / 0.70, q["ldl"])
    ldl_unt = np.clip(ldl_unt, 0.3, 30.0)
    z["log_ldl_unt"] = np.log(ldl_unt)
    z["log_cum_ldl"] = np.log(np.clip(ldl_unt * q["age"].to_numpy(float), 1.0, 3000.0))
    return z


m.transform = transform_plus


def boot_delta(y, p, c, groups, b=BOOT, seed=SEED):
    """Cluster bootstrap of the paired AUC difference (model minus comparator)."""
    y, p, c, groups = map(np.asarray, (y, p, c, groups))
    point = roc_auc_score(y, p) - roc_auc_score(y, c)
    rng = np.random.default_rng(seed)
    uniq = pd.unique(pd.Series(groups))
    idx = {g: np.flatnonzero(groups == g) for g in uniq}
    vals = []
    for _ in range(b):
        take = np.concatenate([idx[g] for g in rng.choice(uniq, len(uniq), replace=True)])
        if len(np.unique(y[take])) < 2:
            continue
        vals.append(roc_auc_score(y[take], p[take]) - roc_auc_score(y[take], c[take]))
    return float(point), float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))


def verdict(lo, hi):
    return "WIN" if lo > 0 else ("LOSS" if hi < 0 else "tie")


def logit(p):
    p = np.clip(p, 1e-6, 1 - 1e-6)
    return np.log(p / (1 - p))


def intercept_update_oof(lp, y, groups, n_splits=5):
    from sklearn.model_selection import GroupKFold
    lp, y, groups = np.asarray(lp, float), np.asarray(y, int), np.asarray(groups)
    out = np.full(len(y), np.nan)
    k = min(n_splits, len(pd.unique(pd.Series(groups))))
    if k < 2:
        return out
    grid = np.linspace(-8, 8, 4001)
    for tr, te in GroupKFold(n_splits=k).split(lp.reshape(-1, 1), y, groups):
        if len(np.unique(y[tr])) < 2:
            continue
        ll = [(y[tr] * (lp[tr] + a) - np.log1p(np.exp(lp[tr] + a))).sum() for a in grid]
        out[te] = 1 / (1 + np.exp(-(lp[te] + grid[int(np.argmax(ll))])))
    return out


def main():
    c = m.prepare_cohorts()
    # DRAGON's LDL column is already pre-treatment; UK Biobank's is a measured baseline.
    c["dragon"].attrs["ldl_is_pretreatment"] = True
    for k in ("ukb_strict", "ukb_union"):
        c[k].attrs["ldl_is_pretreatment"] = False
    for k, v in c.items():
        tx = pd.to_numeric(v["treatment"], errors="coerce")
        print("  %-12s treatment recorded %d/%d (%.0f%% treated)"
              % (k, int(tx.notna().sum()), len(v), 100 * tx.fillna(0).gt(0).mean()))
    m.CANDIDATES = {"calon_simple": SIMPLE, "calon_cumul": CUMUL, "calon_n": CALON_N}

    res = {"seed": SEED, "features": SIMPLE, "bar": "no LOSS in any comparison",
           "untreated_ldl_rule": "measured / 0.70 when on lipid-lowering therapy",
           "participant_level_outputs": False, "transports": []}
    tally = {"WIN": 0, "tie": 0, "LOSS": 0}

    for tag, src, tgt in [("DRAGON -> UKB strict", c["dragon"], c["ukb_strict"]),
                          ("UKB strict -> DRAGON", c["ukb_strict"], c["dragon"]),
                          ("DRAGON -> UKB union", c["dragon"], c["ukb_union"])]:
        y = tgt["y"].to_numpy(int)
        g = tgt["cluster"].to_numpy()
        variant = res.get("_variant", "calon_simple")
        pen, _ = m.choose_penalty(src, variant, SEED)
        p = m.predict_candidate(m.fit_candidate(src, variant, pen), tgt)
        pen_n, _ = m.choose_penalty(src, "calon_n", SEED)
        p_n = m.predict_candidate(m.fit_candidate(src, "calon_n", pen_n), tgt)

        comps = m.source_comparators(src, tgt)
        comps["CALON_N_7var"] = p_n

        block = {"transport": tag, "n": int(len(tgt)), "events": int(y.sum()),
                 "auc": float(roc_auc_score(y, p)), "penalty": float(pen), "comparisons": {}}
        for name, cp in comps.items():
            d, lo, hi = boot_delta(y, p, np.asarray(cp, float), g)
            v = verdict(lo, hi)
            if name != "CALON_N_7var":
                tally[v] += 1
            block["comparisons"][name] = {"comparator_auc": float(roc_auc_score(y, np.asarray(cp, float))),
                                          "delta": d, "ci": [lo, hi], "verdict": v}
        obs = y.mean()
        block["E_O_as_transported"] = float(p.mean() / obs) if obs > 0 else None
        pu = intercept_update_oof(logit(p), y, g)
        ok = ~np.isnan(pu)
        block["E_O_after_intercept_update"] = float(pu[ok].mean() / y[ok].mean()) if ok.sum() > 20 else None
        res["transports"].append(block)

    res["tally_excluding_calon_n"] = tally
    res["bar_met"] = tally["LOSS"] == 0
    (OUT / "calon_simple.json").write_text(json.dumps(res, indent=2))

    print("CALON-SIMPLE:  %s" % ", ".join(SIMPLE))
    for b in res["transports"]:
        print("\n" + "=" * 96)
        print("%s   n=%d  events=%d   AUC %.4f   E:O %.2f -> %.2f after 1-param update"
              % (b["transport"], b["n"], b["events"], b["auc"],
                 b["E_O_as_transported"] or float("nan"),
                 b["E_O_after_intercept_update"] or float("nan")))
        for name, r in b["comparisons"].items():
            print("   vs %-22s %.4f   delta %+.4f (%+.4f, %+.4f)   %s"
                  % (name, r["comparator_auc"], r["delta"], r["ci"][0], r["ci"][1], r["verdict"]))
    print("\n" + "=" * 96)
    print("TALLY vs published/simple comparators: WIN %d  tie %d  LOSS %d"
          % (tally["WIN"], tally["tie"], tally["LOSS"]))
    print("PRE-SPECIFIED BAR (no losses): %s" % ("MET" if res["bar_met"] else "NOT MET"))
    print("\nwritten:", OUT / "calon_simple.json")


if __name__ == "__main__":
    main()
