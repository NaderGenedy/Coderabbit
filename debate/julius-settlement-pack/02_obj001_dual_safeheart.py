# Julius Cell 2 — OBJ-001 dual SAFEHEART (Spec Kit categorical vs local continuous)
# Settles: which implementation is on-disk; C-index gap on ONE frozen carrier risk set.
# Paste Spec Kit functions below (do not invent coefficients).

from __future__ import annotations
import math
from lifelines.utils import concordance_index

# --- Spec Kit categorical SAFEHEART (Pérez de Isla 2017 Table 3) ---
def safeheart_lp_speckit(*, age_years, male, prior_ascvd, hypertension, bmi_kg_m2, active_smoking, ldl_mg_dl, lpa_mg_dl):
    age = float(age_years); bmi = float(bmi_kg_m2); ldl = float(ldl_mg_dl); lpa = float(lpa_mg_dl)
    lp = 0.70 * bool(male)
    lp += 1.07 * (30 <= age < 60)
    lp += 1.45 * (age >= 60)
    lp += 0.69 * bool(hypertension)
    lp += 1.42 * bool(prior_ascvd)
    lp += 0.48 * bool(active_smoking)
    lp += 0.88 * (25 <= bmi < 30)
    lp += 0.98 * (bmi >= 30)
    lp += 0.92 * (100 <= ldl < 160)
    lp += 1.57 * (ldl >= 160)
    lp += 0.42 * (lpa > 50)
    return float(lp)

# --- Local continuous form from code/15_CALON_FINAL.py (NOT claimed published here) ---
def safeheart_lp_local_continuous(*, age, male, htn, smoke, bmi, ldl_mmol, lpa_nmol_or_mg, lpa_threshold=105.0):
    lpa_hi = float(lpa_nmol_or_mg) >= lpa_threshold
    return (
        0.045 * float(age)
        + 0.6 * bool(male)
        + 0.4 * bool(htn)
        + 0.3 * bool(smoke)
        + 0.02 * float(bmi)
        + 0.15 * float(ldl_mmol)
        + 0.25 * lpa_hi
    )

# `risk` must be the frozen analysis frame from Cell 1 (incident carriers only).
# Map columns — adjust names if your Julius frame differs.
df = risk.copy()
df["male"] = (df["sex_F"] == 0) if "sex_F" in df.columns else (df.get("sex") == 1)
df["age"] = df["age_exact_baseline"]
df["bmi"] = df["bmi_direct"]
df["ldl_mmol"] = df["ldl_chem"]
df["ldl_mg"] = df["ldl_mmol"] * MMOL_TO_MGDL_LDL
df["lpa"] = df["lpa_chem"] if "lpa_chem" in df.columns else df["pre_lpa"]
df["htn"] = df.get("bp_med", df.get("hypertension", 0))  # TODO: build from p6153/p6177 if needed
df["smoke"] = df["smoking_current"].fillna(0) if "smoking_current" in df.columns else df["smoking_ever"].fillna(0)
df["prior_ascvd"] = False  # incident cohort by construction; set True only if protocol includes it

# Complete-case for fair dual score (no silent imputation)
need = ["age", "male", "bmi", "ldl_mmol", "lpa", "htn", "smoke"]
cc = df.dropna(subset=need).copy()

cc["lp_spec"] = [
    safeheart_lp_speckit(
        age_years=r.age, male=bool(r.male), prior_ascvd=bool(r.prior_ascvd),
        hypertension=bool(r.htn), bmi_kg_m2=r.bmi, active_smoking=bool(r.smoke),
        ldl_mg_dl=r.ldl_mg, lpa_mg_dl=r.lpa,
    )
    for r in cc.itertuples()
]
cc["lp_local"] = [
    safeheart_lp_local_continuous(
        age=r.age, male=bool(r.male), htn=bool(r.htn), smoke=bool(r.smoke),
        bmi=r.bmi, ldl_mmol=r.ldl_mmol, lpa_nmol_or_mg=r.lpa,
    )
    for r in cc.itertuples()
]

# Time / event for concordance — build from inventory rules
cc["t0"] = pd.to_datetime(cc["date_baseline"])
cc["tev"] = pd.to_datetime(cc["ascvd_first_date_best"])
cc["event"] = (cc["tev"].notna() & (cc["tev"] > cc["t0"])).astype(int)
# censor at death or last follow-up if present; else tev or a study end you define on Julius
if "death_date" in cc.columns:
    cc["tcen"] = pd.to_datetime(cc["death_date"])
else:
    cc["tcen"] = pd.NaT
cc["t_end"] = cc["tev"].where(cc["event"] == 1, cc["tcen"])
# TODO on Julius: set a hard admin censor date if t_end still null
cc = cc.dropna(subset=["t_end"])
cc["time_years"] = (cc["t_end"] - cc["t0"]).dt.days / 365.25
cc = cc[cc["time_years"] > 0]

c_spec = float(concordance_index(cc["time_years"], -cc["lp_spec"], cc["event"]))
c_local = float(concordance_index(cc["time_years"], -cc["lp_local"], cc["event"]))
corr = float(np.corrcoef(cc["lp_spec"], cc["lp_local"])[0, 1])

AggregateReport(
    script="02_obj001_dual_safeheart",
    notes=[
        "If |C_spec - C_local| is large, OBJ-001 stands: two different functions",
        "PDF arbitration still required before calling either 'published'",
        "Lp(a) unit (mg/dL vs nmol/L) must match Spec Kit threshold >50 mg/dL — verify on Julius",
    ],
    metrics={
        "n_complete_case": int(len(cc)),
        "n_events": int(cc["event"].sum()),
        "C_safeheart_speckit_categorical": c_spec,
        "C_safeheart_local_continuous": c_local,
        "delta_C_local_minus_spec": c_local - c_spec,
        "pearson_lp_spec_vs_local": corr,
        "target_local_SAFEHEART_C_from_STATUS": 0.6944,
        "target_Julius_SAFEHEART_C_from_brief": 0.628,
    },
).show()
