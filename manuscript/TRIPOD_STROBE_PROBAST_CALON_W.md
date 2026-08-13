# CALON-W — TRIPOD+AI, STROBE/RECORD and PROBAST reporting and risk-of-bias assessment

**Model:** CALON-W — an eight-term routinely-available-data model for atherosclerotic cardiovascular disease (ASCVD) in genetically defined familial hypercholesterolaemia (FH).
**Assessment date:** 11 August 2026.
**Assessor:** methods/reporting audit, independent of the analysts.
**Governance:** aggregate only. No participant rows, participant identifiers, family identifiers, variant coordinates or participant-level predictions appear in this document. Event-related cells below 10 are suppressed. `wales_clean_treatment_response.csv` was not opened.

> **Status of this document.** This is a *pre-submission* audit, not a completed reporting checklist for a finished manuscript. A CALON-W manuscript does not yet exist as a durable file; the "where addressed" column therefore names the artefact that currently carries the information, or names the section that must be written. An item is marked COMPLETE only where a durable artefact already satisfies it.

> **Material change on 11 August 2026.** An independent statistical QC completed after this audit was commissioned and **invalidated the UK Biobank arm** on the grounds of outcome-to-predictor temporality reversal (Section 1). The UK Biobank analysis is treated throughout as **RETRACTED**: its estimates are not reported as findings, and every checklist item that depended on it is marked NOT MET rather than PARTIAL. The study assessed below is therefore a **single-cohort development study with internal validation only**, in the All-Wales FH registry (PASS).

---

## 0. How to read this document

### 0.1 Status vocabulary

| Status | Meaning |
|---|---|
| **COMPLETE** | The requirement is met in full by an existing, durable artefact. |
| **PARTIAL** | Substantively addressed somewhere, but incomplete, undocumented in a citable place, or not yet in manuscript form. |
| **NOT MET** | Not addressed, or addressed in a way the known defects contradict. Includes everything touched by the UK Biobank leak. |
| **NOT APPLICABLE** | The item does not apply to this design. Where the guideline requires an explicit negative statement, that requirement is noted. |
| **PENDING QC** | Cannot be adjudicated until the two independent audits (statistics; provenance) return a verdict. |

### 0.2 Provenance of the checklist item text

Item numbering and content were retrieved from the source documents, not reconstructed from memory. Item wording below is **abbreviated in the assessor's words**; the authoritative wording is in the sources.

| Instrument | Source used | Structure retrieved |
|---|---|---|
| TRIPOD+AI | Collins GS, Moons KGM, Dhiman P, et al. *BMJ* 2024;385:e078378 (main paper, Table 2 and Table 3) and the TRIPOD+AI Expanded Checklist (Explanation & Elaboration Light), version 7 February 2024 | 27 main items, 52 numbered rows (1–27c); plus TRIPOD+AI for Abstracts, 13 items |
| STROBE (cohort) | STROBE Statement — checklist for cohort studies (official checklist PDF) | 22 items, 34 numbered rows including sub-items |
| RECORD | Benchimol EI, Smeeth L, Guttmann A, et al. *PLoS Med* 2015 — official RECORD checklist PDF (CC BY) | 13 extension items (1.1–22.1) |
| PROBAST | PROBAST tool, version 15 May 2019 (probast.org); Wolff RF, Moons KGM, Riley RD, et al. *Ann Intern Med* 2019 | 4 domains, 20 signalling questions for development (1.1–4.9), applicability per domain, overall judgement rules |

### 0.3 Headline status counts

| Instrument | COMPLETE | PARTIAL | NOT MET | NOT APPLICABLE | PENDING QC | Rows |
|---|---:|---:|---:|---:|---:|---:|
| TRIPOD+AI (main) | 0 | 18 | 27 | 7 | 0 | **52** |
| TRIPOD+AI for Abstracts | 0 | 0 | 12 | 0 | 1 | **13** |
| STROBE (cohort) | 0 | 14 | 17 | 2 | 1 | **34** |
| RECORD | 0 | 5 | 8 | 0 | 0 | **13** |

PROBAST, Wales development assessment — 20 signalling questions, answered on the tool's Y / PY / PN / N / NI scale (every question is phrased so that "yes" indicates absence of bias):

| Answer | Count | Questions |
|---|---:|---|
| Yes | 3 | 1.1, 3.3, 4.5 |
| Probably yes | 1 | 2.3 |
| Probably no | 7 | 2.2, 3.1, 3.2, 3.5, 4.2, 4.4, 4.6 |
| No | 8 | 1.2, 2.1, 3.4, 3.6, 4.1, 4.3, 4.7, 4.8 |
| Unassessable (PENDING QC) | 1 | 4.9 |

**No item on any reporting instrument is COMPLETE, and 15 of 20 PROBAST signalling questions flag potential bias.** That is the correct summary of the study's present state.

---

## 1. WHY THE UK BIOBANK ANALYSIS CANNOT BE REPORTED

*A retraction record. Each row is a stand-alone finding; each is individually sufficient to prevent reporting, and R1 is fatal on its own.*

| # | Finding | Detail | Consequence |
|---|---|---|---|
| **R1** | **Outcome precedes predictor measurement in 100% of cases — fatal temporality reversal** | Every prevalent-ASCVD event pre-dates the blood draw (median 6.6 y, IQR 3.8–11.6, maximum 55.6 y). Mechanism: `pre_lipid_source == "post_event_excluded"` is true for 100% of cases and 0% of non-cases, and `build_ukb`'s `pre_ldl.fillna(ldl_chem)` silently restores exactly those excluded post-event, on-treatment lipid values. | The model does not predict the outcome; it detects the metabolic and treatment consequences of the outcome. No analysis of this data configuration is reportable as prediction. |
| **R2** | **Same defect as a previous retraction in this programme** | Identical failure mode to the `pre_lipid_source` post-event leak that caused the CALON-D retraction on 6 August 2026. | A recurrence of a known, documented programme defect. Any submission would repeat a fault the group has already retracted for. |
| **R3** | **A single leaked variable outperforms the model** | Statin flag alone AUC 0.789 versus the full model 0.757 — statistically inseparable. Statin use in 94.7% of cases versus 36.9% of controls. | The apparent discrimination is treatment status, not risk. |
| **R4** | **Reverse causation is directly demonstrated** | Lower LDL-C predicts case status at AUC 0.784. | Confirms that the lipid signal runs backwards from treatment initiated after the event. |
| **R5** | **The flagship predictor is at chance** | Cumulative cholesterol (log[untreated LDL-C × age]) univariable AUC 0.5051. | The variable the model is built around contributes nothing in this cohort. |
| **R6** | **Both lipid coefficients carry impossible signs** | log(TG/HDL-C) −0.198; cumulative cholesterol −0.160. Higher lifetime cholesterol exposure predicting *lower* ASCVD in FH carriers is biologically impossible. | Sign incoherence confirms the fit is estimating treatment intensity, not atherogenic burden. |
| **R7** | **It is a 7-variable model, not 8** | UK Biobank minimum age is 40.1 y, so `age_sp18 = max(age − 18, 0)` equals `age − 18` for all 890 participants; r(age, age_sp18) = 1.0000000000. The knot was transplanted from Wales without an applicability check. | One declared predictor is an exact linear duplicate. Events-per-variable, model description and degrees of freedom are all misstated. |
| **R8** | **The reported AUC was seed-favourable** | Claimed 0.7605. Across 10 cross-validation seeds the QC obtained 0.7497–0.7596 — the claim sits **above the entire distribution**. At 10-fold × 8 repeats: 0.7566. | The headline number is not reproducible under re-seeding and is not a defensible point estimate. |
| **R9** | **Verdict labels are unstable and the effective sample is tiny** | The Montreal comparison flips 10 LOSS / 10 tie across bootstrap seeds and does not stabilise at B = 5000. Kish effective number of clusters 5.1 against a nominal 62; only 21 of 62 clusters contain any event; one cluster holds 42% of the cohort. | Win/tie/loss labels are seed artefacts. Cluster-bootstrap intervals are far wider than the nominal cluster count implies. |
| **R10** | **Estimand category error in every comparison** | Montreal-FH-SCORE, FH-Risk-Score and SAFEHEART-RE are **incident** risk models scored against a **prevalent** outcome. SAFEHEART-RE's 0.6555 exists only because it was fed treatment-contaminated back-calculated LDL-C; on clean measured LDL-C it is 0.5523, near chance. | The head-to-head comparison was never like-for-like. Comparator "defeats" are artefacts of the contaminated input. |
| **R11** | **Montreal was not faithfully implemented, and the verdict is anchor-dependent** | Implemented with z-anchors from the Welsh cohort rather than its published anchors: Welsh anchors 0.7785 versus UKB-internal anchors 0.7611. | Not an implementation of the published model. Any "we beat / tied Montreal" statement is conditional on an undeclared analyst choice. |
| **R12** | **The comparison was underpowered against its own reported effect** | Minimum detectable difference at 90% power is 0.076 for FH-Risk-Score; the reported FH-RS advantage is +0.059 — below its own detection threshold. | The study could not have detected the difference it reports. |
| **R13** | **Undocumented, inspection-driven specification change** | The HDL-C-for-diabetes swap between the Welsh and UK Biobank specifications was undocumented and followed inspection of UK Biobank performance. | Post-hoc, outcome-informed specification selection with no protocol amendment. |

