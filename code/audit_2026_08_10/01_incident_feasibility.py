#!/usr/bin/env python3
"""A1: independently test whether a DRAGON incident landmark design is feasible.

Only aggregate results are printed or written. Event component cells below ten
are suppressed before serialisation.
"""
from __future__ import annotations

from datetime import datetime
import json
import re

import numpy as np
import pandas as pd
from lifelines import CoxPHFitter
from lifelines.utils import concordance_index

from audit_common import DRAGON_RAW, OUT, event_count, input_paths, num, write_json


DATE_COLUMNS = [
    "BirthDate", "TodayDate",
    "MeasurementDate_1", "MeasurementDate_2", "MeasurementDate_3", "MeasurementDate_4",
]
COMPONENTS = {
    "MI/ACS": "MIACSYear",
    "PCI": "PTCAYear",
    "CABG": "CABGYear",
    "angina": "ANGINAYear",
    "TIA": "TIAYear",
    "PVD": "PVDYear",
}
LIPID_LIMITS = {"LDL": (0.3, 20.0), "HDL": (0.2, 5.0), "Lpa": (0.0, 1000.0)}
DAY_PER_YEAR = 365.2425
COX_BOOT = 2000


def clean_string(value: object) -> str:
    if pd.isna(value):
        return ""
    text = str(value).strip()
    return "" if text.lower() in {"", "nan", "none", "nat"} else text


def parse_mixed_date(value: object) -> tuple[pd.Timestamp | pd.NaT, str]:
    """Parse documented mixed formats without silently changing date order."""
    text = clean_string(value)
    if not text:
        return pd.NaT, "blank"
    attempts: list[tuple[str, str]] = []
    if re.fullmatch(r"\d{1,2}/\d{1,2}/\d{2,4}", text):
        attempts = [("%m/%d/%Y", "slash_mdy"), ("%m/%d/%y", "slash_mdy_2digit"),
                    ("%d/%m/%Y", "slash_dmy_fallback"), ("%d/%m/%y", "slash_dmy_2digit_fallback")]
    elif re.fullmatch(r"\d{1,2}-\d{1,2}-\d{2,4}", text):
        attempts = [("%d-%m-%Y", "hyphen_dmy"), ("%d-%m-%y", "hyphen_dmy_2digit"),
                    ("%m-%d-%Y", "hyphen_mdy_fallback"), ("%m-%d-%y", "hyphen_mdy_2digit_fallback")]
    elif re.fullmatch(r"\d{4}-\d{1,2}-\d{1,2}", text):
        attempts = [("%Y-%m-%d", "iso_ymd")]
    elif re.fullmatch(r"\d{1,2}\.\d{1,2}\.\d{2,4}", text):
        attempts = [("%d.%m.%Y", "dot_dmy"), ("%d.%m.%y", "dot_dmy_2digit")]
    else:
        return pd.NaT, "unrecognised"
    for date_format, label in attempts:
        try:
            parsed = datetime.strptime(text, date_format)
        except ValueError:
            continue
        if "%y" in date_format and parsed.year > 2027:
            parsed = parsed.replace(year=parsed.year - 100)
        if not 1890 <= parsed.year <= 2027:
            continue
        return pd.Timestamp(parsed), label
    return pd.NaT, "invalid"


def parse_series(series: pd.Series) -> tuple[pd.Series, dict[str, int]]:
    parsed: list[pd.Timestamp | pd.NaT] = []
    status: list[str] = []
    for value in series:
        date, label = parse_mixed_date(value)
        parsed.append(date)
        status.append(label)
    parsed_series = pd.Series(parsed, index=series.index, dtype="datetime64[ns]")
    nonblank = pd.Series(status, index=series.index).ne("blank")
    failed = nonblank & parsed_series.isna()
    labels = pd.Series(status).value_counts()
    return parsed_series, {
        "nonblank": int(nonblank.sum()),
        "parsed": int(parsed_series.notna().sum()),
        "failed": int(failed.sum()),
        "slash_mdy": int(labels.get("slash_mdy", 0) + labels.get("slash_mdy_2digit", 0)),
        "slash_dmy_fallback": int(labels.get("slash_dmy_fallback", 0) + labels.get("slash_dmy_2digit_fallback", 0)),
        "hyphen_dmy": int(labels.get("hyphen_dmy", 0) + labels.get("hyphen_dmy_2digit", 0)),
        "hyphen_mdy_fallback": int(labels.get("hyphen_mdy_fallback", 0) + labels.get("hyphen_mdy_2digit_fallback", 0)),
        "dot_dmy": int(labels.get("dot_dmy", 0) + labels.get("dot_dmy_2digit", 0)),
        "iso_ymd": int(labels.get("iso_ymd", 0)),
    }


