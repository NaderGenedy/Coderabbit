"""Cycle 2 cell 02: nested-CV ridge Cox fit for the frozen CALON-G SPEC."""
from __future__ import annotations

# Requires cells 00-01. No prediction vector is printed or written.
if "COHORT_LOCK" not in globals() or COHORT_LOCK.get("status") != "PASS":
    raise RuntimeError("Run the SHA/count/horizon gates before fitting CALON-G")

PREDICTOR_DIAGNOSTICS = predictor_diagnostics(FROZEN)
write_aggregate_csv(
    PREDICTOR_DIAGNOSTICS, OUT / "predictor_diagnostics.csv"
)
emit_aggregate(PREDICTOR_DIAGNOSTICS, "PRESPECIFIED PREDICTOR DIAGNOSTICS")

PRIMARY_FIT = fit_calong_oof(FROZEN, SPEC_PRIMARY, "CALON-G-primary")
MODEL_LP = PRIMARY_FIT.lp
MODEL_RISK_5Y = PRIMARY_FIT.risk5
MODEL_RISK_10Y = PRIMARY_FIT.risk10
OOF_SPLITS = PRIMARY_FIT.splits
FINAL_UKB_BUNDLE = PRIMARY_FIT.final_bundle

write_aggregate_json(
    PRIMARY_FIT.aggregate_dict(), OUT / "calong_model_summary.json"
)
write_aggregate_csv(
    PRIMARY_FIT.fold_summary, OUT / "calong_outer_fold_summary.csv"
)
emit_aggregate(PRIMARY_FIT.aggregate_dict(), "CALON-G PRIMARY OOF")

GREY_FIT = None
if "log_apob_hdl" in FROZEN and FROZEN["log_apob_hdl"].notna().any():
    GREY_FIT = fit_calong_oof(
        FROZEN, SPEC_GREY, "CALON-G-grey sensitivity"
    )
    write_aggregate_json(
        GREY_FIT.aggregate_dict(), OUT / "calong_grey_summary.json"
    )
    emit_aggregate(GREY_FIT.aggregate_dict(), "CALON-G-GREY SENSITIVITY")
else:
    write_aggregate_json(
        {
            "label": "CALON-G-grey sensitivity",
            "status": "NOT_EVALUABLE",
            "reason": "log_apob_hdl unavailable",
            "spec": list(SPEC_GREY),
        },
        OUT / "calong_grey_summary.json",
    )
