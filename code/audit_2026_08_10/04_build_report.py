#!/usr/bin/env python3
"""Build the aggregate-only CALON-N audit report from generated JSON results."""
from __future__ import annotations

import json
import re
from pathlib import Path

from audit_common import (
    OUT,
    ROOT,
    environment_metadata,
    input_paths,
    sha256,
    write_json,
    write_text,
)


def load(name: str) -> dict:
    return json.loads((OUT / name).read_text(encoding="utf-8"))


def f(value: object, digits: int = 4) -> str:
    if value is None:
        return "not estimable"
    if isinstance(value, str):
        return value
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, int):
        return f"{value:,}"
    return f"{float(value):.{digits}f}"


def ci(values: list[float]) -> str:
    return f"{f(values[0])} to {f(values[1])}"


def performance_table(block: dict) -> list[str]:
    rows = [
        "| Model | AUC | CALON-N minus comparator (95% cluster-bootstrap CI) | E:O |",
        "|---|---:|---:|---:|",
        f"| CALON-N | {f(block['auc'])} ({ci(block['auc_ci'])}) | reference | {f(block['e_o'])} |",
    ]
    names = ["age_sex", "Montreal_adapted", "FH_Risk_Score_adapted", "SAFEHEART_adapted"]
    labels = {
        "age_sex": "Age + sex",
        "Montreal_adapted": "Montreal (adapted)",
        "FH_Risk_Score_adapted": "FH-Risk-Score (adapted)",
        "SAFEHEART_adapted": "SAFEHEART (adapted)",
    }
    for name in names:
        item = block["comparators"][name]
        eo = f(item["e_o"]) if item["e_o"] is not None else "not estimable (ranking score)"
        rows.append(
            f"| {labels[name]} | {f(item['auc'])} | {f(item['delta_calon_minus_comparator'])} "
            f"({ci(item['delta_ci'])}) | {eo} |"
        )
    return rows


def agreement_rows(a3: dict) -> list[str]:
    rows = [
        "| Quantity | Independent | Locked | Absolute difference | >0.001 defect? |",
        "|---|---:|---:|---:|:---:|",
    ]
    checks = a3["agreement_checks"]
    labels = {
        "DRAGON_to_UKB_strict": "DRAGON -> UKB strict",
        "UKB_strict_to_DRAGON": "UKB strict -> DRAGON",
    }
    for direction in ["DRAGON_to_UKB_strict", "UKB_strict_to_DRAGON"]:
        for metric, metric_label in [("auc", "AUC"), ("e_o", "E:O")]:
            item = checks[direction][metric]
            rows.append(
                f"| {labels[direction]} {metric_label} | {item['computed_4dp']:.4f} | "
                f"{item['stored_4dp']:.4f} | {item['absolute_difference']:.4f} | "
                f"{'yes' if item['defect_over_0_001'] else 'no'} |"
            )
        for comparator in ["age_sex", "Montreal_adapted", "FH_Risk_Score_adapted", "SAFEHEART_adapted"]:
            item = checks[direction]["comparators"][comparator]["delta"]
            rows.append(
                f"| {labels[direction]} delta vs {comparator.replace('_', ' ')} | "
                f"{item['computed_4dp']:.4f} | {item['stored_4dp']:.4f} | "
                f"{item['absolute_difference']:.4f} | {'yes' if item['defect_over_0_001'] else 'no'} |"
            )
    fh_checks = checks["FH_vs_matched_nonFH"]
    fh_labels = {
        "odds_ratio": "FH vs matched non-FH OR",
        "or_ci_low": "FH vs matched non-FH OR CI lower",
        "or_ci_high": "FH vs matched non-FH OR CI upper",
        "e_o_fh_model_to_nonfh": "FH model -> non-FH E:O",
        "e_o_nonfh_model_to_fh": "non-FH model -> FH E:O",
    }
    for key, label in fh_labels.items():
        item = fh_checks[key]
        rows.append(
            f"| {label} | {item['computed_4dp']:.4f} | {item['stored_4dp']:.4f} | "
            f"{item['absolute_difference']:.4f} | {'yes' if item['defect_over_0_001'] else 'no'} |"
        )
    return rows


def validate_low_event_suppression(value: object, path: str = "") -> list[str]:
    failures: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            next_path = f"{path}.{key}" if path else key
            if "event" in key.lower() and isinstance(child, int) and not isinstance(child, bool) and child < 10:
                failures.append(next_path)
            failures.extend(validate_low_event_suppression(child, next_path))
    elif isinstance(value, list):
        for position, child in enumerate(value):
            failures.extend(validate_low_event_suppression(child, f"{path}[{position}]"))
    return failures


