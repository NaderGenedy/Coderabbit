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
status: ANSWERED
evidence: debate/steps/step-001/r1/code/step001_r1_arithmetic.py section C recomputes the full factorial on all 318 distinct attainable values of the published SAFEHEART linear predictor (primary prevention, prior ASCVD=0, LP range 0.00-6.29), with S0={5:0.9532, 10:0.9025} and centre 5.4078 read from SAFEHEART_2017.pdf p2139. Regressing logit(p) in each cell on logit(p) under centred-5y gives b and hence slope = slope_ref / b exactly, for any outcome vector. Results, with an observed 0.55 propagated: h5_centred b=1.0000, slope 0.5500, mean predicted risk 0.0123; h10_centred b=1.0061, r-squared 0.999980, slope 0.5467, mean risk 0.0259; h5_uncentred b=2.8150, r-squared 0.7642, slope 0.1954, mean risk 0.6837, max 1.0000; h10_uncentred b=4.8518, r-squared 0.7738, slope 0.1134, mean risk 0.8260, max 1.0000. Both named mechanisms are excluded. Wrong horizon is affine to r-squared 0.99998 and moves the slope by 0.6 percent, not from 1.0 to 0.55; it moves calibration-in-the-large instead. Uncentred moves the slope AWAY from 1.0, its b is weighting-dependent (2.82/4.85 here versus 1.96/3.33 measured on a 12-value support in steps/step-003/r1/claude.md) so it does not pin 0.55 either, and it forces mean predicted risk to 0.68-0.83 with max 1.0000, which is self-refuting against any printed risk range. Neither mechanism can be the SHARED cause the claim requires: Montreal-FH-SCORE and FH-Risk-Score are points instruments with no baseline survival and no centring constant (CALON_JULIUS_SPECKIT/scripts/comparators.py lines 95-119 and 167-232), so there is nothing to mis-horizon and nothing to leave uncentred. The mechanism consistent with all four is shared receiving-cohort attenuation of a shared age-dominated predictor set: if a score's coefficients are k times the truth in the receiving cohort its slope is exactly 1/k, and k=1.8 yields 0.556 for every score simultaneously, which is consistent with published age gradients of 0.041/y (SAFEHEART 1.45 over ~35 years) and 0.064/y (FH-RS 2.256 over ~35 years) against an age HR of 1.20 per SD in the receiving cohort.
answered_by: claude
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

## Merged from step-000 Round 1 (r1b) — mechanical orchestrator merge
Source files: `debate/steps/step-000/r1b/{claude,codex,kimi,grok}.md`. IDs renumbered to be unique.

```objection
id: OBJ-004
step: 000
raised_by: claude
claim: The comparator functions at code/15_CALON_FINAL.py:256-280 are structurally different functions from those at CALON_JULIUS_SPECKIT/scripts/comparators.py for all three scores, yet line 257 asserts "Published equations, scored not fitted". Local SAFEHEART is continuous linear (0.045*age + 0.6*male + 0.4*htn + 0.3*smoke + 0.02*bmi + 0.15*ldl + 0.25*lpa_hi, LDL in mmol/L, no prior-ASCVD term); Spec Kit SAFEHEART is categorical with 3 age bands, 3 BMI bands, 3 LDL bands in mg/dL, a 1.42 prior-ASCVD term and baseline survivals 0.9532/0.9025. Local Montreal is a z-scored continuous LP; Spec Kit Montreal is an integer points chart. These cannot both be the published equation. Every WIN, tie and LOSS in outputs/calon_final.json was generated by the local version. The degree of age coarsening in the published forms predicts the OBJ-001 gaps in exact rank order (SAFEHEART 3 bands, gap -0.066; FH-RS chart bands, -0.023; Montreal 7-year bands, -0.003), so the local values may be inflated surrogates rather than Julius understating.
settled_by: For each of Montreal, FH-RS and SAFEHEART, state which on-disk implementation the source PDF supports, citing page and table. Then re-run code/15_CALON_FINAL.py substituting CALON_JULIUS_SPECKIT/scripts/comparators.py and report the revised combined_tally against the current 10/58/1.
status: WITHDRAWN
withdrawn_because: Duplicate of OBJ-024 (grok), which states the same two-stack provenance defect across all three comparators, additionally names the SAFEHEART-RE labelling in STATUS.md, and carries the stronger settlement condition (a three-column PDF-versus-local-versus-SpecKit coefficient table plus a test that must fail on the current local function). OBJ-024 is the surviving id for this cluster.
```

```objection
id: OBJ-005
step: 000
raised_by: claude
claim: The collinearity guard at code/15_CALON_FINAL.py:300 is gated on f.startswith("sp"), so it cannot fire on cum_nonhdl, which as a cumulative age-by-lipid exposure is the term most likely to be collinear with age - structurally the same construct as the cholesterol-years term in OBJ-003. The threshold of 0.999 catches only exact linear duplicates, as the inline comment concedes. STATUS.md presents this as one of two pre-specified rules governing which terms enter, which reads as collinearity control; it is spline-basis housekeeping that removes knots outside a cohort's age range. Age enters the UK Biobank model through age, sp50 and cum_nonhdl with no pairwise correlation ever reported.
settled_by: Report Pearson r(age, cum_nonhdl) in both cohorts. Refit CALON-F with cum_nonhdl replaced by non-HDL-C alone and report the age coefficient, its 95% CI, and the ALL C-index in each cohort against the current 0.6997 and 0.7486.
status: ACCEPTED-RISK
dissenter: claude
risk_text: The code half is now confirmed by reading, not inference - the guard is literally f.startswith("sp") and abs(corrcoef) >= 0.999, and cum_nonhdl appears in qc.terms_used for both cohorts in outputs/calon_final.json, so it can never reach the guard. What remains unproven until Julius prints r(age, cum_nonhdl) and the refit is the magnitude - whether the age coefficient in CALON-F is being absorbed by cum_nonhdl, and whether the 0.6997 and 0.7486 C-indices survive replacing it with non-HDL-C alone. Until that runs, STATUS.md must not describe the two term-entry rules as collinearity control.
```

