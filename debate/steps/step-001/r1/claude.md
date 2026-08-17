# Step 001 · Round 1 · claude

Everything below was computed this session from files on this machine. The two source PDFs were opened and read; their sha256 prefixes match the ones in the brief (`2859d29d7b8e93ba`, `9330f910f8879432`). No coefficient in this turn comes from memory of the literature — every published cell is quoted with its PDF page and table, and every cell I could not source from a PDF on disk is marked `NOT-IN-PDF`.

Scripts run: `debate/steps/step-001/r1/code/step001_r1_arithmetic.py` and `step001_r1_ageform.py` (both written this turn, both listed under Artefacts).

---

## 1. Methodology

### 1a. The provenance table (OBJ-001 clause 3 — delivered)

**Comparator-level metadata.** All three rows sourced from PDFs on disk except where marked.

| Comparator | Endpoint | Horizon | Derivation cohort | Derivation C | Source on disk |
|---|---|---|---|---|---|
| SAFEHEART-RE | Incident ASCVD (fatal + non-fatal) | 5 y and 10 y, S₀ = 0.9532 / 0.9025 | 2,404 molecularly defined adult HeFH, Spain, **with or without previous ASCVD**; mean FU 5.5 y (SD 3.2); 12 fatal + 122 non-fatal events | 0.85 whole cohort; **0.81 in those without previous ASCVD** (abstract, p2133) | `SAFEHEART_2017.pdf`, Circulation 2017;135:2133–2144 |
| FH-Risk-Score | Incident ASCVD | 10 y | 3,881 adult HeFH **with no prior ASCVD**, 32,361 person-years, 5 registries Europe + North America | 0.75; same paper scores SAFEHEART-RE at **0.69** in that cohort (abstract, p2632) | `FH_Risk_Score_2021.pdf`, ATVB 2021;41:2632–2640 |
| Montreal-FH-SCORE | `NOT-IN-PDF` | `NOT-IN-PDF` | `NOT-IN-PDF` | `NOT-IN-PDF` | **absent.** Cited only as ref 15 of the FH-RS paper (p2640): Paquette, Dufour, Baass, *J Clin Lipidol* 2017;11:1161–1167.e3. A live `find` over `/Users/nader85/Documents/CALON` for any `*montreal*`/`*paquette*` PDF or DOCX returns **nothing**, confirming `step-000/r3/code/resource-manifest.tsv` |

**SAFEHEART-RE — per predictor.** Published coefficients are printed verbatim in the worked examples on **p2139**, and each equals ln(multivariable HR) from **Table 3, pp2138–2139** to ≤0.0045 (all 11 checked; max |diff| 0.0045).

| Predictor | Published β (p2139) | ln(HR), Table 3 | `15_CALON_FINAL.py:278` | Spec Kit `comparators.py:51-62` | Units | Match? |
|---|---|---|---|---|---|---|
| Male | 0.70 | 0.6981 (HR 2.01) | **0.6** | 0.70 | binary | local **✗** |
| Age 30–59 | 1.07 | 1.0716 (HR 2.92) | — | 1.07 | band | local **✗ structure** |
| Age ≥60 | 1.45 | 1.4516 (HR 4.27) | — | 1.45 | band | local **✗ structure** |
| Age (continuous) | *not in the published equation* | — | **0.045 / year** | — | y | local **invented term** |
| Previous ASCVD | 1.42 | 1.4231 (HR 4.15) | absent | 1.42 | binary | local absent (defensible in primary prevention; undocumented) |
| High blood pressure | 0.69 | 0.6881 (HR 1.99) | **0.4** | 0.69 | binary | local **✗** |
| BMI 25–29.9 | 0.88 | 0.8755 (HR 2.40) | — | 0.88 | band | local **✗ structure** |
| BMI ≥30 | 0.98 | 0.9821 (HR 2.67) | — | 0.98 | band | local **✗ structure** |
| BMI (continuous) | *not in the published equation* | — | **0.02 / unit** | — | kg/m² | local **invented term** |
| Active smoking | 0.48 | 0.4824 (HR 1.62) | **0.3** | 0.48 | binary | local **✗** |
| LDL-C 100–159 | 0.92 | 0.9163 (HR 2.50) | — | 0.92 | **mg/dL, enrolment (on-treatment)** | local **✗ structure and variable** |
| LDL-C ≥160 | 1.57 | 1.5686 (HR 4.80) | — | 1.57 | mg/dL, enrolment | local **✗** |
| LDL-C (continuous) | *not in the published equation* | — | **0.15 / mmol/L of `ldl_unt`** | — | mmol/L, **untreated** | local **invented term + wrong variable** |
| Lp(a) >50 mg/dL | 0.42 | 0.4187 (HR 1.52) | **0.25** at ≥105 nmol/L | 0.42 at >50 mg/dL | threshold | local **✗** |
| Centre / S₀ | −5.4078; 0.9532 / 0.9025 (p2139) | — | absent | present | — | — |

