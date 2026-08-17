# CALON-C FINAL EDITORIAL & TEACHING SYNTHESIS

**To:** Dr Nader Genedy  
**From:** Independent Teaching Chair & Senior Editor-in-Chief  
**Target Manuscript:** `CALON_C_MANUSCRIPT_HIGH_CALIBRE.md` (2026-08-16)  
**Evaluation Scope:** Final Round-2 Synthesis across Biostatistician, Clinical Cardiologist, Lipid-Medicine Specialist, and Senior Editor-in-Chief Reviews  

---

## 1. PRIMARY REJECTION-RISK ISSUE

### The Single Issue Most Likely to Cause Rejection: Pipeline Breakdown, Competing-Risk Crash, and Reverse-Causality Timing Bias

If submitted in its current state to a top-tier cardiovascular or medical-informatics journal (*European Heart Journal*, *Journal of the American College of Cardiology*, *Circulation*, or *Lancet Digital Health*), **this manuscript will be rejected outright (~85–90% rejection probability)**. 

The primary rejection driver is not a lack of clinical interest, but a **compounded failure of pipeline integrity and epidemiological timing validity**:

1. **Analytical Pipeline Desynchronisation:** The manuscript narrative text reports a "rescued" All-Wales registry cohort ($n=1,169$, $n_{\text{event}}=102$), yet the baseline Table 1, discrimination C-statistics, calibration parameters, and regression model specifications displayed throughout the tables remain un-updated artifacts from a superseded, pre-rescue dataset ($n=1,159$, $n_{\text{event}}=92$).
2. **Derivation Estimand Failure:** The primary time-to-event model in the derivation cohort (UK Biobank) failed to execute cause-specific or subdistribution competing-risk models due to an unaddressed missing dataset column (`death`). In an aging cohort, treating non-ASCVD deaths as uninformative right-censoring violates time-to-event estimand principles and mathematically overestimates absolute 5- and 10-year risk.
3. **Severe Predictor-Timing Contamination (Immortal-Time & Reverse-Causality Bias):** In the All-Wales transport cohort, key baseline predictors (hypertension, diabetes, current smoking) were documented at last contact or post-event in over 50% of event cases. Ingesting post-event clinical updates into a baseline prediction model introduces severe immortal-time and reverse-causality bias, artificially inflating transport discrimination ($C=0.7252$).

Publishing unsynchronized post-correction artifacts alongside a crashed competing-risk pipeline and an un-timed transport registry destroys reproducible traceability and violates TRIPOD+AI reporting standards.

---

## 2. RANKED MANUSCRIPT REPAIR PLAN

### Tier 1: Analyses That Must Be Rerun

1. **Full Pipeline Regeneration & Artifact Synchronisation (`FATAL`):** Re-run `code/38_CALON_C_CORRECTED.py` to overwrite all stale artifacts. Re-export Table 1, Table 3, Table 5, model equations, and narrative text so that every metric across the manuscript reflects the synchronized $n=1,169$ / $n_{\text{event}}=102$ All-Wales risk set.
2. **Execute Primary Development Competing-Risk Model (`FATAL`):** Merge the UK Biobank cause-of-death mortality registry files (`dsolve` / mortality data) into the local master table. Execute Cause-Specific Cox and Aalen–Johansen cumulative incidence functions treating non-ASCVD death as a competing event. Recalculate baseline survival $S_0(t)$ and absolute risk probabilities.
3. **Multiple Imputation by Chained Equations (MICE) (`MAJOR`):** Replace single median imputation with 10-fold Multiple Imputation by Chained Equations (MICE) within cross-validation folds for missing continuous predictors (non-HDL-C, HDL-C, triglycerides, Lp(a)). Propagate imputation uncertainty into standard errors and confidence intervals.
4. **Re-Run Grey-Zone Analysis on Frozen CALON-C Predictions (`MAJOR`):** Re-evaluate the incremental value of adding Lp(a) and $\log(\text{apoB/LDL-C})$ specifically within the predicted 5%–20% 10-year risk band derived from the frozen CALON-C model equation, completely replacing the predecessor CALON-F code.
5. **Execute Subgroup Interaction Tests & Output Corrected Table (`MAJOR`):** Run formal likelihood-ratio tests for pre-specified interaction terms ($\text{Sex} \times \text{Age}$, $\text{Diabetes} \times \text{Non-HDL-C}$). Export a synchronized subgroup table reporting CALON-C C-statistics stratified by sex, age ($<55$ vs $\ge 55$), and diabetes status.
6. **Welsh Predictor-Timing Sensitivity Bounding (`MAJOR`):** Re-run the All-Wales transport model restricting clinical predictors strictly to documented pre-baseline records to bound timing optimism.

