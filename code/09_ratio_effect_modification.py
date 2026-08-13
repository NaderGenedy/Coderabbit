#!/usr/bin/env python3
"""Where does apoB/LDL-C discordance actually carry signal?

Question
--------
The ratio adds little on average. In WHICH stratum is it worth most, is that
stratum reproducible in a second cohort, and does it transport to matched
non-carriers?

Design
------
Primary pre-specified split: TREATMENT STATUS. A high apoB/LDL-C ratio arises by
two opposite routes - an untreated particle-rich phenotype (more particles per
unit cholesterol) or treatment that lowered LDL-C proportionally more than apoB.
These carry opposite causal meaning and must not be pooled.

Secondary modifiers, pre-specified and kept continuous where possible:
    apoB, age, TG/HDL-C, HDL-C, sex, diabetes, ever smoking

Method
------
Logistic regression of established ASCVD on standardised log(apoB/LDL-C), its
interaction with each modifier, and the CALON-N covariate set, with cluster-robust
standard errors (family in the clinic, qualifying-variant component in UK Biobank,
individual in the unrelated non-carrier sample). The INTERACTION is tested; within-
stratum estimates are reported for interpretation only, never as the test.

Discovery and confirmation are separated: a modifier is only claimed if the
interaction replicates with the same sign in a cohort not used to find it.

Governance: aggregate output only. Strata with fewer than 10 events are reported
as non-estimable rather than estimated.
"""
from __future__ import annotations

import os

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

ROOT = Path(os.environ["CALON_PROJECT_ROOT"])
OUT = ROOT / "outputs"
SEED = 20260810
MIN_EVENTS = 10

spec = importlib.util.spec_from_file_location("fhnf", ROOT / "code" / "07_fh_vs_nonfh.py")
f = importlib.util.module_from_spec(spec)
sys.modules["fhnf"] = f
spec.loader.exec_module(f)

COVARS = ["age", "male", "hdl", "hypertension", "smoke_ever"]
MODIFIERS = [("treatment", "binary"), ("apob", "continuous"), ("age", "continuous"),
             ("log_tghdl", "continuous"), ("hdl", "continuous"), ("male", "binary"),
             ("diabetes", "binary"), ("smoke_ever", "binary")]


def prep(d):
    """Standardised log ratio plus complete covariates; aggregate-safe."""
    q = d.copy()
    q["log_ratio"] = np.log((pd.to_numeric(q["apob"], errors="coerce")
                             / pd.to_numeric(q["ldl"], errors="coerce")).where(lambda z: z.gt(0)))
    for c in set(COVARS + [m for m, _ in MODIFIERS] + ["log_ratio", "ldl", "apob"]):
        if c in q:
            q[c] = pd.to_numeric(q[c], errors="coerce")
            q[c] = q[c].fillna(q[c].median())
    s = q["log_ratio"].std()
    q["z_ratio"] = (q["log_ratio"] - q["log_ratio"].mean()) / (s if s > 1e-9 else 1.0)
    return q


def fit_interaction(d, modifier, kind, cluster):
    """Return the ratio main effect, the interaction, and its cluster-robust p."""
    q = d.copy()
    if kind == "continuous":
        m = q[modifier]
        q["_mod"] = (m - m.mean()) / (m.std() if m.std() > 1e-9 else 1.0)
    else:
        q["_mod"] = q[modifier].clip(0, 1)
    q["_int"] = q["z_ratio"] * q["_mod"]

    terms = ["z_ratio", "_mod", "_int"] + [c for c in COVARS if c != modifier]
    X = sm.add_constant(q[terms].astype(float), has_constant="add")
    y = q["y"].astype(int).to_numpy()
    try:
        res = sm.GLM(y, X, family=sm.families.Binomial()).fit(
            cov_type="cluster", cov_kwds={"groups": np.asarray(cluster)})
    except Exception as exc:                     # separation or singular design
        return {"modifier": modifier, "error": str(exc)[:120]}
    return {"modifier": modifier, "kind": kind,
            "or_ratio_at_modifier_zero": float(np.exp(res.params["z_ratio"])),
            "interaction_or": float(np.exp(res.params["_int"])),
            "interaction_ci": [float(np.exp(res.conf_int().loc["_int", 0])),
                               float(np.exp(res.conf_int().loc["_int", 1]))],
            "interaction_p": float(res.pvalues["_int"])}


def stratum_estimates(d, modifier, cluster):
    """Descriptive within-stratum ORs for a binary modifier; never the test."""
    rows = []
    for level in (0, 1):
        s = d.loc[d[modifier].clip(0, 1).eq(level)]
        ev = int(s["y"].sum())
        if ev < MIN_EVENTS or len(s) - ev < MIN_EVENTS:
            rows.append({"level": level, "n": int(len(s)), "events": "<10 non-estimable"})
            continue
        X = sm.add_constant(s[["z_ratio"] + [c for c in COVARS if c != modifier]].astype(float),
                            has_constant="add")
        try:
            r = sm.GLM(s["y"].astype(int).to_numpy(), X, family=sm.families.Binomial()).fit(
                cov_type="cluster", cov_kwds={"groups": np.asarray(cluster)[s.index]})
            rows.append({"level": level, "n": int(len(s)), "events": ev,
                         "or_per_sd": float(np.exp(r.params["z_ratio"])),
                         "ci": [float(np.exp(r.conf_int().loc["z_ratio", 0])),
                                float(np.exp(r.conf_int().loc["z_ratio", 1]))]})
        except Exception as exc:
            rows.append({"level": level, "n": int(len(s)), "events": ev, "error": str(exc)[:90]})
    return rows


