# Phase 0 research — 001-fh-ascvd-risk-analysis

Each decision records what was chosen, why, and what was rejected.

## R1 — Which outcome source for the development cohort?

**Decision.** The corrected outcome extract, restricted to atherosclerotic
components I21, I25, I63, I70, I73, G45.

**Rationale.** The master's own composite is not a MACE endpoint: it is 93.4%
accounted for by chronic ischaemic heart disease alone, its myocardial-infarction
field holds 1,293 of 501,936 and its stroke field 321. A separate field named for
angina flags 41.7% of the cohort with mean systolic pressure 148.9 against a
cohort 139.7 and no male excess — it encodes essential hypertension. Both were
measured, not inferred from the names.

**Rejected.** The master composite (not MACE); any field whose measured content
contradicts its label.

**Residual limitation.** Component date availability is uneven — coronary codes
are essentially fully dated while stroke is 40.9%, transient ischaemic attack
37.0% and peripheral disease 52.8%. The endpoint is therefore coronary-weighted.
The dates cannot be recovered, so this is disclosed rather than fixed.

## R2 — Should heart failure be in the endpoint?

**Decision.** Excluded.

**Rationale.** Heart failure is not atherosclerotic disease. In the development
cohort 62 of 351 events in the broad composite carried heart failure with no
atherosclerotic code at all. Including them inflated the case set and masked a
subgroup loss that reappeared once the endpoint was corrected.

**Rejected.** The broad composite, despite giving a better win tally — the
tally was an artefact of the wrong endpoint.

## R3 — Which fields define the validation cohort?

**Decision.** Genotype by the registry `Positive1` flag; outcome by the registry
`ascvd_combine` composite; baseline from the first measurement date; event age as
the minimum across the dated event-age fields. Outcome-positive participants
without a dated event age are excluded as untimeable.

**Rationale.** These fields do not announce their role. Using the presence of a
recorded mutation instead of the genotype flag returns 3,562 people rather than
2,405. Defining the outcome as "has a dated event age" rather than the composite
changes both the risk set and the event count. An independent rebuild that
guessed from column names produced 1,079/110 instead of 1,159/92.

**Rejected.** Mutation-presence as genotype; dated-event-age as outcome.

## R4 — How are dates parsed?

**Decision.** Mixed-format inference, stated explicitly in the Methods.

**Rationale.** A day-first parser silently re-reads one measurement-date column
as year-day-month, losing 2,186 parses and shifting the censoring set enough to
change the cohort to 948/82. The baseline column itself is unambiguous; the
sensitive column is the one feeding the censor age, which is not where anyone
would look first.

**Rejected.** Day-first parsing.

**Note for anyone comparing date columns.** Compare with both values present. A
bare inequality counts two missing values as a difference and manufactures
disagreements — that error produced a spurious count of 1,350 during this work.

## R5 — Which published version of the first comparator? [OPEN]

Two publications exist. The derivation lists age, sex, HDL-C, hypertension and
smoking with no lipoprotein(a) term; the later refinement's keyword list does
include lipoprotein(a). The coefficients currently in use match the earlier form.

**Action.** Read both source PDFs, state which version is scored and why, and
record its exact coefficients in the provenance table. Do not inherit the
assumption.

## R6 — Does the development cohort's carrier flag identify FH? [OPEN]

Measured: untreated LDL-C excess over non-carriers is +0.55 mmol/L, 91.1% of
flagged carriers sit below 6.5 mmol/L, and the variant-identifier column is empty
for all 501,936 rows. Heterozygous FH should show roughly +3 to +4 mmol/L.

An attempt to re-derive the flag against pathogenicity annotation failed: the
variant call file and the master share no participants, so the flag's provenance
cannot currently be reconstructed from local files.

**Action.** Establish what produced the flag. Until then the development cohort
is described as variant carriers, not FH. Blocking for the label only — the
model, comparison and validation remain valid for variant carriers.
