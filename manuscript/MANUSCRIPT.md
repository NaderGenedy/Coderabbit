# Apolipoprotein B–LDL discordance identifies established cardiovascular disease in genetically defined familial hypercholesterolaemia, but absolute risk does not transport between clinic and biobank

Short title: CALON-N in genetically defined familial hypercholesterolaemia

Article type: Original Research

Target journal: *Journal of Clinical Lipidology*

Manuscript status: full master version for author and journal-length editing; not submission-ready until the Welsh ethics/governance reference and patient/public-involvement statement are confirmed.

## Highlights

- CALON-N is a seven-variable classifier fitted from raw clinical and laboratory measurements; no published score is a model input.
- Selected predictors were age, sex, HDL-C, hypertension, smoking, log(apoB/LDL-C), and log(apoA1).
- Discrimination transported asymmetrically, being lower into the biobank: AUC 0.767 from DRAGON to UK Biobank and 0.848 in reverse.
- CALON-N exceeded adapted FH-Risk-Score and SAFEHEART in UK Biobank but did not exceed Montreal-FH-SCORE.
- In DRAGON, age plus sex alone outperformed every fitted candidate by point estimate.
- Post-event biomarkers and target-informed selection prohibit prospective-risk or clinical-deployment claims.

## Abstract

**Background:** Existing familial hypercholesterolaemia (FH) instruments use conventional lipids and were developed for different outcomes in clinically ascertained cohorts. We found no FH-specific instrument developed from raw apolipoprotein B (apoB), LDL cholesterol (LDL-C), and apolipoprotein A1 (apoA1) measurements and evaluated by reciprocal transport between clinical and population-biobank ascertainment settings. We therefore tested whether apoB–LDL discordance could support a de novo classifier of established atherosclerotic cardiovascular disease (ASCVD).

**Methods:** This retrospective cross-sectional model-development study used DRAGON, a genetically ascertained specialist-clinic cohort (424 participants; 62 established ASCVD cases; 219 families), and a primary UK Biobank cohort of coordinate-linked *LDLR* carriers with a local ClinVar pathogenic/likely pathogenic classification (890 participants; 57 cases; 62 qualifying-variant connected components). Ten low-dimensional penalised-logistic architectures using raw variables only were prespecified; published FH scores were comparators, not inputs. Eligible architectures had physiologically coherent coefficient directions in both source fits. The model maximising the lower of the two reciprocal-transport AUCs was selected. Uncertainty used 4,000 target family- or qualifying-variant-component bootstrap samples.

**Results:** CALON-N contained age, male sex, HDL-C, hypertension, ever smoking, log(apoB/LDL-C), and log(apoA1). With DRAGON-fitted coefficients, UK Biobank AUC was 0.767 (95% CI 0.712–0.828); with UK Biobank-fitted coefficients, DRAGON AUC was 0.848 (0.796–0.896). In UK Biobank, CALON-N exceeded adapted FH-Risk-Score by 0.071 (0.024–0.110) and adapted SAFEHEART by 0.227 (0.122–0.294), but not Montreal-FH-SCORE (difference −0.008, −0.036 to 0.007). In DRAGON, age plus sex (AUC 0.895) and Montreal (0.893) both exceeded CALON-N by point estimate; the Montreal difference was −0.045 (−0.093 to −0.002). Calibration did not transport: expected:observed ratios were 3.00 in UK Biobank and 0.45 in DRAGON. CALON-N exceeded the best comparator in only one of 14 estimable or descriptive subgroup analyses.

**Conclusions:** A de novo apoB-discordance model was feasible and retained moderate-to-high discrimination across two genetically defined FH settings, but it did not outperform all comparators or transport absolute probabilities. The data reject universal-superiority and prospective-risk claims. CALON-N is a research classifier requiring validation using pre-event apolipoproteins in an independent FH registry.

Keywords: familial hypercholesterolaemia; apolipoprotein B; apolipoprotein A1; LDL cholesterol; ascertainment; cardiovascular disease; prediction model; transportability; UK Biobank

## Introduction

Heterozygous familial hypercholesterolaemia (HeFH) is an autosomal codominant disorder characterised by lifelong exposure to elevated concentrations of LDL-C and a substantially increased risk of premature ASCVD.[1–3] The average risk is high, but the distribution of risk is wide. Age at diagnosis, sex, smoking, blood pressure, diabetes, the severity and duration of LDL exposure, lipoprotein(a) [Lp(a)], treatment history, genotype, and the route through which a person enters care all contribute to heterogeneity. A clinic-referred index case with symptomatic coronary disease is therefore not interchangeable with an asymptomatic relative identified by cascade testing or with a carrier discovered through population sequencing.

Several FH-specific instruments attempt to organise this heterogeneity. Montreal-FH-SCORE was developed to identify prevalent cardiovascular disease using age, sex, HDL-C, hypertension, and smoking, and was subsequently validated and refined.[4,15] FH-Risk-Score was derived in 3,881 adults without previous ASCVD from five registries in Europe and North America, contributing 32,361 person-years; it predicts incident ASCVD using age, sex, HDL-C, untreated or imputed untreated LDL-C, hypertension, smoking, and Lp(a).[5] SAFEHEART-RE predicts incident events in a prospective Spanish registry and gives previous ASCVD a major role.[6] More recently, Montreal and FH-Risk-Score were evaluated cross-sectionally in an Australian specialist FH cohort, demonstrating that a score can perform differently when the endpoint and ascertainment setting change.[16] Their distinct intended populations, endpoints, time origins, predictor definitions, and baseline hazards make comparative transport a scientific question rather than a simple leaderboard.

ApoB offers a different view of the atherogenic phenotype. Each LDL, intermediate-density lipoprotein, very-low-density lipoprotein remnant, and Lp(a) particle carries one apoB molecule; apoB therefore approximates the number of circulating atherogenic particles, whereas LDL-C quantifies the cholesterol carried within the LDL fraction.[7] When apoB and LDL-C are discordant, a person may carry more or fewer particles than the cholesterol concentration suggests. This discordance has biological and epidemiological support in non-FH populations, and lower apoA1 has also been associated with cardiovascular risk across long prospective follow-up.[7,19]

The ratio apoB/LDL-C is nevertheless not a pure biological exposure. It is mathematically coupled to LDL-C, changes when treatment alters cholesterol content and particle composition, and may become especially high after intensive LDL-C lowering. In cross-sectional clinical data, an ASCVD event may precede both treatment intensification and the blood sample. A positive apoB/LDL-C association can consequently represent particle–cholesterol discordance, treatment response, reverse causation, or a mixture of all three. A prior hypothesis-generating analysis in this same 424-person Welsh cohort reported an association between apoB/LDL-C discordance and ASCVD, but its small event count, mixed event timing, and later correction require restraint.[17,18] The present study does not treat that association as independent evidence.

The analytic problem is equally important. Adding one laboratory variable at a time to a previously selected score gives that score an architectural advantage and encourages repeated outcome-guided testing. Conversely, fitting many flexible terms to fewer than 65 cases per cohort invites optimism and unstable signs. We therefore used a small, prespecified set of raw-variable architectures, ridge penalisation, cluster-aware validation, a coefficient-direction gate, and a maximin transport rule. Published instruments were prohibited as inputs and used only as comparators.

