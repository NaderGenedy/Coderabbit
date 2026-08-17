# DEBATE ROUND: LIPID-MEDICINE SPECIALIST SYNTHESIS

**Reviewer Seat:** LIPID-MEDICINE SPECIALIST  
**Protocol:** CALON-C Four-Specialist Debate & Consensus Protocol (Round 2)  
**Target Manuscript:** `CALON_C_MANUSCRIPT_HIGH_CALIBRE.md` (2026-08-16)  

---

## 1. Cross-Specialist Audit & Named Stance Map

Having audited the independent Round 1 reviews submitted by the **Biostatistician**, the **Cardiologist**, and the **Senior Editor-in-Chief**, I provide a lipid-medicine, metabolic, and pharmacological synthesis. I evaluate how their findings intersect with lipid biology, cumulative atherogenic particle exposure, treatment back-calculation, and guideline-directed dyslipidaemia care.

```
+---------------------------------------------------------------------------------------------------+
| CROSS-SPECIALIST STANCE MATRIX: LIPID-MEDICINE AUDIT                                              |
+---------------------------------------------------------------------------------------------------+
| ISSUE                            | BIOSTATISTICIAN   | CARDIOLOGIST      | EDITOR-IN-CHIEF   | MY STANCE (LIPID MED) |
+----------------------------------+-------------------+-------------------+-------------------+-----------------------+
| Unexecuted UKB Competing Risk    | Fatal Blocker     | Major Defect      | Fatal Blocker     | ACCEPT (Fatal)        |
| Unsynchronized Welsh Artefacts   | Fatal Blocker     | Major Defect      | Fatal Blocker     | ACCEPT (Fatal)        |
| Welsh Predictor Timing Bias      | Fatal Blocker     | Fatal Bias        | Fatal Blocker     | ACCEPT (Fatal)        |
| Clinical "De-Risking" Danger     | Secondary Caveat  | Fatal Safety Risk | Critical Warning  | ACCEPT (Fatal Safety) |
| Non-Significance of Lipid Terms  | Statistical Fact  | Clinical Paradox  | Noted Limitation  | REJECT OVER-CLAIM     |
| Fixed /0.70 Lipid Correction     | Measurement Error | Crude Average     | Pragmatic Multiplier| QUALIFY PHARMACOLOGY |
| Lp(a) Scalar Conversion (/2.15)  | Scalar Approx     | Operational Factor| Operational Assumption| QUALIFY BIOCHEMISTRY|
| Omitting Lp(a)/apoB in Model     | Parsimony Gain    | Operational Pragmatism| EHR Evaluability  | QUALIFY / REJECT TIE  |
+----------------------------------+-------------------+-------------------+-------------------+-----------------------+
```

---

### A. Claims Accepted from Other Specialists

1. **Failure of Primary Estimand Execution (Biostatistician, Cardiologist, Senior Editor-in-Chief):**
   * *Claim:* The failure to execute Cause-Specific Cox / Fine-Gray competing risk models in UK Biobank due to a missing dataset column (`death`) invalidates absolute 5- and 10-year risk probabilities ($S_0(t)$).
   * *Lipid-Medicine Stance:* **ACCEPT.** In an aging cohort (median baseline age 57.1 years, followed for up to 15+ years), non-ASCVD mortality is a competing hazard. Treating non-ASCVD deaths as uninformative right-censoring artificially inflates calculated 10-year absolute ASCVD risk.

2. **Un-synchronized Analytical Artefacts & Un-rescued Welsh Tables (Biostatistician, Senior Editor-in-Chief):**
   * *Claim:* Reporting text metrics based on a rescued All-Wales dataset ($n=1,169$, $n_{\text{event}}=102$) while presenting baseline Table 1, discrimination, calibration, and equation files based on the superseded pre-rescue dataset ($n=1,159$, $n_{\text{event}}=92$) violates reproducible reporting standards.
   * *Lipid-Medicine Stance:* **ACCEPT.** Complete pipeline re-execution is required to synchronize all Welsh tables and model parameters.

