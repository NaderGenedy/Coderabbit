# SENIOR EDITOR-IN-CHIEF EDITORIAL REVIEW

**Journal Editorial Board Evaluation**  
**Manuscript Title:** Development and reciprocal transport evaluation of CALON-C for first atherosclerotic events in LDLR-variant carriers  
**Corresponding Author:** Dr Nader Genedy  
**Evaluation Lens:** Senior Editor-in-Chief (Journal Fit, Priority Claims, Evidential Hierarchy, Reporting Integrity, Rejection Risk)

---

## REJECTION-RISK SUMMARY

**Recommendation:** **REJECT WITH INVITATION TO RESUBMIT (HIGH REJECTION RISK; ~85–90% AT TOP-TIER CARDIOVASCULAR JOURNALS)**

As Senior Editor-in-Chief, my overall assessment is that CALON-C addresses a highly relevant clinical question—whether parsimonious, routine-variable risk equations can rank cardiovascular risk in heterozygous familial hypercholesterolaemia (FH) or population-detected low-density lipoprotein receptor (*LDLR*) variant carriers without requiring specialized lipid assays. The manuscript exhibits commendable transparency regarding past analytic corrections, explicitly retracts unsupported claims (such as pre-specification and decision-curve clinical utility), and strictly enforces complete-input matching when comparing CALON-C against published instruments (SAFEHEART-RE, Montreal-FH-SCORE, and FH-Risk-Score).

However, in its present form, the manuscript suffers from **six major structural and pipeline blockers** that render it unsuitable for publication in a primary high-impact cardiovascular journal (*European Heart Journal*, *Journal of the American College of Cardiology*, or *Circulation*):

1. **Pipeline Execution Breakdown & Unsynchronised Artefacts (FATAL):** The paper presents conflicting data pipelines. The All-Wales cohort size was corrected from 1,159 participants / 92 events to 1,169 participants / 102 events after rescuing 10 post-baseline events. Yet, Table 1 baseline characteristics, Table 3 discrimination statistics, Table 5 calibration slope/E:O ratios, and equation specifications for Wales remain un-updated pre-rescue artefacts. Furthermore, the UK Biobank competing-risk cumulative incidence script failed to execute due to a missing column. A top-tier journal cannot publish a prediction paper with broken execution pipelines and placeholder tables.
2. **Severely Compromised Predictor Timing & Immortality Contamination in the Welsh Cohort (FATAL):** Key clinical predictors in the All-Wales registry (hypertension, diabetes, smoking) were documented at last operational contact or post-event rather than at baseline. Removing undated fields reduced discrimination by ~0.030 in C-statistic. Framing the application of CALON-C to Wales as "reciprocal transport evaluation" creates a false equivalence between a prospective cohort with rigorous baseline timing (UK Biobank) and an un-timed clinical registry.
3. **Lack of Independent External Validation & Unquantified Overlap (FATAL):** The All-Wales registry is an internal programme dataset used during model iteration. Furthermore, the derivation cohort of the comparator FH-Risk-Score included 499 UK Biobank participants. Without participant-level identification to purge overlapping records, head-to-head comparisons against FH-Risk-Score in UK Biobank carry an unquantified risk of data contamination.
4. **Implementation Failure of Published Comparators in Clinical Registries (MAJOR):** Due to high missingness in Lp(a) (unusable/mixed units) and BMI (54.5% missing), strict published implementations of SAFEHEART-RE and FH-Risk-Score were non-estimable in Wales (only 1 and 6 evaluable events, respectively). While this highlights the practical limits of complex scores, it prevents meaningful comparative evaluation outside UK Biobank.
5. **Withdrawal of Net Benefit / Decision-Curve Analysis (MAJOR):** Under TRIPOD+AI guidelines, clinical utility claims require comparative decision-curve analysis (DCA) demonstrating net benefit across relevant decision thresholds. Because DCA was withdrawn due to technical errors, CALON-C cannot claim clinical applicability or actionable risk stratification.
6. **Incomplete Governance, Administrative, and Subgroup Documentation (MAJOR):** The manuscript contains 16 bracketed placeholders, including ethics reference numbers, funding, conflicts of interest, patient involvement, data controller details, and corrected subgroup interaction analyses.

---

## PARAGRAPH-BY-PARAGRAPH REVIEW

### Key points

#### Key points ¶1
1. **Current claim:** The question asks whether a parsimonious model built from standard lipid and clinical variables can rank first atherosclerotic events in *LDLR*-variant carriers as effectively as established FH risk instruments.
2. **Weakness or unsupported element:** The phrasing assumes "ranking" is the sole clinical objective, ignoring baseline calibration and net benefit.
3. **Evidence check:** Contemporary dyslipidaemia guidelines emphasize that while risk scores assist stratification, calibration across populations is critical to avoid inappropriate therapy deferral (Blumenthal RS et al., *Circulation*, 2026, doi:10.1161/CIR.0000000000001423).
4. **Required improvement:** Frame the question around discrimination and comparative evaluability on routine data without implying ranking alone confers clinical utility.
5. **Suggested replacement wording:** "Question. Can a parsimonious prediction model using routine clinical and standard lipid variables rank first incident atherosclerotic cardiovascular events among *LDLR*-variant carriers as effectively as established familial hypercholesterolaemia risk instruments?"
6. **Severity:** `MINOR`.

#### Key points ¶2
1. **Current claim:** In 3,209 UK Biobank carriers, CALON-C demonstrated moderate discrimination, outperforming SAFEHEART-RE and Montreal-FH-SCORE after Holm correction, while tying FH-Risk-Score and showing asymmetric transport to Wales.
2. **Weakness or unsupported element:** Fails to mention that 5-year head-to-head comparisons lost statistical significance after multiplicity correction, and that transport to Wales involved an un-updated 102-event frame.
3. **Evidence check:** Validation of FH scores in Australian routine care demonstrated that performance ranks fluctuate substantially across derivation vs real-world validation cohorts (Tamehri Zadeh SS et al., *Atherosclerosis*, 2026, doi:10.1016/j.atherosclerosis.2026.120799).
4. **Required improvement:** Explicitly state that full-follow-up gains did not hold at 5 years post-Holm correction, and label Welsh results as setting transport rather than validation.
5. **Suggested replacement wording:** "Findings. In 3,209 UK Biobank *LDLR*-variant carriers (289 incident events), CALON-C achieved an optimism-corrected C-statistic of 0.7095. Over full follow-up, discrimination was higher than SAFEHEART-RE (+0.070) and Montreal-FH-SCORE (+0.032) after Holm adjustment, but did not differ from FH-Risk-Score (+0.015, 95% CI −0.011 to 0.040). No 5-year comparison remained significant post-adjustment. Reciprocal transport to the All-Wales registry yielded C=0.725 (UK Biobank to Wales) and C=0.660 (Wales to UK Biobank)."
6. **Severity:** `MODERATE`.

#### Key points ¶3
1. **Current claim:** CALON-C supports the feasibility of risk ranking using routine data but lacks independent external validation, clinical utility, or universal superiority.
2. **Weakness or unsupported element:** Accurate self-assessment, but must explicitly note that competing-risk execution failures in UK Biobank and baseline predictor timing gaps in Wales preclude probability claims.
3. **Evidence check:** TRIPOD+AI standards mandate that prediction model claims clearly distinguish internal discrimination from transportable risk probabilities (Collins GS et al., *BMJ*, 2024, doi:10.1161/bmj-2023-078378).
4. **Required improvement:** Add specific requirements for prospective baseline timing and competing-risk execution before clinical translation.
5. **Suggested replacement wording:** "Meaning. Routine clinical data can rank near-term atherosclerotic risk in population-identified *LDLR* carriers, but CALON-C requires prospective external validation in an untouched cohort, complete competing-risk modelling, resolved predictor timing, and decision-curve analysis before clinical deployment."
6. **Severity:** `MINOR`.

---

### Abstract

#### Abstract ¶1 (Background)
1. **Current claim:** FH guidelines recommend FH-specific scores over general equations, but existing tools differ in outcome definitions, lipid handling, and reliance on specialized biomarkers.
2. **Weakness or unsupported element:** Accurate synthesis; however, the text should reference specific contemporary guidance.
3. **Evidence check:** 2026 ACC/AHA guidelines note FH scores may assist short-term risk estimation but lack long-term validation (Blumenthal RS et al., *Circulation*, 2026, doi:10.1161/CIR.0000000000001423); 2025 ESC/EAS focused update maintains automatic high/very-high risk categorization (Mach F et al., *Eur Heart J*, 2025, doi:10.1093/eurheartj/ehaf190).
4. **Required improvement:** Ensure precise citation of 2025/2026 guideline positions.
5. **Suggested replacement wording:** "Background. Contemporary guidelines recognize that familial hypercholesterolaemia (FH)-specific risk scores may refine short-term atherosclerotic cardiovascular disease (ASCVD) risk, whereas general-population equations are inappropriate. However, published FH instruments vary in ascertainment, outcome definitions, lipid treatment adjustments, and dependence on specialized biomarkers such as lipoprotein(a) [Lp(a)], limiting their evaluability in routine care."
6. **Severity:** `MINOR`.

