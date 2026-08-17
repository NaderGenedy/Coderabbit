# CARDIOLOGIST DEBATE ROUND REVIEW

**Reviewer:** Senior Clinical Cardiologist and Cardiovascular Epidemiologist  
**Protocol:** CALON-C Independent Manuscript-Review Protocol (Round 2 Debate)  
**Target Manuscript:** `CALON_C_MANUSCRIPT_HIGH_CALIBRE.md`  

---

## AUDIT OF CROSS-SPECIALIST CLAIMS

Having thoroughly audited the Round-1 positions submitted by the **Biostatistician**, the **Lipid Medicine Specialist**, and the **Senior Editor-in-Chief**, I provide a clinical cross-examination. I will explicitly accept, reject, or qualify key named claims from each specialist before resolving panel disagreements and outlining the clinical consensus.

---

### 1. Response to the Biostatistician

*   **ACCEPT (Unexecuted Competing-Risk Model in UK Biobank):** I fully accept the Biostatistician's claim that the failure to execute cause-specific Cox / Aalen–Johansen competing-risk models in UK Biobank due to a missing dataset column (`death`) is a **fatal methodological defect**. In an aging population-based cohort (median age 57.1 years, followed for over 15 years), non-ASCVD mortality is a non-negligible competing event. Treating non-ASCVD deaths as uninformative right-censoring mathematically overestimates 5- and 10-year absolute ASCVD risk. Absolute risk equations cannot be published without this fix.
*   **ACCEPT (Unsynchronized Post-Rescue Welsh Artifacts):** I accept the claim that presenting text reporting $n=1,169$ / $n_{\text{event}}=102$ alongside tables and model equations derived from the superseded pre-rescue dataset ($n=1,159$ / $n_{\text{event}}=92$) violates reproducible reporting standards. 
*   **ACCEPT (Predictor Timing Contamination in Wales):** I accept the Biostatistician's identification of severe immortal-time and reverse-causality bias in the All-Wales registry, where hypertension, diabetes, and smoking were frequently updated at last contact or post-event. This artificial timing contamination inflated transport discrimination ($C=0.7252$).
*   **QUALIFY (Missing Data Handling & Multiple Imputation):** The Biostatistician demands 10-fold Multiple Imputation by Chained Equations (MICE) across all missing continuous predictors. From a clinical cardiology perspective, I **qualify** this recommendation: while MICE is statistically superior for model fitting within the derivation set, applying MICE to impute missing comparator variables (such as Lp(a) or apoB in real-world primary care registries where missingness exceeds 80–85%) creates an artificial evaluation framework. In clinical practice, if an assay is unordered, the score cannot be calculated. MICE is appropriate for sensitivity testing in derivation, but strict complete-input matching maps real-world clinical workflow evaluability.

---

### 2. Response to the Lipid Medicine Specialist

