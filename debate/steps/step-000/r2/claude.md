I read the actual files rather than the Round‑1 excerpts. That overturns four Round‑1 claims — including two of my own — and surfaces three defects nobody found.

# Step 000 · Round 2 · CLAUDE

> Round 1 was conducted on excerpts. This turn was conducted on the repository. Every number below was produced by a command against a file in the working tree, and where that contradicts my own Round‑1 position I say so.

## What changed when the files were actually opened

| Round‑1 claim | Agent | Status after reading the file |
|---|---|---|
| `calon_final.json` "has events and C but **no n**" | grok (OBJ-005), codex (ledger) | **False.** `ukb.qc.n = 3333`, `wales.qc.n = 1159`. Their settlement condition is already satisfied by the artefact they were auditing. |
| `participant_level_outputs` is a governance surface needing investigation | **claude** (§2h) | **Withdrawn.** The value is the boolean `False`. A disclosure flag, not data. |
| Wales/no-diabetes/Montreal `delta: 0.0` is a degenerate path — HDL all-missing → `std()==0` → NaN | **claude** (OBJ-008) | **Refuted by me.** Wales HDL completeness is 0.887 and `comparator_c = 0.7244553`, a sane value. My mechanism is dead. |
| Same cell: "the comparator LP is the model's own LP" | kimi (OBJ-008) | **Refuted.** 0.7244553 ≠ 0.7228780. Not the same vector. |
| Subgroups may be getting their own fitted models | codex (OBJ-006) | **Confirmed, and worse than stated.** See §2.1. |

The exact zero has a real explanation, and it is the same mechanism that produces my principal new objection. It is not degenerate. It is arithmetic.

---

## 1. Methodology

### 1.1 The tally's model-C and the manuscript's model-C are two different statistics

`code/15_CALON_FINAL.py:312-352` returns `float(np.mean(cs))` — the **mean over 6 repeats of the per-repeat C-index**. That is `row["c_index"]`, and it is the 0.6997 in `STATUS.md:13`.

`delta_ci` at line 354 computes `concordance_index(t, -a, y)` where `a` is `lp` — the **6-repeat-averaged linear predictor** (`acc/cnt`, line 350). That is the C that decides WIN/LOSS.

C(mean LP) ≥ mean C(LP) by variance reduction. The gap is measurable in the artefact, and it is positive in **every one of the 26 estimable subgroup rows**:

| Cohort | Subgroup | events | reported `c_index` − `comparator_c` | reported `delta` | gap |
|---|---|---|---|---|---|
| ukb | ALL | 289 | +0.03258 | +0.03301 | +0.00043 |
| ukb | male | 175 | +0.03935 | +0.04084 | +0.00149 |
| ukb | age<median | 102 | +0.05735 | +0.05896 | +0.00160 |
| ukb | diabetes | 64 | −0.06816 | −0.06437 | +0.00379 |
| ukb | never smoked | 149 | — | — | +0.00074 |
| wales | no diabetes | 63 | −0.00158 | **0.000000** | +0.00158 |

Never negative, 26/26. That is not noise; it is the ensembling gain, and **the comparator cannot receive it.** The model's score for each participant is the mean of six out-of-fold predictions from six independent fold partitions. The comparator is a deterministic formula scored once. The head-to-head therefore compares a 6-member ensemble against a single point estimate, and the manuscript reports the *lower*, non-ensembled C as the model's performance.

**The exact zero is now explained.** Wales/no-diabetes/Montreal: model 0.7228780 vs Montreal 0.7244553 — Montreal is **better** by 0.00158. The ensembling gain for that cell is +0.00158. It lands on exact integer equality in the concordance numerator, and prints `0.0`. Not a bug in `delta_ci`; the general offset hitting a rational coincidence. Both my hypothesis and kimi's are wrong.

**Two cells where the printed direction contradicts the two printed C-indices:**

- `ukb age<median vs SAFEHEART`: model C 0.72978, SAFEHEART C 0.73107 — the comparator is better — yet `delta: +0.00032`.
- `wales no diabetes vs Montreal`: model C 0.72288, Montreal C 0.72446 — comparator better — yet `delta: 0.0`.

Both are ties, so no verdict flips. But a reviewer who subtracts the two C-indices printed in the same JSON object gets the opposite sign to the delta printed beside them, and there is nothing in the file explaining why.

### 1.2 I quantified the threat to the tally, and it does not overturn it

I checked whether the gain kills any WIN by asking, for each of the 10, whether the bootstrap lower bound exceeds the measured gain:

