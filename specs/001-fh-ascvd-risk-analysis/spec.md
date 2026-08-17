# Specification — ASCVD risk analysis in genetically defined familial hypercholesterolaemia

**Feature:** `001-fh-ascvd-risk-analysis` · **Created:** 2026-08-14 · **Status:** draft

WHAT is to be answered and WHY. No packages, no statistical procedures, no file
paths — those live in `plan.md`.

---

## Analysis questions, prioritised

Each is independently answerable. Q1 alone is a publishable result.

### P1 — Does a model built from routinely available variables discriminate incident ASCVD in FH better than the published scores?

The three published FH scores are used clinically but have never been compared
head-to-head against a purpose-built model on a like-for-like **incident**
endpoint in genetically defined cohorts. Answering this alone justifies a paper,
whichever way it falls.

**Independent test.** Fit in the development cohort, score the three comparators
on the same participants and the same outcome, and report paired differences in
discrimination with confidence intervals. Complete without any other question.

**Acceptance scenarios**
1. Given the development cohort with an incident endpoint, when the model and
   the three comparators are scored on identical participants, then each paired
   difference in discrimination is reported with a 95% confidence interval and
   labelled WIN, TIE or LOSS.
2. Given a comparator requiring an input the cohort lacks, when it is scored,
   then the missing input and its consequence are stated rather than substituted.
3. Given any subgroup with fewer than ten events, when results are tabulated,
   then that cell reads "<10, non-estimable" rather than carrying an estimate.

### P2 — Does that model hold in an independent, differently ascertained FH cohort?

A model that works only where it was built is not useful. The validation cohort
is ascertained through a different route (registry cascade testing rather than
population volunteering), which tests transportability rather than just
resampling.

**Independent test.** Apply the frozen model to the validation cohort and report
discrimination and calibration without refitting.

**Acceptance scenarios**
1. Given the frozen model, when applied to the validation cohort, then
   discrimination and calibration are reported with no coefficient re-estimated.
2. Given the validation cohort's event count, when any comparison is a tie, then
   the minimum detectable difference is reported so ties are not read as
   equivalence.

### P3 — Which individual variables carry the risk, and does adjustment change what they appear to do?

Clinicians need to know which measurements matter, and reviewers need to see
whether an association survives adjustment or was confounding all along.

**Independent test.** Report each variable's association with the outcome
unadjusted, age-adjusted, and fully adjusted, side by side.

**Acceptance scenarios**
1. Given every variable in each cohort, when associations are reported, then
   unadjusted, age-adjusted and fully adjusted estimates appear together.
2. Given a variable whose direction reverses across adjustment levels, when
   results are reported, then the reversal is flagged explicitly.

### P4 — Do apoB/LDL-C discordance or Lp(a) reclassify anyone in the intermediate-risk band?

Enhancers rarely improve average discrimination because most people are already
sorted confidently. The clinical question is whether they resolve the band where
the treatment decision is genuinely uncertain.

**Independent test.** Define the intermediate band before examining enhancers,
then compare within it.

**Acceptance scenarios**
1. Given the intermediate band defined before any enhancer is examined, when
   enhancers are added, then the change in discrimination is reported with a
   confidence interval.
2. Given an enhancer with a significant hazard ratio but no significant gain in
   discrimination, when reported, then both facts are stated together.

### P5 — Is the development cohort actually an FH cohort?

The carrier flag may not identify familial hypercholesterolaemia. If the
phenotype does not support the label, every FH claim built on it fails. This is
last in priority order but **blocking for the title, abstract and conclusions**.

**Independent test.** Compare untreated LDL-C in flagged carriers against
non-carriers and against the expected FH phenotype.

**Acceptance scenarios**
1. Given the carrier flag, when untreated LDL-C is compared with non-carriers,
   then the excess is reported against the expected 3–4 mmol/L for
   heterozygous FH.
2. Given a separation inconsistent with FH, when the manuscript is written, then
   the cohort is described as variant carriers and not as FH throughout.

---

## Edge cases

- A comparator requires an input the cohort does not hold.
- A subgroup falls below ten events.
- A variable is too sparse in one cohort to be identified but not the other.
- Non-cardiovascular death is frequent enough to compete with the outcome.
- An outcome component is recorded but undated, so it cannot enter a
  time-to-event analysis.
- The two cohorts capture different event types, making the endpoints
  non-equivalent even when both are called ASCVD.
- Baseline treatment status alone discriminates better than the full model.
- A date column is stored in mixed formats, so the cohort depends on parser
  choice.

---

## Functional requirements

**Cohorts and eligibility**
- **FR-001** Each cohort MUST be defined by a stated genotype criterion, with
  the field or rule named.
- **FR-002** Where one dataset is a subset of another, they MUST be aggregated
  into a single cohort, never reported as independent cohorts.
- **FR-003** Participant flow MUST be reported from source records to analysis
  set, with the count removed at each exclusion.

**Outcome**
- **FR-004** The outcome MUST be defined by explicit diagnostic codes, listed.
- **FR-005** Heart failure MUST be excluded from the atherosclerotic endpoint.
- **FR-006** Any outcome field whose measured content contradicts its name MUST
  be identified and excluded, with the evidence reported.