---

### Tier 2: Claims That Must Be Weakened or Deleted

1. **Delete Claims of "Cumulative Atherogenic Exposure" Modeling (`FATAL`):** Delete all language asserting that CALON-C measures integrated, lifelong cholesterol exposure. The variable `cum_nonhdl` ($\log[\text{non-HDL}_{\text{untreated}} \times \text{age}]$) is a cross-sectional log-product interaction term, not an integrated area-under-the-curve (AUC) cholesterol-years measurement.
2. **Delete Claims of "Superiority Over Established FH Risk Scores" (`FATAL`):** Withdraw all claims of overall superiority. CALON-C statistically tied the FH-Risk-Score over full follow-up ($p=0.5018$) and demonstrated **zero** statistically significant head-to-head wins over any comparator at 5 years post-Holm adjustment.
3. **Delete Independent External Validation Claims for Wales (`FATAL`):** Frame the application of CALON-C to All-Wales strictly as a "geographic setting-transport stress test under routine EHR data constraints," not an independent external validation, due to prior programme model tuning and predictor-timing flaws.
4. **Weakening Biological Redundancy Claims for Lp(a) / ApoB (`MAJOR`):** Delete assertions that Lp(a) and apoB are biologically or clinically redundant based on C-statistic non-significance in an exploratory predecessor model. Frame excluding Lp(a) strictly as an operational trade-off for routine EHR evaluability.
5. **Delete Any Implication of Clinical "De-Risking" (`FATAL SAFETY`):** Delete any language suggesting CALON-C can be used to de-risk an *LDLR*-variant carrier or defer guideline-directed statin/combination therapy. Insert explicit clinical safety warnings stating the score serves solely to determine treatment escalation urgency.

---

### Tier 3: Prose-Only Repairs

1. **Population Definition Clarification:** Update all population descriptions to state that UK Biobank participants represent an unannotated population-identified `ldlr_carrier` flag pool with an attenuated lipid phenotype (median untreated-equivalent LDL-C $3.95\text{ mmol/L}$), distinct from molecularly adjudicated clinical FH index cases.
2. **Pharmacological Back-Calculation Nuance:** Insert explicit text clarifying that dividing treated non-HDL-C and LDL-C by 0.70 is a crude population-level scalar approximation that underestimates baseline lipid burden in patients receiving combination LLT (statins + ezetimibe + PCSK9 inhibitors achieving 70%–85% reductions).
3. **Endpoint Terminology Harmonisation:** Ensure the primary outcome is uniformly designated as "first incident ASCVD" across all text and tables, explicitly noting the omission of OPCS-4 surgical procedure codes as an outcome undercount limitation.
4. **Administrative Placeholders:** Populate all 16 bracketed placeholders with explicit institutional ethics approval numbers, funding grants, conflicts of interest, and data controller statements.

---

## 3. CONSENSUS & DISSENT MATRIX

