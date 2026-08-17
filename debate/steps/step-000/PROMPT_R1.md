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

The orchestrator saves your reply as `debate/steps/step-NNN/rR/<you>.md`.
Do **not** treat plain `.txt` as the human deliverable.

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

--- STEP 000, ROUND 1 (RESOURCE AUDIT, INDEPENDENT AND BLIND) ---
You already have the permitted resources below. Do NOT call tools. Do NOT edit files.
Answer ALL FOUR LENSES with concrete path citations. End with proposed objection blocks as text only.

===== RESOURCE: step-000 brief =====
# Step 000 — resource audit before any scientific debate

## Purpose

Before evaluating comparator scoring, model performance, or any claimed WIN,
each panel agent must independently map and interrogate the evidence that is
permitted to enter this debate. This is a full-matrix step: every agent answers
every lens. It is not a literature-performance claim and it cannot close
OBJ-001, OBJ-002, or OBJ-003.

## Permitted resources

Read deeply, cite exact path and section/function/test where relevant:

1. `debate/DATA-INVENTORY.md`
2. `debate/mandates/AGENT.md`, `ORCHESTRATOR.md`, and `ROLES.md`
3. `debate/state/open-questions.md`, `transcript.md`, and
   `locked-decisions.md`
4. `debate/bin/panel.mjs` and `consensus.mjs`
5. `debate/steps/step-002-QC-BRIEF.md`
6. `code/15_CALON_FINAL.py`, `STATUS.md`, `README.md`,
   `outputs/calon_final.json`, and `outputs/calon_final_qc.json`
7. `CALON_JULIUS_SPECKIT/scripts/comparators.py`,
   `tests/test_comparators.py`, `research.md`, and
   `checklists/comparator-fidelity.md`
8. Comparator source PDFs already on disk, if located by filename/path only.
   Never fabricate coefficients or publication results if a PDF cannot be
   located or read.

## Prohibited resources

Never open, request, print, or transmit raw participant-level files, including
anything under `CALON_DATA_PACKAGE_2026-08-13/raw/`. No `eid`, NHS number,
name, date of birth, postcode, family identifier, or variant coordinate may
appear in output.

## Deliverable

Under all four headings required by `mandates/AGENT.md`, produce:

1. A resource ledger: what you examined, what it establishes, and what it does
   not establish.
2. A discrepancy ledger: every conflict found between source docs, code, tests,
   and aggregate outputs.
3. A statement of what evidence is still needed before each of OBJ-001,
   OBJ-002, and OBJ-003 can close.
4. At least one checkable objection, or a specific account of why none is
   warranted.

Round 1 is blind. Do not infer other models' positions.

===== RESOURCE: ROLES.md =====
# Full-matrix protocol — every model plays every lens

## The design

There are no fixed seats. On every step, **each model independently produces a
position under all four lenses**, blind to the others. Only then do they
exchange and attack.

| | Methodology | Implementation | Adversarial audit | Fifth lens |
|---|---|---|---|---|
| **Claude** | ✓ | ✓ | ✓ | ✓ |
| **Codex** | ✓ | ✓ | ✓ | ✓ |
| **Kimi** | ✓ | ✓ | ✓ | ✓ |
| **Grok** | ✓ | ✓ | ✓ | ✓ |
| *Gemini* | optional | optional | optional | optional |

Sixteen independent positions per step from four models, then debate.

## Why this beats fixed seats

With one seat each, a disagreement is confounded: when the audit seat contradicts
the methodology seat you cannot tell whether that is a real conflict or just two
different jobs producing different emphases. Worse, a wrong seat assignment hides
a model's best insight — if Grok would have caught the collinearity but Grok was
assigned implementation, the catch never happens.

With the full matrix, every disagreement is **four models answering the same
question**. That is a signal you can act on. It also removes the need for
rotation entirely: nobody settles into a stance, because everybody argues every
position on every step.

The cost is roughly four times the invocations. For the stages that matter —
specification, gaps, analysis choice — that is worth paying. For mechanical
checklist work it is not; see the triage table below.

## The four lenses

Each model answers all four, in one turn, clearly separated by heading.

**1. Methodology.** Is the estimand right? Does the design answer the question
asked? Are the reporting standards met? Would a reviewer accept the inference the
design licenses?

**2. Implementation.** Would the code actually do what it claims? Is anything
silently degrading — a check that cannot fail, a filter excluding its own target,
a default swallowing an error? Is it reproducible from the stated inputs?

**3. Adversarial audit.** Assume the conclusion is wrong. What is the most likely
way it is wrong? What would have failed if it were? Attack the strongest version
of the claim, not a weak paraphrase.

**4. Fifth lens — clinical and publication reality.** Would a lipidologist
believe this? Does it change practice? Where does a hostile reviewer open? Is
anything over-claimed relative to what the numbers support?

## Round structure

