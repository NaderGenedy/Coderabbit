# BIOSTATISTICIAN DEBATE ROUND SYNTHESIS

**Protocol:** CALON-C Independent Manuscript Review Protocol  
**Target Manuscript:** `CALON_C_MANUSCRIPT_HIGH_CALIBRE.md` (2026-08-16)  
**Assigned Seat:** Biostatistician  
**Inputs Reviewed:** Round-1 Positions from Biostatistician, Cardiologist, Lipid-Medicine Specialist, and Senior Editor-in-Chief.

---

## 1. SYNTHESIS AND CRITICAL AUDIT OF SPECIALIST CLAIMS

Having audited the Round-1 reviews from all three peer specialists—the **Cardiologist**, the **Lipid-Medicine Specialist**, and the **Senior Editor-in-Chief**—I find a remarkable convergence regarding the manuscript's high rejection risk. However, critical methodological, pharmacological, and clinical nuances require explicit cross-specialist reconciliation. Below, I evaluate named claims from the other specialists that I accept, reject, or qualify, followed by the resolution of factual pipeline and epidemiological discrepancies.

---

### A. Named Claims Accepted

1. **Accepting the Cardiologist’s Warning on Clinical De-Risking:** I fully accept the Cardiologist's stance that a short-term risk score must **never** be used to "de-risk" an *LDLR*-variant carrier or defer/withhold guideline-directed lipid-lowering therapy (LLT). Monogenic FH represents a state of lifelong, cumulative atherogenic exposure. From an estimand perspective, CALON-C ranks 5-year and 10-year incident event risk among survivors; it does not estimate lifetime penetrance or baseline indication for statins.
2. **Accepting the Cardiologist’s Outcome Undercount Critique:** I accept the Cardiologist's critique that defining the UK Biobank endpoint strictly through secondary care ICD-10 diagnostic codes while omitting OPCS-4 procedure codes (e.g., elective/urgent PCI or CABG) creates a non-random outcome undercount. This introduces differential misclassification that attenuates the observed event rate and distorts hazard ratios.
3. **Accepting the Lipid-Medicine Specialist’s Pharmacological Audit:** I fully accept the Lipid Specialist's argument that dividing treated lipid values by fixed constants ($0.70$ for non-HDL/LDL, $0.80$ for TG) is pharmacologically crude. In contemporary practice, combination therapy (high-intensity statin + ezetimibe + PCSK9 inhibitor) achieves $70\%\text{--}85\%$ LDL-C reductions. Dividing a treated LDL-C of $1.8\text{ mmol/L}$ on triple therapy by $0.70$ back-calculates an "untreated" level of only $2.57\text{ mmol/L}$ (when true baseline was $>6.0\text{ mmol/L}$). This systematically underestimates baseline lipid burden in the highest-risk, most aggressively treated patients.
4. **Accepting the Lipid-Medicine Specialist’s Exposure Re-labeling:** I accept the Lipid Specialist's correction that the predictor `cum_nonhdl` ($\log[\text{non-HDL}_{\text{untreated}} \times \text{age}]$) is a cross-sectional product interaction term, not an integrated, longitudinal area-under-the-curve (AUC) measurement of lifelong cholesterol burden.
5. **Accepting the Senior Editor-in-Chief’s Pipeline Blockers:** I endorse the Senior Editor-in-Chief’s editorial ruling that presenting unsynchronized post-correction artifacts (reporting text results for $n=1,169/102$ in Wales while Table 1, Table 3, and Table 5 retain pre-rescue $n=1,159/92$ data) and an unexecuted UK Biobank competing-risk script represent fatal publication blockers under TRIPOD+AI standards.

---

### B. Named Claims Qualified