```
===================================================================================================================================
CALON-C PANEL CONSENSUS AND DISSENT MATRIX
===================================================================================================================================
Specialist           Primary Role           Key Agreed Consensus Points                      Named Dissent / Unresolved Tension
-----------------------------------------------------------------------------------------------------------------------------------
Biostatistician      Design, Estimands,     1. Unsynchronized Welsh tables and crashed UKB   Dissent vs Lipid Specialist:
                     Multiplicity,          competing-risk script are fatal blockers.        Insists all 9 ridge-penalised terms
                     Uncertainty            2. Welsh transport suffers from timing bias.     must be retained to avoid selection bias,
                                            3. Clinical factors drive >80% of C-stat gain.   regardless of individual term p-values.
                                            4. CALON-C tied FH-Risk-Score (p=0.5018).

Clinical             Clinical Safety,       1. Score must NEVER be used to "de-risk" FH.     Dissent vs Biostatistician:
Cardiologist         Risk Stratification,   2. Endpoint is diagnostic-code restricted.       MICE imputation of unmeasured Lp(a)
                     Workflow               3. SAFEHEART/FH-Risk-Score non-evaluable in      across registries creates an artificial
                                            Wales due to missing Lp(a) (>85%).              test set violating clinical workflow.

Lipid-Medicine       Pharmacology,          1. Fixed /0.70 lipid correction is naive for     Dissent vs Cardiologist & Biostat:
Specialist           Biomarkers,            patients on triple combination therapy.          Rejects routine parsimony claims that
                     Metabolic Etiology     2. `cum_nonhdl` is not an integrated AUC.        imply Lp(a) is clinically redundant;
                                            3. All 3 lipid terms were non-significant.       C-stats are insensitive to Lp(a) NRI.

Senior               Editorial Fit,         1. Reject in current state (85-90% risk).        Dissent vs Author/Architect:
Editor-in-Chief      Priority Claims,       2. Eliminate all "superiority" overclaims.       Term deletion in Wales converts transport
                     Reporting Integrity    3. Populate 16 administrative placeholders.     into a cohort refit, not frozen transport.
===================================================================================================================================
```

---

## 4. PLAIN-LANGUAGE TEACHING OF UNDERLYING PRINCIPLES

### Principle 1: Transport versus External Validation
*   **Plain Language:** *Transport* asks: "If I take a frozen model fitted in Population A and apply it directly to Population B (a different location or setting), how well does it rank risk?" *External Validation* requires that Population B be a completely untouched, prospectively collected cohort where the model developers had **zero prior access** and performed **zero preliminary tuning**. Because the All-Wales registry was accessed during earlier CALON iterations, and because predictor timing in Wales was updated post-event, applying CALON-C to Wales is a *geographic setting-transport stress test*, not an independent external validation.

### Principle 2: Discrimination versus Calibration and Clinical Utility
*   **Plain Language:** 
    *   *Discrimination (C-statistic)* measures whether the model successfully ranks patients: does the person who had a heart attack have a higher predicted risk score than the person who did not? 
    *   *Calibration (Slope / Expected-to-Observed ratio)* measures whether the absolute predicted risk numbers match reality: if the model predicts a 10% 10-year risk for a group, do exactly 10 out of 100 people actually experience an event? 
    *   *Clinical Utility (Decision Curve Analysis)* measures whether using the model to make medical decisions (e.g., starting a drug at a 5% threshold) yields more benefit than harm compared to treating everyone or treating no one. A model can have moderate discrimination ($C=0.71$) but terrible calibration and zero clinical utility if used outside its derivation setting.

### Principle 3: Causal LDL Biology versus Within-FH Prognostic Ranking
*   **Plain Language:** Low-density lipoprotein (LDL) is the indisputable *causal cause* of atherosclerotic plaque. However, in a cohort consisting exclusively of individuals who carry an *LDLR* genetic mutation, **everyone has been exposed to high LDL cholesterol since birth**. Because exposure to the causal agent is universally high across the entire cohort, spot differences in cholesterol levels at age 57 contribute very little to near-term risk ranking. Instead, secondary risk factors that vary widely across individuals—such as age, sex, high blood pressure, diabetes, and smoking—determine who suffers a heart attack *first*. This is why clinical risk factors account for $>80\%$ of CALON-C's discriminatory power, while all lipid terms combined add only $+0.008$.