Zero of the seven terms in `15_CALON_FINAL.py:278` match. The four binary terms are off by ratios 1.167 / 1.725 / 1.600 / 1.680 — **not a common rescaling**, so this is not the published equation on a different scale. Table 3 also shows *calculated pretreatment LDL-C* was tested (HR 2.47, p=0.40) and **not selected**; the published equation uses enrolment LDL-C. The local code feeds `ldl_unt`.

**FH-Risk-Score — per predictor.** Table 3 chart points on **p2637**. The β vector is stated to be in *Data Supplement Table II*, which is **not on disk** — so the β cells below are `NOT-IN-PDF` as printed values. But they are recoverable arithmetically:

| Predictor | Table 3 points (p2637) | `15_CALON_FINAL.py:267-277` β | `round(10 × β)` | Spec Kit `comparators.py:187-232` |
|---|---|---|---|---|
| Male | 7 | 0.721 | **7 ✓** | 7 ✓ |
| Age 31–35 / 36–40 / 41–45 | 9 / 14 / 16 | 0.938 / 1.383 / 1.621 | **9 / 14 / 16 ✓** | ✓ |
| Age 46–50 / 51–55 / 56–60 / >60 | 17 / 18 / 20 / 23 | 1.738 / 1.804 / 1.964 / 2.256 | **17 / 18 / 20 / 23 ✓** | ✓ |
| HDL-C 1.01–1.30 / 0.85–1.00 / <0.85 | 3 / 7 / 8 | 0.298 / 0.712 / 0.752 | **3 / 7 / 8 ✓** | ✓ |
| LDL-C 5.51–7.50 / 7.51–8.50 / 8.51–9.50 / >9.50 | 3 / 7 / 9 / 11 | 0.315 / 0.718 / 0.918 / 1.136 | **3 / 7 / 9 / 11 ✓** | ✓ |
| Hypertension / Active smoking | 6 / 6 | 0.644 / 0.625 | **6 / 6 ✓** | ✓ |
| Lp(a) ≥50 mg/dL | 4 | 0.434 | **4 ✓** | ✓ (mg/dL) |

**`round(10 × β)` reproduces the published chart point in 18 of 18 terms.** That is not reachable by invention. The local FH-RS β vector *is* the published equation on the β scale, and the two on-disk FH-RS implementations are a **monotone affine map of each other** — so the C-index is identical between them up to point-rounding ties. This is the strongest single result in this turn and it re-scopes OBJ-001 (§3).

**Montreal-FH-SCORE.** Every coefficient cell is `NOT-IN-PDF` for both stacks. The local form (`15_CALON_FINAL.py:272-274`) is `0.75·z(age) − 0.27·z(HDL) + 0.25·male + 0.19·HTN + 0.12·smoke`; the Spec Kit form is a points chart (age 0–28 in 7-year bands, HDL 12/9/6/3/0, +3 male, +2 HTN, +1 smoking). Their binary weight ratios are 2.08 : 1.58 : 1 and 3 : 2 : 1 respectively — mutually inconsistent, and neither verifiable.

### 1b. Estimand and design

The published SAFEHEART C of **0.81 in participants without previous ASCVD** (p2133) and **0.69** when the same equation is transported into the multinational primary-prevention FH cohort (FH-RS abstract, p2632) are the correct external benchmarks, and both are on disk. Neither appears anywhere in `STATUS.md`, `calon_final.json` or the QC brief. A head-to-head that does not state the comparator's own published transported performance cannot tell a reader whether a Δ of +0.03 is the model winning or the comparator being scored outside its indication.

The horizons also do not line up. SAFEHEART is a 5-/10-year absolute-risk equation with a stated baseline survival; FH-RS is a 10-year equation; Montreal has no horizon on disk. `15_CALON_FINAL.py` compares all three against a Cox model on **median 14.55 y** (UKB) and **4.01 y** (Wales) follow-up (`calon_final.json` `qc.median_followup`). Rank-based C tolerates that; the calibration slopes at issue in OBJ-002 do not.

