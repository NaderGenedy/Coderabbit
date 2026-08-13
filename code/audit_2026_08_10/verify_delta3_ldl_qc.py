#!/usr/bin/env python3
"""Aggregate-only verification of the DRAGON pretreatment-LDL correction rule."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path("${CALON_PROJECT_ROOT}")
SOURCE = Path("${CALON_WALES_DATA}/FH_Dragon3 (1).csv")
OUT = ROOT / "outputs" / "audit_2026_08_10" / "delta3_ldl_qc_verification.json"


def main():
    raw = pd.read_csv(SOURCE, usecols=["MtachedLDLC", "LastLDL", "OnTreatment"],
                      low_memory=False)
    pre = pd.to_numeric(raw["MtachedLDLC"], errors="coerce")
    last = pd.to_numeric(raw["LastLDL"], errors="coerce")
    treatment = pd.to_numeric(raw["OnTreatment"], errors="coerce").fillna(0).gt(0)
    diff = pre - last

    out = {
        "task": "DELTA 3 DRAGON pretreatment-LDL aggregate QC",
        "participant_level_outputs": False,
        "rows": int(len(raw)),
        "treated_percent": float(100 * treatment.mean()),
        "median_mtachedldlc_mmol_l": {
            "not_on_treatment": float(pre.loc[~treatment].median()),
            "on_treatment": float(pre.loc[treatment].median()),
        },
        "median_mtachedldlc_minus_lastldl_mmol_l": float(diff.median()),
        "interpretation": (
            "MtachedLDLC behaves as a pretreatment/highest-recorded LDL-C field in "
            "DRAGON. Applying a statin back-correction to it would double-correct the "
            "treated majority."
        ),
    }
    OUT.write_text(json.dumps(out, indent=2) + "\n")
    print("rows:", out["rows"])
    print("treated_percent:", round(out["treated_percent"], 1))
    print("median_mtachedldlc_not_treated:", out["median_mtachedldlc_mmol_l"]["not_on_treatment"])
    print("median_mtachedldlc_treated:", out["median_mtachedldlc_mmol_l"]["on_treatment"])
    print("median_difference_from_lastldl:", out["median_mtachedldlc_minus_lastldl_mmol_l"])
    print("written:", OUT)


if __name__ == "__main__":
    main()