We set explicit negative stopping rules. CALON-N would not be described as universally superior unless its paired AUC interval was above zero against every comparator in both primary cohorts and no evaluable subgroup showed a credible decrement. It would not be described as a prospective risk model because biomarker timing did not establish a pre-event baseline. It would not be recommended for absolute-risk decisions unless calibration transported without target recalibration and decision curves compared genuine probabilities on the same scale.

The objectives were therefore to: (1) develop a de novo, low-dimensional classifier from raw clinical and apolipoprotein variables; (2) quantify reciprocal transport between a specialist FH clinic and genotype-first UK Biobank carriers; (3) compare performance with age plus sex and adapted Montreal-FH-SCORE, FH-Risk-Score, and SAFEHEART implementations; (4) assess calibration, missingness, endpoint, genetic-definition, and subgroup robustness; and (5) determine which positive and negative claims remained defensible after independent computational and reporting QC.

## Methods

### Study design and estimand

This was a retrospective cross-sectional case-identification and reciprocal-transport study. The estimand was the probability that established ASCVD was already recorded at the time represented by the available contemporary clinical and laboratory phenotype. It was not first-event incidence, five- or ten-year absolute risk, treatment benefit, or a causal effect of any biomarker. Contemporary lipid measurements could occur after ASCVD and after lipid-lowering treatment had been initiated or intensified. This temporal structure is a defining property of the estimand rather than a correctable modelling detail.

The analysis had two phases. Phase A tested whether discordance terms augmented a Montreal-based score architecture. After the investigator required a genuinely de novo model, Protocol Amendment 1 replaced score augmentation with ten raw-variable candidates. Phase A remained a diagnostic and is now explicitly labelled `phase_a_score_augmentation`; its selected `montreal_ratio` architecture is not CALON-N. The canonical Phase B record is `scratch_selection.json`, where “scratch” means from scratch. It contains exactly the ten candidates described below and selects `calon_n_apoa1`. No Phase A score or coefficient enters the Phase B model.

### Why this is not external validation

The protocol, Phase B candidates, sign rules, outcomes, metrics, subgroup event thresholds, and stopping rule were written before the Phase B run on 9 August 2026. However, earlier CALON programme analyses had already examined outcomes and predictors in both DRAGON and UK Biobank, and the maximin selection rule deliberately consumed outcome performance in both directions. Each final transport application used frozen source preprocessing and coefficients, but the architecture itself was selected with knowledge from both datasets. The correct design label is target-informed reciprocal multi-cohort development, or exploratory internal–external validation. It is not protected, independent external validation. Only a third cohort not used in any part of architecture development can provide that test.

### Data sources, dates, and participant flow

The DRAGON analytical file was obtained locally on 2 August 2026 and linked in memory to the canonical PASS registry during the locked analysis on 9 August 2026. The file contains a uniform administrative `TodayDate` of 5 August 2024 but does not preserve a validated single recruitment window or upstream export timestamp. Historical measurement dates span routine service care rather than a planned baseline visit. We therefore report the dates of the available analytical snapshots and analysis lock, not an unsupported recruitment period. The absence of a definitive source-data cut is a STROBE limitation requiring confirmation from the data custodian.

The UK Biobank master file contained baseline assessments from 13 March 2006 to 1 October 2010; all 890 strict carriers had baseline dates between 19 April 2007 and 22 September 2010. UK Biobank recruitment and resource design are described elsewhere.[13,14] The local full participant-to-variant call file was dated 19 March 2026, and the local ClinVar and VEP annotation exports were dated 8 June 2026. The upstream UK Biobank genomic release identifier and ClinVar release accession were not retained in the files. Reproducibility is therefore anchored to SHA-256 hashes of the exact local snapshots; release-matched replication by another group will require the custodian to restore the upstream release metadata.

DRAGON contributed 424 exported records. All 424 linked to PASS, 412 family labels agreed directly, and 12 were realigned using the canonical PASS family identifier. No participant was removed for missing predictors because missing values were completed using source-training data; all 424 entered every primary candidate, and 62 had the primary outcome. The final resampling unit was 219 families.

The UK Biobank call file contained 6,597,041 carrier–variant rows for 468,965 participants. Coordinate linkage identified 890 participants with at least one local ClinVar P/LP *LDLR* call and no locally conflicting call; all 890 linked to the master phenotype file and carried the local `ldlr_carrier` flag. Fifty-seven had prevalent ASCVD. Adding locally predicted loss-of-function calls produced a prespecified union of 1,264 participants and 80 cases. Again, source-training completion meant that all eligible participants entered each primary candidate. A participant flow and the exposure hierarchy are given in the Supplement.

### DRAGON specialist-clinic cohort

DRAGON comprised 424 genetically ascertained participants managed in a specialist Welsh FH service. The export included 202 columns spanning demographics, clinical history, routine lipids, apolipoproteins, Lp(a), treatment fields, family information, and recorded variants. The outcome flag identified 62 established ASCVD cases. The export contained clinically recorded variants or labels across *LDLR* (n=363), *APOB* (n=50), *PCSK9* (n=5), and other genes or labels. These counts describe the clinic export; they do not constitute a newly adjudicated molecular classification.

To test whether the broader clinic phenotype drove transport, we used a conservative archived exact-HGVS *LDLR* P/LP sensitivity. Local variant strings were normalised and matched to an archived ClinVar table only when a P/LP assertion with stated criteria was present and no VUS, benign/likely benign, or conflicting classification was recorded. This sensitivity contained 164 participants, 20 cases, and 79 families. It was not treated as the definitive clinic cohort because unparseable variants and variants absent from the archive cannot validly be reclassified as non-pathogenic.

### UK Biobank carrier definitions and dependence structure

The primary UK Biobank exposure was coordinate-verified local *LDLR* P/LP carrier status. Chromosome, position, reference, and alternate alleles were normalised across the complete call file and local ClinVar annotations. A participant was included if any qualifying P/LP call was present and no local conflicting call applied. ClinVar review status was unavailable in the local table, so “P/LP” denotes the study’s local classification rather than an exact reproduction of current ClinVar or blinded laboratory adjudication.

The union sensitivity added local ClinVar or VEP consequences consistent with predicted loss of function. The primary and union cohorts were clustered separately. We constructed a bipartite graph linking each participant only to qualifying variants for that definition and then identified connected components. This matters because UK Biobank carriers commonly had many non-qualifying calls; using an arbitrary first call would create incorrect bootstrap clusters. The corrected procedure yielded 62 components in the strict cohort and 66 in the union.

Exact published *LDLR* variants from Patel and Fahed were evaluated in a separate concordance programme to verify columns, variant bridging, untreated-LDL reconstruction, and the direction of the prevalent-inclusive ASCVD association.[11,12] Those external variant lists are benchmark controls, not substitute development cohorts. Likewise, the exploratory three-gene TUDOR label was excluded because its *APOB* and *PCSK9* entries provide gene labels without participant-level variant coordinates or pathogenicity provenance and overlap poorly with the coordinate-verified strict set.

### Outcome definition

