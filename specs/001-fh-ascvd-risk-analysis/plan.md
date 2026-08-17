# Implementation plan — 001-fh-ascvd-risk-analysis

**Spec:** `spec.md` · **Constitution:** v1.0.0 · **Created:** 2026-08-14

HOW the specification is executed. Every choice here is gated against the
constitution.

---

## Technical context

| | |
|---|---|
| Language | Python 3.12 (3.9 tolerated; avoid 3.10+ syntax in shared code) |
| Core packages | pandas, numpy, lifelines (Cox, KM, concordance), scikit-learn, statsmodels, scipy |
| Model class | Penalised Cox proportional hazards, ridge (L2) |
| Penalty | 0.05, fixed; selected within training folds where tuned |
| Random seed | 20260813, stated in every script |
| Resampling | 5-fold cross-validation, 6 re-randomised repeats; cluster bootstrap 1,200 replicates |
| Storage | Local approved storage only; no cloud, no external service |
| Target platform | Single workstation, macOS |
| Scale | 501,936 source records → 3,333 development; 7,253 → 1,159 validation |
| Performance goal | Full pipeline under 30 minutes; no step silently exceeding memory |

**Unknowns carried into research:** the correct published version of one
comparator; whether the development cohort's carrier flag identifies FH.

---

## Constitution check — gate

| Principle | Gate | Status |
|---|---|---|
| I Estimand before estimation | Estimand fixed in `spec.md` before any fitting; incident design; 5-year horizon; competing death handled | PASS |
| II Nothing known after baseline | Post-baseline events only; minimum lag reported; leak detector mandatory | PASS |
| III Comparators frozen | Raw variables only; comparator coefficients read from source PDFs, never refitted | PASS |
| IV Every number traces | Outcome provenance recorded per cohort; QC checks must be capable of failing | PASS |
| V Report the loss | WIN/TIE/LOSS by CI rule; minimum detectable difference where underpowered | PASS |
| Data governance | Local only; identifiable files labelled; <10 suppression | PASS |
| Reporting standards | TRIPOD+AI, STROBE/RECORD, PROBAST as checklists gating the manuscript | PASS |

**Complexity tracking.** One justified deviation.

| Deviation | Why needed | Simpler alternative rejected because |
|---|---|---|
| Cohort-adaptive predictor set (a term may be dropped in one cohort) | The validation cohort cannot identify predictors with fewer than ten events in a level; forcing them in yields an implausible coefficient | Forcing one identical specification produced a wrong-signed smoking coefficient and EPV 8.4. The rule is mechanical and pre-specified, applied once per cohort, so it is not tuning |

---

## Project structure

```
code/
  15_CALON_FINAL.py          model, cohorts, CV, subgroup head-to-head
  15b_QC_ADDENDUM.py         coefficient signs, completeness, calibration
  17_grey_zone_enhancers.py  intermediate-band enhancer panel        [P4]
  18_RAW_QC_INDEPENDENT.py   raw rebuild, independent of the pipeline
  22_REDERIVE_LDLR_PLP.py    carrier-flag interrogation              [P5]
outputs/
  calon_final.json           head-to-head and subgroup results
  calon_final_qc.json        QC battery
  raw_qc_independent.json    independent verification
specs/001-fh-ascvd-risk-analysis/
  spec.md plan.md research.md data-model.md quickstart.md
  contracts/  checklists/
```

---

## Phase 0 — research

Recorded in `research.md`. Four questions resolved, two open.

---

## Phase 1 — design

`data-model.md` — cohorts, derived variables, and the exact field rules.
`contracts/` — input and output schemas.
`quickstart.md` — how to run and what a correct run prints.

---

## Statistical procedures

**Cohort construction.** Development: variant carriers, prevalent excluded,
outcome from the corrected file restricted to atherosclerotic components.
Validation: registry genotype flag, registry outcome composite, exclusions in
fixed order (missing baseline → prevalent → outcome-positive-without-date → no
positive follow-up).

**Predictor eligibility, applied once per cohort then frozen.**
1. Drop any spline term correlating ≥0.999 with age.
2. Score a binary predictor only where both levels hold ≥10 events.
Both are mechanical. Neither consults the outcome beyond the event count that
also governs reporting suppression.

**Untreated lipids.** Divide by 0.70 where treatment is recorded — *except*
where a field already holds a pre-treatment value, in which case no correction
is applied. This distinction is keyed off the source dataset, not assumed.

**Cross-validation.** Clusters permuted per repeat so the repeat standard
deviation measures resampling variability rather than returning zero.
Family-clustered in the validation cohort; unrelated assumption in the biobank
cohort, stated as a limitation.

**Comparison.** Paired difference in Harrell's C, cluster bootstrap, 1,200
replicates. WIN if the lower bound exceeds zero, LOSS if the upper bound falls
below zero, otherwise TIE. Where all comparisons in a cohort are ties, report the
minimum detectable difference.

**Calibration.** Slope from regressing the outcome on the cross-validated linear
predictor; observed/expected ratio; calibration plot by predicted-risk decile.

**Enhancers.** Intermediate band fixed at 5–20% predicted five-year risk before
enhancers are examined. Compared within band only.

---

## Failure handling

Scripts stop on a missing input rather than degrade. Model convergence failures
are counted and their rows excluded from scoring, never zero-filled — a bare
`except: lp = 0` once produced a spurious concordance of 0.5613.

---

## Re-run of the constitution check after design

All gates still PASS. The single complexity deviation is recorded above with its
rationale and remains justified: it is a stated rule applied identically to both
cohorts, which happens to fire in only one.

---

## Open risks carried to tasks

1. **The carrier flag may not identify FH.** Blocking for the FH label only.
2. **The endpoint is coronary-weighted** because stroke, TIA and peripheral
   components are inconsistently dated. Not fixable; must be disclosed.
3. **The two cohorts capture different event types.** Affects how transportability
   is described.
4. **Validation cohort is underpowered** to resolve differences below roughly
   0.15 in concordance. Ties must not be read as equivalence.