| Cohort | Subgroup | Comparator | `lo` | gain | survives? |
|---|---|---|---|---|---|
| ukb | ALL | Montreal | +0.0131 | +0.00043 | yes |
| ukb | ALL | FH-RS | +0.0071 | +0.00043 | yes |
| ukb | male | Montreal / FH-RS | +0.0060 | +0.00149 | yes |
| ukb | age<median | Montreal | +0.0126 | +0.00160 | yes |
| ukb | age≥median | FH-RS | +0.0035 | +0.00125 | yes |
| ukb | no statin | Montreal | +0.0022 | +0.00082 | yes |
| ukb | no diabetes | Montreal | +0.0020 | +0.00056 | yes |
| ukb | smoker | Montreal | +0.0065 | +0.00188 | yes |
| ukb | never smoked | Montreal | **+0.00082** | **+0.00074** | **margin 8×10⁻⁵** |

**0 of 10 WINs die.** I am reporting that plainly because it is what the numbers say. But `never smoked vs Montreal` survives by 8×10⁻⁵ against a `repeat_sd` of 0.0027–0.0061 — it is a coin-flip WIN, not a WIN.

### 1.3 The two-specification problem has a cause, and it is a missingness convention

I argued in Round 1 that UK Biobank and Wales fit different models. Confirmed — `terms_used` is 8 in each cohort and they are **not the same 8** (`ukb` drops `sp18`,`sp30`; `wales` drops `dm`,`smoke`). What I missed is *why*.

```python
# build_ukb, lines ~199-201
x["dm"]      = n("diabetes_combined").gt(0).astype(float)
x["smoke"]   = n("smoking_ever").gt(0).astype(float)
x["htn_any"] = ((n("bpmed").fillna(0).gt(0)) | n("sbp").ge(140) | n("dbp").ge(90)).astype(float)
```
```python
# build_wales, lines ~236-240
x["smoke"] = sm.where(sm.isin([0, 1]))     # NaN preserved
x["dm"]    = dm.where(dm.isin([0, 1]))     # NaN preserved
```

`NaN.gt(0)` is `False`. So in UK Biobank every missing diabetes, smoking and hypertension value silently becomes **absent**; in Wales the same three preserve `NaN`. `outputs/calon_final_qc.json` duly reports `ukb.completeness.dm = 1.0`, `.smoke = 1.0`, `.htn_any = 1.0` against `wales` 0.584 / 0.736 / 1.0.

Those 1.0s are manufactured. The completeness metric is computed downstream of the fill, so **it cannot report incompleteness for the three variables most likely to be incomplete.** This is the shape the mandate names: a check whose condition makes failure impossible.

It also drives F7. `usable()` counts events by level on the *filled* variable, so in UK Biobank the whole missing-diabetes population sits in the `dm=0` stratum, `min(e0,e1)` is inflated, and the rule can never fire. `STATUS.md:36-39` presents F7 as "mechanical, not a post-hoc choice… fires on `dm`, `smoke` in Wales only." It fires in Wales only because Wales is the only cohort that admits to having missing data.

### 1.4 Informative censoring of the heart-failure-only group

`build_ukb`: `end = ev.where(incident | hf_only, death.fillna(STUDY_END))`. The 62 heart-failure-only participants are censored **at their heart-failure date** with `E=0`. Heart failure is strongly prognostic of subsequent atherosclerotic events; removing that person-time at the moment risk becomes visible violates the non-informative censoring assumption of both the Cox fit and Harrell's C. `STATUS.md:26-31` presents this as the endpoint *correction* and reports it raised C from 0.6940 to 0.6996. The correction to the endpoint definition is right. The censoring rule chosen to implement it is not the only option and is not the neutral one — censoring at study end, or a competing-risks formulation, would not discard 17.7% of the original event set's high-risk follow-up.

### 1.5 What still blocks OBJ-001/002/003

- **OBJ-001** — unchanged and unclosable: no comparator PDF is in the tree. **New requirement:** the settlement must specify identical missing-data handling, because the published categorical forms need BMI (Welsh completeness **0.455**), smoking (**0.736**) and diabetes (**0.584**). The local continuous SAFEHEART carries BMI at coefficient 0.02, so it is nearly immune to 54.5% missing BMI; the Spec Kit categorical form carries BMI bands at 0.88/0.98 and would be crippled by it. Scoring the published form in Wales as specified would **degrade the comparators and manufacture WINs where there are currently none.** That inverts the direction kimi's OBJ-001 assumes.
- **OBJ-002** — cannot be settled from local artefacts at all. `outputs/calon_final_qc.json` contains **no comparator calibration slopes**; the 0.52–0.57 cluster is Julius-only. The local model slopes are `ukb [1.214, 1.017, 1.411]` and `wales [1.257, 0.940, 1.575]` — and see §2.3, they describe the wrong model. codex is right that additive centring moves the intercept, not the slope; kimi is right that dividing Montreal by the cohort SD *does* rescale the slope. Both mechanisms are live and the proposed test separates neither without an affine-invariance check first.
- **OBJ-003** — the mechanism is now confirmed in local code. `SPEC` contains `cum_nonhdl`, defined at `_finish` as `log(nonhdl_unt × age)` — an explicit age product. The guard at line 300 is gated on `f.startswith("sp")` and cannot see it. Age enters through `age`, `sp50` and `cum_nonhdl` with no correlation ever computed. This is the same construct as Julius's cholesterol-years.