3. **Predictor Timing Contamination / Reverse Causality in All-Wales (Biostatistician, Cardiologist, Senior Editor-in-Chief):**
   * *Claim:* Clinical risk factors (hypertension, diabetes, smoking) recorded at last contact or post-event in >50% of Welsh cases introduce immortal-time and reverse-causality bias, inflating apparent transport discrimination ($C=0.7252$).
   * *Lipid-Medicine Stance:* **ACCEPT.** Ingesting clinical diagnoses established *after* a index lipid panel or post-ASCVD event distorts the baseline hazard. The ~0.030 drop in $C$-statistic when restricting to dated predictors quantifies this optimism.

4. **Clinical Danger of "De-Risking" Monogenic FH Patients (Cardiologist, Senior Editor-in-Chief):**
   * *Claim:* Heterozygous familial hypercholesterolaemia (HeFH) represents a lifelong, cumulative exposure state. Standard guidelines (2026 ACC/AHA; 2025 ESC/EAS) classify monogenic FH as high or very high risk by default. A short-term 5- or 10-year risk score must **never** be used to "de-risk" a patient, de-escalate therapy, or defer guideline-directed lipid-lowering therapy (LLT).
   * *Lipid-Medicine Stance:* **ACCEPT.** Short-term risk equations in FH serve solely to determine *treatment escalation urgency* (e.g., immediate triple therapy with high-intensity statin + ezetimibe + PCSK9 inhibitor/inclisiran), never primary treatment withholding.

5. **Phenotypic Attenuation in Biobank Population Carriers vs. Clinical FH (Cardiologist, Senior Editor-in-Chief):**
   * *Claim:* Population-identified `ldlr_carrier` participants in UK Biobank display an attenuated lipid phenotype (median untreated-equivalent LDL-C 3.95 mmol/L; median LDL-C excess over non-carriers only +0.15 to +0.23 mmol/L), differing fundamentally from clinic-referred FH index cases with severe hypercholesterolaemia (untreated LDL-C >4.9 to 5.5 mmol/L).
   * *Lipid-Medicine Stance:* **ACCEPT.** The UK Biobank carrier pool includes low-penetrance variants, missense variants of uncertain significance (VUS), or polygenic phenocopies, diluting true monogenic loss-of-function biology.

---

### B. Claims Rejected from Other Specialists

1. **Rejection of the Biostatistician's Narrative Tolerance for Non-Significant Lipid Terms:**
   * *Biostatistician's Position:* The Biostatistician notes that individual $p$-values are secondary in ridge-penalised prediction models ($\lambda=0.02$) and that all 9 terms should be retained to prevent selection bias.
   * *Lipid-Medicine Rejection:* While statistical shrinkage retains variables in the linear predictor, **I REJECT framing CALON-C as a "cumulative atherogenic exposure" or "remnant cholesterol" model.** In Table 2, every single lipid term fails to achieve multivariable statistical significance:
     - `cum_nonhdl`: HR $1.119$ per SD ($95\%\text{ CI } 0.954\text{--}1.334$, $p>0.05$)
     - `tg_filter`: HR $0.996$ per SD ($95\%\text{ CI } 0.884\text{--}1.122$, $p>0.05$)
     - `untreated remnant cholesterol`: HR $1.113$ per SD ($95\%\text{ CI } 0.970\text{--}1.296$, $p>0.05$)
     Ablation analysis proves that clinical factors (hypertension, diabetes, smoking) account for $+0.033$ of the $+0.041$ C-statistic gain over age/sex, while all three lipid terms combined contribute a negligible $+0.008$. Presenting CALON-C as a novel lipid-mechanistic score creates a false biological narrative; it functions mathematically as a routine clinical risk score in a high-risk population.