**Round 1 — independent, blind.** Each model receives the step question, the
objection register and the transcript, but **not** the other models' round-1
output. Four turns, four models, all four lenses each. No cross-talk.

**Round 2+ — exchange and attack.** Each model now receives every other model's
positions and must engage specifically: name which position it disagrees with,
under which lens, and why. Filing no objection requires stating what was checked
and why it held.

**Close.** `bin/consensus.mjs` decides. Never a model, never the orchestrator.

## Where the full matrix earns its cost

| Stage | Protocol | Why |
|---|---|---|
| Project specification | **Full matrix** | Framing errors are the expensive ones |
| Requirements | Full matrix | Cheap relative to the cost of an omission |
| **Gaps / missing pieces** | **Full matrix — highest value** | Where every real defect in this project was found |
| Best-suited analyses | Full matrix | Genuine methodological disagreement |
| Explicit reasoning per choice | Full matrix | This is the record that survives peer review |
| TRIPOD / STROBE mapping | **One model, one pass** | Mechanical checklist; sixteen positions on a tick-box is theatre |
| Hallucination detection | Full matrix, bounded | Catches internal fabrication; cannot verify a published number |
| QC vs prior studies | One model + human | Bounded by literature access |

## The honest limit on hallucination detection

Cross-model disagreement reliably catches **internal** fabrication: invented
coefficients, numbers contradicting a state file, claims with no named artefact.
Four models each running an audit lens catches this far better than one.

It cannot establish that a published C-index is real. Four models can agree on a
wrong remembered number, and they will do so confidently. That check is human,
against the PDFs on disk. Extract comparator coefficients from those PDFs and
never from any model's memory — this project has already shipped comparator
functions carrying invented weights while their docstrings claimed published
provenance, and no amount of cross-model agreement would have caught it.

===== RESOURCE: open-questions.md =====
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

===== RESOURCE: DATA-INVENTORY.md (first 120 lines) =====
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


===== RESOURCE: STATUS.md =====
# Analysis status — which results are current, which are retracted

**Last updated: 13 August 2026.** Read this before using any number from this
repository. Several analyses here have been withdrawn and their documents are
retained for provenance, not for citation.

---

## Current — usable

| Analysis | Script | What it is |
|---|---|---|
| **CALON-F** | `code/15_CALON_FINAL.py` | Two-cohort **incident ASCVD** model in genotype-confirmed HeFH. Spec: age (+ spline) + sex + hypertension + T2DM + smoking + cumulative non-HDL-C + TG/HDL-C. Endpoint **ASCVD only** (I21/I25/I63/I70/I73/G45); I50 heart failure excluded. UK Biobank n=3,333 / 289 events, C=0.6997; All-Wales n=1,159 / 92 events, C=0.7486. Locked 13 August 2026. |
| CALON-F QC | `code/15b_QC_ADDENDUM.py` | Coefficient signs, completeness, calibration slope. |

CALON-F is the only analysis in this repository whose design makes temporal
leakage structurally impossible: events must be **dated after** baseline, and
participants with a pre-baseline event are excluded. It does not use the
mislabelled `prevalent_ascvd` field (see below), and no published score is an
input to it.

Head-to-head against Montreal-FH-SCORE, FH-Risk-Score and SAFEHEART-RE across 13
subgroups per cohort: **10 wins, 58 ties, 1 loss** of 69 estimable cells. The
single loss is UK Biobank diabetics vs SAFEHEART-RE (64 events, -0.062).

**Endpoint corrected 13 August 2026.** The composite `ascvd_first_date_best`
includes I50 heart failure, which is not atherosclerotic disease. 62 of 351
events in the broad version were heart-failure-only. Those participants are now
non-cases, censored at their recorded event date. This raised discrimination
(0.6940 -> 0.6996) and reintroduced one loss that the broad endpoint had masked.
The correct endpoint was preferred over the higher tally.

UK Biobank calibration slope is 1.214 (1.017, 1.411) — the interval no longer
covers 1, so predictions are somewhat too compressed. Stated limitation.

Two pre-specified rules govern which terms enter in each cohort. A spline term is
dropped where its correlation with age reaches 0.999 (fires on `sp18`, `sp30` in
UK Biobank only). A binary predictor is scored only where both levels hold at
least ten events, the same threshold used to report a stratum as non-estimable
(fires on `dm`, `smoke` in Wales only). Both are applied once per full cohort and
held fixed across every subgroup.

**BMI and HDL-C were REMOVED on 13 August 2026.** BMI had been added after the
UK Biobank diabetic subgroup was seen to lose, which is outcome-informed
selection. Once the endpoint was corrected to ASCVD-only, BMI and HDL-C
contributed nothing (UK Biobank 0.6996 -> 0.6997, Wales 0.7499 -> 0.7486, tally
unchanged at 10/58/1), so the model reverted to the pre-specified seven
variables. This removes the outcome-informed disclosure from the Methods and
raises Welsh EPV to 11.5.

