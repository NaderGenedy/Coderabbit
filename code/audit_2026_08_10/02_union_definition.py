#!/usr/bin/env python3
"""A2: audit whether the UKB P/LP-or-predicted-LoF union merits primacy.

The genetic construction and both reciprocal transports are re-derived from raw
sources. Only aggregate results are printed or written.
"""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from audit_common import (
    CALON_N,
    OUT,
    build_dragon,
    build_ukb,
    event_count,
    metric_block,
    nested_subset_auc_delta,
    paired_auc_delta,
    source_comparators,
    transport,
    write_json,
)


BOOTSTRAP = 4000
SEEDS = {
    "calon_forward": 20260826,
    "calon_reverse": 20260926,
    "age_sex_forward": 20260819,
    "age_sex_reverse": 20260919,
    "metric_forward_union": 20261519,
    "metric_reverse_union": 20261520,
    "paired_forward": 20261619,
    "paired_reverse": 20261620,
}


def phenotype(frame: pd.DataFrame) -> dict:
    events = int(frame["y"].sum())
    ldl = pd.to_numeric(frame["ldl"], errors="coerce")
    result = {
        "n": int(len(frame)),
        "events": event_count(events),
        "ldl_nonmissing_n": int(ldl.notna().sum()),
        "ldl_mean_mmol_l": float(ldl.mean()),
        "ldl_median_mmol_l": float(ldl.median()),
        "treatment_pct": float(100 * frame["treatment"].mean()),
        "ascvd_pct": float(100 * frame["y"].mean()) if events >= 10 else "<10, non-estimable",
    }
    return result


def evaluate_direction(
    source: pd.DataFrame,
    target: pd.DataFrame,
    calon_seed: int,
    age_sex_seed: int,
    metric_seed: int,
) -> tuple[dict, dict]:
    calon = transport(source, target, CALON_N, calon_seed)
    age_sex = transport(source, target, ["age", "male"], age_sex_seed)
    comparators = source_comparators(source, target)
    comparators["age_sex"] = age_sex["prediction"]
    # Stable report order.
    comparators = {
        "age_sex": comparators["age_sex"],
        "Montreal_adapted": comparators["Montreal_adapted"],
        "FH_Risk_Score_adapted": comparators["FH_Risk_Score_adapted"],
        "SAFEHEART_adapted": comparators["SAFEHEART_adapted"],
    }
    y = target["y"].to_numpy(int)
    block = metric_block(
        y,
        calon["prediction"],
        target["cluster"].to_numpy(),
        comparators,
        metric_seed,
        BOOTSTRAP,
    )
    block.update({
        "n": int(len(target)),
        "events": event_count(int(y.sum())),
        "selected_C_calon_n": calon["penalty"],
        "selected_C_age_sex": age_sex["penalty"],
        "safeheart_e_o_warning": "Not calibration-compatible: a 5-year risk is compared with prevalent ASCVD.",
    })
    return block, calon


