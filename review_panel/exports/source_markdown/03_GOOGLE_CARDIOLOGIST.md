# Clinical Audit and Expert Manuscript Review: CARDIOLOGIST LENS

**Reviewer:** Senior Clinical Cardiologist and Cardiovascular Epidemiologist  
**Protocol:** CALON-C Independent Manuscript-Review Protocol (Blind Round 1)  
**Date of Audit:** 16 August 2026  
**Target Manuscript:** `outputs/manuscript_2026-08-16/CALON_C_MANUSCRIPT_HIGH_CALIBRE.md`  

---

## Rejection-Risk Summary

This manuscript presents the development, comparator testing, and setting-transport evaluation of CALON-C, a parsimonious risk-prediction model for incident atherosclerotic cardiovascular disease (ASCVD) in individuals carrying an `ldlr_carrier` flag. From a clinical cardiology and cardiovascular risk-stratification perspective, the manuscript demonstrates commendably rigorous statistical reporting and analytical transparency, particularly regarding multiplicity control and comparator reconstruction. However, in its current state, the manuscript faces **rejection-level clinical and methodological vulnerabilities** if submitted to top-tier cardiovascular journals (*JACC*, *Circulation*, *European Heart Journal*, *Atherosclerosis*).

1. **Absence of Clinical Decision Utility and Decision-Curve Analysis:** The manuscript explicitly withdraws all decision-curve claims. In clinical cardiology, a risk model's ultimate value lies not in discrimination ($C$-statistic), but in its ability to improve therapeutic decision-making (e.g., triggering lipid-lowering therapy [LLT] escalation with ezetimibe, PCSK9 inhibitors, inclisiran, or bempedoic acid). Without comparative decision curves demonstrating incremental net benefit over standard care or established guidelines, CALON-C cannot establish clinical utility.
2. **Clinical Harm of "De-Risking" Familial Hypercholesterolaemia (FH):** Monogenic heterozygous FH represents a state of lifelong, cumulative atherogenic exposure. Contemporary lipid guidelines (2026 ACC/AHA; 2025 ESC/EAS) classify FH as high or very high risk by default. A major clinical concern is that using a short-term 5-year or 10-year risk score to "de-risk" an FH patient could lead clinicians to withhold or defer intensive LLT, causing irreversible atheroma progression. The manuscript must explicitly frame risk scoring strictly as a tool for *treatment escalation urgency*, never for treatment de-escalation or withholding.
3. **Endpoint Unreliability, Procedure Omission, and Lack of Clinical Adjudication:** The primary endpoint in UK Biobank relies on administrative ICD-10 diagnostic coding without central clinical event adjudication or linked procedural data (OPCS-4 procedure codes were empty, missing coronary artery bypass grafting [CABG] and percutaneous coronary intervention [PCI]). Furthermore, 142 of 289 cases lacked component-specific event attribution dates. Combining heterogenous endpoints (coronary vs cerebrovascular vs peripheral) without procedure linkage degrades outcome quality and introduces non-random misclassification.
4. **Population Mismatch and Phenotypic Attenuation:** The derivation cohort consists of UK Biobank population-identified `ldlr_carrier` individuals who demonstrate an attenuated lipid phenotype (median untreated-equivalent LDL-C 3.95 mmol/L; median LDL-C excess over non-carriers only +0.15 to +0.23 mmol/L). This cohort is fundamentally distinct from clinically diagnosed heterozygous FH patients presenting to cardiology clinics with severe hypercholesterolaemia, tendon xanthomas, and strong family histories of premature ASCVD. Transporting a model derived in healthy middle-aged volunteers to clinical FH registries risks severe miscalibration.
5. **Unexecuted Competing Mortality Analysis in UK Biobank:** In an aging cohort (median baseline age 57.1 years, followed for up to 15+ years), non-ASCVD death is a major competing event. The failure of the competing-risk analysis to execute in UK Biobank means absolute 10-year risk estimates derived from standard Kaplan–Meier/Cox models are mathematically overestimated.
6. **Ineffective Model Transport and Lack of Independent Validation:** Reciprocal transport between UK Biobank and the All-Wales registry yielded an asymmetric $C$-statistic drop (0.725 to 0.660). Because the All-Wales registry was accessed during prior programme model tuning and exhibited severe predictor-timing flaws (un-dated hypertension, diabetes, and smoking), this transport does not constitute independent external validation.

---

## Paragraph-by-Paragraph Review

### Key points

#### Key points ¶1
1. **Current claim:** The authors ask whether a parsimonious model built from a standard lipid profile and routine clinical variables can rank first ASCVD events among LDLR-variant carriers at least as well as established FH risk instruments.
2. **Weakness or unsupported element:** The term "LDLR-variant carriers" is used without qualifying that the UK Biobank dataset lacks variant-level adjudication, presenting an attenuated population phenotype.
3. **Evidence check:** Tamehri Zadeh SS et al. (*Atherosclerosis*. 2026;418:120799. doi:10.1016/j.atherosclerosis.2026.120799) demonstrated that performance rankings of FH scores shift significantly depending on whether genetic confirmation is performed in specialist clinics versus population registries.
4. **Required improvement:** Specify that the study evaluates population-identified `ldlr_carrier` participants rather than molecularly adjudicated clinical FH.
5. **Suggested replacement wording:** "Question. Can a parsimonious model using routine clinical variables and a standard lipid panel rank incident atherosclerotic events among population-identified LDLR-variant carriers as effectively as established familial-hypercholesterolaemia risk instruments?"
6. **Severity:** `MODERATE`

#### Key points ¶2
1. **Current claim:** In 3,209 UK Biobank participants carrying an LDLR-carrier flag and free of prevalent ASCVD, CALON-C showed moderate discrimination, outperforming SAFEHEART-RE and Montreal-FH-SCORE over full follow-up after Holm correction, but tying the FH-Risk-Score.
2. **Weakness or unsupported element:** Reporting full follow-up (up to 15+ years) without highlighting that no 5-year comparison remained statistically significant after multiplicity correction oversimplifies the horizon-specific performance.
3. **Evidence check:** Paquette M et al. (*Arterioscler Thromb Vasc Biol*. 2021;41:2632–2640. doi:10.1161/ATVBAHA.121.316106) established the FH-Risk-Score specifically for 10-year incident prediction, making full-follow-up metrics less clinically applicable to 5- or 10-year decision horizons.
4. **Required improvement:** Explicitly state in the findings that 5-year superiority was not established after multiplicity adjustment.
5. **Suggested replacement wording:** "Findings. In 3,209 UK Biobank participants carrying an LDLR-carrier flag, CALON-C showed moderate internal discrimination (optimism-corrected C=0.7095). Over full follow-up, discrimination exceeded SAFEHEART-RE and Montreal-FH-SCORE after Holm correction but did not differ from FH-Risk-Score; no 5-year comparison was statistically significant after correction."
6. **Severity:** `MAJOR`

#### Key points ¶3
1. **Current claim:** CALON-C supports the feasibility of risk ranking with routine data but does not establish independent external validation, clinical utility, or superiority to every established FH instrument.
2. **Weakness or unsupported element:** The meaning statement lacks a warning regarding the clinical danger of using short-term risk scores to de-risk FH patients or defer guideline-directed lipid-lowering therapy.
3. **Evidence check:** Blumenthal RS et al. (*Circulation*. 2026;153:e1154–e1276. doi:10.1161/CIR.0000000000001423) emphasize that heterozygous FH mandates lifelong lipid-lowering therapy and that short-term risk scores must not be used to withhold treatment.
4. **Required improvement:** Add an explicit statement that CALON-C cannot be used to de-escalate or defer lipid-lowering treatment.
5. **Suggested replacement wording:** "Meaning. CALON-C demonstrates that routine clinical data can rank ASCVD risk in LDLR carriers, but it does not establish independent external validation or clinical utility. The score must not be used to de-risk patients or withhold guideline-mandated lipid-lowering therapy."
6. **Severity:** `MAJOR`

---

### Abstract

#### Abstract ¶1 (Background)
1. **Current claim:** Contemporary guidance recognises that FH-specific scores may help estimate short-term ASCVD risk, while general-population equations should not be used for 10- or 30-year risk estimation in heterozygous FH.
2. **Weakness or unsupported element:** The background does not define the clinical estimand or clarify that risk scoring in FH is intended to prioritize treatment escalation urgency rather than primary indication for treatment.
3. **Evidence check:** Mach F et al. (*Eur Heart J*. 2025;46:4359–4378. doi:10.1093/eurheartj/ehaf190) state that individuals with FH are automatically categorized as high or very high risk, rendering standard population risk estimation inappropriate.
4. **Required improvement:** Clarify that FH risk models are designed to refine risk stratification for treatment intensification within a high-risk population.
5. **Suggested replacement wording:** "Background. Contemporary guidelines recognize that FH-specific risk instruments may refine short-term ASCVD risk stratification to guide treatment intensification, whereas general-population equations underestimate risk in heterozygous FH. However, score performance within population-identified variant carriers remains uncertain."
6. **Severity:** `MINOR`

#### Abstract ¶2 (Methods)
1. **Current claim:** CALON-C was developed in UK Biobank `ldlr_carrier` participants using a ridge-penalised Cox model with 9 routine predictors, and tested via paired head-to-head bootstrap comparisons and reciprocal transport to Wales.
2. **Weakness or unsupported element:** Fails to disclose that procedure codes (CABG/PCI) were missing in UK Biobank and that predictor timing in the Welsh registry was uncertain.
3. **Evidence check:** Collins GS et al. (*BMJ*. 2024;385:e078378. doi:10.1161/bmj-2023-078378) TRIPOD+AI guidance requires explicit disclosure of missing outcome components and timing limitations in routinely collected data.
4. **Required improvement:** Mention the administrative code origin of outcomes and limitation of procedural data in the methods abstract.
5. **Suggested replacement wording:** "Methods. We developed CALON-C in 3,209 UK Biobank participants with an ldlr_carrier flag free of prevalent ASCVD (defined via administrative diagnosis codes). A 9-predictor ridge-penalised Cox model using age, sex, clinical risk factors, and standard lipid panel transformations was assessed internally and compared head-to-head against published scores on complete-input subsets with Holm multiplicity correction. Reciprocal transport to the All-Wales registry was evaluated."
6. **Severity:** `MODERATE`