def valid_lipid(raw: pd.DataFrame, slot: int) -> pd.Series:
    usable = pd.Series(False, index=raw.index)
    for lipid, (low, high) in LIPID_LIMITS.items():
        value = num(raw, f"{lipid}_{slot}")
        usable |= value.between(low, high)
    return usable


def extract_anchor(raw: pd.DataFrame, parsed_dates: dict[str, pd.Series]) -> tuple[pd.Series, pd.Series, dict]:
    usable_slots: list[pd.Series] = []
    date_present_slots: list[pd.Series] = []
    dated_candidates: list[pd.Series] = []
    for slot in range(1, 5):
        usable = valid_lipid(raw, slot)
        date_column = f"MeasurementDate_{slot}"
        date_present = raw[date_column].map(clean_string).ne("")
        usable_slots.append(usable)
        date_present_slots.append(usable & date_present)
        dated_candidates.append(parsed_dates[date_column].where(usable))
    any_lipid = np.logical_or.reduce([value.to_numpy() for value in usable_slots])
    any_dated_text = np.logical_or.reduce([value.to_numpy() for value in date_present_slots])
    candidate_table = pd.concat(dated_candidates, axis=1)
    anchor = candidate_table.min(axis=1)
    anchor_slot = pd.Series(np.nan, index=raw.index)
    for row_position in np.flatnonzero(anchor.notna().to_numpy()):
        dates = candidate_table.iloc[row_position]
        matching = np.flatnonzero(dates.eq(anchor.iloc[row_position]).to_numpy())
        if matching.size:
            anchor_slot.iloc[row_position] = int(matching[0] + 1)
    reasons = {
        "no_usable_lipid_in_four_slots": int((~any_lipid).sum()),
        "usable_lipid_but_no_date_text": int((any_lipid & ~any_dated_text).sum()),
        "usable_lipid_with_date_text_but_unparseable": int((any_lipid & any_dated_text & anchor.isna().to_numpy()).sum()),
        "parseable_anchor": int(anchor.notna().sum()),
    }
    if sum(reasons.values()) != len(raw):
        raise RuntimeError("Anchor-loss categories are not exhaustive")
    return anchor, anchor_slot, reasons


def component_ages(
    raw: pd.DataFrame,
    birth: pd.Series,
) -> tuple[pd.DataFrame, dict[str, dict[str, int]]]:
    ages = pd.DataFrame(index=raw.index)
    audit: dict[str, dict[str, int]] = {}
    birth_year = birth.dt.year
    for label, column in COMPONENTS.items():
        value = num(raw, column)
        age_coded = value.between(0, 110)
        calendar_coded = value.between(1900, 2027)
        converted = value.where(age_coded)
        converted = converted.where(~calendar_coded, value - birth_year)
        converted = converted.where(converted.between(0, 110))
        ages[label] = converted
        nonblank = raw[column].map(clean_string).ne("")
        audit[label] = {
            "nonblank": int(nonblank.sum()),
            "numeric": int(value.notna().sum()),
            "age_coded": int(age_coded.sum()),
            "calendar_coded": int(calendar_coded.sum()),
            "unusable": int((nonblank & converted.isna()).sum()),
        }
    return ages, audit