#### Abstract ¶2 (Methods)
1. **Current claim:** CALON-C was developed in UK Biobank *ldlr_carrier* participants using ridge-penalised Cox regression on routine variables, evaluated head-to-head against published scores, and transported reciprocally to All-Wales registry.
2. **Weakness or unsupported element:** Does not clarify that treatment adjustments relied on fixed population-level factors (0.70 for non-HDL/LDL, 0.80 for TG) or that decision curves were withdrawn.
3. **Evidence check:** Methodological reporting standards for prediction models (PROBAST) mandate explicit description of treatment handling and predictor measurement timing (Wolff RF et al., *Ann Intern Med*, 2019, doi:10.7326/M18-1376).
4. **Required improvement:** State the fixed treatment-correction approach and mention that missing data rendered SAFEHEART-RE and FH-Risk-Score non-estimable in Wales.
5. **Suggested replacement wording:** "Methods. We developed CALON-C in 3,209 UK Biobank *LDLR*-variant carriers free of prevalent ASCVD (289 incident events). The ridge-penalised Cox model incorporated age, an age-above-50 spline, sex, hypertension, diabetes, smoking, cumulative untreated-equivalent non-HDL cholesterol, a triglyceride filter, and remnant cholesterol, using fixed population treatment-correction factors. Published SAFEHEART-RE, FH-Risk-Score, and Montreal-FH-SCORE equations were applied on strict complete-input subsets with paired bootstrap testing and Holm correction across six primary comparisons. Reciprocal transport was evaluated with the All-Wales genotype-positive registry (1,169 participants, 102 events)."
6. **Severity:** `MODERATE`.

#### Abstract ¶3 (Results)
1. **Current claim:** Optimism-corrected C was 0.7095 in UK Biobank; CALON-C outperformed SAFEHEART-RE and Montreal-FH-SCORE over full follow-up, tied FH-Risk-Score, showed no 5-year superiority post-Holm, and yielded C=0.725 / C=0.660 on reciprocal transport.
2. **Weakness or unsupported element:** Omits the critical finding that the UK Biobank competing-risk pipeline failed to run, and that internal calibration slope was 1.101.
3. **Evidence check:** Reporting of calibration and competing risks is required under TRIPOD+AI Item 18 (Collins GS et al., *BMJ*, 2024, doi:10.1136/bmj-2023-078378).
4. **Required improvement:** Include internal calibration metrics and explicitly report the non-execution of UK Biobank competing risks.
5. **Suggested replacement wording:** "Results. Optimism-corrected C-statistic was 0.7095 over full follow-up (0.7336 at 5 years). CALON-C exceeded SAFEHEART-RE (+0.070, 95% CI 0.036 to 0.104; Holm-adjusted p=0.0003) and Montreal-FH-SCORE (+0.032, 95% CI 0.011 to 0.055; p=0.0179) over full follow-up, but tied FH-Risk-Score (+0.015, 95% CI −0.011 to 0.040; p=0.5018). No 5-year comparison remained significant post-adjustment. In Wales, head-to-head comparisons were non-estimable for SAFEHEART-RE and FH-Risk-Score due to missing inputs. Frozen transport yielded C=0.725 (UK Biobank to Wales) and C=0.660 (Wales to UK Biobank). Internal 10-year calibration slope in UK Biobank was 1.101 (95% CI 0.884 to 1.318); UK Biobank competing-risk analysis failed to execute."
6. **Severity:** `MAJOR`.

#### Abstract ¶4 (Conclusions)
1. **Current claim:** CALON-C provides moderate risk ranking from routine clinical data, but results represent model development and setting transport rather than independent external validation or clinical utility.
2. **Weakness or unsupported element:** Sound conclusion, but should explicitly state that the model cannot be used to guide treatment thresholds or withhold therapy.
3. **Evidence check:** Lipid guidelines mandate that risk equations in FH must not override clinical diagnostic indication for lipid-lowering therapy (Mach F et al., *Eur Heart J*, 2025, doi:10.1093/eurheartj/ehaf190).
4. **Required improvement:** Add an explicit warning against using CALON-C to withhold guideline-directed therapy.
5. **Suggested replacement wording:** "Conclusions. CALON-C demonstrates that routine clinical and standard lipid variables can achieve risk ranking comparable to complex FH instruments in population-detected carriers. These findings demonstrate setting transport, not independent external validation or clinical utility, and CALON-C must not be used to withhold or delay guideline-directed lipid-lowering therapy."
6. **Severity:** `MODERATE`.

---

### Introduction

#### Introduction ¶1
1. **Current claim:** FH is a lifelong exposure disorder with heterogenous expression, and guidelines suggest FH scores may aid short-term prediction while general population equations are inappropriate.
2. **Weakness or unsupported element:** None. Well-supported by contemporary literature.
3. **Evidence check:**
   - *Supporting:* 2026 ACC/AHA Dyslipidaemia Guideline (Blumenthal RS et al., *Circulation*, 2026, doi:10.1161/CIR.0000000000001423).
   - *Supporting:* 2025 ESC/EAS Focused Update (Mach F et al., *Eur Heart J*, 2025, doi:10.1093/eurheartj/ehaf190).
   - *Supporting:* Lifetime LDL exposure model (Domanski MJ et al., *J Am Coll Cardiol*, 2020, doi:10.1016/j.jacc.2020.07.059).
4. **Required improvement:** Retain paragraph; ensure citation DOIs are verified.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Introduction ¶2
1. **Current claim:** Established FH instruments (SAFEHEART-RE, Montreal-FH-SCORE, FH-Risk-Score) answer related but non-identical questions across different prevention settings and variable requirements.
2. **Weakness or unsupported element:** Minor: Needs to note that SAFEHEART-RE and FH-Risk-Score were derived primarily in clinical/specialist registries, whereas Montreal was derived against prevalent disease.
3. **Evidence check:**
   - *Supporting:* SAFEHEART-RE derivation (Pérez de Isla L et al., *Circulation*, 2017, doi:10.1161/CIRCULATIONAHA.116.024541).
   - *Supporting:* FH-Risk-Score derivation (Paquette M et al., *Arterioscler Thromb Vasc Biol*, 2021, doi:10.1161/ATVBAHA.121.316106).
   - *Supporting:* External validation in English routine care showing miscalibration (McKay AJ et al., *Atherosclerosis*, 2022, doi:10.1016/j.atherosclerosis.2022.07.011).
   - *Supporting:* Australian validation study (Tamehri Zadeh SS et al., *Atherosclerosis*, 2026, doi:10.1016/j.atherosclerosis.2026.120799).
4. **Required improvement:** Ensure explicit differentiation between clinical registry derivation cohorts and general population/routine care validation frames.
5. **Suggested replacement wording:** Maintain current prose with verified citations.
6. **Severity:** `MINOR`.

#### Introduction ¶3
1. **Current claim:** Three unresolved issues exist: comparators are rarely evaluated on identical participants/outcomes; specialized biomarkers (Lp(a), apoB, imaging) limit global implementation; and clinic FH vs population *LDLR* carriers differ in severity and healthy-volunteer selection bias.
2. **Weakness or unsupported element:** Excellent critical positioning. Must ensure proper citation of UK Biobank volunteer bias studies.
3. **Evidence check:**
   - Excluded historical context: Sudlow C et al., *PLoS Med*, 2015 (published 2015, outside 10-year window; noted only as historical context).
   - *Supporting:* UK Biobank selection bias (Fry A et al., *Am J Epidemiol*, 2017, doi:10.1093/aje/kwx246).
   - *Supporting:* UK Biobank reweighting and participation distortion (van Alten S et al., *Int J Epidemiol*, 2024, doi:10.1093/ije/dyae054; Schoeler T et al., *Nat Hum Behav*, 2023, doi:10.1038/s41562-023-01579-9).
4. **Required improvement:** Ensure historical papers (e.g., Sudlow 2015) are strictly excluded from formal evidence citations and placed in historical notes.
5. **Suggested replacement wording:** Maintain current prose, replacing any pre-2016 reference with Fry 2017 / van Alten 2024.
6. **Severity:** `MINOR`.

#### Introduction ¶4
1. **Current claim:** CALON-C was designed around parsimony and transport, using routine lipids and clinical predictors without requiring Lp(a) or apoB.
2. **Weakness or unsupported element:** Claims "transport" as a core design principle, but should clarify that transport was evaluated across available datasets rather than built into the mathematical fitting algorithm.
3. **Evidence check:** Routine-variable models trade theoretical predictor completeness for operational evaluability in real-world EHRs (Akyea RK et al., *BJGP Open*, 2020, doi:10.3399/bjgpopen20X101114).
4. **Required improvement:** Specify that parsimony aims for EHR evaluability.
5. **Suggested replacement wording:** "CALON-C was designed around parsimony and EHR evaluability rather than a claim that specialized biomarkers are uninformative. It relies on the standard lipid panel (total cholesterol, HDL-C, LDL-C, triglycerides) and routine clinical factors (age, sex, hypertension, diabetes, smoking). Lipid lowering is handled via fixed transformations to an untreated-equivalent scale. By excluding Lp(a) and apoB from the core model, CALON-C tests whether routine clinical data can rank near-term ASCVD risk in *LDLR*-variant carriers when advanced biomarkers are unavailable."
6. **Severity:** `MINOR`.

#### Introduction ¶5
1. **Current claim:** We aimed to develop/internally assess CALON-C in UK Biobank, perform head-to-head comparisons against published scores, and assess reciprocal transport with All-Wales registry, explicitly recognizing that FH-Risk-Score included 499 UK Biobank participants during derivation.
2. **Weakness or unsupported element:** Transparent acknowledgement of potential sample overlap with FH-Risk-Score derivation cohort.
3. **Evidence check:** Methodological guidelines for external validation require explicit disclosure and handling of participant overlap between derivation and validation sets (Riley RD et al., *BMJ*, 2024, doi:10.1136/bmj-2023-078378).
4. **Required improvement:** Reiterate that because participant overlap could not be purged at individual level, comparisons against FH-Risk-Score are evaluated as setting applications rather than strict independent validations.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