2. **Rejection of the Cardiologist's Pragmatic Dismissal of Lp(a) and apoB Utility:**
   * *Cardiologist's Position:* The Cardiologist argues that routine lipid panels are sufficient for primary care triage and that excluding Lp(a) and apoB is an acceptable operational trade-off given that >80% of registry records lack Lp(a).
   * *Lipid-Medicine Rejection:* **I REJECT the implication that Lp(a) or apoB are clinically redundant in FH risk assessment.** Lp(a) is an independent, genetically determined causal driver of residual ASCVD and aortic stenosis in FH (Paquette et al., *ATVB*, 2021; Blumenthal et al., *Circulation*, 2026). The authors' finding that adding Lp(a) yielded a non-significant $C$-statistic change ($\Delta C = -0.0038$) in an exploratory grey-zone analysis reflects the known insensitivity of rank discrimination metrics ($C$-statistic) to independent biomarkers, combined with using an outdated predecessor model (CALON-F). C-statistic insensitivity must not be weaponized to challenge guideline mandates (ACC/AHA 2026; ESC/EAS 2025) for universal baseline Lp(a) screening in FH.

---

### C. Claims Qualified with Lipid-Medicine & Pharmacological Nuance

1. **Qualification of Treatment Back-Calculation Mechanics (Cardiologist & Biostatistician):**
   * *Cardiologist/Biostatistician Stance:* The Cardiologist labels fixed division factors (dividing treated non-HDL/LDL by 0.70 and TG by 0.80) as a "crude population average," citing an internal audit correlation of $r=0.32$ (MAE 1.20 mmol/L).
   * *Lipid-Medicine Qualification:* **This fixed $/0.70$ multiplier is pharmacologically unviable for contemporary FH care.** In monogenic FH, modern LLT is multi-agent:
     - High-intensity statins (atorvastatin 80 mg, rosuvastatin 40 mg) achieve $50\text{--}55\%$ LDL-C reduction.
     - Addition of ezetimibe 10 mg adds $15\text{--}20\%$ (cumulative $65\text{--}70\%$).
     - Addition of a PCSK9 inhibitor (alirocumab, evolocumab) or inclisiran adds $50\text{--}60\%$, yielding overall reductions of $75\text{--}85\%$.
     Dividing a treated LDL-C of $1.8\text{ mmol/L}$ on triple therapy by $0.70$ back-calculates an estimated untreated LDL-C of only $2.57\text{ mmol/L}$—a massive underestimation when the patient's true pre-treatment LDL-C was $>6.0\text{ mmol/L}$. This creates systematic, severe under-correction in the highest-risk, most aggressively treated patients, artificially blunting the observed hazard ratio of untreated non-HDL-C.

2. **Qualification of Scalar Lp(a) Unit Conversion ($\text{nmol/L}$ to $\text{mg/dL}$) (Biostatistician & Senior Editor-in-Chief):**
   * *Biostatistician/Editor-in-Chief Stance:* The conversion of UK Biobank Lp(a) from $\text{nmol/L}$ to $\text{mg/dL}$ via a scalar divisor of $2.15$ is treated as a minor operational approximation for comparator scoring.
   * *Lipid-Medicine Qualification:* **Converting $\text{nmol/L}$ to $\text{mg/dL}$ with a fixed divisor is biochemically invalid.** Lp(a) mass ($\text{mg/dL}$) measures total particle weight (apolipoprotein(a), apoB-100, and lipid core), whereas molarity ($\text{nmol/L}$) measures exact particle number. Because the apolipoprotein(a) size varies wildly across individuals due to kringle IV type 2 (KIV-2) repeat number polymorphisms (ranging from 10 to >50 repeats), a fixed $2.15$ scalar introduces non-linear misclassification. Patients with small apo(a) isoforms are systematically misclassified when applying point thresholds in comparators like the FH-Risk-Score ($\ge 50\text{ mg/dL}$).