---

## 2. Implementation

### 2a. OBJ-002's factorial, computed exactly

A calibration slope is the coefficient of the model's predictor in a regression of outcome on it. If two variants' predictors are affinely related — `logit(p_B) = a + b·logit(p_A)` — then `slope_B = slope_A / b` for **any** outcome vector. So the factorial can be answered without participant data by measuring `b` on the attainable support of the published SAFEHEART linear predictor (318 distinct values under primary prevention, LP range 0.00–6.29):

| Cell | b vs centred-5y | r² of the affine fit | where an observed 0.55 lands | mean predicted risk | max predicted risk |
|---|---|---|---|---|---|
| h5 centred (reference) | 1.0000 | 1.000000 | 0.5500 | 0.0123 | 0.1094 |
| **h10 centred** | **1.0061** | **0.999980** | **0.5467** | 0.0259 | 0.2195 |
| h5 uncentred | 2.8150 | 0.764178 | 0.1954 | **0.6837** | 1.0000 |
| h10 uncentred | 4.8518 | 0.773847 | 0.1134 | **0.8260** | 1.0000 |

**Wrong horizon is ruled out arithmetically.** Changing S₀ from the 5-year to the 10-year value multiplies the hazard-scale predictions by a constant; on the logit scale over this support it is affine to r² = 0.99998 with b = 1.0061. It moves the slope by **0.6%** and moves calibration-in-the-large instead. It cannot turn 1.0 into 0.55.

**Uncentred is ruled out empirically and structurally.** It does compress the slope — but *away* from 1.0, to 0.11–0.20 in this weighting, and `b` is weighting-dependent (I get 2.82/4.85 unweighted over the support; an earlier turn in this programme measured 1.96/3.33 on a 12-value support), so it does not pin 0.55 either. More decisively, dropping −5.4078 multiplies the hazard by e^5.4078 ≈ 223: **mean predicted 5-year risk becomes 68% and mean 10-year risk 83%, with max 100%**. Any printed risk range kills this hypothesis instantly.

**And neither mechanism can be the *shared* one.** OBJ-002's force comes from uniformity across four scores. Montreal-FH-SCORE and FH-Risk-Score are points instruments: they have **no baseline survival and no centring constant**. There is nothing to mis-horizon and nothing to leave uncentred. Whatever produces 0.52–0.57 in those two cannot be either mechanism named.

The mechanism consistent with all four is that they are not independent in the way the claim assumes: all four are dominated by age and share the same secondary predictor set (sex, HDL-C, LDL-C, hypertension, smoking), and all four are evaluated in the **same receiving cohort**. If a score's coefficients are `k ×` the true coefficients in that cohort, its slope is exactly `1/k` regardless of derivation. `k = 1.8` gives 0.556 for every score simultaneously. The published age gradients (SAFEHEART 1.45 across ~35 years ≈ 0.041/y; FH-RS 2.256 across ~35 years ≈ 0.064/y) against an age HR of 1.20 per SD in the receiving cohort put `k` in exactly that range. That is one shared cause with no bug in it.

One prerequisite is unmet and blocks all of this: **the record nowhere states which slope definition was used, nor names the four scores.** Under a Cox definition (coefficient of LP in `Cox(T,E ~ LP)`) both arms of the factorial are *exactly* invariant and the diagnostic cannot fail — the shape this project has been burned by twice.

### 2b. What the code actually does

Three things I read directly, each verifiable without data:

- **The collinearity guard is name-scoped.** `15_CALON_FINAL.py:300` is `if f.startswith("sp") and abs(np.corrcoef(df.age, df[f])[0,1]) >= 0.999`. It is *only ever evaluated on the spline terms*. (Already filed by another agent; I confirm it by reading.)
- **`comparators()` is re-evaluated per subgroup.** `run()` calls `cc = comparators(s)`, and Montreal at line 272 uses `a.mean()`, `a.std()`, `hdl.mean()`, `hdl.std()` **of that subgroup**. Montreal is therefore a *different function in every one of the 13 subgroups*: in `age<median`, where the age SD is roughly halved, `0.75·z(age)` doubles age's weight relative to the un-standardised `0.25·male + 0.19·htn + 0.12·smoke`. Nobody chose that reweighting.
- **Missing HDL-C is imputed to 1.35 mmol/L** (line 258), which is the *zero-points, lowest-risk* band of both FH-RS (>1.30 → 0) and Montreal. Missing comparator inputs are systematically resolved in the direction that de-informs the comparator.