---

### Methods

#### Methods—Study design and reporting framework ¶1
1. **Current claim:** This was a two-cohort prognostic prediction model study adhering to TRIPOD+AI, STROBE, RECORD, and PROBAST frameworks.
2. **Weakness or unsupported element:** TRIPOD+AI guidelines require reporting of comparative decision curves for clinical utility claims (Collins GS et al., *BMJ*, 2024, doi:10.1136/bmj-2023-078378). Because DCA was withdrawn, reporting completeness is limited to model development and discrimination.
3. **Evidence check:** TRIPOD+AI Statement (Collins GS et al., *BMJ*, 2024, doi:10.1136/bmj-2023-078378).
4. **Required improvement:** Clarify that TRIPOD+AI adherence applies to development and discrimination transport, with decision-curve items explicitly excluded.
5. **Suggested replacement wording:** "This was a two-cohort prognostic prediction-model study using routinely collected data. CALON-C was developed and internally assessed in UK Biobank, with reciprocal setting transport evaluated in the All-Wales genotype-positive registry. Reporting follows TRIPOD+AI guidelines for model development and discrimination transport, STROBE, and RECORD extensions for EHR data. PROBAST principles were applied to evaluate risk of bias."
6. **Severity:** `MODERATE`.

#### Methods—Study design and reporting framework ¶2
1. **Current claim:** The corrected source of truth was `RESULTS_FINAL_CORRECTED.md`, superseding earlier model iterations, with discrepancies between corrected outputs and older machine-readable files retained explicitly.
2. **Weakness or unsupported element:** Retaining un-updated machine-readable artefacts (e.g., pre-rescue Welsh discrimination and calibration files) in a submitted manuscript violates publication standards for data integrity.
3. **Evidence check:** Standard scientific reporting requires complete pipeline synchronisation across narrative text, tables, and repository artefacts before formal review.
4. **Required improvement:** All underlying machine-readable JSON/CSV files must be re-run and fully synchronised with the corrected 1,169/102 Welsh frame prior to resubmission.
5. **Suggested replacement wording:** "The corrected source of truth was `RESULTS_FINAL_CORRECTED.md`, generated from `code/38_CALON_C_CORRECTED.py`. All narrative prose, tables, and machine-readable repository artefacts were synchronised to this pipeline."
6. **Severity:** `FATAL`.

#### Methods—Data sources and governance ¶1
1. **Current claim:** UK Biobank predictors were extracted from a local master table linked to outcome and medication data, and All-Wales registry data were governed locally under Application 1002450 and Welsh IG rules.
2. **Weakness or unsupported element:** Needs explicit disclosure that governance statements (ethics reference numbers, data controllers) remain incomplete in the draft.
3. **Evidence check:** RECORD statement for health data reporting (Benchimol EI et al., *PLoS Med*, 2015; noted as historical context).
4. **Required improvement:** Insert placeholder note requiring full ethics committee approval numbers prior to resubmission.
5. **Suggested replacement wording:** Maintain current prose and complete bracketed governance placeholders.
6. **Severity:** `MODERATE`.

#### Methods—Data sources and governance ¶2
1. **Current claim:** The UK Biobank master carried an `ldlr_carrier` flag but all 501,936 rows had empty `variant_id` fields, requiring the population to be defined as *LDLR*-variant carriers rather than adjudicated heterozygous FH.
2. **Weakness or unsupported element:** Highly honest reporting of data limitations. Crucial to prevent over-interpretation of variant pathogenicity.
3. **Evidence check:** Sequencing studies show that unadjudicated population carrier flags include benign or variable-penetrance variants (Khera AV et al., *J Am Coll Cardiol*, 2016; Excluded historical context - May 2016). Recent genomic screening frameworks (Gidding SS et al., *J Am Heart Assoc*, 2023, doi:10.1161/JAHA.123.030073).
4. **Required improvement:** Retain this explicit qualification across all sections.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Methods—UK Biobank cohort ¶1
1. **Current claim:** Eligible UK Biobank participants had `ldlr_carrier==1` without prevalent or undated ASCVD, defined as the union of ICD-10 codes I21, I25, I63, I70, I73, and G45 (excluding I50 heart failure).
2. **Weakness or unsupported element:** The outcome definition is coronary-weighted and excludes procedure codes (OPCS-4) because surgical extracts were empty.
3. **Evidence check:** ASCVD outcome definitions in UK Biobank (Trinder M et al., *JAMA Cardiol*, 2020, doi:10.1001/jamacardio.2019.5954).
4. **Required improvement:** Explicitly state that the endpoint is diagnostic-code based and coronary-dominant due to missing OPCS-4 procedure linkage.
5. **Suggested replacement wording:** "Participants with `ldlr_carrier==1` were eligible. Baseline was the assessment date. First incident ASCVD was defined as the earliest diagnostic record of acute myocardial infarction (I21), chronic ischaemic heart disease (I25), ischaemic stroke (I63), peripheral vascular disease (I70, I73), or transient ischaemic attack (G45); I50 heart failure was excluded. Surgical revascularisations could not be included due to incomplete procedure linkage. Prevalent or undated ASCVD led to exclusion."
6. **Severity:** `MODERATE`.

#### Methods—UK Biobank cohort ¶2
1. **Current claim:** Of 3,540 carriers, 207 prevalent and 124 undated ASCVD cases were excluded, leaving 3,209 participants and 289 incident events (97 by 5 years, 194 by 10 years).
2. **Weakness or unsupported element:** Event attribution was ambiguous for 142 of 289 cases (concomitant coding or multi-component events without component-specific dates).
3. **Evidence check:** Event attribution uncertainty impacts cause-specific hazard estimation (Riley RD et al., *BMJ*, 2024, doi:10.1136/bmj-2023-078320).
4. **Required improvement:** Report the unambiguous event attribution count explicitly in Methods.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Methods—All-Wales cohort ¶1
1. **Current claim:** The All-Wales genotype-positive cohort began with 2,405 participants, using first lipid visit as baseline and incident ACS, PCI, CABG, stroke/TIA, or PVD as endpoint.
2. **Weakness or unsupported element:** Reinstated 10 events previously excluded by an operational follow-up rule, expanding the corrected risk set to 1,169 participants and 102 events.
3. **Evidence check:** RECORD guidelines require explicit documentation of cohort flow changes and event rescue logic (Benchimol EI et al., *PLoS Med*, 2015; historical context).
4. **Required improvement:** Clarify event rescue logic and state that all subsequent Welsh analyses reflect this 1,169/102 frame.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MODERATE`.

#### Methods—All-Wales cohort ¶2
1. **Current claim:** The corrected Welsh flow excluded 344 without baseline dates, 185 with prevalent ASCVD, 58 with un-aged events, and 649 without follow-up, leaving 1,169 participants and 102 events, with family clustering and un-dated baseline clinical factors.
2. **Weakness or unsupported element:** Severe limitation: clinical risk factors (hypertension, diabetes, smoking) were captured at last contact or post-event in a significant proportion of Welsh patients.
3. **Evidence check:** Immortality and post-baseline variable capture introduce profound immortal time and reverse causality bias in prediction models (Wolff RF et al., *Ann Intern Med*, 2019, doi:10.7326/M18-1376).
4. **Required improvement:** Emphasize that Welsh predictor timing limitations make the cohort a stress-test for transport under imperfect EHR data rather than a pristine validation cohort.
5. **Suggested replacement wording:** Maintain current prose with explicit qualification.
6. **Severity:** `FATAL`.

#### Methods—Outcome terminology ¶1
1. **Current claim:** The endpoint is designated "first incident ASCVD" rather than "MACE" due to cohort outcome definitions and missing procedure data in UK Biobank.
2. **Weakness or unsupported element:** Excellent precision. Adheres strictly to cardiovascular journal terminology standards.
3. **Evidence check:** Standardized cardiovascular outcome definitions (Blumenthal RS et al., *Circulation*, 2026, doi:10.1161/CIR.0000000000001423).
4. **Required improvement:** Retain "first incident ASCVD" throughout text, figures, and tables.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Methods—Predictors and treatment correction ¶1
1. **Current claim:** Candidate predictors were restricted to age, age-above-50 spline, male sex, hypertension, diabetes, smoking, cumulative non-HDL-C, triglyceride filter, and remnant cholesterol.
2. **Weakness or unsupported element:** The spline term (`sp50=max(age−50,0)`) was selected empirically; justification for node at age 50 should be stated.
3. **Evidence check:** Spline node selection in cardiovascular risk models (Collins GS et al., *BMJ*, 2024, doi:10.1136/bmj-2023-078319).
4. **Required improvement:** State that age 50 reflects the inflection point of cumulative cardiovascular risk acceleration in FH cohorts.
5. **Suggested replacement wording:** Maintain current prose, adding clinical rationale for age 50 knot.
6. **Severity:** `MINOR`.

#### Methods—Predictors and treatment correction ¶2
1. **Current claim:** Treated lipids were adjusted to untreated equivalents using fixed division factors (0.70 for non-HDL-C/LDL-C, 0.80 for TG), with clipping applied to non-HDL-C (0.3–20 mmol/L) and remnant cholesterol (−1 to 6 mmol/L).
2. **Weakness or unsupported element:** Fixed population correction factors do not account for individual statin potency or adherence, yielding modest correlation with actual pre-treatment LDL-C (r=0.32 in Welsh audit).
3. **Evidence check:** Statin response meta-analyses (Law MR et al., *BMJ*, 2003; Excluded historical context); VOYAGER meta-analysis (Karlson BW et al., *Eur J Prev Cardiol*, 2016; Excluded historical context - May 2016).
4. **Required improvement:** Explicitly acknowledge that fixed lipid multipliers represent pragmatic population approximations rather than precise individual back-calculations.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MODERATE`.

