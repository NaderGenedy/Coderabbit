"""Cycle 2 cell 04: full OOF head-to-head with paired cluster B=2,000."""
from __future__ import annotations

if "COMPARATORS" not in globals():
    raise RuntimeError("Run cell 03 before the head-to-head")
HEADTOHEAD, HEADTOHEAD_GATE = run_headtohead(
    FROZEN, PRIMARY_FIT, COMPARATORS, OUT
)
emit_aggregate(HEADTOHEAD, "FULL HEAD-TO-HEAD TABLE")
emit_aggregate(HEADTOHEAD_GATE, "TRIPOD+AI HEAD-TO-HEAD GATES")
if HEADTOHEAD_GATE["bootstrap_gate"] != "PASS":
    raise RuntimeError(
        "confirmatory paired cluster bootstrap did not complete exactly B=2000"
    )
