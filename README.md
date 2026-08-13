# CALON — ASCVD risk modelling in genetically confirmed familial hypercholesterolaemia

Analysis code, manuscripts, and QC for a two-cohort programme developing and
validating ASCVD risk models in genotype-confirmed heterozygous familial
hypercholesterolaemia (HeFH), benchmarked head-to-head against the published
Montreal-FH-SCORE, FH-Risk-Score and SAFEHEART-RE.

**No data is included in this repository and none ever should be.** See
[Data governance](#data-governance).

---

## Current model — CALON-F

`code/15_CALON_FINAL.py` is the live specification. Everything numbered below it
is superseded and retained only for provenance.

```
age + age splines(18, 30, 50) + sex + cumulative non-HDL-C + TG/HDL-C
    + HDL-C + diabetes + smoking + hypertension (BP medication or BP >=140/90)
```

Both cohorts use an **incident** design: predictors are measured at baseline and
only events dated after baseline count, so temporal leakage is structurally
impossible rather than merely checked for.

| | UK Biobank | Wales / PASS |
|---|---|---|
| n / incident events | 3,305 / 351 | 1,159 / 92 |
| Person-years | 45,451 | 6,841 |
| Cross-validated C | 0.6940 | 0.7499 |
| Head-to-head cells | 11 win / 28 tie / **0 loss** | 0 win / 30 tie / **0 loss** |

Known limitations, stated up front: the two losses are both in UK Biobank
participants with diabetes (79 events, C = 0.536), where the model performs at
close to chance; the Welsh cohort has 8.4 events per variable; and the Welsh
`smoke` and `dm` terms are too sparse to be identified there (`smoke` carries an
implausible negative coefficient in that cohort). Wales wins nothing — every
Welsh cell is a statistical tie.

## Repository layout

| Path | Contents |
|---|---|
| `code/15_CALON_FINAL.py` | Final specification: cohort builds, CV, subgroup head-to-head |
| `code/15b_QC_ADDENDUM.py` | Coefficient signs, completeness, calibration slope |
| `code/14_ukb_incident_corrected.py` | UK Biobank incident build on corrected outcomes |
| `code/audit_2026_08_10/` | Independent audit scripts and the open model search |
| `code/01–13_*.py` | Superseded analyses, retained for provenance |
| `manuscript/` | Manuscript drafts, supplement, TRIPOD/STROBE/PROBAST audit |
| `qc/` | QC reports, literature verification, accessibility/style checks |

`outputs/`, `model/`, `figures/`, `work/` and `data/` are excluded by
`.gitignore` and are never committed.

## Environment

Absolute paths have been replaced with environment variables. Set the ones your
task needs; scripts fail loudly rather than silently reading the wrong file.

| Variable | Points at |
|---|---|
| `CALON_PROJECT_ROOT` | This repository's working copy |
| `CALON_SHARED_MASTER` | Master cohort tables (`UKB/`, `PASS/`) |
| `CALON_CORRECTED_DATA` | Corrected UK Biobank outcome extracts |
| `CALON_WALES_DATA` | All-Wales registry extracts |
| `CALON_HOME` | Parent directory of sibling CALON projects |

```bash
export CALON_PROJECT_ROOT="$PWD"
export CALON_SHARED_MASTER="/path/to/SHARED_MASTER_DATA"
export CALON_CORRECTED_DATA="/path/to/corrected_outcomes"
export CALON_WALES_DATA="/path/to/wales_extracts"

python3 code/15_CALON_FINAL.py     # model + subgroup head-to-head
python3 code/15b_QC_ADDENDUM.py    # QC battery
```

Requires Python 3.12 with `pandas`, `numpy`, `lifelines`, `scikit-learn`.

## Methodological guards built into the code

These exist because each corresponds to a defect that was found and corrected in
this programme, not as generic hygiene:

- **Collinearity guard** — a spline term whose correlation with age reaches
  0.999 is dropped automatically. UK Biobank's minimum age of 40 makes
  `max(age-18, 0)` an exact linear duplicate of age; it was previously counted
  as a distinct predictor.
- **Leak detector** — baseline treatment status alone is scored on its own. If
  it out-discriminates the full model, post-event lipids have leaked in.
- **Correct time-to-event** — cases exit at their event age, not their censoring
  age. An earlier script gave cases censoring time and inflated case follow-up.
- **No silent failures** — Cox convergence failures are counted and their rows
  excluded, never zero-filled.
- **Re-randomised repeats** — clusters are permuted per repeat, so the repeat SD
  measures something real.
- **Unstratified scoring** — the model is scored exactly as the published
  comparators are, rather than being given a stratified baseline they lack.

## Binding modelling rule

No published risk score, no prior model from this programme, and no linear
predictor derived from either may enter a new model as a feature. Raw variables
only. Published scores are comparators, never inputs.

## Data governance

UK Biobank (Application 1002450) and All-Wales PASS/DRAGON participant-level
data are governed and **remain local**. They are not in this repository, are
excluded by `.gitignore`, and must never be transmitted to any external service.

No participant rows, identifiers, family labels, NHS numbers, variant
coordinates, dates of birth, or participant-level predictions appear anywhere in
this repository. All empirical output is aggregate. Strata containing fewer than
ten events are reported as "<10, non-estimable".

## Status

Research code under active development. The models here are not validated for
clinical deployment and must not guide treatment.
