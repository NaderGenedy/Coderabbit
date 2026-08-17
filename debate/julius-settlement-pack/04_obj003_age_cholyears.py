# Julius Cell 4 — OBJ-003 age × cholesterol-years collinearity
# Pearson r(age, age*untreated_TC) + design for refit (prints aggregates only).

from __future__ import annotations

d = cc.copy() if "cc" in dir() else risk.copy()
d["age"] = d["age_exact_baseline"] if "age_exact_baseline" in d.columns else d["age"]
d["tc"] = d["tc_chem"]  # untreated TC if available; document if on-treatment

# If you have a verified untreated-TC column on Julius, rename here:
# d["tc"] = d["untreated_tc"]

d["chol_years"] = d["age"] * d["tc"]
sub = d.dropna(subset=["age", "tc", "chol_years"])
r = float(np.corrcoef(sub["age"], sub["chol_years"])[0, 1])

AggregateReport(
    script="04_obj003_age_cholyears",
    notes=[
        "If |r| is extremely high (e.g. >0.95), collinearity is confirmed structurally",
        "Next Julius cell: Cox/logit with age+chol_years vs age+tc; report age HR both ways",
        "Do not claim the preferred model until the refit HR moves (or fails to)",
    ],
    metrics={
        "n": int(len(sub)),
        "pearson_age_vs_chol_years": r,
        "drop_rule_threshold_in_spec": 0.999,
        "would_trip_0_999_drop": abs(r) >= 0.999,
    },
).show()

print(
    """
# REFIT TEMPLATE (run after reviewing r):
# from lifelines import CoxPHFitter
# m1 = CoxPHFitter().fit(sub[['age','chol_years','time_years','event']], duration_col='time_years', event_col='event')
# m2 = CoxPHFitter().fit(sub[['age','tc','time_years','event']], duration_col='time_years', event_col='event')
# print(m1.summary[['exp(coef)','exp(coef) lower 95%','exp(coef) upper 95%']])
# print(m2.summary[['exp(coef)','exp(coef) lower 95%','exp(coef) upper 95%']])
"""
)
