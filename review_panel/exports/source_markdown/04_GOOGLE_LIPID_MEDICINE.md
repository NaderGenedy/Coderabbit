# Rejection-risk summary: Lipid-medicine specialist audit

### Primary editorial verdict
**Major Revision / Reject in current form.** The CALON-C manuscript presents a pragmatic, routine-variable risk ranking approach for individuals carrying an `ldlr_carrier` flag in population biobanks and clinical registries. However, from a lipid-medicine and metabolic cardiovascular disease perspective, the manuscript suffers from fundamental mechanistic, pharmacological, and phenotypic definition flaws that severely compromise its clinical validity and scientific claims.

### Key lipid-medicine vulnerabilities

1. **Phenotypic and genetic misclassification (`ldlr_carrier` flag):**
   The study relies on an unannotated `ldlr_carrier` flag in UK Biobank where `variant_id` was entirely missing across all 501,936 master rows. Monogenic heterozygous familial hypercholesterolaemia (HeFH) is defined by pathogenic or likely pathogenic variants causing severe lifelong non-HDL-C/LDL-C elevation (typically untreated LDL-C $>4.9\text{ mmol/L}$). In this UK Biobank carrier cohort, median untreated-equivalent LDL-C is only $3.95\text{ mmol/L}$ ($\text{IQR } 3.32\text{--}4.68\text{ mmol/L}$). This mild elevation indicates that the cohort includes benign variants, variants of uncertain significance (VUS), or misclassified non-FH individuals, diluting true monogenic FH biology.

2. **Pharmacological invalidity of fixed lipid treatment correction:**
   The model applies a static population-level correction factor, dividing treated non-HDL-C and LDL-C by $0.70$ (assuming a universal $30\%$ reduction) and triglycerides by $0.80$. Contemporary lipid-lowering therapy in FH involves high-intensity statins (typically $50\text{--}55\%$ LDL-C reduction), ezetimibe (additional $15\text{--}20\%$), and PCSK9 inhibitors ($50\text{--}60\%$), achieving combined reductions of $70\text{--}85\%$. Dividing a treated LDL-C of $1.8\text{ mmol/L}$ on triple therapy by $0.70$ yields an estimated pre-treatment LDL-C of only $2.57\text{ mmol/L}$, when true pre-treatment LDL-C was $>6.0\text{ mmol/L}$. This creates severe systematic under-correction in high-risk, aggressively treated patients.

3. **Flawed representation of cumulative atherogenic exposure:**
   The predictor `cum_nonhdl` is specified as $\log(\text{non-HDL-C}_{\text{untreated}} \times \text{age})$. Multiplying a single cross-sectional lipid measurement by current age and taking the natural log is a simple mathematical transform of baseline age and spot lipid concentration. It does not measure integrated lifelong area-under-the-curve cumulative cholesterol exposure (such as cholesterol-years or longitudinal trajectory modeling).

4. **Statistical non-significance of all lipid-derived predictors:**
   In the multivariable Cox model (Table 2), every lipid-derived term fails to achieve independent statistical significance:
   - `cum_nonhdl`: HR $1.119$ per SD ($95\%\text{ CI } 0.954\text{--}1.334$)
   - `tg_filter`: HR $0.996$ per SD ($95\%\text{ CI } 0.884\text{--}1.122$)
   - `untreated-equivalent remnant cholesterol`: HR $1.113$ per SD ($95\%\text{ CI } 0.970\text{--}1.296$)
   
   The incremental discrimination of the entire lipid apparatus beyond basic clinical risk factors (age, sex, hypertension, diabetes, smoking) is only $+0.008$ in C-statistic. Calling CALON-C a "cumulative atherogenic exposure model" overstates its biological mechanism; it functions primarily as a routine clinical risk model.

5. **Inappropriate Lp(a) conversion and clinical misinterpretation:**
   Lp(a) values in UK Biobank ($\text{nmol/L}$) were converted to $\text{mg/dL}$ by dividing by a fixed factor of $2.15$. Because Lp(a) particle mass varies widely with apo(a) isoform size (kringle IV type 2 repeats), fixed molar-to-mass conversions introduce substantial individual-level classification error. Furthermore, dismissing Lp(a) utility based on a non-significant C-statistic change in an exploratory, predecessor-model grey-zone analysis contradicts established guideline recommendations (ACC/AHA 2026, ESC/EAS 2025) to measure Lp(a) for FH risk stratification.

---

# Paragraph-by-paragraph review

## Key points

### Key points ¶1
1. **Current claim:** The question asks whether a parsimonious model built from a standard lipid profile and routine clinical variables can rank first ASCVD events among LDLR-variant carriers as well as established FH scores.
2. **Weakness or unsupported element:** Framed as evaluating "LDLR-variant carriers", but the underlying genetic definition in UK Biobank lacks variant-level annotation and phenotypic severity validation.
3. **Evidence check:** Monogenic FH requires confirmed pathogenic/likely pathogenic variants or severe untreated LDL-C elevation ($>4.9\text{ mmol/L}$) (Gidding et al., *JAHA* 2023, doi:10.1161/JAHA.123.030073).
4. **Required improvement:** Clarify that the question pertains to population-identified `ldlr_carrier` flag holders rather than strictly confirmed clinical FH.
5. **Suggested replacement wording:** "Can a parsimonious model built from standard lipid panels and routine clinical variables rank first atherosclerotic events among individuals with an unannotated population LDLR-carrier flag as effectively as established familial hypercholesterolaemia risk instruments?"
6. **Severity:** `MODERATE`

### Key points ¶2
1. **Current claim:** In 3,209 UK Biobank LDLR-carrier participants, CALON-C showed moderate internal discrimination, outperforming SAFEHEART-RE and Montreal-FH-SCORE over full follow-up after Holm correction, but tying FH-Risk-Score.
2. **Weakness or unsupported element:** Does not mention that all three lipid-derived variables in CALON-C failed to reach multivariable statistical significance in the primary equation.
3. **Evidence check:** Non-HDL-C and remnant cholesterol drive atherogenesis, but predictive independence requires rigorous adjustment for clinical covariates (Sniderman et al., *JAMA Cardiol* 2019, doi:10.1001/jamacardio.2019.3780).
4. **Required improvement:** State explicitly that discrimination was driven predominantly by routine clinical variables rather than lipid terms.
5. **Suggested replacement wording:** "In 3,209 UK Biobank participants carrying an LDLR-carrier flag, CALON-C achieved moderate internal discrimination ($C=0.7095$), outperforming SAFEHEART-RE and Montreal-FH-SCORE on common complete-input subsets over full follow-up, while tying FH-Risk-Score; discrimination was driven primarily by non-lipid clinical risk factors."
6. **Severity:** `MODERATE`

### Key points ¶3
1. **Current claim:** CALON-C supports the feasibility of risk ranking with routine data but does not establish independent external validation, clinical utility, or superiority to every established FH instrument.
2. **Weakness or unsupported element:** Appropriately cautious meaning, fully aligned with lipid guideline boundaries.
3. **Evidence check:** Guideline recommendations highlight that FH risk scores refine short-term risk but cannot replace absolute LDL-C lowering targets (Blumenthal et al., *Circulation* 2026, doi:10.1161/CIR.0000000000001423).
4. **Required improvement:** None; wording is balanced.
5. **Suggested replacement wording:** Retain current text.
6. **Severity:** `MINOR`

---

## Abstract

### Abstract ¶1 (Background)
1. **Current claim:** Contemporary guidelines recognise that FH-specific scores may help estimate short-term ASCVD risk, while general-population equations should not be used for risk estimation in heterozygous FH.
2. **Weakness or unsupported element:** Correctly summarizes guideline consensus; no substantive lipid-medicine defect.
3. **Evidence check:** Confirmed by 2026 ACC/AHA Dyslipidemia Guideline (Blumenthal et al., *Circulation* 2026, doi:10.1161/CIR.0000000000001423) and 2025 ESC/EAS Guidelines (Mach et al., *Eur Heart J* 2025, doi:10.1093/eurheartj/ehaf190).
4. **Required improvement:** None.
5. **Suggested replacement wording:** Retain current text.
6. **Severity:** `MINOR`

### Abstract ¶2 (Methods)
1. **Current claim:** CALON-C was developed using a ridge-penalised Cox model incorporating age, an age spline, sex, clinical risk factors, cumulative untreated-equivalent non-HDL-C, a triglyceride filter, and remnant cholesterol.
2. **Weakness or unsupported element:** The method description describes `cum_nonhdl` as "cumulative untreated-equivalent non-HDL cholesterol", which implies serial integrated measurement rather than a baseline cross-sectional product of $\log(\text{non-HDL-C} \times \text{age})$.
3. **Evidence check:** True cumulative exposure measures long-term cholesterol burden over years (Domanski et al., *JACC* 2020, doi:10.1016/j.jacc.2020.07.059; Ference et al., *Eur Heart J* 2017, doi:10.1093/eurheartj/ehx144).
4. **Required improvement:** Replace "cumulative" with "age-adjusted transformed baseline" to avoid mechanistic overstatement.
5. **Suggested replacement wording:** "The ridge-penalised Cox model incorporated age, an age-above-50 spline, sex, hypertension, diabetes, smoking, a baseline non-HDL-C by age log-product term, a triglyceride filter, and untreated-equivalent remnant cholesterol."
6. **Severity:** `MAJOR`