3. **Qualification of `cum_nonhdl` Variable Definition (All Specialists):**
   * *Manuscript & Specialist Description:* The variable `cum_nonhdl` is described throughout as "cumulative untreated-equivalent non-HDL cholesterol exposure."
   * *Lipid-Medicine Qualification:* **`cum_nonhdl` is mathematically $\log(\text{non-HDL}_{\text{untreated}} \times \text{age})$, which is an age-lipid product interaction term, not a cumulative exposure integral.** True cumulative exposure (cholesterol-years or area-under-the-curve [AUC]) requires serial longitudinal measurements or validated age-at-treatment-initiation trajectory modeling (Domanski et al., *JACC*, 2020; Ference et al., *Eur Heart J*, 2017). Multiplying a single spot lipid level by baseline age and taking the natural log simply creates a non-linear interaction between age and spot cholesterol. Calling this "cumulative atherogenic exposure" overstates the model's biological specification.

---

## 2. Resolution of Factual Disagreements & Preserved Dissent

### Resolved Factual Points (Backed by 2016–2026 Evidence)

1. **Phenotypic Severity Spectrum:**
   * *Resolution:* Manuscript claims of evaluating "genetically confirmed FH" are factually incorrect. UK Biobank dataset contains an unannotated `ldlr_carrier` flag with empty `variant_id` fields across all 501,936 master rows. Median untreated LDL-C ($3.95\text{ mmol/L}$) confirms this is a population-identified variant carrier pool with attenuated phenotype, distinct from clinical FH index cases ($>4.9\text{ mmol/L}$) (Gidding et al., *JAHA*, 2023; Trinder et al., *JAMA Cardiol*, 2020).
2. **Lipid Predictor Multivariable Non-Significance:**
   * *Resolution:* Examination of the primary Cox model equation (Table 2) confirms that all three lipid-derived predictors (`cum_nonhdl`, `tg_filter`, remnant cholesterol) fail to achieve statistical significance ($p>0.05$; 95% CIs cross 1.0). The C-statistic gain attributable to all lipid terms combined is $+0.008$.
3. **Head-to-Head 5-Year Horizon Non-Significance:**
   * *Resolution:* After Holm multiplicity adjustment across the 6 primary confirmatory comparisons, CALON-C demonstrates **zero statistically significant wins at 5 years** against SAFEHEART-RE ($p=0.0560$), Montreal-FH-SCORE ($p=0.1413$), or FH-Risk-Score ($p=0.5018$). Superiority claims are limited strictly to full follow-up against SAFEHEART-RE and Montreal.

---

### Preserved Named Dissent

```
+---------------------------------------------------------------------------------------------------+
| PRESERVED NAMED DISSENT MATRIX                                                                    |
+---------------------------------------------------------------------------------------------------+
| DISSENT ISSUE                   | SPECIALIST A POSITIONS            | SPECIALIST B POSITIONS        |
+---------------------------------+-----------------------------------+-------------------------------+
| Retaining Non-Significant Lipid | BIOSTATISTICIAN:                  | LIPID-MEDICINE SPECIALIST:    |
| Terms in Linear Predictor       | Retain all 9 terms under ridge    | Relabel model as routine      |
|                                 | penalty (lambda=0.02) to prevent  | clinical risk score; stop     |
|                                 | selection bias in prediction.     | claiming "lipid mechanics."   |
+---------------------------------+-----------------------------------+-------------------------------+
| Routine-Panel Parsimony vs.     | CARDIOLOGIST:                     | LIPID-MEDICINE SPECIALIST:    |
| Mandatory Lp(a) Screening       | Parsimony enables immediate       | Omitting Lp(a) compromises    |
|                                 | scalable primary care triage      | guideline compliance; C-stats |
|                                 | without waiting for Lp(a).        | are insensitive to Lp(a) NRI. |
+---------------------------------+-----------------------------------+-------------------------------+
| Status of All-Wales Dataset     | SENIOR EDITOR-IN-CHIEF:           | BIOSTATISTICIAN:              |
| Evaluation                      | Non-independent internal          | Geographic setting transport  |
|                                 | development dataset due to prior  | stress-test under real-world  |
|                                 | programme exposure.               | EHR missingness constraints.  |
+---------------------------------+-----------------------------------+-------------------------------+
```

