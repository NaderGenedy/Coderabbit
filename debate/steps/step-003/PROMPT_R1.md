# Debating agent mandate — Claude, Codex, Kimi, Grok, Gemini

You are **one voice on a panel**, invoked cold with no memory of any prior turn.
Everything you need is in the files you were given. Read them before writing.

## Your job

You answer **all four lenses**, not one. Every model on this panel does the same,
independently, so that disagreement is four models on the same question rather
than four roles talking past each other.

Attack the current step. Not politely — specifically. A turn that says the work
looks reasonable is a wasted invocation and worse than silence, because it
creates a false impression that the step was examined.

## The four lenses — answer each under its own heading

**1. METHODOLOGY.** Is the estimand right? Does the design answer the question
asked? Are reporting standards met? Is the inference the design licenses the one
being drawn?

**2. IMPLEMENTATION.** Would the code do what it claims? Is anything silently
degrading — a check that cannot fail, a filter excluding its own target, a
default swallowing an error? Is it reproducible from the stated inputs?

**3. ADVERSARIAL AUDIT.** Assume the conclusion is wrong. What is the most
likely way it is wrong, and what would have failed if it were? Attack the
strongest version of the claim.

**4. CLINICAL AND PUBLICATION REALITY.** Would a lipidologist believe this? Does
it change practice? Where does a hostile reviewer open? Is anything over-claimed
relative to what the numbers support?

If a lens genuinely has nothing to add on this step, say so **and say what you
checked**. Silence without an account is not acceptable.

## Output format — Markdown first (mandatory)

Write your **entire turn as Markdown** a human can open in an editor:

1. Start with a title: `# Step NNN · Round R · <your-name>`.
2. Use these exact H2 headings (full matrix — every agent answers every lens):
   - `## 1. Methodology`
   - `## 2. Implementation`
   - `## 3. Adversarial audit`
   - `## 4. Clinical and publication reality`
3. Put tables in GitHub-flavoured Markdown. Put runnable snippets in fenced
   code blocks with a language tag (`python`, `bash`, `r`, `json`).
4. Put every objection in a fenced ` ```objection ` block (schema in
   `state/open-questions.md`).
5. End with `## Artefacts` listing any code/tests/paths you propose.

The orchestrator saves your reply as:

`debate/steps/step-NNN/rR/<you>.md`

Do **not** rely on plain `.txt` as the human deliverable. If you also emit
code, put it in fenced blocks in that same `.md`, or name a proposed path under
`debate/steps/step-NNN/rR/code/` — never invent that you already wrote a file
unless the orchestrator confirms it.

## What a good turn contains

1. **All four lenses answered**, each under its own heading (above).
2. **At least one objection, or an explicit statement that you tried and failed
   to find one** — naming what you checked and why it held. "No objections" with
   no account of what you looked for is not acceptable.
