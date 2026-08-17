#!/usr/bin/env python3
"""Compare isolated CALON-C reproduction outputs with the locked aggregate outputs."""
from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOCKED = ROOT / "outputs"
REPRO = Path(__file__).resolve().parent / "performance_reproduction"
OUT = Path(__file__).resolve().parent / "results_reconciliation.csv"
TOL = 1e-12


def numeric(value):
    return None if value is None else float(value)


def main() -> None:
    original = json.loads((LOCKED / "calon_c.json").read_text())
    reproduced = json.loads((REPRO / "calon_c.json").read_text())
    rows = []

    for cohort in ("UK Biobank", "Wales"):
        for horizon in ("full", "10y", "5y"):
            def selected(payload):
                return [
                    row for row in payload["head_to_head"]
                    if row["cohort"] == cohort and row["horizon"] == horizon
                    and row["estimand"] == "refit_varset" and row["comparator"] == "age+sex"
                ][0]

            left, right = selected(original), selected(reproduced)
            for key in ("C_model", "C_comparator", "delta", "lo", "hi", "rho"):
                difference = abs(numeric(left[key]) - numeric(right[key]))
                rows.append({
                    "cohort": cohort,
                    "horizon": horizon,
                    "metric": f"age+sex_refit__{key}",
                    "locked": left[key],
                    "reproduced": right[key],
                    "absolute_difference": difference,
                    "status": "PASS" if difference <= TOL else "FAIL",
                })

    for key in ("ledger_ukb", "ledger_wales", "transport", "S1_unambiguous_date", "S2_correction_factor"):
        same = original[key] == reproduced[key]
        rows.append({
            "cohort": "all",
            "horizon": "all",
            "metric": key,
            "locked": "identical" if same else "different",
            "reproduced": "identical" if same else "different",
            "absolute_difference": 0 if same else None,
            "status": "PASS" if same else "FAIL",
        })

    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    failures = sum(row["status"] == "FAIL" for row in rows)
    print(f"{len(rows) - failures}/{len(rows)} reconciliation checks PASS")


if __name__ == "__main__":
    main()