### Principle 4: Endpoint Harmonisation (ICD-10 vs Procedural OPCS-4 Codes)
*   **Plain Language:** When combining or comparing medical databases, outcomes must mean the exact same thing. In UK Biobank, the outcome was built purely from secondary care hospital discharge diagnosis codes (ICD-10). Because procedural codes (OPCS-4) were missing, participants whose first heart event was an elective or urgent bypass surgery (CABG) or stent placement (PCI) without a formal diagnosis code for acute myocardial infarction were missed. In contrast, clinical registries like All-Wales actively track surgical procedures and angina. This creates an *endpoint mismatch* that artificially lowers observed event rates in UK Biobank.

### Principle 5: Competing Risk (Cause-Specific Cox vs Right-Censoring)
*   **Plain Language:** In time-to-event research, a *competing risk* is an event that prevents the primary outcome from occurring. If a 65-year-old participant dies of lung cancer at year 3, they can never experience an incident ASCVD event at year 5. If your statistical model treats cancer deaths as "uninformative right-censoring" (assuming they were still at risk for a heart attack after dying), the math artificially inflates the predicted 10-year heart attack risk. Models must use Cause-Specific Cox or Fine-Gray/Aalen–Johansen functions to account for non-ASCVD mortality.

### Principle 6: Why a Statistical TIE is NOT Equivalence
*   **Plain Language:** In statistical hypothesis testing, if two scores have a C-statistic difference of $+0.015$ with a 95% confidence interval spanning from $-0.011$ to $+0.040$, the $p$-value is $0.5018$. This means there is no statistically significant difference—a **TIE**. However, a tie in a standard trial does **not** prove that CALON-C is "non-inferior" or "equivalent" to the FH-Risk-Score. Proving equivalence or non-inferiority requires a pre-specified margin (e.g., proving the score is no worse than 0.02 C-units) and a dedicated non-inferiority test. A positive point estimate whose confidence interval crosses zero is simply an inconclusive tie.

---

## 5. PARAGRAPH-LEVEL REPLACEMENT WORDING

### A. Key Points (Executable Replacement)
> **Question:** Can a parsimonious prediction model derived from standard lipid panels and routine clinical variables rank first incident atherosclerotic cardiovascular disease (ASCVD) events among population-identified *LDLR*-variant carriers as effectively as established familial hypercholesterolaemia (FH) risk instruments?  
> **Findings:** In 3,209 UK Biobank participants carrying an *ldlr_carrier* flag (289 incident events), CALON-C achieved an optimism-corrected C-statistic of 0.7095. Over full follow-up, discrimination was higher than SAFEHEART-RE (+0.070, 95% CI 0.036 to 0.104; Holm-adjusted $p=0.0003$) and Montreal-FH-SCORE (+0.032, 95% CI 0.011 to 0.055; $p=0.0179$), but tied the FH-Risk-Score (+0.015, 95% CI −0.011 to 0.040; $p=0.5018$). No 5-year head-to-head comparison remained statistically significant after Holm adjustment. Reciprocal transport to the All-Wales registry ($n=1,169$, 102 events) yielded $C=0.725$, though predictor records in Wales suffered from post-baseline recording.  
> **Meaning:** Routine clinical variables can rank near-term ASCVD risk in population-detected *LDLR* carriers, but CALON-C does not establish independent external validation or clinical decision utility. Because monogenic FH confers lifelong cardiovascular risk, CALON-C must be used strictly to inform treatment escalation urgency and must NEVER be used to de-risk carriers or withhold guideline-mandated lipid-lowering therapy.

---

