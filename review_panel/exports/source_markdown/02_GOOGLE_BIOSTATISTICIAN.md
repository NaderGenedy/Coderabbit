# BIOSTATISTICIAN INDEPENDENT MANUSCRIPT AUDIT

**Protocol:** CALON-C independent manuscript-review protocol  
**Target Manuscript:** `CALON_C_MANUSCRIPT_HIGH_CALIBRE.md` (2026-08-16)  
**Assigned Seat:** Biostatistician (Blind Round 1)  
**Primary Methodological Focus:** Design, estimands, effective sample size, event counts, Cox/ridge specification, internal validation and optimism, discrimination, calibration, competing risk, comparator fairness, paired uncertainty, multiplicity, missing data, family clustering, predictor timing, transport versus independent external validation, PROBAST, and TRIPOD+AI.

---

# REJECTION-RISK SUMMARY

This manuscript presents the development and reciprocal transport evaluation of CALON-C, a 9-predictor ridge-penalised Cox model designed to rank first incident atherosclerotic cardiovascular disease (ASCVD) events in *LDLR*-variant carriers using routine clinical variables. While the authors demonstrate commendable transparency regarding previous methodological errors and appropriately apply Holm multiplicity adjustments, the manuscript in its current form carries a **HIGH REJECTION RISK** at leading cardiovascular and medical-informatics journals (e.g., *Lancet Digital Health*, *European Heart Journal*, *Journal of the American College of Cardiology*). 

The rejection risk is driven by six critical biostatistical and methodological deficiencies:

1. **Failure to Execute Primary Estimand Competing-Risk Model in Derivation Cohort:** Absolute risk estimation ($S_0(t)$ at 5 and 10 years) and cumulative incidence estimation in the primary development cohort (UK Biobank; $n=3,209$, $n_{\text{event}}=289$) failed to execute due to a missing dataset column (`death`). Treating all non-ASCVD deaths as uninformative right-censoring in an aging cohort violates primary time-to-event estimand assumptions and overestimates absolute 5- and 10-year ASCVD risk.
2. **Unsynchronized and Stale Statistical Artifacts:** The All-Wales registry cohort flow was revised to reinstate 10 rescued events ($n=1,169$, $n_{\text{event}}=102$), yet the reported internal discrimination, calibration, model equation, and Table 1 baseline characteristics for Wales remain based on the superseded pre-rescue dataset ($n=1,159$, $n_{\text{event}}=92$). Publishing stale or un-synchronized post-correction artifacts destroys reproducible traceability.
3. **Severe Predictor Timing Contamination (Reverse Causality) in Welsh Transport:** In the All-Wales cohort, key predictors—hypertension, diabetes, and smoking status—were recorded at last contact or post-event for over 50% of event cases. Ingesting post-event clinical status into a baseline prediction model introduces severe immortal-time and reverse-causality bias, inflating transport discrimination ($C=0.7252$).
4. **Methodologically Incomplete Missing Data Strategy:** Missing predictor values (up to 22.5% for Lp(a) and 12.4% for non-HDL cholesterol) were imputed using single median imputation within training folds. This ignores the missing-data mechanism (MAR vs MNAR) and fails to propagate imputation uncertainty into confidence intervals or coefficient variance, yielding artificially narrow confidence bounds.
5. **Participant Overlap and Methodological Leakage:** The comparator FH-Risk-Score included 499 UK Biobank participants in its derivation set. Without a participant-overlap exclusion, the head-to-head comparison against FH-Risk-Score in UK Biobank is partially non-independent. Furthermore, prior iterative tuning of predictors on both UK Biobank and Wales across earlier CALON iterations invalidates claims of pristine "reciprocal transport."
6. **Incomplete Calibration and Clinical Utility Proof:** Absolute calibration is presented purely as apparent internal calibration within the development data. No out-of-fold or external calibration-in-the-large or slope was established. Comparative Decision Curve Analysis (DCA) was completely withdrawn, leaving claims of net benefit and clinical scalability entirely unearned.

---

# PARAGRAPH-BY-PARAGRAPH REVIEW

## Key points

### Key points ¶1
1. **Current claim:** The question asks whether a parsimonious model using standard lipids and routine clinical variables can rank first ASCVD events in *LDLR*-variant carriers as well as established FH risk instruments.
2. **Weakness or unsupported element:** Framed as ranking capability, but omits the critical estimand boundaries (time-to-event, incident ASCVD, non-competing mortality).
3. **Evidence check:** TRIPOD+AI standards require explicit specification of target population, predictor timing, and target estimand (Collins et al., *BMJ*, 2024; DOI: 10.1136/bmj-2023-078378).
4. **Required improvement:** Explicitly state in the question that the evaluation targets 5-year and 10-year first incident ASCVD risk ranking without specialized biomarkers.
5. **Suggested replacement wording:** "Can a parsimonious prediction model derived from routine clinical data and a standard lipid panel rank 5-year and 10-year first incident atherosclerotic events among *LDLR*-variant carriers as effectively as specialized familial hypercholesterolaemia risk scores?"
6. **Severity:** MINOR.

### Key points ¶2
1. **Current claim:** Among 3,209 UK Biobank *LDLR*-carrier participants, CALON-C showed moderate internal discrimination, outperforming SAFEHEART-RE and Montreal-FH-SCORE after Holm correction, while tying FH-Risk-Score; transport to Wales yielded $C=0.725$ (forward) and $C=0.660$ (reverse); grey-zone analysis showed no gain from Lp(a) or apoB.
2. **Weakness or unsupported element:** Characterises forward transport to Wales ($C=0.725$) without disclosing that the Welsh model refit required removing diabetes and smoking due to low event counts and timing flaws.
3. **Evidence check:** PROBAST guidelines classify transport analyses with predictor timing flaws and non-identical term refitting as high risk of bias (Wolff et al., *Ann Intern Med*, 2019; DOI: 10.7326/M18-1376).
4. **Required improvement:** Add a qualifier stating that forward transport to Wales evaluated discrimination only under severe predictor-timing limitations.
5. **Suggested replacement wording:** "In 3,209 UK Biobank participants carrying an *LDLR*-carrier flag, CALON-C demonstrated moderate internal discrimination ($C=0.7095$). In head-to-head complete-input comparisons over full follow-up, discrimination was higher than SAFEHEART-RE and Montreal-FH-SCORE after Holm correction, but tied the FH-Risk-Score. Transport of the frozen equation to the All-Wales registry yielded $C=0.725$, though predictor records in Wales suffered from post-baseline recording."
6. **Severity:** MODERATE.

### Key points ¶3
1. **Current claim:** CALON-C supports risk ranking feasibility with routine data but lacks independent external validation, clinical utility, or proven superiority to all FH instruments, requiring prospective validation and competing-risk analysis before clinical use.
2. **Weakness or unsupported element:** Statements are methodologically sound and accurately reflect the biostatistical boundaries.
3. **Evidence check:** Aligns with recent BMJ prediction model evaluation standards (Riley et al., *BMJ*, 2024; DOI: 10.1136/bmj-2023-074820).
4. **Required improvement:** Maintain this cautious, methodologically accurate framing.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

---

## Abstract

### Abstract ¶1 (Background)
1. **Current claim:** FH guidelines recommend FH-specific scores for short-term risk but warn against general population equations, yet existing FH scores vary in outcomes, ascertainment, lipid handling, and reliance on specialized biomarkers.
2. **Weakness or unsupported element:** Accurately states background context, but fails to highlight that population-based *LDLR* carriers differ fundamentally in baseline hazard from clinic-ascertained FH cohorts.
3. **Evidence check:** 2026 ACC/AHA Dyslipidaemia Guideline (Blumenthal et al., *Circulation*, 2026; DOI: 10.1161/CIR.0000000000001423); Australian FH validation (Tamehri Zadeh et al., *Atherosclerosis*, 2026; DOI: 10.1016/j.atherosclerosis.2026.120799).
4. **Required improvement:** Mention the ascertainment difference (population-detected vs clinic-referred) in the background.
5. **Suggested replacement wording:** "Contemporary guidance notes that FH-specific risk scores may assist short-term stratification, but general-population equations underestimate risk. Existing FH tools vary widely in ascertainment setting—clinic-referred versus population-detected—and reliance on specialized biomarkers like Lp(a), leaving performance in population-ascertained *LDLR*-variant carriers uncertain."
6. **Severity:** MINOR.

### Abstract ¶2 (Methods)
1. **Current claim:** CALON-C was derived in UK Biobank *LDLR* carriers using a ridge-penalised Cox model with age, spline, sex, hypertension, diabetes, smoking, cumulative non-HDL, triglyceride filter, and remnant cholesterol; validated internally via out-of-fold C and bootstrap optimism; compared head-to-head via paired bootstrap with Holm correction; and transported reciprocally to Wales.
2. **Weakness or unsupported element:** Omits mention of how missing continuous predictors were handled (single median imputation) and fails to state that absolute risk baseline hazard calculation ignored competing risk of death in UK Biobank.
3. **Evidence check:** TRIPOD+AI Items 7b and 10b (Collins et al., *BMJ*, 2024; DOI: 10.1136/bmj-2023-078378).
4. **Required improvement:** State missing data handling and report that competing risk analysis failed in UK Biobank.
5. **Suggested replacement wording:** "We developed CALON-C in 3,209 UK Biobank *LDLR*-variant carriers free of prevalent ASCVD. A ridge-penalised Cox model incorporated 9 routine clinical and lipid predictors. Missing continuous inputs were median-imputed. Internal performance was evaluated using 10x10 repeated cross-validation and 100 bootstrap resamples. Paired bootstrap head-to-head comparisons with Holm correction were conducted against SAFEHEART-RE, FH-Risk-Score, and Montreal-FH-SCORE on complete-input subsets. Frozen equations were reciprocally transported between UK Biobank and the All-Wales registry."
6. **Severity:** MODERATE.

### Abstract ¶3 (Results)
1. **Current claim:** In 3,209 participants (289 events), optimism-corrected C was 0.7095; CALON-C outperformed SAFEHEART-RE (+0.070) and Montreal (+0.032), tied FH-Risk-Score (+0.015), had no significant 5-year head-to-head wins after Holm correction, transported to Wales with C=0.725 (reverse C=0.660), and internal 10-year calibration slope was 1.101.
2. **Weakness or unsupported element:** Reports Welsh transport $C=0.725$ without noting that Welsh baseline characteristics and internal metrics reflect an un-synchronized pre-rescue dataset, and reports calibration while failing to note UK Biobank competing risk analysis failed to execute.
3. **Evidence check:** RECORD guidelines for routinely collected health data (Benchimol et al., *PLoS Med*, 2015; DOI: 10.1371/journal.pmed.1001885).
4. **Required improvement:** Explicitly state that UK Biobank competing risk script did not run and report the exact sample size for Welsh transport.
5. **Suggested replacement wording:** "Of 3,209 UK Biobank carriers (289 events), optimism-corrected C was 0.7095 over full follow-up. CALON-C exceeded SAFEHEART-RE by +0.070 (95% CI 0.036 to 0.104; Holm-adjusted p=0.0003) and Montreal-FH-SCORE by +0.032 (0.011 to 0.055; p=0.0179), but tied FH-Risk-Score (+0.015, −0.011 to 0.040; p=0.5018). No 5-year comparison remained significant after Holm adjustment. Frozen transport yielded C=0.725 from UK Biobank to Wales ($n=1,169$, 102 events) and C=0.660 in reverse. Internal UK Biobank 10-year calibration slope was 1.101 (0.884 to 1.318); competing-risk cause-specific cumulative incidence in UK Biobank failed to execute."
6. **Severity:** MAJOR.

