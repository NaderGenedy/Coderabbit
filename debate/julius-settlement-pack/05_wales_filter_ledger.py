# Julius Cell 5 — Wales filter ledger (local 1159/92 vs Julius 1059)
# Start from WALES_FH_CLEANED; print n and events after each exclusion. Aggregates only.

from __future__ import annotations

w = wales.copy()  # Julius: assign WALES_FH_CLEANED to `wales`
steps = []

def snap(label, frame, event_col="ascvd_combine"):
    n = int(len(frame))
    ev = int(frame[event_col].fillna(0).astype(float).sum()) if event_col in frame.columns else None
    steps.append({"step": label, "n": n, "events": ev})
    return frame

cur = snap("0_raw", w)
# Genotype flag is Positive1 — NOT Mutation1 (inventory)
cur = snap("1_Positive1_eq_1", cur[cur["Positive1"] == 1])

# Prevalent / undated / complete follow-up — encode your Julius protocol explicitly:
# TODO: align with the filter used in 15_CALON_FINAL.py build_wales() once confirmed
# Example placeholders (edit to match the true pipeline before trusting):
if "ascvd_combine" in cur.columns:
    # keep all Positive1 for ledger visibility; refine on Julius
    pass

# Date parser sensitivity (inventory trap 6)
if "MeasurementDate.2" in cur.columns:
    a = cur.copy()
    a["_d"] = pd.to_datetime(a["MeasurementDate.2"], errors="coerce", dayfirst=False)
    b = cur.copy()
    b["_d"] = pd.to_datetime(b["MeasurementDate.2"], errors="coerce", dayfirst=True)
    steps.append({
        "step": "dateparse_dayfirst_False_nonnull",
        "n": int(a["_d"].notna().sum()),
        "events": None,
    })
    steps.append({
        "step": "dateparse_dayfirst_True_nonnull",
        "n": int(b["_d"].notna().sum()),
        "events": None,
    })

AggregateReport(
    script="05_wales_filter_ledger",
    notes=[
        "Targets: local analysis n=1159 events=92; Julius n=1059; trap6 path 948/82",
        "Fill TODO filters until one ledger reproduces one of those three exactly",
        "First diverging line is the non-comparability point for Wales C-indices",
    ],
    metrics={"ledger": steps},
).show()