The primary DRAGON outcome was the binary registry field `ASCVD_combined`. Among the 424 participants, component fields recorded myocardial infarction/acute coronary syndrome in 34, percutaneous coronary intervention in 21, coronary artery bypass grafting in 30, angina in 24, transient ischaemic attack in 9, and peripheral vascular disease in 4; components overlap. The union of these six fields identified 66 participants, whereas a hard-coronary union of myocardial infarction/acute coronary syndrome, coronary artery bypass grafting, or percutaneous coronary intervention identified 56. These were sensitivity outcomes because neither perfectly reproduced the registry flag.

The UK Biobank outcome was the preconstructed binary field `prevalent_ascvd`, positive in 57 strict and 80 union carriers. In the strict cohort, 96 participants had any `first_ascvd` date, of whom 57 were dated before baseline and 39 after baseline, consistent with the prevalent/incident split. Individual coronary, cerebrovascular, revascularisation, and peripheral-arterial components were not fully recoverable from the local proxy, and raw `first_angina` records were not equivalent to the composite. The common estimand is therefore recorded established ASCVD, not identical hard MACE. Outcome adjudication was not repeated blind to predictors.

### Candidate predictors

Candidate variables were chosen from clinically available measurements shared across cohorts and bounded to physiologically plausible ranges before modelling. Age was expressed in years. Sex was coded male versus female. Hypertension and ever smoking were binary source variables. HDL-C and LDL-C were in mmol/L, and apoB and apoA1 in g/L. The discordance term was the natural logarithm of apoB divided by LDL-C. Other prespecified transformations were natural-log TG/HDL-C, log(1+Lp(a)), log apoA1, log LDL-C, and an apoB-on-LDL residual estimated only in source-training observations with both biomarkers measured.

The ratio combines measurements with different conventional units and therefore has no simple unit-free clinical threshold. Its purpose was ranking within the locked equation. No claim is made that a particular apoB/LDL-C cut point is universally transportable. Lp(a) was retained in source units because source harmonisation was incomplete; it was eligible only as a candidate log term and as the previously specified 143-unit subgroup threshold, not as a cross-cohort causal dose.

### Locked Phase B candidate architectures

Ten low-dimensional candidates were prespecified: (1) age plus sex; (2) age, sex, and log(apoB/LDL-C); (3) age, sex, HDL-C, hypertension, and smoking; (4) candidate 3 plus log(apoB/LDL-C), termed CALON-N core; (5) core plus diabetes; (6) core plus log(TG/HDL-C); (7) core plus log Lp(a); (8) core plus log apoA1; (9) the five-variable clinical model plus log LDL-C and an apoB-on-LDL residual; and (10) age, sex, hypertension, and log(apoB/LDL-C), a parsimonious clinic candidate. Published scores and fitted comparator values were prohibited as inputs.

This set was intentionally small. DRAGON and strict UK Biobank contained 62 and 57 cases, respectively; a high-dimensional learner or unrestricted subset search could obtain an attractive apparent AUC while estimating an unstable decision boundary. Ridge penalisation and candidate-level restraint reduce, but do not eliminate, sparse-event optimism. The study used the available sample rather than an a priori model-development sample-size calculation. Accordingly, coefficient estimation and subgroup analysis remain exploratory.

### Missing data and preprocessing

For each source fit, missing raw predictors were replaced with medians estimated from the source-training data. The same source values were then used in the target; no target distribution or target outcome informed completion. Within grouped cross-validation, median estimation, transformation, scaling, residualisation, and penalty tuning were repeated inside the training partition. Binary variables were bounded to 0–1, age to 5–105 years, LDL-C to 0.3–20 mmol/L, HDL-C to 0.2–5 mmol/L, apoB to 0.2–4 g/L, apoA1 to 0.3–4 g/L, Lp(a) to 0–1,000 source units, and body mass index, used only by the SAFEHEART comparator, to 12–70 kg/m².

Median replacement was selected for determinism and transport transparency, not because missingness was assumed completely at random. ApoA1 was observed in 322/424 DRAGON participants and 785/890 strict UK Biobank carriers; apoB in 323/424 and 837/890; LDL-C in 402/424 and 850/890; and HDL-C in 398/424 and 786/890. Completion therefore affected a substantial minority, especially for apoA1 in DRAGON. Multiple imputation, imputation-model uncertainty, and assay-calibration models were not implemented and remain required sensitivities for a future prospective study.

### Model fitting, sign gate, and selection

Each candidate used L2-penalised logistic regression. Continuous and binary model columns were standardised using the source-training mean and standard deviation. The inverse regularisation parameter was chosen from C={0.01, 0.03, 0.10, 0.30, 1.00, 3.00} by the lowest grouped cross-validated Brier score. Family groups remained intact in DRAGON folds, and qualifying-variant connected components remained intact in UK Biobank folds.

Coefficient directions were prespecified as positive for age, male sex, hypertension, smoking, diabetes, apoB/LDL-C, TG/HDL-C, Lp(a), LDL-C, and positive apoB discordance, and negative for HDL-C and apoA1. A candidate was ineligible if any included term violated its direction in either source fit. Among eligible candidates, we selected the architecture with the largest minimum AUC across DRAGON-to-UK Biobank and UK Biobank-to-DRAGON transport, with mean reciprocal AUC as a tie-breaker. This maximin rule prevents a very strong result in one direction from masking failure in the other, but it directly consumes both outcome sets and is the reason the study is not independent validation.

Candidate-specific internal performance used five repeats of nested five-fold grouped validation. Within every outer-training partition, the penalty was retuned using four-fold grouped validation and all preprocessing was refitted. Predictions from the five repeats were rank-aggregated for a descriptive AUC. This procedure nests preprocessing and penalty tuning for a named candidate, but it does not nest the preceding ten-architecture cross-cohort choice. These AUCs are therefore not whole-process optimism-corrected estimates.

### Comparator definitions

Comparators were age plus sex, adapted Montreal-FH-SCORE, adapted FH-Risk-Score, and adapted SAFEHEART. All were calculated on the same target participants and compared with paired AUC differences. Montreal used its published coefficient pattern with age and HDL-C standardised to source-cohort anchors. FH-Risk-Score used the published categorical structure, but current LDL-C substituted where untreated LDL-C could not be recovered and the available Lp(a) variable was used with the local implementation threshold. SAFEHEART used available age, sex, hypertension, smoking, body mass index, LDL-C, and Lp(a), while previous ASCVD was omitted because it would be circular for a prevalent-ASCVD outcome.

The comparisons therefore test adapted implementations under the CALON-N cross-sectional estimand, not the exact published instruments under their intended prospective use. The adapted SAFEHEART AUC of 0.541 in UK Biobank is near chance. This likely reflects major endpoint and input adaptation, particularly removal of previous ASCVD, rather than intrinsic failure of SAFEHEART-RE. Comparator names are consequently accompanied by “adapted” throughout.

### Performance, uncertainty, and calibration

Discrimination was measured by the area under the receiver-operating-characteristic curve (AUC). Reciprocal transport applied the source-fitted median defaults, transformations, scaler, penalty, and coefficients without target refitting or recalibration. Target families or target qualifying-variant components were sampled with replacement 4,000 times. We calculated percentile 95% intervals for CALON-N AUC and paired differences from each comparator. These intervals respect observed target dependence and pairing, but condition on one fitted source model; they do not include source-sampling, candidate-selection, or annotation-release uncertainty.