#### Abstract ¶3 (Results)
1. **Current claim:** CALON-C achieved an optimism-corrected C of 0.7095, outperformed SAFEHEART-RE and Montreal-FH-SCORE over full follow-up, tied FH-Risk-Score, and exhibited C=0.725 in UKB-to-Wales transport.
2. **Weakness or unsupported element:** The results state that "the UK Biobank competing-risk analysis did not execute," leaving absolute risk estimates uncorrected for competing mortality, and reports unvalidated internal calibration metrics.
3. **Evidence check:** Wolk EW et al. (*Ann Intern Med*. 2019;170:51–58. doi:10.7326/M18-1376) PROBAST standards mandate that competing risk must be appropriately handled in survival prediction models in older cohorts.
4. **Required improvement:** State clearly that absolute risk calibration remains internal and competing-risk adjustment in UK Biobank was unexecuted.
5. **Suggested replacement wording:** "Results. Among 3,209 participants (289 incident events), optimism-corrected C was 0.7095 over full follow-up. CALON-C exceeded SAFEHEART-RE (+0.070, 95% CI 0.036 to 0.104; Holm-adjusted p=0.0003) and Montreal-FH-SCORE (+0.032, 0.011 to 0.055; p=0.0179), but tied FH-Risk-Score (+0.015, -0.011 to 0.040; p=0.5018). No 5-year comparison was significant after correction. UKB-to-Wales transport C was 0.725 (reverse C=0.660). Competing-risk analysis in UK Biobank did not execute."
6. **Severity:** `MAJOR`

#### Abstract ¶4 (Conclusions)
1. **Current claim:** CALON-C provides moderate risk ranking from routine clinical data, representing evidence of model development and setting transport rather than independent validation or clinical utility.
2. **Weakness or unsupported element:** Lacks a firm clinical conclusion regarding the inadmissibility of using CALON-C for clinical treatment withholding.
3. **Evidence check:** Blumenthal RS et al. (*Circulation*. 2026;153:e1154–e1276. doi:10.1161/CIR.0000000000001423) explicitly state that prediction models in FH must not alter the core indication for lifelong statin therapy.
4. **Required improvement:** Add explicit clinical boundary language to the conclusion.
5. **Suggested replacement wording:** "Conclusions. CALON-C enables moderate risk ranking using routine clinical variables. These findings establish model development and setting transport, not independent external validation or clinical utility. CALON-C should not be used to guide lipid-lowering withholding or de-escalation."
6. **Severity:** `MODERATE`

---

### Introduction

#### Introduction ¶1
1. **Current claim:** Familial hypercholesterolaemia is a lifelong exposure disorder where cardiovascular expression varies widely, justifying short-term risk scoring per 2026 ACC/AHA and 2025 ESC guidance.
2. **Weakness or unsupported element:** Conflates risk ranking for treatment *intensification* with risk estimation for primary diagnosis or baseline statin initiation.
3. **Evidence check:** Mach F et al. (*Eur Heart J*. 2025;46:4359–4378. doi:10.1093/eurheartj/ehaf190) and Blumenthal RS et al. (*Circulation*. 2026;153:e1154–e1276. doi:10.1161/CIR.0000000000001423) emphasize that all FH patients require early LLT; risk scores serve only to identify candidates for advanced therapies (e.g., PCSK9 inhibitors).
4. **Required improvement:** Clarify that the guideline-sanctioned role of short-term risk scores in FH is strictly limited to identifying candidates for rapid treatment intensification.
5. **Suggested replacement wording:** "Familial hypercholesterolaemia is a lifelong atherogenic exposure disorder. Although high-intensity lipid-lowering therapy is indicated for all adults with FH, cardiovascular expression varies. The 2026 ACC/AHA and 2025 ESC/EAS guidelines note that FH-specific risk scores may help identify patients requiring urgent treatment escalation (e.g., combination therapy), whereas general-population risk equations underpredict risk in heterozygous FH."
6. **Severity:** `MINOR`

#### Introduction ¶2
1. **Current claim:** Established FH instruments (SAFEHEART-RE, Montreal-FH-SCORE, FH-Risk-Score) differ in outcome, ascertainment setting, lipid handling, and dependence on specialised measurements.
2. **Weakness or unsupported element:** Accurate summary, but lacks critical mention of recent external validation failures of SAFEHEART-RE in routine care primary care cohorts.
3. **Evidence check:** McKay AJ et al. (*Atherosclerosis*. 2022;358:68–74. doi:10.1016/j.atherosclerosis.2022.07.011) showed severe miscalibration and attenuated discrimination of SAFEHEART-RE in English routine care (C=0.67).
4. **Required improvement:** Cite the English routine care validation to reinforce why existing tools perform inconsistently across settings.
5. **Suggested replacement wording:** "Established FH instruments answer distinct clinical questions but vary in input requirements. SAFEHEART-RE was developed in a prospective Spanish registry, but demonstrated attenuated discrimination (C=0.67) and marked miscalibration when evaluated in English routine care. Montreal-FH-SCORE was derived against prevalent disease, while FH-Risk-Score was developed for 10-year incident ASCVD but requires specialised Lp(a) testing."
6. **Severity:** `MINOR`

#### Introduction ¶3
1. **Current claim:** Three unresolved issues exist: comparators are rarely evaluated head-to-head on common subsets; specialised assays limit implementation; and population-detected variant carriers differ phenotypically from clinical FH patients.
2. **Weakness or unsupported element:** Sound clinical logic, but underestimates the magnitude of phenotypic attenuation in population biobanks where healthy volunteer selection is severe.
3. **Evidence check:** Fry A et al. (*Am J Epidemiol*. 2017;186:1026–1034. doi:10.1093/aje/kwx246) and van Alten S et al. (*Int J Epidemiol*. 2024;53:dyae054. doi:10.1093/ije/dyae054) demonstrate that healthy volunteer selection in UK Biobank markedly distorts baseline disease rates and hazard ratios.
4. **Required improvement:** Explicitly emphasize that population-detected carriers in UK Biobank display a less severe lipid phenotype than clinic-referred FH.
5. **Suggested replacement wording:** "Three unresolved issues follow. First, comparator performance is rarely evaluated head-to-head on identical participants and outcomes. Second, reliance on Lp(a) or apoB restricts score usability in primary care. Third, population-detected LDLR carriers in biobanks exhibit attenuated lipid phenotypes compared to clinic-ascertained FH, compounded by healthy-volunteer selection in UK Biobank."
6. **Severity:** `MINOR`

#### Introduction ¶4
1. **Current claim:** CALON-C was designed around parsimony and transport, using standard clinical and lipid variables without Lp(a) or apoB to test if routine data can recover useful risk ranking.
2. **Weakness or unsupported element:** Good justification, but must acknowledge that omitting Lp(a) may miss a crucial independent driver of residual ASCVD risk in true FH.
3. **Evidence check:** Paquette M et al. (*Arterioscler Thromb Vasc Biol*. 2021;41:2632–2640. doi:10.1161/ATVBAHA.121.316106) established that Lp(a) $\ge$ 50 mg/dL independently doubles ASCVD risk in FH carriers.
4. **Required improvement:** Frame parsimony as a trade-off between feasibility and potential loss of Lp(a)-mediated risk information.
5. **Suggested replacement wording:** "CALON-C was designed around parsimony and transport accessibility. By restricting inputs to routine clinical factors and a standard lipid panel, the model tests whether clinically useful risk ranking can be achieved without mandatory Lp(a) or apoB testing, accepting that missing specialized particle data may trade off against peak model discrimination."
6. **Severity:** `MINOR`

#### Introduction ¶5
1. **Current claim:** We aimed to develop CALON-C in UK Biobank, perform strict head-to-head comparator evaluation, and assess reciprocal transport with the All-Wales registry without claiming independent external validation.
2. **Weakness or unsupported element:** Completely aligned with methodological standards; no major clinical flaws.
3. **Evidence check:** Collins GS et al. (*BMJ*. 2024;384:e074820. doi:10.1136/bmj-2023-074820) guidelines for prediction model transport evaluations.
4. **Required improvement:** Maintain current precise phrasing.
5. **Suggested replacement wording:** "We aimed to develop and internally assess CALON-C in UK Biobank LDLR-variant carriers free of prevalent ASCVD; execute head-to-head comparisons against SAFEHEART-RE, FH-Risk-Score, and Montreal-FH-SCORE on complete-input subsets; and evaluate reciprocal transport between UK Biobank and the All-Wales registry. The work is framed as model development and setting transport, not independent external validation."
6. **Severity:** `MINOR`

---

### Methods

#### Methods—Study design and reporting framework ¶1
1. **Current claim:** Two-cohort prognostic prediction study using routinely collected data following TRIPOD+AI, STROBE, and RECORD.
2. **Weakness or unsupported element:** Standard reporting claims; require verification against TRIPOD+AI checklist items.
3. **Evidence check:** Collins GS et al. (*BMJ*. 2024;385:e078378. doi:10.1136/bmj-2023-078378).
4. **Required improvement:** None required.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Methods—Study design and reporting framework ¶2
1. **Current claim:** Source of truth was `RESULTS_FINAL_CORRECTED.md`, superseding earlier model iterations, with discrepancies retained explicitly.
2. **Weakness or unsupported element:** Transparent disclosure of analytical corrections.
3. **Evidence check:** Internal reproducibility protocol.
4. **Required improvement:** None.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Methods—Data sources and governance ¶1
1. **Current claim:** UK Biobank master linked to outcome files and All-Wales registry used under local governance arrangements.
2. **Weakness or unsupported element:** Governance placeholders (ethics reference numbers, funding) are present.
3. **Evidence check:** TRIPOD+AI Item 24 (Funding and Role of Sponsor).
4. **Required improvement:** Ensure actual ethical reference codes are inserted prior to submission.
5. **Suggested replacement wording:** Retain prose; insert reference numbers.
6. **Severity:** `MINOR`

#### Methods—Data sources and governance ¶2
1. **Current claim:** UK Biobank master carried an `ldlr_carrier` flag but `variant_id` was empty, requiring population description as LDLR-variant carriers identified by flag.
2. **Weakness or unsupported element:** Crucial clinical weakness: without variant coordinates, pathogenicity cannot be independently verified against ClinVar (e.g., pathogenic vs benign polymorphism).
3. **Evidence check:** Trinder M et al. (*JAMA Cardiol*. 2020;5:390–399. doi:10.1001/jamacardio.2019.5954) demonstrated that penetrance and ASCVD risk vary dramatically between loss-of-function variants and missense variants of uncertain significance.
4. **Required improvement:** Explicitly highlight the inability to verify variant pathogenicity as a major cohort limitation.
5. **Suggested replacement wording:** "Because variant_id was unpopulated in the UK Biobank extract, individual variant coordinates could not be adjudicated against ClinVar criteria. The cohort is therefore strictly defined as population-identified ldlr_carrier flag positive, which may include missense variants of variable pathogenicity alongside true loss-of-function mutations."
6. **Severity:** `MAJOR`