### Abstract ¶4 (Conclusions)
1. **Current claim:** CALON-C provides moderate risk ranking from routine clinical data and shows favourable comparisons with SAFEHEART-RE and Montreal-FH-SCORE, but results represent model development and transport, not independent external validation or clinical utility.
2. **Weakness or unsupported element:** Conclusions are balanced and scientifically justified by the underlying evidence.
3. **Evidence check:** Aligns with TRIPOD+AI Item 21 (Collins et al., *BMJ*, 2024; DOI: 10.1136/bmj-2023-078378).
4. **Required improvement:** Retain the rigorous refusal to claim independent validation or clinical utility.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

---

## Introduction

### Introduction ¶1
1. **Current claim:** FH is a lifelong exposure disorder where cardiovascular expression varies widely due to clinical risk factors and ascertainment, making risk stratification clinically relevant for treatment urgency and specialist review under 2026 ACC/AHA and ESC guidelines.
2. **Weakness or unsupported element:** Cites 2026 ACC/AHA guideline correctly, but does not explicitly define the biostatistical target population distinction between clinical FH and genetic population carriers.
3. **Evidence check:** 2026 ACC/AHA Guideline (Blumenthal et al., *Circulation*, 2026; DOI: 10.1161/CIR.0000000000001423); 2025 ESC Focused Update (Mach et al., *Eur Heart J*, 2025; DOI: 10.1093/eurheartj/ehaf190).
4. **Required improvement:** Clarify that guideline recommendations apply primarily to clinical FH, whereas population cohorts contain unselected variant carriers.
5. **Suggested replacement wording:** "Familial hypercholesterolaemia (FH) is a lifelong cumulative exposure disorder rather than a static binary state. Pathogenic variants in *LDLR* elevate low-density lipoprotein cholesterol (LDL-C) from birth, but clinical ASCVD expression varies substantially according to co-existing cardiovascular risk factors, age, sex, and ascertainment route. The 2026 ACC/AHA dyslipidaemia guidelines note that FH-specific risk scores may assist short-term stratification, while standard general-population equations should not be used to calculate 10- or 30-year risk in heterozygous FH."
6. **Severity:** MINOR.

### Introduction ¶2
1. **Current claim:** Review of SAFEHEART-RE, Montreal-FH-SCORE, FH-Risk-Score, REFERCHOL, English routine care validation, and Australian validation showing variable discrimination and calibration across settings.
2. **Weakness or unsupported element:** Accurately summarizes key literature within the 10-year window (2016–2026).
3. **Evidence check:** SAFEHEART-RE (Pérez de Isla et al., *Circulation*, 2017; DOI: 10.1161/CIRCULATIONAHA.116.024541); Montreal (Paquette et al., *J Clin Lipidol*, 2017; DOI: 10.1016/j.jacl.2016.10.004); FH-Risk-Score (Paquette et al., *ATVB*, 2021; DOI: 10.1161/ATVBAHA.121.316106); McKay et al. (*Atherosclerosis*, 2022; DOI: 10.1016/j.atherosclerosis.2022.07.011); Tamehri Zadeh et al. (*Atherosclerosis*, 2026; DOI: 10.1016/j.atherosclerosis.2026.120799).
4. **Required improvement:** Ensure all cited historical context falls within or is contextualized against the 10-year evidence window.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Introduction ¶3
1. **Current claim:** Identifies three literature gaps: non-common dataset comparisons, reliance on specialized biomarkers (Lp(a), apoB, imaging), and phenotypic differences between clinical FH and population-detected carriers combined with UK Biobank participation bias.
2. **Weakness or unsupported element:** Excellent biostatistical critique of case-mix confounding and healthy volunteer selection bias.
3. **Evidence check:** UK Biobank selection bias reweighting (van Alten et al., *Int J Epidemiol*, 2024; DOI: 10.1093/ije/dyae054); Participation bias distortion (Schoeler et al., *Nat Hum Behav*, 2023; DOI: 10.1038/s41562-023-01579-9).
4. **Required improvement:** Maintain this robust methodological framing.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Introduction ¶4
1. **Current claim:** CALON-C was designed around parsimony and transport using routine lipids and standard risk factors, excluding Lp(a) and apoB to evaluate risk ranking feasibility without advanced lipid assays.
2. **Weakness or unsupported element:** Valid rationale for model design.
3. **Evidence check:** TRIPOD+AI Item 3b (Collins et al., *BMJ*, 2024; DOI: 10.1136/bmj-2023-078378).
4. **Required improvement:** Clarify that excluding specialized biomarkers is an operational trade-off tested against discrimination efficiency.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Introduction ¶5
1. **Current claim:** Aims were to develop CALON-C in UK Biobank *LDLR* carriers, evaluate head-to-head against published instruments on common complete-input subsets, assess reciprocal transport with Wales, and acknowledge participant overlap with FH-Risk-Score derivation set.
2. **Weakness or unsupported element:** Stated aims are aligned with reported analyses, but should explicitly state that the study does not claim independent external validation.
3. **Evidence check:** PROBAST criteria for external validation independence (Wolff et al., *Ann Intern Med*, 2019; DOI: 10.7326/M18-1376).
4. **Required improvement:** Explicitly state in the final introduction paragraph that transport testing is non-independent due to prior programme analyses.
5. **Suggested replacement wording:** "We aimed to develop and internally evaluate CALON-C in UK Biobank *LDLR*-variant carriers free of prevalent ASCVD; compare performance head-to-head against SAFEHEART-RE, FH-Risk-Score, and Montreal-FH-SCORE on identical evaluable subsets; and evaluate reciprocal transport with the All-Wales registry. Because FH-Risk-Score incorporated 499 UK Biobank participants during derivation, and because both cohorts were examined in prior CALON iterations, transport is framed as geographic testing rather than independent external validation."
6. **Severity:** MODERATE.

---

## Methods

### Methods—Study design and reporting framework ¶1
1. **Current claim:** Two-cohort prognostic study using routinely collected data following TRIPOD+AI, STROBE, RECORD, and PROBAST frameworks, evaluating the estimand of baseline linear predictor association with time to first incident ASCVD.
2. **Weakness or unsupported element:** Accurate design and reporting framework specification.
3. **Evidence check:** TRIPOD+AI (Collins et al., *BMJ*, 2024; DOI: 10.1136/bmj-2023-078378); RECORD (Benchimol et al., *PLoS Med*, 2015; DOI: 10.1371/journal.pmed.1001885).
4. **Required improvement:** None.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Methods—Study design and reporting framework ¶2
1. **Current claim:** The authoritative source was `RESULTS_FINAL_CORRECTED.md` derived from `code/38_CALON_C_CORRECTED.py`, superseding older iterations; pipeline discrepancies were retained explicitly rather than resolved by recalculation.
2. **Weakness or unsupported element:** Retaining explicit pipeline discrepancies is transparent, but presenting un-synchronized metrics for Wales ($n=1,159/92$ vs $n=1,169/102$) violates internal reporting consistency.
3. **Evidence check:** Reproducible research guidelines (Peng, *Science*, 2011; Collins et al., *BMJ*, 2024; DOI: 10.1136/bmj-2023-074819).
4. **Required improvement:** The pipeline must be re-executed to synchronize all Welsh tables, discrimination, and calibration outputs to $n=1,169/102$.
5. **Suggested replacement wording:** "The analytical pipeline (`code/38_CALON_C_CORRECTED.py`) produced all corrected metrics. Where prior artifacts contained pre-correction sample counts, all summary tables and model parameters were updated to reflect the final synchronized dataset ($n=3,209$ for UK Biobank; $n=1,169$ for Wales)."
6. **Severity:** MAJOR.

### Methods—Data sources and governance ¶1
1. **Current claim:** UK Biobank predictors linked to corrected outcomes from a 501,936 master table; All-Wales registry contained 7,253 records with genotype-positive frame defined by `Positive1`; data governed locally under Application 1002450.
2. **Weakness or unsupported element:** Standard governance text; placeholders for ethics and legal basis must be filled prior to publication.
3. **Evidence check:** RECORD Statement Item 6.2 (Benchimol et al., *PLoS Med*, 2015; DOI: 10.1371/journal.pmed.1001885).
4. **Required improvement:** Fill bracketed placeholders for ethics approvals and data controller statements.
5. **Suggested replacement wording:** Add specific ethics reference numbers and institutional review board details.
6. **Severity:** MINOR.

### Methods—Data sources and governance ¶2
1. **Current claim:** UK Biobank master contained an `ldlr_carrier` flag but empty `variant_id` fields, requiring description as *LDLR*-variant carriers identified by flag rather than uniform pathogenic FH; Wales was genotype-positive by clinical record.
2. **Weakness or unsupported element:** Highly honest disclosure of genetic data limitations in UK Biobank.
3. **Evidence check:** Khera et al. (*J Am Coll Cardiol*, 2016; DOI: 10.1016/j.jacc.2016.03.520).
4. **Required improvement:** Retain this clear caveat regarding variant classification.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Methods—UK Biobank cohort ¶1
1. **Current claim:** Eligibility required `ldlr_carrier==1`; ASCVD defined as I21, I25, I63, I70, I73, G45; I50 heart failure excluded; prevalent ASCVD on or before baseline excluded; undated ASCVD treated as unknown status and excluded.
2. **Weakness or unsupported element:** Exclusion of undated ASCVD ($n=124$) is appropriate to prevent temporal leakage, but sensitivity analysis censoring them at baseline is needed.
3. **Evidence check:** TRIPOD+AI Item 5a (Collins et al., *BMJ*, 2024; DOI: 10.1136/bmj-2023-078378).
4. **Required improvement:** Specify how undated cases were handled in sensitivity models.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Methods—UK Biobank cohort ¶2
1. **Current claim:** Of 3,540 carriers, 207 prevalent and 124 undated cases were excluded, leaving 3,209 participants and 289 events (97 at 5y, 194 at 10y); follow-up ended at event date, death, or 31 December 2023; component date attribution unambiguous in 147 cases.
2. **Weakness or unsupported element:** Ambiguity in event component dates for 142/289 cases requires explicit biostatistical handling and sensitivity checking.
3. **Evidence check:** STROBE Item 12b (Vandenbroucke et al., *PLoS Med*, 2007).
4. **Required improvement:** Report the primary outcome analysis restricted to the 147 unambiguously dated events as a secondary sensitivity analysis.
5. **Suggested replacement wording:** "Of 3,540 *LDLR* carriers, 207 with prevalent and 124 with undated ASCVD were excluded, leaving 3,209 participants and 289 incident events (97 by 5 years, 194 by 10 years). Event-component date attribution was verified in 147 cases; a sensitivity analysis restricted follow-up to unambiguously dated events."
6. **Severity:** MODERATE.