---

## 2. Implementation

### 2.1 codex's OBJ-006 is correct, and the docstring is false as written

`usable()` docstring, line 293: *"Applied ONCE to the full cohort; the resulting spec is then held fixed across every subgroup, so no subgroup gets its own model."* `run()` line 419 repeats it.

What `resolve=False` fixes is the **variable list**. Line 434 then calls `cv(s, cohort_spec, resolve=False)`, and `cv` fits `CoxPHFitter(penalizer=0.05)` on that subgroup's training folds (line 340), imputes with that subgroup's training-fold medians (line 333), and standardises with that subgroup's training-fold mean and SD (lines 335-338). **Every subgroup gets its own coefficients, its own imputation constants and its own scaling.** codex identified this from a truncated excerpt and was right; the docstring's claim is true only of variable selection, and it is written so a reader concludes the stronger thing.

I disagree with one part of codex's framing: the fit-count instrumentation test proposed in their OBJ-006 will not "require zero additional model fits", because refitting is the design. The correct settlement is to relabel: these are 13 stratum-specific models sharing one variable list, not one model evaluated in 13 strata.

### 2.2 The governance instrument cannot enforce its own headline rule

`debate/bin/consensus.mjs` counts rounds from disk:

```js
const turns = readdirSync(stepDir).filter(f => /^r\d+-/.test(f));
rounds = turns.reduce((mx, f) => Math.max(mx, parseInt(f.match(/^r(\d+)/)[1], 10)), 0);
```

The directories on disk are `r1`, `r1b`, `r2`, `r2.default-models-aborted-220652`. The regex requires `r`, digits, then a **hyphen**. Run against the real tree:

```
entries: ["PROMPT_R1.md","PROMPT_R2.md","r1","r1b","r2","r2.default-models-aborted-220652"]
matched by /^r\d+-/ : []
rounds computed = 0
```

`rounds` is **0 and always will be**. The verdict line is `code = rounds >= MAX_ROUNDS ? 2 : 1`. With `MAX_ROUNDS = 4` and `rounds` pinned at 0, **exit code 2 is unreachable and DEADLOCK can never be written.** `open-questions.md` states as rule 5: *"MAX_ROUNDS is enforced in code. Hitting it writes DEADLOCK."* It is not enforced. The file's own preamble says closure "is computed from the objection register, never asserted" precisely because *"two quality checks whose condition was the constant `True` printed PASS for weeks."* The instrument built to prevent that failure contains that failure.

Live output confirms the register state as well: step 000 reports `objections_total: 1`, `by_status: {OPEN: 0, ANSWERED: 1, …}`. **OBJ-000 contributes nothing to `open`.** My Round‑1 claim that its ANSWERED status retires an objection whose evidence confirms it is now demonstrated by execution, not inferred: the only thing blocking step 000 is `agents.size < 2`.

### 2.3 `outputs/calon_final_qc.json` is stale, and `STATUS.md`'s only calibration number describes the retracted model

| File | mtime |
|---|---|
| `code/15b_QC_ADDENDUM.py` | 2026-08-13 19:22 |
| **`outputs/calon_final_qc.json`** | **2026-08-13 21:17** |
| `code/15_CALON_FINAL.py` | 2026-08-13 21:29 |
| `STATUS.md` | 2026-08-13 21:51 |
| `outputs/calon_final.json` | 2026-08-13 22:21 |

The QC JSON predates the current analysis script by 12 minutes. Its contents prove the specification differed:

```
current SPEC (10): age, sp18, sp30, sp50, male, htn_any, dm, smoke, cum_nonhdl, log_tghdl
qc completeness keys (12): … + hdl, bmi
qc features/usable (10): age, sp50, male, cum_nonhdl, log_tghdl, hdl, dm, smoke, htn_any, bmi
EXTRA in qc, absent from current SPEC: ['hdl', 'bmi']
```

`15b_QC_ADDENDUM.py:73` calls `cf.cv(d, cf.SPEC)` — it reads `SPEC` from the analysis module. So the slope was computed when `SPEC` still carried **BMI and HDL-C**: the specification `STATUS.md:79-84` records as retracted for outcome-informed selection.

