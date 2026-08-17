"""Cycle 2 cell 05: frozen-UKB transport; incomplete Wales ledger stops."""
from __future__ import annotations

for _name in ("WALES_START", "WALES_FINAL", "WALES_LEDGER"):
    if _name not in globals():
        raise RuntimeError(
            "Cell 05 requires WALES_START, WALES_FINAL and a completed "
            "WALES_LEDGER; filters are not guessed"
        )
if "WALES_LPA_COMPARABLE" not in globals():
    raise RuntimeError(
        "Cell 05 requires the explicit boolean WALES_LPA_COMPARABLE; "
        "column presence is not an assay-comparability decision"
    )

WALES_REDUCED_FIT = None
_reduced_bundle = None
if bool(globals().get("ALLOW_WALES_REDUCED_LPA_SENSITIVITY", False)):
    _reduced_spec = tuple(x for x in SPEC_PRIMARY if x != "log_lpa")
    WALES_REDUCED_FIT = fit_calong_oof(
        FROZEN,
        _reduced_spec,
        "CALON-G Wales reduced no-Lp(a) sensitivity",
    )
    _reduced_bundle = WALES_REDUCED_FIT.final_bundle
    write_aggregate_json(
        WALES_REDUCED_FIT.aggregate_dict(),
        OUT / "calong_wales_reduced_summary.json",
    )

WALES_TRANSPORT = run_wales_transport(
    WALES_START,
    WALES_FINAL,
    WALES_LEDGER,
    FINAL_UKB_BUNDLE,
    OUT,
    reduced_bundle=_reduced_bundle,
    lpa_comparable=globals().get("WALES_LPA_COMPARABLE"),
)
emit_aggregate(WALES_TRANSPORT, "WALES EXTERNAL GEOGRAPHICAL VALIDATION")