- **FR-007** Differential availability of dates across outcome components MUST
  be quantified and reported as a limitation.
- **FR-008** Only events occurring after baseline MUST count; the minimum
  event-to-baseline interval MUST be reported.

**Descriptive analysis**
- **FR-009** Every variable MUST be summarised with its completeness, split by
  outcome status.
- **FR-010** Associations MUST be reported unadjusted, age-adjusted and fully
  adjusted, side by side.
- **FR-011** Missingness MUST be quantified per variable, and where it exceeds
  20% MUST be tested for association with the outcome.

**Time-to-event analysis**
- **FR-012** Survival curves and hazard ratios MUST be reported for each
  variable individually and for all variables jointly.
- **FR-013** The proportional-hazards assumption MUST be tested and any
  violation reported with the remedy applied.
- **FR-014** Where competing death is frequent, cumulative incidence MUST be
  reported alongside cause-specific estimates.
- **FR-015** Person-years, event counts and incidence rates MUST accompany every
  time-to-event result.

**Model**
- **FR-016** The model MUST use only raw measured variables; no published score
  or derived linear predictor may be a predictor.
- **FR-017** Predictor eligibility rules MUST be stated in advance and applied
  once per cohort, then held fixed across all subgroups.
- **FR-018** Any predictor that is an exact linear function of another MUST be
  detected and dropped.
- **FR-019** Model fitting failures MUST be counted and reported, never silently
  replaced with a default value.
- **FR-020** Baseline treatment status alone MUST be scored as a leakage check.

**Comparators**
- **FR-021** Each comparator MUST be scored exactly as published, with its
  coefficients taken from the source publication.
- **FR-022** Where more than one published version exists, the version scored
  MUST be identified and justified.
- **FR-023** Every comparator MUST carry a provenance record: predictors,
  coefficients, endpoint, horizon, derivation cohort, published performance, and
  whether frozen or refitted.

**Reporting**
- **FR-024** Discrimination and calibration MUST both be reported.
- **FR-025** Every comparison MUST be labelled WIN, TIE or LOSS by the
  confidence-interval rule, with losses reported.
- **FR-026** Subgroups MUST be pre-specified; differences between subgroups MUST
  be supported by an interaction test.
- **FR-027** Events per variable MUST be reported for each cohort.
- **FR-028** Reporting MUST be mapped item-by-item to TRIPOD+AI and
  STROBE/RECORD, with unmet items marked NOT MET.
- **FR-029** Risk of bias MUST be appraised across participants, predictors,
  outcome and analysis.
- **FR-030** Any variable added to the model after a result was seen MUST be
  disclosed as outcome-informed.

---

## Key entities

- **Development cohort** — variant carriers from a population biobank, with
  baseline measurements and dated follow-up.
- **Validation cohort** — genotype-confirmed registry participants, ascertained
  by cascade testing, aggregated with the specialist-clinic subset that carries
  additional measurements.
- **Outcome event** — first atherosclerotic event after baseline, defined by
  diagnostic code and date.
- **Predictor set** — demographic, clinical and lipid measurements available at
  baseline.
- **Comparator score** — a published risk equation with fixed coefficients.
- **Enhancer** — a measurement tested only within the intermediate-risk band.

---

## Success criteria

- **SC-001** Every analysis question P1–P5 has a reported answer, including
  those that fall against the model.
- **SC-002** Every reported comparison carries a confidence interval and a WIN /
  TIE / LOSS label.
- **SC-003** No cell with fewer than ten events carries an estimate.
- **SC-004** The participant flow reconciles: source records minus stated
  exclusions equals the analysis set, in both cohorts.
- **SC-005** Every number in the output can be traced to a named source and a
  runnable step.
- **SC-006** The frozen model is applied to the validation cohort with no
  coefficient re-estimated.
- **SC-007** Both reporting checklists are complete, with unmet items marked NOT
  MET rather than partial.
- **SC-008** Any cohort whose phenotype does not support the FH label is
  described as variant carriers throughout, including in the title and abstract.
- **SC-009** Every limitation found during the analysis appears in the
  limitations section, including analyses that could not be done.

---

## Assumptions

- Analysis is descriptive and predictive, not causal; no intervention effect is
  estimated.
- A five-year horizon is the primary time frame, chosen for clinical
  decision relevance.
- The intermediate-risk band is 5–20% predicted five-year risk, following
  prevention-guideline convention, fixed before enhancers are examined.
- Untreated lipid values are back-calculated where treatment is recorded, using
  the published adjustment factor.
- Where a dataset stores a pre-treatment lipid value directly, no further
  back-correction is applied.
- The development cohort is the larger one; the differently ascertained cohort
  is reserved for validation.
- Ten events is the minimum for any reported estimate.
- Family structure is accounted for in the registry cohort; the biobank cohort
  is treated as unrelated unless shown otherwise.

---

## Out of scope

- Causal inference on any predictor.
- Clinical deployment, thresholds, or treatment recommendations.
- Re-derivation of published comparator equations.
- Any analysis requiring participant-level data to leave approved storage.