```objection
id: OBJ-006
step: 000
raised_by: claude
claim: The Welsh C-index of 0.7486 is internal cross-validation of a Wales-refitted model, not external validation. code/15_CALON_FINAL.py:434 calls cv(s, cohort_spec) with cohort_spec resolved per cohort by usable(), and STATUS.md confirms the specs differ (spline rule fires in UK Biobank only, minimum-information rule in Wales only), giving 8 different terms in each cohort - corroborated by STATUS.md's own Welsh EPV of 11.5 = 92/8. No transported model exists anywhere in this pipeline, so CALON-F has no demonstrated transportability. This also means the step-002 Table B row "Model C, Wales 0.7486 vs 0.698/0.700/0.713" may not be a discrepancy at all: if Julius transported UK Biobank coefficients (step-002 section D.4 describes UK-Biobank-fitted imputation applied to Welsh predictors) whilst the local pipeline refits, the two figures estimate different quantities and the gap is the expected transport penalty.
settled_by: Freeze the UK Biobank coefficient vector, apply it unchanged to the Welsh cohort with no refitting, and report Welsh C-index, calibration slope and calibration-in-the-large. Report the two cohort specifications side by side, naming every term in each.
status: ACCEPTED-RISK
dissenter: claude
risk_text: Now confirmed from the delivered file, not inferred - outputs/calon_final.json qc.terms_used is age/sp50/male/htn_any/dm/smoke/cum_nonhdl/log_tghdl for UKB and age/sp18/sp30/sp50/male/htn_any/cum_nonhdl/log_tghdl for Wales, two different 8-term specs, each cross-validated within its own cohort by cv(s, cohort_spec, resolve=False). What remains unproven until Julius runs a frozen-coefficient transport is the size of the transport penalty - CALON-F's actual external C-index, calibration slope and calibration-in-the-large in Wales are all unmeasured. Until that number exists, no document may describe Wales as external validation, and the 0.7486 headline must be labelled internal cross-validation of a Wales-fitted model. This is the objection I regard as the most consequential open item in the register.
```

```objection
id: OBJ-007
step: 000
raised_by: claude
claim: STATUS.md reports the UK Biobank analysis as n=3,333, which equals 3,540 carriers minus 207 prevalent ASCVD and does not subtract the 124 undated atherosclerotic cases. Step-002 section A lists "Risk set after both exclusions 3,209" under numbers that AGREE across both analyses. 3,540-207=3,333 and 3,333-124=3,209, so a figure recorded as agreed is contradicted by the local pipeline's own status document. This is material, not clerical: 124 participants with atherosclerotic disease of unknown date retained as non-cases attenuate every coefficient, and are an untested alternative explanation for the null age HR in OBJ-003 that the OBJ-003 refit will not distinguish from collinearity.
settled_by: Print the analysis n actually used by code/15_CALON_FINAL.py after all exclusions and state the disposition of the 124 undated cases. If retained, refit with them excluded and report the age HR with 95% CI and the ALL C-index against the current 0.6997.
status: WITHDRAWN
withdrawn_because: Duplicate of OBJ-021 (kimi), which states the identical 3,333-versus-3,209 arithmetic and carries the sharper settlement condition (instrument build_ukb() to print each exclusion count and the disposition of the 124 undated cases). OBJ-021 is the surviving id for this cluster; the local denominator of exactly 3,333 is now independently confirmed and recorded in OBJ-021's risk text.
```

```objection
id: OBJ-008
step: 000
raised_by: claude
claim: outputs/calon_final.json records wales.subgroups."no diabetes".vs.Montreal.delta as exactly 0.0 whilst every neighbouring cell is an irrational-looking float, including near-zero ones (wales male vs SAFEHEART 9.775171065484756e-05; ukb age<median vs SAFEHEART 0.00031926881181920663). A difference of two C-indices over 63 events from two continuous scores cannot land on exact binary zero by chance. The leading candidate is code/15_CALON_FINAL.py:258, where d.hdl.fillna(1.35) replaces missing HDL with a constant: if HDL is wholly missing in that Welsh subgroup, hdl.std() is 0, the Montreal z-term becomes 0/0 = NaN across the vector, and the comparator is degenerate. Separately, line 447 computes comparator_c on the full subgroup (tt, yy) whilst line 440 computes the delta on the ok mask, so the two stored quantities use different risk sets - and step-002 Table B quotes the stored local comparator C-indices as the reference for OBJ-001.
settled_by: For the Welsh no-diabetes subgroup, print HDL non-missing count, hdl.std() after fillna, and the model and Montreal C-indices to six decimal places. Separately print ok.sum() against len(s) and fold_failures for every subgroup in both cohorts, and recompute comparator_c restricted to ok.
status: WITHDRAWN
withdrawn_because: My stated mechanism is refuted by the delivered file. The Welsh no-diabetes Montreal comparator_c is 0.7244553065363216 on n=633, events=63, fold_failures=0, which a NaN or zero-variance HDL z-term could not produce; Welsh HDL completeness is 1028 of 1159, not zero. The second clause, that two stored quantities are computed on different bases, is confirmed but is not the ok mask - it is two different model-C estimators, present in 69 of 69 cells, now filed with full arithmetic as OBJ-028. Superseded by OBJ-028.
```

```objection
id: OBJ-009
step: 000
raised_by: claude
claim: The 10/58/1 tally rests on a single seed (outputs/calon_final.json top-level key "seed"), in a project where STATUS.md documents this exact failure mode: AUC 0.7605 was found seed-favourable, with ten cross-validation seeds giving 0.7497-0.7596 so that the reported point estimate sat above the entire distribution. A verdict is a threshold crossing (code/15_CALON_FINAL.py:444, v = "WIN" if lo > 0) and several deltas sit within 3e-04 of zero. Additionally, the 13 UK Biobank subgroups are ALL plus six complementary pairs, so every participant appears in 7 of 13 rows and the 39 cells are heavily dependent, with no multiplicity control anywhere in lines 426-454. Separately, a cross-validated calibration slope of 1.214 is above 1 where CV optimism normally puts it below 1, which is the signature of over-shrinkage; no penalty or tuning procedure is disclosed in any supplied resource.
settled_by: Re-run code/15_CALON_FINAL.py over at least ten seeds and report the distribution of combined_tally WIN, tie and LOSS counts, plus the seed-to-seed range of the ALL C-index in each cohort. Report the number of bootstrap replicates used by delta_ci, and the penalty type and tuning procedure used by cv().
status: ACCEPTED-RISK
dissenter: claude
risk_text: Seed stability of the 10/58/1 tally is unproven until the ten-seed re-run is executed, and the multiplicity structure is confirmed by reading main() - 13 subgroups are ALL plus six complementary pairs so every participant sits in 7 of 13 rows, with no multiplicity control in run(). Two parts of my original claim are now settled locally and should not be re-litigated - the bootstrap count is BOOT = 1200 at code/15_CALON_FINAL.py:66 and the penalty is a fixed CoxPHFitter(penalizer=0.05) with no tuning procedure, both visible in source. One part I withdraw - the 1.214 over-shrinkage argument rests on outputs/calon_final_qc.json, which OBJ-029 shows describes the superseded 10-variable model; there is currently no calibration slope for the published model at all.
```