3. Each objection filed as an ` ```objection ` block (the orchestrator merges
   into `state/open-questions.md` after schema checks). A malformed block
   blocks every step until fixed.
4. `settled_by` must name a **test that could actually be run** — a script, a
   recomputation, a specific number to check. "Further discussion" is not a
   settlement condition and will be rejected.
5. Your reasoning, in full, in `steps/step-NNN/rR/<you>.md` (Markdown).

## What you must not do

- **Never declare consensus.** You cannot close a step. `bin/consensus.mjs`
  decides, from the register. Typing "consensus reached" achieves nothing except
  wasting a turn.
- **Never answer your own objection.** `answered_by` must differ from
  `raised_by`; the script rejects self-closure.
- **Never write "we discussed and agree" as evidence.** Evidence must name a
  file, path or number. Prose agreement resolves nothing.
- **In round 1, never speculate about what the others will say.** You are blind
  to them by design; guessing collapses four independent positions into one.
- **Never soften another agent's objection.** If you think it is wrong, say so
  with a reason and leave it OPEN, or answer it with an artefact. Do not rewrite
  it.
- **Never invent a citation, coefficient or published performance figure.** If
  you do not have the number, say you do not have it. A plausible fabricated
  coefficient is the single most damaging thing you can contribute here, and
  this project has already been damaged that way once.

## Governance — absolute, applies to every agent

- You will never be given participant-level data, and you must never ask for it.
  You reason about aggregate counts.
- Never emit an `eid`, NHS number, name, date of birth, postcode, family
  identifier or variant coordinate. If you think you need one to make a point,
  make the point with a count instead.
- Any stratum under 10 events is `<10, non-estimable`. Do not estimate in it and
  do not ask anyone else to.

## What earns a strong turn

The defects found in this project so far were all of one kind: something that
looked checked but was not. Two quality checks whose condition was a constant
printed PASS for weeks. A claim about a data field propagated through three
docstrings into a status document before anyone measured it. A file-discovery
filter that silently excluded the most important input. A comparator scored with
invented coefficients while its docstring claimed published provenance.

Look for that shape. Ask of every claim: **what would have failed if this were
wrong?** If the answer is nothing, you have found something.


--- STEP 003, ROUND 1 (INDEPENDENT — blind) — JULIUS PYTHON DELIVERABLE ---
Goal: produce **copy-paste Julius-ready Python** that settles OBJ-001, OBJ-002,
OBJ-003 (and the dual SAFEHEART / n=3333 vs 3209 / Wales ledger defects from
step-000 Round 1). The PI will run this code on Julius AI after reviewing.

Answer ALL FOUR LENSES in Markdown.

Then under ## Artefacts you MUST include:
1. A complete Julius notebook cell sequence as fenced ```python blocks
   (or one script per objection). Use ONLY column names from DATA-INVENTORY.md.
2. Aggregate-only prints (n, events, C-index, slopes, correlations). Never eid.
3. Import or paste Spec Kit SAFEHEART/Montreal/FH-RS from the comparators.py
   excerpt below — do NOT invent coefficients from memory.
4. Explicit TODO where a PDF coefficient must be typed from disk.
5. A short Julius paste order (Cell 1, Cell 2, ...).

Do not declare consensus. File new objections only if the code design itself is flawed.

--- BRIEF ---
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


--- OBJECTION REGISTER ---
# Objection register

**This file is the consensus engine.** `bin/consensus.mjs` parses it and decides
whether a step may close. Nothing else decides that — not a model saying
"consensus reached", not the orchestrator's judgement.

## How to file an objection

