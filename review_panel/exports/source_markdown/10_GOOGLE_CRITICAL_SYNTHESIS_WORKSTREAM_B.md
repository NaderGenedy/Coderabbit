# Critical synthesis of the Google debate (workstream B)

**Files reviewed:** `01_GOOGLE_FINAL_TEACHING_SYNTHESIS.md` and `06`–`09_GOOGLE_DEBATE_*.md`  
**Authoritative cross-check:** `outputs/manuscript_2026-08-16/CALON_C_MANUSCRIPT_HIGH_CALIBRE.md`  
**Verified manuscript SHA-256:** `528cd91b05212e2f4063581b7065069b64785418220066364c41e63bf8602692`  
**Evidence caution:** the Google run returned no grounded Google Search evidence (`citationMetadata` and `groundingMetadata` were null). Panel confidence, literature ledgers, rejection probabilities, demanded analyses and proposed replacement text are therefore not treated as evidence unless supported by the manuscript itself.

## Resolved consensus

- **The draft is not submission-ready.** This is the manuscript's own verdict (lines 496–535), not merely panel opinion.
- **Welsh outputs are unsynchronised.** The corrected risk set is 1,169/102, while Welsh discrimination and calibration tables still show the pre-rescue 1,159/92 frame (lines 162, 176, 379–404, 506–508). Regeneration from one pipeline of record is necessary.
- **UK Biobank competing-risk output is absent.** The analysis did not execute because the processed frame lacked `death`; this blocks definitive interpretation of absolute risks, although it does not invalidate every relative-risk or discrimination result (lines 142–144, 212, 298–300, 510).
- **Welsh predictor timing materially limits transport interpretation.** Hypertension, diabetes and smoking were not consistently demonstrably baseline; the dated-field sensitivity reduced C by about 0.030 (lines 76, 206, 280–284). Wales is a routine-data transport stress test, not independent external validation.
- **The model is driven mainly by conventional clinical factors.** Clinical variables added about +0.033 C and the lipid apparatus about +0.008; all three lipid-derived adjusted intervals crossed the null (lines 166–168, 260–264, 489). This supports describing CALON-C as a parsimonious clinical prognostic model, not a lipid-mechanistic engine.
- **Comparator conclusions must stay horizon- and instrument-specific.** Full-follow-up discrimination was higher than SAFEHEART-RE and Montreal-FH-SCORE, tied FH-Risk-Score, and produced no multiplicity-controlled five-year win (lines 180–190). A tie is not equivalence or non-inferiority.
- **No clinical-utility or de-risking claim is justified.** Decision-curve claims were withdrawn; no threshold is validated; the manuscript already says CALON-C must not defer guideline-directed treatment (lines 24, 32, 200, 288–290, 316–320, 524).
- **Population and endpoint boundaries are real.** UK Biobank has an operational `ldlr_carrier` flag without usable variant identifiers, and UKB lacked procedure capture while Wales included procedures and angina (lines 64, 68–82, 270, 302, 328).

## Preserved dissent

- **Retain versus prune lipid terms:** ridge retention of the fixed nine-term architecture can be methodologically defensible; non-significance does not by itself justify post hoc deletion. The stronger resolution is to retain if genuinely frozen but narrow the biological narrative (lines 104, 166–168, 264).
- **Routine-panel parsimony versus Lp(a)/apoB completeness:** omission can support evaluability, but cannot be interpreted as biological redundancy or a reason not to measure Lp(a)/apoB when clinically indicated (lines 256–258, 292–296).
- **Fixed treatment correction versus pharmacological realism:** the manuscript supports calling `/0.70` and `/0.80` crude population approximations and reports poor reconstruction correlation/MAE; it does not establish the panel's asserted prevalence or magnitude of triple-therapy under-correction in this cohort (lines 98–100).
- **Complete-case comparator scoring versus imputation:** the manuscript intentionally uses strict complete-input subsets to reproduce published instruments and separately reports evaluability (lines 118, 122–124, 188, 214–216). Missing specialised comparator assays should not be silently imputed merely to make a tool calculable.
- **Transport versus cohort refit:** frozen UKB-to-Wales application is a legitimate, limited transport estimate. The reverse seven-term Welsh equation is a different cohort-specific fit, not validation of the identical nine-term model (lines 104, 138, 204–206).
- **DCA as mandatory versus claim-dependent:** valid comparative DCA is necessary before clinical-use/net-benefit claims, but not necessarily before publication of a narrowly framed development/ranking study that explicitly withdraws utility claims (lines 24, 252, 290, 320).