`STATUS.md:33` states: *"UK Biobank calibration slope is 1.214 (1.017, 1.411) — the interval no longer covers 1."* That is `calon_final_qc.json.ukb.calibration_slope` verbatim, from the 12-term model. **No calibration statistic exists anywhere on disk for the 8-term model that produced C = 0.6997 and the 10/58/1 tally.** The corroborating detail: `epv = 36.125 = 289/8` in `calon_final.json`, against 289/10 = 28.9 for the QC file's spec.

This retracts a component of my own Round‑1 argument. I used "the model's slope is 1.214, above 1, whilst comparators sit at 0.52–0.57" to argue against grok's shared-bug hypothesis in OBJ-002. That comparison was between Julius's comparators and a **superseded** local model. It does not bear on OBJ-002 and I withdraw it.

### 2.4 UK Biobank clustering is asserted, not measured

`build_ukb`, line 204: `x["cluster"] = np.arange(len(x))  # population-ascertained: unrelated`. Wales uses a genuine family key (`kish_effective_clusters` 442.9 against n = 1,159). UK Biobank gets `kish = 3333.0` — exactly n, i.e. no clustering at all.

`cluster` is the bootstrap resampling unit in `delta_ci` (line 356) and the fold-assignment unit in `cv` (line 322). **Every confidence interval behind all 10 WINs assumes complete independence among 3,333 LDLR variant carriers.** `CLAUDE.md` §2 lists kinship as GENUINELY MISSING with the explicit workaround *"otherwise disclose precision may be mildly overstated."* Carriers of the same LDLR variant are enriched for relatedness by founder effect; the comment is a hypothesis in a code comment doing load-bearing statistical work. A WIN is `lo > 0`, and three of the ten have `lo ≤ 0.0022`.

### 2.5 Constants now recovered, answering my own Round‑1 asks

`SEED = 20260813` (single), `REPEATS = 6`, `BOOT = 1200`, `MIN_EVENTS = 10`, `CoxPHFitter(penalizer=0.05)`. The ridge penalty is a **hard-coded constant with no tuning procedure anywhere** — which is a named candidate for over-shrinkage, though §2.3 means the slope evidencing it belongs to another model. `delta_ci` also drops any bootstrap replicate with `y[tk].sum() < MIN_EVENTS` and returns `None` if fewer than 200 of 1,200 survive; the percentile CI is therefore conditioned on high-event resamples. In UK Biobank subgroups (≥64 events) this will rarely bind; it is a real conditioning in the smaller Welsh strata.

### 2.6 The 124 undated cases: mechanism confirmed, no exclusion exists

`grep -n "undated" code/15_CALON_FINAL.py` returns nothing. The only exclusion is `prevalent = ev.notna() & base.notna() & ev.le(base) & athero`, which requires a date. A participant with `athero == True` and `ascvd_first_date_best` missing falls through every branch: not `prevalent`, not `incident`, not `hf_only`, so `end = death.fillna(STUDY_END)` and `E = 0`. **They are retained as controls with full follow-up to 2023-12-31.** kimi (OBJ-006), grok (OBJ-005), codex (OBJ-009) and I all flagged 3,333 vs 3,209 from arithmetic; the code confirms the worst of the three dispositions, and `ukb.qc.n = 3333` in the artefact settles which branch the pipeline took.

---

## 3. Adversarial audit

**Assume the resource base is clean enough to proceed to step 001. What most likely makes that wrong?**

Round 1 converged, blind and 4/4, on comparator provenance. I still think that is the largest single exposure — but it is now the *examined* one, and the panel is about to spend three steps on it. The unexamined exposure is that **the model side of the comparison is not one object.** Three distinct facts, each verified above, all point the same way:

1. The C reported to the reader (`np.mean(cs)`) is not the C that decides the verdict (`C` of the averaged LP), and the difference is positive in 26/26 cells.
2. The model is refitted, re-imputed and re-standardised inside every subgroup while the comparator formula is frozen.
3. The model's out-of-fold prediction is a 6-member ensemble; the comparator is not and structurally cannot be.

If the head-to-head is wrong, this is the most likely reason, and it is invisible to every settlement condition currently on the register — OBJ-001, OBJ-002 and OBJ-003 all interrogate the comparator or the coefficient, never the model's evaluation machinery.

**What would have failed if this were right?** Nothing. `calon_final.json` stores `c_index` and `delta` side by side in the same object, computed from different statistics, with no reconciliation and no assertion. I subtracted them and the residual was positive 26 times out of 26. That took one command.

**And what did I find that argues the other way?** The honest counter to my own case: the gain is small (0.0004–0.0038), 0 of 10 WINs die under it, and the largest gain (+0.0038) is in the diabetes cell, where it makes the model's single **LOSS look less bad** than the raw C-indices imply (−0.0644 reported against −0.0682 implied). The mechanism is not uniformly self-serving. It is uniformly *directional*, which is a reproducibility defect, not proof of a manufactured result.

