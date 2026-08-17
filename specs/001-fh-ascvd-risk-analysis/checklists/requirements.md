# Spec-quality checklist — 001-fh-ascvd-risk-analysis

Reviewed 2026-08-14 against `spec.md`. A reviewer marks these, not the
implementer.

## Content quality

- [x] No implementation detail — no packages, procedures, seeds or file paths
- [x] Focused on analytic value and what a reader learns
- [x] Readable by a clinical collaborator who does not code
- [x] All mandatory sections present

## Requirement completeness

- [x] No `[NEEDS CLARIFICATION]` markers remain
- [x] Requirements are testable and unambiguous
- [x] Success criteria are measurable
- [x] Success criteria are technology-agnostic
- [x] Acceptance scenarios defined for every prioritised question
- [x] Edge cases identified
- [x] Scope bounded — out-of-scope section present
- [x] Dependencies and assumptions recorded

## Analysis readiness

- [x] Every analysis question has acceptance criteria
- [x] P1 alone yields a defensible result
- [x] Questions cover the primary argument of the intended paper
- [x] No implementation leakage

## Constitution compliance

- [x] **I Estimand before estimation** — FR-004 to FR-008 fix the outcome and
      time origin before any model; assumptions state the horizon
- [x] **II Nothing enters that could not be known at baseline** — FR-008
      (post-baseline events only), FR-020 (leak detector)
- [x] **III Comparators frozen, never inputs** — FR-016, FR-021, FR-022, FR-023
- [x] **IV Every number traces to a source** — SC-005, FR-023
- [x] **V Report the loss** — FR-025, FR-030, SC-001, SC-009

## Reviewer notes

Two judgements worth recording, both deliberate.

**P5 is last in priority but blocking for the label.** Whether the development
cohort is genuinely FH does not stop questions P1–P4 from being answered — the
model, comparison and validation are all valid for *variant carriers* regardless.
It blocks only the words used in the title, abstract and conclusions. Ordering it
P5 reflects analytic dependency, not importance.

**No clarification markers were needed.** The five decisions that would normally
warrant them — analysis population, missing-data handling, comparator definition,
what counts as pre-specified, and the risk horizon — are all settled in
Assumptions from prior work in this programme, and each is recorded there rather
than asked again.

**One known tension, carried forward to the plan.** FR-007 requires reporting
differential date availability across outcome components, and it is already known
that this makes the endpoint coronary-weighted. That is a limitation to disclose,
not a defect to fix, because the missing dates cannot be recovered. The plan must
not quietly drop it.