### Abstract ¶3 (Results)
1. **Current claim:** In 3,209 participants with 289 events, optimism-corrected C was 0.7095, exceeding SAFEHEART-RE and Montreal-FH-SCORE but tying FH-Risk-Score over full follow-up.
2. **Weakness or unsupported element:** Fails to state that in the multivariable model, non-HDL-C, remnant cholesterol, and triglyceride filter hazard ratios all had 95% CIs crossing 1.0.
3. **Evidence check:** Multi-variable predictive contributions must be presented transparently when claiming a model evaluates lipid biology (Sniderman et al., *JAMA Cardiol* 2019, doi:10.1001/jamacardio.2019.3780).
4. **Required improvement:** Note the lack of independent multivariable statistical significance for individual lipid terms in the development equation.
5. **Suggested replacement wording:** "Optimism-corrected C was 0.7095 over full follow-up. CALON-C exceeded SAFEHEART-RE by +0.070 (95% CI 0.036 to 0.104; Holm p=0.0003) and Montreal-FH-SCORE by +0.032 (0.011 to 0.055; p=0.0179), but did not differ from FH-Risk-Score (+0.015, −0.011 to 0.040; p=0.5018). In multivariable modeling, clinical risk factors accounted for most discrimination, whereas individual lipid-derived terms did not achieve statistical significance."
6. **Severity:** `MAJOR`

### Abstract ¶4 (Conclusions)
1. **Current claim:** CALON-C provides moderate risk ranking from routine clinical and standard lipid measurements, showing favourable comparisons with SAFEHEART-RE and Montreal-FH-SCORE while tying FH-Risk-Score.
2. **Weakness or unsupported element:** Appropriately limits conclusions to model development and setting transport.
3. **Evidence check:** Aligns with prediction model validation standards (Collins et al., *BMJ* 2024, doi:10.1136/bmj-2023-074819).
4. **Required improvement:** None.
5. **Suggested replacement wording:** Retain current text.
6. **Severity:** `MINOR`

---

## Introduction

### Introduction ¶1
1. **Current claim:** Familial hypercholesterolaemia is a lifelong exposure disorder where pathogenic variants elevate LDL-C from early life, but cardiovascular expression varies widely across individuals.
2. **Weakness or unsupported element:** Sound mechanistic introduction to FH biology and cumulative exposure.
3. **Evidence check:** Supported by landmark genetic and epidemiological synthesis (Ference et al., *Eur Heart J* 2017, doi:10.1093/eurheartj/ehx144; Mach et al., *Eur Heart J* 2025, doi:10.1093/eurheartj/ehaf190).
4. **Required improvement:** None.
5. **Suggested replacement wording:** Retain current text.
6. **Severity:** `MINOR`

### Introduction ¶2
1. **Current claim:** Established FH risk instruments (SAFEHEART-RE, Montreal-FH-SCORE, FH-Risk-Score) answer related but non-identical questions across different cohort populations and predictors.
2. **Weakness or unsupported element:** Accurately summarizes published FH risk scores and their design heterogeneity.
3. **Evidence check:** Supported by primary instrument publications (Pérez de Isla et al., *Circulation* 2017, doi:10.1161/CIRCULATIONAHA.116.024541; Paquette et al., *ATVB* 2021, doi:10.1161/ATVBAHA.121.316106; Tamehri Zadeh et al., *Atherosclerosis* 2026, doi:10.1016/j.atherosclerosis.2026.120799).
4. **Required improvement:** None.
5. **Suggested replacement wording:** Retain current text.
6. **Severity:** `MINOR`

### Introduction ¶3
1. **Current claim:** Three unresolved issues exist: comparators are rarely evaluated on common participants; specialised measurements (Lp(a), apoB) constrain clinical implementation; and population-detected variant carriers differ from clinic-ascertained FH patients.
2. **Weakness or unsupported element:** Excellent highlighting of ascertainment bias between population carriers and clinic FH.
3. **Evidence check:** Population screening identifies milder FH phenotypes compared to cascade clinic identification (Gidding et al., *JAHA* 2023, doi:10.1161/JAHA.123.030073; Akyea et al., *BJGP Open* 2020, doi:10.3399/bjgpopen20X101114).
4. **Required improvement:** None.
5. **Suggested replacement wording:** Retain current text.
6. **Severity:** `MINOR`

### Introduction ¶4
1. **Current claim:** CALON-C was designed around parsimony and transport, using age, sex, common risk factors, standard lipid panels, and fixed treatment transformations, while omitting Lp(a) and apoB.
2. **Weakness or unsupported element:** Describes fixed lipid treatment transformation as standard practice, but in lipid medicine, dividing treated values by fixed constants ($0.70$ for non-HDL/LDL, $0.80$ for TG) ignores treatment intensity and combination therapy.
3. **Evidence check:** High-intensity statin plus ezetimibe or PCSK9i lowers LDL-C by $70\text{--}85\%$, making a fixed $30\%$ imputation factor ($/0.70$) highly inaccurate for aggressively treated patients (Mach et al., *Eur Heart J* 2025, doi:10.1093/eurheartj/ehaf190).
4. **Required improvement:** Acknowledge that fixed multiplicative lipid transformations represent crude population-level approximations rather than individual pharmacology reconstructions.
5. **Suggested replacement wording:** "CALON-C uses routine clinical variables and standard lipid panels, incorporating simple population-level fixed lipid treatment transformations while intentionally omitting Lp(a) and apoB to assess global routine-data feasibility."
6. **Severity:** `MODERATE`

### Introduction ¶5
1. **Current claim:** The study aimed to develop and internally evaluate CALON-C in UK Biobank LDLR-variant carriers, apply published comparators head-to-head on common evaluable subsets, and assess reciprocal transport with the All-Wales registry.
2. **Weakness or unsupported element:** Appropriately states study objectives and explicit methodological boundaries.
3. **Evidence check:** TRIPOD+AI prediction protocol alignment (Collins et al., *BMJ* 2024, doi:10.1136/bmj-2023-074819).
4. **Required improvement:** None.
5. **Suggested replacement wording:** Retain current text.
6. **Severity:** `MINOR`

---

## Methods

### Methods—Study design and reporting framework
1. **Current claim:** Paragraphs 1–2 define a two-cohort prognostic prediction study using UK Biobank and All-Wales registry under TRIPOD+AI, STROBE, and RECORD guidelines.
2. **Weakness or unsupported element:** Standard design description. No lipid-specific errors.
3. **Evidence check:** Collins et al., *BMJ* 2024 (doi:10.1136/bmj-2023-074819).
4. **Required improvement:** None.
5. **Suggested replacement wording:** Retain current text.
6. **Severity:** `MINOR`

### Methods—Data sources and governance
1. **Current claim:** Paragraphs 1–2 report data governance and note that `variant_id` was empty in all 501,936 local master table rows, restricting the population definition to an `ldlr_carrier` flag.
2. **Weakness or unsupported element:** Critical lipid-medicine vulnerability: an unannotated `ldlr_carrier` flag without variant coordinates prevents verification of pathogenic/likely pathogenic status versus benign variants or sequencing artifacts.
3. **Evidence check:** Monogenic hypercholesterolaemia clinical spectrum varies widely; genetic adjudication is required to distinguish true HeFH from polygenic hypercholesterolaemia or non-pathogenic variants (Trinder et al., *JAMA Cardiol* 2020, doi:10.1001/jamacardio.2019.5954; Khera et al., *JACC* 2016 [Excluded historical context]).
4. **Required improvement:** Highlight this limitation prominently and avoid calling the cohort "genetically confirmed FH".
5. **Suggested replacement wording:** Retain current cautious text; ensure no downstream claims imply confirmed monogenic HeFH pathogenicity.
6. **Severity:** `MAJOR`

### Methods—UK Biobank cohort
1. **Current claim:** Paragraphs 1–2 describe eligibility (3,209 included carriers, 289 incident ASCVD events over full follow-up) and exclusion of prevalent/undated events.
2. **Weakness or unsupported element:** None; cohort flow is clearly documented.
3. **Evidence check:** Standard epidemiologic reporting standards (Wolff et al., *Ann Intern Med* 2019, doi:10.7326/M18-1376).
4. **Required improvement:** None.
5. **Suggested replacement wording:** Retain current text.
6. **Severity:** `MINOR`

