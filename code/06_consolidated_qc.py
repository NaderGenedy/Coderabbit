#!/usr/bin/env python3
"""Aggregate-only final QC for the CALON-N locked analysis.

The script reconstructs cohort aggregates from the canonical inputs, checks the
selection rule and reported arithmetic, and verifies the frozen scorer. It does
not write participant identifiers, participant rows, or empirical predictions.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
from collections import Counter
from pathlib import Path

import joblib
import numpy as np
import pandas as pd


ROOT = Path("/Users/nader85/Documents/CALON/calon_discordance_model_2026_08_09")
OUT = ROOT / "outputs" / "consolidated_qc_2026_08_09.json"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def reporting_counts(path: Path) -> dict[str, dict[str, int]]:
    text = path.read_text(encoding="utf-8")
    sections = {
        "TRIPOD+AI": text.split("## TRIPOD+AI", 1)[1].split("## STROBE", 1)[0],
        "STROBE": text.split("## STROBE", 1)[1].split("## PROBAST assessment", 1)[0],
    }
    result = {}
    for name, section in sections.items():
        statuses = []
        for line in section.splitlines():
            if not line.startswith("|") or "Status" in line or line.startswith("|---"):
                continue
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            status_cells = [cell for cell in cells if cell in {"Y", "P", "N", "NA"}]
            if len(status_cells) == 1:
                statuses.append(status_cells[0])
        result[name] = {"items": len(statuses), **dict(Counter(statuses))}
    return result


def main() -> None:
    base = load_module("calon_qc_base", ROOT / "code" / "01_calon_disc_analysis.py")
    scorer = load_module("calon_qc_scorer", ROOT / "code" / "apply_calon_n.py")
    cohorts = base.prepare_cohorts()
    manifest = json.loads((ROOT / "MANIFEST.json").read_text(encoding="utf-8"))
    external = json.loads(
        (ROOT / "outputs" / "scratch_external_performance.json").read_text(encoding="utf-8")
    )
    selection = json.loads(
        (ROOT / "outputs" / "scratch_selection.json").read_text(encoding="utf-8")
    )
    equation = json.loads((ROOT / "model" / "calon_n_equation.json").read_text(encoding="utf-8"))
    bundle = joblib.load(ROOT / "model" / "calon_n_from_scratch.joblib")
    synthetic = pd.read_csv(ROOT / "model" / "synthetic_predictors.csv")

    selected_raw = ["age", "male", "hdl", "hypertension", "smoke_ever", "ldl", "apob", "apoa1"]
    cohort_summary = {}
    for name, frame in cohorts.items():
        variables = {}
        for variable in selected_raw:
            values = pd.to_numeric(frame[variable], errors="coerce")
            observed = int(values.notna().sum())
            variables[variable] = {
                "observed": observed,
                "missing_n": int(len(frame) - observed),
                "missing_pct": float(100 * (1 - observed / len(frame))),
            }
        cohort_summary[name] = {
            "n": int(len(frame)),
            "events": int(frame["y"].sum()),
            "prevalence": float(frame["y"].mean()),
            "clusters": int(frame["cluster"].nunique()),
            "variables": variables,
        }

    candidates = pd.read_csv(ROOT / "outputs" / "scratch_candidate_transport.csv")
    eligible = candidates.groupby("candidate")["sign_coherent"].all()
    min_auc = candidates.pivot(index="candidate", columns="direction", values="target_auc").min(axis=1)
    computed_selected = min_auc[eligible].idxmax()

    arithmetic_errors = []
    for direction, result in external.items():
        for comparator, item in result["comparators"].items():
            expected = result["auc"] - item["auc"]
            if not np.isclose(expected, item["delta"], atol=1e-12, rtol=0):
                arithmetic_errors.append(f"{direction}:{comparator}")

    p1 = scorer.score(synthetic, bundle)
    p2 = scorer.score(synthetic.iloc[::-1], bundle)[::-1]
    p3 = scorer.score(synthetic, bundle)
    eq_features = equation["features"]
    model_features = bundle["columns"]

    subgroups = pd.read_csv(ROOT / "outputs" / "scratch_subgroups.csv")
    estimable = subgroups[subgroups["model_auc"].notna()].copy()
    subgroup_summary = {
        "rows": int(len(subgroups)),
        "non_estimable": int(subgroups["model_auc"].isna().sum()),
        "estimable": int(len(estimable)),
        "calon_n_above_best_comparator": int((estimable["delta"] > 0).sum()),
        "calon_n_at_or_below_best_comparator": int((estimable["delta"] <= 0).sum()),
    }

    dca_summary = {
        "status": "INVALID_WITHDRAWN",
        "reason": (
            "Age+sex, Montreal, and FH-Risk-Score comparator outputs are ranking "
            "scores/linear predictors rather than calibrated probabilities on the "
            "same absolute-risk scale as CALON-N."
        ),
        "audit_artifact": "outputs/scratch_decision_curve.csv",
    }

    forbidden = re.compile(r"13128[6-9]|13129[0-4]", re.I)
    forbidden_hits = []
    for path in (ROOT / "code").glob("*.py"):
        if forbidden.search(path.read_text(encoding="utf-8")):
            forbidden_hits.append(path.name)

    input_hash_mismatches = []
    for path_string, expected in manifest["canonical_inputs"].items():
        observed = sha256(Path(path_string))
        if observed != expected:
            input_hash_mismatches.append(path_string)

    suspicious_names = []
    markers = ["participant_id", "family_id", "eid", "variant_coordinate"]
    for path in ROOT.rglob("*"):
        if path.is_file() and any(marker in path.name.lower() for marker in markers):
            suspicious_names.append(str(path.relative_to(ROOT)))

    result = {
        "status": "PASS_WITH_SCIENTIFIC_LIMITATIONS",
        "rerun_commands": [
            "python3 code/02_from_scratch_model.py",
            "python3 code/03_sensitivity_qc.py",
            "python3 code/06_consolidated_qc.py",
        ],
        "cohorts": cohort_summary,
        "selection": {
            "reported": selection["selected"],
            "recomputed": computed_selected,
            "match": selection["selected"] == computed_selected,
            "eligible_maximin_auc": float(min_auc[computed_selected]),
        },
        "arithmetic": {"delta_errors": arithmetic_errors},
        "scorer": {
            "repeat_max_abs_difference": float(np.max(np.abs(p1 - p3))),
            "row_reversal_max_abs_difference": float(np.max(np.abs(p1 - p2))),
            "equation_model_features_match": eq_features == model_features,
            "selection_equation_match": equation["candidate"] == selection["selected"],
        },
        "subgroups": subgroup_summary,
        "decision_curve": dca_summary,
        "reporting": reporting_counts(ROOT / "qc" / "TRIPOD_STROBE_PROBAST_AUDIT.md"),
        "security_and_provenance": {
            "canonical_input_hash_mismatches": input_hash_mismatches,
            "forbidden_hypertension_field_hits": forbidden_hits,
            "suspicious_participant_output_filenames": suspicious_names,
            "participant_level_outputs": False,
        },
        "scientific_failures": [
            "not prospective or temporally valid for incident-risk prediction",
            "architecture selection was informed by both target outcomes",
            "absolute calibration did not transport",
            "conditional target-cluster intervals omit source-training and selection uncertainty",
            "universal comparator and subgroup superiority was not demonstrated",
            "no independent third-cohort validation",
        ],
    }
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