def ratio_effect_across(d, modifier, cluster, n_band=4):
    """Ratio OR within quartile bands of a continuous modifier - shows where it peaks."""
    q = d.copy()
    try:
        q["_band"] = pd.qcut(q[modifier], n_band, labels=False, duplicates="drop")
    except Exception:
        return []
    rows = []
    for b in sorted(q["_band"].dropna().unique()):
        s = q.loc[q["_band"].eq(b)]
        ev = int(s["y"].sum())
        lo, hi = float(s[modifier].min()), float(s[modifier].max())
        if ev < MIN_EVENTS or len(s) - ev < MIN_EVENTS:
            rows.append({"band": int(b), "range": [lo, hi], "n": int(len(s)),
                         "events": "<10 non-estimable"})
            continue
        X = sm.add_constant(s[["z_ratio"] + [c for c in COVARS if c != modifier]].astype(float),
                            has_constant="add")
        try:
            r = sm.GLM(s["y"].astype(int).to_numpy(), X, family=sm.families.Binomial()).fit(
                cov_type="cluster", cov_kwds={"groups": np.asarray(cluster)[s.index]})
            rows.append({"band": int(b), "range": [lo, hi], "n": int(len(s)), "events": ev,
                         "or_per_sd": float(np.exp(r.params["z_ratio"])),
                         "ci": [float(np.exp(r.conf_int().loc["z_ratio", 0])),
                                float(np.exp(r.conf_int().loc["z_ratio", 1]))]})
        except Exception as exc:
            rows.append({"band": int(b), "range": [lo, hi], "n": int(len(s)),
                         "events": ev, "error": str(exc)[:90]})
    return rows


def run_cohort(name, d, cluster):
    d = prep(d)
    block = {"cohort": name, "n": int(len(d)), "events": int(d["y"].sum()),
             "interactions": [], "treatment_strata": [], "gradients": {}}
    for mod, kind in MODIFIERS:
        if mod not in d:
            continue
        block["interactions"].append(fit_interaction(d, mod, kind, cluster))
    if "treatment" in d:
        block["treatment_strata"] = stratum_estimates(d, "treatment", cluster)
    for mod in ("apob", "age", "log_tghdl"):
        if mod in d:
            block["gradients"][mod] = ratio_effect_across(d, mod, cluster)
    return block


def main():
    cohorts = f.m.prepare_cohorts()
    dragon = cohorts["dragon"]
    strict = cohorts["ukb_strict"]

    fh, pool = None, None
    import importlib
    rb = importlib.import_module("fhnf")
    # rebuild the matched non-carrier arm exactly as in script 07
    spec2 = importlib.util.spec_from_file_location("rob", ROOT / "code" / "08_fh_vs_nonfh_robustness.py")
    rob = importlib.util.module_from_spec(spec2)
    sys.modules["rob"] = rob
    spec2.loader.exec_module(rob)
    fh_u, nc_pool = rob.build()
    keep, ctrl = f.match(fh_u["age"].to_numpy(float), fh_u["male"].to_numpy(float),
                         nc_pool, 5, 1.0, SEED)
    ctrl = ctrl.reset_index(drop=True)
    ctrl["cluster"] = np.arange(len(ctrl))

    out = {"seed": SEED, "min_events_per_cell": MIN_EVENTS,
           "primary_prespecified_modifier": "treatment",
           "participant_level_outputs": False, "cohorts": []}
    for name, d, cl in [("DRAGON clinic", dragon, dragon["cluster"].to_numpy()),
                        ("UKB strict carriers", strict, strict["cluster"].to_numpy()),
                        ("UKB matched non-carriers", ctrl, ctrl["cluster"].to_numpy())]:
        out["cohorts"].append(run_cohort(name, d, cl))

    (OUT / "ratio_effect_modification.json").write_text(json.dumps(out, indent=1))

    for c in out["cohorts"]:
        print("\n" + "=" * 92)
        print("%s   n=%d  events=%d" % (c["cohort"], c["n"], c["events"]))
        print("  interaction of log(apoB/LDL-C) with each modifier (cluster-robust):")
        for r in sorted([x for x in c["interactions"] if "interaction_p" in x],
                        key=lambda x: x["interaction_p"]):
            print("     %-12s interaction OR %5.2f (%4.2f-%5.2f)  p=%.3f"
                  % (r["modifier"], r["interaction_or"], r["interaction_ci"][0],
                     r["interaction_ci"][1], r["interaction_p"]))
        if c["treatment_strata"]:
            print("  PRIMARY SPLIT - ratio OR per SD within treatment strata:")
            for r in c["treatment_strata"]:
                lbl = "untreated" if r["level"] == 0 else "treated  "
                if "or_per_sd" in r:
                    print("     %s n=%-5d events=%-4d OR %.2f (%.2f-%.2f)"
                          % (lbl, r["n"], r["events"], r["or_per_sd"], *r["ci"]))
                else:
                    print("     %s n=%-5d %s" % (lbl, r["n"], r.get("events", r.get("error"))))
        for mod, rows in c["gradients"].items():
            shown = [r for r in rows if "or_per_sd" in r]
            if not shown:
                continue
            print("  ratio OR per SD across %s quartiles:" % mod)
            for r in rows:
                if "or_per_sd" in r:
                    print("     Q%d [%6.2f,%6.2f] n=%-5d ev=%-4d OR %.2f (%.2f-%.2f)"
                          % (r["band"] + 1, r["range"][0], r["range"][1], r["n"],
                             r["events"], r["or_per_sd"], *r["ci"]))
                else:
                    print("     Q%d [%6.2f,%6.2f] n=%-5d %s"
                          % (r["band"] + 1, r["range"][0], r["range"][1], r["n"],
                             r.get("events", "")))
    print("\nwritten:", OUT / "ratio_effect_modification.json")


if __name__ == "__main__":
    main()