**Disposition.** The UK Biobank arm is withdrawn. Its 890 participants, 57 prevalent events, 62 variant clusters, AUC 0.7605, and the 15 UK Biobank head-to-head comparisons (5 wins, 9 ties, 1 loss) **must not appear as results** in any manuscript, abstract, figure, table or supplement. Retaining them as a *methodological negative* — "a cross-sectional FH prediction analysis in which 100% of events preceded biomarker measurement, and what that does to apparent discrimination" — is legitimate and is the only defensible use of this material.

**Consequence for the study's headline claim.** The programme's stated result ("24 head-to-head comparisons — 6 wins, 17 ties, 1 loss") is no longer available. What survives is **9 Welsh comparisons: 1 win, 8 ties, 0 losses**, from a single cohort, unverified (Section 2.3), with no external validation of any kind.

---

## 2. The study as it now stands

### 2.1 The assessable object

| Element | Specification |
|---|---|
| Design | Retrospective cohort, prospective/incident estimand; model **development with internal validation only** |
| Cohort | All-Wales FH registry (PASS); genotype-confirmed carriers |
| Participants / events / clusters | 1,159 / 92 incident ASCVD / 711 family clusters |
| Exposure time | 6,841 person-years; median follow-up 4.24 y as briefed, **4.01 y** on independent reconstruction (unresolved discrepancy) |
| Model | Cox proportional hazards, penalizer 0.05, baseline hazard **stratified by ascertainment** (proband vs cascade) |
| Predictors (8 terms) | age; `age_sp18 = max(age − 18, 0)`; male sex; log(TG/HDL-C); ever smoking; hypertension; cumulative cholesterol = log(untreated LDL-C × age); HDL-C |
| Untreated LDL-C | measured / 0.70 where on lipid-lowering therapy at baseline (fixed divisor) |
| Internal validation | Repeated k-fold CV, families re-permuted per repeat; `IterativeImputer` fitted on the training fold only; paired ΔC with family-cluster bootstrap 95% CI |
| Comparators | Montreal-FH-SCORE, FH-Risk-Score, SAFEHEART-RE (published equations; adaptations apply) |
| Result | Wales C = 0.7587; 9 comparisons: 1 win, 8 ties, 0 losses |
| External validation | **None** |
| Calibration | **None performed** |
| Transport analysis | **None performed** |
| Binding programme rule observed | No published score, prior model, or linear predictor is an input — raw variables only. Confirmed for CALON-W. |

### 2.2 Why the Welsh arm is not invalidated by the UK Biobank leak

The Welsh arm anchors time-zero at a dated baseline lipid measurement, classifies each component event by its dated age, and excludes events at or before baseline. Predictors are therefore dated pre-baseline, and the R1 mechanism (post-event lipids restored by a `fillna`) does not apply. This is a genuine structural difference, not a presumption of innocence.

### 2.3 Why the Welsh arm is nonetheless UNVERIFIED

The checks that destroyed the UK Biobank arm **have not been run in Wales**. Specifically outstanding:

| Check | Status in Wales | Why it matters |
|---|---|---|
| Univariable AUC/C of cumulative cholesterol | **Not run** | R5 showed it at chance in the other cohort |
| Coefficient signs for log(TG/HDL-C) and cumulative cholesterol | **Not run / not reported** | R6 showed both reversed |
| Statin/treatment flag alone versus the full model | **Not run** | R3 showed a single leaked variable beating the model |
| Collinearity of `age` and `age_sp18` | **Not run** | R7: if the Welsh minimum baseline age exceeds 18, `age_sp18` is again an exact linear duplicate of age and CALON-W is a 7-term model in Wales too |
| Seed stability of C and of the win/tie/loss labels | **Not run** | R8, R9: the labels already shifted once when the CV configuration changed (10-fold × 8 repeats vs 5-fold × 4), so they sit near the decision boundary |
| Effective (Kish) number of family clusters | **Not run** | R9: nominal 711 families may correspond to a far smaller effective sample |
| Faithfulness of the comparator implementations | **Not established** | R10, R11: Montreal z-anchors were taken from the Welsh development cohort, i.e. from the very data in which it is being compared |

Until these return, **no Welsh number should be described as verified**, and the C = 0.7587 headline is provisional.

### 2.4 Defects of the Welsh arm that stand independently

1. **Informative censoring.** The censoring rule (age at death, else latest lipid/BMI record) excludes 659 otherwise-eligible genotype-positive participants, **including 10 with dated post-baseline ASCVD events**, solely for lacking a later clinic/BMI/death record. There is no administrative outcome-coverage end date.
2. **Differential recording of risk factors by event status.** Diabetes is present in 58% of the cohort but covers 77% of events; smoking 74% and 87%. Missingness is associated with the outcome, so a missing-at-random assumption is not tenable.
3. **Events per variable ≈ 11.5** (92 events / 8 terms), below conventional adequacy and without a Riley-type sample-size justification.
4. **Selection optimism.** Roughly 40 model specifications were explored across the programme; measured selection optimism in this dataset is **+0.0168 AUC**, uncorrected. HDL-C entered the specification post hoc, after an initial head-to-head loss (in the now-retracted cohort — so the change that produced the current predictor set was driven by data that is itself withdrawn).
5. **Lost provenance.** The Welsh cohort's original producing script is lost; the current build is a documented **near-reproduction** (untreated-LDL treated rate 7.1% versus an archived 11%).
6. **Internal inconsistency of reported discrimination.** Age + sex is reported as C = 0.7036 by the independent reconstruction and 0.7391 by `outputs/welsh_prospective_model.json`, under different CV configurations, against a CALON-W headline of 0.7587. Unreconciled.
7. **No durable artefact.** No script or results file in the package produces the 8-term CALON-W numbers. `code/12_welsh_prospective_model.py` and `outputs/welsh_prospective_model.json` implement the **predecessor** specification (with diabetes, without HDL-C).
8. **Standing HOLD.** `outputs/audit_2026_08_10/WELSH_PROSPECTIVE_VERIFICATION.md` placed the 1,159-person risk set under an explicit HOLD for prospective model fitting until the censor/risk-set repair is frozen, and specifically warned against fitting a model to the current risk set and carrying it into the repaired cohort. CALON-W was fitted to the held risk set.

---

## 3. TRIPOD+AI (Collins et al., BMJ 2024;385:e078378)

Applicability tags follow the source: **D** = model development, **E** = model evaluation. This study is a **development** study; the comparator scoring is an **evaluation** component, so E-tagged items are assessed against the comparator analyses where relevant.

### 3.1 Title and abstract

| Item | Requirement (abbreviated) | Status | Where addressed / what is missing |
|---|---|---|---|
| 1 (D;E) | Title identifies the study as developing or evaluating a multivariable prediction model, the target population, and the outcome predicted | **NOT MET** | Working title claims "two ascertainment settings" and a "head-to-head". With the UK Biobank arm retracted, one setting remains and the head-to-head reduces to 9 comparisons with 1 win. Title must state: development with internal validation, All-Wales genotype-confirmed FH registry, incident ASCVD, no external validation. |
| 2 (D;E) | Abstract addresses every item of the TRIPOD+AI for Abstracts checklist | **NOT MET** | No CALON-W abstract exists. See §3.9 for the item-level assessment of the 13-item abstract checklist. |

