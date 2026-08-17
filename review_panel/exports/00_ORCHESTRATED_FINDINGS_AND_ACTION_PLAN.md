# CALON-C: orchestrated findings and action plan

## Scope and completeness

- **13 original review outputs were available:** nine Google Gemini reports, three Cursor blind-round reports (Kimi, Grok and Claude), and one Cursor cross-model debate from Grok.
- **Cursor debate is incomplete:** Kimi and Claude debate responses and the final Cursor teaching synthesis were not produced. Grok’s debate is therefore a strong adjudication, not a completed three-model consensus.
- **Authoritative manuscript checked:** `outputs/manuscript_2026-08-16/CALON_C_MANUSCRIPT_HIGH_CALIBRE.md`.
- **Manuscript SHA-256:** `528cd91b05212e2f4063581b7065069b64785418220066364c41e63bf8602692`.
- **Evidence window:** 17 August 2016–17 August 2026.
- **Evidence limitation:** the Google run had no grounded-search output. Its “verified” literature labels, exact rejection probabilities and proposed new results are not evidence. Kimi also had no live literature connector. Grok used local extracts; Claude reported DOI/PubMed/Crossref checks. All load-bearing citations still require a final reproducible audit.

## Executive judgement

- **Current verdict: NO-GO for submission.** This is supported by the manuscript’s own submission-readiness statement, not by the Google panel’s unsupported “85–90%” rejection estimate.
- **The paper is salvageable**, but most defensibly as a **prediction-methods, comparator-evaluability and setting-transport study**, not as a clinical-deployment paper, a definitive HeFH risk equation, or a demonstration of universal superiority.
- **The critical path is sequential:** establish the study population → rebuild the Welsh risk set and outputs → resolve UK Biobank competing-risk/absolute-risk reporting → add uncertainty → rewrite the comparative estimand → complete governance and citation/prose repair.

## Findings supported across models and by the manuscript

### 1. Population identity is the first scientific gate

- UK Biobank eligibility uses an operational `ldlr_carrier` flag, while `variant_id` is empty throughout the available master table.
- The manuscript therefore cannot establish that all included participants have pathogenic/likely pathogenic LDLR variants or clinically recognised heterozygous familial hypercholesterolaemia.
- The reported phenotype is attenuated relative to clinic FH: median untreated-equivalent LDL-C is 3.95 mmol/L, and the programme reports only a small LDL-C excess over non-carriers.
- **Implication:** title, abstract, guideline framing and comparator interpretation must refer to a population-identified carrier flag unless variant-level classification can be rebuilt. HeFH guidance must not be transferred silently to this frame.

### 2. Welsh results mix two analytical frames

- The corrected Welsh risk set is **1,169 participants/102 events**.
- Welsh discrimination and calibration artefacts still use the earlier **1,159/92** frame.
- Table 5 juxtaposes Kaplan–Meier and Aalen–Johansen estimates from different frames; this makes the row internally uninterpretable.
- **Implication:** regenerate the corrected Welsh baseline table, follow-up, discrimination, calibration, equation, CIF and all manuscript displays from one pipeline of record before retaining a numerical Welsh finding.

### 3. Welsh inclusion and predictor timing threaten transport validity

- Some clinical predictors were recorded at last contact or after the event rather than demonstrably at baseline.
- A dated-field sensitivity reportedly lowered C by approximately 0.030; this bounds concern but does not prove baseline validity.
- Retaining participants without operational follow-up only when they had a dated event appears outcome-conditioned and requires redesign or explicit sensitivity analysis.
- **Implication:** Wales remains an exploratory routine-data transport stress test, not independent external validation. Use a baseline-defined inclusion/censoring rule and pre-baseline predictors wherever possible.

### 4. UK Biobank competing-risk output is missing

- The UK Biobank Aalen–Johansen/competing-risk analysis did not execute because the processed frame lacked the expected death field.
- This does **not** erase Cox ranking, hazard associations or C-statistics, but it blocks definitive absolute-risk interpretation.
- Publishing `S0(5)`, `S0(10)` and worked absolute-risk examples creates a deployable-looking object without competing-risk calibration.
- **Implication:** link and validate mortality data, estimate cumulative incidence with death as a competing event, and reassess calibration; otherwise remove or quarantine deployable absolute-risk material and retain a ranking-only paper.

### 5. Comparator conclusions are narrower than a general “superiority” claim

- Full follow-up: CALON-C was higher than SAFEHEART-RE and Montreal-FH-SCORE after Holm correction.
- FH-Risk-Score: **tie**, not equivalence or non-inferiority: ΔC +0.015, 95% CI −0.011 to 0.040; Holm p=0.5018.
- Five-year family: **no comparison remained significant after Holm correction**.
- SAFEHEART-RE was tested in a primary-prevention frame with previous ASCVD fixed at zero and treatment-suppressed measured LDL-C.
- Montreal-FH-SCORE was developed for prevalent disease, so it is a cross-estimand ranking benchmark rather than a like-for-like incident-risk contest.
- **Implication:** preserve the two full-follow-up findings, but place intended-use qualifiers in the same sentence; foreground the FH-Risk-Score tie and five-year null; do not claim universal superiority, equivalence or non-inferiority.