Calibration was described using Brier score, Brier score relative to the target null prevalence model, calibration intercept, calibration slope, and expected:observed (E:O) ratio. A negative scaled Brier score indicates that transported probabilities were less accurate than assigning every target participant the observed target prevalence. Calibration curves used target prediction quintiles for description only. No intercept or slope was updated in the target.

### Withdrawal of decision-curve analysis at QC

A comparative decision-curve table was generated during development. Final QC established that CALON-N and adapted SAFEHEART produced probabilities, whereas age plus sex, Montreal, and FH-Risk-Score were ranking scores or linear predictors that had not been calibrated onto the same target probability scale. Applying identical probability thresholds to those quantities is invalid. The analysis was therefore marked `valid_for_comparator_inference=False`, all net-benefit claims were withdrawn, and no clinical threshold is proposed. This withdrawal was made before final manuscript interpretation.

### Subgroups and sensitivity analyses

Prespecified subgroups were sex, age below versus at or above the cohort median, recorded lipid treatment, diabetes, and Lp(a) below versus at or above 143 in source units. Subgroups did not influence architecture selection. A stratum with fewer than 10 cases was classified non-estimable; 10–19 cases was descriptive; at least 20 was evaluable. No interaction tests or subgroup-specific confidence intervals were estimated, so subgroup results assess stress and sparsity rather than effect modification or fairness.

Sensitivities included the P/LP-or-predicted-loss-of-function UK Biobank union; the conservative archived exact-HGVS *LDLR* P/LP DRAGON subset; the DRAGON component-union and hard-coronary outcomes; and complete-case transport among participants with all CALON-N inputs observed. The pooled research equation was fitted only after reciprocal transport and is provided to freeze a candidate for a third cohort. Its performance in the two development datasets is not an untouched validation result.

### Reproducibility, reporting, and governance

All analysis occurred locally. No participant identifier, family identifier, variant coordinate, participant row, or participant-level prediction was written to the package. The package contains aggregate tables, figures, source code, a deterministic model object, a synthetic input file, protocol and amendment, phase map, QC reports, and SHA-256 manifests. Synthetic scoring was invariant to repeated calls and row order.

Reporting was mapped item by item to TRIPOD+AI and the STROBE cross-sectional checklist, and risk of bias was appraised with PROBAST.[8–10] The local mapping is a transparency aid rather than formal certification. UK Biobank analyses were conducted under Application 1002450; UK Biobank has NHS National Research Ethics Service approval (North West–Haydock Research Ethics Committee, 11/NW/0382), and participants provided consent under UK Biobank governance. The exact Welsh service/registry approval, legal basis, consent or waiver, and R&D/information-governance reference were not recoverable from the supplied files and remain a hard author-completion item before submission.

## Results

### Cohort flow and contrasts

All 424 DRAGON records were linked and analysed, including 62 cases across 219 families. The strict UK Biobank coordinate bridge contributed 890/890 eligible carriers, including 57 cases across 62 qualifying-variant components. The union sensitivity contributed 1,264 carriers, 80 cases, and 66 components. Thus, missing laboratory data changed values through source-median completion but did not change the primary analysis denominators.

DRAGON participants were younger than strict UK Biobank carriers (mean 48.4±18.6 versus 57.3±8.0 years), were more frequently recorded as receiving lipid-lowering treatment (86.6% versus 40.6%), and had more than twice the prevalence of established ASCVD (14.6% versus 6.4%). These contrasts establish spectrum shift before any model is fitted. Descriptive details and biomarker coverage are reported in Table 1 and Supplementary Table S1.

| Characteristic | DRAGON | UKB strict LDLR P/LP | UKB P/LP-or-LoF |
|---|---:|---:|---:|
| Participants | 424 | 890 | 1,264 |
| Established ASCVD | 62 (14.6%) | 57 (6.4%) | 80 (6.3%) |
| Family/qualifying-variant components | 219 | 62 | 66 |
| Age, years | 48.4±18.6 | 57.3±8.0 | 57.0±8.1 |
| Male sex | 172 (40.6%) | 387 (43.5%) | 559 (44.2%) |
| Recorded lipid treatment | 367 (86.6%) | 361 (40.6%) | 458 (36.2%) |
| LDL-C, mmol/L | 4.70 [3.50, 6.00] | 3.86 [3.12, 4.66] | 3.76 [3.06, 4.52] |
| apoB, g/L | 1.28 [1.03, 1.57] | 1.12 [0.94, 1.32] | 1.09 [0.92, 1.29] |
| apoA1 observed | 322 (75.9%) | 785 (88.2%) | 1,114 (88.1%) |

### Candidate selection

The sign-coherent maximin rule selected the clinical core plus log apoA1, named CALON-N. Its source-fitted transport AUCs were 0.7672 from DRAGON to strict UK Biobank and 0.8481 in reverse, giving a minimum of 0.7672. The next candidates were core plus diabetes (minimum 0.7605), core plus Lp(a) (0.7591), and the core without the extra term (0.7567). The residual-discordance candidate had AUC 0.7586 into UK Biobank and 0.8219 into DRAGON but failed the sign gate because LDL-C was negative in both source fits. The TG/HDL-C candidate failed because that term was negative in the DRAGON source fit. These candidates remained tabulated rather than being silently discarded.

Age plus sex produced the lowest minimum reciprocal AUC (0.7319) because its AUC into UK Biobank was 0.7319. Yet in the reverse direction its AUC was 0.8950, higher than all ten fitted candidates. This contrast is central: a model can satisfy a transport-oriented maximin rule while a simpler predictor remains stronger in one receiving cohort.

### Candidate-specific internal validation

Repeated nested grouped AUC for CALON-N was 0.8932 in DRAGON and 0.7943 in strict UK Biobank. For age plus sex, the corresponding AUCs were 0.8858 and 0.7104; for the five-variable clinical model, 0.8906 and 0.7500; and for age plus sex plus the ratio, 0.8881 and 0.7964. In UK Biobank the smaller age/sex/ratio candidate had a marginally higher internal AUC than CALON-N, whereas CALON-N had the better locked reciprocal minimum. Because architecture selection was not nested, these values describe candidate-specific resampling rather than unbiased estimates of the whole development procedure.

### Frozen pooled research equation

The following equation was fitted after the transport analyses by pooling DRAGON and strict UK Biobank. It has no untouched validation, should not be used for clinical care, and must not be interpreted as a five- or ten-year risk equation. The reciprocal results used separate source-fitted models, not this pooled representation.

```text
logit(p_established_ASCVD) = -5.673054
  + 0.112263 × age_years
  + 0.580373 × male
  - 0.629887 × HDL_C_mmol_L
  + 0.105120 × hypertension
  + 0.143724 × ever_smoker
  + 1.910359 × log(apoB_g_L / LDL_C_mmol_L)
  - 1.672421 × log(apoA1_g_L)
```