**Where I attacked and the artefact held.** Tally arithmetic reconciles exactly (39 + 39 = 78 = 2 × 13 × 3; 10+28+1+0 and 0+30+0+9). Event counts, person-years, C-indices and n in `STATUS.md` match `calon_final.json` to the digit. `fold_failures = 0` in both cohorts, so `ok` is all-True and the `comparator_c`-vs-delta risk-set concern I raised in Round 1 does not bite on this run. The `-cc[cn]` sign convention in `concordance_index` is correct. `leak_detector_tx_alone_C` is 0.592 (ukb) and 0.492 (wales) — a real diagnostic with a real threshold that could have failed and did not. `unexpected_signs` is empty in both. The endpoint construction (I21/I25/I63/I70/I73/G45, I50 excluded) matches `CLAUDE.md` §0a's verified guidance and correctly uses `corrected_ascvd_outcomes.csv` rather than `prevalent_ascvd`. That last point is worth stating plainly: on the field-provenance question that has burned this project before, `code/15` is one of only two scripts doing it right.

---

## 4. Clinical and publication reality

**I agree with kimi's OBJ-007 and it is the sharpest publication objection on the table.** Verified: `ukb.tally = {WIN: 10, tie: 28, LOSS: 1, non_estimable: 0}`; `wales.tally = {WIN: 0, tie: 30, LOSS: 0, non_estimable: 9}`. All ten wins are in the development cohort. `STATUS.md:22-24` pools them into "10 wins, 58 ties, 1 loss of 69 estimable cells" and never states the split. In the cohort that is unambiguously a genotype-confirmed FH registry, the model wins nothing and 9 of 39 cells were too small to estimate.

**Where a hostile reviewer now opens, in order:**

1. **"Your calibration slope is for a different model."** §2.3. `STATUS.md` reports a single calibration statistic for CALON‑F and it was computed with BMI and HDL-C in the specification — the terms the same document says were removed for outcome-informed selection. The locked model has **no reported calibration at all**. For a prediction model this is not a detail; TRIPOD requires calibration of the model being presented, and a reviewer who checks the mtimes finds the QC artefact is older than the code.
2. **"Which C did you compare?"** §1.1. Two cells print a positive or zero delta while the two C-indices in the same object say the comparator is better.
3. **"Your UK Biobank participants are all unrelated?"** §2.4. In LDLR carriers, asserted in a code comment, with the project's own inventory recording kinship as unavailable.
4. **Comparator provenance** — Round 1's unanimous finding, unchanged. Still no PDF in the tree.
5. **`n = 3,333` includes 124 people with known atherosclerotic disease coded as controls with full follow-up** (§2.6).
6. **The subgroups where it matters.** `on statin` C = 0.612 (131 events), `diabetes` C = 0.559 (64 events, the sole loss), Welsh `hypertensive` C = 0.558 (52 events). Treated, diabetic, hypertensive FH patients are the population a clinic actually has to triage, and the model is near-chance in all three.
7. **`STATUS.md:24` says the diabetic loss is −0.062; the artefact says −0.0643716927.** Trivial alone; read alongside item 1 it establishes that the status document was typed rather than generated.

**Would a lipidologist believe it?** They will not reach the statistics. `STATUS.md:13` calls the UK Biobank arm "genotype-confirmed HeFH" while the register's own OBJ-000 evidence records an untreated LDL-C excess of +0.226 mmol/L and 2.1% above 6.5 mmol/L. That is a population carrier cohort. Grok and I reached this independently in Round 1 and the file has not moved.

**What survives today.** A pre-specified 7-variable incident-ASCVD model achieving internally cross-validated C ≈ 0.70 in UK Biobank LDLR carriers and ≈ 0.75 in the All-Wales FH registry, each fitted to its own cohort with a partly different term set; **statistically indistinguishable from three published FH scores in every one of the 30 estimable Welsh cells**; near-chance in treated, diabetic and hypertensive strata; with no calibration statistic yet computed for the locked specification. The UK Biobank head-to-head should not be quoted at all until §1.1 and OBJ-001 are settled.

---

## Objections

> **Numbering note.** The register on disk (verified by running `consensus.mjs`) contains only OBJ-000 through OBJ-003; no Round‑1 proposal was merged. I have used OBJ-004 onward per the orchestrator's instruction, but codex, kimi and grok each proposed different objections under those same ids in Round 1. The orchestrator must renumber on merge.