---

## 3. Five Consensus Points

1. **Fatal Pipeline & Execution Blockers:**
   The manuscript cannot be published in its current form due to two fatal execution defects: (a) the UK Biobank competing-risk cause-specific cumulative incidence pipeline failed to execute due to a dataset schema bug (`death` column missing), leaving absolute risk estimates mathematically unadjusted for non-ASCVD mortality; and (b) All-Wales baseline tables, internal discrimination, calibration, and model equations reflect an un-synchronized pre-rescue dataset ($n=1,159$, $n_{\text{event}}=92$) rather than the corrected post-rescue risk set ($n=1,169$, $n_{\text{event}}=102$).

2. **Severe Predictor Timing Contamination in All-Wales Transport:**
   Documentation of key clinical risk factors (hypertension, diabetes, smoking) at last contact or post-event in >50% of All-Wales cases introduces severe immortal-time and reverse-causality bias. Restricting analysis to pre-baseline documented predictors dropped discrimination by ~0.030. The Welsh cohort represents an exploratory stress-test under imperfect registry data, not an independent external validation.

3. **Absolute Clinical Safety Boundary (No "De-Risking" in FH):**
   Monogenic FH carries a high lifelong cumulative risk of ASCVD. CALON-C and all short-term FH risk tools must **never** be used to "de-risk" an *LDLR*-variant carrier, de-escalate lipid-lowering therapy, or defer guideline-directed statin/ezetimibe/PCSK9i initiation. Risk scoring serves exclusively to determine treatment escalation urgency.

4. **Multiplicity-Controlled Head-to-Head Benchmark Findings:**
   Under strict complete-input subset matching and Holm multiplicity control across 6 primary comparisons, CALON-C statistically outperformed SAFEHEART-RE ($\Delta C = +0.070$, $p=0.0003$) and Montreal-FH-SCORE ($\Delta C = +0.032$, $p=0.0179$) over full follow-up in UK Biobank. However, CALON-C **tied FH-Risk-Score** ($\Delta C = +0.015$, $p=0.5018$) over full follow-up and achieved **no statistically significant superiority over any comparator at the 5-year horizon**.

5. **Withdrawal of Unearned Clinical Utility & External Calibration Claims:**
   Because comparative Decision Curve Analysis (DCA) was withdrawn due to execution errors, CALON-C provides no proof of net benefit or clinical utility over standard care. Furthermore, internal calibration in UK Biobank (10-year slope $1.101$) cannot be extrapolated externally; absolute risk probabilities must not be used clinically outside derivation settings.

---

## 4. Five Unresolved Disputes

1. **Model Identity: Lipid Exposure Engine vs. Routine Clinical Score:**
   - *Dispute:* The **Biostatistician** maintains that retaining all 9 ridge-penalized terms ($\lambda=0.02$) is methodologically sound for prediction, regardless of individual term $p$-values. The **Lipid-Medicine Specialist** contends that because every lipid term is non-significant ($p>0.05$) and all lipid terms combined add only $+0.008$ to the C-statistic, calling CALON-C a "cumulative atherogenic exposure model" is a biological over-claim; it functions mathematically as a routine clinical score.

2. **Role of Routine-Panel Parsimony vs. Guideline-Mandated Lp(a) Screening:**
   - *Dispute:* The **Cardiologist** argues that a routine-variable model excluding Lp(a) fills an urgent health-system gap, enabling immediate scalable triage in primary care where Lp(a) is unmeasured in >80% of records. The **LIPID-MEDICINE SPECIALIST** counters that promoting an Lp(a)-free score risks legitimizing the omission of Lp(a) testing, violating 2026 ACC/AHA and 2025 ESC/EAS guidelines mandating universal baseline Lp(a) screening in FH.