The coefficient signs matched the lock. Purely descriptively, the penalised pooled coefficients correspond to an odds ratio of 3.07 per 10 years of age, 1.79 for male sex, 0.53 per 1 mmol/L higher HDL-C, 3.76 per doubling of apoB/LDL-C, and 0.31 per doubling of apoA1. These translations have no coefficient confidence intervals, mix cross-sectional association with treatment and ascertainment, and are not causal effect estimates.

### DRAGON-to-UK Biobank transport

With coefficients and preprocessing fitted in DRAGON, CALON-N achieved AUC 0.7672 (95% CI 0.7117–0.8282) in 890 strict UK Biobank carriers. Adapted Montreal achieved 0.7747, a CALON-N difference of −0.0075 (−0.0365 to 0.0073). The data therefore do not establish either superiority or equivalence to Montreal. CALON-N exceeded age plus sex by 0.0353 (0.0179–0.0605), adapted FH-Risk-Score by 0.0710 (0.0237–0.1101), and adapted SAFEHEART by 0.2265 (0.1216–0.2936) on the conditional target-component bootstrap.

The UK Biobank union produced nearly the same CALON-N AUC, 0.7673 (0.7187–0.8129). Montreal achieved 0.7680, difference −0.0007 (−0.0247 to 0.0100). CALON-N remained above age plus sex by 0.0234 (0.0018–0.0457), adapted FH-Risk-Score by 0.0710 (0.0358–0.1001), and adapted SAFEHEART by 0.2396 (0.1543–0.2954). Broadening the local carrier definition therefore changed sample size and precision more than point discrimination.

### UK Biobank-to-DRAGON transport

Age plus sex alone ranked established ASCVD most strongly in DRAGON, with AUC 0.8950. Adapted Montreal was next at 0.8928, followed by adapted FH-Risk-Score at 0.8570, CALON-N at 0.8481 (95% CI 0.7956–0.8963), and adapted SAFEHEART at 0.7997. CALON-N was lower than age plus sex by −0.0469 (−0.1004 to 0.0025) and lower than Montreal by −0.0448 (−0.0927 to −0.0024). It was not separable from FH-Risk-Score (−0.0089, −0.0705 to 0.0505) or SAFEHEART (+0.0483, −0.0305 to 0.1298).

| Target and source fit | CALON-N AUC (95% CI) | Difference vs age+sex | Difference vs Montreal | Difference vs FH-RS | Difference vs SAFEHEART |
|---|---:|---:|---:|---:|---:|
| UKB strict; DRAGON fit | 0.767 (0.712–0.828) | +0.035 (+0.018,+0.060) | −0.008 (−0.036,+0.007) | +0.071 (+0.024,+0.110) | +0.227 (+0.122,+0.294) |
| DRAGON; UKB strict fit | 0.848 (0.796–0.896) | −0.047 (−0.100,+0.003) | −0.045 (−0.093,−0.002) | −0.009 (−0.071,+0.050) | +0.048 (−0.030,+0.130) |
| UKB union; DRAGON fit | 0.767 (0.719–0.813) | +0.023 (+0.002,+0.046) | −0.001 (−0.025,+0.010) | +0.071 (+0.036,+0.100) | +0.240 (+0.154,+0.295) |

### Calibration and overall accuracy

Discrimination transported more successfully than probability. In strict UK Biobank, the DRAGON-fitted model had Brier score 0.0823 versus a null Brier of 0.0599, yielding a scaled Brier score of −37.3%. Its calibration intercept was −1.446, slope 0.951, and E:O 3.004. On aggregate, an apparent CALON-N probability of 15% would therefore correspond to roughly 5% observed prevalence, although dividing an individual probability by three is not a valid recalibration method.

In DRAGON, the UK Biobank-fitted model had Brier score 0.1115 versus a null Brier of 0.1248, scaled Brier +10.7%, calibration intercept +0.657, slope 0.752, and E:O 0.447. It predicted fewer than half the observed cases. The opposite intercept errors are consistent with the difference in case prevalence and ascertainment, while the slopes show that a single intercept update would not fully repair transport. The union results were similar to strict UK Biobank: Brier 0.0828, scaled Brier −39.7%, intercept −1.486, slope 0.929, and E:O 3.047.

No comparative decision-curve result is reported. Because the invalid table used heterogeneous score scales as if they were probabilities, neither a treatment threshold nor a referral threshold can be inferred from it. Marked calibration drift independently prevents clinical threshold recommendations.

### Sensitivity analyses

In the conservative exact-HGVS *LDLR* P/LP DRAGON subset, UK Biobank-fitted CALON-N achieved AUC 0.8267 among 164 participants and 20 cases. The estimate was lower than in full DRAGON but remains imprecise because the sensitivity excludes unparseable and archive-absent clinic variants. Using the DRAGON component-union outcome produced AUC 0.8473 with 66 cases; the hard-coronary outcome produced 0.8429 with 56 cases. These results do not suggest that the primary reverse-transport AUC was driven by one outcome coding choice.

Complete-case transport was more sensitive. DRAGON-to-UK Biobank complete-case analysis included 726 participants and 50 cases and yielded AUC 0.7530, below the completed-data result of 0.7672. Reverse complete-case analysis included only 304 DRAGON participants and 45 cases but yielded AUC 0.8910, compared with 0.8481 after source-median completion. Thus, missingness and assay availability materially contributed to directional transport, particularly in DRAGON, but complete cases also select a smaller and potentially different clinic subset. Neither approach removes missing-not-at-random bias.

### Subgroup stress tests

Twenty subgroup rows were attempted; six contained fewer than 10 cases and were non-estimable. Of the remaining 14 evaluable or descriptive rows, CALON-N exceeded the best comparator in one: UK Biobank women, by 0.0049. It did not exceed the best comparator in any DRAGON subgroup.

In strict UK Biobank, CALON-N was below the best comparator among men (0.708 versus 0.715), participants aged at or above the median (0.663 versus 0.667), treated carriers (0.659 versus 0.672), participants with diabetes (0.690 versus 0.708; descriptive), participants without diabetes (0.767 versus 0.773), and those with Lp(a)<143 (0.740 versus 0.751). In DRAGON, deficits were larger in men (0.845 versus 0.914), women (0.842 versus 0.894), treated participants (0.837 versus 0.889), and those without diabetes (0.842 versus 0.896). The Lp(a)-high DRAGON stratum, where a discordance-based model might be expected to help, showed 0.869 versus 0.872. These are sparse descriptive comparisons without interaction inference; they reject an all-subgroup claim but do not prove biological effect modification.

## Discussion

### Principal findings

CALON-N is de novo in the strict architectural sense: seven terms were fitted from raw clinical and laboratory measurements, and no published risk score or fitted comparator enters the equation. It retained moderate-to-high discrimination when transported in both directions, with AUC 0.767 from the specialist clinic into strict UK Biobank carriers and 0.848 in reverse. In UK Biobank it ranked cases better than age plus sex and the adapted FH-Risk-Score and SAFEHEART implementations, while remaining close to Montreal. It did not outperform all comparators in both directions. In DRAGON, age plus sex alone had the highest point AUC, Montreal was significantly higher on the conditional family bootstrap, absolute probabilities failed in opposite directions, and 13 of 14 estimable or descriptive subgroup rows did not beat the best comparator.