def verify_age_interpretation(
    raw: pd.DataFrame,
    ages: pd.DataFrame,
    birth: pd.Series,
) -> dict:
    raw_components = pd.DataFrame({label: num(raw, column) for label, column in COMPONENTS.items()})
    minimum_raw = raw_components.min(axis=1)
    minimum_age = ages.min(axis=1)
    reported_event_age = num(raw, "age_at_event")
    compare_age = minimum_age.notna() & reported_event_age.notna()
    direct_error = (minimum_age[compare_age] - reported_event_age[compare_age]).abs()
    calendar_compare = minimum_raw.notna() & reported_event_age.notna() & birth.notna()
    calendar_implied_age = minimum_raw[calendar_compare] - birth[calendar_compare].dt.year
    calendar_error = (calendar_implied_age - reported_event_age[calendar_compare]).abs()
    return {
        "rows_compared_to_reported_event_age": int(compare_age.sum()),
        "direct_age_interpretation_median_absolute_error_years": float(direct_error.median()) if len(direct_error) else None,
        "direct_age_interpretation_within_one_year_pct": float(100 * direct_error.le(1).mean()) if len(direct_error) else None,
        "calendar_year_interpretation_median_absolute_error_years": float(calendar_error.median()) if len(calendar_error) else None,
        "calendar_year_interpretation_within_one_year_pct": float(100 * calendar_error.le(1).mean()) if len(calendar_error) else None,
        "conclusion": "age_at_event_not_calendar_year" if len(direct_error) and direct_error.median() < calendar_error.median() else "not_resolved",
    }


def cox_if_viable(
    raw: pd.DataFrame,
    anchor_slot: pd.Series,
    anchor_age: pd.Series,
    at_risk: pd.Series,
    follow_up: pd.Series,
    incident: pd.Series,
) -> dict:
    if int(incident.sum()) < 40:
        return {"status": "not_fitted_gate_failed", "c_index": None, "c_index_ci": None}
    frame = pd.DataFrame(index=raw.index)
    frame["age"] = anchor_age
    frame["male"] = raw["Gender"].astype("string").str.strip().str.upper().eq("M").astype(float)
    sbp, dbp = num(raw, "BloodPressureSystolic"), num(raw, "BloodPressureDiastolic")
    bp_med = num(raw, "BloodPressureMedication")
    frame["hypertension"] = (sbp.ge(140) | dbp.ge(90) | bp_med.gt(0)).astype(float)
    smoking = num(raw, "Smoking_binary")
    frame["smoke_ever"] = smoking.gt(0).astype(float).where(smoking.notna())
    anchor_ldl = pd.Series(np.nan, index=raw.index)
    anchor_hdl = pd.Series(np.nan, index=raw.index)
    for slot in range(1, 5):
        use = anchor_slot.eq(slot)
        anchor_ldl.loc[use] = num(raw, f"LDL_{slot}").loc[use]
        anchor_hdl.loc[use] = num(raw, f"HDL_{slot}").loc[use]
    frame["hdl"] = anchor_hdl.where(anchor_hdl.between(0.2, 5))
    apob = num(raw, "ApoB").where(num(raw, "ApoB").between(0.2, 4))
    apoa1 = num(raw, "ApoA1").where(num(raw, "ApoA1").between(0.3, 4))
    ldl = anchor_ldl.where(anchor_ldl.between(0.3, 20))
    frame["log_ratio"] = np.log((apob / ldl).where(lambda value: value.gt(0)))
    frame["log_apoa1"] = np.log(apoa1)
    frame["duration"] = follow_up
    frame["event"] = incident.astype(int)
    family = raw["FamilyNumber"].astype("string").str.strip()
    missing = family.isna() | family.eq("")
    family.loc[missing] = "INTERNAL_ROW_" + pd.Series(np.arange(len(raw)), index=raw.index).astype(str)
    frame["cluster"] = family
    frame = frame.loc[at_risk].copy()
    for column in ["age", "male", "hdl", "hypertension", "smoke_ever", "log_ratio", "log_apoa1"]:
        median = frame[column].median()
        if not np.isfinite(median):
            raise RuntimeError(f"No usable values for Cox feature {column}")
        frame[column] = frame[column].fillna(median)
    for column in ["age", "hdl", "log_ratio", "log_apoa1"]:
        scale = frame[column].std(ddof=0)
        frame[column] = (frame[column] - frame[column].mean()) / max(scale, 1e-9)
    fit_columns = ["duration", "event", "cluster"] + [
        "age", "male", "hdl", "hypertension", "smoke_ever", "log_ratio", "log_apoa1"
    ]
    cox = CoxPHFitter(penalizer=0.1)
    cox.fit(frame[fit_columns], duration_col="duration", event_col="event", cluster_col="cluster", robust=True)
    risk = cox.predict_partial_hazard(frame).to_numpy()
    point = float(concordance_index(frame["duration"], -risk, frame["event"]))
    rng = np.random.default_rng(20260811)
    groups = frame["cluster"].to_numpy()
    levels = pd.unique(groups)
    members = {group: np.flatnonzero(groups == group) for group in levels}
    values: list[float] = []
    for _ in range(COX_BOOT):
        draw = rng.choice(levels, len(levels), replace=True)
        index = np.concatenate([members[group] for group in draw])
        if frame["event"].to_numpy()[index].sum() < 2:
            continue
        values.append(concordance_index(
            frame["duration"].to_numpy()[index], -risk[index], frame["event"].to_numpy()[index]
        ))
    return {
        "status": "fitted_family_cluster_robust",
        "penalizer": 0.1,
        "c_index": point,
        "c_index_ci": [float(value) for value in np.percentile(values, [2.5, 97.5])],
        "bootstrap_replicates": COX_BOOT,
    }