### Methods—All-Wales cohort
1. **Current claim:** Paragraphs 1–2 outline the All-Wales genotype-positive cohort (1,169 participants, 102 events in corrected frame) with family clustering.
2. **Weakness or unsupported element:** Notes that hypertension, diabetes, and smoking status were incompletely dated in Wales, often reflecting last contact rather than baseline status.
3. **Evidence check:** Predictor measurement must precede outcome baseline in prognostic modeling (Riley et al., *BMJ* 2024, doi:10.1136/bmj-2024-074820).
4. **Required improvement:** Acknowledge potential reverse causality or misclassification due to post-baseline predictor timing.
5. **Suggested replacement wording:** Retain current text and limitations disclosure.
6. **Severity:** `MODERATE`

### Methods—Outcome terminology
1. **Current claim:** The outcome is defined as first incident ASCVD, avoiding the term MACE due to endpoint heterogeneity across cohorts.
2. **Weakness or unsupported element:** Clinically sound outcome definition.
3. **Evidence check:** ASCVD definition alignment with guideline standards (Blumenthal et al., *Circulation* 2026, doi:10.1161/CIR.0000000000001423).
4. **Required improvement:** None.
5. **Suggested replacement wording:** Retain current text.
6. **Severity:** `MINOR`

### Methods—Predictors and treatment correction
1. **Current claim (¶1–3):** Predictors included age, age spline, sex, hypertension, diabetes, smoking, `cum_nonhdl`, `tg_filter`, and remnant cholesterol; treated non-HDL/LDL were divided by $0.70$ and TG by $0.80$.
2. **Weakness or unsupported element:** Severe lipid pharmacology flaw: fixed $0.70$ division assumes every treated participant experienced exactly $30\%$ LDL-C reduction. High-intensity statin + ezetimibe + PCSK9i combination therapy lowers LDL-C by up to $85\%$. Applying $/0.70$ severely underestimates true untreated lipid levels in the highest-risk, most aggressively treated FH patients. Furthermore, `cum_nonhdl` ($\log[\text{non-HDL}_{\text{untreated}} \times \text{age}]$) is not a true cumulative exposure integral.
3. **Evidence check:** Statin and non-statin response curves demonstrate marked variability across monogenic FH patients receiving combination therapies (Mach et al., *Eur Heart J* 2025, doi:10.1093/eurheartj/ehaf190; Akyea et al., *BJGP Open* 2020, doi:10.3399/bjgpopen20X101114).
4. **Required improvement:** Explicitly state the biological limitations of fixed multiplicative lipid imputations and re-label `cum_nonhdl` as an age-lipid product interaction term.
5. **Suggested replacement wording:** "For treated participants, non-HDL-C and LDL-C were divided by $0.70$ and triglycerides by $0.80$ as a fixed population-level approximation, acknowledging that this does not reflect individual pharmacological response or multi-agent lipid-lowering therapy. The variable `cum_nonhdl` was computed as $\log(\text{non-HDL-C}_{\text{untreated}} \times \text{age})$ as a baseline cross-sectional proxy."
6. **Severity:** `FATAL`

### Methods—Model specification and estimation
1. **Current claim (¶1–2):** A ridge-penalised Cox model (penalty 0.02) was fitted, evaluating internal discrimination via repeated 10-fold cross-validation and 100 bootstrap optimism iterations.
2. **Weakness or unsupported element:** Sound statistical penalisation and cross-validation procedures.
3. **Evidence check:** PROBAST guidelines for internal validation (Wolff et al., *Ann Intern Med* 2019, doi:10.7326/M18-1376).
4. **Required improvement:** None.
5. **Suggested replacement wording:** Retain current text.
6. **Severity:** `MINOR`

### Methods—Comparator implementation
1. **Current claim (¶1–5):** Published SAFEHEART-RE, FH-Risk-Score, and Montreal-FH-SCORE equations were transcribed and applied; Lp(a) in $\text{nmol/L}$ was converted to $\text{mg/dL}$ by dividing by $2.15$.
2. **Weakness or unsupported element:** Dividing Lp(a) in $\text{nmol/L}$ by $2.15$ to derive $\text{mg/dL}$ is biochemically imprecise. Lp(a) mass includes apolipoprotein(a), apolipoprotein B-100, and lipid payload; because apo(a) size varies due to KIV-2 repeats, molar concentration ($\text{nmol/L}$) cannot be linearly converted to mass concentration ($\text{mg/dL}$) with a single fixed divisor across individuals.
3. **Evidence check:** EAS and ACC/AHA guidelines state that molar ($\text{nmol/L}$) and mass ($\text{mg/dL}$) Lp(a) units cannot be directly converted using a single factor due to apo(a) isoform heterogeneity (Mach et al., *Eur Heart J* 2025, doi:10.1093/eurheartj/ehaf190; Blumenthal et al., *Circulation* 2026, doi:10.1161/CIR.0000000000001423).
4. **Required improvement:** Explicitly acknowledge that using $2.15$ as an Lp(a) conversion factor introduces measurement error into comparator implementations requiring Lp(a) in $\text{mg/dL}$.
5. **Suggested replacement wording:** "UK Biobank Lp(a) was recorded in nmol/L; for comparator thresholds requiring mg/dL, it was divided by 2.15 as an approximate conversion factor, recognizing that individual apo(a) isoform variation limits exact molar-to-mass translation."
6. **Severity:** `MAJOR`

### Methods—Head-to-head comparisons and multiplicity
1. **Current claim (¶1–2):** Head-to-head evaluation used paired bootstrap differences on common complete-input subsets, controlling family-wise error across six confirmatory comparisons using Holm correction.
2. **Weakness or unsupported element:** Methodologically rigorous comparator methodology.
3. **Evidence check:** Standard reporting for prediction model comparative evaluation (Collins et al., *BMJ* 2024, doi:10.1136/bmj-2023-074819).
4. **Required improvement:** None.
5. **Suggested replacement wording:** Retain current text.
6. **Severity:** `MINOR`

### Methods—Calibration, model equation, and transport
1. **Current claim (¶1–2):** Raw-unit UK Biobank equation and baseline survival functions were reported, with external calibration claims withdrawn pending independent external evaluation.
2. **Weakness or unsupported element:** Appropriate correction acknowledging internal calibration limitations.
3. **Evidence check:** TRIPOD+AI standards (Collins et al., *BMJ* 2024, doi:10.1136/bmj-2023-074819).
4. **Required improvement:** None.
5. **Suggested replacement wording:** Retain current text.
6. **Severity:** `MINOR`

### Methods—Proportional hazards, competing risk, and sensitivity analyses
1. **Current claim (¶1–2):** Proportional hazards were tested using Schoenfeld residuals; Aalen–Johansen competing risk was performed in Wales but failed to execute in UK Biobank due to missing death column.
2. **Weakness or unsupported element:** Failure to execute competing risk in the development cohort (UK Biobank) leaves absolute risk estimates vulnerable to overestimation in older participants.
3. **Evidence check:** Competing mortality is significant in older cardiovascular cohorts (Wolff et al., *Ann Intern Med* 2019, doi:10.7326/M18-1376).
4. **Required improvement:** Flag the missing UK Biobank competing risk execution as a key computational limitation.
5. **Suggested replacement wording:** Retain text but highlight the limitation in Discussion.
6. **Severity:** `MODERATE`

### Methods—Grey-zone and subgroup analyses
1. **Current claim (¶1–2):** An exploratory predecessor-model grey-zone analysis evaluated adding Lp(a), $\log(\text{apoB/LDL-C})$, or both within a $5\%\text{--}20\%$ 10-year risk band in UK Biobank.
2. **Weakness or unsupported element:** Using an older model specification (CALON-F) to test biomarker increments in a grey zone does not provide valid evidence regarding CALON-C's interaction with Lp(a) or apoB.
3. **Evidence check:** Incremental value of biomarkers must be tested on the final model equation (Collins et al., *BMJ* 2024, doi:10.1136/bmj-2023-074819).
4. **Required improvement:** Explicitly label this as an exploratory, historical secondary analysis that cannot draw definitive conclusions about Lp(a) or apoB utility in CALON-C.
5. **Suggested replacement wording:** "An ancillary exploratory analysis from a predecessor model generation examined adding Lp(a) and apoB/LDL-C within an intermediate predicted risk band; this does not represent evaluation of the final CALON-C equation."
6. **Severity:** `MODERATE`

### Methods—Literature verification
1. **Current claim:** Background and novelty claims were cross-checked against primary PDFs and structured PubMed searches.
2. **Weakness or unsupported element:** Explicitly acknowledges literature search parameters and tool constraints.
3. **Evidence check:** Conforms to search verification standards.
4. **Required improvement:** None.
5. **Suggested replacement wording:** Retain current text.
6. **Severity:** `MINOR`