### 3.2 Introduction

| Item | Requirement (abbreviated) | Status | Where addressed / what is missing |
|---|---|---|---|
| 3a (D;E) | Healthcare context (diagnostic vs prognostic) and rationale for developing/evaluating, with references to existing models | **PARTIAL** | Context and the three comparators are set out in `SKELETON_CLAUDE.md` ¶1–¶3 and `MANUSCRIPT_SPEC_CLAUDE.md`. Missing: a justification for developing a **new** model when the surviving evidence is 8 ties and 1 win against three published scores in a single cohort. |
| 3b (D;E) | Target population, intended purpose in the care pathway, intended users | **NOT MET** | No stated care-pathway position, decision supported, or intended user. The retraction removes the second setting, so any purpose statement inherited from the two-cohort framing is void and must be rewritten for a Welsh specialist-registry population. |
| 3c (D;E) | Known health inequalities between sociodemographic groups in the target population | **NOT MET** | Absent. No ethnicity or deprivation description; the cohort is predominantly White European. Requires a referenced paragraph plus the cohort's own distribution. |
| 4 (D;E) | Study objectives, stating development, validation, or both | **NOT MET** | Objectives were written around reciprocal two-cohort comparison. Must now read: development of one model in one registry cohort, internal validation only, comparator evaluation secondary, no external validation, no calibration. |

### 3.3 Methods — data, participants, data preparation

| Item | Requirement (abbreviated) | Status | Where addressed / what is missing |
|---|---|---|---|
| 5a (D;E) | Sources of data separately for development and evaluation; rationale; representativeness | **PARTIAL** | Source snapshots with byte counts and SHA-256 in `outputs/audit_2026_08_10/OPEN_MODEL_SEARCH_RUN_META.json`; cohort definition in `WELSH_PROSPECTIVE_VERIFICATION.md`. Missing: representativeness of a specialist genotype-confirmed registry relative to the intended target population; explicit statement that the build is a near-reproduction of a lost script. |
| 5b (D;E) | Dates of participant data: accrual start and end; end of follow-up | **NOT MET** | No accrual window and **no administrative outcome-coverage end date** — this is the root of the informative-censoring defect. Median follow-up is disputed (4.24 y briefed vs 4.01 y reconstructed). |
| 6a (D;E) | Study setting, number and location of centres | **PARTIAL** | All-Wales registry identified; the number of contributing clinics/centres is not reported. |
| 6b (D;E) | Eligibility criteria | **PARTIAL** | The eight-step reconstruction (genotype-positive; dated baseline; exclude prevalent ASCVD; exclude outcome-positive without event age; require positive operational follow-up) is documented in the verification report. Missing from any manuscript, and the last step — which removes 659 participants including 10 with events — must be presented as an **eligibility criterion**, not a data-availability footnote. |
| 6c (D;E) | Treatments received and how handled in development/evaluation | **NOT MET** | Untreated LDL-C is back-calculated as measured/0.70 for baseline-treated participants using a fixed divisor. The dated rule yields only 7.1% treated against an archived 11% and an undated `OnTreatment` positivity of ~86%, so baseline treatment status is not credibly established. Treatment during follow-up is not addressed at all. |
| 7 (D;E) | Data pre-processing and quality checking, including whether similar across sociodemographic groups | **PARTIAL** | Variable construction, range checks and per-variable source columns are in `OPEN_MODEL_SEARCH_PROVENANCE.csv`; build logic in `code/12_welsh_prospective_model.py`. Missing: any check that pre-processing behaved similarly across sociodemographic groups, and the fact that recording itself differs by event status (2.4-2) is a data-quality finding that must be stated here. |

### 3.4 Methods — outcome and predictors

| Item | Requirement (abbreviated) | Status | Where addressed / what is missing |
|---|---|---|---|
| 8a (D;E) | Outcome definition, **time horizon**, how and when assessed, rationale, consistency across sociodemographic groups | **NOT MET** | Composite incident ASCVD is derived from component event ages (MI/ACS, PCI, CABG, angina, TIA, PVD). **No prediction time horizon is defined**, and none can be, because no baseline survival function is reported (item 22). Outcome ascertainment depends on continued clinic contact and is therefore not consistent across participants. |
| 8b (D;E) | If outcome assessment is subjective, qualifications and demographics of assessors | **NOT APPLICABLE** | Outcomes are routinely recorded registry fields; no adjudication was performed. The paper must state this explicitly rather than leave it silent. |
| 8c (D;E) | Actions to blind outcome assessment | **NOT APPLICABLE** | Retrospective registry extraction; blinding not possible. Must be stated, with the consequence flagged (PROBAST 3.5). |
| 9a (D) | Choice of initial predictors and any pre-selection before model building | **NOT MET** | Roughly 40 specifications were explored across the programme; HDL-C was added post hoc after a head-to-head loss **in the cohort that has now been retracted**, and the HDL-for-diabetes swap was undocumented and followed performance inspection (R13). None of this is reported. A full specification-search history is required. |
| 9b (D;E) | All predictors defined, including how and when measured; blinding actions | **PARTIAL** | Definitions and source columns in the provenance CSV. Missing: the hypertension composite (BP medication, or SBP ≥ 140, or DBP ≥ 90) and its coverage; that "cumulative cholesterol" is log(back-calculated untreated LDL-C × age), not a measured cumulative exposure; that `age_sp18` may be collinear with age (2.3). |
| 9c (D;E) | If predictor measurement is subjective, qualifications and demographics of assessors | **NOT APPLICABLE** | All predictors are laboratory values, recorded diagnoses or recorded behaviours. State explicitly. |

### 3.5 Methods — sample size, missing data, analysis

| Item | Requirement (abbreviated) | Status | Where addressed / what is missing |
|---|---|---|---|
| 10 (D;E) | How study size was arrived at, separately for development and evaluation; justification of sufficiency; any calculation | **NOT MET** | No sample-size calculation. EPV ≈ 11.5 (92/8), below conventional adequacy. Requires a Riley-type minimum sample size for the number of candidate terms with the observed event rate, and an explicit statement of the shortfall. |
| 11 (D;E) | Missing data handling; reasons for omitting data | **PARTIAL** | `IterativeImputer` fitted **on the training fold only** and applied to the held-out fold — a genuine strength, correctly avoiding leakage. Missing: per-predictor missingness in the 1,159 analysis set; missingness **by outcome status**; justification of the implied MAR assumption when missingness demonstrably tracks events; and the 659 omitted participants reported as omissions here. |
| 12a (D) | How data were used, including partitioning, considering sample-size requirements | **PARTIAL** | Repeated k-fold with families re-permuted per repeat; no held-out partition. Missing: whether sample-size requirements were considered when partitioning, and per-fold event counts (folds with fewer than 10 events must be flagged and suppressed). |
| 12b (D) | Handling of predictors: functional form, rescaling, transformation, standardisation | **PARTIAL** | The functional forms are explicit (linear spline at 18 y; log TG/HDL-C; log[untreated LDL-C × age]). Missing: rationale for the 18-year knot; confirmation that any scaling was fitted inside the training fold; and an applicability check for the knot in this age distribution (R7 shows the knot was transplanted without one). |
| 12c (D) | Type of model, rationale, all model-building steps, hyperparameter tuning, internal validation method | **NOT MET** | Cox with penalizer **fixed at 0.05** — not tuned, and not documented as pre-specified. The ~40-specification search is **not replayed inside the cross-validation folds**, so the internal validation does not remove selection optimism. Stratification of the baseline hazard by ascertainment must be reported as a modelling decision with its rationale. |
| 12d (D;E) | Heterogeneity in parameter values and performance across clusters, if handled/quantified | **PARTIAL** | Clustering is handled: family-grouped folds, families re-permuted per repeat, family-cluster bootstrap. Missing: any quantification of heterogeneity across families or ascertainment strata, the **effective (Kish) cluster count** (R9 showed a nominal-to-effective collapse in the other cohort), and consideration of TRIPOD-Cluster. |
| 12e (D;E) | All performance measures and plots, with rationale; criteria for comparing models | **NOT MET** | Discrimination only. **No calibration of any kind** (no calibration slope, no calibration-in-the-large, no observed:expected, no flexible calibration curve), no clinical utility. The win/tie/loss decision rule is not pre-specified and its labels already moved once with the CV configuration. |
| 12f (E) | Model updating arising from evaluation | **NOT APPLICABLE** | No updating performed for CALON-W. State explicitly; note that updating cannot be evaluated while no absolute-risk output exists. |
| 12g (E) | For evaluated models, how predictions were calculated (formula, code, object, API) | **NOT MET** | The comparators are not faithfully implemented as published: Montreal-FH-SCORE uses **z-anchors derived from the Welsh development cohort itself**, and SAFEHEART-RE's prior-ASCVD term was omitted. Each adaptation must be declared as an adaptation, with the exact equation used and a quantification of the adaptation's effect. As implemented, "Montreal" is anchor-dependent (R11) and is being compared using anchors estimated in the comparison data. |
| 13 (D;E) | Class imbalance methods, why and how; subsequent recalibration | **NOT APPLICABLE** | No class-imbalance method used (event fraction ≈ 7.9%). The guideline still requires this to be stated. |
| 14 (D;E) | Approaches used to address model fairness, with rationale | **NOT MET** | No fairness analysis, no subgroup performance (sex, age band, treatment status, deprivation, ethnicity), no representativeness assessment. |
| 15 (D) | Model output (probabilities, classification); rationale and thresholds | **NOT MET** | No probability output exists: a stratified-baseline Cox model without a reported baseline survival function cannot produce absolute risk. No thresholds, no risk groups. |
| 16 (D;E) | Differences between development and evaluation data in setting, eligibility, outcome, predictors | **NOT MET** | The item was to be answered by the two-cohort design, which is withdrawn. As it stands there is no evaluation dataset. For the comparator evaluation, differences between this cohort and each comparator's derivation cohort (setting, endpoint, LDL-C basis, treatment era) are unreported — and are the reason R10's estimand mismatch went unnoticed. |
| 17 (D;E) | Ethics committee / IRB approval and consent or waiver | **NOT MET** | Not stated anywhere in the package. Requires the registry (PASS/DRAGON) approval reference and consent basis. |