**Cohorts: two, not three.** DRAGON is a complete subset of the All-Wales
registry - 424/424 records matched on `DatabaseNumber` - and contributes only 5
incident events, so it is not a separate cohort. Reporting it separately would
double-count the same patients.

**The one remaining loss** is UK Biobank diabetics vs SAFEHEART-RE (64 events,
-0.064). It was previously masked by 62 heart-failure-only events in the broad
endpoint. It is reported, not removed.

**Grey-zone enhancers** (`code/17_grey_zone_enhancers.py`): in the 5-20%
predicted 10-year risk band (n=1,685, 218 events), log(apoB/LDL-C) carries
HR 1.154 (1.027, 1.295) per SD but does NOT significantly improve
discrimination (delta C +0.0146, CI -0.0050 to +0.0330). Lp(a) adds nothing
(HR 1.033). UK Biobank only - Wales has no apoB and a different Lp(a) assay.

---

## Retracted — must not be cited as findings

### 1. The cross-sectional UK Biobank arm (CALON-N and CALON-W, prevalent design)

**Retracted 11 August 2026** for outcome-to-predictor temporality reversal.

Every prevalent-ASCVD event pre-dated the blood draw (median 6.6 years, IQR
3.8–11.6, maximum 55.6). `pre_lipid_source == "post_event_excluded"` was true for
100% of cases and 0% of non-cases, and `build_ukb`'s `pre_ldl.fillna(ldl_chem)`
silently restored exactly those excluded post-event, on-treatment lipid values.
The model did not predict the outcome; it detected the metabolic and treatment
consequences of it.

**Withdrawn quantities:** the 890-participant / 57-prevalent-event cohort, its 62
variant clusters, **AUC 0.7605**, **0.767**, **0.848**, **0.7672**, and the 15
UK Biobank head-to-head comparisons (5 wins, 9 ties, 1 loss). These must not
appear as results in any manuscript, abstract, figure, table or supplement.

The material remains legitimate as an explicitly labelled **methodological
negative** — a cross-sectional FH prediction analysis in which 100% of events
preceded biomarker measurement, and what that does to apparent discrimination.

Full record: `manuscript/TRIPOD_STROBE_PROBAST_CALON_W.md`, Section 1.

Independently, the same audit found **AUC 0.7605 to be seed-favourable**: across
ten cross-validation seeds the QC obtained 0.7497–0.7596, so the reported point
estimate sat above the entire distribution.

### 2. The FH-Risk-Score-updating architecture

**Withdrawn 13 August 2026.** Feeding a published score's linear predictor into a
new model, with ascertainment-specific baseline hazards, is disallowed by the
programme's binding rule and its premise was falsified by measurement. See
`FINAL_REPORT.md`.

### 3. Comparative decision-curve analysis

**Withdrawn at QC.** The comparators are ranking scores and linear predictors,
not calibrated probabilities on a common scale, so net benefit is not comparable
across them.

### 4. The apoB effect-modification result

**Withdrawn 10 August 2026** as tautological: log(apoB/LDL) = log apoB − log LDL,
so interacting the ratio with apoB places apoB on both sides.

---

## Documents that still contain retracted numbers

These carry a banner at the top. They are kept as the provenance record of what
was believed at the time, and are **not** submission drafts:


===== RESOURCE: step-002 QC brief =====
# Step 002 — QC of results and methodology, by all agents

**Protocol:** full matrix. Every model QCs every number and every method under
all four lenses, independently in round 1, then exchanges.

**Governance:** every figure below is aggregate. No participant data appears here
and none may be requested. Strata under 10 events are `<10, non-estimable`.

---

## What you are QC-ing

Two independent analyses of the same data disagree. One is a local Python
pipeline; the other is a Julius AI run from a written specification. **Your job
is to determine which numbers are trustworthy and which method is right — not to
split the difference.**

## A. Numbers that AGREE across both analyses

Treat these as probably sound, but say so only if you have checked the logic.

| Quantity | Value |
|---|---|
| UK Biobank LDLR carriers | 3,540 |
| Prevalent ASCVD excluded | 207 |
| Undated atherosclerotic cases excluded | 124 |
| Incident events, 5-year | 97 |
| Incident events, 10-year | 194 |
| Risk set after both exclusions | 3,209 |
| Minimum event-to-baseline lag | 1 day |
| Model C-index, UK Biobank | 0.698 vs 0.6997 |
| Montreal C-index, UK Biobank | 0.670 vs 0.6671 |
| Welsh registry / PASS / DRAGON | 7,253 / 7,253 / 424 (424/424 matched) |

Event-date completeness: I21 100%, I25 100%, I63 40.9%, I70 64.3%, I73 52.8%,
G45 37.0%. The endpoint is therefore coronary-weighted.

## B. Numbers that DISAGREE — the core of this QC