3. **Methodological Validity of Fixed Lipid Treatment Back-Calculation:**
   - *Dispute:* The **Biostatistician** accepts fixed division factors ($/0.70$ for non-HDL/LDL) as a pragmatic population-level adjustment that performs adequately in sensitivity analyses ($\Delta C = 0.0022$). The **Lipid-Medicine Specialist** asserts that static $/0.70$ division ignores combination LLT (statins + ezetimibe + PCSK9i = 75–85% reduction), causing massive under-estimation of untreated LDL-C in aggressively treated high-risk patients.

4. **Scientific Value of Non-Significant Biomarker Increments in the Grey Zone:**
   - *Dispute:* The **Cardiologist** and **Biostatistician** view the non-significant C-statistic changes ($\Delta C = -0.0038$ for Lp(a); $+0.0146$ for apoB/LDL-C) in the 5%–20% risk band as empirical proof that specialized biomarkers add no rank-discrimination value. The **Lipid-Medicine Specialist** argues that this analysis is flawed because it was conducted on a superseded model (CALON-F) and because $C$-statistics are inherently insensitive to biomarker reclassification (NRI/net benefit analysis required).

5. **Classification of the All-Wales Cohort Evaluation:**
   - *Dispute:* The **Senior Editor-in-Chief** classifies All-Wales as an internal development registry that cannot provide external transport claims due to prior programme exposure and severe predictor-timing flaws. The **Biostatistician** views All-Wales as a valid geographic setting-transport stress test that quantifies model degradation under real-world EHR data limitations.

---

## 5. Lessons for Dr Genedy

Dr Genedy, these five unresolved disputes offer fundamental methodological and clinical lessons for your research program:

1. **Distinguish Multivariable Prediction from Causal Biological Mechanism:**
   * *Lesson:* Do not confuse multivariable predictor performance with causal physiology. In a cohort pre-selected for high lifelong LDL-C exposure (monogenic *LDLR* carriers), spot lipid variations are narrow and suppressed by treatment. Consequently, age, sex, hypertension, and diabetes dominate multivariable risk ranking. Retaining lipid terms in a penalized model is statistically acceptable, but you must transparently state that discrimination is driven by clinical risk factors (+0.033 C-gain) rather than lipid mechanics (+0.008 C-gain).

2. **Respect the Insensitivity of Rank Discrimination ($C$-Statistic) to Biomarkers:**
   * *Lesson:* A non-significant change in $C$-statistic ($\Delta C$) does not mean a biomarker lacks clinical utility. Rank discrimination ($C$-statistic) is notoriously insensitive to adding even powerful independent risk factors (like Lp(a) or apoB) to a model already containing age and sex. To evaluate biomarker utility in intermediate-risk grey zones, you must perform categorical Net Reclassification Improvement (NRI), Integrated Discrimination Improvement (IDI), and Decision Curve Analysis (DCA) rather than relying solely on $\Delta C$.

3. **Incorporate Pharmacological Precision in Treatment Adjustment:**
   * *Lesson:* Population-average multipliers (such as dividing treated LDL-C by 0.70) were developed for general-population cohorts on low-to-moderate intensity statin monotherapy. In modern FH cohorts where patients receive combination therapy (high-intensity statins + ezetimibe + PCSK9 inhibitors), a static 30% reduction assumption severely under-calculates pre-treatment cholesterol burden. Future iterations should incorporate statin intensity categories and multi-agent LLT indicators to prevent systematic pharmacological bias.