The study supports a narrow conclusion: apoB/LDL-C and apoA1 can contribute to a coherent cross-sectional classifier across genetically defined FH settings, but additional laboratory detail does not guarantee better ranking than age and sex in a selected clinic. CALON-N is hypothesis-generating, not a validated clinical calculator.

### Interpreting apoB–LDL discordance

The selected positive apoB/LDL-C term is compatible with a particle–cholesterol discordance hypothesis. At a given measured LDL-C, a higher apoB concentration can indicate more atherogenic particles carrying less cholesterol per particle. This can be relevant when LDL-C appears controlled but particle burden remains elevated.[7] The protective apoA1 coefficient is also directionally consistent with long-term population evidence relating higher apoA1 and lower apoB/apoA1 balance to lower cardiovascular risk.[19]

The present data cannot isolate that biology. In DRAGON, the blood phenotype is contemporary and may follow both disease and treatment. Intensive lipid lowering can reduce LDL-C more than apoB, mechanically increasing apoB/LDL-C. Individuals with established ASCVD are also more likely to receive intensive therapy. Consequently, the ratio may identify people whose clinical history led to treatment, rather than predicting the history from a pre-event exposure. This is reverse causation and confounding by treatment indication, not necessarily a false association. It means the association answers a different question: whether a contemporary phenotype helps identify already-recorded disease.

The ratio also shares LDL-C in its denominator with an important treatment target. A strong ratio coefficient does not show that apoB is superior to LDL-C in every representation. Indeed, the residual-discordance candidate, which preserved LDL-C and represented apoB orthogonally to source LDL-C, produced an incoherent negative LDL-C coefficient and failed the locked sign gate. That failure is informative. It suggests that the data do not stably separate an LDL-C effect from discordance under this cross-sectional, treated design.

### Why transport was asymmetric

At least five between-cohort differences can produce the observed asymmetry.

1. **Age and disease accumulation.** UK Biobank carriers were about nine years older on average, whereas all 62 DRAGON cases fell in the older half of that cohort. Age therefore carried exceptional rank information in the clinic target, allowing age plus sex to reach AUC 0.895.
2. **Ascertainment.** DRAGON represents recognised specialist-clinic FH, including phenotype-referred probands and family-linked relatives. UK Biobank represents volunteer, population-based, genotype-first ascertainment. The relation between measured phenotype and disease status need not be invariant across those routes.
3. **Treatment recognition.** Recorded lipid treatment was 86.6% in DRAGON and 40.6% in strict UK Biobank, with different source fields and uncertain timing. A ratio affected by therapy will shift differently across these settings.
4. **Genetic spectrum.** DRAGON contains clinically recorded *LDLR*, *APOB*, *PCSK9*, and other labels, whereas the primary UK Biobank analysis is local coordinate-verified *LDLR* P/LP. Variant severity, review provenance, and family sharing differ.
5. **Phenotype and endpoint timing.** DRAGON biomarkers and diagnoses derive from routine service history; UK Biobank biomarkers are anchored to recruitment and prevalence to linked pre-baseline records. Endpoint components are not identical.

These differences violate the strong conditional-invariance assumption required for simple model transport: that disease status has the same relation to the included predictors in source and target. Reciprocal fitting reveals this rather than resolving it. The model that travels from clinic to biobank need not be the model that travels from biobank to clinic.

### Calibration failure is the clearest negative result

The most decisive result is not an AUC difference but the E:O reversal. DRAGON-derived probabilities overpredicted UK Biobank cases threefold and had a Brier score worse than the constant target prevalence. UK Biobank-derived probabilities underpredicted DRAGON cases by more than half. Calibration slopes of 0.95 and 0.75 indicate that both baseline odds and predictor effects changed. A local intercept correction might fix average prevalence but would not necessarily fix risk spread, missingness, or individual calibration.

This failure has direct clinical implications. A score can rank two people correctly while assigning both the wrong absolute probabilities. Any decision threshold—whether for imaging, treatment intensification, or specialist review—depends on calibrated probabilities and the consequences of false positives and false negatives. Because those requirements were not met, target recalibration was deliberately not used to rescue the main result, and the invalid comparative decision curve was withdrawn. CALON-N cannot currently guide care.

### The apoA1 term and missing data

Log apoA1 improved the prespecified minimum reciprocal AUC and retained a protective coefficient in both source fits. Its inclusion distinguishes CALON-N from the conventional FH comparators, but it should be considered provisional. HDL-C and apoA1 overlap biologically and statistically, so their coefficients are conditional on each other and ridge shrinkage. Approximately one quarter of DRAGON lacked apoA1, and source-median replacement assigned the same completed value to those participants. This preserves sample size and prevents target leakage but suppresses imputation uncertainty and can attenuate or distort conditional associations.

The complete-case analyses show that this choice matters. Reverse transport increased from AUC 0.848 to 0.891 in a much smaller subset with complete laboratory data. That difference could reflect better measurement, selection of a clinic subgroup, or both. Multiple imputation with compatible transformations, predictive mean matching or robust continuous models, inclusion of outcome information within training-fold imputation where appropriate, and full pipeline repetition across imputations are the obvious untested sensitivities. They should be prespecified in the next study rather than used now to choose a better-looking result.

### What the UK Biobank exposure audit establishes

First, the coordinate bridge is technically credible for the primary local definition. The complete 6.6-million-row call file, rather than a 3,094-row annotated subset, was linked to local ClinVar and VEP tables. All 890 strict and 1,264 union carriers linked to the phenotype master. Bootstrap dependence was reconstructed from shared qualifying variants rather than arbitrary non-qualifying calls. These steps solve earlier exposure-linkage and clustering errors.

Second, exact published-variant benchmarks provided a positive control outside model selection. When the analysis used externally listed Patel *LDLR* variants and a prevalent-inclusive covariate structure, the observed association was concordant with Patel’s *LDLR*-specific estimate. This supports use of the participant identifier, variant-coordinate columns, and broad ASCVD fields. It does not prove that the local P/LP definition is laboratory adjudicated, nor that CALON-N replicates Patel or Fahed.[11,12]

Third, neither exercise validates the exploratory three-gene TUDOR label. Its correct denominator is 426,731 participants with exposure records, not the 501,936-person phenotype master, and its *APOB* and *PCSK9* labels lack variant-level pathogenicity evidence in the available file. The non-overlap between raw *APOB* call participants and TUDOR-labelled *APOB* participants suggests a different upstream release or construction. Mixing a stringent *LDLR* definition with less-stringent gene flags can dilute or otherwise distort association. CALON-N therefore uses the auditable *LDLR* cohort and describes the three-gene result only as exploratory context.

### Comparators and the information ceiling

The comparator results require symmetry of criticism. CALON-N was developed under the current outcome, while Montreal, FH-Risk-Score, and SAFEHEART were adapted away from their original settings. The excellent Montreal performance in DRAGON is unsurprising because its variables—especially age—map closely to prevalent disease in specialist FH cohorts.[4,15,16] The lower adapted FH-Risk-Score and SAFEHEART AUCs in UK Biobank should not be read as evidence that those prospective tools fail clinically. Untreated LDL-C was unavailable, Lp(a) units were not fully harmonised, previous ASCVD was removed from SAFEHEART, and the endpoint was prevalent rather than incident disease.

