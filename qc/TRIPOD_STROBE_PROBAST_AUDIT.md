# CALON-N full TRIPOD+AI, STROBE, and PROBAST audit

Audit date: 9 August 2026

Status: Y=addressed; P=partly addressed or not recoverable from the supplied data; N=not addressed/failed; NA=not applicable. This is a transparent local mapping to the reporting frameworks, not formal certification or a numerical quality score.

## TRIPOD+AI item-level mapping

| Local item | Paraphrased reporting requirement | Status | Manuscript/package evidence and residual action |
|---:|---|:---:|---|
| 1 | Identify model purpose and development/validation design in title | Y | Result-led title states established disease and clinic–biobank probability-transport failure. |
| 2 | Structured abstract with setting, participants, modelling, performance and conclusion | Y | Structured abstract reports both cohorts, selection, AUCs, calibration and non-use. |
| 3 | Explain clinical context and existing models | Y | Introduction distinguishes Montreal, FH-Risk-Score and SAFEHEART endpoints. |
| 4 | State intended use, target population and estimand | Y | Cross-sectional established-ASCVD identification; prospective-risk and treatment use excluded. |
| 5 | Describe data sources and settings | Y | DRAGON/PASS specialist service and UK Biobank sections. |
| 6 | Give relevant dates and data cuts | P | Local snapshot and analysis dates plus UKB baseline range reported; validated DRAGON recruitment/data-cut and upstream UKB/ClinVar release IDs remain unavailable. |
| 7 | State eligibility and cohort construction | Y | Methods and analytical compendium give full strict/union construction. |
| 8 | Report participant flow and analysis denominators | Y | 424→424 DRAGON and 6,597,041 calls→890 strict/1,264 union flow table; no missingness exclusion. |
| 9 | Define outcome, timing and components | Y | Primary fields, DRAGON component counts and UKB prevalence timing reported. |
| 10 | Report outcome assessment/blinding/adjudication | P | Absence of repeated blinded central adjudication stated; full original adjudication procedure not recoverable. |
| 11 | Define every predictor, coding, units and timing | Y | Methods and compendium variable table; post-event timing prominent. |
| 12 | Establish predictor availability at intended use time | N | Fails for prospective use; model deliberately restricted to cross-sectional research. |
| 13 | Explain study-size considerations | P | Available-sample and sparse-event low-dimensional rationale stated; no formal a priori development calculation. |
| 14 | Report missingness for each predictor | Y | Cohort coverage in Table S1 and compendium. |
| 15 | Describe missing-data handling | Y | Source-training median completion; assumptions and limitations explicit. |
| 16 | Keep preprocessing inside resampling | Y | Completion, transformations, scaling, residualisation and tuning refitted inside training folds. |
| 17 | Describe the complete candidate set | Y | Ten Phase B raw-variable architectures listed. |
| 18 | Describe model type, penalisation and hyperparameter selection | Y | Ridge logistic regression; six-value C grid; grouped Brier selection. |
| 19 | Describe clustering/dependence handling | Y | PASS families and qualifying-variant connected components kept intact. |
| 20 | Explain architecture/feature selection | Y | Sign gate and maximin reciprocal-AUC rule; both outcomes consumed. |
| 21 | Report internal validation | Y | Candidate-specific repeated nested grouped AUCs with scope caveat. |
| 22 | Report external/transport evaluation honestly | P | Reciprocal source-frozen transport is complete but target-informed, not protected validation. |
| 23 | State discrimination and overall-accuracy metrics | Y | AUC, Brier and scaled Brier reported. |
| 24 | State calibration metrics and plots | Y | Intercept, slope, E:O, quintile plots and figures reported. |
| 25 | Report uncertainty and resampling unit | Y | 4,000 target family/component bootstrap intervals and paired differences. |
| 26 | Incorporate source-development and architecture uncertainty | N | Conditional intervals omit both; explicit limitation. |
| 27 | Evaluate clinical utility with valid probability-scale methods | N | Comparative DCA withdrawn because comparator outputs were not probabilities on a common scale. |
| 28 | Prespecify subgroup handling and minimum information | Y | Ten strata per cohort; <10 non-estimable, 10–19 descriptive. |
| 29 | Report fairness/effect-modification inference | P | Sex and other stress tests reported, but no powered interactions, ancestry or deprivation analysis. |
| 30 | Describe comparator implementation and fairness | P | Same participants and outcomes; material adaptations explicitly disclosed. |
| 31 | Give full model specification | Y | Equation, features, transformations, median defaults and deterministic object supplied. |
| 32 | Give instructions and boundaries for use | Y | Model card, scorer and repeated prohibition of prospective/clinical use. |
| 33 | Provide an example without disclosing participants | Y | Synthetic-only input; no empirical participant prediction. |
| 34 | Describe recalibration or updating | Y | No target recalibration; pooled equation clearly labelled unvalidated. |
| 35 | Interpret results against objectives and stopping rules | Y | Universal-superiority hypothesis rejected. |
| 36 | Discuss limitations, bias and applicability | Y | Eight limitations, confidence hierarchy and PROBAST assessment. |
| 37 | Make protocol, code and model accessible | Y | Protocol lock/amendment, scripts, model, outputs and manifests supplied. |
| 38 | State data access, privacy and governance | Y | Aggregate-only design and restricted participant-level data statement. |
| 39 | State ethics, funding, conflicts and PPI | P | UKB approval/application, funding and conflicts reported; Welsh approval and PPI confirmation remain hard author tasks. |
| 40 | Disclose generative-AI assistance and human accountability | Y | Declarations state scope, no participant-data transmission and author responsibility. |