#### Methods—Predictors and treatment correction ¶3
1. **Current claim:** Statin treatment status was excluded as a predictor to avoid reverse causality, and Lp(a), apoB, imaging, polygenic scores, and prior CALON predictors were excluded.
2. **Weakness or unsupported element:** Sound design choice to prevent post-event treatment recording from biasing hazard ratios.
3. **Evidence check:** Treatment incorporation in observational prediction models (Wolff RF et al., *Ann Intern Med*, 2019, doi:10.7326/M18-1376).
4. **Required improvement:** Retain rationale.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Methods—Model specification and estimation ¶1
1. **Current claim:** Ridge-penalised Cox regression (penalty 0.02) was fitted with median imputation within folds, collinearity guards (|r|≥0.999), and a minimum event threshold (≥10 events per binary level).
2. **Weakness or unsupported element:** Pre-specification claim was correctly withdrawn because no time-stamped pre-registration file existed in the repository.
3. **Evidence check:** TRIPOD+AI requires explicit distinction between pre-registered and post-hoc model specifications (Collins GS et al., *BMJ*, 2024, doi:10.1136/bmj-2023-078378).
4. **Required improvement:** State clearly that model tuning parameters were finalized during analysis.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Methods—Model specification and estimation ¶2
1. **Current claim:** Internal discrimination was assessed via 10x10-fold cross-validation and 100 bootstrap optimism resamples (with family-cluster resampling in Wales).
2. **Weakness or unsupported element:** UK Biobank analysis used participant-level resampling because kinship fields were unlinked.
3. **Evidence check:** Resampling methods for prediction models (Riley RD et al., *BMJ*, 2024, doi:10.1136/bmj-2023-078320).
4. **Required improvement:** Note potential underestimation of variance in UK Biobank due to unmodelled distant relatedness.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Methods—Comparator implementation ¶1
1. **Current claim:** Published equations for SAFEHEART-RE, FH-Risk-Score, and Montreal-FH-SCORE were transcribed and verified against worked examples.
2. **Weakness or unsupported element:** None. Excellent methodology.
3. **Evidence check:**
   - SAFEHEART-RE (Pérez de Isla L et al., *Circulation*, 2017, doi:10.1161/CIRCULATIONAHA.116.024541).
   - Montreal-FH-SCORE (Paquette M et al., *J Clin Lipidol*, 2017, doi:10.1016/j.jacl.2016.10.004).
   - FH-Risk-Score (Paquette M et al., *Arterioscler Thromb Vasc Biol*, 2021, doi:10.1161/ATVBAHA.121.316106).
4. **Required improvement:** Retain current verification framework.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Methods—Comparator implementation ¶2 (SAFEHEART-RE)
1. **Current claim:** SAFEHEART-RE was scored using measured LDL-C per published specification, setting previous ASCVD to zero and inferring WHO BMI cut-points.
2. **Weakness or unsupported element:** The correction from back-calculated untreated LDL-C to measured LDL-C moved performance in CALON-C's favour (+0.032 to +0.070). This must be presented transparently.
3. **Evidence check:** Model evaluation standards require scoring published tools exactly as defined in primary literature (Riley RD et al., *BMJ*, 2024, doi:10.1136/bmj-2023-078320).
4. **Required improvement:** Highlight that adhering to published measured LDL-C syntax is the strict primary implementation.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Methods—Comparator implementation ¶3 (FH-Risk-Score)
1. **Current claim:** FH-Risk-Score was restricted to age ≤65 years per derivation chart bounds.
2. **Weakness or unsupported element:** Excluding carriers >65 years reduces evaluable sample size but preserves scoring fidelity.
3. **Evidence check:** FH-Risk-Score derivation paper (Paquette M et al., *Arterioscler Thromb Vasc Biol*, 2021, doi:10.1161/ATVBAHA.121.316106).
4. **Required improvement:** Retain age gate.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Methods—Comparator implementation ¶4 (Montreal-FH-SCORE)
1. **Current claim:** Montreal-FH-SCORE used ever smoking and was evaluated purely as a risk-ranking instrument for incident events.
2. **Weakness or unsupported element:** Montreal was derived against prevalent disease; using it for incident ranking tests cross-estimand transport.
3. **Evidence check:** Montreal-FH-SCORE validation (Paquette M et al., *J Clin Lipidol*, 2017, doi:10.1016/j.jacl.2017.07.008).
4. **Required improvement:** Emphasize that Montreal comparison evaluates ranking capacity across different outcome designs.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Methods—Comparator implementation ¶5 (Lp(a) handling)
1. **Current claim:** UK Biobank Lp(a) in nmol/L was converted to mg/dL using a 2.15 divisor for comparator threshold evaluation; missing inputs led to exclusion rather than favorable imputation.
2. **Weakness or unsupported element:** The 2.15 divisor is an approximation subject to isoform size variation.
3. **Evidence check:** Lp(a) measurement conversion challenges (Sniderman AD et al., *JAMA Cardiol*, 2019, doi:10.1001/jamacardio.2019.3780).
4. **Required improvement:** Explicitly state that the 2.15 divisor is an operational assumption.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Methods—Head-to-head comparisons and multiplicity ¶1
1. **Current claim:** Paired cluster bootstrap resampling (2,000 draws) evaluated differences in C-statistics on identical complete-input subsets.
2. **Weakness or unsupported element:** Standard statistically sound approach for model comparison.
3. **Evidence check:** TRIPOD+AI Item 15b (Collins GS et al., *BMJ*, 2024, doi:10.1136/bmj-2023-078378).
4. **Required improvement:** Retain paired bootstrap methodology.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Methods—Head-to-head comparisons and multiplicity ¶2
1. **Current claim:** Holm adjustment controlled family-wise error across six confirmatory comparisons (3 comparators x 2 horizons [full, 5-year] in UK Biobank).
2. **Weakness or unsupported element:** Rigorous multiplicity control.
3. **Evidence check:** Multiplicity adjustment in prognostic model comparisons (Riley RD et al., *BMJ*, 2024, doi:10.1136/bmj-2023-078320).
4. **Required improvement:** Retain primary confirmatory family declaration.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Methods—Calibration, model equation, and transport ¶1
1. **Current claim:** Raw-unit baseline survival and linear predictor coefficients were provided for 5- and 10-year risk calculation.
2. **Weakness or unsupported element:** Absolute risk equations are valid only where baseline hazard is representative.
3. **Evidence check:** Calibration transportability (Debray TPA et al., *J Clin Epidemiol*, 2015; historical context).
4. **Required improvement:** Explicitly restrict baseline survival usage to internal evaluation.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Methods—Calibration, model equation, and transport ¶2
1. **Current claim:** Calibration was assessed via slope, expected:observed (E:O) ratio, Brier score, and decile plots within development data.
2. **Weakness or unsupported element:** The author response correctly withdrew external calibration claims pending out-of-fold baseline estimation.
3. **Evidence check:** PROBAST calibration assessment standards (Wolff RF et al., *Ann Intern Med*, 2019, doi:10.7326/M18-1376).
4. **Required improvement:** Label all calibration figures and text strictly as "internal calibration".
5. **Suggested replacement wording:** Maintain current prose with explicit internal labeling.
6. **Severity:** `MODERATE`.

#### Methods—Calibration, model equation, and transport ¶3
1. **Current claim:** Reciprocal transport evaluated frozen equations applied without refitting across cohorts.
2. **Weakness or unsupported element:** Must avoid calling Wales an independent validation cohort.
3. **Evidence check:** External validation terminology standards (Riley RD et al., *BMJ*, 2024, doi:10.1136/bmj-2023-078320).
4. **Required improvement:** Use "reciprocal setting transport" throughout.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Methods—Proportional hazards, competing risk, and sensitivity analyses ¶1
1. **Current claim:** Schoenfeld residuals assessed proportional hazards, and Aalen-Johansen estimates accounted for competing risk of death.
2. **Weakness or unsupported element:** The UK Biobank competing risk script failed to execute due to code errors, leaving competing risks evaluated only in Wales.
3. **Evidence check:** Competing risk analysis in cardiovascular risk models (Riley RD et al., *BMJ*, 2024, doi:10.1136/bmj-2023-078320).
4. **Required improvement:** State clearly in Methods that UK Biobank competing risk analysis was unexecuted due to pipeline failure.
5. **Suggested replacement wording:** "Proportional hazards were evaluated using Schoenfeld residual tests. Cause-specific hazards and Aalen–Johansen cumulative incidence were planned to account for competing mortality; however, the UK Biobank competing-risk pipeline failed to execute due to dataset schema discrepancies, leaving competing risks evaluated only in the Welsh cohort."
6. **Severity:** `FATAL`.