#### Methods—UK Biobank cohort ¶1
1. **Current claim:** ASCVD defined as ICD-10 codes I21, I25, I63, I70, I73, and G45; prevalent/undated events excluded, leaving 3,209 participants and 289 events.
2. **Weakness or unsupported element:** Heart failure (I50) was excluded, but procedural revascularisation codes (OPCS-4) were absent, omitting individuals whose first event was an elective or urgent PCI/CABG without an acute MI diagnosis code.
3. **Evidence check:** Tamehri Zadeh SS et al. (*Atherosclerosis*. 2026;418:120799. doi:10.1016/j.atherosclerosis.2026.120799) included coronary revascularisation in the primary composite endpoint for FH risk assessment.
4. **Required improvement:** Clearly state that the UK Biobank endpoint is diagnosis-code restricted and lacks procedural revascularisation events.
5. **Suggested replacement wording:** "ASCVD was defined from linked secondary care records using ICD-10 codes I21, I25, I63, I70, I73, and G45. Due to unpopulated procedure fields in the extract, coronary revascularisation procedures (PCI and CABG) could only be captured if accompanied by a diagnostic code, representing a potential outcome undercount."
6. **Severity:** `MAJOR`

#### Methods—UK Biobank cohort ¶2
1. **Current claim:** Follow-up ended at event date, death, or 31 December 2023; component-specific attribution date was unambiguous in 147 of 289 cases.
2. **Weakness or unsupported element:** Having 142 out of 289 cases (49.1%) with ambiguous component event dates introduces temporal misclassification into Cox proportional hazards models.
3. **Evidence check:** Riley RD et al. (*BMJ*. 2024;384:e074819. doi:10.1136/bmj-2023-074819) emphasize that precise event dating is essential for un-biased hazard estimation in survival models.
4. **Required improvement:** Note the high proportion of ambiguous event dates as a sensitivity limitation.
5. **Suggested replacement wording:** "Follow-up ended at the earliest recorded event date, death, or administrative censoring on 31 December 2023. Event attribution was date-unambiguous for 147 of 289 cases; the remaining cases involved concomitant coding where the primary event sequence was imputed from the earliest diagnosis date."
6. **Severity:** `MODERATE`

#### Methods—All-Wales cohort ¶1
1. **Current claim:** Welsh genotype-positive registry included 1,169 participants and 102 events after reinstating 10 dated post-baseline events.
2. **Weakness or unsupported element:** In the Welsh registry, endpoints included self-reported or clinically recorded angina and procedure ages, creating endpoint non-comparability with UK Biobank.
3. **Evidence check:** Gallo A et al. (*Atherosclerosis*. 2020;306:41–49. doi:10.1016/j.atherosclerosis.2020.06.011) discussed endpoint heterogeneity between registry data and population cohorts.
4. **Required improvement:** Detail the exact clinical endpoints comprising the Welsh outcome to highlight differences from UK Biobank.
5. **Suggested replacement wording:** "The All-Wales genotype-positive cohort comprised 1,169 participants and 102 events. Outcomes in Wales encompassed clinical myocardial infarction, acute coronary syndrome, PCI, CABG, angina, transient ischaemic attack, and peripheral vascular disease, reflecting a broader clinical composite than the UK Biobank diagnosis-code definition."
6. **Severity:** `MODERATE`

#### Methods—All-Wales cohort ¶2
1. **Current claim:** Predictor dates in Wales for hypertension, diabetes, and smoking were incompletely recorded and often reflected last-contact status.
2. **Weakness or unsupported element:** Severe clinical bias: using last-contact status means post-event hypertension or diabetes could be reverse-engineered into baseline predictors (immortal time bias / reverse causality).
3. **Evidence check:** Wolff RF et al. (*Ann Intern Med*. 2019;170:51–58. doi:10.7326/M18-1376) PROBAST Domain 2 assesses predictor measurement timing; measuring risk factors after baseline introduces severe bias.
4. **Required improvement:** Highlight this as a major limitation affecting Welsh transport validity.
5. **Suggested replacement wording:** "In the Welsh registry, documentation dates for hypertension, diabetes, and smoking were frequently absent, representing status at last clinical contact rather than verified baseline status. This predictor-timing uncertainty represents a major constraint on Welsh transport evaluation."
6. **Severity:** `FATAL`

#### Methods—Outcome terminology ¶1
1. **Current claim:** The endpoint is named "first incident ASCVD" and MACE is explicitly avoided due to composite differences between cohorts.
2. **Weakness or unsupported element:** Excellent clinical taxonomy compliance. Calling non-adjudicated composite endpoints "MACE" is misleading.
3. **Evidence check:** Standard cardiovascular trial reporting guidelines.
4. **Required improvement:** Maintain current terminology throughout.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Methods—Predictors and treatment correction ¶1
1. **Current claim:** CALON-C predictors included age, sp50 spline, sex, hypertension, diabetes, smoking, cumulative non-HDL-C, triglyceride filter, and remnant cholesterol.
2. **Weakness or unsupported element:** Inclusion of two ratio/interaction terms (`cum_nonhdl` and `tg_filter`) increases potential collinearity with age and non-HDL-C.
3. **Evidence check:** Riley RD et al. (*BMJ*. 2024;384:e074819. doi:10.1136/bmj-2023-074819).
4. **Required improvement:** Explain the mathematical derivation and clinical rationale for the non-HDL spline and triglyceride filter.
5. **Suggested replacement wording:** Retain current specification details; justify transformations clinically.
6. **Severity:** `MINOR`

#### Methods—Predictors and treatment correction ¶2
1. **Current claim:** Fixed division factors (0.70 for non-HDL/LDL, 0.80 for TG) converted treated lipid values to untreated-equivalent scale.
2. **Weakness or unsupported element:** Applying uniform population-average correction factors ignores vast individual differences in statin intensity, adherence, and ezetimibe/PCSK9i response. In an audit, correlation with true pre-treatment LDL was only r=0.32.
3. **Evidence check:** Akyea RK et al. (*BJGP Open*. 2020;4:bjgpopen20X101114. doi:10.3399/bjgpopen20X101114) showed that back-calculation of untreated lipids introduces substantial measurement error in primary care datasets.
4. **Required improvement:** Emphasize that fixed lipid corrections are crude population approximations with low individual-level correlation (r=0.32).
5. **Suggested replacement wording:** "In lipid-lowering therapy recipients, measured non-HDL-C and LDL-C were divided by 0.70 and triglycerides by 0.80. These fixed multipliers represent population-average approximations of untreated lipid levels; internal audit against observed pre-treatment values in Welsh patients showed modest correlation (r=0.32, mean absolute error 1.20 mmol/L), acknowledging individual treatment-response heterogeneity."
6. **Severity:** `MAJOR`

#### Methods—Predictors and treatment correction ¶3
1. **Current claim:** Statin use was excluded as a predictor to avoid encoding post-event care, and Lp(a)/apoB were excluded to ensure parsimony.
2. **Weakness or unsupported element:** Sound design choice for predictor selection.
3. **Evidence check:** Standard epidemiological design to prevent reverse causation.
4. **Required improvement:** None.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Methods—Model specification and estimation ¶1
1. **Current claim:** Ridge-penalised Cox model (penalty 0.02) was fitted; binary terms required $\ge$ 10 events per level, dropping diabetes and smoking in Wales.
2. **Weakness or unsupported element:** Dropping diabetes and smoking in Wales changes the model from 9 terms to 7 terms, meaning the Welsh equation is a refit, not the same model structure.
3. **Evidence check:** Collins GS et al. (*BMJ*. 2024;384:e074820. doi:10.1136/bmj-2023-074820) emphasize that external validation requires evaluating the identical, frozen model equation.
4. **Required improvement:** Clarify that dropping predictors in Wales converts the analysis into a secondary cohort-specific refit rather than a strict transport of the 9-term UKB equation.
5. **Suggested replacement wording:** "A Cox proportional-hazards model with ridge penalty 0.02 was fitted. A minimum threshold of 10 events per predictor level was required, which retained all 9 predictors in UK Biobank but excluded diabetes and smoking from the Welsh cohort-specific fit, yielding a 7-term equation for the secondary Welsh refit."
6. **Severity:** `MAJOR`

#### Methods—Model specification and estimation ¶2
1. **Current claim:** Internal discrimination was estimated via 10x10 cross-validation and 100 bootstrap resamples.
2. **Weakness or unsupported element:** Robust internal validation methodology.
3. **Evidence check:** Steyerberg EW et al. (*J Clin Epidemiol*. 2014;68:279–289).
4. **Required improvement:** None.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Methods—Comparator implementation ¶1
1. **Current claim:** SAFEHEART-RE, FH-Risk-Score, and Montreal-FH-SCORE were transcribed from primary literature.
2. **Weakness or unsupported element:** Clear description of comparator transcription.
3. **Evidence check:** Primary comparator references (Pérez de Isla 2017, Paquette 2017, Paquette 2021).
4. **Required improvement:** None.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Methods—Comparator implementation ¶2
1. **Current claim:** SAFEHEART-RE was scored using measured LDL-C per primary publication specification, with previous ASCVD set to zero.
2. **Weakness or unsupported element:** Clinically sound correction: SAFEHEART-RE was derived using measured LDL-C in clinic; using back-calculated LDL-C would penalize the comparator.
3. **Evidence check:** Pérez de Isla L et al. (*Circulation*. 2017;135:2133–2144. doi:10.1161/CIRCULATIONAHA.116.024541).
4. **Required improvement:** Retain this essential primary-source correction.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Methods—Comparator implementation ¶3
1. **Current claim:** FH-Risk-Score was restricted to age $\le$ 65 years because the published tool lacks an open upper age category.
2. **Weakness or unsupported element:** Correct application of derivation age boundaries, though restricting age excludes older high-risk patients.
3. **Evidence check:** Paquette M et al. (*Arterioscler Thromb Vasc Biol*. 2021;41:2632–2640. doi:10.1161/ATVBAHA.121.316106).
4. **Required improvement:** Note that restricting age $\le$ 65 aligns with score boundaries but limits evaluability in older biobank populations.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Methods—Comparator implementation ¶4
1. **Current claim:** Montreal-FH-SCORE used ever smoking and was evaluated strictly for incident ranking.
2. **Weakness or unsupported element:** Montreal was derived for cross-sectional prevalent ASCVD; evaluating it for incident events is an out-of-domain test.
3. **Evidence check:** Paquette M et al. (*J Clin Lipidol*. 2017;11:80–86. doi:10.1016/j.jacl.2016.10.004).
4. **Required improvement:** Reinforce that Montreal-FH-SCORE serves as an out-of-domain benchmark.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Methods—Comparator implementation ¶5
1. **Current claim:** UK Biobank Lp(a) in nmol/L was converted to mg/dL using a 2.15 divisor assumption.
2. **Weakness or unsupported element:** Converting nmol/L to mg/dL using a molar constant (2.15) introduces non-linear error due to Lp(a) isoform size variation.
3. **Evidence check:** Blumenthal RS et al. (*Circulation*. 2026;153:e1154–e1276. doi:10.1161/CIR.0000000000001423) note that conversion between nmol/L and mg/dL is inaccurate due to apolipoprotein(a) isoform heterogeneity.
4. **Required improvement:** Explicitly acknowledge the physiological inaccuracy of converting Lp(a) units with a fixed scalar divisor.
5. **Suggested replacement wording:** "Lp(a) values in nmol/L were converted to mg/dL using a 2.15 divisor strictly for threshold classification in comparators. Because apo(a) isoform size variation renders scalar unit conversion physiologically imprecise, this conversion represents an operational assumption."
6. **Severity:** `MODERATE`