Current count: 30 Y, 7 P, 3 N. The counts are a gap profile, not a compliance score. The three failures are prospective predictor timing, complete source/selection uncertainty, and valid comparative decision analysis; they cannot be repaired by wording.

## STROBE cross-sectional item-level mapping

STROBE contains 22 official numbered items; the local table expands statistical item 12 into four methodological rows, producing 25 local rows.

| STROBE item | Paraphrased requirement | Status | Manuscript/package evidence and residual action |
|---|---|:---:|---|
| 1 | Identify observational design in title/abstract | Y | Abstract states retrospective cross-sectional development/transport. |
| 2 | Scientific background and rationale | Y | FH risk heterogeneity, apoB biology and transport rationale. |
| 3 | Specific objectives and hypotheses | Y | Five objectives and negative stopping rules. |
| 4 | Present key design early | Y | First Methods paragraph states design and estimand. |
| 5 | Describe setting, locations and dates | P | Settings, UKB dates and local snapshots given; validated DRAGON recruitment/data-cut absent. |
| 6 | Explain eligibility and participant selection | P | Analytical rules and flow complete; original clinic referral/invitation process incomplete. |
| 7 | Define outcomes, exposures, predictors, confounders and diagnostic criteria | Y | Dedicated carrier, outcome and predictor sections. |
| 8 | Give sources and measurement methods, including comparability | P | Columns, units and harmonisation stated; original assays and outcome adjudication incomplete. |
| 9 | Describe efforts to address bias | Y | Grouped folds, sign gate, maximin rule, sensitivity analyses and limitations. |
| 10 | Explain study size | P | Available-sample/event-limited rationale; no formal a priori calculation. |
| 11 | Explain quantitative variable handling | Y | Bounds, logs, binary coding, ratio and subgroup threshold. |
| 12a | Describe all statistical methods and confounding adjustment | Y | Penalised logistic pipeline, comparators and paired cluster bootstrap. |
| 12b | Describe subgroup and interaction methods | P | Prespecified strata and event floors; no interaction inference by design. |
| 12c | Explain missing-data handling | Y | Source-fold median completion and complete-case sensitivity. |
| 12d | Explain loss, matching and sensitivity methods | Y | No longitudinal loss estimand; linkage, cluster units and sensitivities reported. |
| 13 | Report numbers at each study stage and reasons | Y | Flow table in Methods/compendium; no predictor-missingness exclusion. |
| 14 | Provide descriptive participant data and missingness | Y | Table 1 and Table S1. |
| 15 | Report outcome events or summary measures | Y | Primary/alternative event counts and components. |
| 16 | Report main estimates with precision | Y | AUCs and paired differences with cluster-bootstrap intervals. |
| 17 | Report other analyses | Y | Union, exact-HGVS, alternative outcomes, complete cases and subgroups. |
| 18 | Summarise key results against objectives | Y | Principal findings. |
| 19 | Discuss limitations and direction/magnitude of bias | Y | Eight limitations and confidence hierarchy. |
| 20 | Give cautious overall interpretation | Y | No universal, prospective, calibration or deployment claim. |
| 21 | Discuss generalisability | Y | Clinic/biobank, ancestry, treatment, genotype and endpoint contrasts. |
| 22 | State funding and funder role | Y | No dedicated grant; routine institutional support; author confirmation requested. |

Current local count: 20 Y and 5 P. There is no fully omitted STROBE item after revision, but partial date, selection, measurement, study-size and interaction reporting remain.

## PROBAST assessment

| Domain | Signalling summary | Risk of bias | Applicability concern |
|---|---|---|---|
| Participants | Specialist-service and volunteer-biobank spectra differ; referral pathway and survivor selection are incompletely captured. | High | High |
| Predictors | Several biomarkers may follow ASCVD/treatment; treatment timing and assays are not harmonised; apoA1 missingness is material. | High | High for prospective use |
| Outcome | Prevalent recorded ASCVD; components differ; no repeated blinded central adjudication. | High | High |
| Analysis | Few cases; both outcomes used for architecture selection; single median completion; adapted comparators; conditional target-only intervals; no independent third cohort. Grouping and deterministic scoring are strengths but cannot remove selection bias. | High | High |

Overall PROBAST judgement: **HIGH risk of bias and HIGH applicability concern for prospective prediction or clinical deployment.** For the narrower cross-sectional research estimand, applicability remains constrained by spectrum, timing, measurement and genetic-definition differences.

## Submission blockers after revision

The statistical and reporting narrative is complete enough for co-author review, but journal submission remains blocked until the authors provide or confirm:

1. the exact Welsh PASS/DRAGON ethics approval or service-evaluation determination, consent/waiver, legal basis, data controller, and R&D/information-governance reference;
2. the patient/public-involvement statement and CRediT contributions;
3. the validated DRAGON recruitment/data-cut and the upstream UKB genomic and ClinVar release identifiers if recoverable;
4. laboratory platforms and original outcome-adjudication details; and
5. final author-by-author funding and conflict disclosures.

Clinical use remains blocked regardless of reporting completion because no untouched prospective validation, transportable calibration, or valid decision analysis exists.