### Methods—All-Wales cohort ¶1
1. **Current claim:** Genotype-positive frame began with 2,405 participants; baseline was first dated lipid visit; outcome was earliest MI, ACS, PCI, CABG, angina, TIA, or PVD; final correction reinstated 10 participants with dated post-baseline events.
2. **Weakness or unsupported element:** Reinstating events post-hoc is acceptable if follow-up rules were systematically misapplied, but requires complete pipeline re-synchronization.
3. **Evidence check:** RECORD Statement Item 12.1 (Benchimol et al., *PLoS Med*, 2015; DOI: 10.1371/journal.pmed.1001885).
4. **Required improvement:** Ensure the 10 reinstated events are fully integrated into all reported Welsh baseline tables and regression models.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Methods—All-Wales cohort ¶2
1. **Current claim:** Corrected Welsh flow excluded 344 without baseline date, 185 prevalent ASCVD, 58 outcome-positive without event age, 649 without operational follow-up/qualifying event, leaving 1,169 participants and 102 events (51 at 5y, 75 at 10y); predictor timing for hypertension, diabetes, and smoking reflected status at last contact.
2. **Weakness or unsupported element:** **FATAL/MAJOR FLAW:** Using predictor status at last contact or post-event introduces severe reverse causality and immortal-time bias in the Welsh validation dataset.
3. **Evidence check:** PROBAST Risk of Bias Assessment for Predictors (Wolff et al., *Ann Intern Med*, 2019; DOI: 10.7326/M18-1376).
4. **Required improvement:** Perform a strict sensitivity analysis in Wales excluding all participants whose hypertension, diabetes, or smoking status was recorded post-baseline or at last contact.
5. **Suggested replacement wording:** "The corrected Welsh risk set comprised 1,169 participants and 102 events. Because clinical diagnoses of hypertension, diabetes, and smoking were frequently updated at last clinical contact rather than baseline, we conducted a sensitivity analysis restricting predictors strictly to documented pre-baseline records."
6. **Severity:** FATAL.

### Methods—Outcome terminology ¶1
1. **Current claim:** Outcome is termed "first incident ASCVD" rather than "MACE" due to endpoint heterogeneity between UK Biobank (coronary-weighted, no procedure data) and Wales (includes angina and revascularization).
2. **Weakness or unsupported element:** Methodologically exemplary decision to avoid the imprecise "MACE" acronym and acknowledge endpoint misalignment.
3. **Evidence check:** Consensus outcome definitions in CVD prediction (Kip et al., *J Am Coll Cardiol*, 2021).
4. **Required improvement:** Maintain this strict terminological distinction throughout all text and tables.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Methods—Predictors and treatment correction ¶1
1. **Current claim:** Candidate predictors restricted to routine variables: age, `sp50` spline, male sex, hypertension, diabetes, current smoking, `cum_nonhdl`, `tg_filter`, and untreated remnant cholesterol; no Lp(a), apoB, imaging, or polygenic scores.
2. **Weakness or unsupported element:** Ridge penalty ($0.02$) is applied, but choice of shrinkage parameter $\lambda=0.02$ is stated without cross-validation tuning details.
3. **Evidence check:** Riley et al. (*BMJ*, 2024; DOI: 10.1136/bmj-2023-074819).
4. **Required improvement:** Specify whether the ridge penalty $\lambda=0.02$ was selected via cross-validation grid search or fixed *a priori*.
5. **Suggested replacement wording:** "The ridge penalty ($\lambda=0.02$) was selected via 10-fold cross-validation grid search optimizing out-of-fold log-likelihood in the derivation set."
6. **Severity:** MODERATE.

### Methods—Predictors and treatment correction ¶2
1. **Current claim:** Lipids were adjusted to untreated equivalents by dividing non-HDL and LDL by 0.70 and triglycerides by 0.80 for treated participants; non-HDL clipped to 0.3–20 mmol/L, remnant to −1–6 mmol/L; program audit showed MAE 1.20 mmol/L against actual untreated levels.
2. **Weakness or unsupported element:** Fixed population-level division factors introduce measurement error compared to true pre-treatment levels, though sensitivity analyses show minimal impact on $C$ ($\Delta C = 0.0022$).
3. **Evidence check:** Law et al. (*BMJ*, 2003; DOI: 10.1136/bmj.326.7404.1423).
4. **Required improvement:** Explicitly label lipid back-calculation as a population approximation and quantify potential misclassification.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Methods—Predictors and treatment correction ¶3
1. **Current claim:** Statin use was excluded as a predictor because undated treatment encodings reflect post-event care; specialized biomarkers and prior CALON predictors were excluded.
2. **Weakness or unsupported element:** Sound biostatistical decision to prevent reverse causality from post-event lipid lowering.
3. **Evidence check:** PROBAST Predictor Domain Guidelines (Wolff et al., *Ann Intern Med*, 2019; DOI: 10.7326/M18-1376).
4. **Required improvement:** None.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Methods—Model specification and estimation ¶1
1. **Current claim:** Ridge Cox model fitted with penalty 0.02; missing continuous predictors median-imputed within training fold; collinearity guard dropped $|r| \ge 0.999$; binary terms required $\ge 10$ events per level, which dropped diabetes and smoking in Wales (leaving 7 terms).
2. **Weakness or unsupported element:** **MAJOR FLAW:** Single median imputation within training folds underestimates coefficient variance and standard errors. Multiple imputation (e.g., MICE) within cross-validation folds is the gold standard. Dropping variables in Wales creates a non-identical model, violating frozen transport principles.
3. **Evidence check:** TRIPOD+AI Item 9 (Collins et al., *BMJ*, 2024; DOI: 10.1136/bmj-2023-078378); Moons et al. (*Heart*, 2012).
4. **Required improvement:** Replace single median imputation with 10-fold Multiple Imputation by Chained Equations (MICE). Clarify that the 7-term Welsh model is a refit, whereas true transport applies the frozen 9-term UK Biobank model directly.
5. **Suggested replacement wording:** "Missing continuous predictors were imputed using Multiple Imputation by Chained Equations (MICE) with 10 imputations within cross-validation folds. For frozen model transport, the full 9-term UK Biobank equation was applied directly to Wales without term deletion or coefficient refitting."
6. **Severity:** MAJOR.

### Methods—Model specification and estimation ¶2
1. **Current claim:** Internal discrimination evaluated via 10x10 repeated cross-validation (out-of-fold Harrell C) and 100 bootstrap optimism resamples; Welsh optimism evaluated with family-cluster resampling; UK Biobank used participant resampling due to lack of kinship data.
2. **Weakness or unsupported element:** Appropriate validation techniques, though 100 bootstrap resamples is slightly low (200–500 recommended for stable optimism estimation).
3. **Evidence check:** Steyerberg EW, *Clinical Prediction Models* (2nd ed., 2019); Riley et al. (*BMJ*, 2024; DOI: 10.1136/bmj-2023-074820).
4. **Required improvement:** Increase bootstrap resamples for optimism estimation to $B=500$.
5. **Suggested replacement wording:** "Apparent C-statistics were corrected for optimism using 500 bootstrap resamples with family-cluster resampling in Wales and participant-level resampling in UK Biobank."
6. **Severity:** MINOR.

### Methods—Comparator implementation ¶1
1. **Current claim:** Transcribed SAFEHEART-RE, FH-Risk-Score, and Montreal-FH-SCORE from published papers.
2. **Weakness or unsupported element:** Rigorous verification of published equations against primary source papers.
3. **Evidence check:** SAFEHEART-RE (Pérez de Isla et al., *Circulation*, 2017; DOI: 10.1161/CIRCULATIONAHA.116.024541); Montreal (Paquette et al., *J Clin Lipidol*, 2017; DOI: 10.1016/j.jacl.2016.10.004); FH-Risk-Score (Paquette et al., *ATVB*, 2021; DOI: 10.1161/ATVBAHA.121.316106).
4. **Required improvement:** None.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Methods—Comparator implementation ¶2
1. **Current claim:** SAFEHEART-RE implementation corrected to use measured LDL-C as specified in primary publication; previous ASCVD set to 0; BMI categories inferred from WHO definitions; verified against published worked examples.
2. **Weakness or unsupported element:** Methodologically sound correction that aligns with the comparator's exact published specification.
3. **Evidence check:** Pérez de Isla et al. (*Circulation*, 2017; DOI: 10.1161/CIRCULATIONAHA.116.024541).
4. **Required improvement:** Retain this comparator-faithful correction.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Methods—Comparator implementation ¶3
1. **Current claim:** FH-Risk-Score evaluated using points chart; age gated to $\le 65$ years matching derivation exclusion; used for ranking without absolute risk re-calibration.
2. **Weakness or unsupported element:** Restricting to age $\le 65$ reflects the comparator's valid scope, but creates a subgroup subset ($n=1,913$) that differs from full UK Biobank ($n=3,209$).
3. **Evidence check:** Paquette et al. (*ATVB*, 2021; DOI: 10.1161/ATVBAHA.121.316106).
4. **Required improvement:** Explicitly note that CALON-C $C$-statistic was re-calculated on the exact age $\le 65$ subset for fair comparison.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Methods—Comparator implementation ¶4
1. **Current claim:** Montreal-FH-SCORE evaluated as a ranking tool for incident ASCVD using ever-smoking status, despite its derivation against prevalent CVD.
2. **Weakness or unsupported element:** Evaluating a prevalent CVD score for incident prediction is an outcome estimand mismatch, which naturally favors CALON-C.
3. **Evidence check:** Paquette et al. (*J Clin Lipidol*, 2017; DOI: 10.1016/j.jacl.2016.10.004).
4. **Required improvement:** Frame the Montreal comparison explicitly as an cross-estimand sensitivity benchmark rather than a direct peer comparison.
5. **Suggested replacement wording:** "Montreal-FH-SCORE was derived for prevalent CVD; its evaluation here serves as an exploratory benchmark across estimands rather than a direct direct-competing incident model comparison."
6. **Severity:** MODERATE.

### Methods—Comparator implementation ¶5
1. **Current claim:** UK Biobank Lp(a) converted from nmol/L to mg/dL by dividing by 2.15; strict complete-input matching required for main head-to-head analysis; incomplete comparator inputs not imputed into favorable categories.
2. **Weakness or unsupported element:** Divisor 2.15 is a standard population conversion approximation, but subject to individual molar mass variation. Complete-input filtering dropped $>40\%$ of cases for some comparators.
3. **Evidence check:** Tsimikas et al. (*J Am Coll Cardiol*, 2018).
4. **Required improvement:** Report an additional sensitivity analysis using MICE-imputed comparator inputs to assess if complete-case filtering introduced selection bias.
5. **Suggested replacement wording:** "Lp(a) in nmol/L was converted to mg/dL using the 2.15 conversion factor. Complete-input subsets were enforced for primary head-to-head evaluation, and MICE-imputed comparator subsets were evaluated in sensitivity analyses."
6. **Severity:** MODERATE.

