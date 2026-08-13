# CALON-N model card

> ## ⚠ CONTAINS RETRACTED RESULTS — NOT A SUBMISSION DRAFT
>
> This document reports the **cross-sectional UK Biobank arm**, retracted on
> 11 August 2026 for outcome-to-predictor temporality reversal: 100% of prevalent
> ASCVD events pre-dated the blood draw, and `pre_ldl.fillna(ldl_chem)` restored
> post-event, on-treatment lipids for every case. The figures **0.7605, 0.767,
> 0.848 and 0.7672**, the 890/57 cohort and the 15 UK Biobank head-to-head
> comparisons are withdrawn and must not be cited as findings.
>
> It is retained as the provenance record of what was believed at the time.
> The current analysis is **CALON-F** (`code/15_CALON_FINAL.py`). See
> [STATUS.md](STATUS.md) — from `manuscript/`, [../STATUS.md](../STATUS.md).

## Intended use

CALON-N is a research classifier for identifying **already established,
recorded ASCVD** among genetically defined FH participants with contemporary
apoB, LDL-C, apoA1 and routine risk-factor data.

It is not a model of incident disease, 5- or 10-year risk, treatment effect,
causal biology, or treatment eligibility. It must not be used for clinical
deployment, treatment withholding, or autonomous triage.

## Architecture

CALON-N was built from raw variables; no published risk score is an input:

- age, years;
- male sex (1=yes, 0=no);
- HDL-C, mmol/L;
- hypertension (1=yes, 0=no);
- ever smoking (1=yes, 0=no);
- log(apoB [g/L] / LDL-C [mmol/L]);
- log(apoA1 [g/L]).

The pooled research equation is:

```text
logit(p) = -5.673054
           + 0.112263 × age
           + 0.580373 × male
           - 0.629887 × HDL-C
           + 0.105120 × hypertension
           + 0.143724 × ever_smoker
           + 1.910359 × log(apoB/LDL-C)
           - 1.672421 × log(apoA1)
```

The frozen program uses the stored scaler and ridge model. The equation and
program agree when all inputs are supplied. Missing values use the pooled
development medians, which is a pragmatic research convention, not a clinically
validated imputation strategy.

## Development data

- DRAGON: 424 participants, 62 established-ASCVD cases, 219 canonical families.
- UK Biobank primary: 890 coordinate-linked local LDLR P/LP carriers, 57 cases,
  62 qualifying-variant connected components.
- UK Biobank union sensitivity: 1,264 P/LP-or-LoF carriers, 80 cases.

The final architecture was selected after reciprocal target performance was
known. The pooled equation uses DRAGON and strict UK Biobank together. It has no
untouched external validation.

## Performance

| Transport | AUC (95% CI) | Calibration slope | E:O |
|---|---:|---:|---:|
| DRAGON→UKB strict | 0.767 (0.712–0.828) | 0.951 | 3.004 |
| UKB strict→DRAGON | 0.848 (0.796–0.896) | 0.752 | 0.447 |
| DRAGON→UKB union | 0.767 (0.719–0.813) | 0.929 | 3.047 |

Candidate-specific nested grouped AUC was 0.893 in DRAGON and 0.794 in strict
UK Biobank. These estimates do not correct for architecture selection across
the two target cohorts.

## Comparator verdict

CALON-N was above adapted FH-Risk-Score and SAFEHEART in the DRAGON→UKB
direction, similar to Montreal in UKB, and below Montreal in the reverse
direction. It did not beat all comparators or all subgroups.

## Known failure modes

- contemporary/post-event lipid and apolipoprotein measurements;
- strong setting-specific calibration drift;
- treatment-related reverse causation in LDL-based terms;
- apoA1 missing in approximately 24% of DRAGON and 12% of strict UKB;
- endpoint and predictor-definition differences between cohorts;
- very few cases in untreated, younger, diabetic and high-Lp(a) strata;
- local ClinVar table lacks review-status enforcement;
- target-informed selection and conditional target-only bootstrap intervals;
- predominantly White-European populations.

## Required next validation

A genuinely new FH cohort must provide:

1. genotype-confirmed pathogenic variants under a frozen rule;
2. biomarkers obtained before the prediction time and before outcome;
3. adjudicated incident ASCVD and competing death;
4. families/variants retained intact in resampling;
5. enough events for calibration and treatment/sex subgroup assessment;
6. blinded scoring with this model frozen before outcomes are examined;
7. local recalibration evaluated separately from discrimination.

## Files

- Model: `model/calon_n_from_scratch.joblib`
- Equation: `model/calon_n_equation.json`
- Scorer: `code/apply_calon_n.py`
- Synthetic test: `model/synthetic_predictors.csv`
- Main performance: `outputs/scratch_external_performance.json`
- Subgroups: `outputs/scratch_subgroups.csv`

