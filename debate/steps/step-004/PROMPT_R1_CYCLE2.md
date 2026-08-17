# Step 004 · Round 1 · Cycle-2 CALON-G model lock

You are one member of the Cycle-2 model-selection panel. Work independently,
but use the full Julius Spec-kit evidence injected into this prompt by the
orchestrator.

## Objective

Design a **single new pre-specified candidate model, CALON-G**, which will be
fitted on the frozen UK Biobank cohort and assessed against all three
PDF-faithful comparators. We aim to be competitive — preferably WIN or TIE —
but this is **not permission to tune the feature set after seeing subgroup
WIN/TIE/LOSS results**. A universal-winner search would be exploratory and
cannot be presented as a confirmatory model.

## Locked evidence from Julius

- Frozen cohort: 3,540 carriers → 207 prevalent permitted-ASCVD exclusions →
  124 undated exclusions → **n=3,209**, 289 full events, 97 at 5 years, 194 at
  10 years; cohort SHA-256
  `8c3a1e0598770c1beefe29db28d42fb7074f233f382c25c19eb0c843b59f49b2`.
- The old five-year mask is invalid. Horizon code must use:
  `t_h = minimum(time, H)` and `e_h = event & (time <= H)`.
- The current 68 TIE / 9 LOSS / 1 WIN tally is withdrawn: invalid horizon
  mask, B=300 pilot, candidate comparator implementations, and an exploratory
  Lp(a) conversion.
- Centre SAFEHEART: omission of 5.4078 yielded a 77% five-year mean risk and
  0.166 slope versus 1.22% and 0.871 when centred.
- Age/cholesterol-years r=0.606 and age/cumulative non-HDL r=0.577. They are
  meaningful shared information, not r>=0.999 duplicate terms.
- Montreal, SAFEHEART and FH-Risk PDFs now exist at
  `/Users/nader85/Downloads/CALON-DeepResearch/papers/` with text extracts at
  `/Users/nader85/Downloads/CALON_FH_PROGRAMME_2026-08-09/04_papers/extracted_text/`.
  Any score must be page/table-verified before it can be named as published.

## Candidate clinical ingredients supplied by investigator

1. Age with a transparent spline/spike functional form
2. Sex
3. Smoking
4. Hypertension medication
5. Type 2 diabetes
6. log(TG/HDL)
7. Cumulative non-HDL **or** a grey-zone apoB/HDL term
8. Lp(a)

## Mandatory design constraints

1. **Primary model has one lipid-burden path:** cumulative non-HDL *or* apoB/HDL,
   not both. The alternative is a declared sensitivity model.
2. Retain Lp(a) only with a frozen unit/assay policy. If external comparator
   scoring requires nmol/L→mg/dL conversion, name the conversion as exploratory
   sensitivity rather than a fact.
3. Preprocessing (imputation, scaling, splines, penalty) must be learned in each
   training fold only. Use cluster/family-aware repeated cross-validation.
4. Model development has 289 full events: justify effective degrees of freedom
   and the ridge penalty. Do not fit a flexible forest or opaque ensemble just
   to chase C-index.
5. Primary evaluation is full follow-up and 5-year horizon with the corrected
   truncation. Use B=2,000 paired cluster bootstraps for final CIs.
6. All three comparators must use the *same frozen evaluable set*, PDF-locked
   functions, and no healthy-default imputation. If a comparator cannot be
   scored, label it NOT-EVALUABLE; do not drop survivors.
7. Report the full matrix; any `n_events < 10` is `<10, non-estimable`.

## Deliverable

Write a Cycle-2 model protocol, under the mandatory four headings:

1. Choose **one** CALON-G primary formula and explain why each term stays or
   goes. State one sensitivity formula only.
2. State exact preprocessing, missing-data policy, penalty selection, fold
   structure, predictor degrees of freedom and calibration strategy.
3. Give acceptance gates for a final result: cohort hash, 97 five-year events,
   PDF provenance, B=2,000, full matrix, multiplicity warning.
4. Draft a Julius-ready fit-and-evaluate pseudocode block; it must use
   corrected horizon truncation.
5. File an objection only if a specific condition must be met before fitting;
   do not create generic objections. If you file one, use `step: 004`.

Do not claim CALON-G wins before it is fitted.