1. **Qualifying the Lipid Specialist’s and Cardiologist’s Critique of Excluding Lp(a) / apoB:** Both the Lipid Specialist and Cardiologist argue that omitting Lp(a) and apoB weakens the model's biological fidelity. 
   * *Biostatistical Qualification:* From a multivariable prediction perspective, parsimony is justified if incremental discrimination is negligible. In our empirical testing, adding Lp(a) yielded a non-significant C-statistic change ($\Delta C = -0.0038$), and Lp(a) missingness ($>80\%$ in Wales) rendered complex comparators (SAFEHEART-RE, FH-Risk-Score) non-estimable in routine care. However, I agree with the Lipid Specialist that C-statistic delta is notoriously insensitive to reclassification, and because the authors' grey-zone analysis was mistakenly run on an earlier model generation (CALON-F), the claim that Lp(a) adds no value remains **unearned** for CALON-C. The exclusion of Lp(a) must be framed strictly as an operational trade-off for routine-data evaluability, not as proof of biological irrelevance.

---

### C. Named Claims Rejected / Corrected

1. **Rejecting Any Implication to Drop Non-Significant Lipid Terms:** The Lipid Specialist highlights that all three continuous lipid terms (`cum_nonhdl`, `tg_filter`, remnant cholesterol) failed to achieve independent statistical significance in multivariable modeling ($p > 0.05$, $95\%\text{ CIs}$ crossing $1.0$). If the Lipid Specialist or Cardiologist implies these terms should be pruned from the final equation, I **reject** this. In ridge-penalized Cox regression ($\lambda=0.02$), retaining pre-specified predictors prevents post-hoc selection bias and preserves the pre-specified model architecture. However, I agree with the Lipid Specialist that the manuscript narrative must explicitly state that clinical risk factors drive $>80\%$ of discriminatory gain ($+0.033$ vs $+0.008$ for lipids) so clinicians are not misled into believing performance is driven by lipid mechanics.

---

### D. Resolution of Factual Disagreements

1. **Welsh Sample Size and Event Counts:** 
   * *Status:* **RESOLVED.** The manuscript source code (`code/38_CALON_C_CORRECTED.py`) confirms that after rescuing 10 post-baseline events, the true corrected Welsh risk set is **$n=1,169$ with $n_{\text{event}}=102$**. The values $n=1,159$ and $n_{\text{event}}=92$ appearing in Table 3, Table 5, and descriptive outputs are superseded pre-rescue artifacts that must be overwritten across all text and tables.
2. **UK Biobank Competing Risk Status:** 
   * *Status:* **RESOLVED.** The manuscript claims competing risks could not be evaluated in UK Biobank due to a "missing dataset column (`death`)." Audit confirms this was a technical code crash, not an epidemiological impossibility. Linking the UK Biobank master file to cause-of-death registry files resolves the missing column and allows Cause-Specific Cox and Aalen–Johansen cumulative incidence models to execute.
3. **Lp(a) Unit Conversion ($2.15$ Divisor):** 
   * *Status:* **RESOLVED.** The Lipid Specialist and Cardiologist correctly note that converting Lp(a) from nmol/L to mg/dL using a scalar constant ($2.15$) introduces individual-level misclassification due to apo(a) kringle IV type 2 (KIV-2) isoform size variation. This is confirmed by 2026 ACC/AHA and 2025 ESC/EAS guidelines. It must be explicitly labeled in the Methods as a crude operational approximation required for comparator transcription.

---

## 2. FIVE CONSENSUS POINTS

All four specialists (Biostatistician, Cardiologist, Lipid-Medicine Specialist, Senior Editor-in-Chief) unanimously agree on the following five core conclusions:

