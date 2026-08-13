# CALON-N statistical and computational QC

## Verdict

- Canonical cohort reconstruction: **PASS**.
- Family/qualifying-variant clustering: **PASS**.
- Raw-variable-only architecture: **PASS**.
- Fold-local preprocessing and penalty tuning: **PASS**.
- Physiological sign gate: **PASS** for selected CALON-N.
- Reproducible frozen scorer: **PASS** on synthetic repeated scoring.
- Protected external validation: **FAIL**; both outcomes were known at programme level and informed architecture selection.
- Prospective temporal validity: **FAIL**; contemporary DRAGON biomarkers often follow ASCVD/treatment.
- Absolute-risk transport: **FAIL**; E:O 3.00 and 0.45 across directions.
- All-comparator/all-subgroup superiority: **FAIL**.
- Clinical deployment: **FAIL**.

## Reproduced counts

| Cohort | N | Cases | Clusters |
|---|---:|---:|---:|
| DRAGON | 424 | 62 | 219 canonical families |
| UKB strict local LDLR P/LP | 890 | 57 | 62 qualifying-variant components |
| UKB P/LP-or-LoF | 1,264 | 80 | 66 qualifying-variant components |

DRAGON linkage reproduced 424/424 PASS participant matches, 412 direct family
agreements, and 12 participant-to-family realignments. No DRAGON participant was
dropped for family linkage.

## Model-selection audit

Ten candidates were named in the protocol amendment before phase-B execution.
Every source fit tuned ridge C inside grouped CV. The final architecture used
the highest lower reciprocal-transport AUC among candidates passing sign checks
in both source fits.

Higher-scoring target candidates were rejected when LDL-C, apoB, TG/HDL, or an
apoB-discordance term had a direction opposite to the prespecified physiology.
The largest rejected maximin AUC was produced by a model with negative LDL-C,
consistent with treatment/reverse-causation in a prevalent disease design.

Selected CALON-N coefficients in the pooled frozen model had the required
directions:

| Term | Coefficient | Gate |
|---|---:|---|
| age | +0.1123 | pass |
| male | +0.5804 | pass |
| HDL-C | −0.6299 | pass |
| hypertension | +0.1051 | pass |
| smoking | +0.1437 | pass |
| log(apoB/LDL-C) | +1.9104 | pass |
| log apoA1 | −1.6724 | pass |

## Validation audit

Candidate-specific repeated nested validation nested preprocessing and penalty
tuning but not the cross-cohort architecture choice. The reported transport
intervals resample target clusters conditional on the source-fitted model. They
do not include source-training or programme-selection uncertainty. The paper
states both limitations and avoids confirmatory superiority language.

Subgroups were not used for selection. Rows with fewer than 10 cases are
non-estimable; 10–19 cases are descriptive. No interaction claim is made.

## Calibration and clinical utility audit

Frozen probabilities were not recalibrated in targets. DRAGON→UKB overpredicted
threefold; UKB→DRAGON underpredicted. The generated decision-curve table is
**invalid for comparator inference** because age+sex, Montreal, and FH-Risk-Score
were ranking scores/linear predictors, not calibrated probabilities on the same
scale as CALON-N. The table is retained only as an audit artefact and all
net-benefit claims have been withdrawn from the manuscript.

## Missing-data audit

Source medians were fitted and applied within each training split. This avoids
target-distribution leakage but is statistically limited. Complete-case AUCs
were 0.753 in UKB and 0.891 in DRAGON, showing material missing-data
transport effects. A future validation should use predeclared multiple
imputation and re-estimate the entire pipeline in resamples.

## Reproducibility and privacy audit

- `apply_calon_n.py` produced byte-identical probabilities on two repeated
  executions of the synthetic test file.
- The saved model uses deterministic median completion and deterministic
  transformations.
- The pooled equation is explicitly separated from source-specific external
  transport fits.
- Package outputs were inspected by filename and schema; no participant ID,
  family ID, variant coordinate, participant row, or empirical participant-level
  prediction file is present.
- Canonical input and package hashes are recorded by `code/04_finalize_package.py`.

## Irreducible limitations

No further re-fitting within DRAGON/UKB can create independent validation. A
third cohort with baseline pre-event apoB/LDL/apoA1 and adjudicated outcomes is
required. Continuing candidate search on these outcomes would increase—not
reduce—risk of bias.