```objection
id: OBJ-010
step: 000
raised_by: claude
claim: Two of the three comparators are scored outside the indication stated by the project's own code. CALON_JULIUS_SPECKIT/scripts/comparators.py documents montreal_fh_score as "ranking/prevalent-CVD use only" and fhrs_chart_points as "for adults aged 18-65", and its module docstring states these functions do not impute, convert Lp(a) mass to molar units, or extrapolate outside native eligibility. code/15_CALON_FINAL.py scores Montreal against incident ASCVD in all 26 Montreal cells; its ab() function at lines 265-266 has an open top band applied to a cohort recruiting to age 69; line 261 performs the molar Lp(a) conversion the Spec Kit refuses; line 279 applies a per-mmol/L LDL coefficient against published mg/dL bands. The Montreal column carries the largest deltas in outputs/calon_final.json (ALL +0.033, age<median +0.059, male +0.041, smoker +0.042) whilst SAFEHEART is near-null throughout (ALL +0.0058), so the wins concentrate where the indication mismatch is worst. Beating a prevalent-CVD ranking score on an incident endpoint is not evidence of superiority.
settled_by: Count UK Biobank analysis participants aged over 65 at baseline and report what fraction of FH-RS cells that represents. State each comparator's published endpoint, horizon and derivation cohort in a provenance table. Re-run the tally excluding cells where a comparator is applied outside its published indication and report the revised combined_tally.
status: ACCEPTED-RISK
dissenter: claude
risk_text: The indication statements are confirmed present on disk in CALON_JULIUS_SPECKIT/scripts/comparators.py (sha e0c6d419fc1b733f, 252 lines) and the delta pattern is confirmed in outputs/calon_final.json, where UKB ALL vs Montreal is +0.033006 WIN against vs SAFEHEART +0.005782 tie. What remains unproven until Julius prints the age distribution is the fraction of FH-RS cells scored outside the published 18-65 window, and the revised tally after indication-mismatched cells are dropped. Until that exists, no document may present the Montreal column as evidence of superiority, because Montreal's published use is prevalent-CVD ranking and the endpoint here is incident ASCVD.
```

```objection
id: OBJ-011
step: 000
raised_by: claude
claim: The UK Biobank arm may not be familial hypercholesterolaemia, and STATUS.md's description of CALON-F as a model in "genotype-confirmed HeFH" may be false for that cohort. Three supplied sources conflict: DATA-INVENTORY.md gives ldlr_carrier = 3,540 of 501,936 (0.705%); CLAUDE.md gives is_fh_genetic = 1,623 of 426,732 (0.380%) of which LDLR 1,321 - a 2.7-fold difference in LDLR count for the same biobank with no documented reconciliation and no variant-curation rule stated anywhere. Two independent internal measurements support the milder reading: untreated LDL-C excess of +0.226 mmol/L against the +3 to +4 that defines the phenotype, and crude incidence computed from outputs/calon_final.json of 0.630 per 100 person-years in UK Biobank (289/45,850.03) against 1.345 in the Welsh registry (92/6,841.37) - a 2.1-fold higher rate in the younger cohort. If UK Biobank carriers are a mild population cohort rather than clinic-ascertained FH, then all three externally weighted comparators are uniformly attenuated there, which is a single non-bug explanation for the 0.52-0.57 slope cluster in OBJ-002; note that the internally fitted model's slope is 1.214, above 1, which a shared arithmetic bug in a common scoring pathway would not spare.
settled_by: Publish the variant-curation rule behind ldlr_carrier - filter criteria, ACMG classes included, and counts by class - and reconcile 3,540 against the 1,321 in CLAUDE.md. Report age-standardised incidence in both cohorts to test whether the 2.1-fold rate gap survives age adjustment, and report each cohort's ascertainment route for events. Recompute all four comparator calibration slopes in the Welsh cohort: if they move from 0.52-0.57 toward 1.0 there, the cause is phenotype, not implementation.
status: ACCEPTED-RISK
dissenter: claude
risk_text: Until the variant-curation rule behind ldlr_carrier is published and 3,540 is reconciled against the 1,321 LDLR carriers in CLAUDE.md, the UK Biobank arm cannot be described as genotype-confirmed heterozygous FH in any document, and the case-mix explanation for the 0.52-0.57 comparator slope cluster remains untested against the implementation-bug explanation in OBJ-002. One supporting limb of my claim is withdrawn - the internal slope of 1.214 comes from outputs/calon_final_qc.json which OBJ-029 shows is the superseded model, so it cannot be used as the contrast that a shared bug would not spare. The person-year arithmetic stands as delivered - 289/45850.03 versus 92/6841.37, a 2.1-fold crude rate gap in the wrong direction for a clinic-ascertained FH cohort.
```