### 6. Discrimination is moderate; calibration and utility are not established

- Internal C is approximately 0.71; this is ranking performance, not proof of clinical usefulness.
- Calibration is internal/apparent, not transported or independently external.
- Decision-curve claims were withdrawn; no validated threshold, comparative net benefit or treatment policy exists.
- **Implication:** CALON-C must not be used to de-risk a carrier, defer lipid-lowering treatment, or assign treatment thresholds. A narrowly framed development/ranking paper can be published without DCA only if all clinical-utility claims are removed.

### 7. CALON-C is mainly a conventional clinical prognostic model

- Hypertension, diabetes and smoking added approximately +0.033 C beyond age and sex; the lipid apparatus added approximately +0.008.
- All three lipid-derived adjusted intervals crossed the null.
- This does not challenge LDL causality. Causal importance and within-cohort incremental prediction are different questions, especially under treatment, restricted phenotype and measurement error.
- **Implication:** retain frozen ridge terms if they were genuinely fixed; do not prune solely on p-values. Rewrite the model identity as a parsimonious routine clinical prognostic model with a limited lipid increment.

### 8. `cum_nonhdl` is not measured cholesterol-years

- The variable is `log(untreated-equivalent non-HDL-C × age)` from a single baseline lipid measurement.
- It is a cross-sectional lipid–age product/proxy, not a longitudinal area-under-the-curve measure of cumulative exposure.
- **Implication:** preserve lower-for-longer biology in the Introduction, but rename and qualify this predictor everywhere; do not claim that CALON-C directly measures lifetime cholesterol burden.

### 9. Lipid treatment correction and Lp(a) conversion are assumptions

- Dividing treated LDL/non-HDL-C by 0.70 and triglycerides by 0.80 is a population approximation, not individual pharmacological reconstruction.
- The manuscript’s external reconstruction audit reports correlation 0.32 and mean absolute error 1.20 mmol/L.
- Converting Lp(a) from nmol/L to mg/dL with a fixed divisor can misclassify threshold status because conversion depends on apo(a) isoform/assay characteristics.
- **Implication:** label both as assumptions; run defensible sensitivity analyses if they affect comparator ranking. Do not present triple-therapy under-correction as an observed cohort result unless treatment-specific data demonstrate it.

### 10. Endpoint heterogeneity is substantive

- UK Biobank lacks procedural capture and has unambiguous component-date attribution for only 147/289 events.
- Wales includes angina and revascularisation, while UK Biobank is more coronary-diagnosis weighted.
- **Implication:** keep “first incident ASCVD”, not MACE; harmonise hard-event/component sensitivities where supportable; do not present directional transport differences as simple geographic replication.

### 11. Important methodological strengths should be retained

- Strict complete-input comparator scoring avoids assigning missing required inputs to favourable reference categories.
- CALON-C and each comparator were assessed on the same evaluable participants.
- Paired bootstrap ΔC intervals, Holm multiplicity control and the explicit tie rule are strengths.
- Claude reports that paired comparisons used out-of-fold CALON-C predictions; this would materially strengthen the Methods if independently confirmed from the authoritative code path.
- Comparator worked examples and corrections that moved results in both directions show useful audit discipline.

### 12. Reporting and governance defects are immediate desk-rejection risks

- The manuscript contains **16 explicit placeholders** covering authorship, ethics/legal basis, funding, conflicts, PPI, data controller, availability, Welsh outputs, subgroup outputs and other source gaps.
- A mechanical audit confirms **19/39 references are not cited in the manuscript text**: refs 13, 14, 16, 17 and 22–38.
- Pipeline meta-language (`user-specified`, `reviewer response`, source filenames and model-generation history) remains in journal prose.
- **Implication:** complete all governance fields, cite or delete every orphan reference, verify claim-to-citation fidelity, and move provenance details to supplementary/data-availability material.

## Genuine disagreements and the chair’s adjudication

### Retain or delete non-significant lipid terms?

- **Biostatistical position:** retain a frozen ridge specification; post hoc deletion would introduce selection bias.
- **Clinical/lipid position:** retaining weak terms risks a false mechanistic narrative.
- **Adjudication:** retain the frozen equation for validation fidelity, but remove mechanistic overclaiming. A reduced model can be compared prospectively or as a clearly labelled secondary analysis.

### Complete-case comparators or imputation?

- **Complete-case position:** published scores requiring Lp(a), BMI or other inputs must be scored faithfully on participants with those inputs.
- **Imputation position:** complete-case restriction may select a non-representative subset.
- **Adjudication:** keep strict complete-input scoring as primary and report evaluability as a separate implementation outcome. Do not impute unmeasured Lp(a) merely to make a comparator calculable. A principled missing-data sensitivity may supplement, not replace, the primary analysis.