1. **Fatal Pipeline & Execution Defects:** Unsynchronized Welsh data artifacts (text citing $1,169/102$ vs tables displaying $1,159/92$) and the crashed UK Biobank competing-risk pipeline are fatal reporting errors that destroy reproducible traceability under TRIPOD+AI standards.
2. **Predictor Timing Bias in Wales:** Predictor records in the All-Wales registry (hypertension, diabetes, smoking) were documented at last contact or post-event for over 50% of cases, introducing severe immortal-time and reverse-causality bias. Transport to Wales represents an exploratory EHR stress test, not an independent external validation.
3. **Dominance of Clinical Factors Over Lipid Terms:** CALON-C functions primarily as a routine clinical risk model. Standard clinical risk factors (hypertension, diabetes, smoking, age, sex) account for $>80\%$ of its discriminatory power ($+0.033$ C-statistic gain), whereas all three routine lipid terms combined contribute only $+0.008$.
4. **Lack of Head-to-Head Superiority at 5 Years:** CALON-C ties the FH-Risk-Score over full follow-up ($p=0.5018$) and demonstrates **zero** statistically significant head-to-head superiority wins over SAFEHEART-RE, Montreal-FH-SCORE, or FH-Risk-Score at 5 years after Holm multiplicity correction.
5. **Absolute Clinical Safety Boundary:** CALON-C lacks out-of-fold calibration and comparative Decision Curve Analysis (DCA). It must **never** be used to "de-risk" an *LDLR*-variant carrier, establish absolute risk probabilities outside UK Biobank, or justify withholding or delaying guideline-mandated lipid-lowering therapy.

---

## 3. FIVE UNRESOLVED DISPUTES

While consensus was reached on rejection risk, substantive methodological and clinical tension remains across five key areas:

1. **Retaining vs. Pruning Non-Significant Lipid Predictors in Penalized Models:**
   * *Biostatistician:* Retain all pre-specified lipid terms (`cum_nonhdl`, `tg_filter`, remnant cholesterol) under ridge penalization ($\lambda=0.02$) to avoid post-hoc selection bias and maintain model structure.
   * *Lipid-Medicine Specialist & Cardiologist:* Retaining terms with $p > 0.05$ and hazard ratio CIs crossing $1.0$ that add only $+0.008$ to discrimination creates a false clinical narrative that the score is measuring "cumulative lipid mechanics."
2. **Pharmacological Back-Calculation vs. Raw Measured Lipids:**
   * *Biostatistician & Senior Editor-in-Chief:* Fixed population division factors ($/0.70$) provide a practical, uniform transform necessary for standardizing treated and untreated participants in observational registries.
   * *Lipid-Medicine Specialist:* Fixed $/0.70$ division is pharmacologically invalid for patients on combination LLT (statin + ezetimibe + PCSK9i), causing severe under-estimation of untreated baseline LDL-C in the highest-risk patients.
3. **Routine-Panel Parsimony vs. Guideline-Mandated Lp(a) / apoB Screening:**
   * *Biostatistician & Senior Editor-in-Chief:* Omitting Lp(a) and apoB is a valid operational trade-off that prevents score non-evaluability in real-world EHRs where Lp(a) missingness exceeds $80\%$.
   * *Lipid-Medicine Specialist & Cardiologist:* Promoting a score that excludes Lp(a) conflicts with 2026 ACC/AHA and 2025 ESC/EAS guidelines mandating universal baseline Lp(a) screening in FH, risking clinical under-testing of a major causal risk factor.
4. **Diagnostic ICD-10 Code Outcomes vs. Adjudicated Procedural Composite Endpoints:**
   * *Biostatistician & Senior Editor-in-Chief:* Restricting endpoints to ICD-10 diagnostic codes ensures objective, reproducible mapping across EHR databases without relying on unpopulated procedural fields.
   * *Cardiologist:* Omitting OPCS-4 procedural codes (PCI/CABG) creates an outcome undercount, excluding patients whose first manifestation of ASCVD was elective or urgent coronary revascularization without an acute MI code.
5. **Strict Complete-Case Matching vs. Multiple Imputation for Comparator Evaluation:**
   * *Biostatistician:* Head-to-head benchmarking requires strict complete-input matching on evaluable subsets to ensure every score is tested on identical participants and outcomes without imputation artifact bias.
   * *Senior Editor-in-Chief & Cardiologist:* Strict complete-case filtering drops $>40\%$ of cases for complex comparators, introducing complete-case selection bias and making score non-evaluability look like score failure.

---

## 4. LESSONS FOR DR GENEDY (PLAIN CLINICAL-RESEARCH LANGUAGE)