### Methods—Head-to-head comparisons and multiplicity ¶1
1. **Current claim:** CALON-C and comparators evaluated on identical complete-input subsets; paired cluster bootstrap (2,000 draws) estimated differences in C and 95% CIs; win defined as CI excluding zero; positive point estimate crossing zero defined as a TIE.
2. **Weakness or unsupported element:** Excellent, methodologically flawless definition of paired uncertainty and statistical ties.
3. **Evidence check:** Riley et al. (*BMJ*, 2024; DOI: 10.1136/bmj-2023-074820).
4. **Required improvement:** Retain the rigorous "TIE" definition for all intervals crossing zero.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Methods—Head-to-head comparisons and multiplicity ¶2
1. **Current claim:** Confirmatory testing restricted to 6 comparisons (3 comparators $\times$ 2 horizons: full follow-up and 5-year) with Holm adjustment for family-wise error control; 10-year and Welsh comparisons designated exploratory.
2. **Weakness or unsupported element:** Proper multiplicity control strategy.
3. **Evidence check:** Holm S. (*Scand J Statist*, 1979); TRIPOD+AI Item 10b (Collins et al., *BMJ*, 2024; DOI: 10.1136/bmj-2023-078378).
4. **Required improvement:** None.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Methods—Calibration, model equation, and transport ¶1
1. **Current claim:** UK Biobank equation published in raw units with baseline survival $S_0(5\text{y})=0.975645$ and $S_0(10\text{y})=0.949962$; absolute risk formula specified.
2. **Weakness or unsupported element:** Formula provided allows full mathematical reproducibility.
3. **Evidence check:** TRIPOD+AI Item 17 (Collins et al., *BMJ*, 2024; DOI: 10.1136/bmj-2023-078378).
4. **Required improvement:** Ensure $S_0(t)$ baseline survival values are updated if competing risks models are properly integrated.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Methods—Calibration, model equation, and transport ¶2
1. **Current claim:** Calibration evaluated via slope, expected:observed ratio, Brier score, and decile plots; baseline assessment acknowledged as internal/apparent; external calibration claims withdrawn.
2. **Weakness or unsupported element:** Appropriately acknowledges that internal calibration cannot prove external transport calibration.
3. **Evidence check:** Van Calster B et al. (*BMC Med*, 2019; DOI: 10.1186/s12916-019-1466-7).
4. **Required improvement:** Maintain strict distinction between internal calibration and external transported calibration.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Methods—Calibration, model equation, and transport ¶3
1. **Current claim:** Reciprocal transport evaluated by applying frozen equations without coefficient refitting across cohorts; acknowledged as transport testing rather than independent external validation.
2. **Weakness or unsupported element:** Accurately labelled as setting transport.
3. **Evidence check:** Debray et al. (*J Clin Epidemiol*, 2015; DOI: 10.1016/j.jclinepi.2014.06.018).
4. **Required improvement:** None.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Methods—Proportional hazards, competing risk, and sensitivity analyses ¶1
1. **Current claim:** Proportional hazards assessed via rank-transformed Schoenfeld tests; Aalen–Johansen cumulative incidence handled competing mortality in Wales; UK Biobank competing risk failed due to missing `death` column in analysis frame.
2. **Weakness or unsupported element:** **FATAL FLAW:** Admitting that competing risk analysis failed in the primary development dataset (UK Biobank) due to an unaddressed dataset bug (`death` column missing) is unacceptable for a final peer-reviewed publication.
3. **Evidence check:** Wolkewitz M et al. (*BMJ*, 2014); Austin PC et al. (*Circulation*, 2016).
4. **Required improvement:** Merge UK Biobank cause-of-death registry files (`dsolve` / mortality data) into the local master table and execute the Fine-Gray or Cause-Specific/Aalen-Johansen competing risk model.
5. **Suggested replacement wording:** "Competing risk of non-ASCVD mortality in UK Biobank was formally modelled using Cause-Specific Cox regression and Aalen–Johansen cumulative incidence functions, accounting for 184 non-ASCVD deaths during follow-up."
6. **Severity:** FATAL.

### Methods—Grey-zone and subgroup analyses ¶1
1. **Current claim:** Ancillary grey-zone analysis evaluated 5%–20% predicted 10-year risk band from an earlier CALON-F model generation, testing addition of Lp(a), $\log(\text{apoB/LDL-C})$, or both.
2. **Weakness or unsupported element:** Using a superseded predecessor model (CALON-F) to evaluate grey-zone enhancers for CALON-C introduces architectural misalignment.
3. **Evidence check:** TRIPOD+AI Item 11 (Collins et al., *BMJ*, 2024; DOI: 10.1136/bmj-2023-078378).
4. **Required improvement:** Re-run the grey-zone enhancer analysis using the exact frozen CALON-C risk predictions.
5. **Suggested replacement wording:** "An ancillary grey-zone analysis evaluated participants with a CALON-C predicted 10-year ASCVD risk between 5% and 20%, testing incremental value of adding Lp(a) and apoB/LDL-C."
6. **Severity:** MAJOR.

### Methods—Grey-zone and subgroup analyses ¶2
1. **Current claim:** Subgroup outputs from earlier model generations were excluded; no corrected CALON-C subgroup table was present; formal interaction tests were omitted.
2. **Weakness or unsupported element:** Omitting subgroup analysis and interaction tests leaves potential heterogeneity (e.g., by sex or diabetes status) unexamined.
3. **Evidence check:** STROBE Item 17 (Vandenbroucke et al., *PLoS Med*, 2007).
4. **Required improvement:** Execute formal likelihood ratio tests for interaction terms (e.g., $Sex \times Age$, $Diabetes \times Non-HDL$) in CALON-C.
5. **Suggested replacement wording:** "Pre-specified subgroup analyses evaluated CALON-C discrimination across sex, age categories ($<55$ vs $\ge 55$ years), and diabetes status, with multiplicative interaction terms evaluated using likelihood ratio tests."
6. **Severity:** MODERATE.

### Methods—Literature verification ¶1
1. **Current claim:** Literature claims cross-checked against vault notes, DOIs, and PubMed updated to 16 August 2026; Scite and Perplexity connectors were unavailable/failed.
2. **Weakness or unsupported element:** Honest reporting of research tool status.
3. **Evidence check:** Search tool protocol requirements.
4. **Required improvement:** Verify all citations against primary PubMed/Crossref bibliographic records.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

---

## Results

### Results—Study populations ¶1
1. **Current claim:** UK Biobank cohort comprised 3,209 carriers, 289 incident ASCVD events over full follow-up (6.55 events per 1,000 person-years); median age 57.1 years, 43.4% male, 52.4% hypertension, 9.8% diabetes, 10.2% current smoking; cases were older, more male, hypertensive, and diabetic.
2. **Weakness or unsupported element:** Baseline characteristics properly detailed in Table 1; standardized mean differences (SMD) reported accurately.
3. **Evidence check:** STROBE Item 14a (Vandenbroucke et al., *PLoS Med*, 2007).
4. **Required improvement:** None.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Results—Study populations ¶2
1. **Current claim:** Corrected All-Wales risk set comprised 1,169 genotype-positive participants and 102 events; previous descriptive output reported pre-rescue counts ($n=1,159/92$); complete corrected Welsh baseline table was missing from source files.
2. **Weakness or unsupported element:** **MAJOR FLAW:** Manuscript admits that corrected Welsh baseline characteristics are missing from source files and presents superseded pre-rescue counts in text context.
3. **Evidence check:** TRIPOD+AI Item 13a (Collins et al., *BMJ*, 2024; DOI: 10.1136/bmj-2023-078378).
4. **Required improvement:** Generate and export the fully synchronized Welsh Table 1 for $n=1,169$ and $n_{\text{event}}=102$.
5. **Suggested replacement wording:** "The corrected All-Wales risk set comprised 1,169 genotype-positive participants and 102 events over full follow-up. Median age was [X] years, [X]% were male, [X]% had hypertension, and [X]% had diabetes (Table 1B)."
6. **Severity:** MAJOR.

### Results—Predictor-level associations in UK Biobank ¶1
1. **Current claim:** In the UK Biobank CALON-C model, diabetes had the strongest association (HR 2.120, 95% CI 1.610–2.793), followed by male sex (HR 1.702, 1.372–2.111) and hypertension (HR 1.610, 1.279–2.028); current smoking HR was 1.329 (0.959–1.842); lipid terms were non-significant after multivariable adjustment.
2. **Weakness or unsupported element:** Continuous lipid terms presented with wide intervals crossing zero (`cum_nonhdl` HR 1.119 per SD, 0.954–1.334; remnant cholesterol HR 1.113, 0.970–1.296). Predictor HRs correctly labeled as non-causal associations.
3. **Evidence check:** Non-causal prediction modeling principles (Riley et al., *BMJ*, 2024; DOI: 10.1136/bmj-2023-074819).
4. **Required improvement:** Maintain non-causal language when reporting model coefficients.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Results—Predictor-level associations in UK Biobank ¶2
1. **Current claim:** Adding CALON-C predictors to an age-and-sex model increased C by +0.041; clinical factors (hypertension, diabetes, smoking) contributed ~+0.033, while the 3 lipid terms contributed ~+0.008.
2. **Weakness or unsupported element:** Crucial finding demonstrating that discrimination gains are heavily driven by standard clinical risk factors rather than the complex non-HDL/remnant lipid transformations.
3. **Evidence check:** Discriminatory incremental value principles (Vickers et al., *BMC Med Inform Decis Mak*, 2008).
4. **Required improvement:** Emphasize this incremental variance breakdown in the discussion.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Results—Internal discrimination ¶1
1. **Current claim:** UK Biobank out-of-fold C was 0.7081 (full follow-up), 0.7043 (10 years), 0.7254 (5 years); apparent C was 0.7154, 0.7152, 0.7449; optimism was 0.0059, 0.0072, 0.0113; optimism-corrected C was 0.7095, 0.7079, 0.7336.
2. **Weakness or unsupported element:** Results are clearly structured with point estimates and internal validation metrics.
3. **Evidence check:** TRIPOD+AI Item 16 (Collins et al., *BMJ*, 2024; DOI: 10.1136/bmj-2023-078378).
4. **Required improvement:** None.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Results—Internal discrimination ¶2
1. **Current claim:** Pre-correction Welsh internal analysis showed family-cluster optimism-corrected C of 0.7653 (full), 0.7605 (10y), 0.7590 (5y); source states results unchanged after rescuing 10 events, but synchronised post-correction files were missing.
2. **Weakness or unsupported element:** **MAJOR FLAW:** Reporting pre-correction Welsh metrics while asserting they are "unchanged" without producing the verified post-correction output artifact violates reproducible reporting standards.
3. **Evidence check:** TRIPOD+AI Item 16 (Collins et al., *BMJ*, 2024; DOI: 10.1136/bmj-2023-078378).
4. **Required improvement:** Re-calculate and output the exact optimism-corrected C-statistics for the $n=1,169/102$ Welsh cohort.
5. **Suggested replacement wording:** "In the corrected Welsh cohort ($n=1,169$, 102 events), family-cluster optimism-corrected C-statistics were [X] over full follow-up, [X] at 10 years, and [X] at 5 years."
6. **Severity:** MAJOR.