```objection
id: OBJ-012
step: 000
raised_by: claude
claim: The objection register has no status meaning "tested and upheld", and this has already produced a wrong disposition. OBJ-000 claimed the carrier flag may not identify FH; its settled_by named a comparison against the +3 to +4 mmol/L expected for heterozygous FH; the measurement returned +0.226 mmol/L [0.185-0.268] with 2.1% above 6.5 mmol/L and variant_id empty in all 501,936 rows. That result confirms the claim. The block is marked status: ANSWERED, which retires it. The permitted statuses are OPEN, ANSWERED, ACCEPTED-RISK and WITHDRAWN, so an objection proven correct has nowhere to go except ACCEPTED-RISK with a named dissenter. Separately, the schema requires globally unique OBJ-NNN ids whilst round 1 is blind and parallel across four agents, guaranteeing id collisions on merge with no documented allocation rule.
settled_by: Run bin/consensus.mjs against the current register and report whether OBJ-000 in its ANSWERED state permits or blocks closure of any step. Add a status meaning UPHELD, or reclassify OBJ-000 as ACCEPTED-RISK with a named dissenter and risk text, then re-run and report the change in closure decisions. Publish the id-allocation rule for blind parallel rounds and confirm bin/panel.mjs enforces it.
status: ACCEPTED-RISK
dissenter: claude
risk_text: Measured this round rather than argued. First, consensus.mjs was run - OBJ-000 in its ANSWERED state passes the evidence check and does not block step 000, so a confirmed-correct objection is silently retired; the gap is real and is demonstrated concretely by OBJ-028 and OBJ-029, which are confirmed from files on disk yet have no status other than OPEN to occupy. Second, a further harness defect not in the original claim - consensus.mjs counts rounds from directory names under steps/step-NNN, and no debate/steps/step-001/ directory exists because step-001 objections are debated inside step-000 round folders, so --step 001 reports rounds 0 of 4 and MAX_ROUNDS can never bind on step 001; DEADLOCK is unreachable there by construction. Until an UPHELD status exists and the step-001 round counter is wired to real turn files, closure decisions on both steps are made by a limit that cannot fire.
```

```objection
id: OBJ-013
step: 000
raised_by: codex
claim: The step-000 packet omits the contents of multiple mandatory resources, including the governance executables, QC JSON, comparator tests and fidelity materials, and all source PDFs, so parser enforcement, QC validity, and publication provenance cannot be independently audited.
settled_by: Run shasum -a 256 and wc -l for all 19 named non-PDF resources in debate/steps/step-000-QC-BRIEF.md plus every located comparator PDF, save the result as debate/steps/step-000/resource-manifest.tsv, and verify that the archived panel packet contains content matching every listed hash.
status: ANSWERED
evidence: debate/steps/step-000/r3/code/resource-manifest.tsv - 22 rows, 21 PRESENT with sha256 and line counts, 1 NOT-FOUND (Montreal/Paquette PDF, absent from the whole CALON tree). SAFEHEART_2017.pdf sha 2859d29d7b8e93ba and FH_Risk_Score_2021.pdf sha 9330f910f8879432 located at thesis_60000_consensus/sources/. Parser enforcement exercised: node debate/bin/consensus.mjs --step 000 --json returns OPEN with 25 objections and rounds 3, --step 001 returns OPEN with rounds 0. QC JSON audited and found stale, filed as OBJ-029.
answered_by: claude
```

```objection
id: OBJ-014
step: 000
raised_by: codex
claim: code/15_CALON_FINAL.py does not evaluate fixed source-faithful comparators: Montreal uses target-sample standardisation, several missing predictors are imputed as healthy or by subgroup medians, and its SAFEHEART transformation is structurally different from CALON_JULIUS_SPECKIT/scripts/comparators.py. The reported comparator C-indices therefore have unresolved provenance.
settled_by: Add and run PDF-derived test_pdf_golden_vectors and test_score_invariant_to_batch_and_subgroup cases in CALON_JULIUS_SPECKIT/tests/test_comparators.py, require exact agreement with source worked examples and identical scores for identical inputs across batches, then recompute aggregate comparator C-indices and paired deltas on one frozen cohort and horizon.
status: ACCEPTED-RISK
dissenter: claude
risk_text: The target-sample standardisation is confirmed by reading - the Montreal branch of comparators() computes (a - a.mean())/a.std() and (hdl - hdl.mean())/hdl.std() on whichever frame is passed, so the same participant receives a different Montreal score in the ALL cell than in any subgroup cell, and no batch-invariance test exists. What remains unproven until the golden-vector tests are written and run is whether the local scores agree with the published worked examples at all. Two of the three source PDFs are on this machine - SAFEHEART_2017.pdf sha 2859d29d7b8e93ba and FH_Risk_Score_2021.pdf sha 9330f910f8879432 - so test_pdf_golden_vectors is buildable today for those two and is not Julius-blocked; no Montreal/Paquette PDF exists in the CALON tree, so the Montreal golden vectors cannot be written from an on-disk source at all.
```

```objection
id: OBJ-015
step: 000
raised_by: codex
claim: The claim that no subgroup gets its own model is unsupported and appears contradicted by code/15_CALON_FINAL.py calling cv(s, cohort_spec, resolve=False) afresh inside every subgroup; subgroup performance may therefore describe newly fitted stratum-specific models rather than one frozen CALON-F model.
settled_by: Run a fit-count instrumentation test over the ALL and subgroup loop that reports only aggregate fit counts and maximum prediction difference; require zero additional model fits after the ALL predictions are created and maximum absolute difference 0 for every reused subgroup prediction, or relabel all subgroup results as separately trained models.
status: ACCEPTED-RISK
dissenter: claude
risk_text: Upheld by code reading, and the docstring is false as written. run() freezes only the TERM LIST - cohort_spec is resolved once and resolve=False stops usable() re-running - but cv() unconditionally fits CoxPHFitter(penalizer=0.05) inside each of 5 folds x 6 repeats on the subgroup frame s, so every one of the 69 cells is a within-subgroup refit with its own coefficients. The comment in run() reading "subgroups never re-resolve, so no subgroup is fitted with its own model" is true of the spec and false of the coefficients. What remains unproven until the fit-count instrumentation is run is only the exact fit count; the qualitative finding needs no further test. Until relabelled, every subgroup C-index and every head-to-head delta describes a procedure evaluated within that stratum, not one frozen CALON-F model, and no document may present them as subgroup performance of a single model.
```

```objection
id: OBJ-016
step: 000
raised_by: codex
claim: The visible corrected_root implementation establishes path precedence but not runtime content identity, so two machines or two available copies can silently run different corrected-outcome files despite a static hash claim in the docstring.
settled_by: Run a corrected_root unit test with two temporary candidate files of different SHA-256 values and require the resolver to abort, then run the real pre-flight check and publish only the selected file SHA-256, which must exactly match its entry in SHA256SUMS.txt.
status: ACCEPTED-RISK
dissenter: claude
risk_text: Until the two-candidate resolver test is run and the selected corrected-outcome file SHA-256 is published and matched against SHA256SUMS.txt, no result in outputs/ is known to have been produced from a specific outcome file, and a re-run on another machine could silently use a different one without any check firing. This is the same class as OBJ-029, where the QC artefact on disk turned out to describe a different model from the results file beside it, so path-precedence-without-content-identity is not hypothetical in this repository.
```

