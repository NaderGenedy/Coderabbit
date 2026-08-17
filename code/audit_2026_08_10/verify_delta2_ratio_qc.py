#!/usr/bin/env python3
"""Aggregate-only verification of the DELTA 2 apoB/LDL-C decomposition.

This script intentionally writes no participant rows, identifiers, matched-set
assignments, variant data, or participant-level predictions. It reuses the
locked cohort construction and matching functions, then reports only cohort-
level correlations and cluster-robust regression summaries. Event counts below
10 are suppressed.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm


ROOT = Path("/Users/nader85/Documents/CALON/calon_discordance_model_2026_08_09")
OUT = ROOT / "outputs" / "audit_2026_08_10" / "delta2_ratio_qc_verification.json"
SEED = 20260810
MIN_EVENTS = 10


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


fhnf = load_module("delta2_fhnf", ROOT / "code" / "07_fh_vs_nonfh.py")
robust = load_module("delta2_robust", ROOT / "code" / "08_fh_vs_nonfh_robustness.py")


def event_value(n: int):
    return int(n) if n >= MIN_EVENTS else "<10, non-estimable"


def fit_glm(q: pd.DataFrame, terms: list[str], cluster: np.ndarray):
    x = sm.add_constant(q[terms].astype(float), has_constant="add")
    result = sm.GLM(q["y"].astype(int).to_numpy(), x,
                    family=sm.families.Binomial()).fit(
        cov_type="cluster", cov_kwds={"groups": np.asarray(cluster)})
    return {
        term: {
            "coefficient": float(result.params[term]),
            "ci_95": [float(result.conf_int().loc[term, 0]),
                      float(result.conf_int().loc[term, 1])],
            "p": float(result.pvalues[term]),
        }
        for term in terms if term in {"log_apob", "log_ldl"}
    }


def verify_cohort(name: str, frame: pd.DataFrame, clusters: np.ndarray):
    q = frame.copy()
    for col in ("y", "age", "male", "hdl", "apob", "ldl"):
        q[col] = pd.to_numeric(q[col], errors="coerce")
    q["log_apob"] = np.log(q["apob"].where(q["apob"].gt(0)))
    q["log_ldl"] = np.log(q["ldl"].where(q["ldl"].gt(0)))
    q["log_ratio"] = q["log_apob"] - q["log_ldl"]
    corr_keep = q[["log_ratio", "log_apob", "log_ldl"]].notna().all(axis=1)
    corr_q = q.loc[corr_keep]
    keep = q[["y", "age", "male", "hdl", "log_apob", "log_ldl"]].notna().all(axis=1)
    qc = q.loc[keep].copy()
    cl = np.asarray(clusters)[keep.to_numpy()]
    events = int(qc["y"].sum())

    joint = fit_glm(qc, ["age", "male", "hdl", "log_apob", "log_ldl"], cl)
    ldl_only = fit_glm(qc, ["age", "male", "hdl", "log_ldl"], cl)
    return {
        "cohort": name,
        "n_complete": int(len(qc)),
        "events": event_value(events),
        "correlations": {
            "n_with_both_components": int(len(corr_q)),
            "log_ratio_with_log_apob": float(corr_q["log_ratio"].corr(corr_q["log_apob"])),
            "log_ratio_with_log_ldl": float(corr_q["log_ratio"].corr(corr_q["log_ldl"])),
        },
        "joint_age_sex_hdl_adjusted_cluster_robust": joint,
        "ldl_only_age_sex_hdl_adjusted_cluster_robust": ldl_only["log_ldl"],
    }


def main():
    cohorts = fhnf.m.prepare_cohorts()
    dragon = cohorts["dragon"].copy()
    strict = cohorts["ukb_strict"].copy()

    fh, noncarrier_pool = robust.build()
    keep, controls = fhnf.match(
        fh["age"].to_numpy(float), fh["male"].to_numpy(float),
        noncarrier_pool, ratio=5, calliper=1.0, seed=SEED)
    if len(keep) != len(fh) or len(controls) != 5 * len(fh):
        raise RuntimeError("The locked 1:5 matching frame was not reproduced")
    controls = controls.reset_index(drop=True)

    blocks = [
        verify_cohort("DRAGON clinic", dragon, dragon["cluster"].to_numpy()),
        verify_cohort("UKB strict carriers", strict, strict["cluster"].to_numpy()),
        verify_cohort("UKB age/sex-matched non-carriers", controls,
                      np.arange(len(controls))),
    ]
    out = {
        "task": "DELTA 2 aggregate verification of apoB/LDL-C component structure",
        "seed": SEED,
        "participant_level_outputs": False,
        "estimand": "Established-ASCVD log odds adjusted for age, sex, and HDL-C",
        "cohorts": blocks,
        "interpretation_limit": (
            "Cross-sectional coefficients can verify the inverse-LDL signature but "
            "cannot identify treatment as its cause without correctly coded treatment "
            "exposure and pre-treatment biomarker timing."
        ),
    }
    OUT.write_text(json.dumps(out, indent=2) + "\n")
    for b in blocks:
        print(
            b["cohort"],
            "n=", b["n_complete"],
            "events=", b["events"],
            "corr_ratio_apob=", round(b["correlations"]["log_ratio_with_log_apob"], 3),
            "corr_ratio_ldl=", round(b["correlations"]["log_ratio_with_log_ldl"], 3),
        )
    print("written:", OUT)


if __name__ == "__main__":
    main()