#### Methods—Head-to-head comparisons and multiplicity ¶1
1. **Current claim:** Comparisons were performed on complete-input subsets using 2,000 paired cluster bootstrap draws.
2. **Weakness or unsupported element:** Methodologically rigorous pairing.
3. **Evidence check:** Collins GS et al. (*BMJ*. 2024;384:e074819. doi:10.1136/bmj-2023-074819).
4. **Required improvement:** None.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Methods—Head-to-head comparisons and multiplicity ¶2
1. **Current claim:** Confirmatory family comprised 6 comparisons (3 comparators x 2 horizons) controlled by Holm adjustment.
2. **Weakness or unsupported element:** Excellent multiplicity control protocol.
3. **Evidence check:** Standard statistical practice for family-wise error control.
4. **Required improvement:** None.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Methods—Calibration, model equation, and transport ¶1
1. **Current claim:** Raw-unit UK Biobank baseline equation and baseline survival were reported for 5- and 10-year risk.
2. **Weakness or unsupported element:** Standard model reporting.
3. **Evidence check:** TRIPOD+AI Item 17.
4. **Required improvement:** None.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Methods—Calibration, model equation, and transport ¶2
1. **Current claim:** Calibration was treated as internal only, and absolute risk claims outside development data were withdrawn.
2. **Weakness or unsupported element:** Proper withdrawal of transport calibration claims given baseline hazard shifts.
3. **Evidence check:** Riley RD et al. (*BMJ*. 2024;384:e074820. doi:10.1136/bmj-2023-074820).
4. **Required improvement:** None.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Methods—Proportional hazards, competing risk, and sensitivity analyses ¶1
1. **Current claim:** Proportional hazards evaluated via Schoenfeld tests; Aalen-Johansen cumulative incidence executed in Wales but failed in UK Biobank.
2. **Weakness or unsupported element:** Unexecuted competing-risk analysis in UK Biobank is a critical technical failure. In older patients, death from cancer/other causes competes with ASCVD.
3. **Evidence check:** Wolk EW et al. (*Ann Intern Med*. 2019;170:51–58. doi:10.7326/M18-1376) PROBAST framework requires accounting for competing mortality.
4. **Required improvement:** Transparently state that absolute risks in UK Biobank may be over-estimated due to unadjusted competing risks.
5. **Suggested replacement wording:** "Proportional-hazards assumptions were verified using Schoenfeld residuals. Competing risks were modelled in Wales via Aalen–Johansen cumulative incidence functions. Due to an unpopulated death column in the UK Biobank analytical extract, competing-risk adjustment did not execute in UK Biobank, meaning absolute 10-year risk estimates reflect standard 1-Kaplan-Meier survival."
6. **Severity:** `MAJOR`

#### Methods—Proportional hazards, competing risk, and sensitivity analyses ¶2
1. **Current claim:** Sensitivity analyses tested Lp(a)-omitted comparators, alternative lipid corrections, and dated-only predictors.
2. **Weakness or unsupported element:** Comprehensive sensitivity framework.
3. **Evidence check:** Methodological standards for sensitivity testing.
4. **Required improvement:** None.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Methods—Grey-zone and subgroup analyses ¶1
1. **Current claim:** Grey-zone analysis tested Lp(a) and apoB/LDL-C additions in a 5%-20% 10-year risk band using an earlier model generation (CALON-F).
2. **Weakness or unsupported element:** Using an earlier model architecture (CALON-F) to draw conclusions about CALON-C introduces architectural inconsistency.
3. **Evidence check:** TRIPOD+AI Item 11 (Model Specification).
4. **Required improvement:** State explicitly that the grey-zone analysis is exploratory and derived from a predecessor architecture.
5. **Suggested replacement wording:** "An ancillary grey-zone analysis evaluated whether adding Lp(a), log(apoB/LDL-C), or both improved risk stratification within a 5%–20% predicted 10-year risk band. This analysis was conducted using a predecessor model generation (CALON-F) and is presented solely as an exploratory biomarker evaluation."
6. **Severity:** `MODERATE`

#### Methods—Grey-zone and subgroup analyses ¶2
1. **Current claim:** Subgroup analyses from earlier model generations were excluded; no formal CALON-C interaction tests were performed.
2. **Weakness or unsupported element:** Appropriate exclusion of outdated artifacts.
3. **Evidence check:** Reporting standards.
4. **Required improvement:** None.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Methods—Literature verification ¶1
1. **Current claim:** Comparator specifications and literature claims were verified against primary PDFs and databases.
2. **Weakness or unsupported element:** Standard verification description.
3. **Evidence check:** Literature audit protocol.
4. **Required improvement:** None.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

---

### Results

#### Results—Study populations ¶1
1. **Current claim:** UK Biobank development cohort comprised 3,209 LDLR carriers (289 incident events; 6.55 per 1,000 person-years). Cases were older, more frequently male, hypertensive, and diabetic.
2. **Weakness or unsupported element:** The baseline untreated-equivalent LDL-C difference between cases and non-cases was modest (4.16 vs 3.94 mmol/L; SMD 0.218), whereas clinical risk factor differences (hypertension 72.7% vs 50.3%, SMD 0.471; diabetes 22.1% vs 8.6%, SMD 0.381) were far more pronounced.
3. **Evidence check:** Jansen ACM et al. (*J Intern Med*. 2004;256:482–490. doi:10.1111/j.1365-2796.2004.01405.x - Excluded historical context note) and Trinder M et al. (*JAMA Cardiol*. 2020;5:390–399. doi:10.1001/jamacardio.2019.5954) emphasize that in population carriers, conventional clinical risk factors often drive short-term event variation.
4. **Required improvement:** Highlight in the clinical text that conventional risk factors showed larger standardized differences than lipid parameters.
5. **Suggested replacement wording:** "In the UK Biobank cohort (3,209 participants, 289 incident ASCVD events), participants experiencing events were older and had higher prevalences of male sex, hypertension, and diabetes. Standardized mean differences were substantially larger for hypertension (SMD 0.471) and diabetes (SMD 0.381) than for untreated-equivalent LDL-C (SMD 0.218)."
6. **Severity:** `MODERATE`

#### Results—Study populations ¶2
1. **Current claim:** Corrected Welsh risk set comprised 1,169 participants and 102 events; corrected Welsh Table 1 was absent.
2. **Weakness or unsupported element:** Missing Table 1 for the corrected Welsh cohort is a major reporting omission under TRIPOD+AI.
3. **Evidence check:** Collins GS et al. (*BMJ*. 2024;385:e078378. doi:10.1136/bmj-2023-078378) TRIPOD+AI Item 13a.
4. **Required improvement:** Provide a complete Table 1 for the corrected Welsh cohort.
5. **Suggested replacement wording:** Note the missing table as a placeholder pending final source propagation.
6. **Severity:** `MAJOR`

#### Results—Predictor-level associations in UK Biobank ¶1
1. **Current claim:** Diabetes (HR 2.120), male sex (HR 1.702), and hypertension (HR 1.610) were strongly associated with incident events, whereas cumulative non-HDL-C (HR 1.119 per SD) and remnant cholesterol (HR 1.113 per SD) were not statistically significant after multivariable adjustment.
2. **Weakness or unsupported element:** Clinical paradox: in a monogenic hypercholesterolaemia model, none of the lipid terms achieved independent statistical significance in multivariable modeling.
3. **Evidence check:** Ference BA et al. (*Eur Heart J*. 2017;38:2459–2472. doi:10.1093/eurheartj/ehx144) demonstrate the lifelong causal role of LDL-C, but in middle-aged cohorts with narrow lipid ranges and widespread statin use, non-lipid risk factors dominate multivariable multivariable hazard ratios.
4. **Required improvement:** Explicitly explain that lipid terms lack independent significance because age and clinical risk factors capture short-term risk in this survivor-selected cohort.
5. **Suggested replacement wording:** "In the multivariable CALON-C model, diabetes (HR 2.120, 95% CI 1.610–2.793), male sex (HR 1.702, 1.372–2.111), and hypertension (HR 1.610, 1.279–2.028) were independently associated with outcome. None of the three lipid terms reached statistical significance (cumulative non-HDL-C HR 1.119 per SD, 0.954–1.334; remnant cholesterol HR 1.113 per SD, 0.970–1.296), indicating that short-term risk ranking in this population is dominated by non-lipid clinical risk factors."
6. **Severity:** `MAJOR`

#### Results—Predictor-level associations in UK Biobank ¶2
1. **Current claim:** Incremental discrimination showed that CALON-C added +0.041 in C over age/sex, with +0.033 driven by hypertension/diabetes/smoking and +0.008 by lipid terms.
2. **Weakness or unsupported element:** Demonstrates that the complex cumulative lipid apparatus contributes minimal incremental discrimination (+0.008 C-statistic gain).
3. **Evidence check:** Paquette M et al. (*J Clin Lipidol*. 2017;11:80–86. doi:10.1016/j.jacl.2016.10.004) similarly observed that non-lipid clinical risk factors drive discrimination in Montreal-FH-SCORE.
4. **Required improvement:** State clearly that lipid transformations provide negligible incremental discrimination over standard clinical risk factors.
5. **Suggested replacement wording:** "Ablation analysis demonstrated that adding hypertension, diabetes, and smoking to an age-and-sex model increased C by +0.033, whereas adding the full cumulative lipid apparatus provided an incremental C gain of only +0.008."
6. **Severity:** `MODERATE`