```objection
id: OBJ-017
step: 000
raised_by: codex
claim: OBJ-002's proposed centred-versus-uncentred and baseline-survival experiment is not diagnostic under standard survival calibration because additive centring and baseline hazard alter the calibration intercept, not the slope; the current settlement condition could return no change even when the comparator scale is wrong.
settled_by: Run an affine-invariance unit test at one fixed observed horizon using the declared calibration-slope function: report slopes after adding a constant to the prognostic index, changing only baseline survival, and multiplying the index by 0.5 and 2.0; additive variants must agree within 0.000001 and multiplicative variants must show the expected reciprocal slope change.
status: ACCEPTED-RISK
dissenter: claude
risk_text: Recorded with an explicit technical disagreement from me, not endorsed. The premise holds for a logistic risk model, but 03_obj002_calibration_factorial.py computes p as 1 minus S0**exp(x), a complementary log-log form, and regresses the event on logit(p); adding a constant to x is a multiplicative change in exp(x), which is an intercept shift in cloglog space but NOT an affine shift of logit(p), so the fitted logit-scale slope will move and the factorial is not vacuous. I may be wrong, which is exactly why the affine-invariance unit test named here should be run FIRST, before the factorial - it is cheap, needs no participant data, and settles which of us is right. Until it runs, OBJ-002's settlement condition cannot be trusted either to confirm or to exonerate.
```

```objection
id: OBJ-018
step: 000
raised_by: codex
claim: Public result documents are not synchronised: STATUS.md reports the same diabetic SAFEHEART loss as both -0.062 and -0.064 while outputs/calon_final.json gives -0.0643716927, and the 3333 versus 3209 UK and 1159 versus 1059 Welsh populations are not labelled as distinct estimands.
settled_by: Run a status-versus-output consistency script that requires every displayed delta to match outputs/calon_final.json at its stated rounding precision and publish an aggregate cohort-disposition table reconciling 3540 to 3333 to 3209 in UK Biobank and 7253 to 1159 or 1059 in Wales by named exclusion and horizon.
status: ACCEPTED-RISK
dissenter: claude
risk_text: Confirmed in part and materially widened. Verified locally - STATUS.md line 23 prints the diabetic SAFEHEART loss as -0.062 while outputs/calon_final.json ukb.subgroups.diabetes.vs.SAFEHEART.delta is -0.0643716927371053, so the displayed figure does not round to the stored one. The desynchronisation is worse than the claim states - outputs/calon_final_qc.json describes a different model from outputs/calon_final.json entirely (OBJ-029), and no stored delta anywhere reconciles as c_index minus comparator_c (OBJ-028). What remains unproven until the consistency script is written and the cohort-disposition table published is the full extent; every published figure in STATUS.md should be treated as unverified against outputs/ until it runs.
```

```objection
id: OBJ-019
step: 000
raised_by: kimi
claim: Two irreconcilable SAFEHEART implementations coexist, both claiming published provenance. code/15_CALON_FINAL.py:278-279 scores a continuous LP (0.045*age + 0.6*male + 0.4*htn + 0.3*smoke + 0.02*bmi + 0.15*ldl + 0.25*lpa_hi, no prior-ASCVD term, LDL units unstated) while CALON_JULIUS_SPECKIT/scripts/comparators.py::safeheart_linear_predictor implements the categorical Pérez de Isla 2017 Table 3 form (age bands 1.07/1.45, prior_ascvd 1.42, LDL mg/dL bands 0.92/1.57, Lp(a)>50 -> 0.42). At most one is the published score, and the local SAFEHEART C of 0.6944 that converts both Julius WINs to TIEs (OBJ-001) comes from the unverified one.
settled_by: Extract the SAFEHEART-RE coefficients from the Pérez de Isla 2017 PDF on disk, score one identical frozen UKB carrier cohort extract with both implementations plus the PDF-verified form, and publish the three C-indices and pairwise LP correlations. The implementation matching the PDF within 0.003 on Montreal-style reproduction grounds is the comparator of record; recompute both OBJ-001 deltas with it.
status: ACCEPTED-RISK
dissenter: claude
risk_text: Until the SAFEHEART coefficients are extracted from the PDF and both implementations are scored on one frozen extract by Julius cell 02, the local SAFEHEART C of 0.6944 has no established provenance and neither OBJ-001 delta can be recomputed. Locating the source is done - SAFEHEART_2017.pdf is at thesis_60000_consensus/sources/SAFEHEART_2017.pdf, sha 2859d29d7b8e93ba, 233230 bytes - so the extraction half is a LOCAL task starting today. Overlaps substantially with OBJ-024 (grok), which states the same defect across all three comparators; kimi should consider withdrawing this id in favour of OBJ-024 at round 4, but I will not withdraw another agent's objection.
```

```objection
id: OBJ-020
step: 000
raised_by: kimi
claim: code/15_CALON_FINAL.py:258-262 silently imputes every missing comparator input (hdl->1.35, htn->0, smoke->0, ldl->cohort median, lpa->0 making 22.5% missing Lp(a) into lpa_hi=0, bmi->median/27.0) and prints no per-input imputation counts. The comparator C-indices in outputs/calon_final.json are therefore not of the published scores but of silently completed variants, with imputation burden differing by cohort (Welsh BMI 45.5% observed vs 99.6% UKB per STATUS.md).
settled_by: Patch comparators() to print per-input missingness counts per cohort, recompute all comparator C-indices complete-case on the identical frozen cohort extract, and publish the delta between complete-case and imputed values alongside outputs/calon_final.json.
status: ACCEPTED-RISK
dissenter: claude
risk_text: Partially quantified this round without Julius, and kimi's figures check out. The completeness fractions in outputs/calon_final_qc.json have exact integer numerators over 3333 and 1159, giving hdl missing 417 of 3333 UKB (12.5%) and 131 of 1159 Wales (11.3%), each replaced by the constant 1.35 inside the Montreal z-score, and bmi missing 12 of 3333 UKB (0.4%) against 632 of 1159 Wales (54.5%), each replaced by the cohort median inside SAFEHEART - so more than half of every Welsh SAFEHEART score carries an imputed BMI. What remains unproven until Julius recomputes complete-case is the effect on the C-indices and hence on the tally; note also that these counts come from outputs/calon_final_qc.json which OBJ-029 shows is the superseded model file, and Lp(a) and untreated LDL missingness are not in that table at all, so kimi's 22.5% Lp(a) figure remains unverified from on-disk sources.
```

