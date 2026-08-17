<!--
Sync Impact Report
  Version change: (none) → 1.0.0
  Rationale: initial ratification. No prior constitution existed.
  Added principles: I Estimand Before Estimation; II Nothing Enters That Could
    Not Be Known At Baseline; III Comparators Are Frozen, Never Inputs;
    IV Every Number Traces To A Source; V Report The Loss
  Added sections: Data Governance; Reporting Standards; Governance
  Removed sections: none
  Deferred TODOs: none
-->

# CALON FH ASCVD Analysis Constitution

Rules that no analysis in this programme may violate. Each is here because it
was broken once and cost a retraction, a withdrawn result, or a week of work.
A reviewer must be able to read any script or manuscript and say plainly whether
it complies.

## Core Principles

### I. Estimand Before Estimation

Every analysis MUST state, in one sentence and before any model is fitted, the
population, the exposure or contrast, the outcome, the time horizon, and the
handling of competing events.

An analysis MUST NOT be relabelled after the fact. A cross-sectional classifier
of established disease MUST NOT be described as predicting incident risk, and
verbs MUST match the design: "was associated with" for cross-sectional,
"predicted" only for prospective.

*Rationale.* The same participants gave apparent discrimination of 0.878 under a
prevalent outcome and 0.714 under an incident one, and LDL-C inverted from
OR 0.83 to HR 1.02 between them. The design, not the data, produced the
difference.

### II. Nothing Enters That Could Not Be Known At Baseline

Every predictor MUST be measured before the outcome it predicts. Participants
with an event on or before baseline MUST be excluded from an incident analysis,
and the minimum event-to-baseline interval MUST be reported and be strictly
positive.

Each analysis MUST run a leak detector: score baseline treatment status alone.
If it out-discriminates the full model, post-event information has entered and
the analysis MUST stop rather than be reported with a caveat.

*Rationale.* A UK Biobank arm was retracted after 100% of prevalent events were
found to pre-date the blood draw, with `pre_ldl.fillna(ldl_chem)` silently
restoring post-event, on-treatment lipids for every case.

### III. Comparators Are Frozen, Never Inputs

No published risk score, no prior model from this programme, and no linear
predictor derived from either MAY enter a new model as a feature. Raw measured
variables only.

Published comparators MUST be scored exactly as published. Coefficients MUST NOT
be refitted, re-derived, or invented. Where a comparator is adapted or an input
is unavailable, the adaptation and its consequence MUST be stated in the
Methods.

*Rationale.* A model built on a published score's linear predictor is not a new
model. Separately, comparator functions were once found carrying invented
weights while their docstrings claimed published provenance.

### IV. Every Number Traces To A Source

Every number in a manuscript, table, or figure MUST trace to a named file and a
runnable script. A claim asserted in a docstring, comment, or prior summary is
NOT evidence and MUST be re-measured before reuse.

Quality-control checks MUST be capable of failing. A check whose condition is a
constant, or that validates the fitting while never testing the inputs, is a
defect and MUST be replaced.

Outcome provenance MUST be recorded explicitly: which file, which field.

*Rationale.* A false claim about UK Biobank field labelling propagated through
three script docstrings into a status document before anyone measured it, and
two quality checks printed PASS while testing nothing.

### V. Report The Loss

Results MUST be reported whether or not they favour the model. A subgroup where
the model loses MUST appear in the results with its confidence interval.

A difference is a WIN only where its 95% confidence interval excludes zero. A
positive point estimate whose interval crosses zero is a TIE and MUST be
labelled as one. Where a cohort lacks power to resolve a difference, the minimum
detectable difference MUST be stated rather than allowing a reader to infer
equivalence from ties.

Variables MUST NOT be added after seeing a loss without disclosing that sequence
in the Methods. Where outcome-informed selection has occurred, it MUST be named.

*Rationale.* Zero losses were once achieved only by counting heart failure as
atherosclerotic disease; correcting the endpoint restored the loss. The honest
tally survives review, the flattering one does not.

## Data Governance

Participant-level UK Biobank (Application 1002450) and All-Wales PASS/DRAGON
data MUST remain on approved local storage and MUST NOT be transmitted to any
external service, including cloud analysis tools and AI services.

Any file containing direct identifiers — NHS number, name, date of birth,
postcode — MUST be labelled as identifiable wherever it is stored, and MUST NOT
be placed in a bundle framed for sharing. De-identification for external use
MUST produce a separate derived copy; originals are never modified.

All published output MUST be aggregate. Participant rows, identifiers, family
identifiers, dates of birth, variant coordinates, and participant-level
predictions MUST NOT appear in any output, log, or repository.

Any stratum containing fewer than ten events MUST be reported as
"<10, non-estimable" and MUST NOT be estimated.

## Reporting Standards

Prediction models MUST be reported against TRIPOD+AI and appraised with PROBAST.
Observational analyses MUST follow STROBE, with RECORD where routinely collected
health data are used.

Discrimination alone is insufficient. Calibration MUST be reported — slope,
calibration-in-the-large, observed/expected ratio, and a calibration plot.

Events per variable MUST be reported. Where it falls below ten, this MUST appear
as a stated limitation.

Model selection performed with knowledge of outcome data MUST be described as
target-informed development, never as protected external validation.

## Governance

This constitution supersedes any conflicting practice. Where a specification,
plan, or task conflicts with a principle here, the specification, plan, or task
MUST change — the principle MUST NOT be reinterpreted to fit.

Amendments MUST be a separate, explicit act, recording what changed and why.
Versioning is semantic: MAJOR for removing or redefining a principle, MINOR for
adding or materially expanding one, PATCH for clarification.

Compliance MUST be checked before any analysis is declared locked and before any
manuscript is submitted. A violation found after locking requires the affected
result to be withdrawn, not annotated.

**Version**: 1.0.0 | **Ratified**: 2026-08-14 | **Last Amended**: 2026-08-14