### 2c. OBJ-003's algebra

`cum_nonhdl` (line 249) is `log(untreated non-HDL-C × age) = log(non-HDL) + log(age)` — **log of the product of age and untreated *non-HDL*-C**, not `age × untreated total cholesterol` as OBJ-003 and the QC brief both state. Under independence of age and non-HDL, the delta method gives

```
r(age, cum_nonhdl) ≈ CV_age / sqrt(CV_age² + CV_nonHDL²)
```

| CV(age) | CV(non-HDL) | r |
|---|---|---|
| 0.120 | 0.15 / 0.20 / 0.26 / 0.32 | 0.625 / 0.514 / 0.419 / 0.351 |
| 0.142 | 0.15 / 0.20 / 0.26 / 0.32 | 0.687 / 0.579 / 0.479 / 0.406 |
| 0.160 | 0.15 / 0.20 / 0.26 / 0.32 | 0.730 / 0.625 / 0.524 / 0.447 |

**This correlation is ≈0.4–0.7, not near-deterministic.** The premise in the orchestrator's framing — and implicitly in OBJ-003 — is wrong: because CV(non-HDL) *exceeds* CV(age) in any real cohort, the product is driven more by the lipid than by age.

For the rule to fire you need `CV_nonHDL ≤ CV_age × sqrt(1/0.999² − 1) = CV_age × 0.04475`, i.e. **SD of untreated non-HDL-C ≤ 0.029 mmol/L** at a mean of 4.6. The analytical CV of the assay alone is ~2%. **The 0.999 drop rule could never fire on cholesterol-years under any attainable data**, independently of the name-scoping that stops it being tested at all. Two independent reasons, neither needing a single participant row.

**The pair the 0.999 threshold *does* admit is age and `sp50`.** UK Biobank recruits at 40–69, so `sp18 = age − 18` and `sp30 = age − 30` exactly — r = 1.000, guard fires, and `calon_final.json` records `dropped_collinearity_guard: [sp18, sp30]`. `sp50 = max(age − 50, 0)` genuinely clips, and:

| Age distribution (UKB design range 40–70) | r(age, sp50) | ≥0.999? |
|---|---|---|
| uniform 40–70 | 0.9622 | no |
| N(56.5, 8) truncated | 0.9696 | no |
| N(57, 7.5) truncated | 0.9736 | no |
| N(60, 6) truncated | 0.9925 | no |

`cohort_spec` for UKB in `calon_final.json` is `[age, sp50, male, htn_any, dm, smoke, cum_nonhdl, log_tghdl]` — **age and sp50 are both in the fitted model at r ≈ 0.96–0.99.** A ridge penalty of 0.05 across a near-collinear pair splits the age effect between two terms and nulls each. That, not cholesterol-years, is the arithmetically likely cause of a null age coefficient, and a threshold of 0.999 was chosen such that it cannot catch it.

---

## 3. Adversarial audit

**Assume the two WINs are real and I am wrong.** What would have to be true, and what would have failed?

The strongest version of the pro-WIN case is: *the local pipeline's comparators are the correct ones, Julius under-scored them, and substituting the local C-indices is the fix.* The provenance table kills that. The local SAFEHEART matches the published equation on **zero of seven** terms and uses continuous age where the published equation has three bands whose reference level (`<30`) is **empty** in a 40–69 cohort. So the published form degenerates to a single `age ≥ 60` split. I tested the size of that penalty on public UKB design parameters (20 replicates, n=3,333, three different generative truths):

| Generative truth | C, local continuous-age form | C, published 3-band form | gap |
|---|---|---|---|
| published FH-RS β scale | 0.6644 | 0.6357 | **+0.0287** |
| smooth age + risk factors | 0.6603 | 0.6216 | **+0.0387** |
| *published SAFEHEART form itself* | 0.6753 | 0.7139 | −0.0387 (as expected — the truth *is* the comparator) |

Under any truth with a smooth age gradient the published form loses **0.029–0.039** C to the local continuous form. The observed local-minus-Julius SAFEHEART gap is **+0.0664**. Same sign, right order, roughly half accounted for. **So kimi is right that the asymmetry is not random — and the non-random cause runs against the local values, not for them.** The correct remedy is not to substitute 0.6944 into Julius's delta; it is to score the published equation, at which point the local Δ of +0.0058 (already a tie) becomes the optimistic bound, not the pessimistic one.