---

## Results

### Results—Study populations
1. **Current claim (¶1–2):** UK Biobank development population comprised 3,209 carriers (289 events); cases were older, more often male, hypertensive, diabetic, and had higher non-HDL-C ($5.12$ vs $4.70\text{ mmol/L}$). Corrected Welsh risk set had 1,169 carriers and 102 events.
2. **Weakness or unsupported element:** Untreated-equivalent LDL-C in UK Biobank carriers is $3.95\text{ mmol/L}$ overall ($4.16\text{ mmol/L}$ in cases vs $3.94\text{ mmol/L}$ in non-cases). In monogenic HeFH, untreated LDL-C typically averages $>5.5\text{ mmol/L}$ ($>215\text{ mg/dL}$). This low average confirms that the UK Biobank carrier flag captures a phenotypically mild cohort.
3. **Evidence check:** Clinical FH cohorts show substantially higher untreated LDL-C levels (Pérez de Isla et al., *Circulation* 2017, doi:10.1161/CIRCULATIONAHA.116.024541; Paquette et al., *ATVB* 2021, doi:10.1161/ATVBAHA.121.316106).
4. **Required improvement:** Emphasize in the text that median untreated-equivalent LDL-C levels in this carrier cohort are substantially lower than in clinical FH registries.
5. **Suggested replacement wording:** "Untreated-equivalent LDL-C was $3.95\text{ mmol/L}$ (IQR $3.32\text{--}4.68\text{ mmol/L}$), reflecting a phenotypically milder cohort than traditional clinic-ascertained FH registries."
6. **Severity:** `MAJOR`

### Results—Predictor-level associations in UK Biobank
1. **Current claim (¶1–2):** In the multivariable Cox equation, diabetes (HR $2.120$), male sex (HR $1.702$), and hypertension (HR $1.610$) showed the strongest associations; continuous lipid terms (`cum_nonhdl` HR $1.119$, remnant cholesterol HR $1.113$, triglyceride filter HR $0.996$) were not statistically significant.
2. **Weakness or unsupported element:** Critical lipid-medicine finding: every single lipid-derived variable in CALON-C failed to reach independent statistical significance ($p>0.05$, $95\%\text{ CIs}$ crossing $1.0$). Clinical risk factors provided $+0.033$ of the $+0.041$ C-statistic increment over age/sex, while all lipid terms combined added only $+0.008$.
3. **Evidence check:** Standard multivariable reporting requirements (Wolff et al., *Ann Intern Med* 2019, doi:10.7326/M18-1376).
4. **Required improvement:** State clearly that lipid variables provided negligible independent predictive value beyond standard clinical risk factors.
5. **Suggested replacement wording:** "In the multivariable Cox model, traditional clinical risk factors accounted for the vast majority of predictive discrimination, whereas none of the three lipid-derived terms achieved independent statistical significance."
6. **Severity:** `FATAL`

### Results—Internal discrimination
1. **Current claim (¶1–2):** UK Biobank optimism-corrected C-statistic was $0.7095$ over full follow-up, $0.7079$ at 10 years, and $0.7336$ at 5 years. Provisional Welsh optimism-corrected C was $0.7653$.
2. **Weakness or unsupported element:** Welsh post-correction discrimination artifacts were not fully regenerated after rescuing 10 events.
3. **Evidence check:** Results reporting standards (Collins et al., *BMJ* 2024, doi:10.1136/bmj-2023-074819).
4. **Required improvement:** Explicitly flag Welsh discrimination metrics as provisional until post-rescue pipeline re-execution.
5. **Suggested replacement wording:** Retain current text with the included provisional qualification.
6. **Severity:** `MODERATE`

### Results—Head-to-head comparison with published FH instruments
1. **Current claim (¶1–5):** Over full follow-up in UK Biobank, CALON-C outperformed SAFEHEART-RE ($+0.070$, Holm $p=0.0003$) and Montreal-FH-SCORE ($+0.032$, $p=0.0179$), but tied FH-Risk-Score ($+0.015$, $95\%\text{ CI } -0.011\text{ to } 0.040$, $p=0.5018$). No 5-year comparison remained significant after Holm correction.
2. **Weakness or unsupported element:** Accurately reports head-to-head statistics and Holm corrections without overclaiming non-significant 5-year results.
3. **Evidence check:** Paired comparator evaluation standards (Collins et al., *BMJ* 2024, doi:10.1136/bmj-2023-074819).
4. **Required improvement:** None.
5. **Suggested replacement wording:** Retain current text.
6. **Severity:** `MINOR`

### Results—Calibration and model equation
1. **Current claim (¶1–2):** Internal 10-year calibration in UK Biobank showed slope $1.101$ ($95\%\text{ CI } 0.884\text{--}1.318$) and expected:observed ratio $1.008$ ($0.883\text{--}1.153$).
2. **Weakness or unsupported element:** Text explicitly notes this is an internal/apparent calibration assessment, not external validation.
3. **Evidence check:** TRIPOD+AI calibration reporting (Collins et al., *BMJ* 2024, doi:10.1136/bmj-2023-074819).
4. **Required improvement:** None.
5. **Suggested replacement wording:** Retain current text.
6. **Severity:** `MINOR`

### Results—Reciprocal transport
1. **Current claim (¶1–2):** Frozen UK Biobank equation yielded $C=0.7252$ in Wales, while frozen Welsh equation yielded $C=0.6600$ in UK Biobank.
2. **Weakness or unsupported element:** Transport asymmetry reflects substantial differences in cohort selection, age range, clinical severity, and predictor timing between population carriers and registry patients.
3. **Evidence check:** Transportability depends heavily on domain shifts in baseline risk and predictor distributions (Debray et al., *J Clin Epidemiol* 2015 [Excluded historical context]; Riley et al., *BMJ* 2024, doi:10.1136/bmj-2023-074820).
4. **Required improvement:** Emphasize that reciprocal transport asymmetry demonstrates case-mix and ascertainment divergence.
5. **Suggested replacement wording:** Retain current text.
6. **Severity:** `MODERATE`

### Results—Proportional hazards and competing risk
1. **Current claim (¶1–2):** No proportional-hazards violations were found across 16 terms. Welsh 10-year Aalen–Johansen cumulative incidence was $11.97\%$ ($35$ competing deaths). UK Biobank competing risk script failed to execute.
2. **Weakness or unsupported element:** Missing UK Biobank competing risk analysis leaves 10-year risk estimates unadjusted for competing non-CVD mortality in the development set.
3. **Evidence check:** Survival model reporting with competing risks (Wolff et al., *Ann Intern Med* 2019, doi:10.7326/M18-1376).
4. **Required improvement:** Highlight this missing execution as a required pre-publication pipeline fix.
5. **Suggested replacement wording:** Retain current text.
6. **Severity:** `MODERATE`

### Results—Missing data and comparator evaluability
1. **Current claim:** Missingness in UK Biobank was $12.4\%$ for non-HDL-C and $22.5\%$ for Lp(a). In Wales, missingness was severe (BMI $54.5\%$, diabetes $41.6\%$, smoking $26.4\%$), preventing full execution of SAFEHEART-RE and FH-Risk-Score.
2. **Weakness or unsupported element:** Correctly attributes comparator non-evaluability in Wales to real-world registry missingness rather than score inferiority.
3. **Evidence check:** Pragmatic evaluation of risk scores in routinely collected data (McKay et al., *Atherosclerosis* 2022, doi:10.1016/j.atherosclerosis.2022.07.011).
4. **Required improvement:** None.
5. **Suggested replacement wording:** Retain current text.
6. **Severity:** `MINOR`

### Results—Grey-zone analysis
1. **Current claim (¶1–2):** In 1,685 UK Biobank carriers in a $5\%\text{--}20\%$ predicted 10-year risk band, adding Lp(a) ($\Delta C = -0.0038$), $\log(\text{apoB/LDL-C})$ ($\Delta C = +0.0146$), or both ($\Delta C = +0.0118$) produced no statistically significant discrimination gains.
2. **Weakness or unsupported element:** From a lipid-medicine perspective, dismissing Lp(a) or apoB based on C-statistic change in a small subgroup from a predecessor model generation is flawed. C-statistic is notoriously insensitive to incremental biomarker gains; net reclassification improvement (NRI) and decision curve analysis are required.
3. **Evidence check:** Incremental biomarker value requires reclassification metrics and net benefit analysis (Sniderman et al., *JAMA Cardiol* 2019, doi:10.1001/jamacardio.2019.3780; Mach et al., *Eur Heart J* 2025, doi:10.1093/eurheartj/ehaf190).
4. **Required improvement:** State clearly that C-statistic non-significance in an exploratory predecessor model does not disprove the clinical utility of Lp(a) or apoB in FH.
5. **Suggested replacement wording:** "In an exploratory predecessor-model analysis, adding Lp(a) or apoB/LDL-C ratio did not significantly alter C-statistics within an intermediate-risk band, though C-statistic delta alone is insensitive for evaluating biomarker reclassification utility."
6. **Severity:** `MAJOR`