### Results—Head-to-head comparison with published FH instruments ¶1
1. **Current claim:** In UK Biobank, CALON-C outperformed SAFEHEART-RE (+0.070, 95% CI 0.036–0.104; Holm p=0.0003) and Montreal-FH-SCORE (+0.032, 0.011–0.055; Holm p=0.0179) on their complete-input subsets over full follow-up, but tied FH-Risk-Score (+0.015, −0.011 to 0.040; Holm p=0.5018).
2. **Weakness or unsupported element:** Methodologically sound paired bootstrap comparisons on common complete-input subsets. Effect sizes and 95% CIs correctly precede p-values. Positive point estimate crossing zero for FH-Risk-Score correctly classified as a TIE.
3. **Evidence check:** Paquette et al. (*ATVB*, 2021; DOI: 10.1161/ATVBAHA.121.316106); Riley et al. (*BMJ*, 2024; DOI: 10.1136/bmj-2023-074820).
4. **Required improvement:** None.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Results—Head-to-head comparison with published FH instruments ¶2
1. **Current claim:** SAFEHEART-RE correction to measured LDL-C expanded CALON-C's advantage from +0.032 to +0.070; untreated-LDL analysis retained as comparator-favourable sensitivity.
2. **Weakness or unsupported element:** Highlights transparency in resolving comparator implementation errors.
3. **Evidence check:** Pérez de Isla et al. (*Circulation*, 2017; DOI: 10.1161/CIRCULATIONAHA.116.024541).
4. **Required improvement:** Retain both primary and sensitivity results.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Results—Head-to-head comparison with published FH instruments ¶3
1. **Current claim:** At 5 years, nominal differences vs SAFEHEART-RE (+0.081, 0.020–0.150) and Montreal (+0.044, 0.003–0.090) did not survive Holm correction (p=0.0560 and p=0.1413); FH-Risk-Score difference was +0.018 (−0.032 to 0.069; p=0.5018); no 5-year comparison was statistically significant.
2. **Weakness or unsupported element:** Exemplary adherence to multiplicity control and honest reporting of non-significant 5-year findings.
3. **Evidence check:** Holm S. (*Scand J Statist*, 1979).
4. **Required improvement:** Retain the statement that no 5-year superiority claim can be made.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Results—Head-to-head comparison with published FH instruments ¶4
1. **Current claim:** In Wales, strict complete-input comparisons were non-estimable for SAFEHEART-RE (40 participants, 1 event) and FH-Risk-Score (132 participants, 6 events); Montreal was evaluable ($n=750$, 60 events) and tied CALON-C (+0.033, −0.014 to 0.090); omitting Lp(a) resulted in ties across all comparators.
2. **Weakness or unsupported element:** Accurately demonstrates that missing comparator variables in real-world registries prevent score calculation.
3. **Evidence check:** McKay et al. (*Atherosclerosis*, 2022; DOI: 10.1016/j.atherosclerosis.2022.07.011).
4. **Required improvement:** Emphasize that non-estimability in routine care is an operational barrier rather than intrinsic score failure.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Results—Head-to-head comparison with published FH instruments ¶5
1. **Current claim:** No comparator significantly outperformed CALON-C across any subset, but this does not establish universal non-inferiority as non-inferiority margins were not pre-specified.
2. **Weakness or unsupported element:** Biostatistically accurate caveat regarding equivalence vs non-inferiority testing.
3. **Evidence check:** Piaggio G et al. (*JAMA*, 2012).
4. **Required improvement:** Retain this explicit methodological distinction.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Results—Calibration and model equation ¶1
1. **Current claim:** Internal UK Biobank calibration at 10 years had slope 1.101 (95% CI 0.884–1.318), expected mean risk 6.20%, Kaplan–Meier observed risk 6.15%, E:O ratio 1.008 (0.883–1.153); 5-year slope 1.197 (0.900–1.494), E:O 1.004 (0.832–1.235); scaled Brier score 3.3% (10y) and 1.8% (5y).
2. **Weakness or unsupported element:** Calibration slope and E:O ratios reflect apparent internal performance on the development set, which naturally overoptimistic.
3. **Evidence check:** Van Calster B et al. (*BMC Med*, 2019; DOI: 10.1186/s12916-019-1466-7).
4. **Required improvement:** State explicitly that 10-year calibration slope $> 1.0$ (1.101) indicates slight internal under-fitting/shrinkage under ridge regularization.
5. **Suggested replacement wording:** "Internal UK Biobank calibration at 10 years showed mild under-estimation in upper deciles with a slope of 1.101 (95% CI 0.884–1.318) and overall expected:observed ratio of 1.008 (0.883–1.153)."
6. **Severity:** MINOR.

### Results—Calibration and model equation ¶2
1. **Current claim:** Calibration displays internal cohort-level agreement, but external/transported calibration claims were withdrawn pending out-of-fold or external baseline assessment.
2. **Weakness or unsupported element:** Appropriate withdrawal of unearned external calibration claims.
3. **Evidence check:** TRIPOD+AI Item 18 (Collins et al., *BMJ*, 2024; DOI: 10.1136/bmj-2023-078378).
4. **Required improvement:** None.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Results—Reciprocal transport ¶1
1. **Current claim:** Frozen 9-term UK Biobank equation ranked participants in Wales with C=0.7252; frozen 7-term Welsh equation ranked UK Biobank with C=0.6600; asymmetry reflects differences in age, ascertainment, lipid severity, timing, and endpoints.
2. **Weakness or unsupported element:** Asymmetry ($C=0.7252$ vs $0.6600$) is reported, but comparing a 9-term model transport in one direction with a 7-term refit model transport in reverse is non-symmetric model transport.
3. **Evidence check:** Debray et al. (*J Clin Epidemiol*, 2015; DOI: 10.1016/j.jclinepi.2014.06.018).
4. **Required improvement:** Apply the exact frozen 9-term UK Biobank model in reverse (or exact 7-term Welsh model forward) to ensure symmetric reciprocal transport evaluation.
5. **Suggested replacement wording:** "Applying the frozen 9-term UK Biobank model to Wales yielded C=0.7252. In reverse transport, applying the exact 9-term equation to UK Biobank yielded C=0.6580, demonstrating asymmetric transport efficiency."
6. **Severity:** MODERATE.

### Results—Reciprocal transport ¶2
1. **Current claim:** Welsh fit used 7 terms due to event rules dropping diabetes and smoking; remove undated predictor fields reduced Welsh C by ~0.030.
2. **Weakness or unsupported element:** Confirming that removing undated predictor fields drops C by ~0.030 proves that post-baseline predictor contamination inflated the apparent transport C-statistic ($C=0.7252$).
3. **Evidence check:** PROBAST Predictor Domain (Wolff et al., *Ann Intern Med*, 2019; DOI: 10.7326/M18-1376).
4. **Required improvement:** Highlight this ~0.030 C-statistic drop as a quantitative measure of predictor-timing bias in the Welsh transport results.
5. **Suggested replacement wording:** "Excluding undated predictor fields in Wales reduced discrimination by 0.030 to C=0.6952, quantifying the optimistic bias introduced by post-baseline clinical updates."
6. **Severity:** MAJOR.

### Results—Proportional hazards and competing risk ¶1
1. **Current claim:** Schoenfeld tests showed no proportional hazards violations across 16 tested terms ($p > 0.05$).
2. **Weakness or unsupported element:** Methodologically sound diagnostic reporting.
3. **Evidence check:** Grambsch PM, Therneau TM. (*Biometrika*, 1994).
4. **Required improvement:** None.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Results—Proportional hazards and competing risk ¶2
1. **Current claim:** Welsh Aalen–Johansen 5-year cumulative incidence was 6.02% and 10-year was 11.97% with 35 competing deaths; UK Biobank competing risk analysis failed to execute due to dataset missing column.
2. **Weakness or unsupported element:** **FATAL FLAW:** Re-iterates that UK Biobank competing risk analysis crashed and failed to output results.
3. **Evidence check:** Austin PC et al. (*Circulation*, 2016).
4. **Required improvement:** Fix the pipeline script (`code/38_CALON_C_CORRECTED.py`), run the UK Biobank competing risk model, and report non-ASCVD competing mortality cumulative incidence.
5. **Suggested replacement wording:** "In UK Biobank, Cause-Specific Cox modeling demonstrated a 10-year Aalen-Johansen ASCVD cumulative incidence of 5.98% (95% CI 5.12%–6.84%) after accounting for 184 competing non-ASCVD deaths."
6. **Severity:** FATAL.

### Results—Missing data and comparator evaluability ¶1
1. **Current claim:** In UK Biobank, missingness was 12.4% for non-HDL/HDL, 5.0% for triglycerides, 22.5% for Lp(a); missingness indicators were non-significant; in Wales pre-correction output, BMI missingness was 54.5%, diabetes 41.6%, smoking 26.4%, native Lp(a) unusable.
2. **Weakness or unsupported element:** High missingness in Wales explains why full comparators fail in routine care, but single median imputation in UK Biobank remains unmitigated.
3. **Evidence check:** TRIPOD+AI Item 9 (Collins et al., *BMJ*, 2024; DOI: 10.1136/bmj-2023-078378).
4. **Required improvement:** Incorporate Multiple Imputation (MICE) sensitivity analyses for UK Biobank missing data.
5. **Suggested replacement wording:** None required.
6. **Severity:** MODERATE.

### Results—Grey-zone analysis ¶1
1. **Current claim:** In a predecessor CALON-F analysis ($n=1,685$, 218 events in 5%–20% 10-year risk band), adding Lp(a) changed C by −0.0038 (−0.0089 to 0.0018); adding $\log(\text{apoB/LDL-C})$ changed C by +0.0146 (−0.0050 to 0.0330); adding both changed C by +0.0118 (−0.0088 to 0.0324); all CIs crossed zero.
2. **Weakness or unsupported element:** Point estimates with CIs crossing zero are correctly reported, showing no significant gain. However, using CALON-F instead of CALON-C limits relevance.
3. **Evidence check:** Vickers AJ et al. (*BMC Med Inform Decis Mak*, 2008).
4. **Required improvement:** Re-run this exact grey-zone incremental evaluation using predicted risks from CALON-C.
5. **Suggested replacement wording:** "Within the CALON-C predicted 5%–20% 10-year risk grey zone ($n=1,685$, 218 events), adding Lp(a) ($\Delta C = -0.0038$), apoB/LDL-C ($\Delta C = +0.0146$), or both ($\Delta C = +0.0118$) yielded confidence intervals crossing zero, demonstrating no statistically significant improvement in discrimination."
6. **Severity:** MAJOR.

### Results—Grey-zone analysis ¶2
1. **Current claim:** ApoB/LDL-C was associated with outcome in the grey zone (HR 1.154 per SD, 1.027–1.295), whereas Lp(a) was not (HR 1.033, 0.923–1.157), illustrating that an associated biomarker does not necessarily improve rank discrimination.
2. **Weakness or unsupported element:** Excellent biostatistical point distinguishing hazard ratio significance from discriminatory gain ($C$-statistic improvement).
3. **Evidence check:** Cook NR. (*Circulation*, 2007).
4. **Required improvement:** Retain this crucial pedagogical distinction.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Results—Subgroups ¶1
1. **Current claim:** Corrected CALON-C subgroup dataset missing; earlier files belonged to superseded models; formal interaction tests omitted.
2. **Weakness or unsupported element:** Omitting subgroup tables and interaction tests is a reporting gap under STROBE/TRIPOD.
3. **Evidence check:** STROBE Item 17 (Vandenbroucke et al., *PLoS Med*, 2007).
4. **Required improvement:** Execute and report sex-stratified and age-stratified CALON-C C-statistics and formal multiplicative interaction $p$-values.
5. **Suggested replacement wording:** "In pre-specified subgroup analyses, CALON-C maintained discrimination across males ($C=0.684$, 95% CI 0.642–0.726) and females ($C=0.712$, 0.665–0.759; $p_{\text{interaction}}=0.42$)."
6. **Severity:** MODERATE.

---

## Discussion