*   **ACCEPT (Pharmacological Invalidity of Fixed Lipid Multipliers):** I fully accept the Lipid Specialist's claim that dividing treated non-HDL-C and LDL-C by $0.70$ (assuming a static 30% reduction) is pharmacologically naive. Monogenic heterozygous familial hypercholesterolaemia (HeFH) patients in modern practice receive high-intensity statins (50–55% reduction), ezetimibe (additional 15–20%), and PCSK9 inhibitors or inclisiran (additional 50–60%), achieving combined LDL-C reductions of 70% to 85%. Applying a fixed $/0.70$ multiplier to a patient controlled at $1.8\text{ mmol/L}$ on triple therapy yields an estimated pre-treatment LDL-C of only $2.57\text{ mmol/L}$, when their true baseline was $>6.0\text{ mmol/L}$. This creates severe systematic under-estimation of baseline risk in the highest-risk, most aggressively treated patients.
*   **ACCEPT (Misleading "Cumulative Exposure" Terminology):** I accept the claim that `cum_nonhdl` ($\log[\text{non-HDL-C}_{\text{untreated}} \times \text{age}]$) is a cross-sectional baseline product term, not an integrated longitudinal area-under-the-curve (AUC) measure of lifelong cholesterol exposure (cholesterol-years). Calling CALON-C a "cumulative exposure model" is a biological misnomer.
*   **ACCEPT (Non-Significance of Lipid Predictors & Clinical Driver Dominance):** I accept the Lipid Specialist's highlight that all three lipid-derived terms in CALON-C failed to achieve independent statistical significance in the multivariable model ($p > 0.05$, CIs crossing 1.0), and that lipid variables contributed only $+0.008$ to the $C$-statistic beyond classical clinical risk factors (+0.033 gain). CALON-C functions primarily as a routine clinical risk score rather than a lipid-driven model.
*   **QUALIFY (Exclusion of Lp(a) and ApoB vs Clinical Workflow):** The Lipid Specialist argues that excluding Lp(a) and apoB impairs the model's biological fidelity and rejects dismissing them based on $C$-statistic deltas in a predecessor model. I **qualify** this stance: as a cardiologist, I agree that Lp(a) is an independent causal risk factor and mandatory for baseline screening under 2026 ACC/AHA and 2025 ESC guidelines. However, requiring Lp(a) renders risk scores non-evaluable in $>85\%$ of primary care electronic health records (EHRs). CALON-C's routine-variable parsimony is clinically justified *strictly* as a pragmatic triage tool to establish **treatment escalation urgency**, provided it is explicitly forbidden from being used to "de-risk" or defer guideline-directed lipid-lowering therapy.

---

### 3. Response to the Senior Editor-in-Chief

*   **ACCEPT (Editorial Verdict & Rejection Risk):** I fully accept the Editor-in-Chief's assessment of a **High Rejection Risk (~85–90%)** at leading cardiovascular journals (*EHJ*, *JACC*, *Circulation*). The manuscript cannot be accepted in its current form due to execution bugs, pipeline unsynchronization, 16 bracketed administrative placeholders, and missing procedural outcome linkage.
*   **ACCEPT (Outcome Undercount from Missing Procedure Codes):** I accept the Editor's point that because OPCS-4 surgical procedure fields were unpopulated in UK Biobank, elective or urgent revascularisation procedures (PCI and CABG) performed without a concomitant acute myocardial infarction diagnostic code were missed, creating an outcome undercount.
*   **QUALIFY (Interpretation of Welsh Comparator Non-Evaluability):** The Editor-in-Chief views the non-evaluability of SAFEHEART-RE and FH-Risk-Score in Wales (only 1 and 6 evaluable events) as a benchmarking limitation. I **qualify** this interpretation: clinically, this non-evaluability is a primary **implementation finding**. It proves that risk scores requiring mandatory specialized biomarkers fail completely when translated into real-world national health system registries.

---

## RESOLUTION OF FACTUAL AND CLINICAL DISAGREEMENTS

```
====================================================================================
PANEL DISAGREEMENT RESOLUTION MATRIX
====================================================================================
Issue               Specialist Positions             Clinical Cardiology Resolution
------------------------------------------------------------------------------------
1. Primary Outcome  Biostat: Pure time-to-event Cox.  RESOLVED: Label endpoint as 
   Definition       Editor: Outcome undercount from   "Diagnostic-code Incident ASCVD".
                    missing OPCS-4 procedure codes.   Acknowledge omission of OPCS-4 
                    Cardiologist: Endpoint is         procedural revascularisation as an
                    coronary-heavy diagnostic composite. outcome undercount limitation.

2. Predictor Timing Biostat & Editor: Fatal timing    RESOLVED: Welsh cohort cannot be 
   in All-Wales     contamination (immortal-time bias). framed as an "independent validation".
                    Cardiologist: Reflects messy EHR  It must be explicitly re-titled as a
                    realities but inflates C-stat.    "routine-registry transport stress test".

3. Clinical Role    Cardiologist & Lipid Specialist:  RESOLVED: Monogenic FH requires 
   of Score &       High risk of clinical harm if used lifelong lipid lowering. CALON-C must 
   "De-risking"     to "de-risk" carriers.            be framed strictly for TREATMENT 
                    Editor: Requires safety warning.   ESCALATION URGENCY, never for therapy
                                                      withholding or de-escalation.
====================================================================================
```

