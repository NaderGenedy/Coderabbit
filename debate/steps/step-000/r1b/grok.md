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