## Circular consensus or shared hallucinations

- **The 85–90% rejection probability is unsupported.** It is repeated across all Google reports but is neither estimated nor evidenced in the manuscript; repetition is circular agreement, not calibration.
- **The proposed replacement abstract invents completed analyses.** It states that MICE was used and that UKB Aalen–Johansen CIF was 5.98% with 184 non-ASCVD deaths. The manuscript says median imputation was used and the UKB competing-risk analysis did not execute (lines 104, 142, 212, 399–400, 510). Those numbers must not enter the paper.
- **The replacement abstract also changes bootstrap resampling from 100 to 500 without support.** The manuscript specifies 100 bootstrap resamples (line 106), while 2,000 applies to paired comparator bootstrap (lines 122, 393).
- **“Run `code/38_CALON_C_CORRECTED.py`” is not proven to solve everything.** The manuscript says that file generated the corrected source but also documents missing death data and unsynchronised artefacts (lines 58, 142, 162, 176). Data linkage/schema repair and output verification are prerequisites; a blind rerun is not a demonstrated remedy.
- **“MICE is mandatory” is overconfident.** The manuscript supports concern that median imputation does not propagate uncertainty (line 519), but it does not establish MICE as the only acceptable solution, nor support imputing highly missing comparator biomarkers. The imputation strategy requires a defensible missing-data analysis, leakage-safe implementation and sensitivity analysis.
- **“All three clinical predictors were post-event in >50% of cases” overstates the source.** The manuscript gives a specific earlier-frame fact for blood pressure (55/92 events) and says the other fields were incompletely dated (lines 282–284); it does not establish the same >50% proportion for hypertension, diabetes and smoking separately.
- **“Primary derivation estimand failure” overstates the consequence of missing competing-risk output.** The gap blocks definitive absolute-risk interpretation; it does not erase the Cox ranking, hazard associations or C-statistics (lines 210–212, 298–300).
- **The literature ledgers are not independently verified evidence from this Google run.** With null grounding metadata, their “verified” labels and guideline summaries should not be accepted on panel assertion alone.
- **Exact replacement prose is unsafe as a package.** It combines legitimate reframing with unperformed analyses and invented results; no block should be pasted without line-by-line reconciliation to regenerated outputs.

## Recommendations supported directly by the manuscript

- Regenerate corrected Welsh Table 1, follow-up, discrimination, calibration and equation artefacts for 1,169/102; then reconcile every manuscript number to the machine-readable source (lines 162, 176, 383–404, 506–508).
- Repair/link UKB mortality data and run a pre-specified competing-risk analysis for absolute risk; alternatively suppress transportable 5-/10-year probability claims and clearly retain ranking-only interpretation until available (lines 212, 298–300, 510, 524).
- Obtain genuinely baseline-dated Welsh predictors or retain a dated-only sensitivity and downgrade the Welsh result to an exploratory transport stress test (lines 206, 280–284).
- Keep the model identity modest: parsimonious routine clinical prognostic model with limited lipid increment; do not call the single-time-point age×non-HDL construction a measured lifetime exposure integral (lines 94, 168, 264).
- Preserve the accurate comparator claims: two full-follow-up wins, one tie, no confirmatory five-year wins, no universal superiority/non-inferiority (lines 180–190, 234–250).
- Preserve strict complete-input comparator scoring and separately report real-world evaluability/missingness (lines 118–124, 188, 214–216).
- Label fixed lipid treatment transformations and Lp(a) unit conversion as assumptions/approximations; retain quantitative audit limitations (lines 98, 118, 328).
- Refrain from external-validation, transported-calibration, clinical-utility, treatment-threshold or de-risking claims (lines 136–138, 196, 288–290, 312–320, 332).
- Harmonise and disclose endpoint limitations, including absent UKB procedure capture and ambiguous component dating; do not imply a uniform MACE endpoint (lines 70, 80–82, 298–302).
- Supply the missing governance, authorship, availability and reporting information listed in the 16 placeholders (lines 496–531).
- If subgroup claims are desired, regenerate CALON-C subgroup outputs and use formal interaction/paired-difference evidence with adequate events; otherwise omit subgroup claims (lines 150, 226–228, 308, 509).
- If a CALON-C grey-zone enhancer claim is desired, freeze the base model/band and rerun with reclassification, calibration and decision-analytic outputs; otherwise retain the predecessor analysis only as clearly ancillary or remove it (lines 148, 218–224, 292–296).