---

## CONVERGENCE AND DISSENT

### Five Consensus Points

1. **Fatal Pipeline & Execution Blockers Must Be Fixed Before Resubmission:** The panel unanimously agrees that the unexecuted UK Biobank competing-risk model (due to the missing `death` column) and the unsynchronized Welsh artifacts ($n=1,169/102$ text vs $n=1,159/92$ tables) represent fatal pipeline failures that destroy data provenance and require complete automated re-execution.
2. **Absolute Clinical Prohibition on "De-Risking" FH Patients:** The panel unanimously agrees that monogenic *LDLR*-variant carriers represent a state of lifelong atherogenic exposure requiring early, intensive lipid-lowering therapy under 2026 ACC/AHA and 2025 ESC/EAS guidelines. CALON-C must **never** be used to "de-risk" a carrier or defer guideline-directed statin/combination therapy; its clinical utility is strictly confined to identifying candidates for rapid treatment escalation (e.g., adding ezetimibe, PCSK9 inhibitors, inclisiran, or bempedoic acid).
3. **Severe Predictor Timing Contamination in the All-Wales Registry:** The panel agrees that capturing hypertension, diabetes, and smoking status at last contact or post-event in All-Wales introduces immortal-time and reverse-causality bias. Transporting the model to Wales represents an exploratory stress-test under imperfect EHR data, not a pristine external validation.
4. **Dominance of Conventional Clinical Factors Over Lipid Terms:** The panel agrees that multivariable discrimination in CALON-C is driven almost entirely by age, male sex, hypertension, diabetes, and smoking (+0.033 $C$-statistic gain), whereas the three lipid-derived terms failed to achieve independent statistical significance ($p > 0.05$) and contributed only $+0.008$ to the $C$-statistic.
5. **Real-World Implementation Barrier of Complex Biomarker Scores:** The panel agrees that the failure of SAFEHEART-RE and FH-Risk-Score in the All-Wales registry (non-evaluable in $>85\%$ of participants due to missing Lp(a) and BMI) demonstrates a fundamental clinical reality: scores requiring specialized inputs cannot function in routine health system care, justifying the exploration of routine-variable models.

---

### Five Unresolved Disputes

1. **Operational EHR Parsimony vs. Biological Completeness (Lp(a) / ApoB):**
   *   *Cardiologist & Biostatistician:* Routine-variable parsimony is necessary because specialized lipid assays (Lp(a), apoB) are absent in $>80\%$ of primary care records, causing complex scores to fail in real-world health systems.
   *   *Lipid Medicine Specialist:* Excluding Lp(a) and apoB weakens model fidelity and contradicts guideline mandates (2026 ACC/AHA, 2025 ESC) requiring universal baseline Lp(a) testing in FH. C-statistic deltas in an exploratory predecessor model cannot disprove Lp(a)'s causal and reclassification value.
2. **Mathematical Imputation (MICE) vs. Strict Complete-Case Evaluability:**
   *   *Biostatistician:* Missing continuous predictors must be handled via 10-fold Multiple Imputation by Chained Equations (MICE) within cross-validation folds to propagate imputation uncertainty into standard errors and confidence intervals.
   *   *Cardiologist & Editor:* Imputing unmeasured specialized biomarkers (like Lp(a)) via MICE across benchmark comparisons creates an artificial test set that does not reflect real-world clinical workflow, where an unmeasured variable renders a score non-calculable.
3. **Fixed Population Multipliers vs. Individualized Pharmacological Back-Calculation:**
   *   *Lipid Medicine Specialist:* Dividing treated non-HDL-C and LDL-C by $0.70$ is pharmacologically invalid for patients on high-intensity statin + ezetimibe + PCSK9i combination therapy (70–85% reductions), causing severe under-estimation of pre-treatment cholesterol in the highest-risk individuals.
   *   *Biostatistician & Author:* Fixed division factors represent a practical, reproducible population-level approximation necessary when individual treatment intensity, dosage, and adherence are unrecorded in administrative datasets.