#### Methods—Proportional hazards, competing risk, and sensitivity analyses ¶2
1. **Current claim:** Welsh Aalen-Johansen analysis executed with 35 competing deaths.
2. **Weakness or unsupported element:** Correct execution in Welsh subset.
3. **Evidence check:** Competing risk estimation framework.
4. **Required improvement:** Retain Welsh competing risk reporting.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Methods—Proportional hazards, competing risk, and sensitivity analyses ¶3
1. **Current claim:** Sensitivity analyses tested Lp(a)-omitted comparators, alternative lipid factors, dated-only predictors, and event date attribution.
2. **Weakness or unsupported element:** Censoring ambiguous event dates at baseline creates informative censoring.
3. **Evidence check:** Informative censoring bias (Riley RD et al., *BMJ*, 2024, doi:10.1136/bmj-2023-078320).
4. **Required improvement:** Clarify that date-attribution restriction is an exploratory sensitivity, not a primary outcome definition.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Methods—Grey-zone and subgroup analyses ¶1
1. **Current claim:** An ancillary grey-zone analysis evaluated Lp(a) and log(apoB/LDL-C) additions within a 5%–20% 10-year risk band using an earlier model generation (CALON-F).
2. **Weakness or unsupported element:** Evaluating biomarker enhancers on a superseded model architecture (CALON-F) cannot prove or disprove biomarker utility for CALON-C.
3. **Evidence check:** Predictor addition and reclassification standards (Collins GS et al., *BMJ*, 2024, doi:10.1136/bmj-2023-078378).
4. **Required improvement:** Re-label this analysis strictly as an exploratory predecessor experiment that does not apply to CALON-C.
5. **Suggested replacement wording:** "An ancillary grey-zone analysis evaluated whether adding Lp(a), log(apoB/LDL-C), or both improved discrimination among UK Biobank carriers falling within a 5%–20% predicted 10-year risk band. This exploratory analysis utilized the predecessor CALON-F model structure and does not represent a validation of CALON-C."
6. **Severity:** `MAJOR`.

#### Methods—Grey-zone and subgroup analyses ¶2
1. **Current claim:** Subgroup outputs from earlier generations were present in the repository, but no corrected CALON-C subgroup table was available.
2. **Weakness or unsupported element:** Reporting gap: missing interaction tests and subgroup analyses for the primary model.
3. **Evidence check:** TRIPOD+AI Item 13 (Collins GS et al., *BMJ*, 2024, doi:10.1136/bmj-2023-078378).
4. **Required improvement:** Re-run and generate a verified subgroup table with formal interaction p-values for CALON-C.
5. **Suggested replacement wording:** Maintain current placeholder declaration until code is re-executed.
6. **Severity:** `MAJOR`.

#### Methods—Literature verification ¶1
1. **Current claim:** Citation verification involved primary PDF checks, structured PubMed queries up to 16 August 2026, and Crossref DOI verification.
2. **Weakness or unsupported element:** Must verify that pre-2016 citations are segregated into historical notes.
3. **Evidence check:** Systematic search standards.
4. **Required improvement:** Retain citation verification protocol.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

---

### Results

#### Results—Study populations ¶1
1. **Current claim:** UK Biobank development cohort comprised 3,209 carriers, 289 events, median age 57.1 years, 43.4% male, with cases showing higher age, male prevalence, hypertension, diabetes, and untreated non-HDL-C.
2. **Weakness or unsupported element:** Clinical risk factors (hypertension SMD 0.471, diabetes SMD 0.381) showed larger baseline separation between cases and non-cases than non-HDL-C (SMD 0.269) or remnant cholesterol (SMD 0.320).
3. **Evidence check:** Baseline risk factor distributions in population FH cohorts (Trinder M et al., *JAMA Cardiol*, 2020, doi:10.1001/jamacardio.2019.5954).
4. **Required improvement:** Highlight that baseline clinical risk factor differences matched or exceeded lipid differences.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Results—Study populations ¶2
1. **Current claim:** Corrected All-Wales risk set contained 1,169 participants and 102 events, but corrected Welsh baseline Table 1 and follow-up tables were absent from source files.
2. **Weakness or unsupported element:** Fatal reporting gap: manuscript text references 1,169/102 Welsh frame, but Table 1 presents no Welsh data, and descriptive files retain pre-rescue 1,159/92 values.
3. **Evidence check:** STROBE / RECORD cohort reporting guidelines (Benchimol EI et al., *PLoS Med*, 2015; historical context).
4. **Required improvement:** Generate and publish complete corrected Welsh Table 1 baseline characteristics for the 1,169/102 frame.
5. **Suggested replacement wording:** "The corrected All-Wales risk set comprised 1,169 genotype-positive participants and 102 events (51 by 5 years, 75 by 10 years). Complete baseline characteristics for this corrected Welsh frame are presented in Table 1."
6. **Severity:** `FATAL`.

#### Results—Predictor-level associations in UK Biobank ¶1
1. **Current claim:** Diabetes (HR 2.120, 95% CI 1.610–2.793), male sex (HR 1.702), and hypertension (HR 1.610) had the strongest adjusted associations, whereas lipid terms were non-significant.
2. **Weakness or unsupported element:** None. Honest reporting of multivariable hazard ratios.
3. **Evidence check:** Multivariable predictor associations in secondary/primary FH cohorts (Paquette M et al., *Arterioscler Thromb Vasc Biol*, 2021, doi:10.1161/ATVBAHA.121.316106).
4. **Required improvement:** Reinforce that hazard ratios reflect predictive multivariable associations, not causal effects.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Results—Predictor-level associations in UK Biobank ¶2
1. **Current claim:** CALON-C added +0.041 in C-statistic over age/sex; clinical risk factors added +0.033, leaving ~+0.008 attributable to lipid terms.
2. **Weakness or unsupported element:** Demonstrates that discrimination gains are heavily driven by conventional risk factors rather than complex lipid modeling.
3. **Evidence check:** Incremental value of lipid parameters over clinical risk scores (Akyea RK et al., *BJGP Open*, 2020, doi:10.3399/bjgpopen20X101114).
4. **Required improvement:** Maintain transparent breakdown of discrimination increment.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Results—Internal discrimination ¶1
1. **Current claim:** UK Biobank out-of-fold Harrell C was 0.7081 (full), 0.7043 (10-yr), 0.7254 (5-yr); optimism-corrected C was 0.7095 (full), 0.7079 (10-yr), 0.7336 (5-yr).
2. **Weakness or unsupported element:** Internal validation estimates are robust and show minimal optimism (<0.012).
3. **Evidence check:** Internal validation methodology (Riley RD et al., *BMJ*, 2024, doi:10.1136/bmj-2023-078319).
4. **Required improvement:** Retain internal discrimination metrics.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Results—Internal discrimination ¶2
1. **Current claim:** Pre-correction Welsh internal discrimination showed optimism-corrected C of 0.7653 (full), 0.7605 (10-yr), 0.7590 (5-yr), stated as unchanged post-rescue but un-updated in output files.
2. **Weakness or unsupported element:** Data pipeline mismatch: narrative text claims discrimination was unchanged after adding 10 events, but no synchronised post-rescue discrimination file exists.
3. **Evidence check:** Data integrity and pipeline verification standards.
4. **Required improvement:** Re-calculate and report verified Welsh post-rescue discrimination statistics from a single automated script.
5. **Suggested replacement wording:** "In the corrected All-Wales frame (1,169 participants, 102 events), family-cluster optimism-corrected C-statistic was [insert regenerated C-stat] over full follow-up."
6. **Severity:** `FATAL`.

#### Results—Head-to-head comparison with published FH instruments ¶1
1. **Current claim:** In UK Biobank full follow-up, CALON-C outperformed SAFEHEART-RE (delta +0.070, 95% CI 0.036–0.104; Holm p=0.0003) and Montreal-FH-SCORE (+0.032, 95% CI 0.011–0.055; Holm p=0.0179), but tied FH-Risk-Score (+0.015, 95% CI −0.011 to 0.040; Holm p=0.5018).
2. **Weakness or unsupported element:** Correct evaluation on complete-input subsets. The tie with FH-Risk-Score must be emphasized equally with the wins.
3. **Evidence check:**
   - SAFEHEART-RE (Pérez de Isla L et al., *Circulation*, 2017, doi:10.1161/CIRCULATIONAHA.116.024541).
   - FH-Risk-Score (Paquette M et al., *Arterioscler Thromb Vasc Biol*, 2021, doi:10.1161/ATVBAHA.121.316106).