## Recommendations not supported by the manuscript

- Do not quote any numerical desk-rejection probability.
- Do not insert the proposed 5.98% UKB CIF, 184 competing deaths, MICE completion, 500 bootstrap resamples, or any other “completed” result absent from the manuscript.
- Do not replace strict comparator complete-case evaluation with MICE-imputed Lp(a), apoB or BMI merely to increase evaluability.
- Do not present MICE with ten imputations as a universally mandatory repair without a missingness model and sensitivity justification.
- Do not delete all favourable comparator language: the two full-follow-up superiority findings are directly reported and multiplicity-controlled. Delete only universal or five-year superiority claims, which the manuscript already avoids.
- Do not delete every reference to cumulative exposure: lifelong LDL exposure is legitimate background biology. Rename/qualify only the CALON-C `cum_nonhdl` predictor and mechanistic model identity.
- Do not claim that all nine terms must be retained solely because ridge was used, or conversely prune terms solely because their confidence intervals cross one. That choice requires fidelity to the frozen specification and validation, not a panel vote.
- Do not claim severe triple-therapy under-correction as an observed cohort result; present it as plausible pharmacological measurement error unless treatment-specific data demonstrate it.
- Do not treat restriction to 147 unambiguously attributed events as a clean mandatory sensitivity: the manuscript explicitly warns that censoring ambiguous cases at their event date is informatively constructed (line 144).
- Do not make NRI, IDI, formal interactions or DCA obligatory for the present ranking paper if the associated biomarker, subgroup or clinical-utility claims are removed. They become necessary only if those claims remain.
- Do not call Wales an internal development cohort without qualification; the supportable description is frozen UKB-to-Wales setting transport within a programme-exposed, timing-limited registry, not independent validation.

## Proposed editorial verdict

- **Current verdict: NO-GO / reject with invitation to resubmit.** This follows the manuscript's own “not submission-ready” statement and the unresolved numerical, source and governance gaps—not the panel's unsupported 85–90% estimate.
- **Conditional route to resubmission:** credible after (1) Welsh artefact regeneration, (2) mortality/absolute-risk resolution or suppression of absolute-risk claims, (3) defensible Welsh timing treatment and transport-only framing, and (4) governance/source-traceability completion.
- **Journal positioning:** even after repair, frame as an incremental prediction-methods/common-data benchmarking and transport study, not a top-tier clinical-deployment or biological-mechanism breakthrough.

## Minimal critical path

1. **Freeze and verify inputs:** preserve the authoritative manuscript checksum; identify the exact corrected Wales and UKB mortality inputs; version the code and output manifest.
2. **Repair only publication-blocking analyses:** regenerate the complete 1,169/102 Welsh artefact set; execute and verify UKB competing-risk analysis, or remove/suppress absolute-risk claims if mortality data remain unavailable.
3. **Resolve timing scope:** use demonstrably pre-baseline Welsh predictors where possible; report a dated-only bound; keep Wales labelled as exploratory setting transport.
4. **Perform a numerical traceability audit:** reconcile abstract, text, Tables 1–6, figures, equations and JSON/CSV outputs. Reject any panel replacement number not generated by the verified pipeline.
5. **Make claim-level edits:** preserve supported full-follow-up comparisons; remove mechanistic, universal-superiority, external-validation, clinical-utility and de-risking implications; label assumptions and endpoint limitations.
6. **Complete governance/reporting fields:** authorship, ethics, funding, conflicts, PPI, controller, availability, dates and ascertainment end date.
7. **Defer non-critical expansions:** MICE alternatives, grey-zone NRI/DCA and formal subgroup interactions should be undertaken only if their corresponding claims remain in scope; they are not substitutes for the first six steps.