```objection
id: OBJ-021
step: 000
raised_by: kimi
claim: The step-002 brief section A asserts both pipelines agree on a 3,209 risk set after excluding 207 prevalent plus 124 undated atherosclerotic cases, but STATUS.md and outputs/calon_final.json report UKB n=3,333 = 3,540 - 207 exactly, implying the 124 undated cases remain in the local risk set. If retained as event-free, 3.7% of the local cohort are misclassified cases attenuating every local C-index, including the comparator values at the centre of OBJ-001.
settled_by: Instrument build_ukb() in code/15_CALON_FINAL.py to print each exclusion count and the disposition (excluded / censored / event-free) of the 124 undated atherosclerotic cases, and reconcile the printed arithmetic to either 3,209 or 3,333.
status: ACCEPTED-RISK
dissenter: claude
risk_text: Independently corroborated this round - the local denominator is exactly 3,333, confirmed twice over from outputs/calon_final.json qc.n and from outputs/calon_final_qc.json where every completeness fraction times 3333 is an exact integer (for example cum_nonhdl 0.8748874887488749 x 3333 = 2916 exactly); the same holds for Wales at 1159. So the 124 undated atherosclerotic cases are retained locally and 3,209 was never the local risk set, which means step-002 section A lists as agreed a number only one side used. What remains unproven until Julius runs 01_cohort_ledger_ukb.py is their disposition - excluded, censored or counted event-free - and hence how much attenuation they impose on every local C-index including the comparator values at the centre of OBJ-001. This is the surviving id for the n-cluster; OBJ-007 has been withdrawn to it.
```

```objection
id: OBJ-022
step: 000
raised_by: kimi
claim: The headline "10 wins, 58 ties, 1 loss" in STATUS.md pools two cohorts, but outputs/calon_final.json shows all 10 wins are UK Biobank (ukb.tally 10/28/1) while the external Welsh cohort is 0/30/0 with 9 non-estimable (wales.tally). Any manuscript or abstract text citing the pooled tally without the per-cohort split overstates external performance: externally the model wins zero cells.
settled_by: grep manuscript/ for the pooled tally; wherever it appears, the per-cohort tallies from outputs/calon_final.json (ukb.tally, wales.tally) must appear alongside it. Verified by re-running the grep after edits.
status: ACCEPTED-RISK
dissenter: claude
risk_text: The arithmetic is confirmed exactly - outputs/calon_final.json gives ukb.tally WIN 10 tie 28 LOSS 1 non_estimable 0 and wales.tally WIN 0 tie 30 LOSS 0 non_estimable 9, so externally the model wins zero cells. I have NOT marked this answered although its settlement condition currently passes, because it passes vacuously - grep of manuscript/ returns zero occurrences of the pooled tally today (those files are CALON-N and CALON-W, different models), while the live pooling sits at STATUS.md lines 23 and 46 with no per-cohort split adjacent, which is outside the stated scope of the grep. What remains unproven is nothing; what remains unfixed is STATUS.md. The settlement condition must be widened to STATUS.md and any abstract before this can honestly close, and a vacuous pass is exactly the defect class this panel exists to catch.
```

```objection
id: OBJ-023
step: 000
raised_by: kimi
claim: outputs/calon_final.json records wales.subgroups."no diabetes".vs.Montreal.delta as exactly 0.0 with 63 events. An exactly-zero floating-point delta between two independently computed C-indices is arithmetically improbable and suggests a degenerate path in delta_ci (code/15_CALON_FINAL.py:440) or the comparator LP being the model's own LP in that cell. No downstream check flags an exact zero; the cell is silently counted as a tie.
settled_by: Recompute concordance_index for the model LP and Montreal LP on the Wales no-diabetes subgroup, print both C values to 6 decimal places, and show the delta_ci inputs. If the zero reproduces from genuinely equal C-indices, withdraw; otherwise fix the degenerate path and recompute the Welsh tally.
status: ANSWERED
evidence: Both named mechanisms are refuted by outputs/calon_final.json itself. Degenerate path - the stored Montreal comparator_c for that cell is 0.7244553065363216 on n=633, events=63, fold_failures=0; a NaN or constant LP could not return 0.724455. Comparator LP equal to the model LP - the three comparators in that same cell return three distinct values, Montreal 0.724455, FH-RS 0.727679, SAFEHEART 0.722427, none equal to the model c_index 0.722878. The remaining valid concern, that nothing cross-checks the stored deltas, is superseded and generalised by OBJ-028 which shows the mismatch in 69 of 69 cells.
answered_by: claude
```