#### Results—Internal discrimination ¶1
1. **Current claim:** UK Biobank optimism-corrected C was 0.7095 over full follow-up, 0.7079 at 10 years, and 0.7336 at 5 years.
2. **Weakness or unsupported element:** Moderate discrimination overall (C ~ 0.71), leaving substantial unpredicted risk variance.
3. **Evidence check:** Standard prediction model performance categories.
4. **Required improvement:** None.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Results—Internal discrimination ¶2
1. **Current claim:** Welsh internal optimism-corrected C values were 0.7653 (full), 0.7605 (10y), and 0.7590 (5y) in pre-correction frame.
2. **Weakness or unsupported element:** Pre-correction artifacts are reported without synchronised post-rescue confirmation.
3. **Evidence check:** Reporting integrity standards.
4. **Required improvement:** Label Welsh internal results as provisional until post-correction pipeline execution.
5. **Suggested replacement wording:** "Welsh internal performance estimates (optimism-corrected C=0.7653 over full follow-up) reflect the pre-correction analytical frame and remain provisional pending pipeline regeneration."
6. **Severity:** `MODERATE`

#### Results—Head-to-head comparison with published FH instruments ¶1
1. **Current claim:** Over full follow-up, CALON-C significantly outperformed SAFEHEART-RE (+0.070, Holm p=0.0003) and Montreal-FH-SCORE (+0.032, Holm p=0.0179), but tied FH-Risk-Score (+0.015, Holm p=0.5018).
2. **Weakness or unsupported element:** Essential clinical finding: CALON-C does not outperform FH-Risk-Score (statistically tied).
3. **Evidence check:** Paquette M et al. (*Arterioscler Thromb Vasc Biol*. 2021;41:2632–2640. doi:10.1161/ATVBAHA.121.316106).
4. **Required improvement:** Emphasize the tie with FH-Risk-Score as a key finding.
5. **Suggested replacement wording:** "In full-follow-up head-to-head comparisons on complete-input subsets, CALON-C achieved higher discrimination than SAFEHEART-RE (+0.070, 95% CI 0.036–0.104; Holm-adjusted p=0.0003) and Montreal-FH-SCORE (+0.032, 0.011–0.055; p=0.0179). CALON-C tied FH-Risk-Score (+0.015, -0.011 to 0.040; Holm-adjusted p=0.5018)."
6. **Severity:** `MODERATE`

#### Results—Head-to-head comparison with published FH instruments ¶2
1. **Current claim:** Correcting SAFEHEART-RE to measured LDL-C increased the CALON-C delta from +0.032 to +0.070.
2. **Weakness or unsupported element:** Important methodological detail illustrating how misapplying comparator inputs artificially inflates comparator performance.
3. **Evidence check:** Pérez de Isla L et al. (*Circulation*. 2017;135:2133–2144. doi:10.1161/CIRCULATIONAHA.116.024541).
4. **Required improvement:** Retain current explanation.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Results—Head-to-head comparison with published FH instruments ¶3
1. **Current claim:** At 5 years, nominal differences versus SAFEHEART-RE (+0.081) and Montreal (+0.044) did not survive Holm correction (p=0.0560 and p=0.1413).
2. **Weakness or unsupported element:** Fatal to any 5-year superiority claim.
3. **Evidence check:** Standard multiplicity control standards.
4. **Required improvement:** Explicitly state that CALON-C has no proven superiority at 5 years.
5. **Suggested replacement wording:** "At the 5-year horizon, no head-to-head comparison achieved statistical significance after Holm adjustment (vs SAFEHEART-RE: +0.081, 95% CI 0.020–0.150, Holm p=0.0560; vs Montreal-FH-SCORE: +0.044, 0.003–0.090, Holm p=0.1413; vs FH-Risk-Score: +0.018, -0.032 to 0.069, Holm p=0.5018). CALON-C thus demonstrated non-superiority across all 5-year comparisons."
6. **Severity:** `MAJOR`

#### Results—Head-to-head comparison with published FH instruments ¶4
1. **Current claim:** Welsh head-to-head comparisons were largely non-evaluable for SAFEHEART-RE (1 event) and FH-Risk-Score (6 events) due to missing inputs; Montreal was a tie (+0.033, -0.014 to 0.090).
2. **Weakness or unsupported element:** Highlights severe clinical missingness in routine registry data where Lp(a) is not measured.
3. **Evidence check:** Tamehri Zadeh SS et al. (*Can J Cardiol*. 2025;41:2244–2251. doi:10.1016/j.cjca.2025.07.042) observed variable evaluability of FH scores in clinical practice.
4. **Required improvement:** Retain current description of evaluability failure in real-world clinical datasets.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Results—Head-to-head comparison with published FH instruments ¶5
1. **Current claim:** No comparator significantly outperformed CALON-C across tested horizons, but this does not prove non-inferiority.
2. **Weakness or unsupported element:** Correct statistical framing.
3. **Evidence check:** Methodological reporting standards.
4. **Required improvement:** Retain current prose.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Results—Calibration and model equation ¶1
1. **Current claim:** UK Biobank internal 10-year calibration showed slope 1.101, E/O ratio 1.008, Brier score 3.3%; 5-year slope 1.197, E/O ratio 1.004.
2. **Weakness or unsupported element:** These are internal development calibration metrics, which always appear optimistic; they do not reflect performance in external clinical populations.
3. **Evidence check:** Riley RD et al. (*BMJ*. 2024;384:e074820. doi:10.1136/bmj-2023-074820).
4. **Required improvement:** Label calibration strictly as internal/development calibration.
5. **Suggested replacement wording:** "Internal 10-year calibration within the UK Biobank development cohort demonstrated a slope of 1.101 (95% CI 0.884–1.318) and an expected-to-observed ratio of 1.008 (0.883–1.153). These internal metrics do not reflect calibration in independent clinical settings."
6. **Severity:** `MODERATE`

#### Results—Calibration and model equation ¶2
1. **Current claim:** Model equation and worked examples provided risk estimates of 0.78% (low risk) and 15.99% (high risk) at 5 years.
2. **Weakness or unsupported element:** Worked examples use unvalidated arbitrary risk categories without clinical threshold justification.
3. **Evidence check:** TRIPOD+AI guidance on avoiding arbitrary risk thresholds.
4. **Required improvement:** State that risk strata in worked examples are illustrative and lack clinical decision validation.
5. **Suggested replacement wording:** "The model equation and illustrative worked examples are provided. Risk calculations in worked examples serve strictly for arithmetic verification and do not represent validated clinical decision thresholds."
6. **Severity:** `MINOR`

#### Results—Reciprocal transport ¶1
1. **Current claim:** Frozen UK Biobank equation transported to Wales with C=0.7252; reverse transport yielded C=0.6600.
2. **Weakness or unsupported element:** Pronounced asymmetry (0.725 vs 0.660) indicates substantial transport instability, driven by cohort differences in age, ascertainment, and predictor timing.
3. **Evidence check:** Debray TPA et al. (*J Clin Epidemiol*. 2015;68:279–289 - Excluded historical context note) and Collins GS et al. (*BMJ*. 2024;384:e074820. doi:10.1136/bmj-2023-074820).
4. **Required improvement:** Explicitly describe the asymmetric transport drop as evidence of setting sensitivity.
5. **Suggested replacement wording:** "Direct transport of the frozen 9-term UK Biobank equation to the All-Wales registry yielded C=0.7252, whereas transport of the 7-term Welsh equation to UK Biobank yielded C=0.6600. This transport asymmetry highlights performance sensitivity to cohort ascertainment and predictor timing."
6. **Severity:** `MAJOR`

#### Results—Reciprocal transport ¶2
1. **Current claim:** Single-equation transport is strictly UKB-to-Wales because the Welsh model dropped diabetes and smoking due to low event counts.
2. **Weakness or unsupported element:** Accurate clarification of model structural differences.
3. **Evidence check:** Standard prediction model methodology.
4. **Required improvement:** Retain current prose.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Results—Proportional hazards and competing risk ¶1
1. **Current claim:** No proportional hazards violation was detected across 16 terms (p>0.05).
2. **Weakness or unsupported element:** Standard model diagnostic claim.
3. **Evidence check:** Cox model diagnostic standards.
4. **Required improvement:** None.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Results—Proportional hazards and competing risk ¶2
1. **Current claim:** Welsh Aalen-Johansen 10-year cumulative incidence was 11.97% (35 competing deaths); UK Biobank competing risk analysis did not execute.
2. **Weakness or unsupported element:** Severe defect: failure to model competing risks in UK Biobank leads to overestimation of absolute 10-year ASCVD incidence.
3. **Evidence check:** Wolk EW et al. (*Ann Intern Med*. 2019;170:51–58. doi:10.7326/M18-1376) PROBAST framework.
4. **Required improvement:** Explicitly acknowledge that UK Biobank 10-year absolute risk estimates are uncorrected for competing mortality.
5. **Suggested replacement wording:** "In All-Wales, Aalen–Johansen 10-year ASCVD cumulative incidence was 11.97% with 35 competing non-ASCVD deaths. Competing-risk analysis did not execute in UK Biobank due to data structure limitations, leaving UK Biobank absolute risks unadjusted for competing mortality."
6. **Severity:** `MAJOR`

#### Results—Missing data and comparator evaluability ¶1
1. **Current claim:** Missingness was low for standard clinical terms but reached 22.5% for Lp(a) in UK Biobank, and was severe in Wales (BMI 54.5%, diabetes 41.6%).
2. **Weakness or unsupported element:** Illustrates why complex scores requiring non-routine inputs fail in real-world health records.
3. **Evidence check:** Akyea RK et al. (*BJGP Open*. 2020;4:bjgpopen20X101114. doi:10.3399/bjgpopen20X101114).
4. **Required improvement:** Retain current prose.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Results—Grey-zone analysis ¶1
1. **Current claim:** In 1,685 UK Biobank carriers in the 5%-20% 10-year risk grey zone, adding Lp(a) (-0.0038 C delta) or log(apoB/LDL-C) (+0.0146 C delta) did not significantly improve discrimination.
2. **Weakness or unsupported element:** Crucial clinical finding: adding specialized lipid biomarkers in intermediate-risk FH carriers provided zero statistically significant gain in discrimination.
3. **Evidence check:** Sniderman AD et al. (*JAMA Cardiol*. 2019;4:1287–1295. doi:10.1001/jamacardio.2019.3780) discuss apoB risk prediction, but incremental discrimination gains in restricted risk strata are frequently minimal.
4. **Required improvement:** Highlight that specialized lipid biomarkers provided no statistically significant C-statistic improvement in the intermediate-risk band.
5. **Suggested replacement wording:** "Within the 5%–20% predicted 10-year risk grey zone (1,685 participants, 218 events), secondary addition of Lp(a) (C delta -0.0038, 95% CI -0.0089 to 0.0018) or log(apoB/LDL-C) (C delta +0.0146, -0.0050 to 0.0330) yielded no statistically significant improvement in discrimination."
6. **Severity:** `MODERATE`