### Results—Subgroups
1. **Current claim:** Corrected CALON-C subgroup analyses and formal interaction tests were unavailable in the final corrected package.
2. **Weakness or unsupported element:** Transparent disclosure of missing subgroup data.
3. **Evidence check:** STROBE item 12b reporting standards.
4. **Required improvement:** None.
5. **Suggested replacement wording:** Retain current text.
6. **Severity:** `MINOR`

---

## Discussion

### Discussion—Principal findings
1. **Current claim (¶1–2):** Summarizes four core findings: moderate internal discrimination; superiority over SAFEHEART-RE and Montreal-FH-SCORE but tie with FH-Risk-Score; retention of rank order in transport; and lack of significant biomarker gain in grey-zone analysis.
2. **Weakness or unsupported element:** Fails to restate that lipid-derived predictors contributed minimally to multivariable discrimination relative to clinical risk factors.
3. **Evidence check:** Synthesis of prediction model findings (Collins et al., *BMJ* 2024, doi:10.1136/bmj-2023-074819).
4. **Required improvement:** Integrate the clinical versus lipid predictor contribution into principal findings.
5. **Suggested replacement wording:** "CALON-C achieved moderate internal discrimination for first ASCVD in UK Biobank carriers, driven primarily by clinical risk factors, and demonstrated parity with FH-Risk-Score while outperforming SAFEHEART-RE and Montreal-FH-SCORE on complete-input subsets."
6. **Severity:** `MODERATE`

### Discussion—What is genuinely new
1. **Current claim (¶1–2):** Identifies novelty as the common-data, comparator-faithful evaluation of CALON-C and published FH instruments on identical participants in a UK population frame, combined with reciprocal registry transport.
2. **Weakness or unsupported element:** Claims novelty in evaluating standard lipid panels without Lp(a), but several scores (e.g., Montreal-FH-SCORE) already exclude Lp(a).
3. **Evidence check:** Paquette et al., *J Clin Lipidol* 2017 (doi:10.1016/j.jacl.2016.10.004).
4. **Required improvement:** Frame novelty strictly around head-to-head common-subset comparison and reciprocal transport.
5. **Suggested replacement wording:** Retain current text with priority claims properly qualified.
6. **Severity:** `MINOR`

### Discussion—Comparison with established FH risk instruments
1. **Current claim (¶1–4):** Discusses why CALON-C outperformed SAFEHEART-RE (which relies on measured treatment-suppressed LDL-C and secondary prevention variables absent in primary prevention) and tied FH-Risk-Score (which was built for primary prevention incident events).
2. **Weakness or unsupported element:** Excellent, mechanistically sound discussion of score architecture differences. SAFEHEART-RE was developed in a secondary/primary clinical cohort where measured LDL-C reflected specialist care, whereas FH-Risk-Score was tailored to incident primary prevention.
3. **Evidence check:** Aligns with primary score derivation designs (Pérez de Isla et al., *Circulation* 2017, doi:10.1161/CIRCULATIONAHA.116.024541; Paquette et al., *ATVB* 2021, doi:10.1161/ATVBAHA.121.316106).
4. **Required improvement:** None.
5. **Suggested replacement wording:** Retain current text.
6. **Severity:** `MINOR`

### Discussion—Routine-panel parsimony and global scalability
1. **Current claim (¶1–2):** Argues that relying on standard lipid panels enables global scalability in health systems where Lp(a) and apoB are not routinely measured.
2. **Weakness or unsupported element:** While routine panel availability is an operational advantage, framing it as superior ignores guideline recommendations (ACC/AHA 2026, ESC/EAS 2025) advocating universal baseline Lp(a) measurement to identify high-risk individuals.
3. **Evidence check:** Guidelines recommend measuring Lp(a) at least once in every adult's lifetime, especially in FH (Blumenthal et al., *Circulation* 2026, doi:10.1161/CIR.0000000000001423; Mach et al., *Eur Heart J* 2025, doi:10.1093/eurheartj/ehaf190).
4. **Required improvement:** Balance the scalability argument by stating that routine-panel modeling does not replace the clinical indication for universal Lp(a) testing in FH.
5. **Suggested replacement wording:** "Standard-panel parsimony enhances model implementation in resource-constrained environments, though this practical trade-off does not lessen the clinical mandate for baseline Lp(a) testing in FH care."
6. **Severity:** `MODERATE`

### Discussion—Why the lipid terms did not dominate
1. **Current claim (¶1–2):** Explains that weak multivariable lipid associations do not refute the causal centrality of LDL-C, but reflect restricted range, treatment suppression, and age acting as an exposure proxy in an FH-selected cohort.
2. **Weakness or unsupported element:** Outstanding, highly accurate lipid-medicine explanation. Causal risk factor centrality does not equate to multivariable predictive dominance in a pre-selected high-exposure cohort.
3. **Evidence check:** Supported by genetic and epidemiologic lipid principles (Ference et al., *Eur Heart J* 2017, doi:10.1093/eurheartj/ehx144; Domanski et al., *JACC* 2020, doi:10.1016/j.jacc.2020.07.059).
4. **Required improvement:** None.
5. **Suggested replacement wording:** Retain current text.
6. **Severity:** `MINOR`

### Discussion—Ascertainment, selection, and UK Biobank representativeness
1. **Current claim (¶1–3):** Highlights healthy-volunteer selection bias in UK Biobank and notes that population `ldlr_carrier` flag holders exhibit mild phenotype ($+0.15\text{--}0.23\text{ mmol/L}$ median LDL-C excess), preventing direct equivalence with clinic-referred FH.
2. **Weakness or unsupported element:** Critical lipid-medicine insight into population vs clinic FH ascertainment.
3. **Evidence check:** Supported by UK Biobank participation bias literature (Fry et al., *Am J Epidemiol* 2017, doi:10.1093/aje/kwx246; van Alten et al., *Int J Epidemiol* 2024, doi:10.1093/ije/dyae054) and genetic FH screening studies (Gidding et al., *JAHA* 2023, doi:10.1161/JAHA.123.030073).
4. **Required improvement:** None.
5. **Suggested replacement wording:** Retain current text.
6. **Severity:** `MINOR`

### Discussion—Survivor bias and age
1. **Current claim (¶1–2):** Notes survivor bias in adult biobanks and registries, where older carriers represent individuals who survived early fatal events or selection.
2. **Weakness or unsupported element:** Valid epidemiological qualification regarding age splines in FH cohorts.
3. **Evidence check:** Selection and survival bias in observational FH cohorts (Akyea et al., *BJGP Open* 2020, doi:10.3399/bjgpopen20X101114).
4. **Required improvement:** None.
5. **Suggested replacement wording:** Retain current text.
6. **Severity:** `MINOR`

### Discussion—Predictor timing in Wales
1. **Current claim (¶1–2):** Discusses incompletely dated predictors in the All-Wales registry and notes that removing undated predictors reduced C-statistic by $0.030$.
2. **Weakness or unsupported element:** Transparent discussion of data timing limitations in real-world registries.
3. **Evidence check:** RECORD guidelines for routine registry data (Benchimol et al., *PLoS Med* 2015 [Excluded historical context]).
4. **Required improvement:** None.
5. **Suggested replacement wording:** Retain current text.
6. **Severity:** `MINOR`

### Discussion—Calibration drift and directional but non-significant differences
1. **Current claim (¶1–2):** Emphasises that transport C-statistics do not equal absolute risk calibration, and directional non-significant differences must be interpreted as statistical ties.
2. **Weakness or unsupported element:** Methodologically sound prediction modeling principles.
3. **Evidence check:** Riley et al., *BMJ* 2024 (doi:10.1136/bmj-2023-074820).
4. **Required improvement:** None.
5. **Suggested replacement wording:** Retain current text.
6. **Severity:** `MINOR`

### Discussion—Lp(a), apoB, and the grey zone
1. **Current claim (¶1–2):** Discusses excluding Lp(a) and apoB from the core model and notes that predecessor grey-zone analyses showed no significant C-statistic gain.
2. **Weakness or unsupported element:** From a lipidology perspective, relying on C-statistic deltas from an outdated model specification to dismiss Lp(a) and apoB is overstated. Lp(a) is an independent causal risk factor for ASCVD and aortic stenosis in FH.
3. **Evidence check:** Causal role of Lp(a) in FH and ASCVD (Mach et al., *Eur Heart J* 2025, doi:10.1093/eurheartj/ehaf190; Blumenthal et al., *Circulation* 2026, doi:10.1161/CIR.0000000000001423).
4. **Required improvement:** Reiterate that omitting Lp(a) and apoB is a pragmatic choice for routine data models, not proof that these biomarkers lack predictive or therapeutic value.
5. **Suggested replacement wording:** "Excluding Lp(a) and apoB reflects a pragmatic model boundary for routine health data; it does not diminish their biological role or guideline-mandated clinical utility in FH risk management."
6. **Severity:** `MAJOR`

