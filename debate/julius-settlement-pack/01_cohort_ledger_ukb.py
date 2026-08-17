# Julius Cell 1 — UKB risk-set ledger (OBJ from step-000: n=3333 vs 3209)
# Requires: ukb_master + corrected_ascvd_outcomes joined on eid (do not print eid).

from __future__ import annotations

# Assumes Cell 0 already run; ukb / outcomes DataFrames in scope as `ukb`, `outc`
# If not, load them in Julius then:
#   ukb = <your ukb_master frame>
#   outc = <your corrected_ascvd_outcomes frame>

need = ["eid", "ldlr_carrier", "date_baseline"]
miss = [c for c in need if c not in ukb.columns]
if miss:
    raise KeyError(f"ukb missing columns: {miss}")

m = ukb.merge(outc, on="eid", how="inner", suffixes=("", "_out"))
carriers = m[m["ldlr_carrier"] == 1].copy()
n0 = int(len(carriers))

# Prevalent ASCVD at baseline (dated event on/before baseline)
carriers["date_baseline"] = pd.to_datetime(carriers["date_baseline"], errors="coerce")
carriers["ascvd_first_date_best"] = pd.to_datetime(carriers["ascvd_first_date_best"], errors="coerce")
carriers["ascvd_first_date_dated"] = pd.to_datetime(carriers.get("ascvd_first_date_dated"), errors="coerce")

prevalent = carriers["ascvd_first_date_best"].notna() & (
    carriers["ascvd_first_date_best"] <= carriers["date_baseline"]
)
n_prev = int(prevalent.sum())
risk = carriers.loc[~prevalent].copy()
n_after_prev = int(len(risk))

# Undated atherosclerotic signal: event flags without usable date (inventory trap)
flag_cols = [c for c in ["i21_event", "i25_event", "i50_event", "i63_event", "i70_event", "i73_event", "g45_event"] if c in risk.columns]
if flag_cols:
    any_flag = risk[flag_cols].fillna(0).astype(float).sum(axis=1) > 0
    undated = any_flag & risk["ascvd_first_date_best"].isna()
    n_undated = int(undated.sum())
else:
    n_undated = None

# Two candidate dispositions
n_keep_undated = n_after_prev  # STATUS-style 3540-207 = 3333 if n0==3540
n_drop_undated = n_after_prev - (n_undated or 0)

report = AggregateReport(
    script="01_cohort_ledger_ukb",
    notes=[
        "Compare metrics['n_carriers'] to 3540",
        "Compare metrics['n_after_prevalent_exclusion'] to 3333 (STATUS) vs 3209 (Julius brief)",
        "If n_drop_undated≈3209, STATUS kept undated cases in the risk set",
    ],
    metrics={
        "n_carriers": n0,
        "n_prevalent_excluded": n_prev,
        "n_after_prevalent_exclusion": n_after_prev,
        "n_undated_flagged": n_undated,
        "n_if_undated_dropped": n_drop_undated,
        "matches_3333": n_after_prev == 3333,
        "matches_3209": n_drop_undated == 3209 or n_after_prev == 3209,
    },
)
report.show()