4. **Required improvement:** Ensure balanced emphasis on both significant differences and statistical ties.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Results—Head-to-head comparison with published FH instruments ¶2
1. **Current claim:** Correcting SAFEHEART-RE input syntax to measured LDL-C increased the discrimination delta from +0.032 to +0.070 in CALON-C's favour.
2. **Weakness or unsupported element:** Methodological rigor in scoring comparators per primary publication instructions.
3. **Evidence check:** Comparator scoring fidelity (Riley RD et al., *BMJ*, 2024, doi:10.1136/bmj-2023-078320).
4. **Required improvement:** Retain explanation of syntax impact.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Results—Head-to-head comparison with published FH instruments ¶3
1. **Current claim:** At 5-year follow-up, nominal C-statistic differences vs SAFEHEART-RE (+0.081) and Montreal (+0.044) lost statistical significance post-Holm correction (p=0.0560 and p=0.1413).
2. **Weakness or unsupported element:** Critical finding: no 5-year superiority claim can be made.
3. **Evidence check:** Multiplicity control in clinical trials and prediction model validation (Riley RD et al., *BMJ*, 2024, doi:10.1136/bmj-2023-078320).
4. **Required improvement:** Retain explicit statement withdrawing 5-year superiority claims.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Results—Head-to-head comparison with published FH instruments ¶4
1. **Current claim:** Head-to-head comparisons in Wales were non-estimable for SAFEHEART-RE (1 event) and FH-Risk-Score (6 events) due to severe missingness in Lp(a) and BMI; Montreal tied CALON-C (+0.033, 95% CI −0.014 to 0.090).
2. **Weakness or unsupported element:** Highlights operational non-evaluability of complex scores in clinical registries, but prevents external comparative benchmarking.
3. **Evidence check:** Real-world EHR missingness limitations (Akyea RK et al., *BJGP Open*, 2020, doi:10.3399/bjgpopen20X101114).
4. **Required improvement:** Frame non-evaluability as an implementation finding regarding biomarker complexity.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MODERATE`.

#### Results—Head-to-head comparison with published FH instruments ¶5
1. **Current claim:** Across all strict and Lp(a)-omitted cells, no comparator significantly outperformed CALON-C, but this does not establish formal non-inferiority.
2. **Weakness or unsupported element:** Proper statistical boundary: lack of significant inferiority is not proof of non-inferiority without pre-specified margins.
3. **Evidence check:** Non-inferiority testing methodology.
4. **Required improvement:** Retain qualification.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Results—Calibration and model equation ¶1
1. **Current claim:** Internal 10-year calibration in UK Biobank showed slope 1.101 (95% CI 0.884–1.318), E:O ratio 1.008 (0.883–1.153), and scaled Brier score 3.3%.
2. **Weakness or unsupported element:** Acceptable internal calibration, but cannot be generalized outside UK Biobank.
3. **Evidence check:** Internal vs external calibration assessment (Wolff RF et al., *Ann Intern Med*, 2019, doi:10.7326/M18-1376).
4. **Required improvement:** Retain internal calibration label.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Results—Calibration and model equation ¶2
1. **Current claim:** Calibration metrics reflect internal development fit only; external calibration language was explicitly withdrawn pending independent out-of-fold validation.
2. **Weakness or unsupported element:** Transparent boundary setting.
3. **Evidence check:** PROBAST Item 4 (Wolff RF et al., *Ann Intern Med*, 2019, doi:10.7326/M18-1376).
4. **Required improvement:** Retain disclaimer.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Results—Calibration and model equation ¶3
1. **Current claim:** Model coefficients and raw-unit equations are published, with worked low-risk (0.78% 5-yr) and high-risk (15.99% 5-yr) examples provided for arithmetic verification.
2. **Weakness or unsupported element:** Worked examples verify code, not clinical actionability.
3. **Evidence check:** Model presentation standards (Collins GS et al., *BMJ*, 2024, doi:10.1136/bmj-2023-078378).
4. **Required improvement:** Retain worked examples with verification disclaimer.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Results—Reciprocal transport ¶1
1. **Current claim:** Frozen UK Biobank equation ranked All-Wales participants with C=0.7252; frozen Welsh equation ranked UK Biobank with C=0.6600.
2. **Weakness or unsupported element:** Asymmetric transport (C=0.725 vs C=0.660) reflects case-mix differences, outcome ascertainment, and un-timed baseline variables in Wales.
3. **Evidence check:** Transportability asymmetry across clinical settings (Riley RD et al., *BMJ*, 2024, doi:10.1136/bmj-2023-07820).
4. **Required improvement:** Emphasize that transport asymmetry highlights setting heterogeneity.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MODERATE`.

#### Results—Reciprocal transport ¶2
1. **Current claim:** Welsh cohort fit dropped diabetes and smoking due to low event counts (<10 events per cell), yielding a 7-term model.
2. **Weakness or unsupported element:** Model refitting in Wales yielded a different 7-term equation, making reverse transport an evaluation of a distinct model structure.
3. **Evidence check:** Model refitting vs frozen transport rules (Collins GS et al., *BMJ*, 2024, doi:10.1136/bmj-2023-078319).
4. **Required improvement:** Explicitly state that the single transportable CALON-C model is the 9-term UK Biobank equation applied to Wales.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MODERATE`.

#### Results—Proportional hazards and competing risk ¶1
1. **Current claim:** Proportional hazards held across all 16 tested terms (p>0.05).
2. **Weakness or unsupported element:** None.
3. **Evidence check:** Cox proportional hazards assumption testing.
4. **Required improvement:** Retain PH test results.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Results—Proportional hazards and competing risk ¶2
1. **Current claim:** Welsh Aalen-Johansen 10-year cumulative incidence was 11.97% with 35 competing deaths; UK Biobank competing risk analysis failed to execute.
2. **Weakness or unsupported element:** Unexecuted UK Biobank competing risk analysis is a fatal reporting gap.
3. **Evidence check:** TRIPOD+AI Item 18 (Collins GS et al., *BMJ*, 2024, doi:10.1136/bmj-2023-078378).
4. **Required improvement:** Fix data schema and execute UK Biobank competing risk cumulative incidence pipeline before resubmission.
5. **Suggested replacement wording:** "In All-Wales, 10-year Aalen-Johansen ASCVD cumulative incidence was 11.97% (35 competing deaths). In UK Biobank, execution of the competing-risk pipeline will be reported upon schema resolution."
6. **Severity:** `FATAL`.

#### Results—Missing data and comparator evaluability ¶1
1. **Current claim:** Variable missingness in UK Biobank reached 12.4% for non-HDL-C and 22.5% for Lp(a); Welsh missingness reached 54.5% for BMI and 41.6% for diabetes.
2. **Weakness or unsupported element:** Explains why complex models fail in real-world EHR environments.
3. **Evidence check:** Missing data reporting in EHR cohorts (Akyea RK et al., *BJGP Open*, 2020, doi:10.3399/bjgpopen20X101114).
4. **Required improvement:** Retain detailed missingness breakdown.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Results—Grey-zone analysis ¶1
1. **Current claim:** In 1,685 UK Biobank carriers within 5%–20% predicted 10-year risk, adding Lp(a) (delta C −0.0038), apoB/LDL-C (+0.0146), or both (+0.0118) produced no significant discrimination gain.
2. **Weakness or unsupported element:** Predecessor model experiment (CALON-F). Must not be construed as a decision-curve reclassification claim for CALON-C.
3. **Evidence check:** Incremental value of Lp(a) and apoB in intermediate risk (Sniderman AD et al., *JAMA Cardiol*, 2019, doi:10.1001/jamacardio.2019.3780).
4. **Required improvement:** Retain negative biomarker finding with explicit caveat regarding predecessor model status.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MODERATE`.

#### Results—Grey-zone analysis ¶2
1. **Current claim:** ApoB/LDL-C ratio was associated with ASCVD within the grey zone (HR 1.154 per SD, 95% CI 1.027–1.295) despite failing to improve discrimination.
2. **Weakness or unsupported element:** Key epidemiological lesson: statistically significant multivariable association does not guarantee improved risk discrimination.
3. **Evidence check:** Association vs discrimination distinction in biomarkers (Collins GS et al., *BMJ*, 2024, doi:10.1136/bmj-2023-078319).
4. **Required improvement:** Retain association vs discrimination distinction.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Results—Subgroups ¶1
1. **Current claim:** Corrected CALON-C subgroup estimates and formal interaction tests were absent from source files.
2. **Weakness or unsupported element:** Major reporting gap under TRIPOD+AI Item 13.
3. **Evidence check:** Subgroup analysis standards (Collins GS et al., *BMJ*, 2024, doi:10.1136/bmj-2023-078378).
4. **Required improvement:** Re-run subgroup interaction pipeline across age, sex, and diabetes strata before resubmission.
5. **Suggested replacement wording:** Maintain placeholder statement until execution.
6. **Severity:** `MAJOR`.

---

### Discussion

#### Discussion—Principal findings ¶1
1. **Current claim:** CALON-C demonstrated moderate internal discrimination, outperformed SAFEHEART-RE and Montreal-FH-SCORE over full follow-up, tied FH-Risk-Score, and showed asymmetric reciprocal transport without establishing independent validation.
2. **Weakness or unsupported element:** Balanced summary of principal findings.
3. **Evidence check:**
   - SAFEHEART-RE (Pérez de Isla L et al., *Circulation*, 2017, doi:10.1161/CIRCULATIONAHA.116.024541).
   - FH-Risk-Score (Paquette M et al., *Arterioscler Thromb Vasc Biol*, 2021, doi:10.1161/ATVBAHA.121.316106).
4. **Required improvement:** Retain summary.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Discussion—Principal findings ¶2
1. **Current claim:** Findings are narrower than initially hypothesized but credible: CALON-C does not beat every comparator, lacks 5-year superiority, and shows no head-to-head win in Wales.
2. **Weakness or unsupported element:** Highly commendable scientific self-restraint.
3. **Evidence check:** Reporting objectivity standards in prediction modeling.
4. **Required improvement:** Retain honest self-appraisal.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Discussion—What is genuinely new ¶1
1. **Current claim:** Novelty is incremental and methodological rather than paradigm-shifting, as FH risk modeling and UK Biobank analyses have extensive precedent.
2. **Weakness or unsupported element:** Accurate placement within existing literature.
3. **Evidence check:**
   - REFERCHOL study (Gallo A et al., *Atherosclerosis*, 2020, doi:10.1016/j.atherosclerosis.2020.06.011).
   - English routine care validation (McKay AJ et al., *Atherosclerosis*, 2022, doi:10.1016/j.atherosclerosis.2022.07.011).
   - Australian validation (Tamehri Zadeh SS et al., *Atherosclerosis*, 2026, doi:10.1016/j.atherosclerosis.2026.120799).
