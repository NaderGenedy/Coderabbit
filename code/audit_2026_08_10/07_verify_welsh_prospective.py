#!/usr/bin/env python3
"""Aggregate-only verification of the Welsh prospective FH cohort.

This script deliberately does not read wales_clean_treatment_response.csv. It writes
only aggregate counts and performance statistics: no participant rows, identifiers,
family identifiers, or variant data are exported.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

import numpy as np
import pandas as pd
from lifelines import CoxPHFitter
from lifelines.utils import concordance_index
from sklearn.model_selection import GroupKFold


SEED = 20260810
ROOT = Path("${CALON_PROJECT_ROOT}")
OUT = ROOT / "outputs" / "audit_2026_08_10" / "welsh_prospective_verification.json"
WALES = Path("${CALON_WALES_DATA}/WALES_FH_CLEANED.csv")
MASTER = Path(os.environ["CALON_SHARED_MASTER"])
PASS = MASTER / "PASS" / "pass_master.csv"
FORBIDDEN_BASENAME = "wales_clean_treatment_response.csv"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def number(frame: pd.DataFrame, column: str) -> pd.Series:
    if column not in frame:
        return pd.Series(np.nan, index=frame.index, dtype=float)
    return pd.to_numeric(
        frame[column].astype(str).str.strip().replace({"": np.nan}), errors="coerce"
    )


def date(frame: pd.DataFrame, column: str) -> pd.Series:
    if column not in frame:
        return pd.Series(pd.NaT, index=frame.index, dtype="datetime64[ns]")
    return pd.to_datetime(frame[column], errors="coerce", format="mixed")


def clean_key(series: pd.Series) -> pd.Series:
    return (
        series.astype("string")
        .str.strip()
        .replace({"": pd.NA, "nan": pd.NA, "None": pd.NA})
    )


def pct(numerator: int, denominator: int) -> float:
    return round(100.0 * numerator / denominator, 2)


def suppress_event_cell(value: int) -> int | str:
    return value if value >= 10 else "<10"


def reconstruct_wales(raw: pd.DataFrame) -> tuple[dict, pd.Series, pd.Series, pd.Series]:
    dob = date(raw, "DOB").fillna(date(raw, "DOB_1"))

    def age_at(column: str) -> pd.Series:
        return (date(raw, column) - dob).dt.total_seconds() / (365.25 * 86400.0)

    baseline_age = age_at("MeasurementDate.1")
    baseline_date = date(raw, "MeasurementDate.1")
    event_age = pd.concat(
        [
            number(raw, c)
            for c in [
                "MIACSAge",
                "PCIStentsAge",
                "CABGAge",
                "ANGINAAge",
                "TIAAge",
                "PVDAge",
            ]
        ],
        axis=1,
    ).min(axis=1)
    outcome_positive = number(raw, "ascvd_combine").fillna(0).gt(0)
    genotype_positive = (
        raw["Positive1"].astype(str).str.strip().isin(["1", "1.0"])
    )
    last_clinic_age = pd.concat(
        [age_at(f"MeasurementDate.{i}") for i in range(1, 5)] + [age_at("BMIDate")],
        axis=1,
    ).max(axis=1)
    death_age = number(raw, "AGE_AT_DECEASED")
    operational_censor_age = death_age.fillna(last_clinic_age)

    flow = {}
    active = genotype_positive.copy()
    flow["genotype_positive_start"] = int(active.sum())
    exclude = active & baseline_age.isna()
    flow["excluded_missing_baseline"] = int(exclude.sum())
    active &= ~exclude
    exclude = active & outcome_positive & event_age.notna() & event_age.le(baseline_age)
    flow["excluded_prevalent_ascvd"] = int(exclude.sum())
    active &= ~exclude
    exclude = active & outcome_positive & event_age.isna()
    flow["excluded_outcome_positive_without_event_age"] = int(exclude.sum())
    active &= ~exclude
    no_positive_followup = active & ~operational_censor_age.gt(baseline_age)
    flow["excluded_without_positive_operational_followup"] = int(no_positive_followup.sum())
    dated_incident_excluded = (
        no_positive_followup
        & outcome_positive
        & event_age.notna()
        & event_age.gt(baseline_age)
    )
    flow["dated_incident_events_excluded_by_followup_rule"] = int(dated_incident_excluded.sum())
    active &= ~no_positive_followup

    incident = (
        active
        & outcome_positive
        & event_age.notna()
        & event_age.gt(baseline_age)
    )
    followup = pd.Series(
        np.where(incident, event_age, operational_censor_age) - baseline_age,
        index=raw.index,
    ).clip(lower=0)

    gender = raw["Gender"].astype("string").str.strip().str.upper()
    male = gender.isin(["M", "MALE", "1"]).astype(float)
    family = raw.loc[active, "FamilyNumber"].astype(str).to_numpy()
    cohort = pd.DataFrame(
        {
            "age": baseline_age.loc[active].to_numpy(float),
            "male": male.loc[active].to_numpy(float),
            "time": followup.loc[active].to_numpy(float),
            "event": incident.loc[active].to_numpy(int),
            "family": family,
        }
    ).reset_index(drop=True)

    prediction = np.zeros(len(cohort), dtype=float)
    for train, test in GroupKFold(10).split(
        np.zeros(len(cohort)), cohort["event"].to_numpy(), groups=cohort["family"].to_numpy()
    ):
        x = cohort[["age", "male"]].astype(float)
        x = x.fillna(x.iloc[train].median())
        for column in ["age", "male"]:
            if x[column].nunique() > 2:
                sd = max(float(x[column].iloc[train].std()), 1e-9)
                x[column] = (x[column] - float(x[column].iloc[train].mean())) / sd
        fit_data = x.iloc[train].copy()
        fit_data["T"] = cohort["time"].to_numpy()[train]
        fit_data["E"] = cohort["event"].to_numpy()[train]
        fit = CoxPHFitter(penalizer=0.05).fit(fit_data, "T", "E")
        prediction[test] = np.log(
            fit.predict_partial_hazard(x.iloc[test]).to_numpy() + 1e-12
        )
    c_index = float(
        concordance_index(
            cohort["time"].to_numpy(), -prediction, cohort["event"].to_numpy()
        )
    )

    valid_ldl = number(raw, "LDL.1").where(number(raw, "LDL.1").between(0.3, 20, inclusive="neither"))
    valid_hdl = number(raw, "HDL.1").where(number(raw, "HDL.1").between(0.2, 5, inclusive="neither"))
    valid_tg = number(raw, "TRG.1").where(number(raw, "TRG.1").between(0.2, 25, inclusive="neither"))
    valid_lpa_v1 = number(raw, "Lpa.1").where(number(raw, "Lpa.1").ge(0))
    lpa_any = pd.concat([number(raw, f"Lpa.{i}") for i in range(1, 5)], axis=1).max(axis=1)
    sex_known = gender.isin(["M", "MALE", "1", "F", "FEMALE", "0"])

    smoking_numeric = pd.to_numeric(raw["Smoking"].astype("string").str.strip(), errors="coerce")
    smoking_valid = smoking_numeric.isin([0, 1])

    bp_date = date(raw, "BloodPressureDate")
    sbp = number(raw, "BloodPressureSystolic")
    dbp = number(raw, "BloodPressureDiastolic")
    bp_pair = sbp.between(50, 300) & dbp.between(20, 200)
    bp_pair_prebaseline = bp_pair & bp_date.notna() & bp_date.le(baseline_date)
    bp_medication = number(raw, "BloodPressureMedication")

    diabetes_text = raw["Diabetes"].astype("string").str.strip().str.lower()
    diabetes_yes = diabetes_text.isin(["yes", "y", "1", "1.0", "true"])
    diabetes_no = diabetes_text.isin(["no", "n", "0", "0.0", "false"])
    diabetes_year = number(raw, "DiabetesYear")
    dated_diabetes_prebaseline = (
        diabetes_yes
        & diabetes_year.notna()
        & diabetes_year.le(baseline_date.dt.year)
    )

    treatment_dates = pd.concat(
        [date(raw, f"Treatmentdate{i}") for i in range(1, 4)], axis=1
    )
    treatment_prebaseline = treatment_dates.le(baseline_date, axis=0).any(axis=1)
    treatment_date1_prebaseline = (
        date(raw, "Treatmentdate1").notna()
        & date(raw, "Treatmentdate1").le(baseline_date)
    )
    visit1_drug = pd.Series(False, index=raw.index)
    for column in ["Treatment1.1", "Treatment1.2", "Treatment1.3"]:
        text = raw[column].astype(str).str.strip().str.lower()
        visit1_drug |= ~text.isin(["", "nan", "none", "nat"])

    n = int(active.sum())
    complete_lipids = active & sex_known & valid_ldl.notna() & valid_hdl.notna() & valid_tg.notna()
    complete_tghdl = active & sex_known & valid_tg.notna() & valid_hdl.notna()
    event_after_last_clinic = incident & event_age.gt(last_clinic_age)
    event_after_operational_censor = incident & event_age.gt(operational_censor_age)

    availability = {
        "age": {"n": n, "coverage_pct": 100.0, "prebaseline": True},
        "sex": {"n": int((active & sex_known).sum()), "coverage_pct": pct(int((active & sex_known).sum()), n), "prebaseline": True},
        "ldl_v1_measured": {"n": int(valid_ldl.loc[active].notna().sum()), "coverage_pct": pct(int(valid_ldl.loc[active].notna().sum()), n), "prebaseline": True},
        "hdl_v1": {"n": int(valid_hdl.loc[active].notna().sum()), "coverage_pct": pct(int(valid_hdl.loc[active].notna().sum()), n), "prebaseline": True},
        "triglycerides_v1": {"n": int(valid_tg.loc[active].notna().sum()), "coverage_pct": pct(int(valid_tg.loc[active].notna().sum()), n), "prebaseline": True},
        "tg_hdl_ratio": {"n": int((valid_tg.notna() & valid_hdl.notna() & active).sum()), "coverage_pct": pct(int((valid_tg.notna() & valid_hdl.notna() & active).sum()), n), "prebaseline": True},
        "smoking_explicit_0_or_1": {"n": int((active & smoking_valid).sum()), "coverage_pct": pct(int((active & smoking_valid).sum()), n), "prebaseline": False},
        "bp_pair_dated_prebaseline": {"n": int((active & bp_pair_prebaseline).sum()), "coverage_pct": pct(int((active & bp_pair_prebaseline).sum()), n), "prebaseline": True},
        "bp_medication_status_undated": {"n": int((active & bp_medication.notna()).sum()), "coverage_pct": pct(int((active & bp_medication.notna()).sum()), n), "prebaseline": False},
        "diabetes_status_undated": {"n": int((active & (diabetes_yes | diabetes_no)).sum()), "coverage_pct": pct(int((active & (diabetes_yes | diabetes_no)).sum()), n), "prebaseline": False},
        "dated_prebaseline_diabetes_positive_only": {"n": int((active & dated_diabetes_prebaseline).sum()), "coverage_pct": pct(int((active & dated_diabetes_prebaseline).sum()), n), "prebaseline": True},
        "lpa_v1": {"n": int(valid_lpa_v1.loc[active].notna().sum()), "coverage_pct": pct(int(valid_lpa_v1.loc[active].notna().sum()), n), "prebaseline": True},
        "lpa_any_visit": {"n": int(lpa_any.loc[active].notna().sum()), "coverage_pct": pct(int(lpa_any.loc[active].notna().sum()), n), "prebaseline": False},
        "untreated_ldl_directly_observed": {"n": 0, "coverage_pct": 0.0, "prebaseline": False},
        "cumulative_ldl_valid_at_baseline": {"n": 0, "coverage_pct": 0.0, "prebaseline": False},
    }

    result = {
        "definition": "Positive1 in {1, 1.0}; dated V1; exclude prevalent and undated outcome-positive records; require operational censor age > V1 age",
        "flow": flow,
        "n": n,
        "events": int(incident.sum()),
        "family_clusters_code_style": int(pd.Series(family).nunique()),
        "nonmissing_family_values": int(clean_key(raw.loc[active, "FamilyNumber"]).nunique(dropna=True)),
        "missing_family_records": int(clean_key(raw.loc[active, "FamilyNumber"]).isna().sum()),
        "person_years": float(followup.loc[active].sum()),
        "median_followup_years": float(followup.loc[active].median()),
        "age_sex_groupkfold10_c": c_index,
        "censoring_audit": {
            "dated_incident_events_excluded_only_by_operational_followup_rule": int(dated_incident_excluded.sum()),
            "retained_events_after_last_clinic_measure": suppress_event_cell(int(event_after_last_clinic.sum())),
            "retained_events_after_operational_censor": suppress_event_cell(int(event_after_operational_censor.sum())),
        },
        "temporality_gate": {
            "incident_events_with_dated_prebaseline_age_sex": int((incident & sex_known).sum()),
            "incident_events_complete_age_sex_tg_hdl": int((incident & complete_tghdl).sum()),
            "incident_events_complete_age_sex_ldl_hdl_tg": int((incident & complete_lipids).sum()),
            "threshold": 40,
        },
        "treatment_timing": {
            "any_treatment_start_date_on_or_before_baseline": int((active & treatment_prebaseline).sum()),
            "treatmentdate1_on_or_before_baseline": int((active & treatment_date1_prebaseline).sum()),
            "visit1_drug_record_present": int((active & visit1_drug).sum()),
            "visit1_drug_record_without_prebaseline_start_date": int((active & visit1_drug & ~treatment_prebaseline).sum()),
        },
        "smoking_mapping": {
            "rule": "Smoking == 1 is yes; Smoking == 0 is no; Unknown/blank remain missing",
            "yes": int((active & smoking_numeric.eq(1)).sum()),
            "no": int((active & smoking_numeric.eq(0)).sum()),
            "unknown_or_missing": int((active & ~smoking_valid).sum()),
        },
        "genotyping_score": {
            "available_n": int((active & number(raw, "GenoTypingScore").notna()).sum()),
            "retained_in_proposed_specification": False,
        },
        "availability": availability,
    }
    return result, active, incident, baseline_age


def pass_crosscheck(pass_frame: pd.DataFrame, raw: pd.DataFrame, active: pd.Series) -> dict:
    positive = number(pass_frame, "mutation_positive").eq(1)
    p = pass_frame.loc[positive].copy()
    reference_date = pd.Timestamp("2025-09-30")
    inferred_birth = reference_date - pd.to_timedelta(number(p, "age_days"), unit="D")
    v1_date = date(p, "v1_date")
    age_v1 = (v1_date - inferred_birth).dt.total_seconds() / (365.25 * 86400.0)
    event_age = number(p, "age_at_hard_event")
    hard = number(p, "event_hard_any").eq(1)
    known = hard & age_v1.notna() & event_age.notna()
    prior = known & event_age.lt(age_v1)
    unknown = hard & ~known
    risk = age_v1.notna() & ~prior & ~unknown
    death_date = date(p, "deceased_date")
    death_age = (death_date - inferred_birth).dt.total_seconds() / (365.25 * 86400.0)
    end_age = number(p, "age_years").copy()
    valid_death = death_age.notna() & death_age.ge(age_v1)
    end_age.loc[valid_death] = np.minimum(end_age.loc[valid_death], death_age.loc[valid_death])
    risk &= end_age.notna() & end_age.gt(age_v1)
    incident = risk & hard & event_age.ge(age_v1) & event_age.le(end_age)
    event10 = incident & (event_age - age_v1).le(10)
    analysis_time = pd.Series(np.where(incident, event_age, end_age) - age_v1, index=p.index)
    family = clean_key(p.loc[risk, "family_id"])

    raw_key = clean_key(raw["DatabaseNumber"])
    pass_key = clean_key(pass_frame["participant_id"])
    selected_keys = set(raw_key.loc[active].dropna())
    linked = pass_frame.loc[pass_key.isin(selected_keys)]

    return {
        "rows": int(len(pass_frame)),
        "mutation_positive": int(positive.sum()),
        "raw_to_pass_unique_id_matches": int(len(set(raw_key.dropna()) & set(pass_key.dropna()))),
        "raw_clean_cohort_rows_matched": int(len(linked)),
        "raw_clean_cohort_rows_matched_mutation_positive": int(number(linked, "mutation_positive").eq(1).sum()),
        "hard_endpoint_risk_set_n": int(risk.sum()),
        "hard_endpoint_events_all_followup": int(incident.sum()),
        "hard_endpoint_events_within_10y": int(event10.sum()),
        "family_clusters_with_missing_as_singletons": int(family.nunique(dropna=True) + family.isna().sum()),
        "person_years_all_followup": float(analysis_time.loc[risk].sum()),
        "median_followup_years": float(analysis_time.loc[risk].median()),
        "warning": "This PASS risk set uses a hard endpoint and a 2025-09-30 extraction-reference clock; it is not the 1,159/92 broad-composite cohort.",
    }


def main() -> None:
    for path in [WALES, PASS, OUT]:
        if path.name == FORBIDDEN_BASENAME:
            raise RuntimeError("Forbidden source path")
    raw = pd.read_csv(WALES, low_memory=False)
    pass_frame = pd.read_csv(PASS, low_memory=False)
    wales, active, _, _ = reconstruct_wales(raw)
    result = {
        "governance": {
            "aggregate_only": True,
            "participant_rows_written": False,
            "identifiers_written": False,
            "family_identifiers_written": False,
            "variant_coordinates_written": False,
            "small_event_cells_suppressed_below": 10,
            "forbidden_file_opened": False,
        },
        "sources": {
            "wales": {"path": str(WALES), "sha256": sha256(WALES), "rows": len(raw), "columns": raw.shape[1]},
            "pass": {"path": str(PASS), "sha256": sha256(PASS), "rows": len(pass_frame), "columns": pass_frame.shape[1]},
        },
        "wales_legacy_clean_reproduction": wales,
        "pass_crosscheck": pass_crosscheck(pass_frame, raw, active),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
