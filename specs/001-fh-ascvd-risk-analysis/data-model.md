# Data model — 001-fh-ascvd-risk-analysis

## Cohorts

| Entity | Definition | Size |
|---|---|---|
| Development cohort | Variant carriers, prevalent atherosclerotic disease excluded | 3,333 at risk, 289 events |
| Validation cohort | Registry genotype-positive, exclusions in fixed order | 1,159 at risk, 92 events |
| Clinic subset | Complete subset of the validation cohort, matched on record number | 424, aggregated not separate |

## Outcome

| Field | Rule |
|---|---|
| Event | First atherosclerotic event after baseline |
| Components | I21, I25, I63, I70, I73, G45 |
| Excluded | I50 heart failure — not atherosclerotic |
| Time origin | Baseline measurement date |
| Exit | Event date for cases; death or administrative end otherwise |
| Constraint | Event date strictly after baseline; minimum interval reported |

## Predictors

| Variable | Derivation | Expected direction |
|---|---|---|
| Age | Exact age at baseline, with spline terms at 18, 30, 50 | positive |
| Sex | Male indicator | positive |
| Hypertension | BP medication at baseline, or measured BP ≥140/90 | positive |
| Type 2 diabetes | Recorded diagnosis | positive |
| Smoking | Ever-smoker | positive |
| Cumulative non-HDL-C | log(untreated non-HDL-C × age) | positive |
| TG/HDL-C | log(triglycerides ÷ HDL-C) | positive |

Untreated lipids are back-calculated by dividing by 0.70 where treatment is
recorded, except where the source field already holds a pre-treatment value.

## Enhancers — tested only in the intermediate band

| Variable | Availability |
|---|---|
| log(apoB / LDL-C) | Development cohort; validation only via the clinic subset |
| log(1 + Lp(a)) | Development cohort; assay scale differs in validation, so not pooled |

## Eligibility rules

| Rule | Trigger | Effect |
|---|---|---|
| Collinearity | Spline term correlating ≥0.999 with age | Term dropped |
| Minimum information | Binary predictor with <10 events in either level | Term dropped |

Applied once per cohort to the full cohort, then held fixed across every
subgroup, so no subgroup is fitted with its own specification.
