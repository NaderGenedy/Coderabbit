"""Cycle 2 cell 03: source-verified SAFEHEART, FH-RS and Montreal scores."""
from __future__ import annotations

if "PRIMARY_FIT" not in globals():
    raise RuntimeError("Run cell 02 before scoring comparators")

RUN_EXPLORATORY_LPA_CONVERSION = bool(
    globals().get("RUN_EXPLORATORY_LPA_CONVERSION", False)
)
COMPARATORS = score_comparators_oof(
    FROZEN,
    PRIMARY_FIT.splits,
    exploratory_lpa_conversion=RUN_EXPLORATORY_LPA_CONVERSION,
)
SCORES = COMPARATORS.scores
COMPARATOR_RISKS = COMPARATORS.risks
write_aggregate_csv(
    COMPARATORS.audit, OUT / "comparator_evaluability.csv"
)
emit_aggregate(COMPARATORS.audit, "COMPARATOR EVALUABILITY")
emit_aggregate(
    [
        {"comparator": name, **details}
        for name, details in COMPARATOR_PROVENANCE.items()
    ],
    "COMPARATOR SOURCE STATUS",
)
if COMPARATORS.exploratory_lpa_conversion:
    emit_aggregate(
        {
            "status": "EXPLORATORY ONLY",
            "conversion": "Lp(a) nmol/L divided by 2.15",
            "confirmatory": False,
        },
        "LP(A) UNIT WARNING",
    )