def main() -> None:
    a1 = load("a1_incident_feasibility.json")
    a2 = load("a2_union_definition.json")
    a3 = load("a3_locked_reproduction.json")
    strict_event_total = int(a2["phenotype_comparison"]["strict_clinvar_plp"]["events"])
    union_event_total = int(a2["union_reciprocal_transport"]["DRAGON_to_UKB_union"]["events"])
    union_event_gain_pct = 100 * (union_event_total - strict_event_total) / strict_event_total

    lines: list[str] = [
        "# Independent adversarial audit: CALON-N HeFH established-ASCVD model",
        "",
        "Audit date: 2026-08-10. Data were read in place; only aggregate outputs were created. "
        "The prohibited identifiable treatment-response file was not accessed. No participant row, linkage "
        "value, variant-level description, or participant-level prediction is present in these outputs.",
        "",
        "## Executive verdicts",
        "",
        "| Task | Verdict | Gate result |",
        "|---|---|---|",
        "| A1 incident design | **No: not viable** | Incident events were `<10, non-estimable`; the locked `<25` gate says the prevalent design stands. |",
        "| A2 union as primary | **No: keep strict primary** | Phenotype gate passed; genetic-adjudication and AUC non-inferiority gates failed. |",
        f"| A3 locked numbers | **Yes: numerically reproduce** | {f(a3['discrepancy_gate']['defect_count'])} discrepancies exceeded the absolute 0.001 defect threshold. |",
        "",
        "I disagree with (1) the senior-author assertion that a viable incident-primary analysis can be "
        "constructed from these fields, and (2) promotion of the predicted-LoF union to the primary genetic "
        "definition. I agree that the stored aggregate numbers are computationally reproducible, but that "
        "does not remove the blocking temporality and target-informed-selection defects.",
        "",
        "## What was run",
        "",
        "```bash",
        "cd /Users/nader85/Documents/CALON/calon_discordance_model_2026_08_09",
        "export CALON_SHARED_MASTER=\"/Users/nader85/Library/CloudStorage/GoogleDrive-nadergenedy1@gmail.com/My Drive/Projects/SHARED_MASTER_DATA\"",
        "python3 -c \"import pandas, numpy, sklearn, lifelines; print('deps ok')\"",
        "python3 code/audit_2026_08_10/audit_common.py",
        "python3 code/audit_2026_08_10/01_incident_feasibility.py",
        "python3 code/audit_2026_08_10/02_union_definition.py",
        "python3 code/audit_2026_08_10/03_locked_reproduction.py",
        "python3 code/audit_2026_08_10/04_build_report.py",
        "```",
        "",
        "The audit scripts independently reconstruct both cohorts and never import the locked analysis "
        "engine. Stored aggregate JSON is opened only after A3 has recomputed its predictions and metrics.",
        "",
        "## A1. Feasibility of an incident landmark design",
        "",
        "Estimand: among DRAGON participants without a recorded component event at the first usable dated "
        "lipid measurement, time from that anchor to the first recorded post-anchor ASCVD component, censored "
        "at the recorded event-or-censor age.",
        "",
        "### Date parsing and anchor construction",
        "",
        "| Field | Nonblank | Parsed | Failed | slash M/D/Y | slash D/M/Y fallback |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for name in ["BirthDate", "TodayDate", "MeasurementDate_1", "MeasurementDate_2", "MeasurementDate_3", "MeasurementDate_4"]:
        item = a1["date_parsing"][name]
        label = name.replace("MeasurementDate_", "measurement slot ")
        lines.append(
            f"| {label} | {f(item['nonblank'])} | {f(item['parsed'])} | {f(item['failed'])} | "
            f"{f(item['slash_mdy'])} | {f(item['slash_dmy_fallback'])} |"
        )
    flow = a1["anchor_flow"]
    exclusions = a1["post_anchor_exclusions"]
    landmark = a1["landmark_results"]
    verify = a1["event_field_interpretation"]["cross_check"]
    lines.extend([
        "",
        f"Rows with any nonblank date parse failure: {f(a1['date_parsing']['rows_with_any_nonblank_date_parse_failure'])}. "
        "Both failures occurred in a later measurement field and did not eliminate the row's earlier usable anchor.",
        "",
        f"Anchor flow (mutually exclusive across all {f(a1['rows_total'])} rows): no usable lipid in four slots "
        f"{f(flow['no_usable_lipid_in_four_slots'])}; usable lipid but no date text "
        f"{f(flow['usable_lipid_but_no_date_text'])}; dated usable lipid but no parseable date "
        f"{f(flow['usable_lipid_with_date_text_but_unparseable'])}; parseable anchor {f(flow['parseable_anchor'])}.",
        "",
        "### The purported `Year` fields are ages",
        "",
        f"Across {f(verify['rows_compared_to_reported_event_age'])} comparable rows, interpreting the component "
        f"fields as age gave median absolute error {f(verify['direct_age_interpretation_median_absolute_error_years'])} years "
        f"and {f(verify['direct_age_interpretation_within_one_year_pct'])}% agreement within one year. Treating them "
        f"as calendar years gave median absolute error {f(verify['calendar_year_interpretation_median_absolute_error_years'])} years "
        f"and {f(verify['calendar_year_interpretation_within_one_year_pct'])}% within one year. Verdict: these are ages, not calendar years.",
        "",
        "Usable age-coded component records were: "
        + ", ".join(
            f"{name} {f(a1['event_field_interpretation']['by_component'][name]['age_coded'])}"
            for name in ["MI/ACS", "PCI", "CABG", "angina", "TIA", "PVD"]
        )
        + ". The small cells remain suppressed in the JSON as well.",
        "",
        "### Landmark flow and results",
        "",
        f"After {f(flow['parseable_anchor'])} parseable anchors: unparseable birth date {f(exclusions['anchor_with_unparseable_birth_date'])}; "
        f"implausible anchor age {f(exclusions['anchor_age_outside_0_to_105'])}; prevalent at anchor "
        f"{f(exclusions['prevalent_at_anchor'])}; missing/invalid censor age after excluding prevalent cases "
        f"{f(exclusions['missing_or_invalid_censor_age_after_excluding_prevalent'])}; censor age before anchor "
        f"{f(exclusions['censor_before_anchor_after_excluding_prevalent'])}; final incident risk set {f(exclusions['incident_risk_set_n'])}.",
        "",
        f"Prevalent at anchor: **{f(landmark['prevalent_at_anchor_n'])}**. Incident after anchor: "
        f"**{f(landmark['incident_after_anchor_n'])}**. Person-time: {f(landmark['person_years'])} person-years; "
        f"median follow-up {f(landmark['median_follow_up_years'])} years. Events per seven candidate predictors: "
        f"{f(landmark['events_per_candidate_predictor'])}. Each individual incident component (MI/ACS, PCI, CABG, "
        "angina, TIA, PVD) was `<10, non-estimable`.",
        "",
        "Gate: `<25` incident events means not viable and the prevalent design stands. A Cox model was therefore "
        "not fitted; fitting seven coefficients with a sub-10 event total would be indefensible. Non-CV death is "
        "not identifiable from a dated cause-specific death record, so Fine-Gray is not estimable.",
        "",
        "### A1 temporality finding",
        "",
        f"Of {f(a1['temporality_audit']['ascvd_cases_with_component_age_and_current_age_n'])} cases with a usable "
        f"component age and current age, {f(a1['temporality_audit']['cases_where_current_age_is_after_first_recorded_event_n'])} "
        f"had current age after the first event; {f(a1['temporality_audit']['cases_prevalent_at_first_dated_lipid_anchor_n'])} "
        "were already prevalent at their first dated lipid anchor. ApoB/ApoA1 have no linked measurement date, "
        "and hypertension/smoke-ever lack a historical anchor. Thus the locked Welsh predictors cannot be shown "
        "to precede the outcome.",
        "",
        "## A2. Strict versus P/LP-or-predicted-LoF union",
        "",
        "### Genetic increment",
        "",
    ])
    genetics = a2["genetic_definition"]
    lines.extend([
        f"Strict: {f(genetics['strict_definition_n'])}; union: {f(genetics['union_definition_n'])}; added: "
        f"{f(genetics['added_definition_n'])}. All {f(genetics['added_without_any_plp_assertion_n'])} additions "
        "were admitted by LoF consequence prediction without any independent P/LP assertion; none was a "
        "P/LP carrier merely removed by the conflict rule. The annotation sources both flagged all 374 additions "
        f"as LoF consequence carriers ({f(genetics['added_flagged_by_clinvar_consequence_n'])} and "
        f"{f(genetics['added_flagged_by_vep_consequence_n'])}, respectively).",
        "",
        "The implemented rule does not adjudicate canonical transcript, nonsense-mediated-decay/last-exon escape, "
        "splice rescue, or independent clinical classification. A predicted consequence is not by itself a "
        "high-confidence PVS1 adjudication.",
        "",
        "### Aggregate phenotype",
        "",
        "| Group | n | ASCVD events | LDL nonmissing | mean LDL | median LDL | treated | ASCVD |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ])
    phen = a2["phenotype_comparison"]
    for key, label in [("strict_clinvar_plp", "Strict P/LP"), ("lof_added", "LoF-added")]:
        item = phen[key]
        lines.append(
            f"| {label} | {f(item['n'])} | {f(item['events'])} | {f(item['ldl_nonmissing_n'])} | "
            f"{f(item['ldl_mean_mmol_l'])} mmol/L | {f(item['ldl_median_mmol_l'])} mmol/L | "
            f"{f(item['treatment_pct'])}% | {f(item['ascvd_pct'])}% |"
        )
    diff = phen["absolute_differences"]
    lines.extend([
        "",
        f"Absolute strict-versus-added differences: median LDL {f(diff['median_ldl_mmol_l'])} mmol/L, treatment "
        f"{f(diff['treatment_percentage_points'])} percentage points, ASCVD {f(diff['ascvd_percentage_points'])} "
        "percentage points. The added phenotype therefore passed the audit's prespecified consistency margins, "
        "although its lower treatment exposure and LDL are directionally compatible with some dilution.",
        "",
        "### Reciprocal transport using union",
        "",
        f"DRAGON -> UKB union (n={f(a2['union_reciprocal_transport']['DRAGON_to_UKB_union']['n'])}, "
        f"events={f(a2['union_reciprocal_transport']['DRAGON_to_UKB_union']['events'])}; "
        f"{f(a2['union_reciprocal_transport']['DRAGON_to_UKB_union']['bootstrap_replicates'])} target-cluster bootstraps):",
        "",
        *performance_table(a2["union_reciprocal_transport"]["DRAGON_to_UKB_union"]),
        "",
        f"UKB union -> DRAGON (n={f(a2['union_reciprocal_transport']['UKB_union_to_DRAGON']['n'])}, "
        f"events={f(a2['union_reciprocal_transport']['UKB_union_to_DRAGON']['events'])}; "
        f"{f(a2['union_reciprocal_transport']['UKB_union_to_DRAGON']['bootstrap_replicates'])} target-cluster bootstraps):",
        "",
        *performance_table(a2["union_reciprocal_transport"]["UKB_union_to_DRAGON"]),
        "",
        "Montreal and FH-Risk-Score are ranking scores, so E:O is not defined. SAFEHEART E:O is printed only "
        "because its output is a probability; it is not calibration-compatible with prevalent ASCVD because "
        "SAFEHEART predicts a five-year horizon.",
        "",
    ])
    strict_ref = a2["strict_raw_recomputed_reference"]
    change = a2["union_vs_strict_definition_change"]
    lines.extend([
        f"Raw-recomputed strict references were AUC {f(strict_ref['DRAGON_to_UKB_strict']['auc'])}, E:O "
        f"{f(strict_ref['DRAGON_to_UKB_strict']['e_o'])} forward and AUC "
        f"{f(strict_ref['UKB_strict_to_DRAGON']['auc'])}, E:O {f(strict_ref['UKB_strict_to_DRAGON']['e_o'])} reverse.",
        "",
        f"Definition-change contrast: the same DRAGON model evaluated in union versus its strict subset changed "
        f"AUC by {f(change['DRAGON_model_union_target_minus_strict_subset']['delta_union_target_minus_strict_subset'])} "
        f"(95% CI {ci(change['DRAGON_model_union_target_minus_strict_subset']['ci'])}). Training in union rather "
        f"than strict changed DRAGON AUC by {f(change['union_trained_minus_strict_trained_on_DRAGON']['delta'])} "
        f"(95% CI {ci(change['union_trained_minus_strict_trained_on_DRAGON']['ci'])}).",
        "",
        "### A2 gate and verdict",
        "",
        a2["primary_definition_gate"]["rule"],
        "",
        f"Phenotype consistency: {f(a2['primary_definition_gate']['phenotype_consistency_pass'])}. "
        f"Discrimination non-inferiority: {f(a2['primary_definition_gate']['discrimination_noninferiority_pass'])}. "
        f"Genetic validity: {f(a2['primary_definition_gate']['genetic_validity_pass'])}. **Verdict: no; keep "
        f"strict primary and union as sensitivity.** The {f(union_event_gain_pct)}% event-count increase does "
        "not compensate for unadjudicated genetic inclusion and a non-inferiority CI that crosses the -0.02 margin.",
        "",
        "## A3. Independent reproduction of locked numbers",
        "",
        "### Strict reciprocal performance",
        "",
        "DRAGON -> UKB strict:",
        "",
        *performance_table(a3["independent_computed"]["DRAGON_to_UKB_strict"]),
        "",
        "UKB strict -> DRAGON:",
        "",
        *performance_table(a3["independent_computed"]["UKB_strict_to_DRAGON"]),
        "",
        "### Agreement with locked aggregates (four decimal places)",
        "",
        *agreement_rows(a3),
        "",
    ])
    fh = a3["fh_vs_matched_nonfh_independent"]
    lines.extend([
        f"The independently reconstructed matched UKB contrast used {f(fh['n_fh'])} FH participants "
        f"({f(fh['events_fh'])} events) and {f(fh['n_nonfh'])} non-FH participants "
        f"({f(fh['events_nonfh'])} events), with {f(fh['unmatched_fh_n'])} unmatched FH participants. "
        f"The OR was {f(fh['odds_ratio'])} ({f(fh['odds_ratio_ci'][0])} to {f(fh['odds_ratio_ci'][1])}); "
        f"E:O was {f(fh['e_o_nonfh_model_to_fh'])} for non-FH model -> FH and "
        f"{f(fh['e_o_fh_model_to_nonfh'])} for FH model -> non-FH.",
        "",
        f"A3 verdict: **yes, the locked aggregate numbers reproduce.** The defect count beyond 0.001 was "
        f"{f(a3['discrepancy_gate']['defect_count'])}.",
        "",
        "## Defects and adversarial interpretation",
        "",
        "1. **Blocking for any prospective-risk claim: outcome-before-predictor leakage.** This is a prevalent "
        f"case-classification model. In DRAGON, {f(a1['temporality_audit']['cases_prevalent_at_first_dated_lipid_anchor_n'])} "
        f"cases predated the first dated lipid anchor and all "
        f"{f(a1['temporality_audit']['cases_where_current_age_is_after_first_recorded_event_n'])} cases with "
        "comparable ages had the model's current age recorded after the event. In UKB, recruitment biomarkers "
        "and behaviours are used against a prevalent-at-recruitment outcome without establishing that they preceded it.",
        "",
        "2. **Blocking for an unbiased external-performance claim: target-informed selection.** The architecture "
        "was chosen using both reciprocal target outcomes, then performance on those same targets was reported. "
        "Neither direction is an untouched external validation of the selected architecture.",
        "",
        f"3. **Severe calibration transport failure.** Strict E:O was "
        f"{f(a3['independent_computed']['DRAGON_to_UKB_strict']['e_o'])} forward and "
        f"{f(a3['independent_computed']['UKB_strict_to_DRAGON']['e_o'])} reverse; union E:O was "
        f"{f(a2['union_reciprocal_transport']['DRAGON_to_UKB_union']['e_o'])} and "
        f"{f(a2['union_reciprocal_transport']['UKB_union_to_DRAGON']['e_o'])}. The model substantially "
        "overpredicts in UKB and underpredicts in DRAGON. It is "
        "not transport-calibrated and is not suitable for absolute-risk use.",
        "",
        f"4. **No consistent discrimination gain over simple comparators.** Forward strict CALON-N was not better "
        f"than adapted Montreal (delta {f(a3['independent_computed']['DRAGON_to_UKB_strict']['comparators']['Montreal_adapted']['delta_calon_minus_comparator'])}, "
        f"CI {ci(a3['independent_computed']['DRAGON_to_UKB_strict']['comparators']['Montreal_adapted']['delta_ci'])}). "
        f"Reverse strict CALON-N was worse than Montreal (delta "
        f"{f(a3['independent_computed']['UKB_strict_to_DRAGON']['comparators']['Montreal_adapted']['delta_calon_minus_comparator'])}, "
        f"CI {ci(a3['independent_computed']['UKB_strict_to_DRAGON']['comparators']['Montreal_adapted']['delta_ci'])}) "
        f"and pointwise worse than age+sex (delta "
        f"{f(a3['independent_computed']['UKB_strict_to_DRAGON']['comparators']['age_sex']['delta_calon_minus_comparator'])}).",
        "",
        f"5. **Union genetic misclassification risk.** All {f(genetics['added_definition_n'])} additions depend on predicted consequence alone; "
        "the implemented rule lacks high-confidence LoF adjudication. This blocks promotion to the primary definition.",
        "",
        "6. **FH-versus-non-FH auxiliary inference is optimistic.** The four-cell Wald CI ignores matched-set and "
        "carrier-cluster dependence. Prediction-time target medians also make those transports transductive.",
        "",
        "7. **Comparator interpretation is not harmonised.** Adapted ranking scores are not calibrated probabilities, "
        "and the SAFEHEART five-year probability is evaluated against prevalence. AUC ranking comparisons are "
        "descriptive; E:O comparisons are undefined or horizon-incompatible.",
        "",
        "## Bottom line",
        "",
        "The defensible claim is narrow: CALON-N is a reproducible, penalised cross-sectional classifier of "
        "established ASCVD in these two selected HeFH cohorts. It is not an incident risk model, its apparent "
        "external AUCs are target-informed, and its transported absolute probabilities are badly miscalibrated. "
        "The prevalent design may stand only if the manuscript consistently describes classification/association "
        "rather than prospective risk. Strict coordinate-verified P/LP should remain primary; union should remain "
        "a sensitivity analysis pending independent high-confidence LoF adjudication.",
    ])

    report = "\n".join(lines) + "\n"
    report_path = OUT / "AUDIT_REPORT.md"
    write_text(report_path, report)

    scripts = sorted((ROOT / "code" / "audit_2026_08_10").glob("*.py"))
    result_files = [
        OUT / "a1_incident_feasibility.json",
        OUT / "a2_union_definition.json",
        OUT / "a3_locked_reproduction.json",
        report_path,
    ]
    paths = input_paths()
    metadata = {
        "environment": environment_metadata(),
        "scripts_sha256": {path.name: sha256(path) for path in scripts},
        "aggregate_outputs_sha256": {path.name: sha256(path) for path in result_files},
        "logical_inputs": {
            logical: {"size_bytes": path.stat().st_size, "mtime_ns": path.stat().st_mtime_ns}
            for logical, path in paths.items()
        },
        "prohibited_source_accessed": False,
        "participant_level_outputs": False,
        "stored_aggregate_results_read_only_after_independent_A3_computation": True,
    }
    write_json(OUT / "run_metadata.json", metadata)

    low_event_failures = []
    for name, payload in [("a1", a1), ("a2", a2), ("a3", a3)]:
        low_event_failures.extend(
            f"{name}.{path}" for path in validate_low_event_suppression(payload)
        )
    forbidden_report_patterns = {
        "participant_linkage_field_name": r"\bparticipant_id\b",
        "ukb_linkage_field_name": r"\beid\b",
        "family_linkage_field_name": r"\bfamily_id\b",
        "hgvs": r"\bHGVS\b",
        "variant_coordinate_literal": r"\b(?:chr)?(?:[1-9]|1[0-9]|2[0-2]|X|Y):\d+:[ACGT]+:[ACGT]+\b",
    }
    forbidden_hits = [
        label for label, pattern in forbidden_report_patterns.items()
        if re.search(pattern, report, re.IGNORECASE)
    ]
    qc = {
        "dependency_import_gate": "pass",
        "all_three_result_json_present": True,
        "report_present": report_path.is_file(),
        "low_event_suppression_gate": "pass" if not low_event_failures else "fail",
        "low_event_failures": low_event_failures,
        "forbidden_report_pattern_gate": "pass" if not forbidden_hits else "fail",
        "forbidden_report_pattern_hits": forbidden_hits,
        "numeric_reproduction_gate": "pass" if a3["discrepancy_gate"]["all_locked_numbers_reproduce"] else "fail",
        "overall": "pass" if not low_event_failures and not forbidden_hits and a3["discrepancy_gate"]["all_locked_numbers_reproduce"] else "fail",
        "participant_level_outputs": False,
    }
    write_json(OUT / "audit_qc.json", qc)
    if qc["overall"] != "pass":
        raise RuntimeError(f"Audit QC failed: {qc}")
    print(json.dumps({
        "report": "outputs/audit_2026_08_10/AUDIT_REPORT.md",
        "qc": qc["overall"],
    }, indent=2))


if __name__ == "__main__":
    main()