### 3.6 Open science

| Item | Requirement (abbreviated) | Status | Where addressed / what is missing |
|---|---|---|---|
| 18a (D;E) | Funding source and role of funders | **NOT MET** | Not stated. |
| 18b (D;E) | Conflicts of interest and financial disclosures for all authors | **NOT MET** | Not stated. Intellectual conflicts relating to the authors' own prior FH publications should be disclosed. |
| 18c (D;E) | Where the protocol can be accessed, or state none prepared; deviations | **PARTIAL** | `PROTOCOL_LOCK.md` (9 August 2026) exists but locks the **cross-sectional CALON-DISC/CALON-N** design, not CALON-W (Cox, incident, 8 terms). CALON-W was specified on 10 August and then altered post hoc. A dated amendment log covering the specification change, the HDL-for-diabetes swap, and the UK Biobank withdrawal is required. |
| 18d (D;E) | Registration information, or state not registered | **NOT MET** | Not registered. The guideline requires this to be stated. |
| 18e (D;E) | Availability of the study data | **PARTIAL** | Governance position is documented (aggregate-only outputs, no participant rows). Missing a formal availability statement giving the conditions for registry access; "available on reasonable request" is explicitly deprecated by the guideline. |
| 18f (D;E) | Availability of the analytical code, with versions and documentation | **PARTIAL** | Code, package versions and input SHA-256 hashes exist for the predecessor specification (`code/12_welsh_prospective_model.py`, `OPEN_MODEL_SEARCH_RUN_META.json`, `OPEN_MODEL_SEARCH_QC.json`). **No script or output file in the package produces the 8-term CALON-W numbers**, and the original Welsh producing script is lost, so the cohort build is a near-reproduction. |

### 3.7 Patient and public involvement

| Item | Requirement (abbreviated) | Status | Where addressed / what is missing |
|---|---|---|---|
| 19 (D;E) | Patient and public involvement in design, conduct, reporting, interpretation, dissemination — or state none | **NOT MET** | Not addressed. If there was none, that must be stated explicitly. |

### 3.8 Results, discussion, usability

| Item | Requirement (abbreviated) | Status | Where addressed / what is missing |
|---|---|---|---|
| 20a (D;E) | Participant flow, numbers with and without the outcome, follow-up summary; diagram | **PARTIAL** | The sequential flow (2,405 genotype-positive → 1,159 retained; 92 events) is in `WELSH_PROSPECTIVE_VERIFICATION.md`. Missing: a flow diagram, and explicit presentation of the 659 excluded for lacking a later record **including the 10 with dated events**. |
| 20b (D;E) | Characteristics overall and by data source: key dates, predictors, treatments, sample size, events, follow-up, missing data; differences across demographic groups | **PARTIAL** | Availability tables exist (`OPEN_MODEL_SEARCH_AVAILABILITY_WALES.csv`) but for a different, larger search cohort (1,513 / 64 events), not the 1,159 / 92 analysis set. No Table 1 for CALON-W. |
| 20c (E) | For model evaluation, compare distributions of predictors, demographics and outcome with the development data | **NOT MET** | Applies to the comparator evaluation. No comparison of this cohort's distributions against the Montreal, FH-RS or SAFEHEART derivation cohorts — precisely the omission that allowed the incident-versus-prevalent mismatch (R10) to stand unexamined in the withdrawn arm. |
| 21 (D;E) | Number of participants and outcome events in each analysis | **PARTIAL** | Headline 1,159 / 92 / 711 reported and independently reproduced. Missing: per-analysis counts (per fold, per comparator complete-case set, per repeat), with cells under 10 suppressed. |
| 22 (D) | Full model specification enabling predictions in new individuals and third-party evaluation | **NOT MET** | No coefficients published, and **no baseline survival function** — and because the baseline hazard is stratified by ascertainment, two stratum-specific baseline survivals are required. In its present form the model cannot be applied, evaluated or reproduced by a third party. |
| 23a (D;E) | Performance estimates with confidence intervals, including key subgroups; plots | **NOT MET** | Discrimination only (C = 0.7587), unverified, with no reported CI for CALON-W itself, no calibration, no subgroup performance, no plots. Item 12e's omissions propagate here. |
| 23b (D;E) | Results of heterogeneity in performance across clusters, if examined | **NOT APPLICABLE** | Not examined. Given 711 family clusters and the effective-cluster collapse demonstrated in the withdrawn arm (R9), examining it is strongly indicated (see 12d). |
| 24 (E) | Results of any model updating, including the updated model and its performance | **NOT APPLICABLE** | No updating performed. |
| 25 (D;E) | Overall interpretation, including fairness, in the context of objectives and previous studies | **NOT MET** | Not drafted. Any interpretation must lead with: 8 ties and 1 win against three published scores, in one cohort, with no calibration and no external validation. |
| 26 (D;E) | Limitations — non-representative sample, sample size, overfitting, missing data — and their effect on bias, uncertainty and generalisability | **PARTIAL** | A complete limitation inventory exists (this document §2.3–2.4 and the programme audit files) but has not been written into a manuscript. It must include: selection optimism +0.0168; ~40 specifications; EPV 11.5; informative censoring with 10 lost events; differential recording; no calibration; no external validation; label instability; near-reproduction of the build; and the withdrawal of the UK Biobank arm. |
| 27a (D) | How poor-quality or unavailable predictor values should be handled at implementation | **NOT MET** | Not addressed. Acute given that hypertension, diabetes and smoking are incompletely recorded in the source registry. |
| 27b (D) | Whether users must interact in handling input data, and the expertise required | **NOT MET** | Not addressed. Non-trivial: the model requires a back-calculated untreated LDL-C, which a user must derive. |
| 27c (D;E) | Next steps for future research, with a view to applicability and generalisability | **PARTIAL** | The outcome-refresh data request (SAIL/PEDW hospital-episode linkage plus ONS death registration, with a declared administrative end date) is specified in `MANUSCRIPT_SPEC_CLAUDE.md` §5. Must be brought into the paper as the named condition for a valid prospective analysis. |

### 3.9 TRIPOD+AI for Abstracts (13 items; required by item 2)