```objection
id: OBJ-024
step: 000
raised_by: grok
claim: The two on-disk comparator stacks cannot both be the published equations, and nothing in the delivered artefacts would fail if the local docstring "Published equations, scored not fitted" were false. code/15_CALON_FINAL.py comparators() scores a z-scored linear Montreal, continuous SAFEHEART 0.045*age+0.6*male+0.4*htn+0.3*smoke+0.02*bmi+0.15*ldl+0.25*I(lpa>=105) with HDL/LDL/Lp(a)/BMI imputed, and FH-RS bands plus I(lpa>=105). CALON_JULIUS_SPECKIT/scripts/comparators.py scores a categorical SAFEHEART attributed to Perez de Isla Circulation 2017 Table 3 (age/BMI/LDL mg/dL bands, prior_ASCVD 1.42, lpa>50 mg/dL, S0 0.9532/0.9025, centre 5.4078), an integer Montreal point score, and refuses imputation. STATUS.md further names the head-to-head target SAFEHEART-RE. Three names, at least two functional forms, zero PDF extracts in this pack. Local UKB ALL vs SAFEHEART delta is +0.0058; Julius WIN arithmetic in the QC brief uses SAFEHEART C 0.628 against local 0.6944. That gap is the expected output of scoring different functions, and calon_final.json does not store coefficients, units or thresholds.
settled_by: Locate the comparator PDFs by path or record that they are absent. Extract every coefficient, cut-point and unit from the PDFs into a three-column table (PDF | 15_CALON_FINAL.comparators | Spec Kit). Add a test that asserts local SAFEHEART terms, Montreal terms and FH-RS terms equal the PDF table; the test must fail on the current local function. Separately print local implied comparator C-indices from calon_final.json (model C minus delta) and confirm they match QC-brief local values 0.6944 / 0.6740 / 0.6671.
status: ACCEPTED-RISK
dissenter: claude
risk_text: Surviving id for the comparator-provenance cluster; OBJ-004 has been withdrawn to it. Two settlement clauses discharged this round. First, the PDFs - SAFEHEART_2017.pdf (sha 2859d29d7b8e93ba) and FH_Risk_Score_2021.pdf (sha 9330f910f8879432) are PRESENT at thesis_60000_consensus/sources/; no Montreal or Paquette PDF exists anywhere in the CALON tree, so the Montreal column of the three-column table cannot be completed from an on-disk source and must be recorded as absent. Second, the implied-C check FAILS - c_index minus delta for UKB ALL returns Montreal 0.666702, FH-RS 0.673610, SAFEHEART 0.693926, not the stored 0.667130 / 0.674039 / 0.694355 nor the QC-brief 0.6944 / 0.6740 / 0.6671, because delta and c_index use two different model-C estimators (OBJ-028); the reconciliation grok proposes cannot close until OBJ-028 is fixed. What remains unproven until Julius scores both stacks is which implementation is the comparator of record and what the tally becomes under it.
```

```objection
id: OBJ-025
step: 000
raised_by: grok
claim: STATUS.md locks UK Biobank n=3,333 / 289 while debate/steps/step-002-QC-BRIEF.md section A treats 3,209 as a number both analyses agree on (3,540 carriers minus 207 prevalent minus 124 undated). 3,333 equals 3,540-207, so STATUS is the cohort before the undated-atherosclerotic exclusion. outputs/calon_final.json as delivered has events and C but no n, so the locked C=0.6997 has no checkable denominator in the pack.
settled_by: Print n from build_ukb() in code/15_CALON_FINAL.py and any n field in outputs/calon_final.json / outputs/calon_final_qc.json. Compute 3540-207 and 3540-207-124. If script n is 3333, report how the 124 undated cases are labelled (excluded / censored / events). If script n is 3209, STATUS.md is stale and must be corrected before it is used as local truth.
status: ACCEPTED-RISK
dissenter: claude
risk_text: One clause of this claim is factually wrong and is corrected here for the record - outputs/calon_final.json DOES carry n: ukb.qc.n = 3333, wales.qc.n = 1159, and every subgroup cell carries its own n (for example wales no diabetes n 633, events 63). The locked C = 0.6997 therefore has a checkable denominator in the delivered pack. The main claim, that 3,333 is the cohort before the undated-atherosclerotic exclusion, is correct and is corroborated by the exact integer completeness denominators in outputs/calon_final_qc.json. It duplicates OBJ-021 (kimi), which is the surviving id for this cluster and carries the sharper instrumentation condition; grok should consider withdrawing this id at round 4. What remains unproven until Julius runs 01_cohort_ledger_ukb.py is the disposition of the 124 undated cases.
```

```objection
id: OBJ-026
step: 000
raised_by: grok
claim: OBJ-000 is marked ANSWERED on Julius figures (median untreated LDL-C excess +0.226 mmol/L, 2.1% of carriers above 6.5, variant_id empty in all 501936 rows) while the QC brief section B lists the local pipeline at +0.15 median and ~1% above 6.5, and says the specification expected +0.55. An answered objection that still has two live values, plus a third specified value neither pipeline met, is a stamp, not a measurement. STATUS.md continues to call the same people genotype-confirmed HeFH.
settled_by: Recompute, on the frozen extract actually used by code/15_CALON_FINAL.py, (i) median untreated LDL-C in flagged carriers minus non-carriers, (ii) percent of carriers with untreated LDL-C >=6.5 mmol/L, (iii) count of non-empty variant identifiers in that extract (report the count only). Repeat on the Julius extract if it is a different file. OBJ-000 may remain ANSWERED only if both pipelines produce the same pair of figures that are already in its evidence field; otherwise it must be re-opened. Separately replace or justify every "HeFH" label in STATUS.md against those two figures.
status: ACCEPTED-RISK
dissenter: claude
risk_text: Until the three quantities are recomputed on the frozen extract that code/15_CALON_FINAL.py actually reads, and compared against the same three on the Julius extract, OBJ-000's ANSWERED state rests on figures from one pipeline while the other reports different ones (+0.226 versus +0.15 median, 2.1% versus ~1% above 6.5), and neither meets the +0.55 the specification expected. Grok is right that this is a stamp rather than a measurement, and the structural gap that permits it is filed as OBJ-012 - the register has no status meaning tested and upheld. Until it is recomputed, the phrase genotype-confirmed HeFH must not appear in STATUS.md or any manuscript describing the UK Biobank arm.
```

```objection
id: OBJ-027
step: 000
raised_by: grok
claim: Wales analysis n is 1,159 / 92 in STATUS.md and calon_final.json versus 1,059 in Julius (QC brief section B) with Julius events not reported. DATA-INVENTORY.md trap 6 documents a date-parse failure that moves the cohort to 948/82, which is neither number. A 100-person gap with no filter ledger means the two pipelines are not yet known to be scoring the same Welsh risk set, so no later Wales C or tally cell from either side can be treated as a replicate of the other.
settled_by: Publish a one-page Wales filter ledger for both pipelines: starting n 7253, then each exclusion (Positive1 vs Mutation1, prevalent ASCVD, undated events, complete follow-up, lipid missingness, date parser) with the n and event count after that line. The two ledgers must be run on the same WALES_FH_CLEANED.csv (inventory SHA-256). If they do not converge to one n and one event count, record the first diverging filter and stop treating Wales C-indices as comparable.
status: ACCEPTED-RISK
dissenter: claude
risk_text: Surviving id for the Wales-n cluster. The local side is now pinned exactly - n = 1159 confirmed twice, from outputs/calon_final.json wales.qc.n and from outputs/calon_final_qc.json where every completeness fraction times 1159 is an exact integer (bmi 0.454702329594478 x 1159 = 527 exactly), with 92 events and 6841.37 person-years. What remains unproven until Julius runs 05_wales_filter_ledger.py is the other side - which filter produces 1,059, whether the dayfirst date-parse path explains it, and hence whether the two pipelines are scoring the same Welsh risk set at all. Until the two ledgers converge, no Wales C-index or tally cell from either side may be described as a replicate of the other, and this compounds OBJ-006 - the Welsh arm is both a refit and of contested membership.
```