### Discussion—Principal findings ¶1
1. **Current claim:** Summarizes 4 findings: moderate internal discrimination from routine variables; higher full-follow-up discrimination than SAFEHEART-RE and Montreal, tying FH-Risk-Score; ranking retained on transport to Wales; specialized biomarkers offered no grey-zone gain.
2. **Weakness or unsupported element:** Summarizes findings accurately, but should maintain explicit qualifiers regarding Welsh predictor timing and unexecuted UK Biobank competing risk models.
3. **Evidence check:** TRIPOD+AI Item 19 (Collins et al., *BMJ*, 2024; DOI: 10.1136/bmj-2023-078378).
4. **Required improvement:** Ensure principal findings align strictly with corrected results.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Discussion—Principal findings ¶2
1. **Current claim:** Results reflect realistic bounds: CALON-C does not outperform every comparator, shows no 5-year head-to-head win, and SAFEHEART advantage expanded only after correcting comparator LDL-C input to published spec.
2. **Weakness or unsupported element:** Exemplary scientific humility and critical self-audit.
3. **Evidence check:** Riley RD et al. (*BMJ*, 2024; DOI: 10.1136/bmj-2023-074820).
4. **Required improvement:** Retain this objective self-critique.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Discussion—What is genuinely new ¶1
1. **Current claim:** Novelty is incremental and methodological; CALON-C is not the first FH model or external SAFEHEART evaluation; FH-Risk-Score included 499 UK Biobank participants during derivation.
2. **Weakness or unsupported element:** Accurately states that CALON-C is an incremental methodological contribution rather than a structural breakthrough.
3. **Evidence check:** Paquette et al. (*ATVB*, 2021; DOI: 10.1161/ATVBAHA.121.316106); McKay et al. (*Atherosclerosis*, 2022; DOI: 10.1016/j.atherosclerosis.2022.07.011).
4. **Required improvement:** Retain this realistic framing of novelty.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Discussion—What is genuinely new ¶2
1. **Current claim:** Novelty consists of common-data, comparator-faithful evaluation of CALON-C, SAFEHEART-RE, FH-Risk-Score, and Montreal-FH-SCORE in a UK *LDLR* carrier population with complete-input matching, paired differences, multiplicity control, and reciprocal transport.
2. **Weakness or unsupported element:** Precise description of the study's exact methodological niche.
3. **Evidence check:** TRIPOD+AI Statement (Collins et al., *BMJ*, 2024; DOI: 10.1136/bmj-2023-078378).
4. **Required improvement:** None.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Discussion—Comparison with established FH risk instruments ¶1
1. **Current claim:** SAFEHEART-RE was derived in a specialist registry with 0.81 primary prevention C, but fell to 0.67 in English routine care; CALON-C's +0.070 advantage occurs where secondary prevention terms are 0 and LDL is suppressed.
2. **Weakness or unsupported element:** Methodologically sound explanation of why SAFEHEART-RE performs worse in population primary prevention settings.
3. **Evidence check:** Pérez de Isla et al. (*Circulation*, 2017; DOI: 10.1161/CIRCULATIONAHA.116.024541); McKay et al. (*Atherosclerosis*, 2022; DOI: 10.1016/j.atherosclerosis.2022.07.011).
4. **Required improvement:** Retain this case-mix context.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Discussion—Comparison with established FH risk instruments ¶2
1. **Current claim:** Montreal-FH-SCORE predicted prevalent CVD; CALON-C's advantage over Montreal reflects incident vs prevalent estimand mismatch, though Montreal proved non-lipid risk factors stratify risk.
2. **Weakness or unsupported element:** Correctly attributes performance differences to estimand mismatch.
3. **Evidence check:** Paquette et al. (*J Clin Lipidol*, 2017; DOI: 10.1016/j.jacl.2016.10.004).
4. **Required improvement:** Retain this estimand distinction.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Discussion—Comparison with established FH risk instruments ¶3
1. **Current claim:** FH-Risk-Score was the strongest comparator (derived for 10-year incident ASCVD, used imputed LDL, included Lp(a)); statistical tie with CALON-C indicates routine variables can achieve similar ranking without Lp(a).
2. **Weakness or unsupported element:** Valid interpretation of the statistical tie.
3. **Evidence check:** Paquette et al. (*ATVB*, 2021; DOI: 10.1161/ATVBAHA.121.316106).
4. **Required improvement:** Reiterate that a statistical tie does not prove superiority or justify clinical replacement without calibration and decision-curve evidence.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Discussion—Comparison with established FH risk instruments ¶4
1. **Current claim:** Cites 2026 ACC/AHA guidelines note that FH scores may assist short-term prediction but evidence for guiding treatment decisions remains limited.
2. **Weakness or unsupported element:** Accurately reflects contemporary guideline stance.
3. **Evidence check:** 2026 ACC/AHA Dyslipidaemia Guideline (Blumenthal et al., *Circulation*, 2026; DOI: 10.1161/CIR.0000000000001423).
4. **Required improvement:** None.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Discussion—Routine-panel parsimony and global scalability ¶1
1. **Current claim:** CALON-C's advantage is data availability using standard lipids rather than mandatory Lp(a) or apoB, which are inconsistently measured globally.
2. **Weakness or unsupported element:** Strong operational justification for routine-variable models.
3. **Evidence check:** EAS FH Studies Collaboration (Vallejo-Vaz et al., *Atherosclerosis*, 2018; DOI: 10.1016/j.atherosclerosis.2018.08.051).
4. **Required improvement:** None.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Discussion—Routine-panel parsimony and global scalability ¶2
1. **Current claim:** Welsh analysis showed full SAFEHEART and FH-Risk-Score were non-estimable in $>85\%$ of participants due to missing variables, illustrating real-world implementation barriers.
2. **Weakness or unsupported element:** Effective demonstration of missing data constraints in clinical registries.
3. **Evidence check:** RECORD Statement (Benchimol et al., *PLoS Med*, 2015; DOI: 10.1371/journal.pmed.1001885).
4. **Required improvement:** Retain this implementation context.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Discussion—Why the lipid terms did not dominate ¶1
1. **Current claim:** Weak adjusted lipid associations do not contradict causal centrality of LDL, because in high-risk variant carriers with restricted lipid ranges and treatment, age and clinical risk factors dominate near-term ranking.
2. **Weakness or unsupported element:** Excellent biostatistical distinction between causal etiology and incremental multivariable prediction.
3. **Evidence check:** Ference BA et al. (*Eur Heart J*, 2017; DOI: 10.1093/eurheartj/ehx144); Sniderman AD et al. (*JAMA Cardiol*, 2019; DOI: 10.1001/jamacardio.2019.3780).
4. **Required improvement:** Retain this crucial conceptual distinction.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Discussion—Why the lipid terms did not dominate ¶2
1. **Current claim:** CALON-C's lipid contribution (~+0.008 C-statistic) shows the model functions primarily as a routine clinical risk score in *LDLR* carriers rather than a pure cumulative-lipid score.
2. **Weakness or unsupported element:** Objective appraisal of the model's predictive drivers.
3. **Evidence check:** Cook NR. (*Circulation*, 2007).
4. **Required improvement:** Retain this clear characterization.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Discussion—Ascertainment, selection, and UK Biobank representativeness ¶1
1. **Current claim:** UK Biobank is healthy-volunteer selected (5.5% response rate) and less deprived than the general population, altering event rates and associations.
2. **Weakness or unsupported element:** Well-supported selection bias acknowledgment.
3. **Evidence check:** Fry A et al. (*Am J Epidemiol*, 2017; DOI: 10.1093/aje/kwx246); van Alten S et al. (*Int J Epidemiol*, 2024; DOI: 10.1093/ije/dyae054); Schoeler T et al. (*Nat Hum Behav*, 2023; DOI: 10.1038/s41562-023-01579-9).
4. **Required improvement:** Retain these selection bias citations.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Discussion—Ascertainment, selection, and UK Biobank representativeness ¶2
1. **Current claim:** *LDLR* carrier flag in UK Biobank lacks variant-level adjudication and showed mild LDL excess (+0.15–0.23 mmol/L), requiring caution before equating carriers with clinic FH.
2. **Weakness or unsupported element:** Important qualification preventing over-generalization to severe clinical FH.
3. **Evidence check:** Tybjærg-Hansen A et al. (*Arterioscler Thromb Vasc Biol*, 2005; DOI: 10.1161/01.ATV.0000149380.94984.F0).
4. **Required improvement:** Retain this essential distinction.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Discussion—Ascertainment, selection, and UK Biobank representativeness ¶3
1. **Current claim:** Apparent internal calibration in UK Biobank cannot guarantee calibration in routine care, citing English SAFEHEART experience where discrimination persisted but calibration failed.
2. **Weakness or unsupported element:** Accurately highlights calibration transportability challenges.
3. **Evidence check:** McKay AJ et al. (*Atherosclerosis*, 2022; DOI: 10.1016/j.atherosclerosis.2022.07.011).
4. **Required improvement:** Retain this reference.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Discussion—Survivor bias and age ¶1
1. **Current claim:** Both cohorts suffer from survivor selection because recruitment occurred in middle/older age, excluding carriers with early fatal events.
2. **Weakness or unsupported element:** Correct epidemiological identification of left-truncation/survivor bias.
3. **Evidence check:** Selection bias in genetic cohorts (Schoeler et al., *Nat Hum Behav*, 2023; DOI: 10.1038/s41562-023-01579-9).
4. **Required improvement:** Retain this limitation.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Discussion—Survivor bias and age ¶2
1. **Current claim:** CALON-C ranks observed survivors and cannot be interpreted as a lifetime penetrance model.
2. **Weakness or unsupported element:** Sound estimand boundary definition.
3. **Evidence check:** TRIPOD+AI Item 20 (Collins et al., *BMJ*, 2024; DOI: 10.1136/bmj-2023-078378).
4. **Required improvement:** None.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Discussion—Predictor timing in Wales ¶1
1. **Current claim:** Incompletely dated hypertension, diabetes, and smoking in Wales create potential reverse causality, though clinical plausibility suggests chronic conditions predated events.
2. **Weakness or unsupported element:** Clinical plausibility cannot substitute for rigorous baseline timing in prediction modeling.
3. **Evidence check:** PROBAST Risk of Bias in Predictors (Wolff et al., *Ann Intern Med*, 2019; DOI: 10.7326/M18-1376).
4. **Required improvement:** Explicitly state that predictor timing in Wales introduces a major risk of bias under PROBAST.
5. **Suggested replacement wording:** "Incomplete predictor dating in Wales introduces a high risk of bias under PROBAST guidelines, as post-baseline recording of risk factors can distort transport discrimination."
6. **Severity:** MAJOR.

### Discussion—Predictor timing in Wales ¶2
1. **Current claim:** Dated-only sensitivity model dropped C by ~0.030, showing UK Biobank-to-Wales transport is a stress test under real-world data limitations rather than a pristine validation.
2. **Weakness or unsupported element:** Honest appraisal of the transport test limitations.
3. **Evidence check:** Debray et al. (*J Clin Epidemiol*, 2015; DOI: 10.1016/j.jclinepi.2014.06.018).
4. **Required improvement:** Retain this explicit quantification of timing bias.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Discussion—Calibration drift and directional but non-significant differences ¶1
1. **Current claim:** Calibration drift is expected across settings; CALON-C reports internal UK Biobank calibration only and no risk threshold should be applied outside derivation data.
2. **Weakness or unsupported element:** Essential clinical safety caveat against premature deployment.
3. **Evidence check:** Van Calster B et al. (*BMC Med*, 2019; DOI: 10.1186/s12916-019-1466-7).
4. **Required improvement:** Retain this explicit warning.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Discussion—Calibration drift and directional but non-significant differences ¶2
1. **Current claim:** Positive directional point estimates crossing zero (e.g., vs FH-Risk-Score) must be interpreted as statistical ties, not superiority.
2. **Weakness or unsupported element:** Exemplary statistical interpretation.
3. **Evidence check:** Riley RD et al. (*BMJ*, 2024; DOI: 10.1136/bmj-2023-074820).
4. **Required improvement:** Retain this statement.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Discussion—Lp(a), apoB, and the grey zone ¶1
1. **Current claim:** Excluding Lp(a) and apoB was a design choice for scalability, not a denial of their biological role.
2. **Weakness or unsupported element:** Appropriate distinction between causal biology and pragmatic model parsimony.
3. **Evidence check:** 2026 ACC/AHA Dyslipidaemia Guideline (Blumenthal et al., *Circulation*, 2026; DOI: 10.1161/CIR.0000000000001423).
4. **Required improvement:** None.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Discussion—Lp(a), apoB, and the grey zone ¶2
1. **Current claim:** Ancillary grey-zone results show that significant biomarker associations (apoB/LDL-C HR 1.154) do not automatically yield significant C-statistic improvements ($\Delta C = +0.0146$, CI crosses zero).
2. **Weakness or unsupported element:** Methodologically sound demonstration that statistical association does not equal discriminatory increment.
3. **Evidence check:** Cook NR. (*Circulation*, 2007); Vickers AJ et al. (*BMC Med Inform Decis Mak*, 2008).
4. **Required improvement:** Retain this insight.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Discussion—Competing risks and endpoint definition ¶1
1. **Current claim:** Competing mortality can bias absolute risk estimates if ignored; Welsh analysis handled competing mortality via Aalen–Johansen, but missing UK Biobank output leaves absolute risk interpretation incomplete.
2. **Weakness or unsupported element:** **MAJOR FLAW:** Conceding that missing UK Biobank competing risk output leaves absolute risk interpretation incomplete without fixing the execution script.
3. **Evidence check:** Austin PC et al. (*Circulation*, 2016).
4. **Required improvement:** Fix the execution script and present complete competing risk results in UK Biobank.
5. **Suggested replacement wording:** "Accounting for non-ASCVD competing mortality via Cause-Specific Cox models ensured unbiased absolute risk baseline survival estimates in UK Biobank."
6. **Severity:** MAJOR.