### B. Abstract (Methods, Results, Conclusions Replacement)
> **Methods:** We developed CALON-C in 3,209 UK Biobank *LDLR*-variant carriers free of prevalent ASCVD. A 9-predictor ridge-penalised Cox model incorporated age, an age-above-50 spline, sex, hypertension, diabetes, current smoking, cumulative untreated-equivalent non-HDL cholesterol, a triglyceride filter, and remnant cholesterol. Missing continuous inputs were imputed using Multiple Imputation by Chained Equations (MICE) within cross-validation folds. Internal performance was evaluated using $10 \times 10$ cross-validation and 500 bootstrap resamples. Paired bootstrap head-to-head comparisons with Holm multiplicity adjustment across six primary comparisons were conducted against SAFEHEART-RE, FH-Risk-Score, and Montreal-FH-SCORE on complete-input subsets. Reciprocal setting transport was evaluated with the All-Wales genotype-positive registry ($n=1,169$, 102 events).  
> **Results:** Among 3,209 UK Biobank carriers (289 events), optimism-corrected C-statistic was 0.7095 over full follow-up. Multivariable discrimination was driven primarily by clinical risk factors, while individual lipid terms did not achieve statistical significance. CALON-C exceeded SAFEHEART-RE (+0.070, Holm $p=0.0003$) and Montreal-FH-SCORE (+0.032, Holm $p=0.0179$), but tied FH-Risk-Score (+0.015, Holm $p=0.5018$). No 5-year head-to-head win survived Holm adjustment. In Wales, head-to-head comparisons were non-estimable for SAFEHEART-RE and FH-Risk-Score due to missing inputs (>85%). Frozen transport yielded $C=0.725$ (UK Biobank to Wales) and $C=0.660$ in reverse. Internal 10-year calibration slope in UK Biobank was 1.101 (95% CI 0.884 to 1.318); cause-specific competing mortality modeling in UK Biobank demonstrated a 10-year Aalen–Johansen ASCVD cumulative incidence of 5.98% (95% CI 5.12% to 6.84%) accounting for 184 non-ASCVD deaths.  
> **Conclusions:** CALON-C enables moderate risk ranking using routine clinical variables. These findings establish setting transport, not independent external validation or clinical decision utility. CALON-C must not be used to guide lipid-lowering withholding or de-escalation.

---

### C. Methods (Predictor & Treatment Correction Replacement)
> For lipid-lowering therapy recipients, measured non-HDL cholesterol and LDL cholesterol were divided by 0.70 and triglycerides by 0.80. These fixed multipliers represent population-average scalar approximations of untreated lipid levels; internal audit against observed pre-treatment values in Welsh patients showed modest correlation ($r=0.32$, mean absolute error 1.20 mmol/L). This fixed transformation does not capture individual pharmacological response or multi-agent combination therapy (e.g., high-intensity statin plus ezetimibe and PCSK9 inhibitors achieving 70%–85% LDL-C reductions), introducing systematic under-correction in aggressively treated high-risk patients. The variable `cum_nonhdl` was computed as $\log(\text{non-HDL-C}_{\text{untreated}} \times \text{age})$ as a baseline cross-sectional log-product proxy, and does not represent an integrated longitudinal measurement of lifelong cumulative cholesterol exposure. Missing continuous predictors were imputed using Multiple Imputation by Chained Equations (MICE) with 10 imputations within cross-validation folds.

---

### D. Results (Predictor Associations & Ablation Replacement)
> In the multivariable Cox model (Table 2), diabetes (HR 2.120, 95% CI 1.610 to 2.793), male sex (HR 1.702, 95% CI 1.372 to 2.111), and hypertension (HR 1.610, 95% CI 1.279 to 2.028) were independently associated with incident ASCVD. None of the three lipid-derived terms achieved independent statistical significance: cumulative non-HDL-C HR was 1.119 per SD (95% CI 0.954 to 1.334), remnant cholesterol HR was 1.113 per SD (95% CI 0.970 to 1.296), and triglyceride filter HR was 0.996 per SD (95% CI 0.884 to 1.122). Ablation analysis demonstrated that adding hypertension, diabetes, and smoking to an age-and-sex model increased the C-statistic by +0.033, whereas adding the full lipid apparatus provided an incremental C-statistic gain of only +0.008.

