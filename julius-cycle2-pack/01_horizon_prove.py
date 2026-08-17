"""Cycle 2 cell 01: prove the locked cohort SHA and corrected horizons."""
from __future__ import annotations

# Requires cell 00 plus already-loaded FROZEN, COHORT_LEDGER and COHORT_HASH.
if "FROZEN" not in globals():
    raise RuntimeError("Load the frozen Julius DataFrame as FROZEN before cell 01")
if "COHORT_LEDGER" not in globals():
    raise RuntimeError(
        "Define COHORT_LEDGER with carriers/prevalent/undated/frozen counts"
    )

COHORT_LOCK = validate_frozen_lock(
    FROZEN,
    COHORT_LEDGER,
    globals().get("COHORT_HASH"),
)
_time = pd.to_numeric(FROZEN["time_years"], errors="raise").to_numpy(float)
_event = _binary_event_array(
    pd.to_numeric(FROZEN["event"], errors="raise").to_numpy(), "FROZEN.event"
)
_t5, _e5 = horizon_risk_set(_time, _event, 5.0)
_t10, _e10 = horizon_risk_set(_time, _event, 10.0)
HORIZON_PROOF = pd.DataFrame(
    [
        {
            "horizon": "full",
            "n": len(_time),
            "events": int(_event.sum()),
            "expected_events": EXPECTED["events_full"],
            "status": "PASS",
        },
        {
            "horizon": "5y",
            "n": len(_t5),
            "events": int(_e5.sum()),
            "expected_events": EXPECTED["events_5y"],
            "status": "PASS",
        },
        {
            "horizon": "10y",
            "n": len(_t10),
            "events": int(_e10.sum()),
            "expected_events": EXPECTED["events_10y"],
            "status": "PASS",
        },
    ]
)
if HORIZON_PROOF["events"].tolist() != [289, 97, 194]:
    raise AssertionError("corrected horizon event gate failed")
OUT = Path(globals().get("CYCLE2_OUT", "calon_cycle2_out"))
require_fresh_output_dir(OUT)
write_aggregate_json(COHORT_LOCK, OUT / "findings_lock.json")
write_aggregate_csv(HORIZON_PROOF, OUT / "horizon_proof.csv")
emit_aggregate(COHORT_LOCK, "CYCLE-2 FINDINGS LOCK")
emit_aggregate(HORIZON_PROOF, "CORRECTED HORIZON PROOF")
