#!/usr/bin/env python3
"""Build the prioritised CALON-N forward plan from aggregate delta checks."""
from __future__ import annotations

import json
import re

from audit_common import OUT, write_json, write_text


def f(value: float, digits: int = 1) -> str:
    return f"{float(value):.{digits}f}"


def main() -> None:
    delta = json.loads((OUT / "timeline_delta_verification.json").read_text(encoding="utf-8"))
    fact1 = delta["fact_1_censor_is_genetic_test_age"]
    fact2 = delta["fact_2_event_capture_stops_at_test"]
    fact3 = delta["fact_3_clinic_contact_after_outcome_freeze"]
    fact4 = delta["fact_4_censor_before_first_measurement"]
    fact5 = delta["fact_5_revised_short_window"]
    fact7 = delta["fact_7_dated_ldl_density"]
    refresh = delta["refresh_arithmetic"]

    lines = [
        "# CALON-N prioritised forward plan",
        "",
        "Date: 2026-08-10. This is a forward analysis and manuscript plan, not a manuscript rewrite. "
        "All supporting checks are aggregate-only. The prohibited identifiable treatment-response source was "
        "not accessed, and no row-level data, linkage values, variant-level descriptions, or individual predictions "
        "are written here.",
        "",
        "## Executive decision",
        "",
        "Do not run another model-selection cycle now. First freeze the present CALON-N equation and claims, "
        "request refreshed linked outcomes, and lock genetic/comparator definitions. The current paper can support "
        "only a cross-sectional established-ASCVD classification/transportability claim. A prospective incident-risk "
        "paper becomes plausible only if refreshed linkage produces enough first incident events after a genuinely "
        "pre-outcome baseline.",
        "",
        "Current decisions:",
        "",
        "- Current DRAGON incidence analysis: stop; retain only as a timeline-QC demonstration.",
        "- UKB primary genetic definition: retain strict coordinate-verified LDLR P/LP; union remains sensitivity.",
        "- New multi-gene work: rebuild with gene-specific mechanisms; never apply a generic consequence-based "
        "P/LP-or-LoF rule to LDLR, APOB, and PCSK9 alike.",
        "- Carrier comparison: age/sex/smoking matching is primary; LDL-conditioned matching is secondary and must "
        "be labelled a residual association, not a direct genetic effect.",
        "- Treatment response: drop apoB-versus-LDL response with the current data; serial apoB is absent.",
        "",
        "## Cheap verification of the seven new timeline facts",
        "",
        "| Fact | Verification | Planning consequence |",
        "|---|---|---|",
        f"| 1. Censor age is test age | Verified: {fact1['exact_matches']}/{delta['rows_total']} exact matches "
        f"({f(fact1['exact_match_pct_of_all_rows'])}%). | Treat the recorded censor as genetic-test freeze, not last contact. |",
        f"| 2. No event beyond censor | Qualified: the exact composite-event cell remains `<10, non-estimable` and "
        f"does not contradict the assertion, but {fact2['any_component_age_beyond_censor_n']} rows have at least one later "
        "component age. | The composite field is frozen; the stronger claim that every component field is frozen is false. |",
        f"| 3. Later clinic contact | Verified: {fact3['blood_test_date_parsed']} parseable blood-test dates in "
        f"2018–2025; latest {fact3['latest_blood_test_date']}; all {fact3['today_date_in_2024_n']} TodayDate values are in 2024. | "
        "Refresh outcomes independently of clinic-contact fields and define a single administrative end date. |",
        f"| 4. Censor before first measurement | Verified: {fact4['censor_before_first_measurement_n']} of "
        f"{fact4['first_measurement_anchor_and_censor_comparable_n']} comparable rows. | The earlier 77 was conditional "
        "on prior exclusions and a different anchor; 109 is the unconditional first-measurement count. |",
        f"| 5. Revised short window | Verified: {fact5['nonnegative_follow_up_n']} with nonnegative follow-up, "
        f"{fact5['incident_first_events_n']} incidents, {f(fact5['person_years'])} person-years, median "
        f"{f(fact5['median_follow_up_years'])} years (IQR {f(fact5['follow_up_iqr_years'][0])}–"
        f"{f(fact5['follow_up_iqr_years'][1])}), EPV {f(fact5['events_per_7_predictors'])}. Prevalent-at-anchor "
        "cell remains `<10, non-estimable`. | This is an FH-work-up/detection window, not natural-history incidence. |",
        "| 6. Contact-dependent rates | Not independently verified. The recent-contact marker and risk-time denominator "
        "were not supplied; plausible reconstructions create sub-10 event cells that must be suppressed. | Do not quote "
        "4.8 versus 2.2 until the exact aggregate code and denominator are supplied; retain informative capture as a "
        "design concern. |",
        f"| 7. Dated LDL density | Verified: {fact7['dated_ldl_observations']} dated LDL observations; "
        f"{fact7['participants_with_at_least_2']} people with at least two, {fact7['participants_with_at_least_3']} "
        f"with at least three, and {fact7['participants_with_at_least_4']} with four. | Enough for a cautious LDL-trajectory "
        "description, but only 240 people inform within-person change. |",
        "",
        "### Sanity-check of the linkage-refresh forecast",
        "",
        f"The observed short-window rate is {f(fact5['incidence_rate_per_1000_py'])} per 1,000 person-years "
        f"(exact Poisson 95% CI {f(fact5['poisson_rate_95_ci_per_1000_py'][0])}–"
        f"{f(fact5['poisson_rate_95_ci_per_1000_py'][1])}). The simple assumption "
        f"{refresh['simple_assumption_people']} people × {f(refresh['simple_assumption_years_each'], 0)} years gives "
        f"{f(refresh['simple_person_years'], 0)} person-years and {f(refresh['simple_projected_events_at_observed_rate'])} "
        f"expected events. A data-derived upper feasibility calculation—valid first-measurement anchors through the "
        f"export date, excluding {refresh['data_derived_prevalent_at_anchor_n']} prevalent cases—gives "
        f"{refresh['data_derived_potential_risk_set_n']} at risk, {f(refresh['data_derived_potential_person_years'], 0)} "
        f"person-years, and {f(refresh['data_derived_projected_events_at_observed_rate'])} expected events.",
        "",
        f"My point estimate is therefore approximately **48–70 incident events**, so the arithmetic is sound. It is "
        f"not a promise that the ≥40 gate will clear: propagating only the Poisson rate interval gives "
        f"{f(refresh['simple_projected_events_using_rate_ci'][0])}–{f(refresh['simple_projected_events_using_rate_ci'][1])} "
        f"events under the 10-year simplification and {f(refresh['data_derived_projected_events_using_rate_ci'][0])}–"
        f"{f(refresh['data_derived_projected_events_using_rate_ci'][1])} under the data-derived person-time. The source "
        "rate is based on 17 events in a 0.9-year work-up window, may be contact-dependent, assumes constant hazard, "
        "and ignores competing death. The refresh request is justified; feasibility must be decided from observed "
        "linked endpoints, not this extrapolation.",
        "",
        "## 1. Order of work",
        "",
        "1. **Immediately freeze CALON-N and reset claims (W1/W7/W8).** This prevents another target-informed cycle "
        "and lets any newly linked events serve as honest temporal validation of a locked score.",
        "2. **Submit the outcome-refresh specification first (W1).** Link hospital episodes, procedures, death and "
        "administrative follow-up through one declared date; this is the only route to a defensible incident estimand.",
        "3. **Build the comparator provenance matrix before rerunning comparators (W7).** Exact coefficients, original "
        "predictors, treatment status, outcome and horizon must determine whether a result is validation, updating or "
        "variable-set benchmarking.",
        "4. **Freeze the primary genetic definition, then commission the gene-specific rebuild (W2/W3).** Cohort "
        "membership must be locked before carrier comparisons, interaction work or endpoint counting.",
        "5. **Run the refreshed-event feasibility gate (W1).** Count first incident events and competing deaths before "
        "fitting any survival model; the count determines whether evaluation, updating or no model is allowed.",
        "6. **Run carrier versus non-carrier analyses (W4).** This is answerable now, but only after the genetic set, "
        "matching estimand and prevalence weighting are fixed.",
        "7. **Construct longitudinal LDL burden only after predictor timing is aligned (W5).** The 753 measurements are "
        "useful only if pre-outcome status, treatment exposure and observation density are modelled explicitly.",
        "8. **Run discordance interactions and the grey-zone challenger last among analyses (W5).** They are exploratory, "
        "multiplicity-sensitive and cannot rescue a failed primary model.",
        "9. **Limit W6 to LDL trajectory; do not run apoB treatment-response claims.** A single undated apoB cannot "
        "estimate differential longitudinal response.",
        "10. **Complete final manuscript surgery after all gates (W8).** Outcome table, methods, limitations and claim "
        "language must be generated from the frozen analysis ledger, not drafted around favourable results.",
        "",
        "## 2. Disposition of every senior-author comment",
        "",
        "The table assigns every numbered label, including 18b.",
        "",
        "| Comment | Status | Explicit answer/action |",
        "|---|---|---|",
        "| 1. Treatment response apoB vs LDL-C | **Not answerable with these data** | Serial dated apoB paired to serial LDL and treatment changes is absent. Drop the response claim. |",
        "| 2. Statin alone insufficient because LDL falls more than apoB | **Not answerable with these data** | Requires paired pre/post apoB and LDL under known statin intensity, adherence and add-on therapy. Cross-sectional ratios cannot answer it. |",
        "| 3. Comparators differ | **Answerable now** | Produce the frozen-coefficient versus variable-set-refit provenance table; state untreated LDL/Lp(a), no-LDL, prior-ASCVD and horizon differences explicitly. |",
        "| 4. Superiority overstated | **Answerable now** | Replace superiority with paired estimates and CIs. Current data show no consistent advantage over Montreal or age+sex. |",
        "| 5. Drop add-to-Montreal versus de novo framing | **Answerable now** | Remove the framing; describe CALON-N as one prespecified seven-variable cross-sectional architecture. |",
        "| 6. External-validation definition too strict | **Answerable now** | Clarify terminology: a frozen model can be externally validated; target refitting is model updating; variable-set refitting is benchmarking. The selected CALON-N targets were used in selection, so they are not untouched external validation. |",
        "| 7. Too much file-date detail | **Answerable now** | Move filenames/dates/checksums to the supplement or reproducibility note; retain only cohort version and administrative end date in Methods. |",
        "| 8. Explain SHA-256 | **Answerable now** | Define it once as a digital fingerprint proving file/code identity; it does not prove data validity or confidentiality. |",
        "| 9. Methods below cardio-lipid standard | **Answerable now** | Rewrite to TRIPOD+AI/RECORD level: setting, eligibility, timing, outcome, missingness, clustering, shrinkage, selection, calibration, comparator equations and deviations. |",
        "| 10. Extend validation of prior models | **Answerable now** | Run exact frozen models only where inputs/outcome/horizon match; otherwise report a separate refit benchmark. Do not merge the two lanes. |",
        "| 11. CALON-N and comparators in carriers vs non-carriers | **Answerable now** | Use the current UKB master with prespecified matching/weighting, but label results cross-sectional and transport descriptive. |",
        "| 12. Verify all claims against sources | **Answerable now** | Build a claim-to-source ledger; every comparator coefficient, outcome definition and biological statement must have a primary source or be removed. |",
        "| 13. Purpose-built LDLR/APOB/PCSK9 set | **Answerable only after a genetic data refresh/rebuild** | Do not reuse TUDOR. Apply gene-specific pathogenic mechanisms and independent adjudication. |",
        "| 14. Outcome prose to table | **Answerable now** | Create one aggregate component/provenance/timing table with low-event suppression. |",
        "| 15. Incidence vs prevalence using event and first-LDL dates | **Answerable only after outcome refresh** | Current 17-event work-up window is detection-biased. Use linked first events and a pre-outcome landmark. |",
        "| 16. Discordance only in selected scenarios | **Answerable now, exploratory only** | Test prespecified continuous interactions for diabetes and TG/HDL with FDR control. High-apoB stratification is partly tautological because apoB defines the ratio. |",
        "| 17. Grey-zone model with Lp(a) and TG/HDL | **Answerable now, exploratory only** | Evaluate as a locked challenger with source-only tuning and nested grouped validation; it cannot replace CALON-N without new validation. |",
        "| 18. Meaning of adapted; add prior ASCVD to SAFEHEART | **Answerable now** | Ban ambiguous “adapted”: say frozen or refit. Do not add prior ASCVD when predicting prevalent ASCVD—it is circular. Revisit only for future incident/recurrent outcomes. |",
        "| 18b. Near-complete matching, LDL/smoking, sensitivity and predictive values | **Answerable now with restrictions** | Primary matching: age/sex/smoking. LDL is secondary. Sensitivity/specificity require a frozen threshold; PPV/NPV require full-cohort prevalence or valid reweighting, not the matched sample prevalence. |",
        "| 19. Use union 1,264 instead of strict 890 | **Answerable now** | No. Keep strict primary; union sensitivity. |",
        "| 20. Include P/LP or LoF and validate against their definition | **Answerable only after genetic refresh/adjudication** | For LDLR, high-confidence LoF may qualify. APOB requires variant-specific LDL-receptor-binding impairment; PCSK9 FH requires gain of function. Generic consequence-based LoF inclusion is wrong. |",
        "| 21. Rank cumulative LDL vs gene vs Lp(a) | **Answerable only after outcome and genetic refresh** | Current data can support a descriptive pilot, not a causal ranking. Use refreshed incident outcomes, pre-outcome burden and correlated-predictor decomposition. |",
        "",
        "## 3. Analyses retained: estimands, methods and pre-stated gates",
        "",
        "### A. Refreshed incident CALON-N evaluation",
        "",
        "**Estimand:** Among genetically defined FH participants free of ASCVD at a pre-outcome lipid landmark, "
        "estimate risk of first incident ASCVD through a fixed linked-data end date.",
        "",
        "**Method:** Rebuild first hospital/procedure events from linked records; set time zero at the earliest usable "
        "pre-outcome predictor panel; use cause-specific Cox with cluster-robust inference, cumulative incidence and "
        "Fine-Gray only if non-CV death is identifiable; evaluate the already frozen CALON-N linear predictor with "
        "C-index/time-dependent AUC, calibration, Brier score and decision curves.",
        "",
        "**Gate:** `<40` observed first incidents: no incident primary. `40–69`: evaluate/recalibrate the frozen score "
        "only—no coefficient reselection. `>=70`: a seven-term penalised refit is allowed with bootstrap optimism "
        "correction. In every case, require at least 90% of predictors demonstrably pre-outcome, at least 95% endpoint "
        "linkage completeness, a declared competing-death strategy and median follow-up at least five years.",
        "",
        "### B. Primary genetic-definition adjudication",
        "",
        "**Estimand:** Determine whether broadening strict LDLR P/LP to independently adjudicated high-confidence "
        "LDLR P/LP-or-LoF materially changes phenotype and CALON-N transport.",
        "",
        "**Method:** ClinGen/PVS1-style transcript, NMD/last-exon and splice-rescue adjudication; repeat nested cohort "
        "AUC contrasts and calibration after locking variants without viewing outcomes.",
        "",
        "**Gate:** Promote union only if at least 95% of LoF-only additions pass independent high-confidence review, "
        "phenotype remains within the audit margins (median LDL 0.5 mmol/L, treatment 15 percentage points, ASCVD "
        "3 percentage points), and both reciprocal union-minus-strict AUC lower 95% bounds exceed -0.02. Until then, "
        "strict remains primary.",
        "",
        "### C. Purpose-built LDLR/APOB/PCSK9 carrier set",
        "",
        "**Estimand:** Describe established or incident ASCVD by independently defined FH-causing gene mechanism, "
        "without treating all predicted LoF consequences as equivalent.",
        "",
        "**Method:** LDLR high-confidence loss-of-function/P/LP; APOB established LDL-receptor-binding-defective "
        "variants with variant-specific evidence rather than automatic inclusion of generic truncating consequences; "
        "PCSK9 gain-of-function variants, explicitly excluding PCSK9 loss of function. Deduplicate carriers, freeze "
        "transcript rules and produce a blind adjudication ledger before outcome linkage. These mechanism distinctions "
        "are supported by the current [GeneReviews FH chapter](https://www.ncbi.nlm.nih.gov/books/NBK174884/).",
        "",
        "**Gate:** At least 95% independently reviewable calls, at least 95% concordance with the locked external "
        "definition, and at least 10 outcome events per reported gene stratum; otherwise report `<10, non-estimable` "
        "and do not pool mechanisms to manufacture power.",
        "",
        "### D. Carrier versus non-carrier total association",
        "",
        "**Estimand:** Compare prevalent ASCVD odds in carriers versus non-carriers at the same age, sex and smoking "
        "profile, allowing LDL-mediated pathways to remain part of the total association.",
        "",
        "**Method:** Exact/coarsened matching or overlap weighting on age, sex and smoking, with prespecified support "
        "rules; cluster-robust or matched-set inference; report OR, risk difference and absolute prevalence. Smoking "
        "must be clearly timed, because post-diagnosis smoking is not a clean baseline covariate.",
        "",
        "**Gate:** All matched-covariate absolute standardised differences below 0.10, adequate overlap, at least 20 "
        "events per arm, and concordant estimates from matching and overlap weighting. If these fail, no carrier-effect claim.",
        "",
        "### E. LDL-conditioned carrier secondary",
        "",
        "**Estimand:** Estimate the residual carrier–ASCVD association among people with overlapping measured LDL, "
        "conditional on age, sex and smoking; this is not the natural direct genetic effect.",
        "",
        "**Method:** Secondary LDL matching/weighting with a common-support plot, measured-LDL timing restriction and "
        "sensitivity to untreated versus treated LDL definitions.",
        "",
        "**Gate:** LDL and primary covariate standardised differences below 0.10, no severe loss of carrier support, "
        "and at least 20 events per arm. Regardless of significance, label the result “LDL-conditioned residual "
        "association”; never “genotype effect not mediated by LDL-C” without a formal mediation design.",
        "",
        "### F. Classification metrics in carriers and non-carriers",
        "",
        "**Estimand:** At frozen thresholds, quantify how CALON-N and eligible comparators classify established ASCVD "
        "within carriers and non-carriers.",
        "",
        "**Method:** Report AUC, sensitivity, specificity and likelihood ratios with cluster bootstrap CIs. Estimate "
        "PPV/NPV only in the full population sample or after explicit prevalence reweighting; include calibration and "
        "decision curves only for actual probabilities on the same outcome horizon.",
        "",
        "**Gate:** Every reported outcome cell has at least 10 events, the threshold is frozen before evaluation, and "
        "a superiority claim requires paired delta-AUC lower 95% CI above zero plus positive net benefit at prespecified "
        "thresholds. Otherwise results are descriptive.",
        "",
        "### G. Comparator provenance and benchmarking",
        "",
        "**Estimand:** Compare CALON-N with (i) exact frozen prior-model predictions and separately (ii) refitted "
        "variable-set benchmarks for the same cross-sectional outcome.",
        "",
        "**Method:** One provenance row per score: source, equation, coefficients, treatment status, required inputs, "
        "original population, endpoint, horizon, handling of prior ASCVD, modifications and missingness. Do not compute "
        "E:O for ranking scores or horizon-mismatched probabilities.",
        "",
        "**Gate:** 100% provenance completeness. Call a result external validation only for a frozen model with "
        "compatible inputs/endpoints. Call superiority only if paired delta-AUC lower 95% CI exceeds zero in both "
        "directions and calibration slope is 0.8–1.2 with E:O 0.8–1.25; the present CALON-N fails this gate.",
        "",
        "### H. Cumulative LDL burden, gene and Lp(a)",
        "",
        "**Estimand:** Among event-free carriers, quantify incremental association and predictive information from "
        "pre-outcome cholesterol-years, gene mechanism and Lp(a) for first incident ASCVD.",
        "",
        "**Method:** Model irregular LDL trajectories with mixed effects or prespecified trapezoidal area under the "
        "curve, explicitly accounting for treatment and measurement intensity; compare likelihood contribution, "
        "partial R², incremental C-index and calibration. Use correlated-predictor bootstrap decomposition rather "
        "than ranking standardised coefficients as causal importance.",
        "",
        "**Gate:** At least 200 participants with at least two genuinely pre-outcome LDL measures, at least 40 incident "
        "events, median measurement span at least five years and stable rank ordering in at least 80% of cluster "
        "bootstraps. Without these, report trajectory feasibility only and do not claim what “explains” risk.",
        "",
        "### I. Discordance scenario tests",
        "",
        "**Estimand:** Test whether the cross-sectional apoB/LDL association differs by diabetes or continuous TG/HDL "
        "status; high apoB is descriptive because it is algebraically entangled with the exposure.",
        "",
        "**Method:** Three locked interaction tests maximum, continuous modifiers where possible, penalised logistic "
        "models, cluster bootstrap CIs and Benjamini–Hochberg FDR. Report cohort-specific estimates before any pooling.",
        "",
        "**Gate:** At least 10 events in every displayed stratum, FDR q<0.05, clinically material interaction and "
        "same-direction evidence in both cohorts. Otherwise state no reproducible scenario-specific effect.",
        "",
        "### J. Grey-zone challenger",
        "",
        "**Estimand:** Determine whether adding Lp(a) and TG/HDL materially improves established-ASCVD classification "
        "over frozen CALON-N.",
        "",
        "**Method:** Source-only tuning with nested grouped validation; transport the frozen challenger in each "
        "direction; report paired AUC, calibration and decision-curve contrasts. No target-informed reselection.",
        "",
        "**Gate:** Delta AUC at least 0.02 with lower 95% CI above zero in both directions, no calibration deterioration "
        "beyond the comparator-provenance gate, and positive net benefit at two prespecified thresholds. Even if passed, "
        "call it a challenger until validated in new data.",
        "",
        "### K. LDL trajectory by treatment intensity",
        "",
        "**Estimand:** Describe within-person LDL change across documented treatment-intensity transitions; no apoB "
        "response estimand is supportable.",
        "",
        "**Method:** Align dated LDL values to dated medication/intensity periods; use a mixed-effects trajectory model "
        "with person-level random intercept and time, and report absolute/percentage LDL change. Treat indication, "
        "adherence and contact frequency as limitations, not solved confounders.",
        "",
        "**Gate:** At least 100 people with two LDL values bracketing a documented treatment change, at least one year "
        "of span and at least 30 people per intensity transition. If not met, provide only the aggregate measurement "
        "inventory and drop response language.",
        "",
        "## 4. Drop entirely and stop claiming",
        "",
        "Drop from the current analysis:",
        "",
        "- A current-data incident CALON-N model or Cox result.",
        "- ApoB-versus-LDL treatment response and the claim that statin monotherapy leaves apoB disproportionately high.",
        "- Reuse of the TUDOR genetic file for APOB/PCSK9 and any gene-agnostic LoF carrier rule.",
        "- Adding prior ASCVD to SAFEHEART while the outcome is prevalent ASCVD.",
        "- Confirmatory high-apoB-by-apoB/LDL interaction claims.",
        "- PPV/NPV calculated directly from an artificially matched sample.",
        "- A causal ranking of cumulative LDL, gene and Lp(a) using frozen prevalent outcomes.",
        "- The add-to-Montreal versus de novo narrative.",
        "- Clinical decision-curve or absolute-risk claims from the unrecalibrated transported probabilities.",
        "",
        "The paper should stop claiming: prospective risk prediction; incident validation; independent external "
        "validation of the selected architecture; consistent superiority over established comparators; transportable "
        "absolute risk; and a direct/non-LDL-mediated genetic effect from LDL matching.",
        "",
        "## 5. Disposition of the three blocking audit defects",
        "",
        "| Blocking defect | Plan disposition | What remains in the current paper |",
        "|---|---|---|",
        "| Predictors not demonstrably pre-outcome | **Fixable only in a new refreshed incident analysis.** Require a pre-outcome landmark and linked first events. | **Unfixable for current prevalent results; disclose as temporality/reverse-causation limitation.** |",
        "| Target-informed architecture selection | **Mitigated prospectively by freezing CALON-N now; fixed only by genuinely new temporal outcomes or a new cohort.** Refreshed outcomes unseen during selection can provide temporal validation. | **Unfixable for the reported reciprocal AUCs; call them target-informed transportability estimates.** |",
        "| Severe cross-site miscalibration | **Mitigable by prespecified intercept/slope recalibration after refreshed outcomes, then revalidated.** | **Not fixed now; disclose E:O failure and prohibit absolute-risk/clinical-use claims.** |",
        "",
        "## 6. Central claim and journal tier",
        "",
        "The strongest defensible current claim is:",
        "",
        "> In two selected genetically defined FH cohorts, a penalised seven-variable model containing age, sex, HDL, hypertension, smoking, apoB/LDL and apoA1 showed moderate cross-sectional discrimination for established ASCVD and evidence of ranking transportability, but it was target-informed, not consistently superior to simpler comparators, and not transport-calibrated.",
        "",
        "This is a specialist observational/model-development paper, not a clinical risk-prediction paper. In its "
        "current form it belongs in a mid-tier specialist lipid/genetic-epidemiology journal—roughly Journal of "
        "Clinical Lipidology or Atherosclerosis Plus scope—not Circulation, EHJ, JACC or a top-tier prevention/risk-model "
        "venue. Refreshed incident outcomes plus a genuinely locked temporal/external validation could raise the ceiling, "
        "but 40–70 events would still support restrained evaluation/update rather than an expansive new model search.",
        "",
        "## 7. Where I disagree with W1–W8 or the mediator argument",
        "",
        "- **W1:** Current-data incidence is dead, but W1 itself should not be called dead. The outcome-refresh request "
        "is the highest-priority rescue workstream; its result is gated, not assumed.",
        "- **W2:** Agree: strict remains primary. Do not rerun a vote based on the larger event count.",
        "- **W3:** Agree with a purpose-built set, but disagree with a generic LDLR+APOB+PCSK9 consequence-based "
        "P/LP-or-LoF rule. LDLR LoF can cause FH; APOB requires evidence of impaired LDL-receptor binding and generic "
        "truncating calls must not be assumed to cause FH; PCSK9 FH is gain-of-function, whereas PCSK9 LoF lowers LDL. "
        "Use gene-specific rules.",
        "- **W4:** Agree that age/sex/smoking matching is primary and LDL matching secondary. Disagree with labelling "
        "the latter “genotype effect not mediated by LDL-C”. It is an LDL-conditioned residual association unless a "
        "formal mediation design identifies a controlled or natural direct effect. Also, PPV/NPV cannot come unweighted "
        "from the matched sample.",
        "- **W5:** Split it. Build the LDL measurement inventory now; defer cholesterol-years risk ranking until refreshed "
        "outcomes. High-apoB effect modification is partly tautological and should not be confirmatory.",
        "- **W6:** Largely disagree. The data support a cautious LDL trajectory analysis only if treatment dates align; "
        "they do not support comparative apoB response.",
        "- **W7:** Agree and move it near the front. It determines which comparator analyses are scientifically interpretable.",
        "- **W8:** Split it into an immediate claim reset and final manuscript surgery after analysis gates; do not wait "
        "until the end to stop invalid claims from propagating.",
        "",
        "On the mediator argument: **I agree with the direction and disagree with the proposed label.** Matching on LDL "
        "when estimating the total effect/association of genotype blocks a major causal pathway and can bias toward the "
        "null; it may also induce selection/collider bias. Therefore LDL should not be in the primary match. But an "
        "LDL-matched secondary does not automatically estimate the portion “not mediated by LDL-C”; that requires "
        "well-defined mediator timing, mediator–outcome confounding assumptions and formal mediation analysis. Call it "
        "the LDL-conditioned residual association.",
        "",
        "## Reproducible entry points",
        "",
        "```bash",
        "cd /Users/nader85/Documents/CALON/calon_discordance_model_2026_08_09",
        "PYTHONDONTWRITEBYTECODE=1 python3 code/audit_2026_08_10/05_verify_timeline_delta.py",
        "PYTHONDONTWRITEBYTECODE=1 python3 code/audit_2026_08_10/06_build_forward_plan.py",
        "```",
    ]

    report = "\n".join(lines) + "\n"
    report_path = OUT / "FORWARD_PLAN.md"
    write_text(report_path, report)

    required_labels = [str(value) for value in range(1, 22)] + ["18b"]
    missing_labels = [
        label for label in required_labels
        if not re.search(rf"\| {re.escape(label)}\.", report)
    ]
    forbidden_patterns = {
        "participant_linkage_field": r"\bparticipant_id\b",
        "ukb_linkage_field": r"\beid\b",
        "family_linkage_field": r"\bfamily_id\b",
        "hgvs": r"\bHGVS\b",
        "variant_coordinate": r"\b(?:chr)?(?:[1-9]|1[0-9]|2[0-2]|X|Y):\d+:[ACGT]+:[ACGT]+\b",
    }
    forbidden_hits = [
        name for name, pattern in forbidden_patterns.items()
        if re.search(pattern, report, re.IGNORECASE)
    ]
    qc = {
        "all_comment_labels_assigned": not missing_labels,
        "missing_comment_labels": missing_labels,
        "forbidden_output_pattern_hits": forbidden_hits,
        "low_event_suppression_literal_present": "<10, non-estimable" in report,
        "timeline_verification_loaded": True,
        "participant_level_outputs": False,
        "overall": "pass" if not missing_labels and not forbidden_hits else "fail",
    }
    write_json(OUT / "forward_plan_qc.json", qc)
    if qc["overall"] != "pass":
        raise RuntimeError(f"Forward-plan QC failed: {qc}")
    print(json.dumps({
        "plan": "outputs/audit_2026_08_10/FORWARD_PLAN.md",
        "qc": qc["overall"],
    }, indent=2))


if __name__ == "__main__":
    main()