There is also an information asymmetry. FH-Risk-Score estimated seven coefficients using 3,881 adults and 32,361 person-years, whereas each CALON-N source contained fewer than 65 cases.[5] A small new cohort cannot reliably out-estimate a large multi-registry derivation simply by changing algorithms. The current study instead asks whether raw apolipoprotein terms survive a harsh reciprocal transport test. Their survival at AUC 0.767 and 0.848 is scientifically interesting; their inability to dominate a strong age-based comparator is equally important.

### Novelty and relation to previous work

The biological premise that apoB reflects particle number, that apoB/LDL-C discordance may reveal residual risk, and that apoA1 is inversely associated with ASCVD is not new.[7,17–19] The same DRAGON participants contributed to the earlier hypothesis-generating discordance report, so this is not an independent biological replication.[17,18] Nor is CALON-N the first FH risk instrument: Montreal, SAFEHEART, and FH-Risk-Score are established.[4–6]

The defensible novelty is methodological and incremental. CALON-N is a de novo raw-variable equation that combines log(apoB/LDL-C) with log apoA1 without importing a published score; tests one architecture in reciprocal clinic-to-biobank and biobank-to-clinic transport; preserves family and shared-variant dependence; uses a locked physiological sign gate; and reports the failure of calibration and subgroup universality alongside discrimination. Targeted searches of PubMed and multiple scholarly indexes through 9 August 2026 identified apolipoprotein association studies, general-population apoB model extensions, and FH score validations, but no clearly matching FH-specific raw-apolipoprotein model evaluated by reciprocal specialist-clinic/population-biobank transport. Because this was not a formal systematic review, we avoid an absolute “first” claim.

### Confidence in the findings

Confidence is high that the locked files reconstruct the stated cohorts, that family realignment and qualifying-variant clustering are correct, that the scorer is deterministic, and that the stated algorithm selects CALON-N. All canonical input hashes matched, the primary counts reproduced, comparator deltas were arithmetically exact, the model and equation used the same features, and repeated or row-reversed synthetic scoring differed by zero.

Confidence is moderate in the conditional AUCs within these datasets: intervals respect target clustering, and main results were stable to the UK Biobank union and alternative DRAGON outcomes. Confidence is lower for adapted-comparator contrasts, very low for subgroups, absent for absolute-risk use, and low for a third registry. A non-significant Montreal difference is not equivalence.

PROBAST risk of bias is high, with high applicability concern for prospective prediction or deployment. That judgement is not contradicted by reproducible computation. Reproducibility asks whether the same operations return the same answer; risk-of-bias assessment asks whether that answer estimates the intended quantity without important systematic error. CALON-N performs better on the first question than the second.

### Strengths

Strengths include complete DRAGON-to-PASS linkage and family realignment; use of the full UK Biobank participant-to-variant call file; explicit separation of local P/LP, P/LP-or-LoF, exact-published-variant, and exploratory gene-label definitions; corrected qualifying-variant connected components; raw-variable rather than score-stack development; fold-local completion, transformation, scaling, residualisation, and tuning; nested grouped evaluation for each candidate; reciprocal transport without target recalibration; conditional paired bootstrap intervals; prespecified sign and subgroup rules; complete reporting of failed candidate signs and negative subgroup findings; deterministic scoring; aggregate-only outputs; and withdrawal of an invalid decision-curve analysis during QC.

### Limitations and possible bias

Eight limitations define the interpretation. First, architecture selection was target-informed. Both outcome sets and substantial earlier programme knowledge influenced the final question, so reciprocal transport cannot be presented as protected validation and performance is likely optimistic for a new setting.

Second, the event information was limited: 62 DRAGON and 57 strict UK Biobank cases supported seven terms, penalty tuning, ten architecture comparisons, two directions, and 20 subgroup attempts. Ridge shrinkage and event thresholds reduce instability but do not account for whole-process selection or multiplicity. The target bootstrap omits source-development and selection uncertainty.

Third, missing data were handled by single source-median replacement. This is deterministic and avoids direct target leakage, but assumes the source median is transportable, understates uncertainty, ignores multivariable relations, and is especially consequential for the 24.1% of DRAGON participants without apoA1. Complete-case analysis is not an unbiased remedy.

Fourth, the source populations have substantial spectrum and survivor bias. DRAGON is a treated specialist service; UK Biobank is a volunteer cohort of middle-aged and older adults. Fatal early FH events are absent, clinically severe probands may be overrepresented in the clinic, and healthy-volunteer selection may be stronger in the biobank. These processes can change both prevalence and predictor–outcome relations.

Fifth, outcome definitions and timing were not centrally adjudicated or perfectly harmonised. The registry flag did not equal the union of its visible components, and the UK Biobank proxy did not recover every revascularisation or peripheral-arterial component. Misclassification could be differential by setting and may influence both AUC and calibration.

Sixth, genetic definitions differed. UK Biobank primary exposure was local *LDLR* P/LP without review-status enforcement, while DRAGON contained a broader clinically recorded genetic spectrum. Archived exact-HGVS and published-variant sensitivities improve auditability but do not substitute for contemporary blinded molecular adjudication across all three canonical FH genes.

Seventh, comparator fairness is limited. Montreal, FH-Risk-Score, and SAFEHEART were adapted to available variables and a cross-sectional outcome. The near-chance adapted SAFEHEART result is not a valid judgement on the published prospective instrument, and the current comparison cannot establish clinical superiority.

Eighth, ancestry, socioeconomic context, laboratory platforms, treatment timing, and patient/public priorities were insufficiently characterised. The cohorts are predominantly White European, fairness across ancestry or deprivation was not estimated, and the Welsh recruitment/data-cut, ethics, assay, and outcome-adjudication metadata require completion. These gaps limit reproducibility across laboratories and services even when code is available.

### Next study

The next study should freeze CALON-N before accessing any third cohort and recruit or identify a prospective FH registry with dated pre-event apoB, LDL-C, apoA1, HDL-C, blood pressure, smoking, treatment, genotype, and ascertainment route. It should use adjudicated incident ASCVD, a stated time zero, censoring and competing death, and a prespecified prediction horizon. Families and shared variants must remain intact across resampling. Missing values should be addressed with multiple imputation inside the full validation pipeline, and uncertainty should repeat imputation, preprocessing, model fitting, and any updating within each cluster bootstrap.

That study should compare frozen CALON-N transport, ordinary local recalibration, and a separately specified incident-risk model. Every comparator must express probability at the same horizon before calibration or decision analysis. Only acceptable discrimination, calibration, and net benefit in that untouched setting would justify a simplified implementation or clinical impact trial.

## Conclusions

CALON-N is a novel, sign-coherent, raw-variable classifier for established ASCVD in genetically defined FH. It transported with AUCs of 0.767 and 0.848, but did not beat Montreal, age plus sex, or every comparator across directions and subgroups, and its absolute probabilities did not transport. The model should remain frozen as a research hypothesis for a prospective FH registry with pre-event apoB, LDL-C, apoA1, a dated baseline, and adjudicated follow-up—not promoted as a ten-year risk score or clinical tool.