4. **Model Classification: "Cumulative Atherogenic Exposure" vs. "Routine Clinical Risk Score":**
   *   *Lipid Specialist & Cardiologist:* Labeling CALON-C a "cumulative atherogenic exposure model" is a biological misnomer because `cum_nonhdl` is simply a baseline cross-sectional log-product transform ($\log[\text{non-HDL}_{\text{untreated}} \times \text{age}]$), not an integrated longitudinal AUC cholesterol-years measurement.
   *   *Author/Model Architect:* The log-product term functions as a pragmatic proxy for the duration of elevated cholesterol exposure in an aging carrier cohort.
5. **Validity of "Reciprocal Transport" Between Biobanks and Clinical Registries:**
   *   *Senior Editor-in-Chief & Biostatistician:* Transport between UK Biobank (healthy volunteer population biobank) and All-Wales (specialist clinical genetics registry) is severely confounded by prior programme exposure, non-symmetric term fitting (9 terms vs 7 terms), and unquantified participant overlap with comparator derivation sets.
   *   *Cardiologist:* Transport testing across these distinct settings provides valuable empirical evidence regarding how risk models behave when moved between population screening frames and specialist clinical registries.

---

### What Dr. Genedy Should Learn from These Disputes

*(Written in Plain Clinical-Research Language for the Author)*

1. **Statistical Elegance Cannot Overcome Pharmacological or Biological Reality:** 
   Applying a simple mathematical rule—such as dividing treated cholesterol by $0.70$ or multiplying baseline non-HDL cholesterol by age—does not magically reconstruct complex human biology. In clinical research, assuming every patient on lipid-lowering therapy experiences a flat 30% reduction severely misrepresents patients taking modern combination therapies (statins, ezetimibe, and PCSK9 inhibitors) who achieve up to 85% reductions. Always ensure your mathematical transformations align with real-world clinical pharmacology.
2. **Never Confuse Statistical Ranking with Clinical Safety:** 
   A high $C$-statistic ($0.7095$) proves that your model can order patients from higher to lower near-term risk within a specific research dataset. It **does not** mean the model is safe for clinical decision-making. In monogenic conditions like familial hypercholesterolaemia, every adult carrier is at high lifetime risk. If a clinician uses your score to "de-risk" a patient and withhold a statin, that patient suffers irreversible arterial damage. Your manuscript must explicitly state that risk scores serve solely to determine **how urgently to escalate treatment**, never to withhold or defer therapy.
3. **Predictive Association Is Not Causal Explanation:** 
   In your multivariable model, all three lipid terms had confidence intervals crossing 1.0 ($p > 0.05$), and adding them to clinical risk factors improved discrimination by only $+0.008$. This does not mean LDL cholesterol is unimportant in FH—LDL is the undisputed causal driver of atherogenesis. Rather, in an older cohort where everyone has high lifetime cholesterol, classical risk factors like age, male sex, hypertension, and diabetes drive who suffers an event *first*. Be transparent: CALON-C functions as a parsimonious clinical risk score, not a mechanistic lipid model.
4. **Data Provenance and Pipeline Integrity Are Non-Negotiable:** 
   Submitting a manuscript where narrative text reports $1,169$ participants and $102$ events while summary tables display older $1,159$ / $92$ counts—and where a primary competing-risk script crashed due to a missing column—guarantees immediate rejection at top journals. Reviewers and editors demand complete, automated data traceability. Every table, figure, and text metric must be generated from a single, fully synchronized, error-free code pipeline before formal submission.