### Discussion—Competing risks and endpoint definition
1. **Current claim (¶1–2):** Discusses competing risk estimation in Wales and endpoint heterogeneity (lack of procedure codes in UK Biobank, inclusion of angina/revascularisation in Wales).
2. **Weakness or unsupported element:** Sound critique of endpoint mismatch across cohorts.
3. **Evidence check:** Standard endpoint harmonisation guidelines (Wolff et al., *Ann Intern Med* 2019, doi:10.7326/M18-1376).
4. **Required improvement:** None.
5. **Suggested replacement wording:** Retain current text.
6. **Severity:** `MINOR`

### Discussion—Ancestry and fairness
1. **Current claim (¶1–2):** Notes that cohorts were predominantly European-ancestry and calls for multi-ancestry validation before clinical use.
2. **Weakness or unsupported element:** Important equity limitation.
3. **Evidence check:** TRIPOD+AI fairness item 13 (Collins et al., *BMJ* 2024, doi:10.1136/bmj-2023-074819).
4. **Required improvement:** None.
5. **Suggested replacement wording:** Retain current text.
6. **Severity:** `MINOR`

### Discussion—Overlap and leakage
1. **Current claim (¶1–2):** Notes potential participant overlap with FH-Risk-Score's UK Biobank derivation subset (499 participants) and acknowledges prior programme exposure to both cohorts.
2. **Weakness or unsupported element:** Rigorous disclosure of potential leakage and cohort overlap.
3. **Evidence check:** Validation standards for clinical prediction models (Riley et al., *BMJ* 2024, doi:10.1136/bmj-2023-074820).
4. **Required improvement:** None.
5. **Suggested replacement wording:** Retain current text.
6. **Severity:** `MINOR`

### Discussion—Clinical implications
1. **Current claim (¶1–2):** States that CALON-C is a candidate routine-data ranking tool that cannot be used to guide treatment escalation or de-risk FH carriers without untouched validation and decision-curve analysis.
2. **Weakness or unsupported element:** Fully aligned with 2026 ACC/AHA and 2025 ESC/EAS dyslipidaemia guidelines.
3. **Evidence check:** Guidelines emphasize that risk scores refine management timing but monogenic FH status requires lifelong lipid lowering regardless of score (Blumenthal et al., *Circulation* 2026, doi:10.1161/CIR.0000000000001423; Mach et al., *Eur Heart J* 2025, doi:10.1093/eurheartj/ehaf190).
4. **Required improvement:** None.
5. **Suggested replacement wording:** Retain current text.
6. **Severity:** `MINOR`

### Discussion—Strengths & Limitations
1. **Current claim (¶1–2):** Outlines methodological strengths (incident design, exact comparator transcription, Holm correction) and major limitations (lack of independent external validation, missing `variant_id`, fixed lipid treatment factor, unexecuted UK Biobank competing risks).
2. **Weakness or unsupported element:** Comprehensive self-critique of study limitations.
3. **Evidence check:** TRIPOD+AI and STROBE guidelines (Collins et al., *BMJ* 2024, doi:10.1136/bmj-2023-074819).
4. **Required improvement:** None.
5. **Suggested replacement wording:** Retain current text.
6. **Severity:** `MINOR`

---

## Conclusion

### Conclusion ¶1
1. **Current claim:** CALON-C ranked first incident ASCVD with moderate internal discrimination among UK Biobank LDLR-carrier participants using routine variables, tying FH-Risk-Score and outperforming SAFEHEART-RE and Montreal-FH-SCORE over full follow-up.
2. **Weakness or unsupported element:** Balanced conclusion reflecting study data without overclaiming external validation or clinical adoption.
3. **Evidence check:** Prediction model reporting standards (Collins et al., *BMJ* 2024, doi:10.1136/bmj-2023-074819).
4. **Required improvement:** None.
5. **Suggested replacement wording:** Retain current text.
6. **Severity:** `MINOR`

---

# Whole-manuscript analyses

## A. Novelty map

- **Genuinely new:**
  - The head-to-head evaluation of CALON-C against SAFEHEART-RE, Montreal-FH-SCORE, and FH-Risk-Score on matched, complete-input subsets within a population-based LDLR-carrier frame using paired bootstrap differences and Holm multiplicity control.
  - Reciprocal transport testing of frozen equations between a population biobank (UK Biobank) and a national clinical genotype registry (All-Wales FH registry).

- **Incremental but useful:**
  - Demonstrating that a parsimonious model using standard lipid panels and basic clinical risk factors can achieve discrimination comparable to complex scores requiring Lp(a) in a primary prevention population setting.
  - Empirical demonstration of SAFEHEART-RE performance shifts when evaluated strictly using measured LDL-C versus back-calculated untreated LDL-C.

- **Already established:**
  - That classical clinical risk factors (age, sex, hypertension, diabetes, smoking) account for the vast majority of multivariable ASCVD risk discrimination in FH and hypercholesterolaemic cohorts (Jansen et al., 2004 [Historical Context]; Paquette et al., 2017).
  - That SAFEHEART-RE exhibits calibration drift and lower discrimination when transported outside its derivation registry into population routine care (McKay et al., *Atherosclerosis* 2022).
  - That population-detected genetic carriers have a milder clinical phenotype and lower average LDL-C than clinic-referred FH index cases (Gidding et al., *JAHA* 2023).

- **Unsupported priority claims:**
  - Claiming that CALON-C represents a "cumulative atherogenic exposure model"—the single cross-sectional log-product term `cum_nonhdl` does not capture integrated longitudinal AUC exposure.
  - Claiming that specialized lipid biomarkers (Lp(a), apoB) have no clinical reclassification value based on C-statistic deltas in an exploratory predecessor model analysis.

- **Closest overlapping work:**
  - **Paquette et al., *ATVB* 2021 (FH-Risk-Score):** Developed an incident 10-year ASCVD score for primary prevention in FH. CALON-C overlaps in targeting incident ASCVD in primary prevention but differs by excluding Lp(a) and evaluating reciprocal registry transport.
  - **Tamehri Zadeh et al., *Atherosclerosis* 2026:** Evaluated SAFEHEART-RE and FH-Risk-Score in Australian genetically confirmed FH patients ($C=0.767$ and $0.735$). CALON-C extends this by providing matched head-to-head comparisons on identical complete-input subsets.

---

## B. Agreement and disagreement with recent evidence

1. **2026 ACC/AHA Dyslipidemia Guideline (Blumenthal et al., *Circulation* 2026):**
   - *Agreement:* Agrees that FH risk scores can assist short-term risk estimation, and general population 10-/30-year equations should not be used in FH.
   - *Disagreement (Implementation-driven):* Guidelines recommend universal baseline Lp(a) testing in FH. CALON-C excludes Lp(a) from its core model for routine scalability. This operational choice must not be interpreted as biological or clinical disagreement with guideline-mandated Lp(a) testing.

2. **2025 ESC/EAS Guidelines for Management of Dyslipidaemias (Mach et al., *Eur Heart J* 2025):**
   - *Agreement:* Agrees that lifelong non-HDL-C exposure drives ASCVD in FH and that risk stratification should guide treatment escalation.
   - *Disagreement (Methodological):* ESC/EAS guidelines emphasize absolute LDL-C treatment targets ($<1.4\text{ mmol/L}$ for very high risk). CALON-C provides relative risk ranking ($C$-statistic) but currently lacks transported absolute calibration.

3. **FH-Risk-Score Derivation & Validation (Paquette et al., *ATVB* 2021):**
   - *Agreement:* CALON-C tied FH-Risk-Score in UK Biobank ($C=0.6983$ vs $0.6836$, $\Delta C = +0.015$, $95\%\text{ CI } -0.011\text{ to } 0.040$), supporting the finding that primary-prevention incident risk in FH is predictable using clinical and lipid variables.
   - *Classification:* Methodological alignment.

4. **SAFEHEART-RE External Validation in English Routine Care (McKay et al., *Atherosclerosis* 2022):**
   - *Agreement:* Confirms that SAFEHEART-RE shows lower discrimination ($C=0.6308$ in UK Biobank complete input) when applied in primary prevention populations without secondary prevention history or specialist-clinic measured LDL-C.
   - *Classification:* Population/ascertainment-driven agreement.

5. **Australian FH Score Validation (Tamehri Zadeh et al., *Atherosclerosis* 2026):**
   - *Agreement:* Confirms that relative score performance rankings vary across clinical settings and cohort ascertainment routes.
   - *Classification:* Population/ascertainment-driven agreement.