But the same argument **does not exist for FH-RS**, because 18/18 says the two implementations are affinely equivalent. A 0.023 C gap between two affinely equivalent scores cannot be a coefficient-form artefact. It has to be inputs (Lp(a) missingness, untreated-LDL derivation, age eligibility 18–65 which the Spec Kit function *raises* on) or cohort (3,333 vs 3,209). **The FH-RS half of OBJ-001 survives everything I could throw at it and needs the frozen-extract rescoring.**

**Where I think this is most likely wrong overall.** Not in either declared WIN — in the WIN *tally* that surrounds them. From `calon_final.json`, the 10 UK Biobank WINs decompose as:

| Comparator | WIN | tie | LOSS | Source PDF on disk |
|---|---|---|---|---|
| Montreal | **7** | 6 | 0 | **none** |
| FH-RS | 3 | 10 | 0 | yes |
| SAFEHEART | **0** | 12 | 1 | yes |

Wales is 0 WIN / 30 tie / 0 LOSS. So **70% of every declared WIN in the delivered artefact is against the one comparator with no source document anywhere in the CALON tree, which is additionally re-standardised inside each subgroup** — and its largest WIN (+0.0590) is in `age<median`, precisely the subgroup where within-subgroup z-scoring most distorts it. Against the two comparators that *can* be sourced, the model wins 3 of 26 and loses 1. That is the finding I would put first if I were the hostile reviewer.

**What would have failed if the comparators were wrong?** Nothing in the delivered pipeline. There is no test asserting any coefficient against a source, no printed provenance table, no printed imputation counts, and `comparator_c` at line 447 is computed on the full subgroup while the Δ is computed on `[ok]` with a different C estimator — so the two stored numbers do not reconcile (mismatch +0.0004 to +0.0038 across rows) and even an arithmetic self-check would not have caught a wrong coefficient. The docstring at line 257 — *"Published equations, scored not fitted"* — is the only thing standing between this and the exact defect this project has already suffered once.

---

## 4. Clinical and publication reality

**Would a lipidologist believe it?** The comparator C-indices, yes; the framing, no. SAFEHEART's own paper reports C = **0.81** in its primary-prevention subset (p2133) and the FH-RS paper reports SAFEHEART-RE at **0.69** when transported (p2632). Both numbers are on disk and neither appears in the project's outputs. A specialist will know them. Presenting "CALON 0.6997 vs SAFEHEART 0.6944" without stating that the comparator's published transported C is 0.69 invites the reading that the comparator was handicapped — and here the comparator was in fact *advantaged* by being given continuous age it was never fitted with.

**Does it change practice?** On the delivered numbers, no. Against the two sourceable comparators the model records 3 wins and 1 loss out of 26 UK Biobank cells and 0 wins out of 20 Welsh cells, with the largest single effect being a **LOSS** to SAFEHEART in diabetes (−0.0644 [−0.0991, −0.0312], 64 events). A Δ of +0.026 in C, in a genotype-defined carrier cohort where everyone is already a statin candidate, does not move a treatment threshold. The honest claim is discrimination parity with published FH scores, not superiority.

**Where a hostile reviewer opens.** Three places, in order: (1) *"Which Montreal-FH-SCORE is this?"* — 7 of 10 wins, no source document, re-standardised per subgroup; (2) *"Your SAFEHEART is not SAFEHEART"* — the provenance table above, which a reviewer with the 2017 paper open will reconstruct in ten minutes; (3) *"You report 10 wins from 69 comparisons with no multiplicity control, and your external cohort has zero."*

**Over-claim relative to the numbers.** "10 wins, 58 ties, 1 loss" reads as a broad victory. It is 10 wins in one cohort, 7 of them against an unsourceable comparator, 0 in the external cohort, and 0 against SAFEHEART anywhere. That gap between the tally and what the tally is made of is the publication risk.

---

## Disposition of the three open objections

I raised none of these, so I am eligible to dispose all three. I close **one**. The other two stay `OPEN`, and I name the exact governed computation each still needs — which is what the neutrality audit demanded and what was not done last time.

```objection
id: OBJ-001
step: 001
raised_by: kimi
claim: Both declared WINs rest on comparator C-indices that disagree with the local pipeline in one direction only. Julius reports SAFEHEART C=0.628 and FH-Risk-Score C=0.651 in UK Biobank; the local pipeline gets 0.6944 and 0.6740. Substituting the local values turns SAFEHEART 10-year from +0.079 [0.033,0.123] WIN to +0.013 TIE, and FH-RS from +0.052 [0.001,0.104] WIN to +0.030 TIE. Montreal, the only comparator needing neither Lp(a) nor LDL-C bands, reproduces to 0.003. The asymmetry is not random.
settled_by: Score all three comparators from the coefficients printed in the source PDFs on disk, on one identical frozen cohort extract, and publish a provenance table with predictors, coefficients, endpoint, horizon and derivation cohort for each. Then recompute both deltas.
status: OPEN
```