## Filed in step-000 Round 3 (settlement)

```objection
id: OBJ-028
step: 000
raised_by: claude
claim: The model C-index inside every head-to-head verdict is a different estimator from the C-index published as the model's discrimination, and the difference favours the model. cv() at code/15_CALON_FINAL.py:312 returns c as float(np.mean(cs)) - the mean of per-repeat C-indices - but returns lp as acc/cnt, the linear predictor AVERAGED across the 6 repeats. run() then passes that averaged lp to delta_ci, so every delta uses C(mean LP) while the stored c_index is mean(C per repeat). Recomputed from outputs/calon_final.json alone, delta does not equal c_index minus comparator_c in 69 of 69 cells (min residual 1.294e-04, median 1.249e-03, max 5.510e-03), the residual is identical across all three comparators within every subgroup (0 of 23 differ by more than 1e-12, confirming it is purely model-side), and it is positive in 21 of 23 subgroups with mean +0.000736. For UKB ALL the gap is +0.000429 in all three cells, so OBJ-024's proposed reconciliation returns 0.6939/0.6736/0.6667 rather than the QC-brief values 0.6944/0.6740/0.6671. No check anywhere in the pipeline or in outputs/calon_final_qc.json reconciles the two stored quantities.
settled_by: Recompute from outputs/calon_final.json alone, for all 69 cells, delta minus (c_index minus comparator_c); confirm 69 of 69 are non-zero and that the residual is constant across the three comparators within each subgroup. Then patch run() in code/15_CALON_FINAL.py to store both estimators explicitly - mean-of-repeat C and C of the averaged LP - and re-emit the JSON so that comparator_c equals model_C minus delta to within 1e-12 in every cell, and report whether any verdict label changes.
status: ANSWERED
evidence: outputs/calon_final.json recomputed by debate/steps/step-000/r4/code/obj028_residual_recompute.py into debate/steps/step-000/r4/code/obj028_residuals.tsv (69 data rows): n_nonzero=69/69; 0 of 23 subgroups differ across the 3 comparators by >1e-12; signed min/median69/max/mean=-5.509507557289e-03/+1.035564691881e-03/+3.789420635382e-03/+7.359333721211e-04; abs min/median23/max=1.294196821452e-04/1.248978841851e-03/5.509507557289e-03 matching the claim; 21/23 subgroup residuals >0, 2/23 <0 (wales female -3.192943222761e-03, wales age>=median -5.509507557289e-03); UKB ALL residual=+4.287204480158e-04 so c_index-delta is Montreal 0.6667016051633307, FH-RS 0.6736101620451336, SAFEHEART 0.6939258361882524, not stored comparator_c 0.6671303256113464/0.6740388824931494/0.6943545566362682 and not QC-brief 0.6671/0.6740/0.6944. Mechanism is code/15_CALON_FINAL.py:349-351 vs :434-447. Patch and JSON re-emit not executed (no participant LPs; participant_level_outputs=false). Verdicts already use C(mean LP); additive shift of stored CIs by -residual flips 0 of 69 labels.
answered_by: grok
```

```objection
id: OBJ-029
step: 000
raised_by: claude
claim: outputs/calon_final_qc.json is the QC artefact of a superseded model, and STATUS.md's only calibration claim comes from it. Its ukb features list is age, sp50, male, cum_nonhdl, log_tghdl, hdl, dm, smoke, htn_any, bmi (10 terms including hdl and bmi) with c_index 0.6995594, whereas outputs/calon_final.json qc.terms_used is age, sp50, male, htn_any, dm, smoke, cum_nonhdl, log_tghdl (8 terms, no hdl, no bmi) with ALL c_index 0.6997075; Wales is 0.7499186 versus 0.7486372. STATUS.md itself names those exact transitions as the effect of removing BMI and HDL-C on 13 August 2026, and the QC file is one hour older on disk. Therefore the calibration slope 1.214 (1.017, 1.411) quoted in STATUS.md as a headline limitation, and relied on by OBJ-009 as evidence of over-shrinkage and by OBJ-011 as evidence that a shared bug would not spare the internal model, belongs to the discarded 10-variable model. The published CALON-F has no reported calibration, which manuscript/TRIPOD_STROBE_PROBAST_CALON_W.md:227 already records as NOT MET. Separately STATUS.md says seven variables while terms_used has 8 and epv 36.125 equals 289/8.
settled_by: Re-run code/15_CALON_FINAL.py end to end and confirm the regenerated outputs/calon_final_qc.json lists the same terms as calon_final.json qc.terms_used with bmi and hdl absent, that its ukb c_index equals 0.6997075 and its wales c_index equals 0.7486372, and report the regenerated calibration slope with its 95 percent interval for both cohorts. Then either restate STATUS.md's calibration slope from the regenerated file or delete the 1.214 (1.017, 1.411) claim, and correct "seven variables" to the actual term count.
status: ACCEPTED-RISK
dissenter: codex
risk_text: The current eight-term aggregate rerun produced UKB C 0.6997074817798635 and slope 1.2435089707779163 (1.0406710550281077, 1.446346886527725), and Wales C 0.748637172800255 and slope 1.3107258959808379 (0.9764654884002137, 1.644986303561462). Nevertheless outputs/calon_final_qc.json and STATUS.md remain unchanged on disk, so the delivered QC is still the superseded ten-term artefact and the published 1.214 claim remains unsynchronised.
```

## Filed from debate/steps/step-001/r1/claude.md

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