---

## C. Internal manuscript consistency audit

- **Participant and Event Counts:**
  - UK Biobank: 3,540 total carriers $\rightarrow$ 207 prevalent ASCVD excluded $\rightarrow$ 124 undated ASCVD excluded $\rightarrow$ **3,209 eligible carriers** with **289 events** (97 at 5y, 194 at 10y). Fully consistent across Abstract, Methods, Results, and Table 3.
  - All-Wales Registry: Corrected frame reports **1,169 participants** and **102 events** (51 at 5y, 75 at 10y) after rescuing 10 events. However, Table 3 and Table 5 still display the pre-rescue frame ($n=1,159$, 92 events). **Internal contradiction between narrative text and Tables 3/5.**

- **Discrimination & Effect Sizes:**
  - Optimism-corrected C-statistic in UK Biobank: $0.7095$ (full follow-up), $0.7079$ (10-year), $0.7336$ (5-year). Consistent across Abstract, Results, and Table 3.
  - Head-to-head differences versus SAFEHEART-RE ($+0.070$), Montreal-FH-SCORE ($+0.032$), and FH-Risk-Score ($+0.015$). Consistent across Abstract, Results, Figure 2, and Table 4.

- **Equations & Baseline Hazard:**
  - Equation baseline survival in Table 2: $S_0(5\text{y}) = 0.975645$, $S_0(10\text{y}) = 0.949962$, centered at $-4.217739$. Worked examples in narrative yield $0.78\%$ / $1.62\%$ (low risk) and $15.99\%$ / $30.42\%$ (high risk). Mathematically consistent.

- **Missing Data and Imputation:**
  - Non-HDL-C missing in $12.4\%$, Lp(a) missing in $22.5\%$ in UK Biobank Table 1. Text states median fold-wise imputation was applied. Consistent.

---

## D. Reporting and publication audit

- **TRIPOD+AI & PROBAST Alignment:**
  - High adherence for development and head-to-head comparator evaluation. Explicit reporting of optimism correction, Holm multiplicity control, and raw-unit equations.
  - *Deficits:* Unexecuted competing risk analysis in UK Biobank (TRIPOD+AI item 18); missing post-rescue discrimination/calibration outputs for Wales (TRIPOD+AI item 14b); lack of formal decision curve analysis (withdrawn as requested); absence of variant-level annotation (`variant_id` empty) violating RECORD item 1.3.

- **Clinical Utility & Decision Curves:**
  - Decision-curve claims were explicitly withdrawn. The manuscript appropriately treats CALON-C as a risk-ranking instrument rather than a validated clinical decision tool.

- **Competing Risks & Family Clustering:**
  - Family clustering was incorporated in Welsh bootstrap optimism analysis using family IDs. UK Biobank lacked family linkage fields.
  - Competing risk Aalen–Johansen CIF executed in Wales ($6.02\%$ at 5y, $11.97\%$ at 10y) but failed in UK Biobank.

- **Fairness & Reproducibility:**
  - Ancestry-stratified performance is missing (cohort is predominantly White European). Code and master datasets are held under governed access (UKB Application 1002450), but local repository paths alone do not fulfill open-data repository standards.

---

## E. Top revisions

1. **`FATAL` — Correct lipid treatment transformation overreach:** Re-label fixed $0.70$ lipid division as a crude population approximation; explicitly detail in Discussion how high-intensity statin + ezetimibe + PCSK9i combination therapy leads to systematic under-estimation of untreated LDL-C in high-risk patients.
2. **`FATAL` — Re-frame lipid term non-significance:** Explicitly state in Abstract, Results, and Discussion that all three lipid-derived variables failed to achieve independent multivariable statistical significance in CALON-C, with discrimination driven primarily by routine clinical risk factors (age, sex, hypertension, diabetes, smoking).
3. **`MAJOR` — Re-specify `cum_nonhdl` variable terminology:** Replace claims of modeling "cumulative atherogenic exposure" with "baseline age $\times$ non-HDL-C log-product interaction", clarifying that true cumulative exposure requires integrated longitudinal AUC measurement.
4. **`MAJOR` — Fix Welsh table synchronisation:** Re-run analysis pipelines to update Tables 3 and 5 with the corrected Welsh 1,169 participant / 102 event dataset (currently displaying pre-rescue 1,159 / 92 counts).
5. **`MAJOR` — Correct Lp(a) conversion and grey-zone claims:** Qualify the $2.15$ molar-to-mass Lp(a) conversion factor as an approximation; remove assertions that Lp(a) and apoB lack utility based on non-significant C-statistic changes in an exploratory predecessor model.
6. **`MAJOR` — Fix UK Biobank competing risk script:** Execute the missing UK Biobank competing mortality script to provide proper cause-specific and cumulative incidence functions.
7. **`MODERATE` — Address `ldlr_carrier` flag limitations:** Clarify throughout that UK Biobank carriers represent an unannotated `ldlr_carrier` population with mild lipid phenotype ($3.95\text{ mmol/L}$ median untreated LDL-C), not confirmed monogenic HeFH clinic patients.
8. **`MODERATE` — Regenerate corrected subgroup and interaction analyses:** Supply corrected subgroup tables and test formal interaction terms (e.g., sex $\times$ lipids, diabetes $\times$ lipids) or state their absence as an explicit study limitation.
9. **`MODERATE` — Provide missing submission placeholders:** Insert required administrative placeholders (ethics approval numbers, funding, conflicts of interest, data controller details).
10. **`MINOR` — Refine citation window adherence:** Ensure all supporting citations fall strictly within the 17 August 2016 – 17 August 2026 window, placing older foundational references into an "Excluded historical context" section.

---

## F. Inter-panel tension memo

### Expected Disagreement with Biostatistician
- **Topic:** Retaining or dropping non-significant lipid predictors (`cum_nonhdl`, `tg_filter`, remnant cholesterol) in a penalised multivariable model.
- **Biostatistician position:** The Biostatistician will argue that ridge penalisation ($\lambda=0.02$) shrinks coefficients appropriately, and all pre-specified terms should be retained regardless of individual p-values to preserve model specification and avoid selection bias.
- **Lipid-Medicine Specialist rebuttal:** From a lipid-medicine perspective, publishing a model claimed to capture "cumulative lipid exposure" and "remnant biology" when every single lipid variable has a confidence interval crossing 1.0 (and adds only $+0.008$ to C-statistic) creates a false biological narrative. Clinicians will assume the model's performance reflects lipid mechanics, whereas it is actually functioning as a standard Framingham-like clinical risk score. The text must explicitly clarify this discrepancy.

### Expected Disagreement with Cardiologist
- **Topic:** Operational utility of excluding Lp(a) and apoB to achieve routine-panel parsimony.
- **Cardiologist position:** The Cardiologist may favour excluding Lp(a) and apoB because standard lipid panels are universally available in primary care and emergency settings, enabling immediate clinical risk stratification.
- **Lipid-Medicine Specialist rebuttal:** While routine access is practical, omitting Lp(a) ignores a major causal driver of residual ASCVD risk in FH. Guideline directives (ACC/AHA 2026, ESC/EAS 2025) mandate baseline Lp(a) measurement in FH. Promoting a score that omits Lp(a) risks encouraging clinicians to forego essential lipid subfraction testing in high-risk monogenic patients.

---

# Research-tool status table

| Tool Name | Status | Details / Failure Message |
|---|---|---|
| `/academic` | `NOT EXPOSED/NOT CONFIGURED` | Tool function not callable in this execution environment. |
| Scite AI | `NOT EXPOSED/NOT CONFIGURED` | Integration not configured or callable in current runtime. |
| SciSpace | `NOT EXPOSED/NOT CONFIGURED` | Integration not configured or callable in current runtime. |
| Elicit | `NOT EXPOSED/NOT CONFIGURED` | Integration not configured or callable in current runtime. |
| Native Web Search | `USED — results returned` | Executed targeted literature queries to verify primary publication metadata, DOIs, and 10-year window eligibility (17 Aug 2016 – 17 Aug 2026). |

---

# Eligible evidence ledger (17 August 2016 – 17 August 2026)

