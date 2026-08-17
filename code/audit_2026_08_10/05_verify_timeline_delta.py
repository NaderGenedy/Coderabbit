#!/usr/bin/env python3
"""Cheap aggregate-only verification of the seven post-audit timeline facts."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import chi2

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

from audit_common import OUT, event_count, write_json  # noqa: E402


def load_a1_module():
    path = HERE / "01_incident_feasibility.py"
    spec = importlib.util.spec_from_file_location("timeline_parser", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load the audit date parser")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    a1 = load_a1_module()
    raw = pd.read_csv(a1.DRAGON_RAW, low_memory=False)
    if len(raw) != 424:
        raise RuntimeError("DRAGON row-count invariant failed")

    birth, birth_parse = a1.parse_series(raw["BirthDate"])
    today, today_parse = a1.parse_series(raw["TodayDate"])
    blood_test_date, blood_parse = a1.parse_series(raw["Dateofbloodtest"])
    measurement_dates: dict[int, pd.Series] = {}
    for slot in range(1, 5):
        measurement_dates[slot], _ = a1.parse_series(raw[f"MeasurementDate_{slot}"])

    censor = a1.num(raw, "age_at_event_or_censoring")
    test_age = a1.num(raw, "Ageattest")
    comparable_test = censor.notna() & test_age.notna()
    exact_test_match = comparable_test & censor.eq(test_age)

    component_ages, _ = a1.component_ages(raw, birth)
    reported_event_age = a1.num(raw, "age_at_event")
    composite_beyond = (
        reported_event_age.notna() & censor.notna() & reported_event_age.gt(censor)
    )
    first_component_age = component_ages.min(axis=1)
    first_component_beyond = (
        first_component_age.notna() & censor.notna() & first_component_age.gt(censor)
    )
    any_component_beyond = (
        component_ages.notna() & component_ages.gt(censor, axis=0)
    ).any(axis=1)

    recent_blood = blood_test_date.dt.year.between(2018, 2025)
    today_in_2024 = today.dt.year.eq(2024)

    dated_ldl: list[pd.Series] = []
    for slot in range(1, 5):
        ldl = a1.num(raw, f"LDL_{slot}").where(lambda value: value.between(0.3, 20))
        dated_ldl.append(ldl.notna() & measurement_dates[slot].notna())
    dated_ldl_count = pd.concat(dated_ldl, axis=1).sum(axis=1)

    # The revised landmark definition uses the explicitly labelled first
    # measurement date, not the earliest slot that also contains a usable value.
    anchor_date = measurement_dates[1]
    anchor_age = (anchor_date - birth).dt.total_seconds() / (a1.DAY_PER_YEAR * 86400)
    anchor_censor_comparable = anchor_age.between(0, 105) & censor.between(0, 110)
    censor_before_anchor = anchor_censor_comparable & censor.lt(anchor_age)
    nonnegative_follow_up = anchor_censor_comparable & censor.ge(anchor_age)
    prevalent_at_anchor = (
        component_ages.notna() & component_ages.le(anchor_age, axis=0)
    ).any(axis=1) & nonnegative_follow_up
    incident_components = (
        component_ages.notna()
        & component_ages.gt(anchor_age, axis=0)
        & component_ages.le(censor, axis=0)
    )
    incident = incident_components.any(axis=1) & nonnegative_follow_up & ~prevalent_at_anchor
    follow_up = (censor - anchor_age).where(nonnegative_follow_up)

    observed_events = int(incident.sum())
    observed_py = float(follow_up.sum())
    observed_rate = 1000 * observed_events / observed_py
    rate_low = 1000 * 0.5 * chi2.ppf(0.025, 2 * observed_events) / observed_py
    rate_high = 1000 * 0.5 * chi2.ppf(0.975, 2 * (observed_events + 1)) / observed_py

    export_age = (today - birth).dt.total_seconds() / (a1.DAY_PER_YEAR * 86400)
    potential_valid = (
        anchor_age.between(0, 105) & export_age.between(0, 110) & export_age.ge(anchor_age)
    )
    potential_prevalent = (
        component_ages.notna() & component_ages.le(anchor_age, axis=0)
    ).any(axis=1) & potential_valid
    potential_risk_set = potential_valid & ~potential_prevalent
    potential_follow_up = (export_age - anchor_age).where(potential_risk_set)
    data_derived_py = float(potential_follow_up.sum())

    simple_py = int(nonnegative_follow_up.sum()) * 10.0
    projected_simple = observed_rate / 1000 * simple_py
    projected_data_derived = observed_rate / 1000 * data_derived_py

    result = {
        "task": "timeline_delta_verification",
        "rows_total": len(raw),
        "fact_1_censor_is_genetic_test_age": {
            "comparable_rows": int(comparable_test.sum()),
            "exact_matches": int(exact_test_match.sum()),
            "exact_match_pct_of_all_rows": float(100 * exact_test_match.sum() / len(raw)),
            "status": "verified_to_rounding",
        },
        "fact_2_event_capture_stops_at_test": {
            "composite_event_age_beyond_censor_n": event_count(int(composite_beyond.sum())),
            "first_component_age_beyond_censor_n": event_count(int(first_component_beyond.sum())),
            "any_component_age_beyond_censor_n": event_count(int(any_component_beyond.sum())),
            "status": "verified_only_for_composite_event_age_not_for_all_component_fields",
            "interpretation": (
                "The exact sub-10 composite/first-component cells are suppressed. At least one later component "
                "exceeds the recorded censor age in 24 rows, so the stronger claim that every component field "
                "was frozen at testing is not supported."
            ),
        },
        "fact_3_clinic_contact_after_outcome_freeze": {
            "blood_test_date_nonblank": blood_parse["nonblank"],
            "blood_test_date_parsed": blood_parse["parsed"],
            "blood_test_date_failed": blood_parse["failed"],
            "blood_tests_dated_2018_to_2025_n": int(recent_blood.sum()),
            "latest_blood_test_date": blood_test_date.max().strftime("%Y-%m-%d"),
            "today_date_in_2024_n": int(today_in_2024.sum()),
            "today_date_parsed_n": today_parse["parsed"],
            "status": "verified",
        },
        "fact_4_censor_before_first_measurement": {
            "first_measurement_anchor_and_censor_comparable_n": int(anchor_censor_comparable.sum()),
            "censor_before_first_measurement_n": int(censor_before_anchor.sum()),
            "status": "verified",
            "reconciliation_with_prior_77": (
                "The earlier audit's 77 was conditional on first excluding prevalent-at-anchor rows and used "
                "an earliest-usable-lipid anchor. The 109 count uses the explicitly labelled first measurement "
                "date before outcome exclusions."
            ),
        },
        "fact_5_revised_short_window": {
            "nonnegative_follow_up_n": int(nonnegative_follow_up.sum()),
            "prevalent_at_anchor_n": event_count(int(prevalent_at_anchor.sum())),
            "incident_first_events_n": event_count(observed_events),
            "person_years": observed_py,
            "median_follow_up_years": float(follow_up.median()),
            "follow_up_iqr_years": [float(follow_up.quantile(0.25)), float(follow_up.quantile(0.75))],
            "events_per_7_predictors": observed_events / 7,
            "incidence_rate_per_1000_py": observed_rate,
            "poisson_rate_95_ci_per_1000_py": [rate_low, rate_high],
            "status": "verified_with_one_governance_suppressed_prevalent_cell",
            "interpretation": (
                "This is a work-up/detection window, not a credible long-term natural-history incidence window."
            ),
        },
        "fact_6_contact_dependent_capture": {
            "claimed_rates_per_1000_py": {"with_marker": 4.8, "without_marker": 2.2},
            "status": "not_independently_verifiable_from_the_stated_definition",
            "reason": (
                "The recent-contact marker and its risk-time denominator were not defined. Plausible markers "
                "generate sub-10 event cells, for which rates must remain suppressed. The qualitative concern "
                "about informative outcome capture remains credible but the quoted pair should not be used until "
                "its exact code and denominator are supplied."
            ),
        },
        "fact_7_dated_ldl_density": {
            "dated_ldl_observations": int(sum(value.sum() for value in dated_ldl)),
            "participants_with_at_least_2": int(dated_ldl_count.ge(2).sum()),
            "participants_with_at_least_3": int(dated_ldl_count.ge(3).sum()),
            "participants_with_at_least_4": int(dated_ldl_count.ge(4).sum()),
            "status": "verified",
        },
        "refresh_arithmetic": {
            "simple_assumption_people": int(nonnegative_follow_up.sum()),
            "simple_assumption_years_each": 10.0,
            "simple_person_years": simple_py,
            "simple_projected_events_at_observed_rate": projected_simple,
            "simple_projected_events_using_rate_ci": [rate_low / 1000 * simple_py, rate_high / 1000 * simple_py],
            "data_derived_valid_export_anchors_n": int(potential_valid.sum()),
            "data_derived_prevalent_at_anchor_n": event_count(int(potential_prevalent.sum())),
            "data_derived_potential_risk_set_n": int(potential_risk_set.sum()),
            "data_derived_potential_person_years": data_derived_py,
            "data_derived_median_follow_up_years": float(potential_follow_up.median()),
            "data_derived_follow_up_iqr_years": [
                float(potential_follow_up.quantile(0.25)),
                float(potential_follow_up.quantile(0.75)),
            ],
            "data_derived_projected_events_at_observed_rate": projected_data_derived,
            "data_derived_projected_events_using_rate_ci": [
                rate_low / 1000 * data_derived_py,
                rate_high / 1000 * data_derived_py,
            ],
            "gate": ">=40 observed first incident events after refreshed linkage",
            "judgement": (
                "The 48-to-70 point-estimate arithmetic is correct. It is a feasibility forecast, not evidence "
                "that the gate will be met, because the source rate has 17 events, a wide interval, a short "
                "work-up window, possible informative capture, and no competing-death accounting."
            ),
        },
        "date_parser": {
            "birth_parsed_n": birth_parse["parsed"],
            "today_parsed_n": today_parse["parsed"],
        },
        "participant_level_outputs": False,
    }
    write_json(OUT / "timeline_delta_verification.json", result)
    print(json.dumps({
        "facts_verified": [1, 3, 4, 5, 7],
        "fact_2": "verified only for composite event age; contradicted for all-component interpretation",
        "fact_6": "not independently verifiable without marker code",
        "projected_events": [projected_simple, projected_data_derived],
        "written": "outputs/audit_2026_08_10/timeline_delta_verification.json",
    }, indent=2))


if __name__ == "__main__":
    main()