4. **Required improvement:** Maintain proper literature attribution.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Discussion—What is genuinely new ¶2
1. **Current claim:** The defensible contribution is the common-data, comparator-faithful evaluation of CALON-C against three published instruments on identical complete-input subsets, coupled with reciprocal setting transport.
2. **Weakness or unsupported element:** Accurately states residual novelty while avoiding overblown priority claims.
3. **Evidence check:** Methodological comparative standards (Riley RD et al., *BMJ*, 2024, doi:10.1136/bmj-2023-078320).
4. **Required improvement:** Retain precise residual novelty framing.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Discussion—Comparison with established FH risk instruments ¶1 (SAFEHEART-RE)
1. **Current claim:** SAFEHEART-RE performed strongly in its derivation registry (C=0.81–0.85) but dropped to 0.67–0.78 in external routine care, explaining why CALON-C gained a +0.070 advantage in an incident primary-prevention frame where measured LDL-C was treatment-suppressed.
2. **Weakness or unsupported element:** Sound clinical explanation of why SAFEHEART-RE underperformed in population primary prevention.
3. **Evidence check:**
   - SAFEHEART derivation (Pérez de Isla L et al., *Circulation*, 2017, doi:10.1161/CIRCULATIONAHA.116.024541).
   - English validation (McKay AJ et al., *Atherosclerosis*, 2022, doi:10.1016/j.atherosclerosis.2022.07.011).
4. **Required improvement:** Retain contextual explanation.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Discussion—Comparison with established FH risk instruments ¶2 (Montreal-FH-SCORE)
1. **Current claim:** Montreal-FH-SCORE was derived against prevalent ASCVD, so its comparison against CALON-C evaluates cross-estimand risk ranking rather than direct equivalence.
2. **Weakness or unsupported element:** Appropriate methodological qualification.
3. **Evidence check:** Montreal score derivation (Paquette M et al., *J Clin Lipidol*, 2017, doi:10.1016/j.jacl.2016.10.004).
4. **Required improvement:** Retain cross-estimand framing.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Discussion—Comparison with established FH risk instruments ¶3 (FH-Risk-Score)
1. **Current claim:** FH-Risk-Score was the strongest comparator, and its statistical tie with CALON-C demonstrates that routine data can recover similar ranking capacity without requiring Lp(a).
2. **Weakness or unsupported element:** Must acknowledge that FH-Risk-Score included 499 UK Biobank participants during derivation.
3. **Evidence check:** FH-Risk-Score derivation (Paquette M et al., *Arterioscler Thromb Vasc Biol*, 2021, doi:10.1161/ATVBAHA.121.316106).
4. **Required improvement:** Reiterate that potential sample overlap prevents drawing definitive external non-inferiority conclusions.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Discussion—Comparison with established FH risk instruments ¶4 (Guideline synthesis)
1. **Current claim:** 2026 ACC/AHA dyslipidaemia guidelines emphasize that FH scores remain under-validated for long-term clinical decisions.
2. **Weakness or unsupported element:** Direct alignment with top-tier guideline consensus.
3. **Evidence check:** 2026 ACC/AHA Dyslipidaemia Guideline (Blumenthal RS et al., *Circulation*, 2026, doi:10.1161/CIR.0000000000001423).
4. **Required improvement:** Maintain guideline synthesis.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Discussion—Routine-panel parsimony and global scalability ¶1
1. **Current claim:** CALON-C's main advantage is data availability, using ordinary lipids and clinical factors accessible globally.
2. **Weakness or unsupported element:** Parsimony is an operational advantage only if discrimination and calibration are preserved.
3. **Evidence check:** Global FH care gaps (Vallejo-Vaz AJ et al., *Atherosclerosis*, 2018, doi:10.1016/j.atherosclerosis.2018.08.051).
4. **Required improvement:** Retain parsimony discussion while noting calibration trade-offs.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Discussion—Routine-panel parsimony and global scalability ¶2
1. **Current claim:** Implementation failures of SAFEHEART-RE and FH-Risk-Score in All-Wales illustrate that complex biomarker requirements cause real-world non-evaluability.
2. **Weakness or unsupported element:** Powerful real-world implementation finding.
3. **Evidence check:** EHR data missingness in primary care (Akyea RK et al., *BJGP Open*, 2020, doi:10.3399/bjgpopen20X101114).
4. **Required improvement:** Retain implementation argument.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Discussion—Why the lipid terms did not dominate ¶1
1. **Current claim:** Weak multivariable lipid hazard ratios do not contradict the causal role of LDL, but reflect restricted lipid ranges and statin therapy in selected adult carrier cohorts.
2. **Weakness or unsupported element:** Standard epidemiological distinction between causal etiology and multivariable risk prediction.
3. **Evidence check:** Causal LDL evidence (Ference BA et al., *Eur Heart J*, 2017, doi:10.1093/eurheartj/ehx144); LDL exposure duration (Domanski MJ et al., *J Am Coll Cardiol*, 2020, doi:10.1016/j.jacc.2020.07.059).
4. **Required improvement:** Retain distinction between causal effect and predictive discrimination.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Discussion—Why the lipid terms did not dominate ¶2
1. **Current claim:** Conventional clinical risk factors (hypertension, diabetes, smoking) accounted for +0.033 of the +0.041 C-statistic gain over age/sex, leaving +0.008 for lipid terms.
2. **Weakness or unsupported element:** Honest reporting of predictor contribution breakdown.
3. **Evidence check:** Incremental discrimination studies in FH (Paquette M et al., *J Clin Lipidol*, 2017, doi:10.1016/j.jacl.2016.10.004).
4. **Required improvement:** Retain quantitative breakdown.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Discussion—Ascertainment, selection, and UK Biobank representativeness ¶1
1. **Current claim:** UK Biobank is subject to healthy-volunteer selection bias (5.5% response rate), altering baseline event rates and risk factor associations.
2. **Weakness or unsupported element:** Crucial limitation for external generalisability.
3. **Evidence check:** UK Biobank participation bias (Fry A et al., *Am J Epidemiol*, 2017, doi:10.1093/aje/kwx246; van Alten S et al., *Int J Epidemiol*, 2024, doi:10.1093/ije/dyae054; Schoeler T et al., *Nat Hum Behav*, 2023, doi:10.1038/s41562-023-01579-9).
4. **Required improvement:** Retain selection bias critique.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Discussion—Ascertainment, selection, and UK Biobank representativeness ¶2
1. **Current claim:** Unadjudicated `ldlr_carrier` status in UK Biobank showed only +0.15 to +0.23 mmol/L untreated non-HDL-C elevation over non-carriers, reflecting carrier definition breadth or phenotype attenuation.
2. **Weakness or unsupported element:** Explains why population carriers differ from severe clinic FH phenotypes.
3. **Evidence check:** Monogenic vs polygenic FH expression (Trinder M et al., *JAMA Cardiol*, 2020, doi:10.1001/jamacardio.2019.5954); Population screening yield (Gidding SS et al., *J Am Heart Assoc*, 2023, doi:10.1161/JAHA.123.030073).
4. **Required improvement:** Retain population carrier qualification.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Discussion—Ascertainment, selection, and UK Biobank representativeness ¶3
1. **Current claim:** Apparent internal calibration in UK Biobank cannot establish calibration in routine care, as seen in the English SAFEHEART validation where discrimination persisted but calibration failed.
2. **Weakness or unsupported element:** Precedent-backed critique of calibration transportability.
3. **Evidence check:** English routine care validation (McKay AJ et al., *Atherosclerosis*, 2022, doi:10.1016/j.atherosclerosis.2022.07.011).
4. **Required improvement:** Retain warning against assuming transported calibration.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Discussion—Survivor bias and age ¶1
1. **Current claim:** Middle-aged volunteer recruitment introduces survivor bias, where increasing age captures both cumulative exposure and survival resilience.
2. **Weakness or unsupported element:** Sound epidemiological reasoning regarding age splines in observational cohorts.
3. **Evidence check:** Selection mechanisms in biobank cohorts (Schoeler T et al., *Nat Hum Behav*, 2023, doi:10.1038/s41562-023-01579-9).
4. **Required improvement:** Retain survivor bias analysis.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Discussion—Survivor bias and age ¶2
1. **Current claim:** Survivor bias cannot be fully resolved by multivariable adjustment, requiring prospective family-based cohorts starting from childhood or early adulthood.
2. **Weakness or unsupported element:** Sound call for future longitudinal cohort design.
3. **Evidence check:** Longitudinal FH registries (Vallejo-Vaz AJ et al., *Atherosclerosis*, 2018, doi:10.1016/j.atherosclerosis.2018.08.051).
4. **Required improvement:** Retain future direction recommendations.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Discussion—Predictor timing in Wales ¶1
1. **Current claim:** Incompletely dated clinical predictors in All-Wales (recorded post-event or at last contact) represent a substantive limitation, cost ~0.030 in C-statistic, but reflect real-world registry constraints.
2. **Weakness or unsupported element:** Immortality and post-baseline predictor capture severely impair Welsh model transport validity.
3. **Evidence check:** PROBAST risk of bias in predictor timing (Wolff RF et al., *Ann Intern Med*, 2019, doi:10.7326/M18-1376).
4. **Required improvement:** State unequivocally that Welsh transport serves as an exploratory stress test rather than a formal validation.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `FATAL`.