| Author & Year | Journal | Population / Design | Main Finding Relevant to Review | Verified DOI / Stable ID |
|---|---|---|---|---|
| **Blumenthal et al. (2026)** | *Circulation* | 2026 ACC/AHA Guideline | Endorses FH risk scores for short-term prediction; requires universal baseline Lp(a) testing. | `10.1161/CIR.0000000000001423` |
| **Mach et al. (2025)** | *Eur Heart J* | 2025 ESC/EAS Guidelines | Emphasizes early, intensive LDL-C lowering to absolute targets; advocates Lp(a) measurement. | `10.1093/eurheartj/ehaf190` |
| **Pérez de Isla et al. (2017)** | *Circulation* | 2,404 Spanish FH patients (SAFEHEART) | SAFEHEART-RE derivation; predicts incident/recurrent events using measured LDL-C and Lp(a). | `10.1161/CIRCULATIONAHA.116.024541` |
| **Paquette et al. (2017)** | *J Clin Lipidol* | Montreal FH Cohort | Montreal-FH-SCORE derivation against prevalent CVD using non-lipid clinical risk factors. | `10.1016/j.jacl.2016.10.004` |
| **Paquette et al. (2021)** | *ATVB* | 3,881 primary prevention FH patients | FH-Risk-Score derivation for 10-year incident ASCVD using untreated LDL-C and Lp(a). | `10.1161/ATVBAHA.121.316106` |
| **Gallo et al. (2020)** | *Atherosclerosis* | 1,020 French FH patients (REFERCHOL) | Validated SAFEHEART-RE and cholesterol-year score in French primary/secondary care. | `10.1016/j.atherosclerosis.2020.06.011` |
| **McKay et al. (2022)** | *Atherosclerosis* | English primary care cohort | Demonstrated calibration drift and moderate discrimination of SAFEHEART-RE in routine care. | `10.1016/j.atherosclerosis.2022.07.011` |
| **Tamehri Zadeh et al. (2026)** | *Atherosclerosis* | 655 Australian genetic FH patients | Validated SAFEHEART-RE ($C=0.767$) and FH-Risk-Score ($C=0.735$) for incident events. | `10.1016/j.atherosclerosis.2026.120799` |
| **Tamehri Zadeh et al. (2025)** | *Can J Cardiol* | Australian FH patients | Evaluated Canadian and French FH risk scores for prevalent cardiovascular disease. | `10.1016/j.cjca.2025.07.042` |
| **Zamora et al. (2025)** | *Eur Heart J Digit Health* | Spanish FH registry | Evaluated machine learning and AI algorithms for gender-specific risk stratification in FH. | `10.1093/ehjdh/ztaf092` |
| **Gallo et al. (2021)** | *JACC Cardiovasc Imaging* | French/Spanish FH cohorts | Demonstrated incremental predictive value of coronary artery calcium scoring over SAFEHEART. | `10.1016/j.jcmg.2021.06.011` |
| **Trinder et al. (2020)** | *JAMA Cardiol* | UK Biobank hypercholesterolaemia | Monogenic FH mutation carriers have higher ASCVD risk than polygenic hypercholesterolaemia. | `10.1001/jamacardio.2019.5954` |
| **Gidding et al. (2023)** | *J Am Heart Assoc* | EHR and genomic screening cohort | Phenotypic yield and mild ASCVD risk profile of population-identified genetic FH carriers. | `10.1161/JAHA.123.030073` |
| **Vallejo-Vaz et al. (2018)** | *Atherosclerosis* | EAS FH Studies Collaboration | Global survey of FH identification, treatment gaps, and cardiovascular risk variations. | `10.1016/j.atherosclerosis.2018.08.08.051` |
| **Fry et al. (2017)** | *Am J Epidemiol* | UK Biobank vs general population | Characterized healthy volunteer selection bias in UK Biobank baseline characteristics. | `10.1093/aje/kwx246` |
| **van Alten et al. (2024)** | *Int J Epidemiol* | UK Biobank participation bias | Reweighting analyses showing volunteer selection bias alters hazard ratio estimates. | `10.1093/ije/dyae054` |
| **Schoeler et al. (2023)** | *Nat Hum Behav* | UK Biobank genetic participation | Participation bias distorts phenotypic and genetic associations in UK Biobank analyses. | `10.1038/s41562-023-01579-9` |
| **Domanski et al. (2020)** | *J Am Coll Cardiol* | Cohort pooling project | Quantified time-course of LDL-C exposure and cumulative area-under-curve risk. | `10.1016/j.jacc.2020.07.059` |
| **Ference et al. (2017)** | *Eur Heart J* | EAS Consensus Statement | Mendelian randomization and prospective proof that LDL causes cumulative ASCVD burden. | `10.1093/eurheartj/ehx144` |
| **Collins et al. (2024)** | *BMJ* | TRIPOD+AI Statement | Standard reporting guidelines for clinical prediction models using ML and Cox regression. | `10.1010/bmj-2023-078378` |
| **Wolff et al. (2019)** | *Ann Intern Med* | PROBAST Tool | Risk of bias and applicability assessment standards for prediction model studies. | `10.7326/M18-1376` |
| **Riley et al. (2024)** | *BMJ* | Prediction model evaluation series | Methodology for external validation, sample size calculation, and transportability. | `10.1136/bmj-2023-074820` |
| **Sniderman et al. (2019)** | *JAMA Cardiol* | Narrative review | Biology of apolipoprotein B particles and discordance analysis vs LDL-C/non-HDL-C. | `10.1001/jamacardio.2019.3780` |
| **Boot et al. (2019)** | *Clin Chem* | Diagnostic cohort study | Evaluated non-HDL-C to apoB ratio for identifying remnant-rich dysbetalipoproteinaemia. | `10.1373/clinchem.2018.292425` |
| **Garg et al. (2020)** | *J Endocr Soc* | North American FH cohort | Molecular characterization and clinical variability of monogenic FH mutation carriers. | `10.1210/jendso/bvz015` |
| **Akyea et al. (2020)** | *BJGP Open* | Primary care FH cohort (FAMCAT) | Validated familial hypercholesterolaemia identification algorithms in routine primary care. | `10.3399/bjgpopen20X101114` |

### Excluded historical context note (pre-17 August 2016)
The following references in the source manuscript predated the 17 August 2016 evidence window and were excluded as formal supporting evidence:
- **Khera et al. (2016)** (*JACC*, June 2016, doi:10.1016/j.jacc.2016.03.520) — Monogenic vs polygenic FH diagnostic yield.
- **Tybjærg-Hansen et al. (2005)** (*ATVB*, 2005, doi:10.1161/01.ATV.0000149380.94984.F0) — Background population impact on LDLR mutation phenotype.
- **Sudlow et al. (2015)** (*PLoS Med*, 2015, doi:10.1371/journal.pmed.1001779) — UK Biobank prospective resource design.
- **Debray et al. (2015)** (*J Clin Epidemiol*, 2015, doi:10.1016/j.jclinepi.2014.06.018) — Framework for prediction model transportability.
- **Law et al. (2003)** (*BMJ*, 2003, doi:10.1136/bmj.326.7404.1423) — Statin LDL-C reduction meta-analysis.
- **Karlson et al. (2016)** (*Eur J Prev Cardiol*, May 2016, doi:10.1177/2047487315598710) — VOYAGER statin dose-response analysis.
- **Jansen et al. (2004)** (*J Intern Med*, 2004, doi:10.1111/j.1365-2796.2004.01405.x) — Classical risk factors in FH cohort.
- **Cohen et al. (2006)** (*N Engl J Med*, 2006, doi:10.1056/NEJMoa054013) — PCSK9 loss-of-function sequence variations.
- **Benchimol et al. (2015)** (*PLoS Med*, 2015, doi:10.1371/journal.pmed.1001885) — RECORD statement for routinely collected data.

---

# Claims that must be deleted unless new evidence is produced

1. **Deletion 1:** Any claim or implication that `cum_nonhdl` ($\log[\text{non-HDL-C}_{\text{untreated}} \times \text{age}]$) represents an integrated, longitudinal measurement of lifelong cumulative cholesterol exposure. *Reason:* It is a single cross-sectional product transform.
2. **Deletion 2:** Any claim or title language suggesting that CALON-C's predictive power is driven by its cumulative lipid apparatus. *Reason:* In multivariable modeling, all three lipid terms had $95\%\text{ CIs}$ crossing $1.0$ ($p>0.05$) and added only $+0.008$ to the C-statistic beyond basic clinical risk factors.
3. **Deletion 3:** The claim that dividing treated non-HDL-C and LDL-C by $0.70$ accurately reconstructs individual pre-treatment lipid levels in FH patients. *Reason:* Ignores combination lipid-lowering therapy (statins + ezetimibe + PCSK9i) that achieves $70\text{--}85\%$ reductions, causing massive under-correction in high-risk treated patients.
4. **Deletion 4:** The assertion that Lp(a) and apoB lack predictive utility in FH risk stratification based on non-significant C-statistic changes in an exploratory predecessor model analysis. *Reason:* Predecessor specification, unvalidated grey zone, and C-statistic insensitivity to biomarker reclassification.
5. **Deletion 5:** Any claim that transport to the All-Wales registry constitutes an "independent external validation" of the UK Biobank equation. *Reason:* Prior programme exposure to both datasets, incomplete predictor dating in Wales, and lack of external calibration assessment.