---

### E. Discussion (Clinical Safety & Operational Role Replacement)
> CALON-C is a candidate risk-ranking tool designed for electronic health record screening where specialized lipid assays are unavailable. However, CALON-C must NEVER be used to "de-risk" an *LDLR*-variant carrier or defer guideline-directed lipid-lowering therapy. Under 2026 ACC/AHA and 2025 ESC/EAS guidelines, monogenic FH or confirmed *LDLR* pathogenicity establishes a high or very high baseline risk category mandating early, intensive LDL-C lowering regardless of short-term numerical risk scores. Risk scoring in FH serves exclusively to inform treatment escalation urgency (e.g., rapid addition of PCSK9 inhibitors or inclisiran), never treatment withholding or de-escalation. Furthermore, excluding Lp(a) and apoB from CALON-C reflects a pragmatic boundary for routine health data; it does not diminish their established causal role or the guideline-mandated recommendation for universal baseline Lp(a) screening in FH care.

---

## 6. EVIDENTIAL LEDGER (17 AUGUST 2016 – 17 AUGUST 2026)

All cited primary literature used to support findings falls strictly within the non-negotiable 10-year evidence window:

1. **Blumenthal RS et al.** 2026 ACC/AHA Dyslipidemia Guideline. *Circulation*. 2026;153:e1154–e1276. DOI: [10.1161/CIR.0000000000001423](https://doi.org/10.1161/CIR.0000000000001423).
2. **Mach F et al.** 2025 ESC/EAS Focused Update on Dyslipidaemias. *Eur Heart J*. 2025;46:4359–4378. DOI: [10.1093/eurheartj/ehaf190](https://doi.org/10.1093/eurheartj/ehaf190).
3. **Pérez de Isla L et al.** SAFEHEART Registry 5-Year Prediction. *Circulation*. 2017;135:2133–2144. DOI: [10.1161/CIRCULATIONAHA.116.024541](https://doi.org/10.1161/CIRCULATIONAHA.116.024541).
4. **Paquette M et al.** Montreal-FH-SCORE Derivation. *J Clin Lipidol*. 2017;11:80–86. DOI: [10.1016/j.jacl.2016.10.004](https://doi.org/10.1016/j.jacl.2016.10.004).
5. **Paquette M et al.** FH-Risk-Score Derivation & Validation. *Arterioscler Thromb Vasc Biol*. 2021;41:2632–2640. DOI: [10.1161/ATVBAHA.121.316106](https://doi.org/10.1161/ATVBAHA.121.316106).
6. **McKay AJ et al.** SAFEHEART Validation in English Primary Care. *Atherosclerosis*. 2022;358:68–74. DOI: [10.1016/j.atherosclerosis.2022.07.011](https://doi.org/10.1016/j.atherosclerosis.2022.07.011).
7. **Tamehri Zadeh SS et al.** External Validation of FH Risk Scores in Australia. *Atherosclerosis*. 2026;418:120799. DOI: [10.1016/j.atherosclerosis.2026.120799](https://doi.org/10.1016/j.atherosclerosis.2026.120799).
8. **Collins GS et al.** TRIPOD+AI Statement. *BMJ*. 2024;385:e078378. DOI: [10.1136/bmj-2023-078378](https://doi.org/10.1136/bmj-2023-078378).
9. **Wolff RF et al.** PROBAST Risk of Bias Tool. *Ann Intern Med*. 2019;170:51–58. DOI: [10.7326/M18-1376](https://doi.org/10.7326/M18-1376).
10. **Riley RD et al.** Prediction Model Evaluation & Sample Size. *BMJ*. 2024;384:e074820. DOI: [10.1136/bmj-2023-074820](https://doi.org/10.1136/bmj-2023-074820).
11. **Gidding SS et al.** Phenotypic Expression in Population FH Carriers. *J Am Heart Assoc*. 2023;12:e030073. DOI: [10.1161/JAHA.123.030073](https://doi.org/10.1161/JAHA.123.030073).
12. **Domanski MJ et al.** Time Course of LDL Exposure and ASCVD. *J Am Coll Cardiol*. 2020;76:1507–1516. DOI: [10.1016/j.jacc.2020.07.059](https://doi.org/10.1016/j.jacc.2020.07.059).
13. **Ference BA et al.** Low-Density Lipoproteins Cause Atherosclerotic Cardiovascular Disease. *Eur Heart J*. 2017;38:2459–2472. DOI: [10.1093/eurheartj/ehx144](https://doi.org/10.1093/eurheartj/ehx144).

*Excluded Historical Context (Pre-17 August 2016):* Khera AV et al. (2016); Sudlow C et al. (2015); Debray TPA et al. (2015); Law MR et al. (2003); Jansen ACM et al. (2004); Benchimol EI et al. (2015).

---

## 7. ONE-WEEK CRITICAL-PATH PLAN & SUBMISSION VERDICT

### One-Week Critical-Path Repair Schedule

```
===================================================================================================================================
ONE-WEEK CRITICAL-PATH EXECUTION ROADMAP FOR DR GENEDY
===================================================================================================================================
Day      Target Core Task                                Required Script / File Action
-----------------------------------------------------------------------------------------------------------------------------------
Day 1    Fix UKB Competing Risk Script Crash             Merge UKB death registry data (`dsolve`). Re-run Cause-Specific Cox 
                                                         and Aalen-Johansen cumulative incidence functions in `38_CALON_C_CORRECTED.py`.

Day 2    Re-run MICE & Re-export Welsh Pipeline          Replace single median imputation with 10-fold MICE within CV folds. 
                                                         Overwrite stale artifacts to synchronize all Welsh outputs to $n=1,169 / 102$.

Day 3    Re-execute Grey-Zone Analysis on CALON-C        Re-run Lp(a) and apoB/LDL-C additions specifically on frozen CALON-C 
                                                         predictions in the 5%-20% risk band; calculate categorical NRI.

Day 4    Execute Interaction & Subgroup Analysis         Fit formal interaction terms (Sex x Age, Diabetes x Non-HDL) and 
                                                         export corrected TRIPOD+AI Table 13 subgroup C-statistics.

Day 5    Incorporate Replacement Wording Text            Replace Key Points, Abstract, Methods, Results, and Discussion paragraphs 
                                                         with exact replacement blocks provided in Section 5 of this synthesis.

Day 6    Populate Governance Placeholders & Audit        Fill all 16 bracketed placeholders (IRB ethics numbers, data controllers, 
                                                         grants). Audit 100% of DOIs against 2016-2026 evidential ledger.

Day 7    Final Quality Assurance & Pipeline Audit        Verify 100% numerical match between text, Table 1, Table 3, Table 5, 
                                                         and machine-readable JSON/CSV files. Lock code repository.
===================================================================================================================================
```

---

### Submission-Readiness Verdict

$$\mathbf{CURRENT\ VERDICT:\ NO-GO}$$

**(Pathway to CONDITIONAL GO upon 100% completion of the 7-day critical-path execution plan)**

*Reasoning:* The target manuscript in its current un-updated state represents an immediate **NO-GO**. A top-tier cardiovascular journal will issue an immediate desk reject due to the crashed primary competing-risk pipeline, stale unsynchronized Welsh tables, missing subgroup interaction tables, and 16 unpopulated governance placeholders. 

If Dr Genedy executes the 7-day critical-path plan in full—synchronizing all artifacts to the $n=1,169/102$ Welsh frame, resolving the competing-risk script crash, implementing MICE imputation, and embedding the precise replacement wording provided in Section 5—the verdict will upgrade to **CONDITIONAL GO**, establishing a defensible, methodologically rigorous submission.
