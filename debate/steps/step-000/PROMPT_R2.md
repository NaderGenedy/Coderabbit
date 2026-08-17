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


--- STEP 000, ROUND 2 (EXCHANGE) ---
You previously wrote an independent Round-1 resource audit (blind). Below are
ALL four Round-1 returns. Engage specifically: name the agent, the claim, the
lens, and why you agree/disagree. Do not merely restate your Round-1 view.

Rules for this turn:
1. Answer ALL FOUR LENSES under the mandatory Markdown headings.
2. Attack the strongest opposing claims with evidence paths/numbers.
3. File new objections as ```objection blocks with next free ids starting at OBJ-004
   (do not reuse OBJ-001/002/003; those are step 001). Prefer step: 000 for resource-audit defects.
4. If you believe an objection is settleable only by code, put a minimal test/snippet
   under ## Artefacts.
5. Never declare consensus. Never invent coefficients.

--- STEP-000 BRIEF (context) ---
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


--- ALL POSITIONS, PREVIOUS ROUND (Markdown) ---


========== PRIOR ROUND · CLAUDE ==========

---
agent: claude
step: "000"
round: "1"
protocol: full-matrix-blind
status: round-1-complete
source: debate/steps/step-000/r1b/claude.txt
---

# Step 000 · Round 1 · CLAUDE

> Blind resource audit. This agent did **not** see other agents' outputs.
> Four lenses required: Methodology · Implementation · Adversarial · Clinical/publication.

# Step 000, Round 1 — Claude, independent and blind

---

## Preamble: what I actually received

The brief at `debate/steps/step-000` permits sixteen resources. **Nine were supplied to me; seven were not.** I will not pretend otherwise, because a resource audit conducted on an unstated subset is the exact failure shape this panel exists to catch.

| Permitted resource | Supplied? |
|---|---|
| `debate/DATA-INVENTORY.md` | Yes — **first 120 lines only** |
| `debate/mandates/AGENT.md`, `ROLES.md` | Yes |
| `debate/mandates/ORCHESTRATOR.md` | **No** |
| `debate/state/open-questions.md` | Yes |
| `debate/state/transcript.md`, `locked-decisions.md` | **No** |
| `debate/bin/panel.mjs`, `consensus.mjs` | **No** |
| `debate/steps/step-002-QC-BRIEF.md` | Yes |
| `code/15_CALON_FINAL.py` | Yes — **excerpts only** (lines 70–122, 256–308, 426–467) |
| `STATUS.md` | Yes — truncated mid-section |
| `README.md`, `outputs/calon_final_qc.json` | **No** |
| `CALON_JULIUS_SPECKIT/scripts/comparators.py` | Yes — **truncated inside `fhrs_chart_points`** |
| `tests/test_comparators.py`, `research.md`, `checklists/comparator-fidelity.md` | **No** |
| Comparator source PDFs | **No** — not located, not read, not cited below |

The single most consequential omission is `checklists/comparator-fidelity.md`. That file's name asserts it is the artefact that would settle OBJ-001, and it was not in the round-1 pack. **No coefficient, C-index or publication figure below is recalled from memory.** Every number I quote is traceable to a supplied path.

---

# 1. METHODOLOGY

## 1a. Resource ledger — what each source establishes, and what it does not

| Source | Establishes | Does **not** establish |
|---|---|---|
| `outputs/calon_final.json` | The tally arithmetic is internally exact: UKB 10+28+1 = 39 = 13 subgroups × 3 comparators, 0 non-estimable; Wales 0+30+0+9 = 39, i.e. 10 reported subgroups × 3 plus 3 subgroups skipped whole (`tally["non_estimable"] += 3`, line 432); `combined_tally` 10/58/1/9 = 78 = 2 × 13 × 3. Headline C-indices 0.6997 / 0.7486 and event counts 289 / 92 match `STATUS.md` exactly. | That any cell is *correct*. Internal arithmetic consistency is not validity. |
| `code/15_CALON_FINAL.py:256–280` | The exact functional form of the three scores that generate every WIN/tie/LOSS in the published tally. | That these are the published equations, despite the docstring at line 257 asserting "Published equations, scored not fitted." |
| `CALON_JULIUS_SPECKIT/scripts/comparators.py` | A second, structurally different implementation of the same three scores, with explicit indication limits in its docstrings. | Which of the two is faithful — the PDFs were not supplied. |
| `STATUS.md` | The retraction record, the BMI/HDL removal rationale, and the two pre-specified drop rules. | The provenance of the comparator weights, or that Wales is an external validation. |
| `DATA-INVENTORY.md` (120 lines) | Column names, ten named traps, cohort shapes. | The variant-curation rule behind `ldlr_carrier`. |
| `debate/state/open-questions.md` | OBJ-001/002/003 as live; OBJ-000 as ANSWERED. | That OBJ-000 was correctly closed — see §1e. |

## 1b. The estimand is not what the headline says it is

`STATUS.md` presents CALON-F as a **"Two-cohort incident ASCVD model"** with "UK Biobank n=3,333 / 289 events, C=0.6997; All-Wales n=1,159 / 92 events, C=0.7486". A reader — and a reviewer — will read that as development plus external validation.

It is not. `15_CALON_FINAL.py:434` calls `cv(s, cohort_spec, resolve=False)`, and `cohort_spec` is resolved **per cohort** by `usable()` (line 284), whose own docstring says the rule is "Applied ONCE to the full cohort". `STATUS.md` confirms the two specs differ: the spline rule "fires on `sp18`, `sp30` in UK Biobank only", the minimum-information rule "fires on `dm`, `smoke` in Wales only". So the UK Biobank model is fitted on 8 terms (10 − `sp18` − `sp30`) and the Welsh model on a **different** 8 terms (10 − `dm` − `smoke`). `STATUS.md`'s own EPV arithmetic corroborates this: 92 / 8 = 11.5, exactly the "Welsh EPV to 11.5" it reports.

**Two cohorts, two specifications, two internal cross-validations. There is no transported model anywhere in this pipeline.** C = 0.7486 in Wales is the apparent-minus-optimism performance of a Wales-refit model, not evidence that the UK Biobank model works in Wales. TRIPOD requires that distinction stated explicitly and it is absent from `STATUS.md`.

This also reframes the step-002 Table B row "Model C, Wales 0.7486 vs 0.698/0.700/0.713". If Julius **transported** the model (step-002 §D.4 describes "median imputation fitted in UK Biobank folds then applied to Welsh predictors", which is transport) whilst the local pipeline **refits**, then the two figures are not competing estimates of one quantity and the "−0.04 to −0.05" gap is not a discrepancy to adjudicate. It is the expected penalty for transport. The step-002 brief treats it as a disagreement; it may be a category error.

## 1c. Two of the three comparators are being scored outside their stated indication

This does not require the PDFs. It is stated in the project's own Spec Kit:

- `CALON_JULIUS_SPECKIT/scripts/comparators.py`, `montreal_fh_score` docstring: **"Original Montreal-FH-SCORE points; ranking/prevalent-CVD use only."**
- Same file, `combined_fh_score`: **"ranking/prevalent-CVD use only."**
- Same file, `fhrs_chart_points`: **"Published FH-Risk-Score chart points for adults aged 18-65."**

The local pipeline scores Montreal against **incident** ASCVD in every one of its 26 Montreal cells, and `ab()` at `15_CALON_FINAL.py:265–266` has an open top band (`else 2.256`) with no upper eligibility limit, applied to a cohort whose UK Biobank arm recruits to age 69 and whose median follow-up is 14.55 years (`ukb.qc.median_followup`).

The deltas in `calon_final.json` show where this bites. The Montreal column carries the largest deltas in the file — ALL +0.033, age<median +0.059, male +0.041, smoker +0.042 — whilst the SAFEHEART column is near-null throughout (ALL +0.0058, no-statin +0.0018, age<median +0.00032). **The wins are concentrated against the comparator that the project's own code says is not an incident-risk model.** A win over a score used outside its indication is not a win; it is a demonstration that a prevalent-CVD ranking instrument does not predict incident events, which nobody disputed.

## 1d. Whether the UK Biobank arm is FH at all is unresolved, and everything rests on it

`STATUS.md` describes CALON-F as a model in **"genotype-confirmed HeFH"**. Three supplied sources bear on that and they do not agree:

1. `DATA-INVENTORY.md`: `ldlr_carrier` = 1 in **3,540 of 501,936** = 0.705%.
2. `CLAUDE.md` project instructions, describing the other UK Biobank extract: `is_fh_genetic` = **1,623** of 426,732 = 0.380%, of which **LDLR 1,321**.
3. `open-questions.md`, OBJ-000 evidence: untreated LDL-C excess in flagged carriers **+0.226 mmol/L [0.185–0.268]**, with **2.1%** above 6.5 mmol/L, and `variant_id` empty in all 501,936 rows.

1,321 versus 3,540 LDLR carriers in the same biobank is a 2.7× difference with no documented reconciliation in any supplied resource. And +0.226 mmol/L is not a heterozygous-FH phenotype — OBJ-000's own settlement condition named "+3 to +4 mmol/L expected for heterozygous FH" as the benchmark.

There is an internal number in `calon_final.json` that corroborates this independently. Crude incidence:

- UK Biobank: 289 / 45,850.03 person-years = **0.630 per 100 py**
- Wales: 92 / 6,841.37 person-years = **1.345 per 100 py**

The Welsh registry cohort has **2.1× the event rate** of the UK Biobank "FH" arm — and the Welsh cohort is the younger one (median follow-up 4.01 years, and the Welsh data include childhood-onset ascertainment; the spline knots at ages 18 and 30 survive the collinearity guard in Wales and not in UK Biobank, which only happens if the Welsh age range extends well below 40). A younger cohort with double the atherosclerotic event rate is the signature of a genuinely higher-risk phenotype. The honest reading is that Wales is FH and the UK Biobank arm is a population-ascertained carrier cohort with a mild phenotype.

I record the fair alternative: Welsh events are registry-ascertained and UK Biobank events are linkage-ascertained, so ascertainment intensity could contribute. That is testable and is in my settlement condition below.

## 1e. The objection register has no state for "objection upheld", and that has already produced a wrong outcome

`open-questions.md` permits four statuses: `OPEN`, `ANSWERED`, `ACCEPTED-RISK`, `WITHDRAWN`. There is no state meaning *the test was run and the objection was correct*.

OBJ-000 claimed the carrier flag may not identify FH. Its `settled_by` named a specific comparison against +3 to +4 mmol/L. The test was run. The result was **+0.226 mmol/L** — a twentieth of the benchmark. The objection is marked **`status: ANSWERED`**.

The evidence field confirms the claim and the status field retires it. Whatever `consensus.mjs` does with an ANSWERED block, it is not "hold this step open" — and so the single most consequential question in the project has been recorded as disposed of by the measurement that established it. This is a defect in the debate's own instrument, which is exactly what step 000 is for.

## 1f. The three live settlement conditions are each necessary but not sufficient

- **OBJ-001** (kimi). The proposed test — score all three from the PDF coefficients on one frozen extract — is right. But the claim's framing treats the local values (SAFEHEART 0.6944, FH-RS 0.6740) as the reference against which Julius is deviating. `15_CALON_FINAL.py:256–280` and `CALON_JULIUS_SPECKIT/scripts/comparators.py` are structurally incompatible implementations of the same three scores (§2a), so the local values are not established as the reference. The substitution arithmetic in the claim ("+0.079 → +0.013") is therefore conditional on an unestablished premise. **Add to the settlement: a per-comparator statement of which of the two on-disk implementations the PDF supports, plus the eligibility counts (participants >65 for FH-RS; the indication statement for Montreal) and the units basis for LDL-C and Lp(a).**
- **OBJ-002** (grok). The centred/uncentred × 5y/10y grid is the right first move. But it cannot distinguish an implementation bug from genuine uniform attenuation, and there is a strong attenuation candidate: if the UK Biobank arm is a milder phenotype than the clinic-ascertained cohorts all three scores were derived in (§1d), every externally-weighted LP is over-scaled by roughly the same factor and every slope lands near the same value below 1. Note the direction check that supports this: `STATUS.md` reports the **model's** UK Biobank slope as **1.214 (1.017, 1.411)** — above 1 — whilst all four comparators sit at 0.52–0.57. A shared arithmetic bug in a common scoring pathway would not spare the internally fitted model. External weights being too large for this cohort would. **Add to the settlement: the analysis cohort's age range and SD against each derivation cohort's published age range, and the slope recomputed in the Welsh registry cohort. If the slopes move toward 1 in Wales, it is phenotype, not code.**
- **OBJ-003** (codex). The correlation and the refit are correct and must be run. But a null age HR has a second candidate cause that the proposed test will not separate: **outcome misclassification**. Step-002 §A lists 124 undated atherosclerotic cases excluded — `STATUS.md` reports n = 3,333, which is 3,540 − 207 and does **not** subtract them (§2d). 124 people with known atherosclerotic disease sitting in the risk set labelled event-free would attenuate every coefficient in the model, age included. **Add to the settlement: state the n actually analysed and the disposition of the 124, and refit with them excluded.**

---

# 2. IMPLEMENTATION

## 2a. Discrepancy ledger — the two comparator implementations are not the same functions

| Score | `code/15_CALON_FINAL.py:256–280` | `CALON_JULIUS_SPECKIT/scripts/comparators.py` |
|---|---|---|
| **Montreal** | Continuous, z-scored: `0.75·z(age) − 0.27·z(hdl) + 0.25·male + 0.19·htn + 0.12·smoke` | Integer points: age 0/4/8/12/16/20/24/28 by 7-year band; HDL 12/9/6/3/0 by band; `+2·htn +1·smoke +3·male` |
| **FH-RS** | 8 age bands (`ab`), 5 LDL bands (`lb`), 4 HDL bands (`hb`), `+0.721·male +0.644·htn +0.625·smoke +0.434·lpa_hi`; no eligibility limit | `fhrs_chart_points`, LDL in **mmol/L**, restricted to **ages 18–65** |
| **SAFEHEART** | Continuous linear: `0.045·age + 0.6·male + 0.4·htn + 0.3·smoke + 0.02·bmi + 0.15·ldl + 0.25·lpa_hi`; no prior-ASCVD term | Categorical: `0.70·male + 1.07·(30≤age<60) + 1.45·(age≥60) + 0.69·htn + 1.42·prior_ascvd + 0.48·smoke + 0.88/0.98·BMI bands + 0.92/1.57·LDL bands (**mg/dL**) + 0.42·(Lp(a)>50 mg/dL)`; baselines S₅=0.9532, S₁₀=0.9025; centring constant 5.4078 |

These cannot both be the published equation. Line 257's docstring — **"Published equations, scored not fitted"** — is a provenance claim, and `ROLES.md` warns in terms that "this project has already shipped comparator functions carrying invented weights while their docstrings claimed published provenance." The local SAFEHEART weights are 0.6, 0.4, 0.3, 0.25, 0.15, 0.02 and 0.045. Published Cox coefficients do not arrive as a set of round decimals across an entire model. The Spec Kit values (1.07, 1.45, 0.69, 1.42, 0.48, 0.88, 0.98, 0.92, 1.57, 0.42) have the irregular two-decimal texture of a transcribed table.

**This mechanism also predicts OBJ-001's asymmetry, in the right rank order.** Coarsening a continuous predictor into bands mechanically lowers a C-index. Ranking the three comparators by how much age granularity the local implementation retains relative to the published categorical form:

| Comparator | Local age handling | Published age handling | Predicted C gap | Observed gap (step-002 §B) |
|---|---|---|---|---|
| SAFEHEART | continuous `0.045·age` | **3 bands** — effectively one 60-year cutpoint within a 40–69 cohort | largest | **−0.066** |
| FH-RS | 8 bands (5-year) | chart bands | intermediate | **−0.023** |
| Montreal | continuous z-score | 7-year bands, monotone, age-dominant | smallest | **−0.003** |

The ordering is exact. OBJ-001 concludes "the asymmetry is not random" and it is right — but the asymmetry is equally consistent with the **local** comparators being unfairly strong continuous surrogates, not only with Julius understating them. Both directions must be tested; neither is currently established.

Two further fidelity breaks, both from the Spec Kit's own module docstring, which states these functions "do not impute, convert Lp(a) mass to molar units, extrapolate outside native eligibility":
- `15_CALON_FINAL.py:261` performs exactly the molar conversion the Spec Kit refuses (`lpa >= 105`, against the published 50 mg/dL threshold).
- `15_CALON_FINAL.py:279` applies `0.15 * ldl` where `ldl` is mmol/L, against published bands defined in mg/dL.

Two files in one repository take opposite positions on comparator fidelity and neither references the other.

## 2b. The collinearity guard is name-gated so that it cannot fire on the variable most likely to trip it

`15_CALON_FINAL.py:300`:

```python
if f.startswith("sp") and abs(np.corrcoef(df.age, df[f])[0, 1]) >= 0.999:
    continue                                    # exact linear duplicate of age