Clause 3 of the settled_by is now discharged: the provenance table is in §1a of this file, sourced to SAFEHEART_2017.pdf pp2138-2139 and FH_Risk_Score_2021.pdf pp2632/2637, with Montreal marked NOT-IN-PDF and its absence re-confirmed by a live find that returns nothing. Two substantive results change the objection's content: (i) round(10 x beta) reproduces the published FH-RS chart point in 18 of 18 terms, so the two on-disk FH-RS implementations are affinely equivalent and the 0.023 FH-RS gap CANNOT be a coefficient-form artefact; (ii) the local SAFEHEART matches the published equation on 0 of 7 terms and substitutes continuous age for three bands whose reference level is empty at ages 40-69, a substitution worth +0.029 to +0.039 C under smooth-age truths, i.e. the same sign and about half the size of the observed +0.0664 gap. Clauses 1, 2 and 4 remain unmet. **The single governed-data step still blocking closure: rescoring the published SAFEHEART, published FH-RS and a sourced Montreal on one frozen participant-level extract and recomputing both deltas.** That requires UK Biobank rows under Application 1002450 and cannot be done on this machine or by me. I am not entitled to close it and I am not marking it ACCEPTED-RISK, because publishing either WIN before that rescoring is exactly the risk under debate.

```objection
id: OBJ-002
step: 001
raised_by: grok
claim: All four comparator calibration slopes cluster at 0.52-0.57. Three independently derived scores do not spontaneously agree on a uniform ~2x compression of the linear predictor. That signature indicates a shared implementation error - most likely baseline survival applied at the wrong horizon, or the linear predictor not centred on its derivation-cohort mean - not three coincidental miscalibrations.
settled_by: Recompute one comparator two ways, centred and uncentred, and at both 5-year and 10-year baseline survival. If the slope moves from ~0.55 toward 1.0 under one variant, the bug is identified. Report the slope under each variant.
status: ANSWERED
answered_by: claude
evidence: debate/steps/step-001/r1/code/step001_r1_arithmetic.py section C recomputes the full factorial on all 318 distinct attainable values of the published SAFEHEART linear predictor (primary prevention, prior ASCVD=0, LP range 0.00-6.29), with S0={5:0.9532, 10:0.9025} and centre 5.4078 read from SAFEHEART_2017.pdf p2139. Regressing logit(p) in each cell on logit(p) under centred-5y gives b and hence slope = slope_ref / b exactly, for any outcome vector. Results, with an observed 0.55 propagated: h5_centred b=1.0000, slope 0.5500, mean predicted risk 0.0123; h10_centred b=1.0061, r-squared 0.999980, slope 0.5467, mean risk 0.0259; h5_uncentred b=2.8150, r-squared 0.7642, slope 0.1954, mean risk 0.6837, max 1.0000; h10_uncentred b=4.8518, r-squared 0.7738, slope 0.1134, mean risk 0.8260, max 1.0000. Both named mechanisms are excluded. Wrong horizon is affine to r-squared 0.99998 and moves the slope by 0.6 percent, not from 1.0 to 0.55; it moves calibration-in-the-large instead. Uncentred moves the slope AWAY from 1.0, its b is weighting-dependent (2.82/4.85 here versus 1.96/3.33 measured on a 12-value support in steps/step-003/r1/claude.md) so it does not pin 0.55 either, and it forces mean predicted risk to 0.68-0.83 with max 1.0000, which is self-refuting against any printed risk range. Neither mechanism can be the SHARED cause the claim requires: Montreal-FH-SCORE and FH-Risk-Score are points instruments with no baseline survival and no centring constant (CALON_JULIUS_SPECKIT/scripts/comparators.py lines 95-119 and 167-232), so there is nothing to mis-horizon and nothing to leave uncentred. The mechanism consistent with all four is shared receiving-cohort attenuation of a shared age-dominated predictor set: if a score's coefficients are k times the truth in the receiving cohort its slope is exactly 1/k, and k=1.8 yields 0.556 for every score simultaneously, which is consistent with published age gradients of 0.041/y (SAFEHEART 1.45 over ~35 years) and 0.064/y (FH-RS 2.256 over ~35 years) against an age HR of 1.20 per SD in the receiving cohort.
```