```objection
id: OBJ-004
step: 000
raised_by: claude
claim: debate/bin/consensus.mjs cannot enforce MAX_ROUNDS and can never emit DEADLOCK. It counts rounds with readdirSync(stepDir).filter(f => /^r\d+-/.test(f)), which requires a hyphen after the digits, but the round directories on disk are named r1, r1b, r2 and r2.default-models-aborted-220652. Executed against debate/steps/step-000 the filter matches zero entries and rounds evaluates to 0. The verdict line is code = rounds >= MAX_ROUNDS ? 2 : 1, so with MAX_ROUNDS=4 and rounds pinned at 0, exit code 2 is unreachable for every step regardless of how many rounds are actually run. state/open-questions.md rule 5 states "MAX_ROUNDS is enforced in code. Hitting it writes DEADLOCK", and the module preamble justifies existing as code because "two quality checks whose condition was the constant True printed PASS for weeks". This is that failure, in the instrument built to prevent it.
settled_by: Run node -e "const{readdirSync}=require('fs');const f=readdirSync('debate/steps/step-000');console.log(JSON.stringify(f.filter(x=>/^r\d+-/.test(x))))" and confirm it prints []. Then run node debate/bin/consensus.mjs --step 000 --json and confirm the rounds field is 0 despite two completed rounds on disk. Fix the pattern to /^r(\d+)/ or rename round directories to the r1-<name> form, then re-run and confirm rounds equals 2 and that setting --max-rounds 1 yields verdict DEADLOCK with exit code 2.
status: OPEN
```

```objection
id: OBJ-005
step: 000
raised_by: claude
claim: The C-index that decides every WIN/LOSS verdict is not the C-index reported as the model's performance, and the difference systematically favours the model. code/15_CALON_FINAL.py:312-352 returns float(np.mean(cs)), the mean of six per-repeat C-indices, which becomes row["c_index"] and STATUS.md's 0.6997. delta_ci at line 354 instead computes concordance_index on lp, the six-repeat-AVERAGED linear predictor (acc/cnt, line 350). Averaging six out-of-fold predictions reduces prediction variance, so C(mean LP) exceeds mean C(LP). Computed from outputs/calon_final.json, delta minus (c_index minus comparator_c) is positive in 26 of 26 estimable rows, ranging +0.00043 (ukb ALL) to +0.00379 (ukb diabetes). The comparator is a deterministic formula scored once and structurally cannot receive this ensembling gain, so the head-to-head compares a six-member ensemble against a point estimate. Two cells print a delta whose sign contradicts the two C-indices stored beside it: ukb age<median vs SAFEHEART (model 0.72978, SAFEHEART 0.73107, delta +0.00032) and wales no diabetes vs Montreal (model 0.72288, Montreal 0.72446, delta exactly 0.0 - which also refutes both Round-1 hypotheses for that zero, since Montreal's C is a sane 0.7244553 and is not the model's own LP). I verified this does not currently overturn the tally: 0 of 10 WINs have a lower bound below their cell's gain. But never smoked vs Montreal survives by 8e-05 (lo +0.00082 vs gain +0.00074) against a repeat_sd of 0.0027-0.0061.
settled_by: Recompute all 78 cells two ways and publish both tallies: (a) delta_ci called with a single-repeat out-of-fold LP, matching the reported c_index definition; (b) the current averaged LP, with row["c_index"] redefined as concordance_index on that same averaged LP so the printed C and the printed delta are the same statistic. Report, for each of the 10 WINs, the verdict under (a). Separately state which definition the manuscript will report, and confirm the never smoked vs Montreal cell's verdict across at least ten seeds.
status: OPEN
```

```objection
id: OBJ-006
step: 000
raised_by: claude
claim: The completeness QC cannot report incompleteness for the three variables most likely to be incomplete in UK Biobank, because missingness is converted to "absent" before the metric is computed. code/15_CALON_FINAL.py build_ukb sets x["dm"] = n("diabetes_combined").gt(0).astype(float), x["smoke"] = n("smoking_ever").gt(0).astype(float) and x["htn_any"] = ((n("bpmed").fillna(0).gt(0)) | n("sbp").ge(140) | n("dbp").ge(90)).astype(float). NaN.gt(0) is False, so every missing value becomes 0 and the column can never contain NaN. outputs/calon_final_qc.json accordingly reports ukb.completeness.dm = 1.0, .smoke = 1.0 and .htn_any = 1.0. build_wales does the opposite for two of the three - x["smoke"] = sm.where(sm.isin([0,1])) and x["dm"] = dm.where(dm.isin([0,1])) preserve NaN - and reports 0.736 and 0.584. The two cohorts therefore use different missing-data conventions for the same variables with no disclosure. This also drives the F7 minimum-information rule, which counts events by level on the filled column at line 304-305: in UK Biobank the entire missing-diabetes population is pooled into the dm=0 stratum, inflating e0 so the rule cannot fire. STATUS.md lines 36-39 presents F7 as "mechanical, not a post-hoc choice" firing "on dm, smoke in Wales only"; it fires in Wales only because Wales is the only cohort that admits missingness. This is the proximate cause of the two cohorts fitting different 8-term specifications.
settled_by: Print, from the raw UK Biobank master before any fill, the non-missing counts and fractions for diabetes_combined, smoking_ever, bpmed, sbp and dbp among the 3,333 analysed carriers, and compare each against the 1.0 recorded in outputs/calon_final_qc.json. Then rebuild UK Biobank preserving NaN in dm, smoke and htn_any exactly as build_wales does, re-run usable(), and report which terms F7 drops in each cohort and whether the two cohort specifications converge. Report the ALL C-index in both cohorts under the harmonised convention against the current 0.6997 and 0.7486.
status: OPEN
```

