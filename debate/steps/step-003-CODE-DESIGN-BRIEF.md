# Step 003 — Julius analysis-code design specification

## Decision requested

Design the analysis specification and the copy-paste Julius prompt required to
diagnose the comparator-scoring objections and then build a defensible CALON
ASCVD analysis. The panel has no data access. It must specify what code should
do and why — never report numbers it cannot calculate.

## Required reading

Read before answering:

1. `debate/DATA-INVENTORY.md`
2. `debate/steps/step-000-RESOURCE-AUDIT-BRIEF.md` and its completed outputs
3. `debate/steps/step-002-QC-BRIEF.md`
4. `debate/state/open-questions.md`
5. `CALON_JULIUS_SPECKIT/scripts/comparators.py`,
   `tests/test_comparators.py`, and
   `specs/001-calon-fh-5y/checklists/comparator-fidelity.md`

## Non-negotiable design constraints

- No participant-level data in prompts, outputs, transcripts, or state.
- UK Biobank primary: full follow-up (289 events); five-year (97 events) is a
  pre-specified sensitivity, not a replacement primary.
- Explore unrestrictedly first, but write, date, and hash the chosen
  specification before any comparator head-to-head score is calculated.
- Score Montreal, FH-Risk-Score, and SAFEHEART exactly as published, using
  coefficient values taken from source PDFs on disk and a provenance artefact.
  Do not re-fit, simplify, or reconstruct from memory.
- Use identical patients, outcome, horizon, and missing-data handling for every
  head-to-head comparison. Headline comparisons must be out-of-sample.
- `delta = metric(CALON) - metric(comparator)`; bootstrap paired 95% CIs with
  B ≥ 2,000.
- UK Biobank LDLR carriers are not automatically clinical FH. Endpoint is
  coronary-weighted because event-date completeness is uneven. State both
  constraints; do not claim to solve them.

## Must-design diagnostic code first

### OBJ-001 — comparator provenance and re-score

Write a code plan that:

1. produces one immutable comparator provenance table (citation, source PDF
   table/equation, predictor, coefficient/point, transformations, baseline
   survival, centring constants, horizon, unavailable-data policy);
2. implements each comparator as a pure scoring function;
3. writes a patient-set audit before scoring;
4. recomputes C-index and paired delta CIs from the same frozen cohort;
5. emits full subgroup win/tie/loss tables rather than a selective narrative.

### OBJ-002 — uniform slope compression

Design a factorial diagnostic for at least one source-faithful comparator:

| Variant | Centring | Baseline survival |
|---|---|---|
| A | published | published 5-year |
| B | published | published 10-year |
| C | uncentred | published 5-year |
| D | uncentred | published 10-year |

The code must report calibration slope, calibration-in-the-large, risk range,
and exact implementation variant. It must not assert the cause before the
output exists.

### OBJ-003 — age / cholesterol-years collinearity

Specify: Pearson correlation, condition diagnostics, and a pre-specified
refit replacing `age × untreated total cholesterol` with untreated total
cholesterol. Write criteria for interpreting a shifted age estimate without
overstating causality.

## Then design the model programme

1. **A1 exploration:** variable ledger against MACE and components; unadjusted,
   age-adjusted, fully adjusted; non-linearity, clinical interactions,
   missingness-as-signal. Label every result exploratory.
2. **A2 freeze:** human-readable spec + machine-readable coefficients/features
   artefact; timestamp and SHA-256 before comparator evaluation.
3. **A3 confirmatory:** frozen model, both horizons, comparators, calibration,
   full subgroup tables, TRIPOD+AI/STROBE/RECORD/PROBAST evidence.

## Panel response contract

Answer all four lenses under their own headings.

- Methodology: estimand, validation, freeze boundary, and reporting validity.
- Implementation: file/column-level code contract based only on
  `DATA-INVENTORY.md`; tests and outputs.
- Adversarial audit: ways the Julius code could make a false WIN and the tests
  that would fail.
- Clinical/publication: honest claims permitted before and after the diagnostic
  artefacts.