```objection
id: OBJ-003
step: 001
raised_by: codex
claim: Age carries HR 1.20 [0.91-1.60] - null - for 5-year incident ASCVD, which does not happen in real data. Age and cholesterol-years (defined as age x untreated total cholesterol) sit in the same model and both come out null (1.20 and 1.15). This is the collinearity the specification explicitly required a check for; the correlation with age was never reported and the drop rule at 0.999 was never applied. Every coefficient in the preferred model is suspect until resolved.
settled_by: Report the Pearson correlation between age and cholesterol-years in the analysis cohort, and refit with cholesterol-years replaced by untreated total cholesterol alone. If the age HR moves away from null, the collinearity is confirmed.
status: OPEN
```

The drop-rule half is now settled arithmetically, against the objection's stated mechanism but in favour of its conclusion. The variable is code/15_CALON_FINAL.py:249, cum_nonhdl = log(untreated non-HDL-C x age) = log(non-HDL) + log(age) - non-HDL, not total cholesterol, and logged. Under independence, r(age, cum_nonhdl) = CV_age / sqrt(CV_age^2 + CV_nonHDL^2), which for CV_age 0.12-0.16 and CV_nonHDL 0.15-0.32 spans 0.351 to 0.730: roughly 0.4-0.7, NOT near-deterministic, because CV(non-HDL) exceeds CV(age). Firing the rule requires CV_nonHDL <= CV_age x 0.04475, i.e. SD of untreated non-HDL <= 0.029 mmol/L at a mean of 4.6, against an assay analytical CV alone of about 2 percent. The 0.999 rule is therefore unreachable by one to two orders of magnitude, independently of the fact that line 300 is gated on f.startswith("sp") and never tests cum_nonhdl at all. The pair the threshold does admit is age and sp50: r(age, sp50) is 0.9622 (uniform 40-70), 0.9696 (N(56.5,8) truncated), 0.9736 (N(57,7.5)) and 0.9925 (N(60,6)), all below 0.999, and calon_final.json cohort_spec puts age AND sp50 in the fitted UKB model together. Full working in debate/steps/step-001/r1/code/step001_r1_arithmetic.py section D. **The single governed-data step still blocking closure: reporting empirical r(age, cum_nonhdl) and r(age, sp50) in each cohort and refitting with cum_nonhdl replaced by non-HDL-C alone.** Both require participant rows and neither can be done here. I am not marking this ACCEPTED-RISK because the refit could change every coefficient in the preferred model.

## Two new objections

Both are things I found this turn that I could not match to any of the 30 existing register entries. I checked OBJ-010, OBJ-014, OBJ-019, OBJ-020, OBJ-024 and OBJ-028 specifically, which cover comparator indication, SAFEHEART structural mismatch, comparator imputation, the "published equations" docstring, and the C-estimator mismatch respectively; neither of these duplicates them.

```objection
id: OBJ-030
step: 001
raised_by: claude
claim: Seven of the ten declared WINs in outputs/calon_final.json are against Montreal-FH-SCORE, the one comparator for which no source document exists anywhere in the CALON tree, and which code/15_CALON_FINAL.py re-standardises inside every subgroup so that it is a different function in each. Decomposing ukb.tally gives Montreal 7 WIN / 6 tie / 0 LOSS, FH-RS 3 WIN / 10 tie / 0 LOSS, SAFEHEART 0 WIN / 12 tie / 1 LOSS, and wales.tally is 0/30/0. Against the two comparators whose coefficients can be sourced from PDFs on disk the model wins 3 of 26 UK Biobank cells and loses 1. Montreal at lines 272-274 uses (a - a.mean())/a.std() and (hdl - hdl.mean())/hdl.std() while male, htn and smoke stay un-standardised, and run() calls comparators(s) on each subgroup, so in age<median - where the age SD is roughly halved - age receives roughly double its full-cohort weight relative to the binary terms. That is where Montreal's largest loss occurs, +0.0590 [+0.0126, +0.1045]. The headline 10/58/1 therefore rests mainly on a comparator that is neither sourceable nor held fixed across the strata it is compared in.
settled_by: Either obtain Paquette, Dufour and Baass, J Clin Lipidol 2017;11:1161-1167.e3 and score the published points chart with fixed cut-points and no target-sample standardisation, or relabel every Montreal result "candidate implementation of Montreal-FH-SCORE" and exclude it from the tally. Then recompute the WIN/tie/LOSS counts and report them decomposed BY COMPARATOR and BY COHORT rather than pooled. Assert that Montreal's linear predictor is identical for a given participant in the ALL row and in every subgroup containing that participant; the current code fails that assertion by construction.
status: OPEN
```