| Quantity | Local pipeline | Julius | Gap |
|---|---|---|---|
| **SAFEHEART C, UK Biobank** | **0.6944** | **0.628 / 0.635** | **−0.06** |
| **FH-Risk-Score C, UK Biobank** | **0.6740** | **0.651** | **−0.023** |
| **Wales at risk** | **1,159** | **1,059** | **−100, unexplained** |
| **Wales incident events** | **92** | not reported | missing |
| **Model C, Wales** | **0.7486** | 0.698 / 0.700 / 0.713 | −0.04 to −0.05 |
| **Carrier untreated LDL-C excess** | +0.15 median | +0.226 [0.185–0.268] | third value; spec said +0.55 |
| **Carriers ≥6.5 mmol/L** | ~1% | 2.1% [1.6–2.6] | 2× |

## C. The two claimed WINs, and why they are in doubt

Julius declares two wins at the 10-year horizon:

- SAFEHEART: model 0.707 vs 0.628, Δ **+0.079 [0.033, 0.123]** → WIN
- FH-Risk-Score: model 0.704 vs 0.651, Δ **+0.052 [0.001, 0.104]** → WIN

Substituting the local comparator values: SAFEHEART Δ becomes **+0.013**, FH-RS
Δ becomes **+0.030**. At the reported interval half-widths both cross zero and
become **TIEs**.

**The asymmetry is the tell.** Montreal — the only comparator needing neither
Lp(a) nor LDL-C bands — reproduces to 0.003, and Montreal is where a TIE was
declared. Every comparator that Julius scores *lower* than the local pipeline is
one where a WIN was declared.

## D. Methodological issues to adjudicate

1. **Uniform calibration-slope compression.** All four comparator slopes cluster
   at **0.52–0.57**. Three independently derived scores do not spontaneously
   agree on a ~2× compression of the linear predictor. Shared implementation
   error, or genuine?

2. **Age is null.** Age HR **1.20 [0.91–1.60]** for 5-year incident ASCVD, and
   cholesterol-years (= age × untreated total cholesterol) HR 1.15 [0.90–1.48] in
   the same model. Both null. The specification required a correlation check
   against age with a drop rule at ≥0.999; it was never reported.

3. **Grey-zone AUC 0.489 — below chance.** In the 5–10% predicted-risk band
   (n=234, 22 events) the model has no discriminative ability. This is the band
   where a risk score is supposed to earn its keep.

4. **Welsh O/E = 6.31.** Back-calculated, the model predicts ~3.2% 10-year risk
   in a genotype-confirmed FH registry against 6.13% observed in the LDLR-carrier
   cohort where it was built. It predicts *lower* risk in the higher-risk
   population. Candidate cause: median imputation fitted in UK Biobank folds then
   applied to Welsh predictors. No Welsh missingness table exists to test it.

5. **Strict-horizon Welsh construction.** "Event before horizon OR documented
   follow-up to horizon" admits everyone with an event while making event-free
   admission progressively harder. Event rate 7.4% (n=529, 5y) → 20.4% (n=289,
   10y) as the sample shrinks 45%.

6. **300 bootstrap replicates.** The FH-RS win has CI lower bound **0.001**. A
   2.5th percentile from 300 draws is the 7.5th order statistic — essentially one
   resample. Convention is ≥2,000.

7. **Deviations declared but unexamined:** ridge-**logistic** rather than Cox;
   median imputation rather than survival-aware MICE; SAFEHEART scored with its
   prior-ASCVD term identically zero in an incident-only cohort; FH-RS assigning
   Lp(a)=0 to the 22.5% missing.

## E. What was specified but not delivered

No Table 1. No standardised mean differences. No Kaplan–Meier curves, log-rank,
or Schoenfeld PH checks. No Fine–Gray. No leak detector, EPV, or convergence
counts. No comparator provenance table or coefficients. No calibration plot or
calibration-in-the-large. No subgroups. No PROBAST. No item-level TRIPOD/STROBE —
and 21 of 49 items graded "partly met" against an explicit instruction to mark
anything not met as NOT MET. No model equation, so nobody can apply the model.
Five named reproducibility artefacts are absent from disk.

---

## Your task, under each lens

**Methodology.** Which analysis has the right design? Is ridge-logistic
defensible where Cox was specified? Is the strict-horizon Welsh construction
sound?

**Implementation.** Diagnose the 0.52–0.57 slope cluster. Name the single most
likely bug and the test that would confirm it.

**Adversarial audit.** Assume both WINs are artefacts. What is the strongest
evidence for that, and what single computation would settle it?

**Clinical and publication reality.** With grey-zone AUC 0.489 and a
coronary-weighted endpoint, what can honestly be claimed? Where does a reviewer
open?

File every disagreement as an objection block in `state/open-questions.md`. An
objection whose `settled_by` is not a runnable test will be rejected by
`consensus.mjs`.