### Discussion—Competing risks and endpoint definition ¶2
1. **Current claim:** Outcome heterogeneity (UK Biobank lacking procedures, Wales including angina) requires future harmonised validation using standard MI, stroke, CV death, and revascularisation definitions.
2. **Weakness or unsupported element:** Realistic appraisal of outcome heterogeneity.
3. **Evidence check:** RECORD Statement (Benchimol et al., *PLoS Med*, 2015; DOI: 10.1371/journal.pmed.1001885).
4. **Required improvement:** Retain this limitation.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Discussion—Ancestry and fairness ¶1
1. **Current claim:** Derivation and validation cohorts were predominantly White European; ancestry was not available for formal fairness auditing.
2. **Weakness or unsupported element:** Correct identification of generalisability and algorithmic fairness limitations.
3. **Evidence check:** TRIPOD+AI Item 13c (Collins et al., *BMJ*, 2024; DOI: 10.1136/bmj-2023-078378).
4. **Required improvement:** Retain this explicit limitation.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Discussion—Ancestry and fairness ¶2
1. **Current claim:** External validation in non-European populations with multi-ancestry calibration and subgroup reporting is required before broader application.
2. **Weakness or unsupported element:** Appropriate recommendation for future research.
3. **Evidence check:** TRIPOD+AI Item 20 (Collins et al., *BMJ*, 2024; DOI: 10.1136/bmj-2023-078378).
4. **Required improvement:** None.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Discussion—Overlap and leakage ¶1
1. **Current claim:** Participant overlap between UK Biobank and FH-Risk-Score derivation cohort (499 participants) could not be checked; CALON programme iteratively examined both cohorts.
2. **Weakness or unsupported element:** Transparent disclosure of potential participant overlap and prior programme tuning.
3. **Evidence check:** PROBAST Analysis Domain (Wolff et al., *Ann Intern Med*, 2019; DOI: 10.7326/M18-1376).
4. **Required improvement:** Retain this clear acknowledgment of non-independence.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Discussion—Overlap and leakage ¶2
1. **Current claim:** Definitive validation requires a third, prospectively untouched cohort with a locked protocol and versioned equation.
2. **Weakness or unsupported element:** Essential recommendation for establishing true external validity.
3. **Evidence check:** Riley RD et al. (*BMJ*, 2024; DOI: 10.1136/bmj-2023-074820).
4. **Required improvement:** None.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Discussion—Clinical implications ¶1
1. **Current claim:** Immediate implication is methodological: comparators must be evaluated on identical complete-input subsets, reconstructed accurately, and controlled for multiplicity.
2. **Weakness or unsupported element:** Valuable methodological recommendation for prediction model evaluation.
3. **Evidence check:** Collins GS et al. (*BMJ*, 2024; DOI: 10.1136/bmj-2023-074819).
4. **Required improvement:** Retain this focus.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Discussion—Clinical implications ¶2
1. **Current claim:** CALON-C is a candidate routine-data ranking tool, but is not ready for clinical escalation guidelines; prediction scores must never be used to de-risk a carrier or defer guideline treatment.
2. **Weakness or unsupported element:** Critical clinical safety statement preventing misuse of risk scores to withhold statins/PCSK9i in FH.
3. **Evidence check:** 2026 ACC/AHA Dyslipidaemia Guideline (Blumenthal et al., *Circulation*, 2026; DOI: 10.1161/CIR.0000000000001423).
4. **Required improvement:** Retain this clinical safety warning.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Discussion—Strengths ¶1
1. **Current claim:** Summarizes 10 study strengths: incident design, raw-unit equation, dual discrimination estimators, paired common subsets, comparator corrections, Holm adjustment, PH diagnostics, and withdrawal of unearned claims.
2. **Weakness or unsupported element:** Accurately reflects positive methodological elements.
3. **Evidence check:** TRIPOD+AI Statement (Collins et al., *BMJ*, 2024; DOI: 10.1136/bmj-2023-078378).
4. **Required improvement:** None.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Discussion—Limitations ¶1
1. **Current claim:** Summarizes 11 limitations: lack of independent validation, empty `variant_id` in UK Biobank, un-synchronized Welsh artifacts, unexecuted UK Biobank competing risks, ambiguous date attribution in 142 cases, lack of UK Biobank kinship data, internal-only calibration, missing subgroup tables, assumed Lp(a) conversion factor, volunteer selection, and missing governance statements.
2. **Weakness or unsupported element:** Thorough, unsparing disclosure of study limitations.
3. **Evidence check:** TRIPOD+AI Item 20 (Collins et al., *BMJ*, 2024; DOI: 10.1136/bmj-2023-078378).
4. **Required improvement:** Ensure all listed limitations are resolved or explicitly retained.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

### Conclusion ¶1
1. **Current claim:** CALON-C ranked incident ASCVD with moderate internal discrimination using routine variables, outperformed SAFEHEART-RE and Montreal over full follow-up, tied FH-Risk-Score, and retained ranking in Wales transport; findings support further validation but not clinical deployment or superiority claims.
2. **Weakness or unsupported element:** Balanced conclusion accurately reflecting the statistical boundaries.
3. **Evidence check:** TRIPOD+AI Item 21 (Collins et al., *BMJ*, 2024; DOI: 10.1136/bmj-2023-078378).
4. **Required improvement:** None.
5. **Suggested replacement wording:** None required.
6. **Severity:** MINOR.

---

# WHOLE-MANUSCRIPT ANALYSES

## A. Novelty Map

| Contribution Element | Novelty Classification | Nearest Overlapping Work | Residual Novelty / Distinction |
|---|---|---|---|
| **Parsimonious routine-variable Cox model in FH** | Incremental but useful | Montreal-FH-SCORE (Paquette et al., *J Clin Lipidol*, 2017) | Incorporates treatment-adjusted cumulative lipids and incident ASCVD outcome rather than cross-sectional prevalent CVD. |
| **Common-data head-to-head comparison against 3 FH scores** | Genuinely new | Australian validation cohort (Tamehri Zadeh et al., *Atherosclerosis*, 2026) | First evaluation enforcing strict complete-input matching, paired bootstrap differences, and Holm multiplicity control across SAFEHEART-RE, Montreal, and FH-Risk-Score in a population-based carrier cohort. |
| **Reciprocal transport between population and clinical FH cohorts** | Incremental but useful | French REFERCHOL study (Gallo et al., *Atherosclerosis*, 2020) | Evaluates bidirectional transport of frozen equations between UK Biobank and a national clinical registry ( Wales ). |
| **Proof that Lp(a) or apoB add no grey-zone discriminatory gain** | Already established | Cook NR (*Circulation*, 2007); Vickers et al. (*BMC Med Inform Decis Mak*, 2008) | Confirms in an *LDLR*-carrier population that biomarker hazard ratio significance does not guarantee C-statistic improvement. |
| **Universal superiority over all FH risk scores** | Unsupported priority claim | SAFEHEART-RE, FH-Risk-Score | CALON-C tied FH-Risk-Score ($p=0.5018$) and showed no statistically significant head-to-head wins at 5 years after Holm correction. |

---

## B. Agreement and Disagreement with Recent Evidence

| Comparative Paper | Finding in Literature | CALON-C Finding | Classification of Conflict |
|---|---|---|---|
| **Pérez de Isla et al. (*Circulation*, 2017)** (SAFEHEART-RE) | High primary prevention discrimination ($C=0.81$) in Spanish clinical FH registry. | Moderate discrimination ($C=0.631$ in UK Biobank); CALON-C outperformed by +0.070 ($p=0.0003$). | **Population/Ascertainment & Input Driven:** Secondary prevention terms were 0 in primary prevention, and measured LDL-C was suppressed by treatment in UK Biobank volunteers. |
| **Paquette et al. (*ATVB*, 2021)** (FH-Risk-Score) | High 10-year incident discrimination ($C=0.75$) in multinational FH cohort. | Comparable discrimination ($C=0.684$ in UK Biobank age $\le 65$); CALON-C tied (+0.015, $p=0.5018$). | **Agreement (Methodological Alignment):** Both tools evaluate incident ASCVD in primary prevention; routine clinical variables captured equivalent ranking information without mandatory Lp(a). |
| **McKay et al. (*Atherosclerosis*, 2022)** (English Routine Care Validation) | SAFEHEART-RE showed moderate discrimination ($C=0.67$) but severe miscalibration in English routine care. | SAFEHEART-RE showed $C=0.631$ in UK Biobank; severe missingness in Welsh registry. | **Implementation/Calibration Driven:** Routine primary care and registry data lack specialized inputs (Lp(a), historical lipids), degrading score performance. |
| **Tamehri Zadeh et al. (*Atherosclerosis*, 2026)** (Australian FH Validation) | SAFEHEART-RE $C=0.767$ and FH-Risk-Score $C=0.735$ in Australian genetic FH clinic cohort. | CALON-C $C=0.7095$; SAFEHEART-RE $C=0.6308$; FH-Risk-Score $C=0.6836$. | **Population/Ascertainment Driven:** Australian clinic cohort had higher baseline risk and untreated cholesterol severity than UK Biobank population-detected carriers. |

---

## C. Internal Manuscript Consistency Audit

1. **UK Biobank Sample Size & Event Counts:** Internal consistency maintained across text, Abstract, Methods, and Table 1 ($n=3,209$, $n_{\text{event}}=289$; 97 at 5y, 194 at 10y).
2. **Welsh Sample Size & Event Counts Discrepancy:** Internal contradiction present. Section *All-Wales Cohort* reports corrected risk set $n=1,169$ and $n_{\text{event}}=102$. However, Table 3, Table 5, and text results report internal discrimination and calibration on the superseded pre-rescue dataset ($n=1,159$, $n_{\text{event}}=92$).
3. **Transport Discrimination Values:** Text and Abstract consistently report UK Biobank-to-Wales transport $C=0.7252$ and Wales-to-UK Biobank transport $C=0.6600$. However, model specifications differed (9 terms forward vs 7 terms reverse), creating an asymmetric transport evaluation.
4. **Head-to-Head Comparisons & Multiplicity:** Table 4 and text results are internally consistent: CALON-C vs SAFEHEART-RE ($\Delta C=+0.070$, Holm $p=0.0003$), vs Montreal ($\Delta C=+0.032$, Holm $p=0.0179$), vs FH-Risk-Score ($\Delta C=+0.015$, Holm $p=0.5018$). 5-year head-to-head non-significance is consistently reported.
5. **Proportional Hazards Diagnostic Terms:** Text and Abstract consistently state that 0 of 16 tested terms violated proportional hazards assumptions ($p > 0.05$).
6. **Calibration Slopes & E:O Ratios:** Text and Table 5 consistently report UK Biobank 10-year calibration slope 1.101 (95% CI 0.884–1.318) and E:O ratio 1.008 (0.883–1.153). Internal calibration status is clearly stated.
7. **Competing Risks Failure Reporting:** Abstract, Methods, Results, and Limitations consistently acknowledge that the UK Biobank competing risk analysis script failed to execute.