| Item | Requirement (abbreviated) | Status | What is missing |
|---|---|---|---|
| 1 | Title identifies development/evaluation, target population, outcome | **NOT MET** | See main item 1. |
| 2 | Brief healthcare context and rationale for all models | **NOT MET** | No abstract drafted. |
| 3 | Objectives, stating development, evaluation or both | **NOT MET** | Must state development with internal validation only. |
| 4 | Sources of data | **NOT MET** | Must name the All-Wales FH registry (PASS) — see RECORD 1.1. |
| 5 | Eligibility criteria and setting | **NOT MET** | Must include the follow-up-record requirement that removes 659 participants. |
| 6 | Outcome predicted, including **time horizon** for prognostic models | **NOT MET** | No time horizon exists (main item 8a, 22). |
| 7 | Type of model, model-building steps, internal validation method | **NOT MET** | Must disclose the specification search, not only the final model. |
| 8 | Measures used to assess performance | **NOT MET** | Discrimination only; the absence of calibration must be stated in the abstract. |
| 9 | Number of participants and outcome events | **NOT MET** | 1,159 / 92 available but not written. |
| 10 | Summary of predictors in the final model | **NOT MET** | Must state 8 terms and flag the possible age/`age_sp18` collinearity. |
| 11 | Performance estimates with confidence intervals | **PENDING QC** | C = 0.7587 has no reported CI and is unverified; seed stability outstanding. |
| 12 | Overall interpretation of the main results | **NOT MET** | Must not describe 8 ties and 1 win as superiority. |
| 13 | Registration number and registry/repository name | **NOT MET** | Not registered. |

---

## 4. STROBE (cohort) with RECORD extensions

The Welsh arm is a cohort study, so the **cohort** STROBE checklist applies. (The cross-sectional STROBE variants that would have covered the UK Biobank arm are not used, because that arm is withdrawn.)

### 4.1 STROBE — title, abstract, introduction, methods

| Item | Requirement (abbreviated) | Status | Where addressed / what is missing |
|---|---|---|---|
| 1(a) | Study design indicated with a commonly used term in title or abstract | **NOT MET** | Neither title nor abstract states "retrospective cohort study"; the current title implies a two-setting comparison that no longer exists. |
| 1(b) | Informative, balanced abstract of what was done and found | **NOT MET** | No abstract. Balance now requires stating 8 ties, 1 win, no calibration, no external validation. |
| 2 | Scientific background and rationale | **PARTIAL** | Present in the programme skeleton; not in manuscript form; needs the "why a new model when three exist" answer. |
| 3 | Specific objectives, including prespecified hypotheses | **PARTIAL** | `PROTOCOL_LOCK.md` states directional coefficient constraints and stopping rules, but for the earlier design; CALON-W's objectives and hypotheses are not prespecified in a dated document. |
| 4 | Key elements of design presented early | **NOT MET** | Not drafted. Must state single-cohort development, internal validation only. |
| 5 | Setting, locations, relevant dates: recruitment, exposure, follow-up, data collection | **NOT MET** | No accrual window; **no administrative follow-up end date**; median follow-up disputed (4.24 vs 4.01 y). |
| 6(a) | Eligibility criteria, sources and methods of selection; methods of follow-up | **PARTIAL** | Eight-step rule documented in the audit; must be published, with follow-up defined by clinic/BMI/death record and its consequences stated. |
| 6(b) | For matched studies, matching criteria and numbers exposed/unexposed | **NOT APPLICABLE** | CALON-W is unmatched. (The FH vs matched non-FH work is a separate analysis and not part of this model.) |
| 7 | Define all outcomes, exposures, predictors, confounders, effect modifiers; diagnostic criteria | **PARTIAL** | Predictor definitions exist in the provenance CSV. Missing: the outcome component definitions with their source fields as a table, and the diagnostic criteria for hypertension and diabetes. |
| 8 | For each variable, sources of data and methods of assessment; comparability across groups | **NOT MET** | Sources are listed, but assessment comparability fails on the study's own evidence: recording of diabetes and smoking differs systematically between participants who had events and those who did not. |
| 9 | Efforts to address potential sources of bias | **PARTIAL** | Real efforts exist and should be credited: baseline hazard stratified by ascertainment; family-clustered folds re-permuted per repeat; training-fold-only imputation; exclusion of prevalent events at baseline; a binding rule against published scores as inputs. Missing: any measure against informative censoring, differential recording, or specification-search optimism. |
| 10 | How study size was arrived at | **NOT MET** | Convenience sample; no calculation; EPV 11.5 (see TRIPOD 10). |
| 11 | How quantitative variables were handled; groupings and why | **PARTIAL** | Transformations stated; the 18-year knot has no stated rationale and no applicability check in this age distribution. |
| 12(a) | All statistical methods, including control for confounding | **PARTIAL** | Cox, penalizer 0.05, stratified baseline, repeated grouped CV, cluster bootstrap. Missing: that the penalty was fixed rather than tuned, and that the specification search is not inside the CV. |
| 12(b) | Methods used to examine subgroups and interactions | **NOT MET** | No subgroup or interaction analysis for CALON-W. |
| 12(c) | How missing data were addressed | **PARTIAL** | In-fold `IterativeImputer` documented; the missingness mechanism is not, and the MAR assumption is not defensible on the study's own recording evidence. |
| 12(d) | How loss to follow-up was addressed | **NOT MET** | This is the study's central methodological failure: 659 participants excluded for lacking a later record, including 10 with dated events, and no administrative censoring date. |
| 12(e) | Sensitivity analyses | **PARTIAL** | A complete-case arm exists for the predecessor specification (`welsh_prospective_model.json`, n = 528). No sensitivity analyses for the untreated-LDL divisor, the treated-rate discrepancy, the censoring rule, or MNAR missingness. |

### 4.2 STROBE — results, discussion, other information

| Item | Requirement (abbreviated) | Status | Where addressed / what is missing |
|---|---|---|---|
| 13(a) | Numbers at each stage: eligible, examined, confirmed, included, completing follow-up, analysed | **PARTIAL** | Available in the verification report; not in manuscript form. |
| 13(b) | Reasons for non-participation at each stage | **PARTIAL** | Reasons are recorded per step; the 659-participant step needs its reason stated as a data-coverage artefact rather than a participant characteristic. |
| 13(c) | Consider a flow diagram | **NOT MET** | No flow diagram. |
| 14(a) | Characteristics of participants: demographic, clinical, social; exposures and confounders | **NOT MET** | No Table 1 for the 1,159 analysis set. |
| 14(b) | Number with missing data for each variable of interest | **NOT MET** | Availability tables exist only for the larger search cohort, not the analysis set, and are not stratified by outcome. |
| 14(c) | Summarise follow-up time | **PENDING QC** | 6,841 person-years reproduced; median follow-up 4.24 y (briefed) vs 4.01 y (reconstructed) unresolved. |
| 15 | Report numbers of outcome events or summary measures over time | **PARTIAL** | 92 events total; no distribution over follow-up time, no event-rate table, no component breakdown (with cells under 10 suppressed). |
| 16(a) | Unadjusted and adjusted estimates with precision; state which confounders and why | **NOT MET** | No hazard ratios or confidence intervals reported for any predictor. This also blocks the univariable and coefficient-sign checks that destroyed the other arm (2.3). |
| 16(b) | Report category boundaries when continuous variables were categorised | **NOT APPLICABLE** | No continuous predictor was categorised; the age term uses a linear spline, which must instead be reported under item 11. |
| 16(c) | If relevant, translate relative risk into absolute risk for a meaningful period | **NOT MET** | Impossible as the model stands: no baseline survival function is reported. |
| 17 | Other analyses: subgroups, interactions, sensitivity analyses | **PARTIAL** | The ~40-specification programme search and the complete-case arm exist but are undisclosed as analyses; nothing is reported as a pre-specified secondary analysis. |
| 18 | Summarise key results with reference to objectives | **NOT MET** | Not drafted; must be rewritten around the single surviving cohort. |
| 19 | Limitations, with direction and magnitude of potential bias | **PARTIAL** | Inventory complete (§2.3–2.4) but not written; **direction and magnitude** must be given, not just named — e.g. informative censoring removing 10 events biases discrimination unpredictably and event rate downwards; selection optimism is measured at +0.0168. |
| 20 | Cautious overall interpretation | **NOT MET** | Not drafted. The programme's own kill-list forbids "superior to", "outperforms" and "first"; 8 ties and 1 win must be presented as such. |
| 21 | Generalisability | **NOT MET** | Not addressed. A specialist genotype-confirmed registry with ascertainment-stratified baseline hazard generalises poorly; the retraction removed the only other setting. |
| 22 | Funding source and role of funders | **NOT MET** | Not stated. |