```

The specification at line 70 is `["age", "sp18", "sp30", "sp50", "male", "htn_any", "dm", "smoke", "cum_nonhdl", "log_tghdl"]`. `cum_nonhdl` is **cumulative** non-HDL-C — a lifetime-exposure construct, which is a function of age and a lipid level, structurally identical to the `age × untreated total cholesterol` term that OBJ-003 flags in the Julius model.

The guard tests correlation with age. `cum_nonhdl` does not begin with `sp`. **The guard is therefore incapable of firing on it, by construction.** The threshold compounds it: at ρ ≥ 0.999 the guard catches only exact linear duplicates, as its own inline comment concedes.

`STATUS.md` presents this as a substantive safeguard — "Two pre-specified rules govern which terms enter in each cohort. A spline term is dropped where its correlation with age reaches 0.999". It reads as collinearity control. It is a spline-basis housekeeping rule that removes knots outside a cohort's age range, and nothing more. **This is a check that cannot fail on the case that matters.** Age enters the UK Biobank model through `age`, `sp50` and `cum_nonhdl` — three routes — with no correlation reported between any pair.

## 2c. Comparator inputs are imputed asymmetrically against the model, using out-of-fold statistics

Lines 258–262:

```python
a, hdl, ml = d.age, d.hdl.fillna(1.35), d.male
ht, sk = d.htn_any.fillna(0), d.smoke.fillna(0)
ldl = pd.Series(d.ldl_unt, ...).fillna(np.nanmedian(d.ldl_unt))
lpa_hi = (d.lpa.fillna(0) >= 105).astype(float)
bmi = d.bmi.fillna(d.bmi.median() if d.bmi.notna().any() else 27.0)
```

Three separate problems:

1. **Missing risk factors are imputed to absent.** `htn_any.fillna(0)`, `smoke.fillna(0)`, `lpa.fillna(0)`. Every participant with unknown Lp(a) is scored as not-high. Step-002 §D.7 lists "FH-RS assigning Lp(a)=0 to the 22.5% missing" as a *Julius* deviation. Line 261 shows the local pipeline does the same thing. This is not a point of difference between the two analyses; it is a shared weakness that step-002's framing attributes to one side.
2. **The imputation statistics are computed on the scoring set.** `cc = comparators(s)` at line 435 passes the subgroup itself, so `np.nanmedian(d.ldl_unt)`, `d.bmi.median()`, `a.mean()`, `a.std()`, `hdl.mean()`, `hdl.std()` are all fitted on the same rows being scored, outside any fold structure. For a rank-based C-index a positive affine transform is harmless — I checked this and it holds — but it means "Montreal" is rescaled to each of the 26 subgroups it is evaluated in and is not a fixed score in any calibration sense.
3. **The asymmetry favours the model.** If `cv()` imputes within folds whilst comparators are constant-filled, the comparator is handicapped by design. Every WIN in `calon_final.json` was produced under this asymmetry.

## 2d. `STATUS.md` n = 3,333 contradicts the step-002 "agreed" risk set of 3,209

Step-002 §A lists under **"Numbers that AGREE across both analyses"**: carriers 3,540; prevalent ASCVD excluded 207; undated atherosclerotic cases excluded 124; **risk set after both exclusions 3,209**.

3,540 − 207 = **3,333**. 3,333 − 124 = **3,209**.

`STATUS.md` reports **"UK Biobank n=3,333 / 289 events"**. That is carriers minus prevalent only. The local pipeline's own status document says the second exclusion was not applied. So a number listed as *agreed between both analyses* is contradicted by one of them. The agreement was asserted, not demonstrated — a check that cannot fail, presented as a check that passed.

This is material, not clerical: the 124 are people with atherosclerotic disease of unknown date. Retained as non-cases they attenuate every coefficient, which is a live alternative explanation for OBJ-003's null age HR.

## 2e. An exact `0.0` where an exact zero should be impossible

`calon_final.json`: `wales.subgroups."no diabetes".vs.Montreal.delta: 0.0`.

Every other delta in the file is an irrational-looking float, including neighbours that are near-zero but not zero — `wales.male.vs.SAFEHEART: 9.775171065484756e-05`, `ukb."age<median".vs.SAFEHEART: 0.00031926881181920663`. A difference of two C-indices over 63 events, from two continuous scores, landing on exact binary zero to full double precision is a computational event, not a statistical one.

There is a specific candidate at line 258. Montreal contains `(hdl - hdl.mean()) / hdl.std()`. `DATA-INVENTORY.md` lists no HDL completeness figure for Wales, and `hdl.fillna(1.35)` replaces missing HDL with a **constant**. If HDL is wholly missing in that Welsh subgroup, `hdl` becomes constant, `hdl.std()` becomes 0, and the term becomes 0/0 → NaN across the whole vector. What `delta_ci` then returns is not visible in the excerpts I hold, but a degenerate path is the leading hypothesis and it is cheap to test.

## 2f. `comparator_c` and the delta are computed on different risk sets

Lines 440 and 447:

```python
r = delta_ci(tt[ok], yy[ok], lp[ok], cc[cn][ok], s["cluster"].to_numpy()[ok])
...
"comparator_c": float(concordance_index(tt, -cc[cn], yy))
```

The delta uses the `ok` mask; `comparator_c` uses the full subgroup. `ok` comes from `cv(...)` alongside `fails` (fold failures), so it is not guaranteed to be all-True. Any reader comparing a stored `comparator_c` against the stored `c_index` — which step-002 Table B does, quoting "local pipeline SAFEHEART 0.6944" — is comparing across two different denominators. The −0.06 gap that OBJ-001 is built on may be partly an artefact of which rows each figure was computed over.

The sign convention itself is correct: `concordance_index(tt, -cc[cn], yy)` negates the risk score so higher predicted survival aligns with longer time. I checked that and it holds.

## 2g. One seed, in a project with a documented seed-favourable retraction

`calon_final.json` top-level keys: `['seed', 'spec', 'participant_level_outputs', 'ukb', 'wales', 'combined_tally']` — a single seed.

`STATUS.md` records the precedent in its own retraction section: "the same audit found **AUC 0.7605 to be seed-favourable**: across ten cross-validation seeds the QC obtained 0.7497–0.7596, so the reported point estimate sat above the entire distribution."

A WIN verdict is a threshold crossing — `v = "WIN" if lo > 0` at line 444 — and several deltas sit within 3×10⁻⁴ of zero. A tally of 10/58/1 from one seed, in a pipeline with this exact documented failure mode, has not been shown to be stable. `repeat_sd` is stored per subgroup, so partial repeat structure exists; the tally itself has not been repeated.

Related, and worth one line: a **cross-validated** calibration slope of 1.214 (`STATUS.md`) is above 1, whereas CV slopes normally fall below 1 through optimism. Above 1 is the signature of over-shrinkage. If `cv()` is penalised, the penalty and its tuning are undisclosed in every resource I hold.

## 2h. A governance flag on the output artefact

`calon_final.json` contains a top-level key literally named **`participant_level_outputs`**. I do not know its contents and will not guess. Under UK Biobank Application 1002450 the standing rule is absolute — no participant-level rows or identifiers to disk. A key asserting participant-level output in a committed artefact must be established as benign before this repository is shared, and it takes one command.

---

# 3. ADVERSARIAL AUDIT

**Assume the headline is wrong. Assume CALON-F does not outperform published FH risk scores, and that 10/58/1 is manufactured.**

The most likely mechanism, in order of probability:

**First — the comparators are handicapped, not beaten.** Three independent handicaps stack in the same direction, all in `comparators()`:
- risk factors imputed to absent (`htn_any.fillna(0)`, `smoke.fillna(0)`, `lpa.fillna(0)`), whilst the model's missingness is handled inside `cv()`;
- Montreal scored against incident events despite its own Spec Kit docstring restricting it to prevalent-CVD ranking;
- FH-RS extrapolated past its published 18–65 eligibility into a cohort recruiting to 69.

Every one of these degrades the comparator only. None degrades the model. The wins concentrate exactly where the handicap is heaviest — the Montreal column carries the largest deltas in `calon_final.json` and Montreal is the score used furthest outside its indication.

**Second — the cohort is not FH, so no FH score should work in it.** UK Biobank carrier event rate is 0.630 per 100 py against 1.345 in Wales; untreated LDL-C excess is +0.226 mmol/L against the +3–4 that defines the phenotype; the carrier fraction is 0.705% against 0.380% in the project's other extract. If the UK Biobank arm is a mild population carrier cohort, then all three published scores — derived in clinic-ascertained FH — are attenuated there, uniformly, which is precisely OBJ-002's 0.52–0.57 cluster. On this reading CALON-F does not beat the comparators; it beats *transported* comparators in a population they were not built for, and would not beat them in real FH. Note the Welsh column, where a genuine FH registry is available: **0 WIN, 0 LOSS, 30 tie**. In the only cohort that is unambiguously FH, the model wins nothing.

**Third — the age signal is broken and nobody has looked.** The guard at line 300 cannot fire on `cum_nonhdl`; the 124 undated atherosclerotic cases appear to sit in the risk set as non-cases (§2d); and OBJ-003 reports age null at HR 1.20 [0.91–1.60]. Any one of these degrades the model's own age handling — which would make a *stronger* case that the model is under-performing than that it is over-performing, and is the one branch of this audit that could exonerate the tally.

**What would have failed if the conclusion were right?**

If CALON-F genuinely beat these scores, the Welsh column would not be 30/30 ties in the one true FH cohort; the wins would not be concentrated in the comparator with the worst indication fit; the comparator slopes would not cluster uniformly below 1 whilst the model's sits above 1; and the tally would survive a re-seed. **None of those four has been tested.** Every one of them is cheap.

**The single computation that settles the most.** Re-score all three comparators from the Spec Kit implementations — `CALON_JULIUS_SPECKIT/scripts/comparators.py`, which already exists on disk and already encodes the categorical forms and eligibility limits — on the identical frozen extract that produced `calon_final.json`, with **identical** missing-data handling for model and comparator, and re-run the tally over ten seeds. That one run tests OBJ-001's asymmetry, §2a's fidelity break, §2c's asymmetric imputation and §2g's seed stability simultaneously, and it needs no PDF and no new data.

---

# 4. CLINICAL AND PUBLICATION REALITY

**Would a lipidologist believe it?** Not as written, and the first thing they will check is the phenotype. A specialist reading "genotype-confirmed HeFH" (`STATUS.md`) and then finding an untreated LDL-C excess of +0.226 mmol/L with 2.1% above 6.5 mmol/L will conclude the UK Biobank arm is not their patients. Untreated LDL-C in clinic HeFH does not overlap the population distribution to that degree. The 2.1× event-rate gap against the Welsh registry says the same thing in outcome terms. A cohort labelled FH that behaves epidemiologically like the general population will not survive specialist review, and everything downstream — comparator performance, calibration slopes, the tally — inherits that.

**Does it change practice?** No, and the file says so. Step-002 §D.3: grey-zone AUC **0.489** on n = 234 / 22 events in the 5–10% band. `STATUS.md` on `code/17_grey_zone_enhancers.py`: log(apoB/LDL-C) HR 1.154 (1.027, 1.295) per SD but ΔC **+0.0146 (−0.0050, +0.0330)** — interval covers zero. And in `calon_final.json`, the subgroups where a clinician most needs help are where the model is weakest: `on statin` C = **0.612** (131 events), `diabetes` C = **0.559** (64 events), Welsh `hypertensive` C = **0.558** (52 events). A score at 0.56 in diabetics is not usable for triage. This is a marker, not a tool — `CLAUDE.md` §3 already uses exactly that phrase about the discordance chapter, and it applies here.

**Where does a hostile reviewer open?** In this order:

1. **"Show me the comparator provenance table."** There isn't one — step-002 §E lists it as specified-but-not-delivered — and when they diff `15_CALON_FINAL.py:256–280` against `CALON_JULIUS_SPECKIT/scripts/comparators.py` they will find two irreconcilable implementations under a docstring claiming published provenance. This ends the review.
2. **"Wales is a refit."** Once §1b is visible, the paper has no external validation and the 0.7486 headline goes.
3. **"Your tally counts the same patients seven times."** The 13 UK Biobank subgroups are ALL plus six complementary pairs, so every participant appears in 7 of 13 rows and the 39 cells are heavily dependent. There is no multiplicity control anywhere in `15_CALON_FINAL.py:426–454`. Under 39 correlated tests at 95%, a handful of WINs is the null expectation. "10 wins, 58 ties, 1 loss" is a headline the design cannot support.
4. **"Wales won nothing."** 0 WIN / 0 LOSS / 30 tie. `STATUS.md` blends this into a combined "10 wins, 58 ties, 1 loss" without stating that **all ten wins are UK Biobank** and the Welsh comparison is powerless at 92 events.
5. **Endpoint composition.** Step-002 §A: event-date completeness I21 100%, I25 100%, **I63 40.9%, I70 64.3%, I73 52.8%, G45 37.0%**. The endpoint is coronary-weighted by ascertainment, so "ASCVD" overstates what was measured. `STATUS.md` states the I50 exclusion correction but not the differential dating completeness.
6. **Two numbers for one cell in one document.** `STATUS.md` reports the single loss as **−0.062** in one paragraph and **−0.064** in another. `calon_final.json` gives `ukb.subgroups.diabetes.vs.SAFEHEART.delta: −0.0643716927371053`. The −0.062 is wrong. Trivial in itself; a reviewer reads it as numbers being typed from memory rather than read from artefacts, and then audits everything else.

**What can honestly be claimed today?** That in a cohort of UK Biobank LDLR variant carriers and an All-Wales FH registry, a pre-specified seven-variable model achieves cross-validated C of 0.70 and 0.75 respectively, with performance falling to 0.56–0.61 in treated and diabetic strata and no discrimination in the 5–10% grey zone; and that it was **not distinguishable** from three published FH scores in the Welsh registry across all 30 estimable cells. The UK Biobank comparator results should be held back entirely until §2a is resolved. `STATUS.md`'s own standing rule — "Concede the weak link first" (`CLAUDE.md` §4) — points the same way.

**On self-consistency, where I checked and found no problem:** the tally arithmetic reconciles exactly (78 = 2 × 13 × 3); C-indices and event counts in `STATUS.md` match `calon_final.json` to the digit; the EPV arithmetic (92/8 = 11.5) confirms the stated Welsh spec; the endpoint-correction narrative (62 of 351 heart-failure-only) matches `DATA-INVENTORY.md` trap 3; and `STATUS.md`'s reading of calibration slope 1.214 as "predictions somewhat too compressed" is directionally correct. The arithmetic is sound. The provenance is not.

---

# Evidence still required before OBJ-001, OBJ-002 and OBJ-003 can close

| Objection | Present settlement condition | What must be added before it can close |
|---|---|---|
| **OBJ-001** | Score all three from PDF coefficients on one frozen extract; publish provenance table | (a) Which of the two on-disk implementations the PDF supports, per comparator; (b) count of participants aged >65 (FH-RS eligibility); (c) statement of Montreal's indication against an incident endpoint; (d) units basis for LDL-C and Lp(a) in each; (e) identical missing-data handling for model and comparators; (f) `ok.sum()` vs `len(s)` per subgroup, since `comparator_c` and the delta currently use different risk sets |
| **OBJ-002** | Recompute one comparator centred/uncentred × 5y/10y baseline | (a) Cohort age range and SD against each derivation cohort's published range; (b) the same slopes recomputed in the Welsh registry — if they move toward 1 there, it is phenotype not code; (c) confirmation of whether the slope was computed on the published categorical LP or a continuous surrogate |
| **OBJ-003** | Pearson r(age, cholesterol-years); refit with untreated TC alone | (a) The same correlation for `cum_nonhdl` in the local model, since the guard at `15_CALON_FINAL.py:300` cannot fire on it; (b) the n actually analysed and the disposition of the 124 undated atherosclerotic cases — retained as non-cases they attenuate age independently of any collinearity; (c) age's HR refit after excluding them |

**None of the three can close on the resources supplied to round 1.** The PDFs were not located, and `checklists/comparator-fidelity.md` — the artefact whose name says it settles OBJ-001 — was not in the pack.

---

# Proposed objection blocks

Text only, not written to file. **Numbering collision warning:** round 1 is blind and parallel, so four agents will independently propose `OBJ-004`. The register requires globally unique ids and nothing in the supplied materials allocates ranges. The orchestrator must renumber on merge; I have kept the schema form rather than namespacing, because a namespaced id may not parse.

```objection
id: OBJ-004
step: 000
raised_by: claude
claim: The comparator functions at code/15_CALON_FINAL.py:256-280 are structurally different functions from those at CALON_JULIUS_SPECKIT/scripts/comparators.py for all three scores, yet line 257 asserts "Published equations, scored not fitted". Local SAFEHEART is continuous linear (0.045*age + 0.6*male + 0.4*htn + 0.3*smoke + 0.02*bmi + 0.15*ldl + 0.25*lpa_hi, LDL in mmol/L, no prior-ASCVD term); Spec Kit SAFEHEART is categorical with 3 age bands, 3 BMI bands, 3 LDL bands in mg/dL, a 1.42 prior-ASCVD term and baseline survivals 0.9532/0.9025. Local Montreal is a z-scored continuous LP; Spec Kit Montreal is an integer points chart. These cannot both be the published equation. Every WIN, tie and LOSS in outputs/calon_final.json was generated by the local version. The degree of age coarsening in the published forms predicts the OBJ-001 gaps in exact rank order (SAFEHEART 3 bands, gap -0.066; FH-RS chart bands, -0.023; Montreal 7-year bands, -0.003), so the local values may be inflated surrogates rather than Julius understating.
settled_by: For each of Montreal, FH-RS and SAFEHEART, state which on-disk implementation the source PDF supports, citing page and table. Then re-run code/15_CALON_FINAL.py substituting CALON_JULIUS_SPECKIT/scripts/comparators.py and report the revised combined_tally against the current 10/58/1.
status: OPEN
```

```objection
id: OBJ-005
step: 000
raised_by: claude
claim: The collinearity guard at code/15_CALON_FINAL.py:300 is gated on f.startswith("sp"), so it cannot fire on cum_nonhdl, which as a cumulative age-by-lipid exposure is the term most likely to be collinear with age - structurally the same construct as the cholesterol-years term in OBJ-003. The threshold of 0.999 catches only exact linear duplicates, as the inline comment concedes. STATUS.md presents this as one of two pre-specified rules governing which terms enter, which reads as collinearity control; it is spline-basis housekeeping that removes knots outside a cohort's age range. Age enters the UK Biobank model through age, sp50 and cum_nonhdl with no pairwise correlation ever reported.
settled_by: Report Pearson r(age, cum_nonhdl) in both cohorts. Refit CALON-F with cum_nonhdl replaced by non-HDL-C alone and report the age coefficient, its 95% CI, and the ALL C-index in each cohort against the current 0.6997 and 0.7486.
status: OPEN
```

```objection
id: OBJ-006
step: 000
raised_by: claude
claim: The Welsh C-index of 0.7486 is internal cross-validation of a Wales-refitted model, not external validation. code/15_CALON_FINAL.py:434 calls cv(s, cohort_spec) with cohort_spec resolved per cohort by usable(), and STATUS.md confirms the specs differ (spline rule fires in UK Biobank only, minimum-information rule in Wales only), giving 8 different terms in each cohort - corroborated by STATUS.md's own Welsh EPV of 11.5 = 92/8. No transported model exists anywhere in this pipeline, so CALON-F has no demonstrated transportability. This also means the step-002 Table B row "Model C, Wales 0.7486 vs 0.698/0.700/0.713" may not be a discrepancy at all: if Julius transported UK Biobank coefficients (step-002 section D.4 describes UK-Biobank-fitted imputation applied to Welsh predictors) whilst the local pipeline refits, the two figures estimate different quantities and the gap is the expected transport penalty.
settled_by: Freeze the UK Biobank coefficient vector, apply it unchanged to the Welsh cohort with no refitting, and report Welsh C-index, calibration slope and calibration-in-the-large. Report the two cohort specifications side by side, naming every term in each.
status: OPEN
```

```objection
id: OBJ-007
step: 000
raised_by: claude
claim: STATUS.md reports the UK Biobank analysis as n=3,333, which equals 3,540 carriers minus 207 prevalent ASCVD and does not subtract the 124 undated atherosclerotic cases. Step-002 section A lists "Risk set after both exclusions 3,209" under numbers that AGREE across both analyses. 3,540-207=3,333 and 3,333-124=3,209, so a figure recorded as agreed is contradicted by the local pipeline's own status document. This is material, not clerical: 124 participants with atherosclerotic disease of unknown date retained as non-cases attenuate every coefficient, and are an untested alternative explanation for the null age HR in OBJ-003 that the OBJ-003 refit will not distinguish from collinearity.
settled_by: Print the analysis n actually used by code/15_CALON_FINAL.py after all exclusions and state the disposition of the 124 undated cases. If retained, refit with them excluded and report the age HR with 95% CI and the ALL C-index against the current 0.6997.
status: OPEN
```

```objection
id: OBJ-008
step: 000
raised_by: claude
claim: outputs/calon_final.json records wales.subgroups."no diabetes".vs.Montreal.delta as exactly 0.0 whilst every neighbouring cell is an irrational-looking float, including near-zero ones (wales male vs SAFEHEART 9.775171065484756e-05; ukb age<median vs SAFEHEART 0.00031926881181920663). A difference of two C-indices over 63 events from two continuous scores cannot land on exact binary zero by chance. The leading candidate is code/15_CALON_FINAL.py:258, where d.hdl.fillna(1.35) replaces missing HDL with a constant: if HDL is wholly missing in that Welsh subgroup, hdl.std() is 0, the Montreal z-term becomes 0/0 = NaN across the vector, and the comparator is degenerate. Separately, line 447 computes comparator_c on the full subgroup (tt, yy) whilst line 440 computes the delta on the ok mask, so the two stored quantities use different risk sets - and step-002 Table B quotes the stored local comparator C-indices as the reference for OBJ-001.
settled_by: For the Welsh no-diabetes subgroup, print HDL non-missing count, hdl.std() after fillna, and the model and Montreal C-indices to six decimal places. Separately print ok.sum() against len(s) and fold_failures for every subgroup in both cohorts, and recompute comparator_c restricted to ok.
status: OPEN
```

```objection
id: OBJ-009
step: 000
raised_by: claude
claim: The 10/58/1 tally rests on a single seed (outputs/calon_final.json top-level key "seed"), in a project where STATUS.md documents this exact failure mode: AUC 0.7605 was found seed-favourable, with ten cross-validation seeds giving 0.7497-0.7596 so that the reported point estimate sat above the entire distribution. A verdict is a threshold crossing (code/15_CALON_FINAL.py:444, v = "WIN" if lo > 0) and several deltas sit within 3e-04 of zero. Additionally, the 13 UK Biobank subgroups are ALL plus six complementary pairs, so every participant appears in 7 of 13 rows and the 39 cells are heavily dependent, with no multiplicity control anywhere in lines 426-454. Separately, a cross-validated calibration slope of 1.214 is above 1 where CV optimism normally puts it below 1, which is the signature of over-shrinkage; no penalty or tuning procedure is disclosed in any supplied resource.
settled_by: Re-run code/15_CALON_FINAL.py over at least ten seeds and report the distribution of combined_tally WIN, tie and LOSS counts, plus the seed-to-seed range of the ALL C-index in each cohort. Report the number of bootstrap replicates used by delta_ci, and the penalty type and tuning procedure used by cv().
status: OPEN
```

```objection
id: OBJ-010
step: 000
raised_by: claude
claim: Two of the three comparators are scored outside the indication stated by the project's own code. CALON_JULIUS_SPECKIT/scripts/comparators.py documents montreal_fh_score as "ranking/prevalent-CVD use only" and fhrs_chart_points as "for adults aged 18-65", and its module docstring states these functions do not impute, convert Lp(a) mass to molar units, or extrapolate outside native eligibility. code/15_CALON_FINAL.py scores Montreal against incident ASCVD in all 26 Montreal cells; its ab() function at lines 265-266 has an open top band applied to a cohort recruiting to age 69; line 261 performs the molar Lp(a) conversion the Spec Kit refuses; line 279 applies a per-mmol/L LDL coefficient against published mg/dL bands. The Montreal column carries the largest deltas in outputs/calon_final.json (ALL +0.033, age<median +0.059, male +0.041, smoker +0.042) whilst SAFEHEART is near-null throughout (ALL +0.0058), so the wins concentrate where the indication mismatch is worst. Beating a prevalent-CVD ranking score on an incident endpoint is not evidence of superiority.
settled_by: Count UK Biobank analysis participants aged over 65 at baseline and report what fraction of FH-RS cells that represents. State each comparator's published endpoint, horizon and derivation cohort in a provenance table. Re-run the tally excluding cells where a comparator is applied outside its published indication and report the revised combined_tally.
status: OPEN
```

```objection
id: OBJ-011
step: 000
raised_by: claude
claim: The UK Biobank arm may not be familial hypercholesterolaemia, and STATUS.md's description of CALON-F as a model in "genotype-confirmed HeFH" may be false for that cohort. Three supplied sources conflict: DATA-INVENTORY.md gives ldlr_carrier = 3,540 of 501,936 (0.705%); CLAUDE.md gives is_fh_genetic = 1,623 of 426,732 (0.380%) of which LDLR 1,321 - a 2.7-fold difference in LDLR count for the same biobank with no documented reconciliation and no variant-curation rule stated anywhere. Two independent internal measurements support the milder reading: untreated LDL-C excess of +0.226 mmol/L against the +3 to +4 that defines the phenotype, and crude incidence computed from outputs/calon_final.json of 0.630 per 100 person-years in UK Biobank (289/45,850.03) against 1.345 in the Welsh registry (92/6,841.37) - a 2.1-fold higher rate in the younger cohort. If UK Biobank carriers are a mild population cohort rather than clinic-ascertained FH, then all three externally weighted comparators are uniformly attenuated there, which is a single non-bug explanation for the 0.52-0.57 slope cluster in OBJ-002; note that the internally fitted model's slope is 1.214, above 1, which a shared arithmetic bug in a common scoring pathway would not spare.
settled_by: Publish the variant-curation rule behind ldlr_carrier - filter criteria, ACMG classes included, and counts by class - and reconcile 3,540 against the 1,321 in CLAUDE.md. Report age-standardised incidence in both cohorts to test whether the 2.1-fold rate gap survives age adjustment, and report each cohort's ascertainment route for events. Recompute all four comparator calibration slopes in the Welsh cohort: if they move from 0.52-0.57 toward 1.0 there, the cause is phenotype, not implementation.
status: OPEN
```

```objection
id: OBJ-012
step: 000
raised_by: claude
claim: The objection register has no status meaning "tested and upheld", and this has already produced a wrong disposition. OBJ-000 claimed the carrier flag may not identify FH; its settled_by named a comparison against the +3 to +4 mmol/L expected for heterozygous FH; the measurement returned +0.226 mmol/L [0.185-0.268] with 2.1% above 6.5 mmol/L and variant_id empty in all 501,936 rows. That result confirms the claim. The block is marked status: ANSWERED, which retires it. The permitted statuses are OPEN, ANSWERED, ACCEPTED-RISK and WITHDRAWN, so an objection proven correct has nowhere to go except ACCEPTED-RISK with a named dissenter. Separately, the schema requires globally unique OBJ-NNN ids whilst round 1 is blind and parallel across four agents, guaranteeing id collisions on merge with no documented allocation rule.
settled_by: Run bin/consensus.mjs against the current register and report whether OBJ-000 in its ANSWERED state permits or blocks closure of any step. Add a status meaning UPHELD, or reclassify OBJ-000 as ACCEPTED-RISK with a named dissenter and risk text, then re-run and report the change in closure decisions. Publish the id-allocation rule for blind parallel rounds and confirm bin/panel.mjs enforces it.
status: OPEN
```


========== PRIOR ROUND · CODEX ==========

---
agent: codex
step: "000"
round: "1"
protocol: full-matrix-blind
status: round-1-complete
source: debate/steps/step-000/r1b/codex.txt
---

# Step 000 · Round 1 · CODEX

> Blind resource audit. This agent did **not** see other agents' outputs.
> Four lenses required: Methodology · Implementation · Adversarial · Clinical/publication.

## 1. METHODOLOGY

The evidence package does not yet support adjudicating model superiority. It mixes different cohorts, horizons, metrics, and validation designs, while several required primary artefacts are absent.

### Resource ledger

| Evidence examined | What it establishes | What it does not establish |
|---|---|---|
| `debate/DATA-INVENTORY.md`, “Files,” cohort columns, and “Traps” | Aggregate source dimensions, intended outcome sources, genotype flags, date-parsing hazards, and endpoint exclusions | Lipid units, missingness by analysis cohort, actual derivation code, or which file/hash a run selected |
| `debate/mandates/ROLES.md`, especially “Round structure” and “honest limit” | Independent full-matrix protocol and requirement for PDF-based comparator verification | That `panel.mjs` or `consensus.mjs` implements those rules |
| `debate/state/open-questions.md`, schema and OBJ-001–003 | Valid objection schema and the three unresolved scientific disputes | Evidence resolving any dispute |
| `debate/steps/step-002-QC-BRIEF.md`, sections A–E | The claimed agreements, discrepancies, omitted reporting items, and competing analysis designs | Primary execution logs or proof that either analysis produced those numbers correctly |
| `STATUS.md`, “Current—usable” and “Retracted” | The repository’s declared current and withdrawn findings | A reproducible run manifest; `STATUS.md` is a claim document, not validation evidence |
| `code/15_CALON_FINAL.py`, `SPEC`, `comparators()`, `usable()`, and subgroup loop | Actual comparator transformations and the visible path used for subgroup evaluation | The omitted cohort builders, `cv()`, `delta_ci()`, censoring implementation, file-hash checks, and output writer |
| `CALON_JULIUS_SPECKIT/scripts/comparators.py`, module contract, SAFEHEART, and Montreal functions | A second, materially different comparator implementation that rejects missing inputs | Full FH-RS implementation, correspondence with source PDFs, or test coverage |
| `outputs/calon_final.json`, supplied aggregate excerpt | Events, person-time, C-indices, subgroup deltas, and tally | Cohort sizes, confidence intervals, fold failures, configuration, hashes, or the contents of `participant_level_outputs` |

The supplied packet did not contain the bodies of `debate/mandates/AGENT.md`, `ORCHESTRATOR.md`, `debate/state/transcript.md`, `locked-decisions.md`, `debate/bin/panel.mjs`, `consensus.mjs`, `README.md`, `outputs/calon_final_qc.json`, `CALON_JULIUS_SPECKIT/tests/test_comparators.py`, `research.md`, `checklists/comparator-fidelity.md`, or any comparator PDF. The displayed `DATA-INVENTORY.md`, `15_CALON_FINAL.py`, `STATUS.md`, `comparators.py`, and JSON were also excerpts. I therefore could not verify parser behaviour, QC conditions, source fidelity, or complete execution paths.

### Estimand and design defects

The current materials conflate at least three estimands:

- `STATUS.md` describes full follow-up survival discrimination in 3,333 participants with 289 events.
- `debate/steps/step-002-QC-BRIEF.md`, section A, describes a 3,209-person risk set after another 124 exclusions, with 97 five-year and 194 ten-year events.
- The Julius analysis uses ridge logistic regression at strict horizons, whereas `code/15_CALON_FINAL.py` visibly evaluates time-to-event concordance.

A full-follow-up Harrell C-index cannot simply replace a ten-year fixed-horizon AUC or C-statistic. The proposed substitution behind the two disputed WINs is diagnostic, not conclusive, unless comparator values are recomputed on the identical 3,209-person risk set with the identical endpoint, horizon, and metric.

The incident design is methodologically preferable to the retracted prevalent analysis described in `STATUS.md`; exclusion of pre-baseline disease and heart failure from ASCVD addresses real leakage and endpoint contamination. That does not establish external validation. The visible subgroup loop calls `cv(s, cohort_spec, resolve=False)` separately for every subset at `code/15_CALON_FINAL.py:427-435`. If `cv()` fits models—as its name and returned predictions suggest—these are internally validated subgroup-specific fits, not performance of one fixed CALON-F model. Wales likewise cannot be called external validation unless UK-derived coefficients, preprocessing, and baseline hazard are frozen before Welsh application.

The Julius strict-horizon rule—retain every event before the horizon but retain event-free participants only if observed through the horizon—is a complete-case design vulnerable to informative censoring. Rising event prevalence while the sample contracts is exactly the expected warning. A Cox model, IPCW binary analysis, or another censoring-aware fixed-horizon method is required. Ridge logistic regression is not inherently indefensible, but this selection rule does not satisfy the Cox estimand that was specified.

Endpoint inference must also be narrowed. `debate/steps/step-002-QC-BRIEF.md`, section A, reports complete dating for coronary components but only 37.0%–64.3% for several cerebrovascular/peripheral components. The estimand is therefore dated, coronary-weighted ASCVD—not uniformly ascertained pan-ASCVD.

Reporting standards are not met on the supplied record. Section E of the QC brief reports no Table 1, participant flow, standardised differences, Kaplan–Meier plots, PH diagnostics, model equation, calibration plot, PROBAST assessment, or compliant item-level TRIPOD/STROBE mapping.

## 2. IMPLEMENTATION

The strongest implementation defect is not subtle: the two comparator implementations cannot both be source-faithful.

### Discrepancy ledger

| Conflict | Evidence | Consequence |
|---|---|---|
| Montreal is called a published equation but depends on the validation sample | `code/15_CALON_FINAL.py`, `comparators():272-274`, standardises age and HDL using `a.mean()`, `a.std()`, and corresponding HDL moments; the Spec Kit’s `montreal_fh_score()` uses fixed integer point bands | The same person can receive a different relative score when evaluated in a subgroup. This is fitted preprocessing, not a fixed published score |
| SAFEHEART formulae differ structurally | Local `comparators():278-279` uses continuous age, BMI and LDL terms plus an Lp(a) threshold of 105; Spec Kit `safeheart_linear_predictor()` uses categorical age, BMI and LDL bands and an Lp(a) threshold expressed as 50 mg/dL | At least one implementation is not the claimed published equation. Units and mapping cannot be recovered from the supplied evidence |
| Missingness handling directly contradicts the strict comparator contract | Local code fills HDL with 1.35, hypertension/smoking/Lp(a) with zero, and LDL/BMI with subset-specific medians at `comparators():258-262`; the Spec Kit module says it does not impute | Missingness can systematically depress or reorder comparator scores, particularly the two comparators implicated in the disputed WINs |
| Comparator scoring changes by subgroup | `comparators(s)` is called after slicing at `code/15_CALON_FINAL.py:428-435` | Subgroup C-indices do not evaluate a single frozen comparator transformation |
| “No subgroup gets its own model” is not demonstrated by the code shown | Comment at `code/15_CALON_FINAL.py:293-294`; fresh `cv(s, ...)` call at line 434 | A fit-count test is needed; prose does not establish prediction reuse |
| Constant predictors may enter subgroup fits | `usable()` drops constants when resolving a cohort, but subgroup calls use `resolve=False`; sex, diabetes, hypertension, or smoking are constant in their defining strata | The omitted `cv()` body must show whether constants cause failures, silent dropping, or unstable scaling. `fold_failures` exists but was omitted from the aggregate excerpt |
| The advertised collinearity guard is narrow | `usable():300-301` tests only fields beginning with `sp` against age | It does not test cumulative lipid exposure or other continuous predictors; it cannot resolve OBJ-003 |
| Input provenance is machine-dependent in the visible resolver | `corrected_root():112-121` describes environment/path precedence and a historical MD5 assertion, while `DATA-INVENTORY.md` identifies `SHA256SUMS.txt` as authoritative | Without a runtime digest assertion, path precedence can silently select a stale copy |
| Current-status loss differs internally | `STATUS.md` first reports the diabetic SAFEHEART loss as −0.062, later as −0.064; `outputs/calon_final.json` gives −0.0643716927 | At three decimals, the reproducible value is −0.064. The earlier value is stale |
| Analysis populations are not reconciled | `STATUS.md`: 3,333 UK participants and 1,159 Wales; QC brief: 3,209 UK strict-horizon and 1,059 Wales in Julius | Every table needs an analysis-specific disposition count rather than one unlabeled “risk set” |

Checks that did hold: the supplied JSON’s 289 UK and 92 Welsh events match `STATUS.md`; C=0.699707 and C=0.748637 round to the status values; and 10 WIN + 58 tie + 1 LOSS + 9 non-estimable equals 78 cells, matching two cohorts × 13 strata × three comparators. The visible estimated strata all have at least ten events. Confidence intervals and omitted strata were not supplied, so the verdict labels themselves could not be recomputed.

No comparator test was available to inspect. Consequently, there is no demonstrated test that would fail when a coefficient, unit conversion, threshold, imputation rule, or target-cohort standardisation is wrong.

## 3. ADVERSARIAL AUDIT

Assuming both WINs are artefacts, the most likely mechanism is comparator degradation: a non-source equation, arbitrary score scaling, target-sample standardisation, and healthy-value imputation lower or reorder comparator predictions. The pattern in `debate/steps/step-002-QC-BRIEF.md`, sections B–C, supports this attack: Montreal—the comparator not needing LDL bands or Lp(a)—nearly reproduces, whereas the two affected comparators are precisely those producing declared WINs.

The local all-cohort point advantages are small: UK deltas are +0.0330, +0.0261, and +0.0058; Welsh deltas are +0.0124, +0.0013, and +0.0231 in `outputs/calon_final.json`. No supplied confidence intervals establish that these differences are non-zero, and no clinical-utility analysis establishes that they matter. The model also loses to SAFEHEART in UK diabetes by −0.0644 with 64 events.

What should have failed if the comparators were wrong?

- A PDF-derived worked-example test.
- A unit-conversion test.
- A missing-input rejection test.
- A batch-invariance test proving that a person’s score is unchanged when placed in a subgroup.
- A frozen-risk-set test proving both pipelines score the same inputs.
- A paired C-index/AUC recomputation using the same horizon and censoring rules.

None is present in the supplied evidence.

The single decisive computation is to implement PDF-extracted equations once, score all comparators on one frozen, identically eligible cohort, and report only aggregate eligible counts, event counts, comparator C-statistics, paired deltas, and at least 2,000 cluster-aware bootstrap replicates. No participant-level data are needed in the report.

### Evidence still needed for the seeded objections

- **OBJ-001:** Source-PDF tables or worked examples; a predictor/threshold/unit/endpoint/horizon/derivation-cohort provenance table; explicit missingness policy; identical cohort and performance metric; golden-vector tests; and paired delta recomputation. The Spec Kit’s “source-faithful” docstring is not source evidence.

- **OBJ-002:** The exact definition of calibration slope, predictor scale, link function, horizon, and censoring method. Under the standard Cox/complementary-log-log formulation, changing baseline survival or subtracting a centring constant changes the intercept, not the slope. A slope below one also ordinarily indicates an over-dispersed prognostic index requiring shrinkage, not predictions that are “too compressed.” The more plausible shared error is treating point totals, standardised scores, or probabilities as though they were published unscaled linear predictors. An affine-invariance test is required before the proposed centred/uncentred experiment can diagnose anything.

- **OBJ-003:** Aggregate Pearson correlation is necessary but insufficient. Report correlation, VIF or condition index, term scaling, and age HRs from prespecified models containing age alone, age plus untreated cholesterol, age plus cumulative exposure, and a residualised or centred cumulative term. A changed age coefficient after replacing cholesterol-years changes the conditional estimand; by itself it does not prove collinearity. The `usable()` excerpt cannot answer this because it checks only spline terms.

## 4. CLINICAL AND PUBLICATION REALITY

The defensible claim is narrow: the implemented CALON specification shows internal ranking performance around 0.70 in UK Biobank and 0.75 in Wales under the local pipeline. Relative superiority, external transportability, absolute-risk accuracy, and clinical benefit remain unestablished.

A lipidologist would immediately challenge:

- C=0.559 in UK diabetes, C=0.612 among treated UK participants, C=0.558 in hypertensive Wales, and C=0.600 in older Wales.
- The grey-zone point estimate of AUC 0.489 with 22 events. Without a confidence interval it is not proof of worse-than-chance performance, but it provides no evidence of useful discrimination where treatment decisions are difficult.
- A coronary-weighted endpoint presented as general ASCVD.
- Welsh median follow-up of approximately four years being used to support longer-horizon claims without numbers at risk or censoring-adjusted calibration.
- No applicable equation, calibration plot, calibration-in-the-large, net-benefit analysis, or frozen external-validation result.

The hostile reviewer opens with comparator provenance and subgroup refitting. Next come cohort-flow discrepancies, outcome-date completeness, missing-value treatment, multiplicity across 69 estimable comparisons, and the absence of reporting artefacts listed in `debate/steps/step-002-QC-BRIEF.md`, section E. The 10/58/1 tally should not be used as a clinical headline: it counts many correlated subgroup comparisons, while the all-cohort advantages are small and unresolved.

Proposed objection blocks:

```objection
id: OBJ-004
step: 000
raised_by: codex
claim: The step-000 packet omits the contents of multiple mandatory resources, including the governance executables, QC JSON, comparator tests and fidelity materials, and all source PDFs, so parser enforcement, QC validity, and publication provenance cannot be independently audited.
settled_by: Run shasum -a 256 and wc -l for all 19 named non-PDF resources in debate/steps/step-000-QC-BRIEF.md plus every located comparator PDF, save the result as debate/steps/step-000/resource-manifest.tsv, and verify that the archived panel packet contains content matching every listed hash.
status: OPEN
```

```objection
id: OBJ-005
step: 000
raised_by: codex
claim: code/15_CALON_FINAL.py does not evaluate fixed source-faithful comparators: Montreal uses target-sample standardisation, several missing predictors are imputed as healthy or by subgroup medians, and its SAFEHEART transformation is structurally different from CALON_JULIUS_SPECKIT/scripts/comparators.py. The reported comparator C-indices therefore have unresolved provenance.
settled_by: Add and run PDF-derived test_pdf_golden_vectors and test_score_invariant_to_batch_and_subgroup cases in CALON_JULIUS_SPECKIT/tests/test_comparators.py, require exact agreement with source worked examples and identical scores for identical inputs across batches, then recompute aggregate comparator C-indices and paired deltas on one frozen cohort and horizon.
status: OPEN
```

```objection
id: OBJ-006
step: 000
raised_by: codex
claim: The claim that no subgroup gets its own model is unsupported and appears contradicted by code/15_CALON_FINAL.py calling cv(s, cohort_spec, resolve=False) afresh inside every subgroup; subgroup performance may therefore describe newly fitted stratum-specific models rather than one frozen CALON-F model.
settled_by: Run a fit-count instrumentation test over the ALL and subgroup loop that reports only aggregate fit counts and maximum prediction difference; require zero additional model fits after the ALL predictions are created and maximum absolute difference 0 for every reused subgroup prediction, or relabel all subgroup results as separately trained models.
status: OPEN
```

```objection
id: OBJ-007
step: 000
raised_by: codex
claim: The visible corrected_root implementation establishes path precedence but not runtime content identity, so two machines or two available copies can silently run different corrected-outcome files despite a static hash claim in the docstring.
settled_by: Run a corrected_root unit test with two temporary candidate files of different SHA-256 values and require the resolver to abort, then run the real pre-flight check and publish only the selected file SHA-256, which must exactly match its entry in SHA256SUMS.txt.
status: OPEN
```

```objection
id: OBJ-008
step: 000
raised_by: codex
claim: OBJ-002's proposed centred-versus-uncentred and baseline-survival experiment is not diagnostic under standard survival calibration because additive centring and baseline hazard alter the calibration intercept, not the slope; the current settlement condition could return no change even when the comparator scale is wrong.
settled_by: Run an affine-invariance unit test at one fixed observed horizon using the declared calibration-slope function: report slopes after adding a constant to the prognostic index, changing only baseline survival, and multiplying the index by 0.5 and 2.0; additive variants must agree within 0.000001 and multiplicative variants must show the expected reciprocal slope change.
status: OPEN
```

```objection
id: OBJ-009
step: 000
raised_by: codex
claim: Public result documents are not synchronised: STATUS.md reports the same diabetic SAFEHEART loss as both -0.062 and -0.064 while outputs/calon_final.json gives -0.0643716927, and the 3333 versus 3209 UK and 1159 versus 1059 Welsh populations are not labelled as distinct estimands.
settled_by: Run a status-versus-output consistency script that requires every displayed delta to match outputs/calon_final.json at its stated rounding precision and publish an aggregate cohort-disposition table reconciling 3540 to 3333 to 3209 in UK Biobank and 7253 to 1159 or 1059 in Wales by named exclusion and horizon.
status: OPEN
```


========== PRIOR ROUND · KIMI ==========

---
agent: kimi
step: "000"
round: "1"
protocol: full-matrix-blind
status: round-1-complete
source: debate/steps/step-000/r1b/kimi.txt
---

# Step 000 · Round 1 · KIMI

> Blind resource audit. This agent did **not** see other agents' outputs.
> Four lenses required: Methodology · Implementation · Adversarial · Clinical/publication.

# Step 000, Round 1 — Kimi, resource audit (blind)

  ## Resource ledger — what I examined, what it establishes, what it does not

  **Provided and read in full:** the step-000 brief; `mandates/ROLES.md`; `state/open-questions.md`; `DATA-INVENTORY.md` (lines 1–120 only); `STATUS.md`; `steps/step-002-QC-BRIEF.md`; excerpts of `code/15_CALON_FINAL.py` (SPEC/comparator/`usable()`/tally sections); `CALON_JULIUS_SPECKIT/scripts/comparators.py` (truncated mid-`fhrs_chart_points`); headline aggregates of `outputs/calon_final.json`.

  **Listed as permitted but NOT in my context, therefore unexamined:** `mandates/AGENT.md` (the prompt header substitutes for it) and `ORCHESTRATOR.md`; `bin/panel.mjs` and `bin/consensus.mjs` — so I cannot verify that register rules 1–5 (no self-closure, evidence-must-name-artefact, two-agent minimum, MAX_ROUNDS) are actually enforced in code rather than merely asserted in `open-questions.md`; `state/transcript.md` and `locked-decisions.md`; `tests/test_comparators.py` — so I cannot verify the Spec Kit tests pin coefficients to an external source rather than round-tripping the same constants; `research.md`; `checklists/comparator-fidelity.md`; `outputs/calon_final_qc.json`; and every comparator source PDF. **No coefficient in this turn is verified against a PDF.** Everything I say about provenance is about internal contradiction, which is all a blind audit can establish.

  What the provided material does establish: the locked local output (`calon_final.json`), the register state, and at least one hard internal contradiction in comparator code (below). What it does not establish: which of the two pipelines' comparator C-indices is right, and whether any comparator constant on disk matches its source publication.

  ---

  ## 1. METHODOLOGY

  **The step-002 brief conflates two estimands in one AGREE/DISAGREE frame.** Section A lists "Incident events, 5-year: 97 / 10-year: 194 / risk set 3,209" as agreed, but the locked local output is a full-follow-up survival analysis — `ukb.qc.median_followup` 14.55 years, 289 events (`calon_final.json`). Horizon-restricted risk classification and full-follow-up survival ranking are different estimands; "which numbers are trustworthy" is partly unanswerable until the debate fixes which estimand the WINs refer to. The brief never states this.

  **The strict-horizon Welsh construction is case-enriching by design.** Brief D5: "event before horizon OR documented follow-up to horizon" admits every event but only documented event-free survivors. Event rate inflates 7.4% (n=529) → 20.4% (n=289) as the sample shrinks 45%. A C-index from that construction is not transportable; the Welsh arm of the Julius run is measuring ascertainment, not risk.

  **Montreal is misclassified as an incident-event comparator.** `comparators.py::montreal_fh_score` docstring: "ranking/prevalent-CVD use only." Yet both pipelines score it against incident outcomes and it occupies one third of the tally cells (13 subgroups × 2 cohorts). The Spec Kit's own provenance warning is ignored downstream — a claim propagating past its own docstring, this project's signature failure shape.

  **Minimum event-to-baseline lag of 1 day** (brief A) means near-prevalent events enter the "incident" endpoint. No landmark sensitivity (e.g., exclude <6 months) is reported anywhere I was shown.

  **The three live objections are well-formed**: each `settled_by` names a runnable test. OBJ-003's settlement, however, has a code-level obstacle — see Implementation.

  ## 2. IMPLEMENTATION

  **Two irreconcilable "SAFEHEART" implementations coexist, both claiming published provenance.** `code/15_CALON_FINAL.py:278-279` scores SAFEHEART as a *continuous* LP (`0.045·age + 0.6·male + 0.4·htn + 0.3·smoke + 0.02·bmi + 0.15·ldl + 0.25·lpa_hi`) under the docstring "Published equations, scored not fitted" (line 257). `comparators.py::safeheart_linear_predictor` implements the *categorical* published form (age bands 1.07/1.45; male 0.70; prior-ASCVD 1.42; LDL mg/dL bands 0.92/1.57; Lp(a)>50 → 0.42), citing Pérez de Isla 2017 Table 3. The local version omits the prior-ASCVD term entirely and takes LDL as a continuous variable in unstated units — UK Biobank `ldl_chem` is mmol/L (`DATA-INVENTORY.md`), the Spec Kit expects mg/dL. At most one of these is the published score. This is decisive for OBJ-001: the local SAFEHEART C of 0.6944 — the number that converts both Julius WINs to TIEs — comes from the unverified implementation.

  **`comparators()` silently imputes every missing input** (`15_CALON_FINAL.py:258-262`): `hdl→1.35`, `htn→0`, `smoke→0`, `ldl→` cohort median, `lpa→0` (so the 22.5% missing Lp(a) become `lpa_hi=0`), `bmi→` median or 27.0. No imputation count is printed per input. The comparator C-indices in `calon_final.json` are of silently completed variants, not the published scores, and imputation burden differs by cohort (Welsh BMI 45.5% observed, STATUS.md).

  **The collinearity guard cannot see OBJ-003's failure mode.** `usable()` line 300: `if f.startswith("sp") and abs(corrcoef(age, f)) >= 0.999` — the check only inspects spline features against age. A non-spline term built from age (cholesterol-years = age × TC) is never correlated-checked by anything. The docstring (lines 285–294) presents F3 as a general collinearity guard; the code is a spline-deduplication rule. A check structurally incapable of catching the failure it is cited against.

  **Unverified magic constants in the Spec Kit:** `safeheart_risk` uses centering `5.4078` and baseline survivals `{5: 0.9532, 10: 0.9025}` with no provenance I was shown. If `tests/test_comparators.py` (not provided) merely asserts these same numbers, provenance is circular — exactly how invented weights shipped last time.

  ## 3. ADVERSARIAL AUDIT

  Assume the strongest claim — "the local pipeline's comparator values are correct and both Julius WINs are artefacts" — is wrong. **Most likely way it is wrong:** the local continuous SAFEHEART is accidentally well-tuned to UK Biobank, manufacturing ties. The asymmetry argument in OBJ-001 cuts both ways: Montreal — the one comparator whose published form is integer points anyone can transcribe — reproduces across pipelines to 0.003. SAFEHEART and FH-RS disagree precisely where implementation freedom is greatest (Lp(a) threshold, LDL units/bands, missing-data handling). That pattern is consistent with *either* side being wrong, and only the PDFs arbitrate. If the local SAFEHEART were wrong, what would have failed? The PDF extraction in OBJ-001's `settled_by` — which is why that test, run over both in-repo implementations, is the single computation that settles the WIN dispute.

  **An exactly-zero delta.** `calon_final.json`: `wales.subgroups."no diabetes".vs.Montreal.delta == 0.0` with 63 events and a continuous model LP. Exact 0.0 in floating point between two independently computed C-indices is arithmetically improbable; it suggests a degenerate path in `delta_ci` or the comparator vector being the model's own LP somewhere. Nothing downstream checks for this — the cell counts as a "tie" and moves on.

  **The Welsh tally hides consistently negative point estimates.** Wales hypertensive subgroup: model C 0.5585, all three deltas negative (−0.056, −0.039, −0.027), yet `wales.tally.LOSS = 0` because every CI crosses zero. "Zero losses in Wales" is mechanically true and substantively misleading.

  **The register's one closed objection rests on a disputed number.** OBJ-000 (worked example) closed on "median excess +0.226 mmol/L" — the value brief section B attributes to Julius, against the local pipeline's +0.15 and the spec's +0.55. If OBJ-000 is a real closure rather than an illustration, its evidence belongs to the pipeline currently under QC. Three values for one quantity, unreconciled.

  **OBJ-002 candidate mechanism, named:** `15_CALON_FINAL.py:272-274` z-standardizes Montreal's age and HDL terms *using the validation cohort's own mean/std*. A calibration slope fitted on a cohort-standardized LP is not on the log-HR scale and cannot be compared to 1.0; if the Julius run standardized all four LPs the same way before slope estimation, slopes of β·SD(LP) clustering at 0.52–0.57 would be an artefact of the transform, not of biology. OBJ-002's settlement should therefore require slopes reported on the raw, unstandardized LP scale.

  ## 4. CLINICAL AND PUBLICATION REALITY

  **All ten wins are internal.** `calon_final.json`: `ukb.tally` = 10/28/1; `wales.tally` = **0/30/0** with 9 non-estimable. The pooled "10 wins, 58 ties, 1 loss" in STATUS.md is entirely a UK Biobank result; in the external genotype-confirmed registry the model wins zero cells. A lipidologist reads that as: parity externally, superiority only where the model was built. Any abstract citing the pooled tally without the split over-claims.

  **The model is near-chance exactly where decisions bite:** Welsh hypertensives C 0.5585 (52 events); UKB diabetics C 0.5593 (64 events, the one declared loss); grey-zone 5–10% band AUC 0.489 (brief D3) — below chance in the band where a score must earn its keep — and both enhancers null (STATUS.md grey-zone section: apoB/LDL-C ΔC +0.0146 [−0.0050, +0.0330], Lp(a) HR 1.033).

  **The endpoint is coronary-weighted** (I63 date completeness 40.9%, G45 37.0% — brief A) but is sold as ASCVD. A hostile reviewer opens at: (1) comparator provenance — "show me SAFEHEART's coefficients and your scoring code, side by side"; (2) "your wins vanish in your external cohort"; (3) "your cerebrovascular component is 40–60% undated." What honestly survives today: an incident-ASCVD model in HeFH with C≈0.70/0.75 that ties published scores externally and loses nothing it pre-specified. That is publishable; "10 wins" as currently pooled is not.

  ---

  ## Discrepancy ledger

  1. **SAFEHEART ×2** — `15_CALON_FINAL.py:278-279` (continuous, no prior-ASCVD term, LDL units unstated) vs `comparators.py::safeheart_linear_predictor` (categorical, Pérez de Isla 2017 Table 3). Both claim published provenance. → OBJ-004.
  2. **Risk set** — step-002 brief A: 3,209 after excluding 207 prevalent + 124 undated. STATUS.md/`calon_final.json`: n=3,333 = 3,540 − 207 exactly, implying the 124 undated cases remain in the local risk set. → OBJ-006.
  3. **Montreal ×2** — local standardized-continuous LP (lines 272–274, cohort-dependent scale) vs Spec Kit integer points; Spec Kit docstring restricts it to prevalent-CVD ranking, yet both pipelines evaluate it on incident events.
  4. **FH-RS ×2** — local continuous band weights (`ab`/`lb`/`hb`, lines 275–277) vs Spec Kit integer `fhrs_chart_points`; excerpt truncated, equivalence unconfirmable.
  5. **Silent comparator imputation** — lines 258–262; no counts reported. → OBJ-005.
  6. **Diabetic loss magnitude** — STATUS.md says −0.062 in one paragraph and −0.064 two later; JSON: −0.0644. Trivial, symptomatic.
  7. **Carrier LDL-C excess ×3** — +0.15 (local) vs +0.226 (Julius, also OBJ-000's closing evidence) vs +0.55 (spec). Unreconciled.
  8. **Cosmetic** — ROLES.md "four lenses" vs "Fifth lens" naming; no scientific consequence.

  ## Evidence still needed before closure

  - **OBJ-001:** PDF-extracted SAFEHEART-RE and FH-RS coefficients from the PDFs on disk (not provided to me); a ruling on which in-repo implementation matches; one frozen cohort extract; both deltas recomputed with ≥2,000 bootstrap replicates (brief D6: FH-RS lower CI 0.001 is the 7.5th order statistic of 300 draws).
  - **OBJ-002:** Slopes recomputed on raw, unstandardized LPs, centred and uncentred, at 5- and 10-year baseline survival, with the `5.4078`/`0.9532`/`0.9025` constants verified against the PDF; plus a statement of whether Julius z-standardized LPs before slope estimation.
  - **OBJ-003:** Pearson r(age, cholesterol-years) printed from the analysis cohort — noting the guard at `15_CALON_FINAL.py:300` structurally cannot produce it — and the refit with untreated TC alone, reporting age HR both ways.

  ## Proposed objections (text only — not filed, per step instructions)

  ```objection
  id: OBJ-004
  step: 000
  raised_by: kimi
  claim: Two irreconcilable SAFEHEART implementations coexist, both claiming published provenance. code/15_CALON_FINAL.py:278-279 scores a continuous LP (0.045*age + 0.6*male + 0.4*htn + 0.3*smoke + 0.02*bmi + 0.15*ldl + 0.25*lpa_hi, no prior-ASCVD term, LDL units unstated) while CALON_JULIUS_SPECKIT/scripts/comparators.py::safeheart_linear_predictor implements the categorical Pérez de Isla 2017 Table 3 form (age bands 1.07/1.45, prior_ascvd 1.42, LDL mg/dL bands 0.92/1.57, Lp(a)>50 -> 0.42). At most one is the published score, and the local SAFEHEART C of 0.6944 that converts both Julius WINs to TIEs (OBJ-001) comes from the unverified one.
  settled_by: Extract the SAFEHEART-RE coefficients from the Pérez de Isla 2017 PDF on disk, score one identical frozen UKB carrier cohort extract with both implementations plus the PDF-verified form, and publish the three C-indices and pairwise LP correlations. The implementation matching the PDF within 0.003 on Montreal-style reproduction grounds is the comparator of record; recompute both OBJ-001 deltas with it.
  status: OPEN
  ```

  ```objection
  id: OBJ-005
  step: 000
  raised_by: kimi
  claim: code/15_CALON_FINAL.py:258-262 silently imputes every missing comparator input (hdl->1.35, htn->0, smoke->0, ldl->cohort median, lpa->0 making 22.5% missing Lp(a) into lpa_hi=0, bmi->median/27.0) and prints no per-input imputation counts. The comparator C-indices in outputs/calon_final.json are therefore not of the published scores but of silently completed variants, with imputation burden differing by cohort (Welsh BMI 45.5% observed vs 99.6% UKB per STATUS.md).
  settled_by: Patch comparators() to print per-input missingness counts per cohort, recompute all comparator C-indices complete-case on the identical frozen cohort extract, and publish the delta between complete-case and imputed values alongside outputs/calon_final.json.
  status: OPEN
  ```

  ```objection
  id: OBJ-006
  step: 000
  raised_by: kimi
  claim: The step-002 brief section A asserts both pipelines agree on a 3,209 risk set after excluding 207 prevalent plus 124 undated atherosclerotic cases, but STATUS.md and outputs/calon_final.json report UKB n=3,333 = 3,540 - 207 exactly, implying the 124 undated cases remain in the local risk set. If retained as event-free, 3.7% of the local cohort are misclassified cases attenuating every local C-index, including the comparator values at the centre of OBJ-001.
  settled_by: Instrument build_ukb() in code/15_CALON_FINAL.py to print each exclusion count and the disposition (excluded / censored / event-free) of the 124 undated atherosclerotic cases, and reconcile the printed arithmetic to either 3,209 or 3,333.
  status: OPEN
  ```

  ```objection
  id: OBJ-007
  step: 000
  raised_by: kimi
  claim: The headline "10 wins, 58 ties, 1 loss" in STATUS.md pools two cohorts, but outputs/calon_final.json shows all 10 wins are UK Biobank (ukb.tally 10/28/1) while the external Welsh cohort is 0/30/0 with 9 non-estimable (wales.tally). Any manuscript or abstract text citing the pooled tally without the per-cohort split overstates external performance: externally the model wins zero cells.
  settled_by: grep manuscript/ for the pooled tally; wherever it appears, the per-cohort tallies from outputs/calon_final.json (ukb.tally, wales.tally) must appear alongside it. Verified by re-running the grep after edits.
  status: OPEN
  ```

  ```objection
  id: OBJ-008
  step: 000
  raised_by: kimi
  claim: outputs/calon_final.json records wales.subgroups."no diabetes".vs.Montreal.delta as exactly 0.0 with 63 events. An exactly-zero floating-point delta between two independently computed C-indices is arithmetically improbable and suggests a degenerate path in delta_ci (code/15_CALON_FINAL.py:440) or the comparator LP being the model's own LP in that cell. No downstream check flags an exact zero; the cell is silently counted as a tie.
  settled_by: Recompute concordance_index for the model LP and Montreal LP on the Wales no-diabetes subgroup, print both C values to 6 decimal places, and show the delta_ci inputs. If the zero reproduces from genuinely equal C-indices, withdraw; otherwise fix the degenerate path and recompute the Welsh tally.
  status: OPEN
  ```


========== PRIOR ROUND · GROK ==========

---
agent: grok
step: "000"
round: "1"
protocol: full-matrix-blind
status: round-1-complete
source: debate/steps/step-000/r1b/grok.txt
---

# Step 000 · Round 1 · GROK

> Blind resource audit. This agent did **not** see other agents' outputs.
> Four lenses required: Methodology · Implementation · Adversarial · Clinical/publication.

The step brief forbids tools and file edits; the prompt was truncated, so I'll read only the offloaded full request to recover the permitted resources, then answer all four lenses from those materials.The offloaded prompt is still incomplete. I'll continue from the cut-off so the resource audit uses the full permitted set.# Step 000, Round 1 — Grok
Resource audit only. Not a WIN adjudication. Does not close OBJ-001, OBJ-002, or OBJ-003.

---

## 1. METHODOLOGY

The estimand of this step is not a C-index and not a WIN. It is: **which artefacts are allowed to enter later scientific debate, and do those artefacts agree with each other.** The design does not fully answer that question.

**What the delivered pack can license.** Conflicts among inlined text. Cohort-definition arithmetic. The fact that two comparator stacks on disk implement different functional forms under the same three names. Aggregate counts in `outputs/calon_final.json` versus sentences in `STATUS.md`.

**What it cannot license.** Source-faithful comparator coefficients. That check is defined, in `debate/mandates/ROLES.md` (“The honest limit on hallucination detection”), as human-against-PDF. No comparator PDF was located by filename in this pack. I do not have Pérez de Isla Table 3, the Montreal points table, or the FH-Risk-Score chart except as transcribed inside `CALON_JULIUS_SPECKIT/scripts/comparators.py`. Treating that transcription as the paper would repeat the exact failure this programme has already shipped.

**Reporting-standard failure already visible in the resource layer.** `STATUS.md` reports a two-cohort incident model in “genotype-confirmed HeFH” with a 10 / 58 / 1 head-to-head tally. The register’s own answered OBJ-000 says the UK Biobank carrier flag has median untreated LDL-C excess **+0.226 mmol/L**, **2.1%** above 6.5 mmol/L, and `variant_id` empty in all 501,936 rows. Those numbers do not support the HeFH label. A resource pack that lets “genotype-confirmed HeFH” travel into step 001 as if it were settled has already smuggled a clinical claim past the only check that contradicted it.

**Two analyses, two estimands, one comparison table.** The QC brief (`debate/steps/step-002-QC-BRIEF.md`, sections A–C) places Julius 5- and 10-year ridge-logistic C-indices next to local unrestricted-follow-up C-indices as if they were the same target. They are not.

| Piece | Local CALON-F (`STATUS.md`, `calon_final.json`) | Julius (QC brief) |
|---|---|---|
| Horizon | Unrestricted; UKB median follow-up 14.55 y; Wales median 4.00 y | Strict 5-year and 10-year |
| Events | UKB 289; Wales 92 | UKB 97 (5y) / 194 (10y); Wales not reported |
| Risk set | STATUS 3,333; QC-agreed 3,209 | 3,209 after both exclusions |
| Wales n | 1,159 | 1,059 |
| Learner | Whatever `cv()` in `code/15_CALON_FINAL.py` is (not inlined) | Ridge-logistic, not Cox |
| Primary C | 0.6997 / 0.7486 | 0.698 / 0.698–0.713 |

A later WIN computed as “our 10-year C minus their comparator C” is not the same estimand as “our unrestricted C minus our comparator C”. Step 000 must lock that distinction before step 001 is allowed to talk about deltas.

**Inference the design does not license, already being drawn.** `STATUS.md` presents 10 wins, 58 ties, 1 loss “of 69 estimable cells” as the current result. From `outputs/calon_final.json`, the primary UKB ALL deltas are Montreal +0.033, FH-RS +0.026, SAFEHEART **+0.0058**. Wales contributes **0 wins**. The tally is a cell-count across 13×3×2 subgroup comparisons, not a primary head-to-head. Nothing in the pack reports per-cell confidence intervals, so even the 10 cannot be rebuilt from the delivered JSON excerpt.

**What I checked under this lens and it held.** Endpoint arithmetic is internally consistent in one place: STATUS’s “62 of 351 carrier events were heart-failure-only” gives 351 − 62 = 289, which matches `ukb.qc.events` and `ukb.subgroups.ALL.events`. I21/I25/I63/I70/I73/G45 with I50 out is the same list in STATUS and the QC brief. That is all that held.

---

## 2. IMPLEMENTATION

I could not execute code. I could read what the inlined functions would do.

### 2.1 The comparator stack is two different programs

`code/15_CALON_FINAL.py`, `comparators()` (lines 256–280 of the excerpt), docstring: *“Published equations, scored not fitted.”*

What it actually scores:

- **Montreal** — a z-scored linear form on the **analysis cohort**: `0.75 * (age − mean)/sd − 0.27 * (hdl − mean)/sd + 0.25·male + 0.19·htn + 0.12·smoke`.
- **FH-RS** — ad-hoc age / LDL / HDL bands (`ab`, `lb`, `hb`) plus `0.721·male + 0.644·htn + 0.625·smoke + 0.434·I(Lp(a)≥105)`, with missing Lp(a) filled by 0.
- **SAFEHEART** — a continuous LP: `0.045·age + 0.6·male + 0.4·htn + 0.3·smoke + 0.02·bmi + 0.15·ldl + 0.25·I(Lp(a)≥105)`. No prior-ASCVD term. No baseline survival. No centring constant.

`CALON_JULIUS_SPECKIT/scripts/comparators.py` scores something else under the same names:

- **SAFEHEART** — categorical LP attributed to Pérez de Isla, *Circulation* 2017, Table 3: `0.70·male + 1.07·I(30≤age<60) + 1.45·I(age≥60) + 0.69·HTN + 1.42·prior_ASCVD + 0.48·smoking + BMI bands + LDL bands in mg/dL + 0.42·I(Lp(a)>50 mg/dL)`, then `1 − S0^exp(LP − 5.4078)` with `S0(5)=0.9532`, `S0(10)=0.9025`.
- **Montreal** — integer point score, age bands of 4, HDL bands of 3, +2 HTN, +1 ever-smoke, +3 male. No z-scoring.
- **FH-RS** — `fhrs_chart_points` for ages 18–65 (body truncated in the pack).
- Contract: no imputation, no unit conversion, raise `ComparatorInputError` on missing or out-of-range input.

These cannot both be the published equations. Rankings will differ. C-indices will differ. A 0.06 SAFEHEART C gap (local 0.6944 vs Julius 0.628 / 0.635) is the expected signature of scoring two different functions, not of two honest implementations of one function on one frozen extract.

**What would have failed if the local docstring were false?** Nothing in the delivered artefacts. `calon_final.json` stores deltas and C-indices, not coefficients, not units, not thresholds. No test file was inlined. The check that cannot fail is the claim “Published equations”.

### 2.2 Silent degradation inside `comparators()`

| Default | Effect if the field is missing |
|---|---|
| `hdl.fillna(1.35)` | Missing HDL becomes a specific “normal” value with no flag |
| `ldl.fillna(median of ldl_unt)` | Missing untreated LDL imputed from the scored slice |
| `lpa.fillna(0)` then `≥105` | Missing Lp(a) is never high. QC brief §D.7 already names this for Julius (22.5% assigned 0). Local does the same. |
| `bmi.fillna(median or 27.0)` | Arbitrary 27 if the whole vector is missing |
| `htn_any.fillna(0)`, `smoke.fillna(0)` | Missing coded as absent |

Spec Kit refuses every one of those. Local swallows them and still writes “published”.

Lp(a) threshold **105** versus Spec Kit **50**. I do not know the unit of `d.lpa`. DATA-INVENTORY.md lists `lpa_chem`, `pre_lpa`, `lpa_i0` and does not state units. 105 nmol/L is a common stand-in for ~50 mg/dL; it is also a unit error if `d.lpa` is already mg/dL. Nothing in the delivered pack would fail either way.

LDL for local SAFEHEART is `ldl_unt` with a continuous coefficient 0.15. Spec Kit LDL is **mg/dL categories**. If `ldl_unt` is mmol/L — the inventory’s other lipid fields are — the local term is in a different unit from the paper Spec Kit cites.

Montreal is re-standardised on the validation cohort. For a purely linear score that is rank-invariant. Montreal-FH-SCORE is not linear; it is a step-function point score. Local “Montreal” is a different model that happens to use some of the same variable names.

### 2.3 Cohort construction: a check that already disagrees with itself

STATUS: UKB **n=3,333** / 289 events.

QC brief §A, numbers that agree: 3,540 carriers, 207 prevalent excluded, 124 undated excluded, risk set **3,209**.

3,540 − 207 = **3,333**. 3,540 − 207 − 124 = **3,209**.

STATUS’s denominator is the cohort **before** the undated-atherosclerotic exclusion that both pipelines are said to agree on. Either `build_ukb()` keeps those 124 people, and STATUS is describing the script, or `build_ukb()` drops them, and STATUS is stale. The JSON excerpt has events and C but **no n**. The question is answerable from `build_ukb()` and is not answered by the pack.

Wales: local **1,159** / 92 versus Julius **1,059** / events not reported. Inventory `wales` is 7,253 × 190. Trap 6 says a `dayfirst=True` parse of `MeasurementDate.2` silently moves the cohort from 1,159/92 to 948/82. Julius’s 1,059 is a third number, not that trap. No filter ledger explains the 100.

### 2.4 Other implementation facts that are not yet locked

- `usable()` collinearity guard (`code/15_CALON_FINAL.py` ~300) drops only features whose name starts with `sp` at `|r|≥0.999` with age. It cannot implement the cholesterol-years check OBJ-003 asks for, because cholesterol-years is not in `SPEC` and would not match `startswith("sp")` if it were. That guard firing on `sp18`/`sp30` in UKB (STATUS) is not evidence Julius ran the same check.
- SPEC comments (lines 85–102) still narrate adding BMI after the diabetic loss. STATUS says BMI was removed the same day. The live `SPEC` list has no BMI. Dead comments in the locked script are how a withdrawn specification re-enters a Methods section.
- `corrected_root()` searches several paths. The docstring cites md5 `ab364bc996c7a843c2f3b7f620dafbf0` for `corrected_ascvd_outcomes.csv`. Inventory points at a different folder and SHA-256 in `SHA256SUMS.txt`. Two hash schemes, two locations. Reproducible only if those files are byte-identical, which this pack does not show.
- `outputs/calon_final.json` has a key `participant_level_outputs`. I did not open it and must not. The key name is a governance surface sitting inside a file this debate is allowed to read.
- Permitted but **not inlined**: `debate/mandates/AGENT.md`, `ORCHESTRATOR.md`, `debate/state/transcript.md`, `locked-decisions.md`, `debate/bin/panel.mjs`, `consensus.mjs`, `outputs/calon_final_qc.json`, `README.md`, `tests/test_comparators.py`, `research.md`, `checklists/comparator-fidelity.md`, and every comparator PDF. A resource audit that proceeds as if those were read is the file-discovery failure mode named in the mandate.

**What I checked under this lens and it held.** Local UKB ALL C 0.699707 plus SAFEHEART delta 0.005782 gives implied local SAFEHEART C ≈ 0.6939, which matches the QC brief’s local 0.6944 to rounding. The tally arithmetic holds: UKB 13×3 = 39 = 10+28+1; Wales 30 ties + 9 non-estimable = 39; combined 10+58+1+9 = 78 = 2×39. The WIN/LOSS rule `lo>0 / hi<0 / else tie` is internally consistent. That is all that held.

---

## 3. ADVERSARIAL AUDIT

Assume the conclusion a later step will want — that the resource base is clean enough to debate WINs — is wrong. The most likely way it is wrong is the shape this project has already been damaged by: **a claim that looks sourced and is not measured.**

**Strongest version of the claim I am attacking.** “CALON-F is a locked, leak-free, two-cohort incident model in genotype-confirmed HeFH, scored against published Montreal, FH-Risk-Score and SAFEHEART-RE equations, and the current artefact (`STATUS.md` + `calon_final.json`) is the number set this panel should treat as local truth.”

**Most likely way that is wrong.**

1. **The comparators are not the published equations.** Local `comparators()` is a different model family from Spec Kit, which itself is only a claim about Pérez de Isla 2017. No PDF extract exists in this pack. Montreal agreeing to 0.003 (QC brief §C) does **not** validate SAFEHEART or FH-RS; it is the one comparator that needs neither Lp(a) nor LDL bands, and local Montreal is not even the point score. Agreement on the easy one is the control. Disagreement on the two that need lipids is the experiment. The experiment already failed, in one direction, and that direction is the one that creates WINs.

2. **The UKB arm is not HeFH.** OBJ-000, status ANSWERED, evidence: +0.226 mmol/L, 2.1% above 6.5, `variant_id` empty. QC brief also lists a local +0.15 median and ~1% above 6.5. Heterozygous FH is not a 0.15–0.23 mmol/L shift. The label survived the answer.

3. **The locked n is not locked.** 3,333 versus 3,209 is not rounding. It is whether 124 undated atherosclerotic cases are in the risk set. C = 0.6997 has no stated denominator in the JSON excerpt.

4. **OBJ-000 was closed on one pipeline’s LDL figure while the QC brief records another.** An answered objection with two live values is not answered. It is a stamp.

5. **Wales cannot carry 10-year comparator claims.** Median follow-up 4.005 years (`wales.qc.median_followup`). Julius’s strict-horizon construction (QC brief §D.5) inflates event rate from 7.4% to 20.4% as the sample shrinks 45%. Local Wales still scores SAFEHEART and FH-RS and reports C = 0.7486 on 92 events. External “validation” with 0 wins and a four-year median is being lined up to support a 10-year score comparison.

**What would have failed if any of this were already true?** Coefficient-vs-PDF tests — absent from the pack. A STATUS check that `n == 3540 - 207 - 124` — absent; STATUS prints 3,333. A label check that “HeFH” requires more than a carrier flag — contradicted by OBJ-000 and left in place. A missingness table for Welsh predictors (QC brief §D.4, O/E = 6.31) — stated not to exist. Comparator slopes in `calon_final.json` — not in the excerpt; OBJ-002 therefore has no local number to attack or defend.

**What I tried and did not find.** I looked for a provenance table of predictors, coefficients, endpoint, horizon, derivation cohort. Not in the pack. I looked for a PDF path. Not in the pack. I looked for `test_comparators.py` assertions. Not inlined. I looked for `calon_final_qc.json` comparator slopes. Not inlined. I looked for Julius’s scoring function. Not in the permitted local tree as delivered. Absence is the finding.

---

## 4. CLINICAL AND PUBLICATION REALITY

A lipidologist will not open on the spline knots. They will open here.

**“This is not an FH cohort.”** +0.15 to +0.23 mmol/L untreated LDL-C excess, ≤2.1% above 6.5, empty `variant_id`. That is a putative LDLR-carrier flag in UK Biobank, not genotype-confirmed HeFH. Wales `Positive1` is the closer thing to a clinic population (inventory trap 4: 2,405 vs `Mutation1` 3,562). The paper’s UKB arm is the large number; the clinic arm is the small one. Calling both HeFH is the sentence a reviewer will quote.

**“Which SAFEHEART?”** STATUS says SAFEHEART-RE. The function is named SAFEHEART. Spec Kit implements a 2017 categorical LP plus published S0. Local implements a continuous LP with different coefficients, different Lp(a) cut, no prior-ASCVD term, no S0. I do not have the RE paper and will not invent it. Three names, at least two equations, zero PDF extracts. No lipidologist will accept a WIN against a score whose equation is not in the supplement.

**It does not change practice.** Primary local UKB ALL versus SAFEHEART is +0.0058. Wales: 0 wins, 30 ties, 9 non-estimable. The one LOSS is the diabetic cell (64 events, δ = −0.0644) — the cell where a clinic would most want a better score. Wales hypertensive C = 0.558 (52 events); Wales age≥median C = 0.600 (71 events). Discrimination vanishes in the older, treated, hypertensive patients who are the use case. Grey-zone 5–10% AUC 0.489 (QC brief §D.3, n=234, 22 events) is the band a risk score is for. STATUS’s 5–20% enhancer result (HR 1.154, ΔC +0.0146, CI crosses 0) does not rescue that.

**Endpoint is coronary-weighted.** Date completeness: I21 100%, I25 100%, I63 40.9%, I70 64.3%, I73 52.8%, G45 37.0% (QC brief §A). A C-index of 0.70 in that mixture is not “ASCVD discrimination” in the sense a stroke or PAD clinic would recognise.

**Calibration is already a stated limitation and a second, worse, unstated one.** Local model slope 1.214 (1.017, 1.411) — predictions too compressed, interval excludes 1. Julius comparator slopes 0.52–0.57 — OBJ-002. Welsh O/E 6.31 — the model predicts *lower* risk in the higher-risk registry. You cannot take a 10-year absolute-risk sentence to a clinic with those three facts on the table.

**Where the hostile reviewer starts.** (1) HeFH label vs OBJ-000. (2) Print the three comparator equations next to the three papers. (3) n = 3,333 or 3,209, and 1,159 or 1,059. (4) Show one WIN that is not a UKB subgroup cell. (5) 300 bootstraps on a CI that starts at 0.001 (QC brief §D.6). (6) No model equation, so nobody can apply CALON-F (QC brief §E). (7) Retracted AUCs still sitting in the repo (`STATUS.md`, retracted section: 0.7605 / 0.767 / 0.848 / 0.7672) for anyone who greps.

**Over-claim relative to numbers.** “10 wins, 58 ties, 1 loss” is a subgroup-cell tally. It is true as arithmetic (`combined_tally` in `calon_final.json`) and false as a clinical sentence. The honest sentence from the local artefact is: on the full UKB carrier extract the model is close to its own SAFEHEART implementation; on Wales it ties everything; in UKB diabetics it loses; the people in the file are not phenotypic HeFH.

---

## Resource ledger

| Examined | Establishes | Does not establish |
|---|---|---|
| Step 000 brief | This step is a resource map; it cannot close OBJ-001/002/003 | That the listed files were all delivered |
| `debate/mandates/ROLES.md` | Full-matrix protocol; PDF check is human, not cross-model | Runtime behaviour of `panel.mjs` / `consensus.mjs` |
| `debate/state/open-questions.md` | OBJ-001/002/003 OPEN; OBJ-000 ANSWERED with +0.226 / 2.1% / empty `variant_id` | That OBJ-000’s numbers match the local pipeline |
| `debate/DATA-INVENTORY.md` | File shapes, column names, 10 traps; 3,540 carriers; `Positive1` vs `Mutation1`; date-parse trap 1,159/92 → 948/82 | Any result; any coefficient; units of Lp(a) |
| `STATUS.md` | CALON-F claimed current; prevalent arm retracted; BMI removed; DRAGON not a third cohort; slope 1.214; tally 10/58/1 | That n=3,333 is the analysis n; that comparators are published; that the cohort is HeFH |
| `debate/steps/step-002-QC-BRIEF.md` | Agree-set vs disagree-set; Julius WIN arithmetic; methodological defects D.1–D.7; undelivered TRIPOD items | Which pipeline is right |
| `code/15_CALON_FINAL.py` excerpts | `SPEC`; `comparators()` forms and imputations; `usable()` spline/F7 rules; WIN rule; subgroup list start | `build_ukb` / `build_wales`; `cv`; `delta_ci`; bootstrap count; hashes actually checked |
| Spec Kit `comparators.py` | A different SAFEHEART and Montreal; no-impute contract; claimed 2017 source and S0 values | That those numbers are in the PDF |
| `outputs/calon_final.json` aggregates | Events, C, deltas, tallies, follow-up | n, CIs, comparator C except by back-calc, coefficients, QC slopes |
| Comparator PDFs, `calon_final_qc.json`, `test_comparators.py`, `research.md`, `comparator-fidelity.md`, `transcript.md`, `locked-decisions.md`, `bin/*.mjs`, `AGENT.md`, `README.md` | **Not delivered** | Anything |

## Discrepancy ledger

1. **SAFEHEART / Montreal / FH-RS are different functions in the two trees**, both labelled published. Local continuous vs Spec Kit categorical; local z-Montreal vs Spec Kit points; Lp(a) 105 vs 50; LDL continuous vs mg/dL bands; local imputes, Spec Kit refuses.
2. **STATUS “SAFEHEART-RE” vs code “SAFEHEART” vs Spec Kit “Pérez de Isla 2017”.** Name mismatch, equation mismatch. No PDF.
3. **UKB n: 3,333 (STATUS) vs 3,209 (QC agree-set).** 3,333 = 3,540 − 207. The 124 undated exclusions are missing from STATUS.
4. **Wales n: 1,159 vs 1,059.** Not the date-parse trap (that goes to 948/82). Unexplained.
5. **LDL-C excess: OBJ-000 +0.226 / 2.1% vs QC-brief local +0.15 / ~1% vs “spec said +0.55”.** OBJ-000 is marked ANSWERED anyway.
6. **Loss magnitude: STATUS −0.062 then −0.064; JSON −0.06437.** Same cell, three writings.
7. **C: endpoint note 0.6996; STATUS 0.6997; JSON 0.699707; QC 0.698 vs 0.6997.** Tight except the Julius 0.698, which is a different horizon/learner.
8. **HeFH label (STATUS) vs OBJ-000 evidence and empty `variant_id`.**
9. **Grey zone: STATUS 5–20% n=1,685 / 218 / ΔC +0.0146 ns vs QC 5–10% n=234 / 22 / AUC 0.489.** Different bands; STATUS omits the below-chance result.
10. **BMI: live SPEC excludes it; adjacent comments still justify adding it after the diabetic loss.**
11. **Primary UKB vs SAFEHEART δ = +0.0058 (tie-shaped) vs headline “10 wins”.** All 10 wins are UKB subgroup cells; Wales 0.
12. **Hash/path: script md5 of outcomes file vs inventory SHA-256 in another folder.**
13. **Permitted file list longer than the inlined pack.** PDF fidelity was not performed this turn, whatever later prose may say.

## What still has to exist before OBJ-001 / 002 / 003 can close

**OBJ-001.** Score Montreal, FH-RS, and SAFEHEART from coefficients **printed in on-disk PDFs**, on **one** frozen extract, with a provenance table (predictors, coefficients, units, endpoint, horizon, derivation cohort). Then recompute both deltas. Today: two conflicting functions, no PDF, two cohorts, two horizons. Not closable.

**OBJ-002.** Recompute **one** comparator four ways: centred / uncentred × 5-year / 10-year S0. Report the four slopes. Today: Julius slopes 0.52–0.57 are asserted, not in `calon_final.json`; local model slope is 1.214, which is a different object. Spec Kit has S0 and a 5.4078 centre; local SAFEHEART has neither. The test is well-posed and not run.

**OBJ-003.** Pearson r(age, cholesterol-years) on the Julius analysis cohort, and a refit replacing cholesterol-years with untreated TC. Today: that term is Julius-only; CALON-F `SPEC` has `cum_nonhdl` and age-splines, not cholesterol-years; the local 0.999 guard does not see it. Not closable from CALON-F artefacts.

---

## Proposed objection blocks

Not written to disk. Step 000 instruction: text only.

```objection
id: OBJ-004
step: 000
raised_by: grok
claim: The two on-disk comparator stacks cannot both be the published equations, and nothing in the delivered artefacts would fail if the local docstring "Published equations, scored not fitted" were false. code/15_CALON_FINAL.py comparators() scores a z-scored linear Montreal, continuous SAFEHEART 0.045*age+0.6*male+0.4*htn+0.3*smoke+0.02*bmi+0.15*ldl+0.25*I(lpa>=105) with HDL/LDL/Lp(a)/BMI imputed, and FH-RS bands plus I(lpa>=105). CALON_JULIUS_SPECKIT/scripts/comparators.py scores a categorical SAFEHEART attributed to Perez de Isla Circulation 2017 Table 3 (age/BMI/LDL mg/dL bands, prior_ASCVD 1.42, lpa>50 mg/dL, S0 0.9532/0.9025, centre 5.4078), an integer Montreal point score, and refuses imputation. STATUS.md further names the head-to-head target SAFEHEART-RE. Three names, at least two functional forms, zero PDF extracts in this pack. Local UKB ALL vs SAFEHEART delta is +0.0058; Julius WIN arithmetic in the QC brief uses SAFEHEART C 0.628 against local 0.6944. That gap is the expected output of scoring different functions, and calon_final.json does not store coefficients, units or thresholds.
settled_by: Locate the comparator PDFs by path or record that they are absent. Extract every coefficient, cut-point and unit from the PDFs into a three-column table (PDF | 15_CALON_FINAL.comparators | Spec Kit). Add a test that asserts local SAFEHEART terms, Montreal terms and FH-RS terms equal the PDF table; the test must fail on the current local function. Separately print local implied comparator C-indices from calon_final.json (model C minus delta) and confirm they match QC-brief local values 0.6944 / 0.6740 / 0.6671.
status: OPEN
```

```objection
id: OBJ-005
step: 000
raised_by: grok
claim: STATUS.md locks UK Biobank n=3,333 / 289 while debate/steps/step-002-QC-BRIEF.md section A treats 3,209 as a number both analyses agree on (3,540 carriers minus 207 prevalent minus 124 undated). 3,333 equals 3,540-207, so STATUS is the cohort before the undated-atherosclerotic exclusion. outputs/calon_final.json as delivered has events and C but no n, so the locked C=0.6997 has no checkable denominator in the pack.
settled_by: Print n from build_ukb() in code/15_CALON_FINAL.py and any n field in outputs/calon_final.json / outputs/calon_final_qc.json. Compute 3540-207 and 3540-207-124. If script n is 3333, report how the 124 undated cases are labelled (excluded / censored / events). If script n is 3209, STATUS.md is stale and must be corrected before it is used as local truth.
status: OPEN
```

```objection
id: OBJ-006
step: 000
raised_by: grok
claim: OBJ-000 is marked ANSWERED on Julius figures (median untreated LDL-C excess +0.226 mmol/L, 2.1% of carriers above 6.5, variant_id empty in all 501936 rows) while the QC brief section B lists the local pipeline at +0.15 median and ~1% above 6.5, and says the specification expected +0.55. An answered objection that still has two live values, plus a third specified value neither pipeline met, is a stamp, not a measurement. STATUS.md continues to call the same people genotype-confirmed HeFH.
settled_by: Recompute, on the frozen extract actually used by code/15_CALON_FINAL.py, (i) median untreated LDL-C in flagged carriers minus non-carriers, (ii) percent of carriers with untreated LDL-C >=6.5 mmol/L, (iii) count of non-empty variant identifiers in that extract (report the count only). Repeat on the Julius extract if it is a different file. OBJ-000 may remain ANSWERED only if both pipelines produce the same pair of figures that are already in its evidence field; otherwise it must be re-opened. Separately replace or justify every "HeFH" label in STATUS.md against those two figures.
status: OPEN
```

```objection
id: OBJ-007
step: 000
raised_by: grok
claim: Wales analysis n is 1,159 / 92 in STATUS.md and calon_final.json versus 1,059 in Julius (QC brief section B) with Julius events not reported. DATA-INVENTORY.md trap 6 documents a date-parse failure that moves the cohort to 948/82, which is neither number. A 100-person gap with no filter ledger means the two pipelines are not yet known to be scoring the same Welsh risk set, so no later Wales C or tally cell from either side can be treated as a replicate of the other.
settled_by: Publish a one-page Wales filter ledger for both pipelines: starting n 7253, then each exclusion (Positive1 vs Mutation1, prevalent ASCVD, undated events, complete follow-up, lipid missingness, date parser) with the n and event count after that line. The two ledgers must be run on the same WALES_FH_CLEANED.csv (inventory SHA-256). If they do not converge to one n and one event count, record the first diverging filter and stop treating Wales C-indices as comparable.
status: OPEN
```