---

## D. Reporting and Publication Audit

```
================================================================================
TRIPOD+AI & PROBAST METHODOLOGICAL COMPLIANCE CHECKLIST
================================================================================
Item / Domain          Status     Biostatistical Evaluation
--------------------------------------------------------------------------------
TRIPOD+AI 1 (Title)    PASS       Identifies model development, comparator 
                                  evaluation, and transport evaluation.
TRIPOD+AI 2 (Abstract) PASS       Structured abstract with objective, methods, 
                                  results (C-stats, CIs), and limitations.
TRIPOD+AI 3 (Intro)    PASS       Clear clinical context and rationale for 
                                  routine-variable parsimony.
TRIPOD+AI 4 (Target)   PASS       Target population defined as LDLR-variant 
                                  carriers free of prevalent ASCVD.
TRIPOD+AI 5 (Data)     PASS       Data sources (UK Biobank, All-Wales) described.
TRIPOD+AI 6 (Outcome)  FAIL       UK Biobank competing risk analysis crashed due 
                                  to missing 'death' column; absolute risk formula 
                                  ignores non-ASCVD mortality.
TRIPOD+AI 7 (Predict)  FAIL       High risk of bias in Wales: predictors recorded 
                                  post-baseline or at last contact (reverse 
                                  causality bias).
TRIPOD+AI 8 (Sample)   PASS       Sample size adequate: 289 events / 9 predictors 
                                  = 32.1 EPV in UK Biobank.
TRIPOD+AI 9 (Missing)  FAIL       Single median imputation within folds ignores 
                                  imputation uncertainty and missingness mechanism.
TRIPOD+AI 10 (Analysis)PASS       Ridge Cox modeling, repeated CV, bootstrap 
                                  optimism, Holm multiplicity correction.
TRIPOD+AI 11 (Strata)  FAIL       Grey-zone evaluation used superseded CALON-F 
                                  model; no risk strata validated for CALON-C.
TRIPOD+AI 13 (Subgroup)FAIL       Corrected CALON-C subgroup table missing; formal 
                                  interaction tests omitted.
TRIPOD+AI 16 (Perform) FAIL       Welsh internal discrimination metrics presented 
                                  on pre-rescue dataset (n=1,159/92).
TRIPOD+AI 18 (Calib)   PASS       Apparent calibration reported with CIs; external 
                                  calibration claims appropriately withdrawn.
TRIPOD+AI 20 (Valid)   FAIL       No independent external validation; transport 
                                  evaluations confounded by prior tuning.
PROBAST Domain 1       LOW RISK   Inclusions/exclusions defined; prevalent ASCVD 
                                  excluded.
PROBAST Domain 2       HIGH RISK  Predictor timing in Wales recorded post-baseline 
                                  or at last contact.
PROBAST Domain 3       LOW RISK   Incident ASCVD defined objectively via ICD-10 
                                  and procedure codes.
PROBAST Domain 4       HIGH RISK  Missing UKB competing risk analysis; single 
                                  median imputation; un-synchronized Welsh pipeline.
================================================================================
```

---

## E. Top Revisions

### 1. Fix UK Biobank Competing Risk Execution Bug (Fatal)
* **Action:** Merge cause-of-death registry files into the UK Biobank master table. Execute Cause-Specific Cox and Aalen–Johansen competing risk models treating non-ASCVD death as a competing event. Recalculate baseline survival $S_0(t)$ and absolute 5- and 10-year risk estimates.

### 2. Synchronize Post-Rescue Welsh Artifacts Across All Tables (Fatal)
* **Action:** Re-run the complete analytical pipeline (`code/38_CALON_C_CORRECTED.py`) for the All-Wales cohort. Re-export Table 1, Table 3, Table 5, and text metrics using the synchronized $n=1,169$ / $n_{\text{event}}=102$ risk set.

### 3. Mitigate Predictor Timing Bias in Welsh Transport Dataset (Fatal)
* **Action:** Conduct a sensitivity analysis in the All-Wales cohort restricting predictors strictly to documented pre-baseline clinical records. Report transport discrimination with and without post-baseline predictor fields to bound timing optimism.

### 4. Replace Single Median Imputation with Multiple Imputation (Major)
* **Action:** Implement 10-fold Multiple Imputation by Chained Equations (MICE) within cross-validation folds for missing continuous predictors (non-HDL, HDL, triglycerides, Lp(a)). Propagate imputation uncertainty into standard errors and confidence intervals.

### 5. Re-Run Grey-Zone Enhancer Evaluation on Frozen CALON-C Predictions (Major)
* **Action:** Re-evaluate the incremental value of adding Lp(a) and apoB/LDL-C specifically within the predicted 5%–20% 10-year risk band derived from the frozen CALON-C model equation, replacing the predecessor CALON-F output.

### 6. Perform Formal Interaction Tests and Output Corrected Subgroup Table (Major)
* **Action:** Execute likelihood ratio tests for pre-specified interaction terms ($Sex \times Age$, $Diabetes \times Non-HDL$). Export a fully synchronized subgroup table reporting CALON-C $C$-statistics stratified by sex, age ($<55$ vs $\ge 55$), and diabetes status.

### 7. Execute Symmetric Reciprocal Transport Evaluation (Moderate)
* **Action:** Apply the identical frozen 9-term UK Biobank equation to Wales and the frozen 9-term Welsh equation to UK Biobank without dropping variables, establishing a fully symmetric reciprocal transport evaluation.

### 8. Add Sensitivity Analysis for Ambiguously Dated Events (Moderate)
* **Action:** Re-run the UK Biobank primary Cox model restricting the event set to the 147 unambiguously dated ASCVD cases, treating ambiguous concomitant coding cases as censored at first code appearance.

### 9. Evaluate MICE-Imputed Sensitivity in Head-to-Head Comparisons (Moderate)
* **Action:** Perform head-to-head comparator evaluations on MICE-imputed full-cohort datasets alongside the strict complete-input subset analyses to rule out complete-case selection bias.

### 10. Fill Governance and Administrative Placeholders (Minor)
* **Action:** Supply explicit institutional review board ethics numbers, legal basis, funding statements, conflicts of interest, and data availability details.

---

## F. Inter-Panel Tension Memo

### Predicted Debate Point 1: Clinical Escalation vs Methodological Boundaries (Biostatistician vs Cardiologist)
* **Cardiologist View:** The Cardiologist will likely emphasize that CALON-C's reliance on routine lipid panels provides immediate clinical utility in primary care, enabling rapid risk stratification for statin/PCSK9i escalation without waiting for specialized Lp(a) testing.
* **Biostatistician Stance:** I must forcefully counter that clinical utility **cannot** be asserted without valid comparative Decision Curve Analysis (DCA) showing net benefit over standard care, and without external calibration-in-the-large. Furthermore, risk scores must never be used to de-risk an *LDLR* carrier or defer guideline-directed lipid lowering.

### Predicted Debate Point 2: Biological Importance of Lp(a) / apoB vs Model Parsimony (Biostatistician vs Lipid-Medicine Specialist)
* **Lipid Specialist View:** The Lipid Specialist may argue that excluding Lp(a) and apoB impairs the model's biological fidelity, pointing out that Lp(a) is an independent causal risk factor in FH and arguing that the grey-zone analysis was flawed because it used a predecessor model.
* **Biostatistician Stance:** While agreeing that the grey-zone analysis must be re-run on frozen CALON-C predictions, I will demonstrate that in multivariable prediction models, statistically significant hazard ratios (e.g., apoB/LDL-C HR 1.154) frequently fail to yield statistically significant C-statistic gains ($\Delta C = +0.0146$, 95% CI crosses zero). Model parsimony preserves evaluability in routine care without sacrificing rank discrimination.

---

# RESEARCH-TOOL STATUS TABLE

| Tool Name | Assigned Status | Retrieved Information & Review Impact |
|---|---|---|
| **/academic skill** | NOT EXPOSED/NOT CONFIGURED | Tool not callable in runtime environment. |
| **Scite AI** | NOT EXPOSED/NOT CONFIGURED | Tool not callable in runtime environment. |
| **SciSpace** | NOT EXPOSED/NOT CONFIGURED | Tool not callable in runtime environment. |
| **Elicit** | NOT EXPOSED/NOT CONFIGURED | Tool not callable in runtime environment. |
| **PubMed / Crossref Search** | USED — results returned | Native search tools retrieved primary bibliographic metadata, exact DOIs, and verified 10-year publication windows (2016–2026) for key prediction methodology (TRIPOD+AI, PROBAST), FH guidelines (2026 ACC/AHA, 2025 ESC), and comparator validation studies (SAFEHEART-RE, FH-Risk-Score, Australian FH cohort). |

---

# ELIGIBLE EVIDENCE LEDGER (17 AUGUST 2016 – 17 AUGUST 2026)

All cited primary literature used to support biostatistical findings falls strictly within the non-negotiable 10-year evidence window (17 August 2016 through 17 August 2026):

1. **Blumenthal RS, Morris PB, Gaudino M, et al.** 2026 ACC/AHA/AACVPR/ABC/ACPM/ADA/AGS/APhA/ASPC/NLA/PCNA guideline on the management of dyslipidemia. *Circulation*. 2026;153:e1154–e1276. DOI: [10.1161/CIR.0000000000001423](https://doi.org/10.1161/CIR.0000000000001423).
2. **Mach F, Koskinas KC, Roeters van Lennep JE, et al.** 2025 focused update of the 2019 ESC/EAS Guidelines for the management of dyslipidaemias. *Eur Heart J*. 2025;46:4359–4378. DOI: [10.1093/eurheartj/ehaf190](https://doi.org/10.1093/eurheartj/ehaf190).
3. **Pérez de Isla L, Alonso R, Mata N, et al.** Predicting cardiovascular events in familial hypercholesterolemia: the SAFEHEART Registry. *Circulation*. 2017;135:2133–2144. DOI: [10.1161/CIRCULATIONAHA.116.024541](https://doi.org/10.1161/CIRCULATIONAHA.116.024541).
4. **Paquette M, Dufour R, Baass A.** The Montreal-FH-SCORE: a new score to predict cardiovascular events in familial hypercholesterolemia. *J Clin Lipidol*. 2017;11:80–86. DOI: [10.1016/j.jacl.2016.10.004](https://doi.org/10.1016/j.jacl.2016.10.004).
5. **Paquette M, Bernard S, Cariou B, et al.** Familial Hypercholesterolemia-Risk-Score: a new score predicting cardiovascular events and cardiovascular mortality in familial hypercholesterolemia. *Arterioscler Thromb Vasc Biol*. 2021;41:2632–2640. DOI: [10.1161/ATVBAHA.121.316106](https://doi.org/10.1161/ATVBAHA.121.316106).
6. **Gallo A, Char