def main() -> None:
    input_paths()  # includes the explicit prohibited-source guard
    raw = pd.read_csv(DRAGON_RAW, low_memory=False)
    if len(raw) != 424:
        raise RuntimeError("Unexpected DRAGON row count")

    parsed: dict[str, pd.Series] = {}
    parsing: dict[str, dict[str, int]] = {}
    for column in DATE_COLUMNS:
        parsed[column], parsing[column] = parse_series(raw[column])
    failed_rows = pd.Series(False, index=raw.index)
    for column in DATE_COLUMNS:
        failed_rows |= raw[column].map(clean_string).ne("") & parsed[column].isna()
    parsing["rows_with_any_nonblank_date_parse_failure"] = int(failed_rows.sum())

    anchor, anchor_slot, anchor_flow = extract_anchor(raw, parsed)
    birth = parsed["BirthDate"]
    anchor_age = (anchor - birth).dt.total_seconds() / (DAY_PER_YEAR * 86400)
    valid_anchor_age = anchor.notna() & birth.notna() & anchor_age.between(0, 105)
    component_age, component_encoding = component_ages(raw, birth)
    age_verification = verify_age_interpretation(raw, component_age, birth)

    prevalent = valid_anchor_age & component_age.le(anchor_age, axis=0).any(axis=1)
    censor_age = num(raw, "age_at_event_or_censoring").where(lambda value: value.between(0, 110))
    censor_missing = valid_anchor_age & ~prevalent & censor_age.isna()
    censor_before_anchor = valid_anchor_age & ~prevalent & censor_age.notna() & censor_age.lt(anchor_age)
    at_risk = valid_anchor_age & ~prevalent & censor_age.notna() & censor_age.ge(anchor_age)

    incident_components = pd.DataFrame(index=raw.index)
    after_censor = pd.DataFrame(index=raw.index)
    for component in COMPONENTS:
        incident_components[component] = (
            at_risk & component_age[component].gt(anchor_age) & component_age[component].le(censor_age)
        )
        after_censor[component] = at_risk & component_age[component].gt(censor_age)
    incident = incident_components.any(axis=1)
    first_incident_age = component_age.where(incident_components).min(axis=1)
    end_age = censor_age.where(~incident, first_incident_age)
    follow_up = (end_age - anchor_age).where(at_risk)
    if follow_up.loc[at_risk].lt(0).any():
        raise RuntimeError("Negative follow-up survived landmark checks")

    incident_n_raw = int(incident.sum())
    if incident_n_raw >= 40:
        gate = "viable_as_primary"
        gate_verdict = "yes"
    elif incident_n_raw >= 25:
        gate = "report_both_neither_primary"
        gate_verdict = "borderline"
    else:
        gate = "not_viable_prevalent_design_stands"
        gate_verdict = "no"

    death_columns = [column for column in raw.columns if re.search(r"death|deceased|mortality|cause.*death|\bdod\b", column, re.I)]
    death_nonblank_columns = [
        column for column in death_columns if raw[column].map(clean_string).ne("").any()
    ]
    death_date_like = [column for column in death_nonblank_columns if re.search(r"date|age|year|dod", column, re.I)]
    death_cause_like = [column for column in death_nonblank_columns if re.search(r"cause|cv|card", column, re.I)]
    non_cv_death_identifiable = bool(death_date_like and death_cause_like)

    first_component_age = component_age.min(axis=1)
    current_age = num(raw, "Currentage")
    flag_case = num(raw, "ASCVD_combined").fillna(0).gt(0)
    timing_comparable = flag_case & first_component_age.notna() & current_age.notna()
    current_age_after_event = timing_comparable & current_age.gt(first_component_age)

    result = {
        "task": "A1_incident_feasibility",
        "rows_total": len(raw),
        "date_parsing": parsing,
        "anchor_flow": anchor_flow,
        "post_anchor_exclusions": {
            "anchor_with_unparseable_birth_date": int((anchor.notna() & birth.isna()).sum()),
            "anchor_age_outside_0_to_105": int((anchor.notna() & birth.notna() & ~anchor_age.between(0, 105)).sum()),
            "prevalent_at_anchor": event_count(int(prevalent.sum())),
            "missing_or_invalid_censor_age_after_excluding_prevalent": int(censor_missing.sum()),
            "censor_before_anchor_after_excluding_prevalent": int(censor_before_anchor.sum()),
            "incident_risk_set_n": int(at_risk.sum()),
        },
        "event_field_interpretation": {
            "by_component": {
                component: {
                    measure: event_count(value)
                    for measure, value in measures.items()
                }
                for component, measures in component_encoding.items()
            },
            "cross_check": age_verification,
        },
        "landmark_results": {
            "prevalent_at_anchor_n": event_count(int(prevalent.sum())),
            "incident_after_anchor_n": event_count(incident_n_raw),
            "incident_components": {
                component: event_count(int(incident_components[component].sum()))
                for component in COMPONENTS
            },
            "events_recorded_after_censor_across_any_component_n": event_count(int(after_censor.any(axis=1).sum())),
            "person_years": float(follow_up.loc[at_risk].sum()),
            "median_follow_up_years": float(follow_up.loc[at_risk].median()),
            "events_per_candidate_predictor": (
                float(incident_n_raw / 7)
                if incident_n_raw >= 10
                else "<10, non-estimable"
            ),
            "candidate_predictor_count": 7,
        },
        "incident_gate": {
            "rule": ">=40 primary; 25-39 both/neither primary; <25 not viable",
            "classification": gate,
            "incident_analysis_viable": gate_verdict,
        },
        "cox_model": cox_if_viable(raw, anchor_slot, anchor_age, at_risk, follow_up, incident),
        "competing_risk": {
            "non_cv_death_identifiable": non_cv_death_identifiable,
            "candidate_death_fields_present_n": len(death_columns),
            "candidate_death_fields_with_data_n": len(death_nonblank_columns),
            "fine_gray_status": "eligible" if non_cv_death_identifiable and incident_n_raw >= 40 else (
                "not_estimable_non_cv_death_not_identifiable" if not non_cv_death_identifiable
                else "not_fitted_incident_gate_failed"
            ),
        },
        "temporality_audit": {
            "ascvd_cases_with_component_age_and_current_age_n": event_count(int(timing_comparable.sum())),
            "cases_where_current_age_is_after_first_recorded_event_n": event_count(int(current_age_after_event.sum())),
            "cases_prevalent_at_first_dated_lipid_anchor_n": event_count(int(prevalent.sum())),
            "apob_and_apoa1_have_no_linked_measurement_date": True,
            "hypertension_and_smoke_ever_have_no_historical_anchor": True,
            "interpretation": "The locked Welsh feature set is not demonstrably pre-outcome for prevalent cases.",
        },
        "ascvd_flag_component_consistency": {
            "registry_flag_events": event_count(int(flag_case.sum())),
            "component_union_events": event_count(int(component_age.notna().any(axis=1).sum())),
            "flag_positive_without_usable_component_age_n": event_count(int((flag_case & component_age.isna().all(axis=1)).sum())),
            "component_age_present_but_flag_negative_n": event_count(int((~flag_case & component_age.notna().any(axis=1)).sum())),
        },
        "participant_level_outputs": False,
    }
    write_json(OUT / "a1_incident_feasibility.json", result)
    print(json.dumps({
        "A1": {
            "parseable_anchor": anchor_flow["parseable_anchor"],
            "prevalent_at_anchor": result["landmark_results"]["prevalent_at_anchor_n"],
            "incident_after_anchor": result["landmark_results"]["incident_after_anchor_n"],
            "gate": gate,
        },
        "written": "outputs/audit_2026_08_10/a1_incident_feasibility.json",
    }, indent=2))


if __name__ == "__main__":
    main()