Propose a copy-paste Julius prompt and a file manifest. Do not write runnable
analysis code that assumes unseen data values. File objections as text only;
the orchestrator validates and records them.
# Step 003 — Design Julius-executable analysis code (full matrix)

**Protocol:** full matrix. Every model (Claude, Codex, Kimi, Grok) designs under
**all four lenses** in one turn. Round 1 is blind. No agent owns a seat.

**Governance:** you have no participant data and never will. Plan code from
`debate/DATA-INVENTORY.md` column names and aggregate reference counts only.
Never request rows, eids, NHS numbers, names, or DOBs.

**Upstream:** Step 001 objections OBJ-001, OBJ-002, OBJ-003 (comparator misscoring,
uniform slope cluster, age × cholesterol-years) outrank feature work. Step 002
QC disagreements (SAFEHEART/FH-RS C gaps, Wales n gap, grey-zone AUC) must be
diagnosable by the code you design.

**Fidelity baseline for comparators:** prefer the source-faithful implementations
and tests in `/Users/nader85/Documents/CALON/CALON_JULIUS_SPECKIT/scripts/comparators.py`
and `tests/test_comparators.py` over the simplified SAFEHEART linear score in
`code/15_CALON_FINAL.py`. Extract coefficients from PDFs on disk — never from
memory.

---

## Deliverable of this step

A **Julius-ready analysis specification + code outline** (functions, inputs,
outputs, assertions) that an investigator can paste/run in Julius. The panel
does not run the data; it designs what Julius must do.

Priority order for the code:

1. **OBJ-001 diagnostic** — score Montreal, FH-Risk-Score, SAFEHEART from
   PDF-sourced coefficients on one frozen cohort extract; emit provenance table
   (predictors, coefficients, endpoint, horizon, derivation cohort) and
   C-indices / deltas vs the model on identical patients.
2. **OBJ-002 diagnostic** — for at least one comparator, score centred vs
   uncentred linear predictor, and 5-year vs 10-year baseline survival; report
   calibration slopes under each variant.
3. **OBJ-003 diagnostic** — Pearson(age, cholesterol-years); refit preferred
   model with untreated TC alone instead of the product; report age HR both ways.
4. Only after those diagnostics are specified: exploratory variable ledger hooks
   (labelled exploratory), then a **freeze hook** (dated hash of the
   confirmatory formula **before** any head-to-head claim).

---

## Constraints the code must honour

- Join UKB outcomes from `corrected_ascvd_outcomes.csv`, not `ukb_master`
  outcome columns (trap).
- Exclude prevalent ASCVD and undated atherosclerotic cases (adopt Julius’s
  124 undated exclusion).
- Endpoint components as inventoried; I50 HF excluded from ASCVD.
- Full follow-up primary (289 events); 5-year sensitivity (97 events) — both
  reported, not swapped.
- `on_statin_self` missingness differs by carrier status — do not invent
  carrier-vs-non-carrier statin contrasts without handling that.
- Wales: genotype flag is `Positive1`, not `Mutation1`; outcome `ascvd_combine`.
- No stratum with &lt;10 events estimated; print `&lt;10, non-estimable`.
- Bootstrap for deltas: B ≥ 2000 if a WIN/TIE claim will be made.
- Sign convention: `delta = C(model) − C(comparator)`; positive favours model.

---

## Your task, under each lens (all four required)

**1. METHODOLOGY.** What estimands do these diagnostics answer? What must be
frozen before confirmatory head-to-head? What must **not** be claimed until
OBJ-001/002 artefacts exist?

**2. IMPLEMENTATION.** Pseudocode or Julius-cell outline with exact inventory
column names, join keys, assertion checks (row counts, event counts matching
reference aggregates), and output filenames. Name silent-failure modes you are
guarding against.

**3. ADVERSARIAL AUDIT.** Assume the designed code would still produce false
WINs. How? What single assertion or unit test would catch that before a paper
sentence is written?

**4. CLINICAL AND PUBLICATION REALITY.** What can a lipidologist or TRIPOD
reviewer demand from the output artefacts? Where is over-claim risk highest?

File every material disagreement as an `objection` block (checkable
`settled_by`). Do not declare consensus. Round 1: do not speculate what other
models will say.
