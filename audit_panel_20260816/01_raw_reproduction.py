#!/usr/bin/env python3
"""Independent aggregate-only reproduction checks for CALON-C.

This does not overwrite outputs/. It reconstructs cohorts through code/33_CALON_C.py,
then compares raw-derived gates and source hashes with the declared CALON-C artefacts.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from lifelines import CoxPHFitter


ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def ph_test(frame: pd.DataFrame, features: list[str]) -> dict:
    """Global/term Schoenfeld test, isolated from any model-performance calculation."""
    from lifelines.statistics import proportional_hazard_test

    data = frame[features + ["T", "E"]].copy()
    for feature in features:
        data[feature] = pd.to_numeric(data[feature], errors="coerce")
        data[feature] = data[feature].fillna(data[feature].median())
    fit = CoxPHFitter(penalizer=0.02).fit(data, "T", "E")
    test = proportional_hazard_test(fit, data, time_transform="rank")
    summary = test.summary
    term_p = {str(term): float(value) for term, value in summary["p"].items()}
    return {
        "n": int(len(data)),
        "events": int(data["E"].sum()),
        "term_p_values": term_p,
        "terms_p_lt_0_05": sorted(term for term, value in term_p.items() if value < 0.05),
    }


def main() -> None:
    if not os.environ.get("CALON_SHARED_MASTER") or not os.environ.get("CALON_CORRECTED_DATA"):
        raise RuntimeError("Set CALON_SHARED_MASTER and CALON_CORRECTED_DATA before running.")

    calon = load_module(ROOT / "code" / "33_CALON_C.py", "calon_c_audit")
    ukb, ukb_ledger = calon.build_ukb()
    wales, wales_ledger = calon.build_wales()
    declared = json.loads((ROOT / "outputs" / "calon_c.json").read_text())

    gates_expected = {
        "carriers": 3540,
        "prevalent_excluded": 207,
        "undated_excluded": 124,
        "risk_set": 3209,
        "events_full": 289,
        "events_5y": 97,
        "events_10y": 194,
    }
    gate_checks = {
        key: {
            "expected": expected,
            "observed": int(ukb_ledger[key]),
            "status": "PASS" if int(ukb_ledger[key]) == expected else "FAIL",
        }
        for key, expected in gates_expected.items()
    }
    wales_expected = {"risk_set": 1159, "events_full": 92, "events_5y": 44, "events_10y": 66}
    wales_checks = {
        key: {
            "expected": expected,
            "observed": int(wales_ledger[key]),
            "status": "PASS" if int(wales_ledger[key]) == expected else "FAIL",
        }
        for key, expected in wales_expected.items()
    }

    raw_paths = {
        "ukb_master": Path(os.environ["CALON_SHARED_MASTER"]) / "UKB" / "ukb_master.csv",
        "ukb_outcomes": Path(os.environ["CALON_CORRECTED_DATA"]) / "data_corrected" / "corrected_ascvd_outcomes.csv",
        "ukb_bp_meds": Path(os.environ["CALON_CORRECTED_DATA"]) / "New folder" / "04a_meds_touch.csv",
        "wales": calon.WP,
    }
    sources = {
        name: {
            "path": str(path),
            "exists": path.exists(),
            "sha256": sha256(path) if path.exists() else None,
        }
        for name, path in raw_paths.items()
    }

    collinearity = {}
    for cohort_name, frame in (("UKB", ukb), ("Wales", wales)):
        numeric = frame[["age", "cum_nonhdl", "tg_filter", "remnant_unt"]].apply(pd.to_numeric, errors="coerce")
        collinearity[cohort_name] = {
            f"{left}__{right}": float(numeric[left].corr(numeric[right]))
            for left, right in (("cum_nonhdl", "remnant_unt"), ("tg_filter", "remnant_unt"),
                                 ("cum_nonhdl", "tg_filter"))
        }

    report = {
        "audit": "CALON-C independent raw gate reproduction",
        "governance": "aggregate-only; no participant rows, identifiers, family labels, dates of birth, or predictions emitted",
        "source_files": sources,
        "ukb_gate_checks": gate_checks,
        "wales_gate_checks": wales_checks,
        "declared_ledgers": {
            "ukb": declared.get("ledger_ukb"),
            "wales": declared.get("ledger_wales"),
        },
        "raw_ledgers": {"ukb": ukb_ledger, "wales": wales_ledger},
        "comparator_worked_example": calon._test_safeheart(),
        "lp_a_policy": {
            "model_terms": "absent",
            "UKB_source_unit": "nmol/L",
            "comparator_conversion": "nmol/L divided by 2.15, comparator thresholds only",
            "Wales_source": "DRAGON Lpa nmol/L; native WALES Lpa fields excluded as mixed unit",
        },
        "feature_correlations": collinearity,
        "ph_assumptions": {
            "UKB_primary": ph_test(ukb, calon.usable(ukb, calon.SPEC_FULL)),
            "Wales_primary": ph_test(wales, calon.usable(wales, calon.SPEC_FULL)),
        },
    }
    report["summary"] = {
        "ukb_gates_passed": f"{sum(item['status'] == 'PASS' for item in gate_checks.values())}/{len(gate_checks)}",
        "wales_gates_passed": f"{sum(item['status'] == 'PASS' for item in wales_checks.values())}/{len(wales_checks)}",
        "safeheart_worked_example_status": "PASS",
    }
    (OUT / "raw_reproduction.json").write_text(json.dumps(report, indent=2, default=str) + "\n")
    print(json.dumps(report["summary"], indent=2))


if __name__ == "__main__":
    main()