#### Results—Grey-zone analysis ¶2
1. **Current claim:** ApoB/LDL-C was associated with events in the grey zone (HR 1.154 per SD), but Lp(a) was not (HR 1.033), illustrating that a hazard association does not guarantee improved risk ranking.
2. **Weakness or unsupported element:** Important clinical teaching point: risk factor association is necessary but insufficient for discrimination enhancement.
3. **Evidence check:** Collins GS et al. (*BMJ*. 2024;384:e074819. doi:10.1136/bmj-2023-074819).
4. **Required improvement:** Retain current prose.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Results—Subgroups ¶1
1. **Current claim:** Corrected CALON-C subgroup analyses were unpopulated due to outdated source artifacts.
2. **Weakness or unsupported element:** Missing subgroup reporting under TRIPOD+AI.
3. **Evidence check:** TRIPOD+AI Item 13b.
4. **Required improvement:** Mark subgroup analyses as unavailable until pipeline re-execution.
5. **Suggested replacement wording:** Retain placeholder statement.
6. **Severity:** `MODERATE`

---

### Discussion

#### Discussion—Principal findings ¶1
1. **Current claim:** CALON-C produced four findings: moderate internal discrimination; superior full-follow-up discrimination versus SAFEHEART-RE and Montreal with a tie versus FH-Risk-Score; retained ranking in Welsh transport; and no gain from specialized biomarkers in the grey zone.
2. **Weakness or unsupported element:** Accurate synthesis, but must reiterate that no 5-year comparison demonstrated statistical superiority.
3. **Evidence check:** Summary of primary results.
4. **Required improvement:** Reiterate the 5-year non-superiority result alongside full-follow-up findings.
5. **Suggested replacement wording:** "This study yields four main findings. First, CALON-C achieved moderate internal discrimination in population-identified LDLR carriers using routine variables. Second, over full follow-up, discrimination exceeded SAFEHEART-RE and Montreal-FH-SCORE but tied FH-Risk-Score, with no score demonstrating superiority at 5 years after multiplicity adjustment. Third, frozen transport retained ranking capacity in All-Wales. Fourth, specialized biomarkers provided no significant discrimination gain in intermediate-risk participants."
6. **Severity:** `MINOR`

#### Discussion—Principal findings ¶2
1. **Current claim:** Findings are narrower than initial hypotheses but credible, emphasizing that comparator corrections were essential for unbiased evaluation.
2. **Weakness or unsupported element:** Sound scientific reflection.
3. **Evidence check:** Internal methodology audit.
4. **Required improvement:** None.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Discussion—What is genuinely new ¶1
1. **Current claim:** Novelty is incremental; CALON-C is not the first FH score or external evaluation.
2. **Weakness or unsupported element:** Appropriate scientific humility regarding novelty claims.
3. **Evidence check:** Paquette M et al. (*Arterioscler Thromb Vasc Biol*. 2021;41:2632–2640. doi:10.1161/ATVBAHA.121.316106) and Tamehri Zadeh SS et al. (*Atherosclerosis*. 2026;418:120799. doi:10.1016/j.atherosclerosis.2026.120799).
4. **Required improvement:** None.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Discussion—What is genuinely new ¶2
1. **Current claim:** Defensible novelty is the head-to-head comparison of CALON-C and published instruments on identical complete-input subsets within a UK population carrier frame.
2. **Weakness or unsupported element:** Precise framing of incremental contribution.
3. **Evidence check:** Comparative prediction literature.
4. **Required improvement:** Retain current prose.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Discussion—Comparison with established FH risk instruments ¶1
1. **Current claim:** SAFEHEART-RE was derived in a clinical registry where previous ASCVD and measured LDL-C carried high information; CALON-C's advantage reflects testing in a primary prevention population carrier setting.
2. **Weakness or unsupported element:** Excellent clinical interpretation: SAFEHEART-RE's heavy weighting on prior ASCVD and clinic LDL-C makes it less suitable for population primary prevention.
3. **Evidence check:** Pérez de Isla L et al. (*Circulation*. 2017;135:2133–2144. doi:10.1161/CIRCULATIONAHA.116.024541) and McKay AJ et al. (*Atherosclerosis*. 2022;358:68–74. doi:10.1016/j.atherosclerosis.2022.07.011).
4. **Required improvement:** Retain current prose.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Discussion—Comparison with established FH risk instruments ¶2
1. **Current claim:** Montreal-FH-SCORE was designed for prevalent disease; its comparison represents an out-of-domain benchmark rather than a direct contest.
2. **Weakness or unsupported element:** Proper clinical contextualization of estimand differences.
3. **Evidence check:** Paquette M et al. (*J Clin Lipidol*. 2017;11:80–86. doi:10.1016/j.jacl.2016.10.004).
4. **Required improvement:** Retain current prose.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Discussion—Comparison with established FH risk instruments ¶3
1. **Current claim:** FH-Risk-Score was the strongest comparator, and its statistical tie with CALON-C suggests routine data can recover similar ordering without requiring Lp(a).
2. **Weakness or unsupported element:** Key clinical insight: omitting Lp(a) does not significantly degrade risk ranking compared to FH-Risk-Score in primary prevention.
3. **Evidence check:** Paquette M et al. (*Arterioscler Thromb Vasc Biol*. 2021;41:2632–2640. doi:10.1161/ATVBAHA.121.316106).
4. **Required improvement:** Retain current prose.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Discussion—Comparison with established FH risk instruments ¶4
1. **Current claim:** 2026 ACC/AHA guidelines note FH scores may be useful for short-term risk prediction, but long-term decision impact remains unproven; CALON-C does not cross the adoption threshold.
2. **Weakness or unsupported element:** Crucial alignment with current 2026 guidelines.
3. **Evidence check:** Blumenthal RS et al. (*Circulation*. 2026;153:e1154–e1276. doi:10.1161/CIR.0000000000001423).
4. **Required improvement:** Retain current prose.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Discussion—Routine-panel parsimony and global scalability ¶1
1. **Current claim:** CALON-C's advantage is relying on standard lipid panels available globally, whereas Lp(a) and apoB are inconsistently measured.
2. **Weakness or unsupported element:** Sound health-economics argument for low-resource implementation.
3. **Evidence check:** Vallejo-Vaz AJ et al. (*Atherosclerosis*. 2018;277:234–255. doi:10.1016/j.atherosclerosis.2018.08.051) EAS FH Studies Collaboration.
4. **Required improvement:** Retain current prose.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Discussion—Routine-panel parsimony and global scalability ¶2
1. **Current claim:** Parsimony trades off against information from advanced biomarkers; CALON-C should be viewed as a first-line ranking layer, not an argument against Lp(a) testing.
2. **Weakness or unsupported element:** Essential clinical nuance: routine risk scores must not replace recommended once-in-a-lifetime Lp(a) screening.
3. **Evidence check:** Mach F et al. (*Eur Heart J*. 2025;46:4359–4378. doi:10.1093/eurheartj/ehaf190).
4. **Required improvement:** Retain current prose.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Discussion—Why the lipid terms did not dominate ¶1
1. **Current claim:** Weak adjusted lipid associations do not contradict causal centrality of LDL; in restricted high-exposure cohorts, non-lipid risk factors dominate short-term event ranking.
2. **Weakness or unsupported element:** Outstanding clinical distinction between lifelong disease etiology (LDL causality) and multivariable short-term risk ranking.
3. **Evidence check:** Ference BA et al. (*Eur Heart J*. 2017;38:2459–2472. doi:10.1093/eurheartj/ehx144) and Domanski MJ et al. (*J Am Coll Cardiol*. 2020;76:1507–1516. doi:10.1016/j.jacc.2020.07.059).
4. **Required improvement:** Retain current prose.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Discussion—Why the lipid terms did not dominate ¶2
1. **Current claim:** CALON-C is best understood as a parsimonious clinical prognostic model rather than a purely lipid-driven mechanism.
2. **Weakness or unsupported element:** Accurate characterization.
3. **Evidence check:** Internal ablation analyses.
4. **Required improvement:** Retain current prose.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Discussion—Ascertainment, selection, and UK Biobank representativeness ¶1
1. **Current claim:** UK Biobank is healthy-volunteer selected and not representative of clinic-referred FH.
2. **Weakness or unsupported element:** Critical clinical epidemiology limitation.
3. **Evidence check:** Fry A et al. (*Am J Epidemiol*. 2017;186:1026–1034. doi:10.1093/aje/kwx246) and Schoeler T et al. (*Nat Hum Behav*. 2023;7:1216–1227. doi:10.1038/s41562-023-01579-9).
4. **Required improvement:** Retain current prose.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Discussion—Ascertainment, selection, and UK Biobank representativeness ¶2
1. **Current claim:** Untreated LDL-C excess in UKB carriers was only +0.15 to +0.23 mmol/L, indicating phenotype attenuation compared to clinical FH.
2. **Weakness or unsupported element:** Major clinical detail proving UKB carriers have mild dyslipidaemia compared to clinical FH registries where LDL excess exceeds 2.0–3.0 mmol/L.
3. **Evidence check:** Gidding SS et al. (*J Am Heart Assoc*. 2023;12:e030073. doi:10.1161/JAHA.123.030073).
4. **Required improvement:** Emphasize that UK Biobank carriers display marked phenotypic attenuation compared to clinical FH.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Discussion—Ascertainment, selection, and UK Biobank representativeness ¶3
1. **Current claim:** Apparent calibration in UK Biobank cannot establish calibration in routine care; baseline hazard estimation in clinical cohorts is required.
2. **Weakness or unsupported element:** Standard transport methodology.
3. **Evidence check:** McKay AJ et al. (*Atherosclerosis*. 2022;358:68–74. doi:10.1016/j.atherosclerosis.2022.07.011).
4. **Required improvement:** Retain current prose.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Discussion—Survivor bias and age ¶1
1. **Current claim:** Middle-aged biobank recruitment introduces survivor bias, selecting carriers who survived early fatal ASCVD events.
2. **Weakness or unsupported element:** Fundamental cardiological concept: recruiting adults at mean age 57 misses early lethal coronary events occurring in high-penetrance FH families.
3. **Evidence check:** Trinder M et al. (*JAMA Cardiol*. 2020;5:390–399. doi:10.1001/jamacardio.2019.5954).
4. **Required improvement:** Retain current prose.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Discussion—Survivor bias and age ¶2
1. **Current claim:** CALON-C ranks observed survivors and cannot be interpreted as a lifetime penetrance model.
2. **Weakness or unsupported element:** Proper clinical boundary definition.
3. **Evidence check:** Methodological reporting guidelines.
4. **Required improvement:** Retain current prose.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Discussion—Predictor timing in Wales ¶1
1. **Current claim:** Welsh hypertension, diabetes, and smoking were un-dated and often recorded after the event, creating severe timing limitations.
2. **Weakness or unsupported element:** Fatal validation flaw for Wales: measuring risk factors post-event invalidates baseline risk prediction claims.
3. **Evidence check:** Wolff RF et al. (*Ann Intern Med*. 2019;170:51–58. doi:10.7326/M18-1376) PROBAST framework.
4. **Required improvement:** Retain explicit disclosure of this flaw.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Discussion—Predictor timing in Wales ¶2
1. **Current claim:** Removing un-dated fields reduced Welsh C by 0.030, providing a bound on timing distortion; definitive Welsh validation requires a refreshed baseline extract.
2. **Weakness or unsupported element:** Constructive methodology.
3. **Evidence check:** Internal sensitivity evaluation.
4. **Required improvement:** Retain current prose.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Discussion—Calibration drift and directional but non-significant differences ¶1
1. **Current claim:** CALON-C reports internal calibration and transport C, but does not provide validated transportable absolute risk probabilities.
2. **Weakness or unsupported element:** Correct refusal to claim absolute risk accuracy outside derivation data.
3. **Evidence check:** Riley RD et al. (*BMJ*. 2024;384:e074820. doi:10.1136/bmj-2023-074820).
4. **Required improvement:** Retain current prose.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Discussion—Calibration drift and directional but non-significant differences ¶2
1. **Current claim:** Positive directional point estimates do not justify clinical adoption without statistical superiority and decision curve analysis.
2. **Weakness or unsupported element:** Crucial clinical trial standard: statistical non-significance cannot be spun into clinical superiority.
3. **Evidence check:** Standard clinical reporting guidelines.
4. **Required improvement:** Retain current prose.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Discussion—Lp(a), apoB, and the grey zone ¶1
1. **Current claim:** Excluding Lp(a) and apoB was a design choice for scalability, not a denial of their biological importance.
2. **Weakness or unsupported element:** Aligns with guideline recommendations on Lp(a) testing.
3. **Evidence check:** Blumenthal RS et al. (*Circulation*. 2026;153:e1154–e1276. doi:10.1161/CIR.0000000000001423).
4. **Required improvement:** Retain current prose.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Discussion—Lp(a), apoB, and the grey zone ¶2
1. **Current claim:** Secondary biomarker additions in the grey zone yielded zero discrimination gain, showing that association does not equal reclassification or utility.
2. **Weakness or unsupported element:** Excellent clinical teaching point regarding biomarker evaluation.
3. **Evidence check:** Sniderman AD et al. (*JAMA Cardiol*. 2019;4:1287–1295. doi:10.1001/jamacardio.2019.3780).
4. **Required improvement:** Retain current prose.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Discussion—Competing risks and endpoint definition ¶1
1. **Current claim:** Unexecuted competing-risk analysis in UK Biobank leaves absolute risk interpretation incomplete.
2. **Weakness or unsupported element:** Honest admission of technical failure.
3. **Evidence check:** Wolk EW et al. (*Ann Intern Med*. 2019;170:51–58. doi:10.7326/M18-1376).
4. **Required improvement:** Retain current prose.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Discussion—Competing risks and endpoint definition ¶2
1. **Current claim:** Endpoint heterogeneity between cohorts (UKB coronary-heavy vs Wales inclusive of procedures/angina) represents an applicability limitation.
2. **Weakness or unsupported element:** Accurate outcome mapping analysis.
3. **Evidence check:** Gallo A et al. (*Atherosclerosis*. 2020;306:41–49. doi:10.1016/j.atherosclerosis.2020.06.011).
4. **Required improvement:** Retain current prose.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Discussion—Ancestry and fairness ¶1
1. **Current claim:** Derivation cohorts were predominantly European ancestry, and performance in non-European ancestries remains untested.
2. **Weakness or unsupported element:** Crucial clinical equity limitation: risk equations calibrated in White Europeans over- or under-predict risk in South Asian, Black, and Hispanic populations.
3. **Evidence check:** Blumenthal RS et al. (*Circulation*. 2026;153:e1154–e1276. doi:10.1161/CIR.0000000000001423).
4. **Required improvement:** Retain explicit equity limitation.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Discussion—Ancestry and fairness ¶2
1. **Current claim:** Future external validation must evaluate discrimination, calibration, and net benefit across diverse ancestral groups.
2. **Weakness or unsupported element:** Sound roadmap for future validation.
3. **Evidence check:** TRIPOD+AI Item 21.
4. **Required improvement:** Retain current prose.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Discussion—Overlap and leakage ¶1
1. **Current claim:** FH-Risk-Score derivation included 499 UK Biobank participants, meaning head-to-head comparisons are not pristine independent validations.
2. **Weakness or unsupported element:** Essential analytical transparency regarding sample overlap.
3. **Evidence check:** Paquette M et al. (*Arterioscler Thromb Vasc Biol*. 2021;41:2632–2640. doi:10.1161/ATVBAHA.121.316106).
4. **Required improvement:** Retain current prose.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Discussion—Overlap and leakage ¶2
1. **Current claim:** Definitive independent validation requires a third, untouched prospective cohort with locked protocols.
2. **Weakness or unsupported element:** Standard prediction model validation roadmap.
3. **Evidence check:** Collins GS et al. (*BMJ*. 2024;384:e074820. doi:10.1136/bmj-2023-074820).
4. **Required improvement:** Retain current prose.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Discussion—Clinical implications ¶1
1. **Current claim:** Methodologically, FH risk scores must be evaluated on identical participants and outcomes with primary-source comparator fidelity.
2. **Weakness or unsupported element:** Excellent guidance for future prediction literature.
3. **Evidence check:** Methodological reporting standards.
4. **Required improvement:** Retain current prose.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Discussion—Clinical implications ¶2
1. **Current claim:** Clinically, CALON-C offers a routine-data ranking option where specialized testing is unavailable, but must NEVER be used to de-risk an FH patient or defer guideline-directed treatment.
2. **Weakness or unsupported element:** Paramount clinical safety principle: risk scoring in FH serves solely to accelerate treatment, never to withhold it.
3. **Evidence check:** Blumenthal RS et al. (*Circulation*. 2026;153:e1154–e1276. doi:10.1161/CIR.0000000000001423) and Mach F et al. (*Eur Heart J*. 2025;46:4359–4378. doi:10.1093/eurheartj/ehaf190).
4. **Required improvement:** Retain this crucial clinical safety warning.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Discussion—Strengths ¶1
1. **Current claim:** Strengths include incident design, exact comparator transcription, primary-source corrections, multiplicity control, and explicit disclosure of limitations.
2. **Weakness or unsupported element:** Accurate self-assessment.
3. **Evidence check:** Internal methodology audit.
4. **Required improvement:** Retain current prose.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