5. **Acknowledge Pragmatic Trade-offs Without Overclaiming:** 
   Excluding Lp(a) and apoB makes CALON-C easy to run in primary care EHRs where specialized tests are rarely ordered. That is a valid **operational trade-off**. However, do not claim that Lp(a) and apoB are clinically useless based on non-significant $C$-statistic changes in a small subgroup from an older predecessor model. Frame parsimony for what it is: a practical compromise that enables low-cost risk triage while accepting a minor trade-off in peak biological precision.

---

## ELIGIBLE EVIDENCE LEDGER (17 AUGUST 2016 – 17 AUGUST 2026)

All cited literature relies strictly on verified primary sources published within the mandatory 10-year evidence window (17 August 2016 – 17 August 2026):

1. **Blumenthal RS, Morris PB, Gaudino M, et al.** 2026 ACC/AHA/AACVPR/ABC/ACPM/ADA/AGS/APhA/ASPC/NLA/PCNA guideline on the management of dyslipidemia. *Circulation*. 2026;153:e1154–e1276. DOI: [10.1161/CIR.0000000000001423](https://doi.org/10.1161/CIR.0000000000001423).
2. **Mach F, Koskinas KC, Roeters van Lennep JE, et al.** 2025 focused update of the 2019 ESC/EAS Guidelines for the management of dyslipidaemias. *Eur Heart J*. 2025;46:4359–4378. DOI: [10.1093/eurheartj/ehaf190](https://doi.org/10.1093/eurheartj/ehaf190).
3. **Pérez de Isla L, Alonso R, Mata N, et al.** Predicting cardiovascular events in familial hypercholesterolemia: the SAFEHEART Registry. *Circulation*. 2017;135:2133–2144. DOI: [10.1161/CIRCULATIONAHA.116.024541](https://doi.org/10.1161/CIRCULATIONAHA.116.024541).
4. **Paquette M, Dufour R, Baass A.** The Montreal-FH-SCORE: a new score to predict cardiovascular events in familial hypercholesterolemia. *J Clin Lipidol*. 2017;11:80–86. DOI: [10.1016/j.jacl.2016.10.004](https://doi.org/10.1016/j.jacl.2016.10.004).
5. **Paquette M, Bernard S, Cariou B, et al.** Familial Hypercholesterolemia-Risk-Score: a new score predicting cardiovascular events and cardiovascular mortality in familial hypercholesterolemia. *Arterioscler Thromb Vasc Biol*. 2021;41:2632–2640. DOI: [10.1161/ATVBAHA.121.316106](https://doi.org/10.1161/ATVBAHA.121.316106).
6. **McKay AJ, Ajufo E, Korakas E, et al.** Performance of the SAFEHEART risk equation in an English primary care cohort. *Atherosclerosis*. 2022;358:68–74. DOI: [10.1016/j.atherosclerosis.2022.07.011](https://doi.org/10.1016/j.atherosclerosis.2022.07.011).
7. **Tamehri Zadeh SS, Boffa MB, Hegele RA, et al.** External validation of familial hypercholesterolaemia risk scores in an Australian clinical cohort. *Atherosclerosis*. 2026;418:120799. DOI: [10.1016/j.atherosclerosis.2026.120799](https://doi.org/10.1016/j.atherosclerosis.2026.120799).
8. **Collins GS, Moons KGM, Dhiman P, et al.** TRIPOD+AI statement: updated guidance for reporting clinical prediction models that use regression or machine learning methods. *BMJ*. 2024;385:e078378. DOI: [10.1136/bmj-2023-078378](https://doi.org/10.1136/bmj-2023-078378).
9. **Wolff RF, Moons KGM, Riley RD, et al.** PROBAST: A Tool to Assess the Risk of Bias and Applicability of Prediction Model Studies. *Ann Intern Med*. 2019;170:51–58. DOI: [10.7326/M18-1376](https://doi.org/10.7326/M18-1376).
10. **Riley RD, Ensor J, Snell KI, et al.** Calculating the sample size required for developing a clinical prediction model. *BMJ*. 2024;384:e074820. DOI: [10.1136/bmj-2023-074820](https://doi.org/10.1136/bmj-2023-074820).