def main() -> None:
    dragon = build_dragon()
    ukb, genetic_counts = build_ukb()
    strict = ukb.loc[ukb["strict"].eq(1)].copy().reset_index(drop=True)
    strict["cluster"] = strict["cluster_strict"]
    union = ukb.copy().reset_index(drop=True)
    union["cluster"] = union["cluster_union"]
    added = union.loc[union["strict"].eq(0)].copy().reset_index(drop=True)

    phenotype_strict = phenotype(strict)
    phenotype_added = phenotype(added)

    forward_union_metrics, forward_union_fit = evaluate_direction(
        dragon,
        union,
        SEEDS["calon_forward"],
        SEEDS["age_sex_forward"],
        SEEDS["metric_forward_union"],
    )
    reverse_union_metrics, reverse_union_fit = evaluate_direction(
        union,
        dragon,
        SEEDS["calon_reverse"],
        SEEDS["age_sex_reverse"],
        SEEDS["metric_reverse_union"],
    )

    # Refit the strict comparators under the same locked seeds for a paired
    # definition-change analysis; these are not read from stored JSON.
    forward_strict_fit = transport(dragon, strict, CALON_N, SEEDS["calon_forward"])
    reverse_strict_fit = transport(strict, dragon, CALON_N, SEEDS["calon_reverse"])
    strict_mask = union["strict"].eq(1).to_numpy()
    forward_definition_delta = nested_subset_auc_delta(
        union["y"].to_numpy(int),
        forward_union_fit["prediction"],
        strict_mask,
        union["cluster"].to_numpy(),
        SEEDS["paired_forward"],
        BOOTSTRAP,
    )
    reverse_definition_delta = paired_auc_delta(
        dragon["y"].to_numpy(int),
        reverse_union_fit["prediction"],
        reverse_strict_fit["prediction"],
        dragon["cluster"].to_numpy(),
        SEEDS["paired_reverse"],
        BOOTSTRAP,
    )
    reverse_definition_delta["contrast"] = "union_trained_minus_strict_trained_on_same_DRAGON_target"
    strict_reference = {
        "DRAGON_to_UKB_strict": {
            "auc": forward_strict_fit["auc"],
            "e_o": float(forward_strict_fit["prediction"].sum() / strict["y"].sum()),
            "selected_C": forward_strict_fit["penalty"],
        },
        "UKB_strict_to_DRAGON": {
            "auc": reverse_strict_fit["auc"],
            "e_o": float(reverse_strict_fit["prediction"].sum() / dragon["y"].sum()),
            "selected_C": reverse_strict_fit["penalty"],
        },
    }

    median_ldl_difference = float(
        abs(phenotype_added["ldl_median_mmol_l"] - phenotype_strict["ldl_median_mmol_l"])
    )
    treatment_difference = float(
        abs(phenotype_added["treatment_pct"] - phenotype_strict["treatment_pct"])
    )
    ascvd_difference = float(
        abs(float(phenotype_added["ascvd_pct"]) - float(phenotype_strict["ascvd_pct"]))
    )
    phenotype_pass = (
        median_ldl_difference <= 0.5
        and treatment_difference <= 15.0
        and ascvd_difference <= 3.0
    )
    discrimination_pass = (
        forward_definition_delta["ci"][0] > -0.02
        and reverse_definition_delta["ci"][0] > -0.02
    )
    # The implemented union rule accepts consequence tokens alone; it does not
    # perform transcript/NMD/last-exon/splice-rescue adjudication.
    independent_high_confidence_lof_adjudication_available = False
    genetic_pass = independent_high_confidence_lof_adjudication_available
    promote = bool(phenotype_pass and discrimination_pass and genetic_pass)

    result = {
        "task": "A2_union_definition",
        "genetic_definition": {
            **genetic_counts,
            "added_are_lof_consequence_qualified_by_construction": True,
            "independent_high_confidence_lof_adjudication_available": independent_high_confidence_lof_adjudication_available,
            "missing_adjudication_elements": [
                "canonical_transcript restriction",
                "NMD/last-exon escape review",
                "splice rescue review",
                "independent clinical classification for LoF-only additions",
            ],
        },
        "phenotype_comparison": {
            "strict_clinvar_plp": phenotype_strict,
            "lof_added": phenotype_added,
            "absolute_differences": {
                "median_ldl_mmol_l": median_ldl_difference,
                "treatment_percentage_points": treatment_difference,
                "ascvd_percentage_points": ascvd_difference,
            },
        },
        "union_reciprocal_transport": {
            "DRAGON_to_UKB_union": forward_union_metrics,
            "UKB_union_to_DRAGON": reverse_union_metrics,
        },
        "strict_raw_recomputed_reference": strict_reference,
        "union_vs_strict_definition_change": {
            "DRAGON_model_union_target_minus_strict_subset": forward_definition_delta,
            "union_trained_minus_strict_trained_on_DRAGON": reverse_definition_delta,
        },
        "primary_definition_gate": {
            "rule": (
                "Promote only if >=95% of LoF-only additions have independent high-confidence LoF adjudication; "
                "added median LDL differs by <=0.5 mmol/L, treatment by <=15 percentage points, and ASCVD by "
                "<=3 percentage points; and both reciprocal union-minus-strict AUC lower 95% bounds exceed -0.02."
            ),
            "genetic_validity_pass": genetic_pass,
            "phenotype_consistency_pass": phenotype_pass,
            "discrimination_noninferiority_pass": discrimination_pass,
            "promote_union_to_primary": promote,
            "verdict": "no_keep_strict_primary" if not promote else "yes_promote_union_primary",
        },
        "participant_level_outputs": False,
    }
    write_json(OUT / "a2_union_definition.json", result)
    print(json.dumps({
        "A2": {
            "strict_n": phenotype_strict["n"],
            "added_n": phenotype_added["n"],
            "added_without_any_plp_assertion_n": genetic_counts["added_without_any_plp_assertion_n"],
            "forward_union_auc": forward_union_metrics["auc"],
            "reverse_union_auc": reverse_union_metrics["auc"],
            "verdict": result["primary_definition_gate"]["verdict"],
        },
        "written": "outputs/audit_2026_08_10/a2_union_definition.json",
    }, indent=2))


if __name__ == "__main__":
    main()