### 4.3 RECORD extensions for routinely-collected health data

| Item | Requirement (abbreviated) | Status | Where addressed / what is missing |
|---|---|---|---|
| RECORD 1.1 | Type of data specified in title/abstract; name the databases where possible | **NOT MET** | Neither the All-Wales FH registry (PASS) nor its routinely-collected nature is named in the title or any abstract. |
| RECORD 1.2 | Geographic region and timeframe in title/abstract | **NOT MET** | "Two ascertainment settings" names neither Wales nor any timeframe — and one setting is now withdrawn. |
| RECORD 1.3 | State in title/abstract if databases were linked | **NOT MET** | Linkage occurred (`WALES_FH_CLEANED.csv` to `pass_master.csv`, verified 7,253/7,253 at the internal participant-key level) and is not declared. |
| RECORD 6.1 | Population-selection codes/algorithms listed in detail, or explanation | **PARTIAL** | The eight-step algorithm is documented in the audit; it must appear in the paper or supplement, including the treatment of the single missing family value as a singleton cluster (710 families + 1 → 711 clusters). |
| RECORD 6.2 | Reference validation studies of the codes/algorithms; provide methods and results if validated here | **NOT MET** | No validation of the ASCVD component-age fields, the diabetes/smoking/hypertension fields, or the genotype-positive flag. None referenced, none performed. |
| RECORD 6.3 | Flow diagram or graphical display of the linkage, with numbers at each stage | **NOT MET** | No linkage diagram. |
| RECORD 7.1 | Complete list of codes and algorithms for exposures, outcomes, confounders, effect modifiers | **NOT MET** | No code list exists. The outcome-definition table was planned (audit workstream W8, comment 14) but never built for CALON-W. |
| RECORD 12.1 | Extent of investigator access to the database population | **PARTIAL** | Governed source snapshots with hashes are recorded; the relationship between the investigators and the registry custodians, and what portion of the database was accessible, is not described. |
| RECORD 12.2 | Data-cleaning methods | **PARTIAL** | Range checks and derivations are in the provenance CSV and build script. Missing: the cleaning applied to the composite hypertension variable and the handling of the sentinel strings ("Unknown", "NoValue") in the source. |
| RECORD 12.3 | Whether person-level/institutional linkage occurred; methods and quality evaluation | **PARTIAL** | Person-level linkage was performed and its completeness verified (7,253/7,253; family values agreed for every linked record with a non-missing value). Not reported in any manuscript, and no linkage-error analysis. |
| RECORD 13.1 | Describe in detail the selection of persons included, including filtering on data quality, availability and linkage | **NOT MET** | This is the study's dominant bias and it is currently invisible in any reportable document: 659 participants, including 10 with dated post-baseline ASCVD events, are removed by a **data-availability** filter (presence of a later clinic/BMI/death record), not by a clinical criterion. |
| RECORD 19.1 | Discuss implications of using data not created to answer the research question: misclassification, unmeasured confounding, missing data, changing eligibility over time | **NOT MET** | Not drafted, and it is the single most important discussion paragraph this paper needs. It must cover: outcome ascertainment contingent on clinic contact; risk-factor recording that tracks event status; back-calculated untreated LDL-C; and eligibility that changes with the length of a participant's record. |
| RECORD 22.1 | How to access supplemental information: protocol, raw data, programming code | **PARTIAL** | Package structure, run order and governance are documented in `README.md`. Missing: a protocol that actually covers CALON-W, a code artefact that produces the CALON-W numbers, and an explicit statement that the original Welsh producing script is lost and the current build is a near-reproduction (treated rate 7.1% vs an archived 11%). |

---

## 5. PROBAST risk of bias and applicability

**Assessment unit.** PROBAST is completed once per distinct model development or validation. Two assessments were in scope; **one is now void**:

- **Assessment A — CALON-W development, All-Wales FH registry (PASS), prognostic/incident.** Completed below.
- **Assessment B — CALON-W development, UK Biobank, diagnostic/prevalent.** **Void.** The analysis is withdrawn (Section 1). For the record, it would be HIGH risk of bias in all four domains, driven by a 100% outcome-before-predictor temporality reversal (signalling questions 2.2, 2.3, 3.5, 3.6 all "No"), leakage of treatment status (4.x), an exactly collinear predictor pair (4.2), EPV 7.1 (4.1), and seed-dependent estimates (4.8).
- **Not assessed.** Each published comparator scored in these data (Montreal-FH-SCORE, FH-Risk-Score, SAFEHEART-RE) constitutes a separate *validation* and requires its own PROBAST validation assessment. None has been done. Montreal as implemented would fail on applicability at minimum, since its z-anchors were re-derived in the validation data itself.

**Review question used to anchor applicability** (PROBAST Step 1): *In adults with genetically confirmed FH, which multivariable models predict incident ASCVD from routinely available clinical and lipid data at a defined time horizon, for use in specialist and primary-care risk stratification?*

**Classification** (Step 2): **Development only**, with internal validation (cross-validation). All 20 development signalling questions apply.

### 5.1 Domain 1 — Participants

| # | Signalling question (abbreviated) | Answer | Rationale |
|---|---|---|---|
| 1.1 | Were appropriate data sources used (cohort, RCT, nested case-control)? | **Yes** | A genotype-confirmed national FH registry followed longitudinally is an appropriate source for an incident-ASCVD prognostic model. |
| 1.2 | Were all inclusions and exclusions of participants appropriate? | **No** | 659 otherwise-eligible genotype-positive participants — including 10 with dated post-baseline ASCVD events — are excluded for lacking a later clinic/BMI/death record. Exclusion is determined by data coverage that is plausibly related to both outcome and prognosis, and no administrative outcome-coverage date exists to replace it. An independent audit had already placed this risk set under a HOLD for prospective model fitting; the model was fitted regardless. |

**Domain 1 risk of bias: HIGH.**
Rationale: participant selection is conditioned on post-baseline data availability, which is outcome-related. The direction of the resulting bias is not predictable, and 10 events are certainly lost.

**Domain 1 applicability concern: HIGH.**
Rationale: a specialist genotype-confirmed registry, with a baseline hazard deliberately stratified by proband versus cascade ascertainment, does not match a general FH-care population; the model's absolute risk is by construction setting-specific and the second setting has been withdrawn.

### 5.2 Domain 2 — Predictors

| # | Signalling question (abbreviated) | Answer | Rationale |
|---|---|---|---|
| 2.1 | Were predictors defined and assessed in a similar way for all participants? | **No** | Recording differs systematically by outcome: diabetes present in 58% of the cohort but covering 77% of events; smoking 74% and 87%. Hypertension is a composite of three fields with incomplete coverage. Untreated LDL-C is measured in some participants and back-calculated with a fixed 0.70 divisor in others, and the identification of "treated at baseline" is itself uncertain (7.1% by the dated rule versus an archived 11% and ~86% undated `OnTreatment` positivity). |
| 2.2 | Were predictor assessments made without knowledge of outcome data? | **Probably no** | Predictors are extracted retrospectively from the same clinical record that generates the outcome. Baseline dating limits, but does not eliminate, this: the *presence* of a recorded value is demonstrably associated with having had an event. |
| 2.3 | Are all predictors available at the time the model is intended to be used? | **Probably yes** | All eight terms are routinely available at a lipid-clinic visit, except that untreated LDL-C must be derived by the user from a fixed divisor rather than measured. Unresolved: whether `age_sp18` is an exact linear function of age in this cohort, in which case one declared predictor does not exist. |

**Domain 2 risk of bias: HIGH.**
Rationale: differential ascertainment of predictor values by outcome status is documented in the study's own numbers, and the treatment-adjustment rule is unverified.

**Domain 2 applicability concern: HIGH.**
Rationale: "cumulative cholesterol" is log(back-calculated untreated LDL-C × age) — an age-scaled single measurement, not a measured cumulative exposure — and depends on a fixed 0.70 treatment divisor whose validity in this cohort is unestablished.

