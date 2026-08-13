#!/usr/bin/env python3
"""Reconstruct the aggregate CALON-N 12-comparison tally from audited JSON."""
from __future__ import annotations

import os

import json
from pathlib import Path


ROOT = Path(os.environ["CALON_PROJECT_ROOT"])
AUDIT = ROOT / "outputs" / "audit_2026_08_10"
OUT = AUDIT / "delta3_comparison_tally_verification.json"


def verdict(ci):
    lo, hi = ci
    if lo > 0:
        return "WIN"
    if hi < 0:
        return "LOSS"
    return "TIE"


def main():
    a3 = json.loads((AUDIT / "a3_locked_reproduction.json").read_text())
    a2 = json.loads((AUDIT / "a2_union_definition.json").read_text())

    transports = {
        "DRAGON_to_UKB_strict": a3["independent_computed"]["DRAGON_to_UKB_strict"],
        "UKB_strict_to_DRAGON": a3["independent_computed"]["UKB_strict_to_DRAGON"],
        "DRAGON_to_UKB_union_sensitivity": a2["union_reciprocal_transport"]["DRAGON_to_UKB_union"],
    }
    rows = []
    tally = {"WIN": 0, "TIE": 0, "LOSS": 0}
    for transport, block in transports.items():
        for comparator, result in block["comparators"].items():
            ci = result["delta_ci"]
            status = verdict(ci)
            tally[status] += 1
            rows.append({
                "transport": transport,
                "comparator": comparator,
                "delta_calon_minus_comparator": result["delta_calon_minus_comparator"],
                "delta_ci_95": ci,
                "verdict": status,
            })

    clinic_age_sex = next(
        r for r in rows
        if r["transport"] == "UKB_strict_to_DRAGON" and r["comparator"] == "age_sex")
    losses = [r for r in rows if r["verdict"] == "LOSS"]
    out = {
        "task": "DELTA 3 CALON-N head-to-head tally",
        "participant_level_outputs": False,
        "classification_rule": {
            "WIN": "paired delta 95% CI entirely above zero",
            "TIE": "paired delta 95% CI includes zero",
            "LOSS": "paired delta 95% CI entirely below zero",
        },
        "scope": "8 strict-primary comparisons plus 4 DRAGON-to-UKB-union sensitivity comparisons",
        "tally": tally,
        "comparisons": rows,
        "losses": losses,
        "clinic_age_sex_comparison": clinic_age_sex,
        "interpretation": (
            "The overall tally is descriptive and mixes primary and sensitivity targets. "
            "The strict eight-cell matrix remains the primary comparator result."
        ),
    }
    OUT.write_text(json.dumps(out, indent=2) + "\n")
    print("tally:", tally)
    print("losses:", len(losses))
    print("clinic age+sex verdict:", clinic_age_sex["verdict"])
    print("written:", OUT)


if __name__ == "__main__":
    main()
