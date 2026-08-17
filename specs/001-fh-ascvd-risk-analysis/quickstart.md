# Quickstart — 001-fh-ascvd-risk-analysis

## Environment

```bash
export CALON_PROJECT_ROOT="<this repository>"
export CALON_SHARED_MASTER="<master cohort tables>"
export CALON_WALES_DATA="<registry extracts>"
export CALON_CORRECTED_DATA="<corrected outcome extracts>"   # optional; resolved automatically
```

## Run

```bash
python3 code/18_RAW_QC_INDEPENDENT.py   # verify cohorts against raw first
python3 code/15_CALON_FINAL.py          # model and head-to-head
python3 code/15b_QC_ADDENDUM.py         # signs, completeness, calibration
python3 code/17_grey_zone_enhancers.py  # intermediate-band enhancers
```

## What a correct run prints

Verification: 3,540 carriers, 207 prevalent excluded, 62 heart-failure-only as
non-cases, 289 incident events, 3,333 at risk; validation 1,159 and 92; zero
temporality violations; all checks PASS.

Model: development concordance 0.6997, validation 0.7486; 10 wins, 58 ties, 1
loss across 69 estimable cells.

QC: every coefficient in its expected direction, zero convergence failures, leak
detector below the full model in both cohorts.

## When it fails

A missing environment variable stops the run rather than defaulting. A count
differing from the above means the cohort has changed — do not proceed to the
model until the difference is explained.