### 5.3 Domain 3 — Outcome

| # | Signalling question (abbreviated) | Answer | Rationale |
|---|---|---|---|
| 3.1 | Was the outcome determined appropriately? | **Probably no** | Composite ASCVD is assembled from registry component fields (MI/ACS, PCI, CABG, angina, TIA, PVD) with **no adjudication**, no validated code list, and no reference to any validation study of these fields (RECORD 6.2, 7.1). |
| 3.2 | Was a pre-specified or standard outcome definition used? | **Probably no** | The composite is pre-specified in programme documents, but the CALON-W operationalisation is a **near-reproduction** of a lost script, and no standard (e.g. coded) definition is given. |
| 3.3 | Were predictors excluded from the outcome definition? | **Yes** | No predictor enters the outcome. Events at or before baseline are excluded, and the binding programme rule keeps published scores and `GenoTypingScore` out of the predictor set. This is a genuine strength. |
| 3.4 | Was the outcome defined and determined in a similar way for all participants? | **No** | Outcome detection depends on continued clinic contact — the same process that drives the 659-participant exclusion. Participants with sparse records are systematically less likely to have an event recorded. |
| 3.5 | Was the outcome determined without knowledge of predictor information? | **Probably no** | Outcome and predictors are recorded by the same clinicians in the same record; no blinding was or could be applied. |
| 3.6 | Was the time interval between predictor assessment and outcome determination appropriate? | **No** | There is **no defined prediction time horizon** and no reported baseline survival function, so no interval is specified at all. Follow-up ends at the last clinic/BMI/death record rather than at an administrative coverage date, so the interval is set by data availability. Median follow-up is itself disputed (4.24 vs 4.01 y). |

**Domain 3 risk of bias: HIGH.**
Rationale: unadjudicated, unvalidated outcome ascertainment that varies with clinic contact, combined with an undefined prediction horizon and a data-driven follow-up clock. **The temporality of the outcome is not under experimental control.** In the withdrawn UK Biobank arm this same class of failure was total — 100% of events preceded the predictor measurement — and the Welsh arm's protection against it (dated pre-baseline predictors, baseline-prevalent events excluded) has **not yet been verified by the univariable, coefficient-sign and treatment-flag checks that exposed the defect elsewhere**.

**Domain 3 applicability concern: HIGH.**
Rationale: an unadjudicated registry composite that mixes hard events (MI, CABG, PCI) with softer ones (angina, TIA, PVD), with no code list, does not match the outcome a reader would assume from "ASCVD", and cannot be reproduced in another dataset.

### 5.4 Domain 4 — Analysis

| # | Signalling question (abbreviated) | Answer | Rationale |
|---|---|---|---|
| 4.1 | Were there a reasonable number of participants with the outcome? | **No** | 92 events for 8 model terms — EPV ≈ 11.5, below the conventional 10–20 threshold for reliable development and far below what a Riley-type calculation would require for stable penalised estimation with a specification search on top. No sample-size justification exists. |
| 4.2 | Were continuous and categorical predictors handled appropriately? | **Probably no** | The transformations are individually defensible (linear spline in age, log TG/HDL-C, log of an age-scaled lipid), but the 18-year knot has no stated rationale, was transplanted between cohorts without an applicability check (proven inadequate in the withdrawn arm, where it produced an exactly collinear duplicate of age), and the functional forms were selected within a ~40-specification search. |
| 4.3 | Were all enrolled participants included in the analysis? | **No** | 659 eligible participants, including 10 with dated events, are excluded by a data-availability rule. |
| 4.4 | Were participants with missing data handled appropriately? | **Probably no** | Method: `IterativeImputer` fitted inside the training fold only — correct practice, and it should be credited. But it is a single imputation (no multiple imputation, no pooling of uncertainty) resting on a missing-at-random assumption that the study's own recording statistics contradict (2.1). No MNAR sensitivity analysis. |
| 4.5 | Was selection of predictors based on univariable analysis avoided? | **Yes** | No univariable screening step is used. (The far larger selection problem is captured in 4.8.) |
| 4.6 | Were complexities in the data accounted for appropriately? | **Probably no** | Handled well: censoring via Cox; family clustering via grouped folds re-permuted per repeat and a family-cluster bootstrap; ascertainment via a stratified baseline hazard. Not handled: **competing risk of non-cardiovascular death**, which is treated as ordinary censoring; the informative nature of the censoring itself; and the effective (Kish) cluster count, which in the withdrawn arm collapsed from a nominal 62 to 5.1 and has not been computed for the 711 Welsh families. |
| 4.7 | Were relevant model performance measures evaluated appropriately? | **No** | **No calibration was assessed at all** — no calibration slope, no calibration-in-the-large, no observed:expected ratio, no calibration curve — and no clinical utility. Discrimination alone cannot support any statement about a prediction model's usefulness. The C-statistic itself is reported without a confidence interval for CALON-W and without seed-stability evidence. |
| 4.8 | Were model overfitting and optimism in model performance accounted for? | **No** | Selection optimism was **measured at +0.0168 AUC and left uncorrected**. Roughly 40 specifications were explored, and the search is not replayed inside the cross-validation folds, so the reported C is optimistic by an unquantified further amount. The current predictor set exists because HDL-C replaced diabetes after an inspection-driven, undocumented swap — a decision taken on the strength of results in the cohort that has since been withdrawn. Win/tie/loss labels already moved once when the CV configuration changed. |
| 4.9 | Do predictors and their assigned weights in the final model correspond to the multivariable analysis results? | **PENDING QC** | Unassessable: no coefficients, no baseline survival function and no model object have been published for CALON-W. The two independent audits (statistics; provenance) must return before this can be answered, and the sign-coherence check that failed in the withdrawn arm has not been run here. |

**Domain 4 risk of bias: HIGH.**
Rationale: six of nine signalling questions are "No" or "Probably no", one is unassessable, and the two most consequential — absence of any calibration assessment (4.7) and uncorrected, inspection-driven selection optimism (4.8) — are unambiguous.

### 5.5 Overall PROBAST judgement — Assessment A (CALON-W, Wales)

| Domain | Risk of bias | Applicability concern |
|---|---|---|
| 1 Participants | **HIGH** | **HIGH** |
| 2 Predictors | **HIGH** | **HIGH** |
| 3 Outcome | **HIGH** | **HIGH** |
| 4 Analysis | **HIGH** | (not rated — PROBAST rates applicability for domains 1–3 only) |
| **Overall** | **HIGH RISK OF BIAS** | **HIGH CONCERN REGARDING APPLICABILITY** |

**Summary of sources of potential bias.** Participant selection is conditioned on post-baseline data availability and loses 10 events (1.2, 4.3). Predictor values are recorded preferentially in participants who had events, and the treatment adjustment underpinning the flagship lipid term is unverified (2.1, 2.2). The outcome is an unadjudicated registry composite whose detection depends on clinic contact, with no defined prediction horizon and a follow-up clock set by data availability (3.1, 3.4, 3.6). The analysis is underpowered at EPV 11.5, performs no calibration whatsoever, and reports discrimination from a ~40-specification search whose measured optimism was left uncorrected (4.1, 4.7, 4.8).

**Additional PROBAST rule applied.** The tool directs that a model developed **without any external validation** should be considered for downgrading to high risk of bias even where all domains are low, unless development used a very large dataset with internal validation. CALON-W has no external validation, 92 events, and its only companion cohort has been withdrawn. The rule reinforces the HIGH verdict; it is not the reason for it.

**Summary of applicability concerns.** The development setting (specialist genotype-confirmed registry with ascertainment-stratified baseline hazard), the predictor construction (back-calculated untreated LDL-C on a fixed divisor; an age-scaled single measurement presented as cumulative exposure), and the outcome (unadjudicated mixed composite, no code list, no horizon) each diverge from the review question. Absolute risk is not estimable from the published model at all.

---

## 6. ITEMS BLOCKING SUBMISSION

Ordered by severity. Severity = the degree to which the item invalidates a claim the paper would make, not the effort to fix it.