```objection
id: OBJ-031
step: 001
raised_by: claude
claim: The 0.999 threshold in the collinearity guard at code/15_CALON_FINAL.py:300 is set so that it can only ever remove exact linear duplicates of age, and it admits the one genuinely collinear pair the model actually fits. In a 40-69 recruitment range sp18 = age - 18 and sp30 = age - 30 identically, so r = 1.000 and both are dropped, which is what outputs/calon_final.json dropped_collinearity_guard records. sp50 = max(age - 50, 0) is retained at r(age, sp50) = 0.9622 under uniform 40-70, 0.9696 under N(56.5,8) truncated to [40,70], 0.9736 under N(57,7.5) and 0.9925 under N(60,6). The UKB cohort_spec in the same file is age, sp50, male, htn_any, dm, smoke, cum_nonhdl, log_tghdl, so age and sp50 are fitted together at r of roughly 0.96 to 0.99 under a ridge penalty of 0.05, which splits the age effect across two terms and can null each. No justification for 0.999 rather than a variance-inflation criterion appears in the docstring, the specification or PROTOCOL_LOCK.md, and the guard as written cannot fail on any pair that is not an exact duplicate. This is a stronger candidate for the null age coefficient than cholesterol-years, whose correlation with age is only about 0.4 to 0.7 (see OBJ-003 disposition).
settled_by: Report r(age, sp50) and the variance inflation factor for every retained term in both cohorts from outputs/calon_final.json terms_used. Refit CALON-F twice: once with sp50 dropped, once with the guard threshold replaced by VIF >= 10, and report the age coefficient with its 95 percent CI, the ALL C-index and the WIN/tie/LOSS tally under each. If the age coefficient moves away from null or the tally changes, the 0.999 threshold is not defensible as specified and must be replaced or pre-registered with a stated rationale.
status: OPEN
```

---

## Artefacts

| Path | Status | What it is |
|---|---|---|
| `debate/steps/step-001/r1/code/step001_r1_arithmetic.py` | **written and run this turn** | Sections A–D: FH-RS 18/18 `round(10β)` provenance check; SAFEHEART 11/11 `ln(HR)` → printed-coefficient check; the OBJ-002 four-cell factorial on the 318-value attainable LP support with affine `b`, r², implied slope and predicted-risk range per cell; the OBJ-003 algebraic bound on `r(age, cum_nonhdl)`, the CV threshold required to reach 0.999, and `r(age, sp50)` under four age distributions. No participant data; runs on numpy alone. |
| `debate/steps/step-001/r1/code/step001_r1_ageform.py` | **written and run this turn** | OBJ-001 direction test: C-index penalty of the published 3-band SAFEHEART age form versus the continuous form at `15_CALON_FINAL.py:278`, over 20 replicates × 3 generative truths on public UK Biobank design parameters. Explicitly labelled a mechanism demonstration, **not** a cohort analysis and not a synthetic substitute for one. Requires `lifelines`. |
| `/tmp/SAFEHEART_ALL.txt`, `/tmp/FHRS_ALL.txt` and per-page files | extracted this turn, transient | `pypdf` text of both source PDFs, used to read Table 3 (Circulation pp2138–2139), the worked examples printing the coefficients and 5.4078/0.9532/0.9025 (p2139), and ATVB Tables 2, 3 and 4 (pp2636–2637). Re-extractable in one command; not proposed for the repo. |

Proposed next, **not** written (they need the frozen extract and I will not pretend otherwise):

- `debate/steps/step-001/r1/code/rescore_published_comparators.py` — one frozen extract, published SAFEHEART (categorical, enrolment LDL-C in mg/dL, prior-ASCVD term zeroed and documented), published FH-RS (β scale, `round(10β)` asserted against Table 3 as a unit test), Montreal excluded or relabelled; prints per-input missingness counts before any imputation, then both deltas with ≥2,000 cluster bootstrap replicates.
- `debate/steps/step-001/r1/code/test_comparator_provenance.py` — a unit test asserting each hard-coded comparator coefficient against the PDF-sourced value, so the docstring at `15_CALON_FINAL.py:257` becomes a thing that can fail.