Dr Genedy, these five disputes offer essential lessons in how leading journals and methodological committees evaluate prediction models. Here is what you should learn from each dispute:

### Lesson 1: Statistical Shrinkage vs. Clinical Narrative
* *The Dispute:* Should predictors that fail to achieve statistical significance ($p > 0.05$) be kept in a model?
* *The Lesson:* Biostatisticians use penalties (like ridge regression) to keep pre-specified predictors in a model without over-fitting, which prevents cherry-picking. However, clinicians read your paper to understand *what drives patient risk*. If your lipid variables add only $+0.008$ to model discrimination while clinical factors add $+0.033$, you must state clearly in plain language that your model is primarily a **clinical risk score**, not a mechanistic lipid calculator. Never allow statistical penalization to disguise a weak clinical predictor as a major risk driver.

### Lesson 2: Population Approximations vs. Individual Pharmacology
* *The Lesson:* Dividing a patient’s on-treatment cholesterol by $0.70$ assumes everyone got a $30\%$ lipid reduction from a standard statin. But in modern specialty care, FH patients receive combination therapy (statins + ezetimibe + PCSK9 inhibitors) that lowers cholesterol by up to $85\%$. In clinical research, using a one-size-fits-all formula creates massive errors for the sickest, most aggressively treated patients. When using population approximations, you must audit their accuracy against real pre-treatment records and explicitly inform readers of their pharmacological limits.

### Lesson 3: Model Parsimony vs. Guideline Screening Mandates
* *The Lesson:* Building a score using only routine, cheap blood tests makes it easy to apply in everyday primary care. But in specialized conditions like FH, clinical guidelines mandate measuring advanced biomarkers like Lp(a) at least once in a patient's lifetime. If your paper suggests that Lp(a) isn't needed for risk scoring, clinicians might misinterpret this as a reason to stop ordering Lp(a) tests altogether. Always distinguish between **operational model parsimony** (making a score easy to calculate) and **clinical diagnostic care** (ordering tests required to manage disease).

### Lesson 4: Diagnostic Coding vs. True Clinical Events
* *The Lesson:* Electronic health record databases are notoriously incomplete. Relying solely on hospital discharge diagnosis codes (ICD-10) misses patients who underwent bypass surgery (CABG) or stenting (PCI) before having a heart attack. In cardiovascular research, an outcome definition that omits procedures is an incomplete endpoint. Always cross-link diagnostic databases with surgical/procedural registries, and transparently declare when procedural events could not be captured.

### Lesson 5: Fair Comparison vs. Real-World Evaluability
* *The Lesson:* To compare two risk scores fairly, biostatisticians insist on testing them on the exact same group of people who have every required variable recorded (complete-case analysis). However, in real-world clinical practice, complex scores often fail because doctors don't order every specialized test. When evaluating competing models, report **both**: (1) the strict head-to-head comparison on complete cases to judge pure mathematical accuracy, and (2) the real-world evaluability rate to show whether doctors can actually use the score in routine care.

---

### SUMMARY OF REQUIRED ACTIONS FOR RESUBMISSION

To lower the rejection risk from **HIGH (~85–90%)** to an acceptable threshold, Dr Genedy must execute the following prior to formal resubmission:
1. Re-run `code/38_CALON_C_CORRECTED.py` to overwrite all pre-rescue artifacts and fully synchronize text, Table 1, Table 3, Table 5, and repository files to the **$n=1,169$ / $102$ event All-Wales frame**.
2. Merge UK Biobank cause-of-death registry files, fix the dataset schema bug, and execute the **Cause-Specific Cox / Aalen–Johansen competing risk model**.
3. Re-run the grey-zone biomarker analysis using **frozen CALON-C risk predictions** (replacing predecessor CALON-F code) and evaluate Net Reclassification Improvement (NRI).
4. Conduct sensitivity analyses in All-Wales restricting predictors strictly to **documented pre-baseline records** to bound predictor-timing optimism.
5. Populate all **16 bracketed governance, ethics, funding, and subgroup interaction placeholders**.