4. **Biochemical Units Cannot Be Converted via Arbitrary Scalar Constants:**
   * *Lesson:* Avoid using scalar conversion factors (like dividing nmol/L by 2.15) to convert Lp(a) particle number to mass concentration (mg/dL) when evaluating comparator risk scores. Because apolipoprotein(a) isoform size varies dramatically across individuals, scalar conversions introduce non-linear measurement error. When comparing risk scores, evaluate comparators strictly within their native, published measurement units.

5. **Pragmatic EHR Evaluability Is a Double-Edged Sword:**
   * *Lesson:* Building a parsimonious model using routine variables ensures that 100% of primary care health records can be scored—a massive operational advantage over complex instruments like SAFEHEART-RE or FH-Risk-Score, which were non-estimable in >85% of the Welsh registry due to missing Lp(a) and BMI. However, routine EHR data frequently suffer from un-dated or post-event risk factor entry. You must explicitly frame routine-data models as pragmatic risk-ranking tools for health-system triage, while acknowledging that timing limitations require prospective validation before clinical deployment.

---

### Key Supporting Evidence Ledger (2016–2026 Window)

1. **Blumenthal RS, Morris PB, Gaudino M, et al.** 2026 ACC/AHA/AACVPR/ABC/ACPM/ADA/AGS/APhA/ASPC/NLA/PCNA guideline on the management of dyslipidemia. *Circulation*. 2026;153(18):e1154–e1276. DOI: [10.1161/CIR.0000000000001423](https://doi.org/10.1161/CIR.0000000000001423).
2. **Mach F, Koskinas KC, Roeters van Lennep JE, et al.** 2025 focused update of the 2019 ESC/EAS Guidelines for the management of dyslipidaemias. *Eur Heart J*. 2025;46(38):4359–4378. DOI: [10.1093/eurheartj/ehaf190](https://doi.org/10.1093/eurheartj/ehaf190).
3. **Pérez de Isla L, Alonso R, Mata N, et al.** Predicting cardiovascular events in familial hypercholesterolemia: the SAFEHEART Registry. *Circulation*. 2017;135(22):2133–2144. DOI: [10.1161/CIRCULATIONAHA.116.024541](https://doi.org/10.1161/CIRCULATIONAHA.116.024541).
4. **Paquette M, Bernard S, Cariou B, et al.** Familial Hypercholesterolemia-Risk-Score: a new score predicting cardiovascular events and cardiovascular mortality in familial hypercholesterolemia. *Arterioscler Thromb Vasc Biol*. 2021;41(10):2632–2640. DOI: [10.1161/ATVBAHA.121.316106](https://doi.org/10.1161/ATVBAHA.121.316106).
5. **Gidding SS, Cornel JH, Catapano AL, et al.** Phenotypic expression and cardiovascular risk in population-identified carriers of pathogenic monogenic familial hypercholesterolemia variants. *J Am Heart Assoc*. 2023;12(14):e030073. DOI: [10.1161/JAHA.123.030073](https://doi.org/10.1161/JAHA.123.030073).
6. **Domanski MJ, Tian X, Wu CO, et al.** Time course of LDL-cholesterol exposure and cardiovascular disease event risk. *J Am Coll Cardiol*. 2020;76(13):1507–1516. DOI: [10.1016/j.jacc.2020.07.059](https://doi.org/10.1016/j.jacc.2020.07.059).
7. **Sniderman AD, Thanassoulis G, Glavinovic T, et al.** Apolipoprotein B particles and cardiovascular risk: identification of discordant risk phenotypes. *JAMA Cardiol*. 2019;4(12):1287–1295. DOI: [10.1001/jamacardio.2019.3780](https://doi.org/10.1001/jamacardio.2019.3780).
8. **Collins GS, Moons KGM, Dhiman P, et al.** TRIPOD+AI statement: updated guidance for reporting clinical prediction models using machine learning or multivariable regression. *BMJ*. 2024;385:e078378. DOI: [10.1136/bmj-2023-078378](https://doi.org/10.1136/bmj-2023-078378).