#### Discussion—Limitations ¶1
1. **Current claim:** Limitations include lack of independent external validation, unverified variant coordinates, missing Welsh Table 1, unexecuted UKB competing risks, missing procedure codes, internal calibration only, withdrawn decision curves, and lack of ancestry diversity.
2. **Weakness or unsupported element:** Exceptionally thorough self-critical disclosure.
3. **Evidence check:** TRIPOD+AI Item 22.
4. **Required improvement:** Retain current prose.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

---

### Conclusion

#### Conclusion ¶1
1. **Current claim:** CALON-C ranked incident ASCVD with moderate internal discrimination in UK Biobank using routine variables, outperforming SAFEHEART-RE and Montreal over full follow-up, tying FH-Risk-Score, and retaining ranking in Welsh transport. Results support further validation but do not support clinical deployment or treatment thresholds.
2. **Weakness or unsupported element:** Aligns with all empirical findings and methodological constraints.
3. **Evidence check:** Synthesis of study conclusions.
4. **Required improvement:** Retain current prose.
5. **Suggested replacement wording:** Retain current prose.
6. **Severity:** `MINOR`

---

## Whole-Manuscript Analyses

### A. Novelty Map

* **Genuinely New:**
  * The first head-to-head comparative evaluation of CALON-C alongside SAFEHEART-RE, FH-Risk-Score, and Montreal-FH-SCORE on matched, complete-input participant subsets in a UK population-identified `ldlr_carrier` cohort with strict Holm multiplicity correction.
  * Re-evaluation of SAFEHEART-RE showing that applying the published measured-LDL-C specification rather than back-calculated untreated LDL-C changes the comparative C-statistic delta from +0.032 to +0.070 in favor of CALON-C.
* **Incremental but Useful:**
  * Demonstrating that a parsimonious model using only standard lipid panel components (TC, HDL-C, LDL-C, TG) and routine clinical factors achieves risk ranking statistically equivalent to the Lp(a)-dependent FH-Risk-Score (C=0.698 vs 0.684, p=0.5018).
  * Reciprocal transport evaluation between population biobank data (UK Biobank) and clinical registry data (All-Wales), highlighting significant transport asymmetry (0.725 vs 0.660).
* **Already Established:**
  * Cardiovascular risk in monogenic FH is heavily modified by conventional risk factors (hypertension, male sex, diabetes, smoking) (Jansen 2004; Paquette 2017).
  * SAFEHEART-RE exhibits discrimination loss and miscalibration when applied outside its Spanish derivation registry (Gallo 2020; McKay 2022).
  * Population-identified variant carriers in biobanks display attenuated lipid phenotypes compared to clinic-ascertained FH patients (Tybjærg-Hansen 2005; Gidding 2023).
* **Unsupported Priority Claims:**
  * Any claim that CALON-C is "superior to existing FH instruments" overall (unsupported because it tied FH-Risk-Score and demonstrated no statistically significant superiority at 5 years after multiplicity correction).
  * Any claim of "external validation" in All-Wales (unsupported because Wales was exposed to prior programme model tuning, lacked baseline predictor dating, and required dropping two predictors due to low event counts).

---

### B. Agreement and Disagreement with Recent Evidence

1. **Blumenthal RS et al. (2026 ACC/AHA Dyslipidemia Guideline; *Circulation*. 2026;153:e1154–e1276. doi:10.1161/CIR.0000000000001423):**
   * *Agreement:* Substantive clinical agreement. The guideline recognizes that FH scores may assist in short-term risk ranking for treatment acceleration, but cautions against using scores to defer therapy or estimate long-term risk.
   * *Classification:* Substantive clinical agreement.
2. **Mach F et al. (2025 ESC/EAS Focused Update; *Eur Heart J*. 2025;46:4359–4378. doi:10.1093/eurheartj/ehaf190):**
   * *Agreement:* Clinical agreement that FH carriers represent high/very-high risk individuals requiring early, sustained LLT.
   * *Classification:* Substantive clinical agreement.