```objection
id: OBJ-007
step: 000
raised_by: claude
claim: outputs/calon_final_qc.json describes a model specification that no longer exists, and STATUS.md quotes its calibration slope as the locked model's. The QC file's ukb.completeness has 12 keys including hdl and bmi, and ukb.features (the usable() output) is ['age','sp50','male','cum_nonhdl','log_tghdl','hdl','dm','smoke','htn_any','bmi'] - 10 terms including both. The current SPEC in code/15_CALON_FINAL.py has 10 terms and contains neither hdl nor bmi, resolving to 8 (confirmed by outputs/calon_final.json ukb.qc.terms_used and epv 36.125 = 289/8; the QC spec would give 289/10 = 28.9). code/15b_QC_ADDENDUM.py line 73 calls cf.cv(d, cf.SPEC), reading SPEC from the analysis module, so the QC file was generated while SPEC still carried BMI and HDL-C - the specification STATUS.md lines 79-84 records as retracted for outcome-informed selection. mtimes confirm the ordering: calon_final_qc.json 2026-08-13 21:17, code/15_CALON_FINAL.py 21:29, STATUS.md 21:51, calon_final.json 22:21. STATUS.md line 33 states "UK Biobank calibration slope is 1.214 (1.017, 1.411) - the interval no longer covers 1", which is calon_final_qc.json ukb.calibration_slope verbatim. No calibration statistic exists on disk for the 8-term model that produced C=0.6997 and the 10/58/1 tally, so the model being presented has no reported calibration at all.
settled_by: Re-run code/15b_QC_ADDENDUM.py against the current code/15_CALON_FINAL.py SPEC and publish the regenerated outputs/calon_final_qc.json. Confirm features has 8 entries matching outputs/calon_final.json ukb.qc.terms_used and that completeness has 10 keys with neither hdl nor bmi. Report the recomputed calibration slope and 95% interval for both cohorts, and correct or retract STATUS.md line 33. Add an assertion to 15b that aborts if its resolved feature list differs from the terms_used recorded in outputs/calon_final.json.
status: OPEN
```

```objection
id: OBJ-008
step: 000
raised_by: claude
claim: Every confidence interval behind all 10 WINs assumes 3,333 mutually unrelated participants, on the strength of a code comment rather than a measurement. code/15_CALON_FINAL.py build_ukb line 204 sets x["cluster"] = np.arange(len(x)) with the comment "population-ascertained: unrelated", giving each participant a unique cluster; outputs/calon_final.json records ukb.qc.kish_effective_clusters = 3333.0, exactly n. build_wales instead uses a genuine family key and gets 442.89 effective clusters from 1,159 participants. cluster is the resampling unit in delta_ci (line 356) and the fold-assignment unit in cv (line 322), so it sets both the CI width and the leak-free split. CLAUDE.md section 2 lists KING/kinship as GENUINELY MISSING with the stated workaround "otherwise disclose precision may be mildly overstated", so the project's own inventory records that this cannot currently be verified. LDLR carriers are enriched for relatedness by founder effect, which is the specific case where the assumption fails. A WIN is declared when the bootstrap lower bound exceeds zero, and three of the ten have lo <= 0.0022 (no statin vs Montreal +0.0022, no diabetes vs Montreal +0.0020, never smoked vs Montreal +0.00082).
settled_by: Report the number of related pairs at 3rd degree or closer among the 3,333 analysed UK Biobank carriers, as an aggregate count only, from any available kinship resource; if none is available, state that in STATUS.md as a stated limitation on precision. Then re-run delta_ci with clusters defined by any available relatedness grouping, or as a sensitivity by variant identity, and report the revised lower bound and verdict for all 10 WIN cells against the current values.
status: OPEN
```