### Is MICE mandatory?

- Google repeatedly demanded ten-fold MICE; Cursor raised missing-data uncertainty.
- **Adjudication:** MICE is not automatically mandatory and is not yet an analysis result. Pre-specify the missingness model, implement any imputation leakage-safely within resampling, and compare it with fold-wise median imputation. Do not rewrite the manuscript as though MICE has already been performed.

### Should DCA, NRI, subgroup interactions and a new grey-zone analysis be mandatory?

- These analyses are useful only if utility, reclassification, subgroup or biomarker-enhancer claims remain central.
- **Adjudication:** they are secondary to population validity, Welsh pipeline repair and competing-risk analysis. Remove the associated claims rather than adding unstable analyses solely to satisfy an AI reviewer.

### What paper is recoverable?

- Kimi: corrected common-data head-to-head methods paper.
- Grok: comparator-coding and setting-transport paper, with the equation demoted.
- Claude: comparator-evaluability/implementation-failure paper, centred on Welsh non-estimability.
- **Adjudication:** combine these into one coherent contribution: **a parsimonious routine-variable model plus a comparator-faithful, common-data evaluability and setting-transport study in a population-identified LDLR-carrier-flag frame**. Do not market it as a definitive HeFH equation or clinical-deployment tool.

## Panel claims that must not be copied into the manuscript

- The Google panel’s **85–90% rejection probability** is uncalibrated opinion.
- Google replacement text states that **MICE was performed**; the manuscript says fold-wise median imputation was used.
- Google replacement text changes the bootstrap count from **100 to 500** without analytical support.
- Google replacement text invents a UK Biobank **10-year Aalen–Johansen incidence of 5.98% with 184 non-ASCVD deaths**. The manuscript explicitly says the UKB competing-risk analysis did not execute.
- Google proposes specific subgroup interactions and results not present in the source material.
- Assertions that rerunning `code/38_CALON_C_CORRECTED.py` alone will fix every defect are unproven; mortality linkage, risk-set logic and output verification are prerequisites.
- “Immortal-time bias” is not the most precise universal label for all Welsh timing problems. Use temporal leakage/reverse-causality/predictor-misclassification language unless the time-at-risk mechanism is demonstrated.
- No Google literature ledger should be called verified: grounded-search metadata were null.

## Ranked critical path

### Gate 1 — Resolve the population

- Reconstruct or audit LDLR variant classification against sequence/ClinVar/ACMG evidence if the governed data permit.
- Report variant classes, carrier frequency and phenotype.
- If impossible, lock the title and claims to the operational `ldlr_carrier` flag and remove HeFH-equivalence language.

### Gate 2 — Rebuild the Welsh risk set and pipeline

- Use baseline-defined eligibility/censoring independent of future event occurrence.
- Use demonstrably pre-baseline predictors where possible and retain a dated-only sensitivity.
- Regenerate baseline, follow-up, discrimination, calibration, equation, CIF/KM and all tables/figures from one 1,169/102 pipeline—or report a different final count if the corrected eligibility rule changes it.

### Gate 3 — Resolve absolute risk in UK Biobank

- Link and validate mortality data.
- Estimate competing-risk cumulative incidence and recalibrate absolute-risk quantities.
- Until this passes, remove S0/worked examples from the main clinical narrative and retain ranking-only interpretation.

### Gate 4 — Add uncertainty and lock model identity

- Provide 95% confidence intervals for all internal and transport C-statistics and for the directional transport difference.
- Independently verify that head-to-head predictions are out of fold and identify whether Welsh comparisons use a local seven-term refit or the frozen UKB equation.
- Quantify or explicitly acknowledge residual specification-search optimism across earlier CALON generations.

### Gate 5 — Rewrite the comparative story

- Descriptive comparative-ranking question; delete “at least as well as”.
- Same-sentence qualifiers for SAFEHEART-RE and Montreal.
- Foreground FH-Risk-Score tie and five-year Holm-null findings.
- Keep full-follow-up wins only as setting-specific discrimination results.
- Rename the lipid–age term and remove utility/de-risking/external-validation language.

### Gate 6 — Submission completion

- Fill all 16 placeholders.
- Verify every DOI, title, publication date and exact numerical claim from primary sources.
- Cite or delete all 19 orphan references; replace out-of-window evidential anchors where possible.
- Remove audit/pipeline voice and produce a journal-facing manuscript plus a separate reproducibility supplement.

## Submission decision

- **Now:** NO-GO.
- **After Gates 1–6:** CONDITIONAL GO to a specialist lipid, atherosclerosis, cardiovascular-prediction or methods journal, subject to the regenerated results.
- **Not supported by current evidence:** clinical deployment, treatment thresholds, independent external validation, universal superiority, mechanistic cumulative-exposure claims or top-tier priority framing.