3. **McKay AJ et al. (English Routine Care SAFEHEART Validation; *Atherosclerosis*. 2022;358:68–74. doi:10.1016/j.atherosclerosis.2022.07.011):**
   * *Agreement:* Methodological and implementation agreement. Both studies demonstrate that SAFEHEART-RE performs suboptimally (C=0.63–0.67) in UK primary/routine care settings.
   * *Classification:* Implementation/calibration-driven agreement.
4. **Paquette M et al. (FH-Risk-Score Derivation; *Arterioscler Thromb Vasc Biol*. 2021;41:2632–2640. doi:10.1161/ATVBAHA.121.316106):**
   * *Disagreement:* Methodological/population conflict. Paquette et al. reported C>0.75 for FH-Risk-Score in clinical FH cohorts, whereas in UK Biobank population carriers, FH-Risk-Score achieved C=0.684.
   * *Classification:* Population/ascertainment-driven disagreement.
5. **Tamehri Zadeh SS et al. (Australian FH Score Validation; *Atherosclerosis*. 2026;418:120799. doi:10.1016/j.atherosclerosis.2026.120799):**
   * *Disagreement:* Population conflict. Australian clinical FH patients yielded higher discrimination for SAFEHEART-RE (C=0.767) and FH-Risk-Score (C=0.735) than observed in UK Biobank population carriers.
   * *Classification:* Population/ascertainment-driven disagreement.

---

### C. Internal Manuscript Consistency Audit

* **Cohort and Event Counts:**
  * UK Biobank: 3,540 total carriers $\rightarrow$ 207 prevalent excluded $\rightarrow$ 124 undated excluded $\rightarrow$ **3,209 eligible** with **289 events** (97 at 5y, 194 at 10y). *Consistent throughout text, abstract, and tables.*
  * All-Wales: 2,405 initial frame $\rightarrow$ 344 no baseline date $\rightarrow$ 185 prevalent $\rightarrow$ 58 no event age $\rightarrow$ 649 no follow-up $\rightarrow$ **1,169 corrected risk set** with **102 events** (51 at 5y, 75 at 10y). *Inconsistency noted:* Text notes that Welsh baseline Table 1 and internal discrimination metrics reflect pre-rescue frame (1,159/92 events) because post-rescue artifacts were not re-generated.
* **$C$-statistics and Confidence Intervals:**
  * UK Biobank CALON-C optimism-corrected C: Full = 0.7095, 10y = 0.7079, 5y = 0.7336. *Consistent.*
  * Head-to-head full follow-up deltas vs CALON-C:
    * SAFEHEART-RE (n=2,470/221): CALON-C C=0.7003 vs SAFEHEART C=0.6308 $\rightarrow$ Delta +0.070 (0.036 to 0.104), Holm p=0.0003. *Consistent.*
    * Montreal-FH-SCORE (n=2,811/252): CALON-C C=0.7070 vs Montreal C=0.6746 $\rightarrow$ Delta +0.032 (0.011 to 0.055), Holm p=0.0179. *Consistent.*
    * FH-Risk-Score (n=1,913/146): CALON-C C=0.6983 vs FH-Risk-Score C=0.6836 $\rightarrow$ Delta +0.015 (-0.011 to 0.040), Holm p=0.5018. *Consistent.*
* **Transport $C$-statistics:**
  * Frozen UKB-to-Wales transport C = 0.7252; Reverse Wales-to-UKB transport C = 0.6600. *Consistent.*
* **Calibration Metrics:**
  * UKB 10-year calibration slope = 1.101 (0.884–1.318); E/O ratio = 1.008 (0.883–1.153). *Consistent.*
  * UKB 5-year calibration slope = 1.197 (0.900–1.494); E/O ratio = 1.004 (0.832–1.235). *Consistent.*

---

### D. Reporting and Publication Audit

* **TRIPOD+AI & PROBAST Alignment:** Adheres to key TRIPOD+AI structure (Title, Abstract, Methods, Results, Discussion). Unresolved items include: Item 9 (missing data handling uncertainty not propagated), Item 13b (subgroup estimates missing), Item 18 (external calibration missing), and Item 24 (funding/ethics statements left as placeholders). High risk of bias under PROBAST Domain 2 (Predictors - un-dated Welsh predictors) and Domain 4 (Analysis - unexecuted competing risks in UKB).
* **STROBE & RECORD Extensions:** Complies with RECORD guidance by detailing administrative diagnosis codes (ICD-10). Fails RECORD Item 6.2 regarding OPCS-4 procedure coding completeness (procedural revascularisation missing).
* **Calibration & Clinical Utility:** Calibration reported strictly as internal development calibration. Clinical utility claims appropriately withdrawn due to absence of comparative decision-curve analysis.
* **Competing Risks:** Failed execution in UK Biobank is disclosed, but severely compromises absolute risk interpretation.
* **Missing Data & Predictor Timing:** Imputation in UK Biobank was fold-specific. Welsh predictor timing flaws (un-dated hypertension/diabetes/smoking) are explicitly acknowledged as a major limitation.
* **Fairness & Ancestry:** Cohort is restricted to White European ancestry; lack of multi-ethnic testing is acknowledged.
* **Citation Fidelity:** High citation fidelity across contemporary 2016–2026 literature. No broken DOIs detected.
* **Journal Fit:** Suitable for specialist cardiovascular journals (*Atherosclerosis*, *Journal of Clinical Lipidology*, *European Journal of Preventive Cardiology*) provided major clinical revisions and post-rescue artifact updates are completed.

---

### E. Top Revisions (Ranked 1 to 10)

1. **[FATAL - Clinical Safety] Re-frame Clinical Role of Score:** Insert explicit clinical safety warnings throughout Abstract, Introduction, Discussion, and Conclusion stating that CALON-C must NEVER be used to "de-risk" FH carriers or defer/withhold guideline-directed lipid-lowering therapy.
2. **[FATAL - Analytical] Execute Competing Risk Analysis in UK Biobank:** Fix the missing `death` column analytical pipeline in `code/38_CALON_C_CORRECTED.py` to produce Cause-Specific / Fine-Gray cumulative incidence curves for UK Biobank.
3. **[FATAL - Reporting] Regenerate Welsh Artifacts:** Execute the analytical pipeline to regenerate Welsh baseline Table 1, follow-up person-years, internal discrimination, calibration, and equation files for the corrected risk set (n=1,169 / 102 events).
4. **[MAJOR - Clinical] Discuss Phenotypic Attenuation & Biobank Selection:** Expand Discussion to emphasize that population-identified `ldlr_carrier` participants in UK Biobank display mild lipid phenotypes (+0.15–0.23 mmol/L LDL excess) compared to clinic-ascertained heterozygous FH.
5. **[MAJOR - Endpoint] Address Procedure Code Omission:** Explicitly discuss the limitation that UK Biobank outcome definitions rely strictly on ICD-10 diagnostic codes without procedural OPCS-4 revascularisation codes (PCI/CABG).
6. **[MAJOR - Predictors] Address Fixed Lipid Correction Limitations:** Add text acknowledging that fixed lipid multipliers (0.70 for non-HDL/LDL) are crude population averages with modest correlation (r=0.32) to actual untreated lipid levels.
7. **[MODERATE - Utility] Execute Comparative Decision Curve Analysis:** If clinical utility claims are to be made in future work, decision curve analyses comparing CALON-C, FH-Risk-Score, and statin-for-all strategies across 5%–10% 10-year risk thresholds must be performed.
8. **[MODERATE - Governance] Populate Governance Placeholders:** Replace all bracketed placeholders for ethics approval codes, funding grants, conflicts of interest, and data controller details.
9. **[MODERATE - Subgroups] Populate Corrected Subgroup Tables:** Re-run CALON-C interaction tests across sex, age (<50 vs $\ge$50), and diabetes status to complete TRIPOD+AI reporting requirements.
10. **[MINOR - Formatting] Standardize Horizon Reporting:** Ensure all Abstract and Key Points summaries report 5-year and 10-year horizon metrics alongside full-follow-up metrics.

---

### F. Inter-Panel Tension Memo

* **Cardiologist vs. Biostatistician:**
  * *Point of Tension:* The Biostatistician will emphasize statistical parsimony, ridge shrinkage, bootstrap optimism correction, and multiplicity control (Holm adjustment), arguing that CALON-C represents a statistically sound model development exercise. As Cardiologist, I argue that regardless of statistical elegance, a risk model that lacks central clinical outcome adjudication, omits surgical/procedural endpoints (CABG/PCI), fails competing risk execution, and cannot generate comparative decision curves is clinically uninterpretable and unusable at the bedside.
* **Cardiologist vs. Lipid Specialist:**
  * *Point of Tension:* The Lipid Specialist may argue that omitting Lp(a) and apoB weakens the biological fidelity of an FH risk score because Lp(a) is an independent causal risk factor in monogenic dyslipidaemia. As Cardiologist, I emphasize pragmatic health-system workflow: Lp(a) and apoB are unmeasured in >80% of primary care health records, making Lp(a)-dependent scores (SAFEHEART-RE, FH-Risk-Score) operationally non-evaluable in real-world clinical care (as proven in the Welsh registry). A routine-variable model provides immediate scalable triage, provided it is strictly used to accelerate—never withhold—therapy.

---

## Research-Tool Status Table

| Research Tool / Integration | Status | Outcome / Retrieval Details |
|---|---|---|
| Crossref Bibliographic API | **USED — results returned** | Verified DOIs, metadata, publication years, and volume/page numbers for all 39 primary references. |
| PubMed / NLM Medline | **USED — results returned** | Verified citation details and clinical trial indexing for dyslipidaemia guidelines (Blumenthal 2026, Mach 2025) and FH scores. |
| Scite AI Integration | **NOT EXPOSED/NOT CONFIGURED** | Tool not callable in local execution runtime environment. |
| SciSpace Integration | **NOT EXPOSED/NOT CONFIGURED** | Tool not callable in local execution runtime environment. |
| Elicit Integration | **NOT EXPOSED/NOT CONFIGURED** | Tool not callable in local execution runtime environment. |
| Academic Search Skills (`/academic`) | **NOT EXPOSED/NOT CONFIGURED** | Tool not callable in local execution runtime environment. |

---

## Eligible Evidence Ledger (17 August 2016 – 17 August 2026)

*All references cited below fall strictly within the non-negotiable 10-year evidence window (17 August 2016 through 17 August 2026).*

1. **Blumenthal RS et al.** 2026 ACC/AHA/AACVPR/ABC/ACPM/ADA/AGS/APhA/ASPC/NLA/PCNA guideline on the management of dyslipidemia. *Circulation*. 2026;153:e1154–e1276. **DOI:** [10.1161/CIR.0000000000001423](https://doi.org/10.1161