===== RESOURCE: 15_CALON_FINAL.py comparator/SPEC excerpts =====
70:SPEC = ["age", "sp18", "sp30", "sp50", "male", "htn_any", "dm", "smoke",
71-        "cum_nonhdl", "log_tghdl"]
72-
73-# CALON base specification, as originally specified by the investigator:
74-#   age, sex, hypertension, type 2 diabetes, smoking, cumulative non-HDL-C,
75-#   TG/HDL-C.  The spline terms are the functional form of AGE, not extra
76-#   variables; the collinearity guard drops any knot outside a cohort's range.
77-# BMI was REMOVED on 13 Aug 2026. It had been added after the diabetic subgroup
78-# was seen to lose, which is outcome-informed selection; reverting to the
79-# pre-specified set removes that vulnerability from the Methods.
80-# HDL-C was also removed - it is not in the specified set, and TG/HDL-C already
81-# carries HDL information.
82-# Lp(a) and log(apoB/LDL-C) are NOT in the base model. They are evaluated as
83-# GREY-ZONE RISK ENHANCERS in code/17_grey_zone_enhancers.py.
84-
85-# BMI: PROVENANCE OF THIS TERM, TO BE DISCLOSED IN THE METHODS.
86-# BMI was not in the originally specified variable set. It was added on
87-# 13 August 2026 AFTER the UK Biobank diabetic subgroup was found to lose to
88:# FH-Risk-Score (-0.050) and SAFEHEART-RE (-0.077). A within-subgroup diagnostic
89-# showed why: in diabetics every other term collapses toward chance (age 0.550,
90-# cumulative non-HDL 0.528) and hypertension reverses (0.469), while BMI is the
91-# only term that discriminates BETTER in diabetics than outside them
92:# (0.585 vs 0.547). SAFEHEART carries BMI; omitting it conceded that subgroup.
93-# Adding it resolves both losses (diabetics 0.5367 -> 0.5817, all three
94-# comparisons tie) at no cost elsewhere. Two alternatives were tested and
95-# rejected as ineffective: dm x age and dm x cumulative non-HDL, both of which
96-# left the losses intact.
97-# The sequence - loss observed, then variable added - is outcome-informed and
98-# must be reported as such. BMI is applied uniformly to both cohorts; no
99-# completeness rule was introduced, because one would have required a threshold
100-# close to Welsh BMI completeness (45.5%) for a gain of +0.0014 in Welsh C.
101-# Welsh BMI is 45.5% observed against 99.6% in UK Biobank, so the Welsh BMI
102-# coefficient is attenuated by median completion. This is a stated limitation.
103-
104-_s = importlib.util.spec_from_file_location(
105-    "vw", ROOT / "code" / "audit_2026_08_10" / "07_verify_welsh_prospective.py")
106-vw = importlib.util.module_from_spec(_s)
107-sys.modules["vw"] = vw
108-_s.loader.exec_module(vw)
109-
110-
111-# ----------------------------------------------------------------- cohorts
112-def corrected_root():
113-    """Locate the corrected-outcome data, preferring copies held ON THIS MAC.
114-
115-    The file lives in two places, verified byte-identical (md5
116-    ab364bc996c7a843c2f3b7f620dafbf0, 18,118,515 bytes): the synced Google Drive
117-    folder and the UnionSine external drive. Hard-coding the external path made
118-    the model unrunnable whenever that drive was unplugged. Resolution order:
119-    CALON_CORRECTED_DATA, then any local Google Drive copy, then UnionSine.
120-    """
121-    marker = Path("data_corrected") / "corrected_ascvd_outcomes.csv"
122-    cands = []
--
256:def comparators(d):
257-    """Published equations, scored not fitted. Never model inputs."""
258-    a, hdl, ml = d.age, d.hdl.fillna(1.35), d.male
259-    ht, sk = d.htn_any.fillna(0), d.smoke.fillna(0)
260-    ldl = pd.Series(d.ldl_unt, index=d.index).fillna(np.nanmedian(d.ldl_unt))
261-    lpa_hi = (d.lpa.fillna(0) >= 105).astype(float)
262-    bmi = d.bmi.fillna(d.bmi.median() if d.bmi.notna().any() else 27.0)
263-
264-    def ab(v):
265-        return (0 if v <= 30 else .938 if v <= 35 else 1.383 if v <= 40 else 1.621 if v <= 45
266-                else 1.738 if v <= 50 else 1.804 if v <= 55 else 1.964 if v <= 60 else 2.256)
267-
268-    lb = lambda v: (0 if v <= 5.5 else .315 if v <= 7.5 else .718 if v <= 8.5
269-                    else .918 if v <= 9.5 else 1.136)
270-    hb = lambda v: (0 if v > 1.30 else .298 if v >= 1.01 else .712 if v >= 0.85 else .752)
271-    return {
272:        "Montreal": np.asarray(0.75 * (a - a.mean()) / a.std()
273-                               - 0.27 * (hdl - hdl.mean()) / hdl.std()
274-                               + 0.25 * ml + 0.19 * ht + 0.12 * sk, float),
275-        "FH-RS": np.asarray([ab(v) for v in a] + np.array([lb(v) for v in ldl])
276-                            + np.array([hb(v) for v in hdl]) + 0.721 * ml + 0.644 * ht
277-                            + 0.625 * sk + 0.434 * lpa_hi, float),
278:        "SAFEHEART": np.asarray(0.045 * a + 0.6 * ml + 0.4 * ht + 0.3 * sk
279-                                + 0.02 * bmi + 0.15 * ldl + 0.25 * lpa_hi, float),
280-    }
281-
282-
283-# ------------------------------------------------------------------- model
284-def usable(df, feats):
285-    """F3 collinearity guard + F7 minimum-information rule + drop constants.
286-
287-    F7, pre-specified: a binary predictor is scored only where BOTH levels hold
288-    at least MIN_EVENTS events - the same threshold already used to report a
289-    stratum as non-estimable. This is mechanical, not a post-hoc choice: it
290-    drops `smoke` and `dm` in Wales (fewer than 10 events among smokers and
291-    among diabetics respectively, and `smoke` carries an implausible negative
292-    coefficient there) and drops nothing in UK Biobank, where every level holds
293-    79 events or more. Applied ONCE to the full cohort; the resulting spec is
294-    then held fixed across every subgroup, so no subgroup gets its own model.
295-    """
296-    out = []
297-    for f in feats:
298-        if f not in df or df[f].nunique(dropna=True) < 2:
299-            continue
300-        if f.startswith("sp") and abs(np.corrcoef(df.age, df[f])[0, 1]) >= 0.999:
301-            continue                                    # exact linear duplicate of age
302-        vals = set(pd.unique(df[f].dropna()))
303-        if vals <= {0.0, 1.0, 0, 1}:                    # binary -> minimum-information rule
304-            e1 = int(df.loc[df[f].eq(1), "E"].sum())
305-            e0 = int(df.loc[df[f].eq(0), "E"].sum())
306-            if min(e0, e1) < MIN_EVENTS:
307-                continue
308-        out.append(f)
--
426:          % ("subgroup", "ev", "C", "vs Montreal", "vs FH-RS", "vs SAFEHEART"))
427-    for label, mask in subgroups:
428-        s = d.loc[mask].reset_index(drop=True)
429-        yy, tt = s.E.to_numpy(int), s["T"].to_numpy(float)
430-        if yy.sum() < MIN_EVENTS:
431-            print("  %-16s %5s  <10 events, non-estimable" % (label, "<10"))
432-            tally["non_estimable"] += 3
433-            continue
434-        lp, ok, c, sd, fails, _ = cv(s, cohort_spec, resolve=False)
435-        cc = comparators(s)
436-        row = {"n": int(len(s)), "events": int(yy.sum()), "c_index": c,
437-               "repeat_sd": sd, "fold_failures": fails, "vs": {}}
438-        cells = []
439:        for cn in ("Montreal", "FH-RS", "SAFEHEART"):
440-            r = delta_ci(tt[ok], yy[ok], lp[ok], cc[cn][ok], s["cluster"].to_numpy()[ok])
441-            if r is None:
442-                cells.append("n/e".ljust(24)); tally["non_estimable"] += 1; continue
443-            dd, lo, hi = r
444-            v = "WIN" if lo > 0 else ("LOSS" if hi < 0 else "tie")
445-            tally[v] += 1
446-            row["vs"][cn] = {"delta": dd, "ci": [lo, hi], "verdict": v,
447-                             "comparator_c": float(concordance_index(tt, -cc[cn], yy))}
448-            cells.append(("%+.3f (%+.3f,%+.3f) %s" % (dd, lo, hi, v)).ljust(24))
449-        res["subgroups"][label] = row
450-        print("  %-16s %5d %8.4f | %s" % (label, yy.sum(), c, " ".join(cells)))
451-    res["tally"] = tally
452-    print("\n  %s TALLY:  WIN %d   tie %d   LOSS %d   non-estimable %d"
453-          % (name.upper(), tally["WIN"], tally["tie"], tally["LOSS"], tally["non_estimable"]))
454-    return res
455-
456-
457-def main():
458-    print("=" * 104)
459-    print("CALON-F  final two-cohort incident model")
460-    print("  spec:", " + ".join(SPEC))
461-    print("=" * 104)
462-    print("\nPRE-FLIGHT QC")
463-    U, W = build_ukb(), build_wales()
464-
465-    ukb_subs = [("ALL", U.index == U.index), ("male", U.male.eq(1)), ("female", U.male.eq(0)),
466-                ("age<median", U.age.lt(U.age.median())), ("age>=median", U.age.ge(U.age.median())),
467-                ("on statin", U.tx.eq(1)), ("no statin", U.tx.eq(0)),

===== RESOURCE: Spec Kit comparators.py =====
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

===== RESOURCE: outputs/calon_final.json headline aggregates =====
top_keys ['seed', 'spec', 'participant_level_outputs', 'ukb', 'wales', 'combined_tally']
ukb.qc.events: 289
ukb.qc.person_years: 45850.03148528405
ukb.qc.median_followup: 14.55441478439425
ukb.subgroups.ALL.events: 289
ukb.subgroups.ALL.c_index: 0.6997074817798635
ukb.subgroups.ALL.vs.Montreal.delta: 0.03300587661653287
ukb.subgroups.ALL.vs.FH-RS.delta: 0.02609731973472995
ukb.subgroups.ALL.vs.SAFEHEART.delta: 0.005781645591611095
ukb.subgroups.male.events: 175
ukb.subgroups.male.c_index: 0.6667995711614966
ukb.subgroups.male.vs.Montreal.delta: 0.040837121111436
ukb.subgroups.male.vs.FH-RS.delta: 0.03826763421138901
ukb.subgroups.male.vs.SAFEHEART.delta: 0.022770970114209255
ukb.subgroups.female.events: 114
ukb.subgroups.female.c_index: 0.6875151261894191
ukb.subgroups.female.vs.Montreal.delta: 0.017101517407088207
ukb.subgroups.female.vs.FH-RS.delta: 0.03660320196401057
ukb.subgroups.female.vs.SAFEHEART.delta: 0.008911175533443005
ukb.subgroups.age<median.events: 102
ukb.subgroups.age<median.c_index: 0.7297838153666375
ukb.subgroups.age<median.vs.Montreal.delta: 0.058958307249280084
ukb.subgroups.age<median.vs.FH-RS.delta: 0.021688368598973384
ukb.subgroups.age<median.vs.SAFEHEART.delta: 0.00031926881181920663
ukb.subgroups.age>=median.events: 187
ukb.subgroups.age>=median.c_index: 0.6530123234234436
ukb.subgroups.age>=median.vs.Montreal.delta: 0.02484300857400379
ukb.subgroups.age>=median.vs.FH-RS.delta: 0.03835954202453762
ukb.subgroups.age>=median.vs.SAFEHEART.delta: 0.01952429549399226
ukb.subgroups.on statin.events: 131
ukb.subgroups.on statin.c_index: 0.611929771801316
ukb.subgroups.on statin.vs.Montreal.delta: 0.012265589757910367
ukb.subgroups.on statin.vs.FH-RS.delta: 0.0045485790389449
ukb.subgroups.on statin.vs.SAFEHEART.delta: 0.00202994436448789
ukb.subgroups.no statin.events: 158
ukb.subgroups.no statin.c_index: 0.6907803281710915
ukb.subgroups.no statin.vs.Montreal.delta: 0.02977876106194688
ukb.subgroups.no statin.vs.FH-RS.delta: 0.028779037610619507
ukb.subgroups.no statin.vs.SAFEHEART.delta: 0.0017505530973451755
ukb.subgroups.diabetes.events: 64
ukb.subgroups.diabetes.c_index: 0.5592739043631642
ukb.subgroups.diabetes.vs.Montreal.delta: -0.024422864453102267
ukb.subgroups.diabetes.vs.FH-RS.delta: -0.03788451474094312
ukb.subgroups.diabetes.vs.SAFEHEART.delta: -0.0643716927371053
ukb.subgroups.no diabetes.events: 225
ukb.subgroups.no diabetes.c_index: 0.6872415608461728
ukb.subgroups.no diabetes.vs.Montreal.delta: 0.021304269166263268
ukb.subgroups.no diabetes.vs.FH-RS.delta: 0.013014657584929479
ukb.subgroups.no diabetes.vs.SAFEHEART.delta: -0.007557791762218824
ukb.subgroups.smoker.events: 140
ukb.subgroups.smoker.c_index: 0.6754868618722408
ukb.subgroups.smoker.vs.Montreal.delta: 0.04215445018939912
ukb.subgroups.smoker.vs.FH-RS.delta: 0.015337185832388633
ukb.subgroups.smoker.vs.SAFEHEART.delta: 0.0028644897282051884
ukb.subgroups.never smoked.events: 149
ukb.subgroups.never smoked.c_index: 0.710849567099567
ukb.subgroups.never smoked.vs.Montreal.delta: 0.025194013303769358
ukb.subgroups.never smoked.vs.FH-RS.delta: 0.02156121317706683
ukb.subgroups.never smoked.vs.SAFEHEART.delta: 0.004026765917009789
ukb.subgroups.hypertensive.events: 210
ukb.subgroups.hypertensive.c_index: 0.6410701865562064
ukb.subgroups.hypertensive.vs.Montreal.delta: 0.02250421181161999
ukb.subgroups.hypertensive.vs.FH-RS.delta: 0.03187529946367029
ukb.subgroups.hypertensive.vs.SAFEHEART.delta: 0.011517952364024198
ukb.subgroups.normotensive.events: 79
ukb.subgroups.normotensive.c_index: 0.7026625200001161
ukb.subgroups.normotensive.vs.Montreal.delta: 0.028303612652559873
ukb.subgroups.normotensive.vs.FH-RS.delta: 0.01644728245245708
ukb.subgroups.normotensive.vs.SAFEHEART.delta: -0.01286686238468171
ukb.tally.WIN: 10
ukb.tally.tie: 28
ukb.tally.LOSS: 1
ukb.tally.non_estimable: 0
wales.qc.events: 92
wales.qc.person_years: 6841.37234770705
wales.qc.median_followup: 4.005475701574264
wales.subgroups.ALL.events: 92
wales.subgroups.ALL.c_index: 0.748637172800255
wales.subgroups.ALL.vs.Montreal.delta: 0.012405710367184075
wales.subgroups.ALL.vs.FH-RS.delta: 0.0012571951042120721
wales.subgroups.ALL.vs.SAFEHEART.delta: 0.0230658936475282
wales.subgroups.male.events: 55
wales.subgroups.male.c_index: 0.7152329749103942
wales.subgroups.male.vs.Montreal.delta: -0.010948191593352918
wales.subgroups.male.vs.FH-RS.delta: -0.0065493646138807815
wales.subgroups.male.vs.SAFEHEART.delta: 9.775171065484756e-05
wales.subgroups.female.events: 37
wales.subgroups.female.c_index: 0.7527270468381165
wales.subgroups.female.vs.Montreal.delta: 0.020126723816623282
wales.subgroups.female.vs.FH-RS.delta: 0.012262392843831571
wales.subgroups.female.vs.SAFEHEART.delta: 0.030711889675736126
wales.subgroups.age<median.events: 21
wales.subgroups.age<median.c_index: 0.8327765404602823
wales.subgroups.age<median.vs.Montreal.delta: 0.003062360801781794
wales.subgroups.age<median.vs.FH-RS.delta: 0.03048440979955458
wales.subgroups.age<median.vs.SAFEHEART.delta: 0.02644766146993327
wales.subgroups.age>=median.events: 71
wales.subgroups.age>=median.c_index: 0.600243783520234
wales.subgroups.age>=median.vs.Montreal.delta: 0.03642125792296447
wales.subgroups.age>=median.vs.FH-RS.delta: -0.024622135543637236
wales.subgroups.age>=median.vs.SAFEHEART.delta: 0.027206240858117958
wales.subgroups.untreated.events: 91
wales.subgroups.untreated.c_index: 0.7487198574361056
wales.subgroups.untreated.vs.Montreal.delta: 0.012000631612190116
wales.subgroups.untreated.vs.FH-RS.delta: -0.0007669576594256933
wales.subgroups.untreated.vs.SAFEHEART.delta: 0.01707608671133065
wales.subgroups.no diabetes.events: 63
wales.subgroups.no diabetes.c_index: 0.7228779921307611
wales.subgroups.no diabetes.vs.Montreal.delta: 0.0
wales.subgroups.no diabetes.vs.FH-RS.delta: -0.003223961312464163
wales.subgroups.no diabetes.vs.SAFEHEART.delta: 0.0020279756642921365
wales.subgroups.never smoked.events: 73
wales.subgroups.never smoked.c_index: 0.725152281503236
wales.subgroups.never smoked.vs.Montreal.delta: 0.025085658345570305
wales.subgroups.never smoked.vs.FH-RS.delta: 0.003038831783325202
wales.subgroups.never smoked.vs.SAFEHEART.delta: 0.011543481807799072
wales.subgroups.hypertensive.events: 52
wales.subgroups.hypertensive.c_index: 0.5584976963296578
wales.subgroups.hypertensive.vs.Montreal.delta: -0.05559869544960405
wales.subgroups.hypertensive.vs.FH-RS.delta: -0.039291815499301164
wales.subgroups.hypertensive.vs.SAFEHEART.delta: -0.027178133250504777
wales.subgroups.normotensive.events: 40
wales.subgroups.normotensive.c_index: 0.7760972716488731
wales.subgroups.normotensive.vs.Montreal.delta: 0.021945432977461432
wales.subgroups.normotensive.vs.FH-RS.delta: 0.006376037959667791
wales.subgroups.normotensive.vs.SAFEHEART.delta: 0.025326215895610904
wales.tally.WIN: 0
wales.tally.tie: 30
wales.tally.LOSS: 0
wales.tally.non_estimable: 9
combined_tally.WIN: 10
combined_tally.tie: 58
combined_tally.LOSS: 1
combined_tally.non_estimable: 9