```objection
id: OBJ-009
step: 000
raised_by: claude
claim: The heart-failure endpoint correction is implemented with informative censoring. code/15_CALON_FINAL.py build_ukb sets hf_only = ev.notna() & base.notna() & ev.gt(base) & ~athero and then end = ev.where(incident | hf_only, death.fillna(STUDY_END)), so the 62 heart-failure-only participants are assigned E=0 and censored at their heart-failure date. Heart failure is strongly prognostic of subsequent atherosclerotic events, so removing their follow-up at the moment their risk becomes manifest violates the non-informative censoring assumption underlying both the Cox partial likelihood and Harrell's C. STATUS.md lines 26-31 presents this as the endpoint correction and reports it raised discrimination from 0.6940 to 0.6996 and reintroduced the diabetic loss. Excluding I50 from the endpoint is right; censoring at the I50 date is one implementation among several and is the one that discards the most high-risk person-time, and no sensitivity analysis against the alternatives is reported anywhere in the repository.
settled_by: Re-run code/15_CALON_FINAL.py under three dispositions of the 62 heart-failure-only participants - censored at heart-failure date as now, censored at death or STUDY_END, and handled as a competing risk - and report the ALL C-index, the calibration slope and the full combined_tally under each. If the tally or the diabetic loss changes across dispositions, report all three in the manuscript rather than only the current one.
status: OPEN
```

---

## Artefacts

Reproduces every number in this turn. Read-only, aggregate output only, no participant rows.

```bash
# 1. OBJ-004 — the round counter never matches (governance instrument)
cd debate
node -e "const{readdirSync}=require('fs');const f=readdirSync('steps/step-000');
console.log('entries:',JSON.stringify(f));
console.log('matched:',JSON.stringify(f.filter(x=>/^r\d+-/.test(x))));"
node bin/consensus.mjs --step 000 --json   # inspect the .rounds field
```

```python
# 2. OBJ-005 — the ensembling gap, and which WINs it threatens
#    proposed path: debate/steps/step-000/r2/code/verify_ensembling_gap.py
import json
d = json.load(open('outputs/calon_final.json'))
rows = []
for coh in ('ukb', 'wales'):
    for lab, r in d[coh]['subgroups'].items():
        for cn, v in r['vs'].items():
            gap = v['delta'] - (r['c_index'] - v['comparator_c'])
            rows.append((coh, lab, cn, r['events'], v['delta'], v['ci'][0], gap, v['verdict']))
assert all(g > 0 for *_, g, _ in rows), "gap should be positive in every cell"
print("cells:", len(rows), " positive gaps:", sum(1 for *_, g, _ in rows if g > 0))
for c, l, n, e, dl, lo, g, vd in rows:
    if vd == 'WIN':
        print(f"{c:6}{l:14}{n:10}{e:5d} delta={dl:+.5f} lo={lo:+.5f} gap={g:+.5f} "
              f"{'MARGINAL' if lo - g < 5e-4 else ''}")
```

```python
# 3. OBJ-006 — completeness is measured downstream of the fill
#    proposed path: debate/steps/step-000/r2/code/verify_manufactured_completeness.py
#    Run inside the analysis environment; prints aggregate fractions only.
import pandas as pd, numpy as np, importlib
cf = importlib.import_module('code.15_CALON_FINAL')
U = cf.build_ukb()
for f in ('dm', 'smoke', 'htn_any'):
    print(f"{f:9} post-build completeness = {U[f].notna().mean():.4f}  "
          f"fraction coded 0 = {(U[f] == 0).mean():.4f}")
# compare against raw non-missing rates for diabetes_combined / smoking_ever /
# bpmed+sbp+dbp in the same 3,333 rows; any gap is the manufactured 1.0.
```

```bash
# 4. OBJ-007 — the QC artefact predates the code that defines its specification
stat -f "%Sm  %N" -t "%Y-%m-%d %H:%M" \
  outputs/calon_final_qc.json code/15_CALON_FINAL.py STATUS.md outputs/calon_final.json
python3 -c "
import json,re
q=json.load(open('outputs/calon_final_qc.json'))
spec=re.search(r'SPEC = \[(.*?)\]',open('code/15_CALON_FINAL.py').read(),re.S).group(1)
spec=[s.strip().strip('\"') for s in spec.replace(chr(10),' ').split(',') if s.strip()]
print('stale terms in QC, absent from current SPEC:',
      [k for k in q['ukb']['completeness'] if k not in spec])"
```

**Proposed new files** (none written this turn): `debate/steps/step-000/r2/code/verify_ensembling_gap.py`, `verify_manufactured_completeness.py`, `verify_qc_spec_drift.py`, and a one-line patch to `debate/bin/consensus.mjs` changing the round-count filter from `/^r\d+-/` to `/^r\d+/`.