Write a fenced ` ```objection ` block. Free prose between blocks is ignored, so
argue as much as you like around them; only the blocks are parsed.

**Required fields** — a block missing any of these makes the whole register
MALFORMED and blocks every step until fixed:

| Field | Meaning |
|---|---|
| `id` | `OBJ-NNN`, unique, never reused |
| `step` | the step number this belongs to |
| `raised_by` | `claude` \| `codex` \| `kimi` \| `grok` \| `gemini` |
| `claim` | the specific, checkable thing you say is wrong |
| `settled_by` | what evidence would settle it — name the test, not "further discussion" |
| `status` | `OPEN` \| `ANSWERED` \| `ACCEPTED-RISK` \| `WITHDRAWN` |

**Conditional fields:**
- `status: ANSWERED` → `evidence` naming a file, path or number, **and**
  `answered_by` which must differ from `raised_by`
- `status: ACCEPTED-RISK` → `dissenter` (a name) and `risk_text` (≥10 chars)
- `status: WITHDRAWN` → `withdrawn_because` (≥10 chars)

## Rules the script enforces, which you cannot talk your way past

1. **You may not close your own objection.** `answered_by` must differ from
   `raised_by`.
2. **"We agree" is not evidence.** `evidence` must contain a path, filename or
   number. Prose consensus does not resolve anything.
3. **Accepting a risk requires a name against it.** Anonymous acceptance is how
   disagreement gets quietly smoothed away.
4. **A step with objections from fewer than two agents cannot close.** A step
   nobody challenged has not been debated, it has been rubber-stamped.
5. **MAX_ROUNDS is enforced in code.** Hitting it writes DEADLOCK. Deadlock is a
   legitimate outcome and gets published as an open risk with the dissenter
   named. Manufacturing agreement to avoid it is the one unforgivable move.

---

## Live objections

The three below are real and unresolved, taken from an independent appraisal of
the Julius analysis run on 14 August 2026. They are seeded here deliberately: a
cold model reading this file must have something substantive to bite on, and
these are the sharpest open questions in the project.

```objection
id: OBJ-001
step: 001
raised_by: kimi
claim: Both declared WINs rest on comparator C-indices that disagree with the local pipeline in one direction only. Julius reports SAFEHEART C=0.628 and FH-Risk-Score C=0.651 in UK Biobank; the local pipeline gets 0.6944 and 0.6740. Substituting the local values turns SAFEHEART 10-year from +0.079 [0.033,0.123] WIN to +0.013 TIE, and FH-RS from +0.052 [0.001,0.104] WIN to +0.030 TIE. Montreal, the only comparator needing neither Lp(a) nor LDL-C bands, reproduces to 0.003. The asymmetry is not random.
settled_by: Score all three comparators from the coefficients printed in the source PDFs on disk, on one identical frozen cohort extract, and publish a provenance table with predictors, coefficients, endpoint, horizon and derivation cohort for each. Then recompute both deltas.
status: OPEN
```

```objection
id: OBJ-002
step: 001
raised_by: grok
claim: All four comparator calibration slopes cluster at 0.52-0.57. Three independently derived scores do not spontaneously agree on a uniform ~2x compression of the linear predictor. That signature indicates a shared implementation error - most likely baseline survival applied at the wrong horizon, or the linear predictor not centred on its derivation-cohort mean - not three coincidental miscalibrations.
settled_by: Recompute one comparator two ways, centred and uncentred, and at both 5-year and 10-year baseline survival. If the slope moves from ~0.55 toward 1.0 under one variant, the bug is identified. Report the slope under each variant.
status: OPEN
```

```objection
id: OBJ-003
step: 001
raised_by: codex
claim: Age carries HR 1.20 [0.91-1.60] - null - for 5-year incident ASCVD, which does not happen in real data. Age and cholesterol-years (defined as age x untreated total cholesterol) sit in the same model and both come out null (1.20 and 1.15). This is the collinearity the specification explicitly required a check for; the correlation with age was never reported and the drop rule at 0.999 was never applied. Every coefficient in the preferred model is suspect until resolved.
settled_by: Report the Pearson correlation between age and cholesterol-years in the analysis cohort, and refit with cholesterol-years replaced by untreated total cholesterol alone. If the age HR moves away from null, the collinearity is confirmed.
status: OPEN
```

## Worked example — what a resolved objection looks like

```objection
id: OBJ-000
step: 000
raised_by: kimi
claim: The UK Biobank arm is described as familial hypercholesterolaemia, but the carrier flag may not identify FH.
settled_by: Compare untreated LDL-C in flagged carriers against non-carriers and against the +3 to +4 mmol/L expected for heterozygous FH.
status: ANSWERED
answered_by: claude
evidence: verify/01_endpoints_htn_hf_mace.py output; median excess +0.226 mmol/L (95% CI 0.185-0.268), 2.1% of carriers above 6.5 mmol/L, variant_id empty in all 501936 rows
```


--- DATA INVENTORY ---
# Data inventory — everything needed to plan analysis code

**Read this before writing a line of code.** Every column name below was verified
against the actual file headers on 15 August 2026, not recalled from memory.

**You will never see participant data.** This inventory gives you file shapes,
column names and derivation rules. That is enough to write correct code and is
all you are permitted. Never request a data extract, a row, or an identifier.

---

## Files

| Key | File | Rows × Cols | Role |
|---|---|---|---|
| `ukb_master` | `ukb_master.csv` | 501,936 × 179 | Exposures, covariates, baseline date, carrier flag. **Its own outcome columns are unusable — see traps.** |
| `ukb_outcomes` | `corrected_ascvd_outcomes.csv` | 501,936 × 14 | **The outcome source.** Join on `eid`. |
| `ukb_bpmeds` | `04a_meds_touch.csv` | 501,936 × 13 | Touchscreen BP medication. Columns prefixed `participant.` |
| `wales` | `WALES_FH_CLEANED.csv` | 7,253 × 190 | The Welsh analysis cohort |
| `pass` | `pass_master.csv` | 7,253 × 141 | Same registry, different column naming. Zero shared column names with `wales`. |
| `dragon` | `FH_Dragon3 (1).csv` | 424 × 202 | Complete subset of `wales` (424/424 on `DatabaseNumber`) |

All in one folder: `CALON_DATA_PACKAGE_2026-08-13/raw/all_inputs/`.
SHA-256 for each is in `SHA256SUMS.txt`.

---

## UK Biobank columns

**Cohort and time**
`eid` · `ldlr_carrier` (1 = carrier; 3,540 of 501,936) · `date_baseline` ·
`age_exact_baseline` · `sex_F` (1 = female) · `death_date` · `death_cause`

**Lipids** — `tc_chem` · `ldl_chem` · `hdl_chem` · `tg_chem` · `apob` ·
`apob_chem` · `nmr_apob` · `lpa_chem` · `pre_lpa` · `lpa_i0`

**Risk factors** — `sbp` · `dbp` · `diabetes_combined` · `diabetes_any` ·
`smoking_ever` · `smoking_current` · `smoking_status` · `bmi_direct`

**Treatment** — `on_statin_self` · `statin_ever` · `statin_duration_years` ·
`age_at_statin_start`

**BP medication** (separate file) — `participant.p6153_i0` (women),
`participant.p6177_i0` (men). Code `2` in either means BP medication. Baseline
instance `_i0` only.

**Outcomes** (`ukb_outcomes`) — `ascvd_first_date_best` · `ascvd_first_date_dated`
· component flags `i21_event` `i25_event` `i50_event` `i63_event` `i70_event`
`i73_event` `g45_event`

---

## Welsh columns

**Cohort** — `Positive1` (**the genotype flag**) · `Mutation1` (**not** the flag)
· `DatabaseNumber` · `FamilyNumber` · `Gender` · `Proband`

**Outcome** — `ascvd_combine` (**the outcome flag**) · event ages `MIACSAge`
`PCIStentsAge` `CABGAge` `ANGINAAge` `TIAAge` `PVDAge`

**Time** — `DOB`, `DOB_1` · `MeasurementDate.1` … `.4` · `BMIDate` ·
`AGE_AT_DECEASED` · `Treatmentdate1`

**Lipids, serial** — `TC.1–.4` · `LDL.1–.4` · `HDL.1–.4` · `TRG.1–.4` · `Lpa.1–.4`

**Risk factors** — `Smoking` · `Diabetes` · `BloodPressureMedication` ·
`BloodPressureSystolic` · `BloodPressureDiastolic`

## DRAGON columns — what it adds to Wales

Join `dragon` onto `wales` on `DatabaseNumber` (424/424). It contributes:

- **`ApoB`** — the *only* apoB anywhere in the Welsh data
- Serial lipids `TC_1–4`, `LDL_1–4`, `HDL_1–4`, `TRG_1–4`, `Lpa_1–4` with
  `MeasurementDate_1–4`
- `MtachedLDLC` — **already pre-treatment**
- `age_at_event`, `age_at_event_or_censoring`, `Smoking_binary`,
  `Diabetes_binary`, `onBPtreat`, `eGFR`, `BMI`

Note the naming difference: Wales uses dots (`TC.1`), DRAGON uses underscores
(`TC_1`). Do not assume one from the other.

---

## Traps — each of these has already produced a wrong result

**1. `first_angina` is hypertension.** Flags 41.7% of UK Biobank, mean SBP 148.9
vs 139.7, no male excess. It encodes I10. **Never use it.**

**2. `first_ascvd` is not MACE.** 93.4% accounted for by `first_other_ihd` alone;
the MI field holds 1,293 people and stroke 321, of 501,936. **Use
`ukb_outcomes`, never the master's outcome columns.**

**3. `has_hf` / `i50_event` is heart failure.** Not atherosclerotic. **Exclude
from the endpoint.** 62 of 351 carrier events were heart-failure-only.

**4. `Positive1`, not `Mutation1`.** Positive1 gives 2,405; Mutation1-present
gives 3,562. Using the wrong one changes the cohort by 1,157 people.

**5. `ascvd_combine`, not "has a dated event age".** Different risk set and
different event count.

**6. Welsh dates need `format="mixed"`.** `MeasurementDate.2` parses 3,783 values
under mixed and only 1,597 under `dayfirst=True`, with 1,417 genuine
disagreements. It feeds the censor age, so a day-first parser silently changes
the cohort from 1,159/92 to 948/82.

**7. `MtachedLDLC` is already pre-treatment.** Do **not** apply the ÷0.70 statin
back-correction to it — that double-corrects the treated majority.

**8. `on_statin_self` is populated for carriers and missing for every
non-carrier.** Any back-calculated carrier-vs-non-carrier comparison is
one-sided. Keep such comparisons symmetric and uncorrected as primary.

**9. DRAGON `eGFR` and `BMI` hold empty strings and values like `">90"`.** Parse
as text before coercing.

**10. Comparing dates:** use `a.notna() & b.notna() & (a != b)`. A bare `a != b`
counts NaT vs NaT as a difference and invents disagreements.

---

## Derivations the analysis needs

| Quantity | Rule |
|---|---|
| Untreated lipid | Divide by 0.70 where on treatment — **except** `MtachedLDLC` |
| Cumulative non-HDL-C | `log((TC − HDL) × age)`, on the untreated scale |
| TG/HDL-C | `log(TG / HDL)` |
| Hypertension | BP medication **or** SBP ≥140 **or** DBP ≥90 |
| Endpoint | `i21 | i25 | i63 | i70 | i73 | g45` — **I50 excluded** |
| Prevalent | event date ≤ baseline → **exclude** |
| Incident | event date > baseline |
| Undated case | atherosclerosis-positive, no usable date → **exclude**, not a non-case |
| Welsh exit | event age for cases, else `AGE_AT_DECEASED` or last contact |

---

## Reference counts — your code must reproduce these

| | Value |
|---|---|
| UK Biobank carriers | 3,540 |
| Prevalent excluded | 207 |
| Undated excluded | 124 |
| Risk set | 3,209 |
| Events — 5 y / 10 y / full | 97 / 194 / 289 |
| Welsh genotype-positive | 2,405 |
| Welsh risk set / events | 1,159 / 92 |
| DRAGON matched into Wales | 424 / 424 |

**If your code produces different numbers, your code is wrong** — or you have
found something, in which case file an objection saying which number and why.

## Known limitations to carry, not fix

Event-date completeness: I21 100%, I25 100%, I63 40.9%, I70 64.3%, I73 52.8%,
G45 37.0%. The endpoint is coronary-weighted; the dates cannot be recovered.

The UK Biobank cohort is **LDLR variant carriers, not FH** — untreated LDL-C
excess +0.15 to +0.23 mmol/L median, ~1–2% above 6.5 mmol/L, `variant_id` empty
in all 501,936 rows, and high-confidence loss-of-function carriers show no
stronger phenotype. Write "LDLR variant carriers" throughout.

Wales cannot resolve concordance differences below roughly 0.15. Ties there are
a power statement, not equivalence.


--- SPECKIT comparators.py (source of truth for published forms) ---
"""Source-faithful FH comparator functions used only after G5 approval.

These functions are pure and deliberately strict. They do not impute, convert Lp(a)
mass to molar units, extrapolate outside native eligibility, or pretend that a
ranking score is an absolute-risk model.
"""

from __future__ import annotations

import math


class ComparatorInputError(ValueError):
    """A required input is missing, outside range, or in an unsupported unit."""


def _require_finite(name: str, value: float) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError) as exc:
        raise ComparatorInputError(f"{name} must be numeric") from exc
    if not math.isfinite(parsed):
        raise ComparatorInputError(f"{name} must be finite")
    return parsed


def safeheart_linear_predictor(
    *,
    age_years: float,
    male: bool,
    prior_ascvd: bool,
    hypertension: bool,
    bmi_kg_m2: float,
    active_smoking: bool,
    ldl_mg_dl: float,
    lpa_mg_dl: float,
) -> float:
    """Published categorical SAFEHEART linear predictor.

    Source: Pérez de Isla et al., Circulation 2017, Table 3 and worked examples.
    """
    age = _require_finite("age_years", age_years)
    bmi = _require_finite("bmi_kg_m2", bmi_kg_m2)
    ldl = _require_finite("ldl_mg_dl", ldl_mg_dl)
    lpa = _require_finite("lpa_mg_dl", lpa_mg_dl)
    if age < 18:
        raise ComparatorInputError("SAFEHEART adult application requires age >=18")
    if bmi <= 0 or ldl < 0 or lpa < 0:
        raise ComparatorInputError("BMI and lipid inputs must be non-negative")

    lp = 0.70 * bool(male)
    lp += 1.07 * (30 <= age < 60)
    lp += 1.45 * (age >= 60)
    lp += 0.69 * bool(hypertension)
    lp += 1.42 * bool(prior_ascvd)
    lp += 0.48 * bool(active_smoking)
    lp += 0.88 * (25 <= bmi < 30)
    lp += 0.98 * (bmi >= 30)
    lp += 0.92 * (100 <= ldl < 160)
    lp += 1.57 * (ldl >= 160)
    lp += 0.42 * (lpa > 50)
    return float(lp)


def safeheart_risk(horizon_years: int, **inputs: object) -> float:
    """Return published five- or ten-year SAFEHEART absolute risk."""
    baseline_survival = {5: 0.9532, 10: 0.9025}
    if horizon_years not in baseline_survival:
        raise ComparatorInputError("SAFEHEART supports only five- and ten-year risk")
    lp = safeheart_linear_predictor(**inputs)
    risk = 1.0 - baseline_survival[horizon_years] ** math.exp(lp - 5.4078)
    if not 0 <= risk <= 1:
        raise ArithmeticError("SAFEHEART calculation returned an invalid probability")
    return risk


def _montreal_age_points(age: float) -> int:
    if age <= 21:
        return 0
    if age <= 28:
        return 4
    if age <= 35:
        return 8
    if age <= 42:
        return 12
    if age <= 49:
        return 16
    if age <= 56:
        return 20
    if age <= 63:
        return 24
    return 28


def montreal_fh_score(
    *, age_years: float, hdl_mmol_l: float, hypertension: bool, smoking_ever: bool, male: bool
) -> int:
    """Original Montreal-FH-SCORE points; ranking/prevalent-CVD use only."""
    age = _require_finite("age_years", age_years)
    hdl = _require_finite("hdl_mmol_l", hdl_mmol_l)
    if age < 18 or hdl < 0:
        raise ComparatorInputError("Montreal score requires adult age and non-negative HDL-C")
    if hdl <= 0.60:
        hdl_points = 12
    elif hdl <= 0.90:
        hdl_points = 9
    elif hdl <= 1.20:
        hdl_points = 6
    elif hdl <= 1.50:
        hdl_points = 3
    else:
        hdl_points = 0
    return (
        _montreal_age_points(age)
        + hdl_points
        + 2 * bool(hypertension)
        + bool(smoking_ever)
        + 3 * bool(male)
    )


def combined_fh_score(
    *,
    age_years: float,
    hdl_mmol_l: float,
    hypertension: bool,
    smoking_ever: bool,
    male: bool,
    lpa_mg_dl: float,
) -> int:
    """Published Combined-FH-SCORE points; ranking/prevalent-CVD use only."""
    age = _require_finite("age_years", age_years)
    hdl = _require_finite("hdl_mmol_l", hdl_mmol_l)
    lpa = _require_finite("lpa_mg_dl", lpa_mg_dl)
    if age < 18 or hdl < 0 or lpa < 0:
        raise ComparatorInputError("Combined score requires adult age and non-negative lipids")
    if hdl <= 0.70:
        hdl_points = 8
    elif hdl <= 1.00:
        hdl_points = 6
    elif hdl <= 1.30:
        hdl_points = 4
    elif hdl <= 1.60:
        hdl_points = 2
    else:
        hdl_points = 0
    if lpa <= 5.0:
        lpa_points = 0
    elif lpa <= 37.0:
        lpa_points = 1
    elif lpa <= 69.0:
        lpa_points = 2
    elif lpa <= 101.0:
        lpa_points = 3
    else:
        lpa_points = 4
    return (
        _montreal_age_points(age)
        + hdl_points
        + 2 * bool(hypertension)
        + 2 * bool(smoking_ever)
        + 3 * bool(male)
        + lpa_points
    )


def fhrs_chart_points(
    *,
    age_years: float,
    male: bool,
    hdl_mmol_l: float,
    untreated_ldl_mmol_l: float,
    hypertension: bool,
    active_smoking: bool,
    lpa_mg_dl: float,
) -> int:
    """Published FH-Risk-Score chart points for adults aged 18-65."""
    age = _require_finite("age_years", age_years)
    hdl = _require_finite("hdl_mmol_l", hdl_mmol_l)
    ldl = _require_finite("untreated_ldl_mmol_l", untreated_ldl_mmol_l)
    lpa = _require_finite("lpa_mg_dl", lpa_mg_dl)
    if not 18 <= age <= 65:
        raise ComparatorInputError("FH-Risk-Score native age range is 18-65")
    if min(hdl, ldl, lpa) < 0:
        raise ComparatorInputError("FH-Risk-Score lipid inputs must be non-negative")

    if age <= 30:
        age_points = 0
    elif age <= 35:
        age_points = 9
    elif age <= 40:
        age_points = 14
    elif age <= 45:
        age_points = 16
    elif age <= 50:
        age_points = 17
    elif age <= 55:
        age_points = 18
    elif age <= 60:
        age_points = 20
    else:
        age_points = 23

    if hdl > 1.30:
        hdl_points = 0
    elif hdl >= 1.01:
        hdl_points = 3
    elif hdl >= 0.85:
        hdl_points = 7
    else:
        hdl_points = 8

    if ldl <= 5.50:
        ldl_points = 0
    elif ldl <= 7.50:
        ldl_points = 3
    elif ldl <= 8.50:
        ldl_points = 7
    elif ldl <= 9.50:
        ldl_points = 9
    else:
        ldl_points = 11

    return (
        7 * bool(male)
        + age_points
        + hdl_points
        + ldl_points
        + 6 * bool(hypertension)
        + 6 * bool(active_smoking)
        + 4 * (lpa >= 50)
    )


def fhrs_chart_risk_percent(points: int) -> str:
    """Published categorical ten-year risk associated with FHRS chart points."""
    if isinstance(points, bool) or not isinstance(points, int) or points < 0:
        raise ComparatorInputError("FHRS points must be a non-negative integer")
    bands = [
        (9, "1%"), (14, "2%"), (17, "3%"), (20, "4%"), (22, "5%"),
        (24, "6%"), (25, "7%"), (26, "8%"), (27, "9%"), (29, "10%"),
        (30, "11%"), (31, "13%"), (32, "14%"), (33, "15%"), (34, "17%"),
        (35, "18%"), (36, "20%"), (37, "22%"), (38, "24%"), (39, "27%"),
        (40, "29%"), (41, "31%"), (42, "34%"), (43, "37%"), (44, "40%"),
        (45, "43%"), (46, "47%"), (47, "50%"), (48, "53%"), (49, "57%"),
        (50, "60%"), (51, "63%"), (52, "68%"),
    ]
    for upper, risk in bands:
        if points <= upper:
            return risk
    return ">75%"