| # | Blocking item | Instruments | Action that resolves it |
|---|---|---|---|
| **1** | **The UK Biobank arm is retracted for a 100% outcome-before-predictor temporality reversal.** Its results, its 15 comparisons, its AUC 0.7605 and the "24 comparisons / 6 wins" headline cannot be reported. | TRIPOD 1, 4, 5a, 12g, 16, 20c, 23a, 25; PROBAST domains 2, 3, 4 | Remove the arm from every document, figure, table and abstract. Rewrite the paper as a single-cohort Welsh development study. If retained at all, retain it only as an explicitly labelled methodological negative — "an FH prediction analysis in which every event preceded biomarker measurement" — with Section 1 of this document as its record. Add an amendment note to `PROTOCOL_LOCK.md` dated to the withdrawal. |
| **2** | **The Welsh arm has not been subjected to the checks that destroyed the other arm.** Univariable performance of cumulative cholesterol, coefficient signs, statin-flag-alone discrimination, and `age`/`age_sp18` collinearity are all unrun. | TRIPOD 9b, 12c, 22, 23a; PROBAST 3.6, 4.2, 4.9; STROBE 16(a) | Run the identical QC battery in Wales before anything else: univariable C for every term; full coefficient table with signs and CIs; treatment-flag-alone model versus the full model; Pearson r(age, age_sp18) and the cohort's minimum baseline age; effective (Kish) cluster count. Publish the results whichever way they fall. If cumulative cholesterol is at chance or the lipid signs reverse in Wales too, the model does not exist. |
| **3** | **No calibration of any kind has been performed.** | TRIPOD 12e, 23a; PROBAST 4.7; STROBE 16(c) | From out-of-fold linear predictors, report calibration slope, calibration-in-the-large, observed:expected and a flexible calibration curve at a **declared time horizon**, using the stratum-specific baseline hazards. Without this there is no prediction-model paper, only a discrimination note. |
| **4** | **No model specification is published: no coefficients, no baseline survival, hence no absolute risk and no third-party evaluation.** | TRIPOD 15, 22, 23a; STROBE 16(a), 16(c) | Publish the full equation with both ascertainment-stratum baseline survival functions at the declared horizon, plus a machine-readable model object and a worked example. |
| **5** | **Informative censoring: 659 eligible participants excluded, including 10 with dated events; no administrative outcome-coverage date.** An audit HOLD on this risk set was already in force when the model was fitted. | RECORD 13.1; STROBE 12(d), 13; PROBAST 1.2, 4.3 | Obtain an administrative outcome-coverage end date (SAIL/PEDW hospital-episode linkage plus ONS death registration) or a validated last-known-alive date; rebuild the risk set; refit; report the original and repaired analyses side by side. Until then, no result from this risk set should be presented as a prospective estimate. |
| **6** | **Selection optimism +0.0168 measured and uncorrected; ~40 specifications explored; the current predictor set was chosen by an undocumented, inspection-driven swap.** | TRIPOD 9a, 12a, 12c, 26; PROBAST 4.8 | Replay the entire specification search — including the HDL-for-diabetes decision — inside every training fold, and report that nested-CV C as the headline. Publish a dated specification-search log. Quote the measured optimism beside every discrimination estimate. |
| **7** | **Comparators are not faithfully implemented and are not like-for-like.** Montreal's z-anchors were derived from the Welsh cohort itself; SAFEHEART-RE's prior-ASCVD term was removed; all three are incident models. | TRIPOD 12g, 16, 20c; PROBAST (separate validation assessments) | Score each comparator with its **published** anchors and coefficients; label every deviation as an adaptation and quantify its effect; tabulate each comparator's derivation cohort, endpoint and LDL-C basis against this cohort; complete a PROBAST validation assessment for each. |
| **8** | **Verdict labels sit near the decision boundary and are configuration-dependent** (they already moved once between 10-fold × 8 repeats and 5-fold × 4). | TRIPOD 12e, 23a | Pre-specify one CV configuration and one superiority rule before re-running. Report paired ΔC with cluster-bootstrap CIs as the primary quantity and demote the win/tie/loss tally; show both configurations side by side; report label stability across seeds. |
| **9** | **EPV 11.5 with no sample-size justification.** | TRIPOD 10; STROBE 10; PROBAST 4.1 | Report the Riley minimum sample size and required events for 8 terms at the observed event rate, state the shortfall, and add stability evidence (bootstrap predictor-inclusion frequencies and prediction-instability plots). |
| **10** | **Differential recording of risk factors by event status** (diabetes 58%/77%, smoking 74%/87%) with a single in-fold imputation resting on an untenable MAR assumption. | TRIPOD 7, 11; RECORD 19.1; STROBE 8, 12(c); PROBAST 2.1, 4.4 | Tabulate missingness by outcome status for every predictor; move to multiple imputation with pooled uncertainty; add an MNAR delta-adjustment sensitivity analysis; state the likely direction of bias. |
| **11** | **No external validation and no transport analysis.** With the UK Biobank arm withdrawn there is now no second dataset at all. | TRIPOD 5a, 16, 20c; PROBAST overall rule | Either (a) identify a genuinely independent FH cohort with dated pre-baseline predictors and adjudicated incident events and validate there, or (b) state plainly in the title, abstract and conclusions that this is development with internal validation only, and make no transportability claim. |
| **12** | **Provenance: the original producing script is lost; the current build is a near-reproduction (treated rate 7.1% vs an archived 11%); no artefact in the package produces the CALON-W numbers.** | TRIPOD 18f, 22; RECORD 22.1; STROBE 22 | Commit a numbered, hashed script and a JSON output that regenerate every reported number; freeze the cohort definition with its input SHA-256; state the near-reproduction openly; add a sensitivity analysis using the undated `OnTreatment` rule as the alternative treatment definition. |
| **13** | **Unreconciled internal discrepancies:** age + sex C = 0.7036 vs 0.7391; median follow-up 4.24 y vs 4.01 y. | TRIPOD 21, 23a; STROBE 14(c) | Reconcile under a single declared CV configuration and a single follow-up definition; publish the reconciliation. |
| **14** | **No outcome code list, no algorithm validation, no linkage diagram.** | RECORD 6.2, 6.3, 7.1; STROBE 7 | Publish the outcome-definition table (component, source field, code system, codes, n with cells under 10 suppressed); reference or perform a validation of the ascertainment algorithm; add a linkage flow diagram. |
| **15** | **No fairness or subgroup analysis; no health-inequalities framing.** | TRIPOD 3c, 14, 23a; STROBE 12(b) | Report performance by sex, age band, treatment status and, where recorded, ethnicity and deprivation, with events per subgroup and cells under 10 marked non-estimable. |
| **16** | **Governance and open-science basics absent:** ethics approval, funding, conflicts, registration, PPI, data and code availability statements, participant flow diagram, Table 1. | TRIPOD 17, 18a–18f, 19, 20a, 20b; STROBE 1, 5, 13(c), 14(a), 22; RECORD 22.1 | Add each as a standard statement. Register the study or state explicitly that it was not registered. |
| **17** | **Two independent audits (statistics; provenance) are still running.** | All PENDING QC items: TRIPOD Abstracts 11, PROBAST 4.9, STROBE 14(c) | Do not submit before both return. Any item marked PENDING QC in this document must be re-adjudicated against their verdicts, and this document re-issued with a new date. |

---

## 7. Assessor's bottom line

Three statements should be taken forward verbatim into the manuscript's own limitations, because a methods reviewer will otherwise write them for you:

1. **This is a single-cohort model-development study with internal validation only.** There is no external validation, no calibration, and no transport analysis. The companion cohort was withdrawn for a fatal temporality defect.
2. **The surviving comparative evidence is 8 ties and 1 win across 9 head-to-head comparisons against three published FH risk scores**, from a cohort in which those comparators were not faithfully implemented. That does not support any claim of superiority, and the programme's own kill-list already forbids the language.
3. **The Welsh arm is structurally protected against the defect that destroyed the other arm, but that protection has not been demonstrated.** Until the univariable, coefficient-sign, treatment-flag and collinearity checks are run in Wales, the correct description of CALON-W is *unverified*, not *validated*.

---

*Prepared 11 August 2026. Item lists retrieved from the TRIPOD+AI statement and Expanded Checklist (BMJ 2024;385:e078378), the STROBE cohort checklist, the RECORD checklist (PLoS Med 2015, CC BY), and PROBAST v15/05/2019 (Ann Intern Med 2019). Item wording is abbreviated by the assessor; the source documents are authoritative. Re-issue required when the two independent audits report.*