## Declarations

**Ethics and data governance:** UK Biobank analyses were conducted under Application 1002450. UK Biobank has approval from the NHS National Research Ethics Service North West–Haydock Research Ethics Committee (11/NW/0382), and participants provided consent under UK Biobank governance. The authors must insert and verify the full Welsh PASS/DRAGON approval or service-evaluation determination, consent or waiver, UK GDPR legal basis, data controller, and R&D/information-governance reference before submission. Only aggregate, de-identified results are reported.

**Funding:** No dedicated external grant funding is declared for the analyses reported here. Cohort access, data governance, and analyses were supported through routine academic and clinical research activity within Cardiff and Vale University Health Board, the All-Wales Familial Hypercholesterolaemia Service, and UK Biobank Application 1002450. All authors must confirm this statement before submission.

**Conflicts of interest:** The authors declare no relevant conflicts of interest for this work. Each author must complete the journal’s individual disclosure form before submission.

**Patient and public involvement:** Patient or public involvement was not documented in the supplied analysis records. The corresponding author must either confirm that patients and the public were not involved in study design, analysis, interpretation, or writing, or replace this sentence with an accurate description before submission.

**Author contributions:** To be completed by the author group using the CRediT taxonomy before submission; contributions cannot be inferred safely from the analytical files.

**Data availability:** Participant-level NHS Wales and UK Biobank data cannot be redistributed. Aggregate outputs, source code, deterministic model object, synthetic input, protocol, phase map, QC reports, and checksum manifest are available in the governed analysis package, subject to institutional and UK Biobank requirements.

**Generative-AI disclosure:** Generative-AI-assisted tools were used for code review, literature retrieval support, document structuring, and language editing. No participant-level data were transmitted to a generative-AI service. The authors must verify the analyses, references, declarations, and final wording and accept responsibility for the manuscript.

## References

1. Beheshti SO, Madsen CM, Varbo A, Nordestgaard BG. Worldwide prevalence of familial hypercholesterolemia: meta-analyses of 11 million subjects. *J Am Coll Cardiol.* 2020;75:2553–2566. doi:10.1016/j.jacc.2020.03.057.
2. Ference BA, Ginsberg HN, Graham I, et al. Low-density lipoproteins cause atherosclerotic cardiovascular disease. *Eur Heart J.* 2017;38:2459–2472. doi:10.1093/eurheartj/ehx144.
3. Khera AV, Won HH, Peloso GM, et al. Diagnostic yield and clinical utility of sequencing familial hypercholesterolemia genes in patients with severe hypercholesterolemia. *J Am Coll Cardiol.* 2016;67:2578–2589. doi:10.1016/j.jacc.2016.03.520.
4. Paquette M, Dufour R, Baass A. The Montreal-FH-SCORE: a new score to predict cardiovascular events in familial hypercholesterolemia. *J Clin Lipidol.* 2017;11:80–86. doi:10.1016/j.jacl.2016.10.004.
5. Paquette M, Bernard S, Cariou B, et al. Familial Hypercholesterolemia-Risk-Score: a new score predicting cardiovascular events and cardiovascular mortality in familial hypercholesterolemia. *Arterioscler Thromb Vasc Biol.* 2021;41:2632–2640. doi:10.1161/ATVBAHA.121.316106.
6. Pérez de Isla L, Alonso R, Mata N, et al. Predicting cardiovascular events in familial hypercholesterolemia: the SAFEHEART Registry. *Circulation.* 2017;135:2133–2144. doi:10.1161/CIRCULATIONAHA.116.024541.
7. Sniderman AD, Thanassoulis G, Glavinovic T, et al. Apolipoprotein B particles and cardiovascular disease: a narrative review. *JAMA Cardiol.* 2019;4:1287–1295. doi:10.1001/jamacardio.2019.3780.
8. Collins GS, Moons KGM, Dhiman P, et al. TRIPOD+AI statement: updated guidance for reporting clinical prediction models that use regression or machine learning methods. *BMJ.* 2024;385:e078378. doi:10.1136/bmj-2023-078378.
9. Wolff RF, Moons KGM, Riley RD, et al. PROBAST: a tool to assess the risk of bias and applicability of prediction model studies. *Ann Intern Med.* 2019;170:51–58. doi:10.7326/M18-1376.
10. von Elm E, Altman DG, Egger M, et al. The Strengthening the Reporting of Observational Studies in Epidemiology (STROBE) statement. *PLoS Med.* 2007;4:e296. doi:10.1371/journal.pmed.0040296.
11. Patel AP, Wang M, Fahed AC, et al. Association of rare pathogenic DNA variants for familial hypercholesterolemia, hereditary breast and ovarian cancer syndrome, and Lynch syndrome with disease risk in adults according to family history. *JAMA Netw Open.* 2020;3:e203959. doi:10.1001/jamanetworkopen.2020.3959.
12. Fahed AC, Wang M, Patel AP, et al. Association of the interaction between familial hypercholesterolemia variants and adherence to a healthy lifestyle with risk of coronary artery disease. *JAMA Netw Open.* 2022;5:e222687. doi:10.1001/jamanetworkopen.2022.2687.
13. Sudlow C, Gallacher J, Allen N, et al. UK Biobank: an open access resource for identifying causes of disease. *PLoS Med.* 2015;12:e1001779. doi:10.1371/journal.pmed.1001779.
14. Bycroft C, Freeman C, Petkova D, et al. The UK Biobank resource with deep phenotyping and genomic data. *Nature.* 2018;562:203–209. doi:10.1038/s41586-018-0579-z.
15. Paquette M, Brisson D, Dufour R, et al. Cardiovascular disease in familial hypercholesterolemia: validation and refinement of the Montreal-FH-SCORE. *J Clin Lipidol.* 2017;11:1161–1167.e3. doi:10.1016/j.jacl.2017.07.008.
16. Tamehri Zadeh SS, Chan DC, Pang J, et al. Canadian and French risk scores are valid in identifying cardiovascular disease in Australian patients with familial hypercholesterolemia. *Can J Cardiol.* 2025;41:2244–2251. doi:10.1016/j.cjca.2025.07.042.
17. Genedy N, Zouwail S. ApoB/LDL-C discordance as a predictor of atherosclerotic cardiovascular disease in genetically confirmed heterozygous familial hypercholesterolemia: a hypothesis-generating cohort study. *J Clin Lipidol.* 2026;20:490–503. doi:10.1016/j.jacl.2025.11.008.
18. Correction to “ApoB/LDL-C discordance as a predictor of atherosclerotic cardiovascular disease in genetically confirmed heterozygous familial hypercholesterolemia: a hypothesis-generating cohort study.” *J Clin Lipidol.* 2026. doi:10.1016/j.jacl.2026.03.024.
19. Walldius G, de Faire U, Alfredsson L, et al. Long-term risk of a major cardiovascular event by apoB, apoA1, and the apoB/apoA1 ratio: experience from the Swedish AMORIS cohort. *PLoS Med.* 2021;18:e1003853. doi:10.1371/journal.pmed.1003853.
