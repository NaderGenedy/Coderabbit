"""Cycle 2 cell 06: censoring-aware OOF calibration and 10-year DCA."""
from __future__ import annotations

for _required in (
    "COHORT_LOCK",
    "PRIMARY_FIT",
    "COMPARATORS",
    "HEADTOHEAD_GATE",
    "RUN_EXPLORATORY_LPA_CONVERSION",
):
    if _required not in globals():
        raise RuntimeError("Run cells 00-04 before calibration/DCA")
CALIBRATION, CALIBRATION_BINS, DCA_10Y = run_calibration_dca(
    FROZEN, PRIMARY_FIT, COMPARATORS, OUT
)
emit_aggregate(CALIBRATION, "OOF CALIBRATION SLOPE/INTERCEPT")
emit_aggregate(DCA_10Y, "10-YEAR DCA AT 5%, 7.5%, 10%")

_wales_reporting = (
    WALES_TRANSPORT
    if "WALES_TRANSPORT" in globals()
    else {
        "status": "NOT_RUN",
        "reason": "Wales cell not completed; external reporting item remains pending",
    }
)
TRIPOD_AI_CHECKLIST, STROBE_FLOW = reporting_standard_tables(
    COHORT_LOCK, HEADTOHEAD_GATE, CALIBRATION, _wales_reporting
)
write_aggregate_csv(TRIPOD_AI_CHECKLIST, OUT / "tripod_ai_checklist.csv")
write_aggregate_csv(STROBE_FLOW, OUT / "strobe_flow.csv")
emit_aggregate(TRIPOD_AI_CHECKLIST, "TRIPOD+AI CHECKLIST")
emit_aggregate(STROBE_FLOW, "STROBE FLOW")

PASTE_RUN_META = {
    "cohort_sha256": COHORT_LOCK["cohort_sha256"],
    "spec_sha256": SPEC_SHA256,
    "spec": SPEC_LOCK,
    "endpoint": PRIMARY_ENDPOINT,
    "participant_level_outputs": False,
    "run_complete": True,
    "exploratory_lpa_conversion_requested": RUN_EXPLORATORY_LPA_CONVERSION,
    "exploratory_lpa_conversion_used": COMPARATORS.exploratory_lpa_conversion,
    "headtohead_status": HEADTOHEAD_GATE["analysis_status"],
    "wales_status": (
        WALES_TRANSPORT.get(
            "status", WALES_TRANSPORT.get("primary", {}).get("status", "PASS")
        )
        if "WALES_TRANSPORT" in globals()
        else "NOT_RUN"
    ),
    "wales_lpa_comparable": globals().get("WALES_LPA_COMPARABLE"),
    "mice_mar_sensitivity": (
        "PRESPECIFIED, not auto-run: m>=20; outcome not imputed; pooling method "
        "must be declared in Julius before execution"
    ),
    "versions": {
        "python": os.sys.version.split()[0],
        "numpy": np.__version__,
        "pandas": pd.__version__,
        "lifelines": _installed_version("lifelines"),
        "matplotlib": _installed_version("matplotlib"),
    },
}
write_aggregate_json(PASTE_RUN_META, OUT / "run_meta.json")
emit_aggregate(PASTE_RUN_META, "CYCLE-2 RUN METADATA")