#### Discussion—Predictor timing in Wales ¶2
1. **Current claim:** Removing undated fields changed C-statistic by 0.030, proving that baseline timing cannot be assumed without explicit prospective dates.
2. **Weakness or unsupported element:** Rigorous sensitivity bounding.
3. **Evidence check:** Predictor measurement timing standards (Collins GS et al., *BMJ*, 2024, doi:10.1136/bmj-2023-078319).
4. **Required improvement:** Retain sensitivity bound discussion.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Discussion—Calibration drift and directional but non-significant differences ¶1
1. **Current claim:** Calibration drift occurs when baseline hazard and case mix differ, so CALON-C cannot provide valid absolute risk probabilities outside UK Biobank.
2. **Weakness or unsupported element:** Essential caveat protecting against inappropriate clinical risk scoring.
3. **Evidence check:** External validation calibration principles (Riley RD et al., *BMJ*, 2024, doi:10.1136/bmj-2023-078320).
4. **Required improvement:** Retain absolute risk caveat.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Discussion—Calibration drift and directional but non-significant differences ¶2
1. **Current claim:** Directional point estimates favoring CALON-C over FH-Risk-Score do not justify clinical superiority or adoption without statistical significance post-adjustment.
2. **Weakness or unsupported element:** Proper statistical interpretation.
3. **Evidence check:** Multiplicity and inference rules in model benchmarking.
4. **Required improvement:** Retain tie interpretation.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Discussion—Lp(a), apoB, and the grey zone ¶1
1. **Current claim:** Excluding Lp(a) and apoB was a design choice for scalability, not a rejection of their biological importance, aligned with 2026 guidelines recommending baseline Lp(a) testing.
2. **Weakness or unsupported element:** Reconciles model parsimony with clinical guideline recommendations.
3. **Evidence check:** 2026 ACC/AHA Dyslipidaemia Guideline (Blumenthal RS et al., *Circulation*, 2026, doi:10.1161/CIR.0000000000001423); 2025 ESC/EAS Focused Update (Mach F et al., *Eur Heart J*, 2025, doi:10.1093/eurheartj/ehaf190).
4. **Required improvement:** Retain clinical guidelines context.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Discussion—Lp(a), apoB, and the grey zone ¶2
1. **Current claim:** Ancillary grey-zone results show that significant biomarker association (apoB/LDL-C HR 1.154) does not automatically yield discrimination improvement or reclassification gain.
2. **Weakness or unsupported element:** Must reinforce that grey-zone testing was conducted on predecessor model CALON-F.
3. **Evidence check:** Biomarker reclassification evaluation standards (Collins GS et al., *BMJ*, 2024, doi:10.1136/bmj-2023-078378).
4. **Required improvement:** Retain biomarker lesson with model version caveat.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Discussion—Competing risks and endpoint definition ¶1
1. **Current claim:** Non-execution of the UK Biobank competing risk script prevents absolute risk interpretation, as competing mortality can inflate Cox risk estimates in older cohorts.
2. **Weakness or unsupported element:** Correct self-identification of a critical technical gap.
3. **Evidence check:** Competing risk standards in prediction models (Riley RD et al., *BMJ*, 2024, doi:10.1136/bmj-2023-078320).
4. **Required improvement:** Require pipeline fix prior to publication.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `FATAL`.

#### Discussion—Competing risks and endpoint definition ¶2
1. **Current claim:** Endpoint heterogeneity (UK Biobank diagnostic-weighted vs Wales procedure-inclusive) requires future validation using harmonised MI, stroke, CV death, and revascularisation definitions.
2. **Weakness or unsupported element:** Sound discussion of outcome applicability limitations.
3. **Evidence check:** Harmonised outcome reporting standards (RECORD statement; historical context).
4. **Required improvement:** Retain endpoint harmonisation call.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Discussion—Ancestry and fairness ¶1
1. **Current claim:** Study cohorts were predominantly White European, preventing performance extrapolation to diverse ancestry groups.
2. **Weakness or unsupported element:** Crucial equity and generalisability limitation.
3. **Evidence check:** TRIPOD+AI Item 13/21 on algorithmic fairness and demographic representation (Collins GS et al., *BMJ*, 2024, doi:10.1136/bmj-2023-078378).
4. **Required improvement:** Retain ancestry limitation statement.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Discussion—Ancestry and fairness ¶2
1. **Current claim:** Future external validations must report performance, calibration, and net benefit stratified across sex, age, socioeconomic status, and self-reported ancestry.
2. **Weakness or unsupported element:** Aligns with modern AI/ML fairness standards in cardiology.
3. **Evidence check:** Algorithmic stratification in FH (Zamora A et al., *Eur Heart J Digit Health*, 2025, doi:10.1093/ehjdh/ztaf092).
4. **Required improvement:** Retain fairness recommendations.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Discussion—Overlap and leakage ¶1
1. **Current claim:** Temporal leakage was avoided, but potential overlap exists because 499 UK Biobank participants were included in the derivation of FH-Risk-Score.
2. **Weakness or unsupported element:** Transparent identification of potential comparator contamination.
3. **Evidence check:** External validation overlap rules (Riley RD et al., *BMJ*, 2024, doi:10.1136/bmj-2023-078320).
4. **Required improvement:** Retain overlap qualification.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Discussion—Overlap and leakage ¶2
1. **Current claim:** Definitive validation requires an untouched third cohort with a pre-locked protocol, frozen equation, and zero involvement in model tuning.
2. **Weakness or unsupported element:** Exact scientific requirement for confirming clinical utility.
3. **Evidence check:** Independent external validation standards (Collins GS et al., *BMJ*, 2024, doi:10.1136/bmj-2023-078319).
4. **Required improvement:** Retain call for independent third-cohort validation.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Discussion—Clinical implications ¶1
1. **Current claim:** The immediate contribution is methodological, establishing standards for comparator-faithful evaluation on identical complete-input sets with multiplicity control.
2. **Weakness or unsupported element:** Proper positioning of paper's primary impact.
3. **Evidence check:** Methodological reporting standards (Collins GS et al., *BMJ*, 2024, doi:10.1136/bmj-2023-078378).
4. **Required improvement:** Retain methodological implications.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Discussion—Clinical implications ¶2
1. **Current claim:** CALON-C is a candidate routine-data ranking tool for resource-constrained settings, but must never be used to withhold lipid-lowering therapy or de-risk FH patients.
2. **Weakness or unsupported element:** Essential clinical safety guidance.
3. **Evidence check:** 2026 ACC/AHA Dyslipidaemia Guideline (Blumenthal RS et al., *Circulation*, 2026, doi:10.1161/CIR.0000000000001423); 2025 ESC/EAS Focused Update (Mach F et al., *Eur Heart J*, 2025, doi:10.1093/eurheartj/ehaf190).
4. **Required improvement:** Retain clinical safety disclaimers.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Discussion—Strengths ¶1
1. **Current claim:** Strengths include incident design, complete-input head-to-head benchmarking, primary score syntax corrections, Holm adjustment, PH residual diagnostics, and explicit retraction of overclaims.
2. **Weakness or unsupported element:** Objective inventory of scientific strengths.
3. **Evidence check:** TRIPOD+AI adherence guidelines.
4. **Required improvement:** Retain strengths summary.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

#### Discussion—Limitations ¶1
1. **Current claim:** Limitations include lack of independent validation, empty UK Biobank `variant_id` fields, unsynchronised Welsh artefacts, unexecuted UK Biobank competing risks, ambiguous date attribution, unmeasured relatedness, internal-only calibration, missing subgroup tables, and European volunteer cohort selection.
2. **Weakness or unsupported element:** Comprehensive, highly transparent limitation inventory.
3. **Evidence check:** Standard prediction model limitation reporting.
4. **Required improvement:** Retain complete limitations list.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

---

### Conclusion

#### Conclusion ¶1
1. **Current claim:** CALON-C achieved moderate internal discrimination in UK Biobank *LDLR* carriers, outperformed SAFEHEART-RE and Montreal-FH-SCORE over full follow-up, tied FH-Risk-Score, and demonstrated reciprocal setting transport to Wales without establishing independent validation or clinical utility.
2. **Weakness or unsupported element:** Concise, balanced final synthesis.
3. **Evidence check:** TRIPOD+AI reporting guidelines (Collins GS et al., *BMJ*, 2024, doi:10.1136/bmj-2023-078378).
4. **Required improvement:** Retain conclusion prose.
5. **Suggested replacement wording:** Maintain current prose.
6. **Severity:** `MINOR`.

---

## WHOLE-MANUSCRIPT ANALYSES

### A. Novelty Map

```
+-----------------------------------------------------------------------------------+
| NOVELTY SPECTRUM & PRIORITY AUDIT                                                 |
+-----------------------------------------------------------------------------------+
| 1. GENUINELY NEW:                                                                 |
|    - First head-to-head complete-input comparison of CALON-C against exact            |
|      published specifications of SAFEHEART-RE, Montreal-FH-SCORE, and FH-Risk-Score |
|      in a population-based LDLR-carrier cohort.                                   |
|    - Exposure of severe operational non-evaluability of complex biomarker scores      |
|      (SAFEHEART-RE, FH-Risk-Score) in routine national clinical registries (Wales)  |
|      due to missing Lp(a) and BMI inputs.                                         |
|                                                                                   |
| 2. INCREMENTAL BUT USEFUL:                                                        |
|    - Demonstration that a 9-term equation using standard routine lipids and clinical   |
|      factors achieves discrimination comparable to FH-Risk-Score (delta C +0.015,     |
|      95% CI -0.011 to 0.040; Holm p=0.5018) without requiring Lp(a).                |
|    - Reciprocal setting transport testing of frozen equations between population      |
|      biobanks and clinical genetics registries.                                   |
|                                                                                   |
| 3. ALREADY ESTABLISHED:                                                           |
|    - Age, male sex, hypertension, diabetes, and smoking dominate near-term ASCVD      |
|      risk prediction in FH / LDLR carriers (Paquette 2017; Paquette 2021).        |
|    - SAFEHEART-RE suffers from substantial calibration drift when transported outside |
|      its primary derivation registry (McKay 2022; Gallo 2020).                    |
|    - UK Biobank healthy-volunteer selection distorts absolute risk rates (Fry 2017;  |
|      van Alten 2024).                                                             |
|                                                                                   |
| 4. UNSUPPORTED PRIORITY CLAIMS (MUST BE MODIFIED):                                |
|    - "First external validation of all three models": WITHDRAWN. (FH-Risk-Score used   |
|      499 UK Biobank participants during derivation; overlap unquantified).
