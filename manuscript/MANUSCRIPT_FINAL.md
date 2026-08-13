# Apolipoprotein B–LDL discordance identifies established cardiovascular disease in genetically defined familial hypercholesterolaemia, but absolute risk does not transport between clinic and biobank

> ## ⚠ CONTAINS RETRACTED RESULTS — NOT A SUBMISSION DRAFT
>
> This document reports the **cross-sectional UK Biobank arm**, retracted on
> 11 August 2026 for outcome-to-predictor temporality reversal: 100% of prevalent
> ASCVD events pre-dated the blood draw, and `pre_ldl.fillna(ldl_chem)` restored
> post-event, on-treatment lipids for every case. The figures **0.7605, 0.767,
> 0.848 and 0.7672**, the 890/57 cohort and the 15 UK Biobank head-to-head
> comparisons are withdrawn and must not be cited as findings.
>
> It is retained as the provenance record of what was believed at the time.
> The current analysis is **CALON-F** (`code/15_CALON_FINAL.py`). See
> [STATUS.md](STATUS.md) — from `manuscript/`, [../STATUS.md](../STATUS.md).

Short title: CALON-N in genetically defined familial hypercholesterolaemia

Article type: Original Research

Target journal: *Journal of Clinical Lipidology*

## Highlights

- CALON-N is a seven-variable classifier fitted from raw clinical and laboratory measurements; no published score is a model input.
- Selected predictors were age, sex, HDL-C, hypertension, smoking, log(apoB/LDL-C), and log(apoA1).
- Discrimination transported asymmetrically, being lower into the biobank: AUC 0.767 from clinic to UK Biobank and 0.848 in reverse.
- CALON-N exceeded adapted FH-Risk-Score and SAFEHEART in UK Biobank but not Montreal-FH-SCORE; in the clinic, age plus sex alone outperformed every fitted candidate.
- Absolute probabilities failed in opposite directions (expected:observed 3.00 and 0.45); post-event biomarkers and target-informed selection prohibit prospective-risk or deployment claims.

## Abstract

**Background:** Existing familial hypercholesterolaemia (FH) instruments use conventional lipids and were developed for different outcomes in clinically ascertained cohorts. We found no FH-specific instrument developed from raw apolipoprotein B (apoB), LDL cholesterol (LDL-C), and apolipoprotein A1 (apoA1) measurements and evaluated by reciprocal transport between clinical and population-biobank settings.

**Methods:** This retrospective cross-sectional model-development study used DRAGON, a genetically ascertained specialist-clinic cohort (424 participants; 62 established atherosclerotic cardiovascular disease [ASCVD] cases; 219 families), and a primary UK Biobank cohort of coordinate-linked *LDLR* carriers with a local ClinVar pathogenic/likely pathogenic classification (890 participants; 57 cases; 62 qualifying-variant components). Ten low-dimensional penalised-logistic architectures using raw variables only were prespecified; published FH scores were comparators, not inputs. Eligible architectures required physiologically coherent coefficient directions in both source fits. The model maximising the lower of the two reciprocal-transport areas under the curve (AUCs) was selected. Uncertainty used 4,000 target family- or variant-component bootstrap samples.

**Results:** CALON-N contained age, male sex, HDL-C, hypertension, ever smoking, log(apoB/LDL-C), and log(apoA1). With clinic-fitted coefficients, UK Biobank AUC was 0.767 (95% CI 0.712–0.828); with UK Biobank-fitted coefficients, clinic AUC was 0.848 (0.796–0.896). In UK Biobank, CALON-N exceeded adapted FH-Risk-Score by 0.071 (0.024–0.110) and adapted SAFEHEART by 0.227 (0.122–0.294), but not Montreal-FH-SCORE (−0.008, −0.036 to 0.007). In the clinic, age plus sex (0.895) and Montreal (0.893) both exceeded CALON-N; the Montreal difference was −0.045 (−0.093 to −0.002). Calibration did not transport: expected:observed ratios were 3.00 and 0.45. CALON-N exceeded the best comparator in one of 14 estimable subgroup analyses. Against 4,450 age- and sex-matched UK Biobank non-carriers, discrimination was largely genotype-independent (0.795 transported versus 0.840 internal), but a model fitted in non-carriers under-predicted carrier risk by 31% (expected:observed 0.69, 0.55–0.90) and a carrier-fitted model over-predicted non-carrier risk by 51% (1.51, 1.32–1.75).

**Conclusions:** A de novo apoB-discordance model was feasible and retained moderate-to-high discrimination across two genetically defined FH settings, but did not outperform all comparators or transport absolute probabilities. The data reject universal-superiority and prospective-risk claims. CALON-N is a research classifier requiring validation with pre-event apolipoproteins in an independent FH registry.

Keywords: familial hypercholesterolaemia; apolipoprotein B; apolipoprotein A1; LDL cholesterol; ascertainment; prediction model; transportability; UK Biobank

## Introduction

Heterozygous familial hypercholesterolaemia (HeFH) is an autosomal codominant disorder characterised by lifelong exposure to elevated LDL-C and substantially increased risk of premature ASCVD.[1–6] Detection remains incomplete in most health systems, and cascade testing now supplies a growing share of newly identified carriers.[2–4] The average risk is high, but the distribution of risk is wide. Age at diagnosis, sex, smoking, blood pressure, diabetes, the severity and duration of LDL exposure, lipoprotein(a) [Lp(a)], treatment history, genotype, and the route through which a person enters care all contribute. A clinic-referred index case with symptomatic coronary disease is therefore not interchangeable with an asymptomatic relative identified by cascade testing or a carrier discovered through population sequencing.

Several FH-specific instruments organise this heterogeneity differently. Montreal-FH-SCORE was developed to identify prevalent cardiovascular disease using age, sex, HDL-C, hypertension, and smoking, and was subsequently validated and refined.[8,9] FH-Risk-Score was derived in 3,881 adults without previous ASCVD from five registries contributing 32,361 person-years; it predicts incident ASCVD using age, sex, HDL-C, untreated or imputed untreated LDL-C, hypertension, smoking, and Lp(a).[10] SAFEHEART-RE predicts incident events in a prospective Spanish registry and gives previous ASCVD a major role.[11] Montreal and FH-Risk-Score were recently evaluated cross-sectionally in an Australian specialist FH cohort, demonstrating that a score performs differently when endpoint and ascertainment change.[12] Their distinct intended populations, endpoints, time origins, predictor definitions, and baseline hazards make comparative transport a scientific question rather than a leaderboard. That transport is not assured: applied to an English routine-care FH population, SAFEHEART-RE fell from a derivation C-statistic of 0.85 to 0.67 and needed recalibration before predicted and observed risks aligned.[42]

ApoB offers a different view of the atherogenic phenotype. Each LDL, intermediate-density lipoprotein, very-low-density lipoprotein remnant, and Lp(a) particle carries one apoB molecule, so apoB approximates circulating atherogenic particle number, whereas LDL-C quantifies cholesterol carried within the LDL fraction.[13,14] ApoB and non-HDL cholesterol reflect residual risk better than LDL-C in statin-treated patients, and discordance between LDL-C and apoB-based measures has been associated with coronary events in non-FH populations.[15,16] Calculated LDL-C is itself estimator-dependent, which further complicates direct comparison.[18] When apoB and LDL-C are discordant, a person may carry more or fewer particles than the cholesterol concentration suggests. This discordance has biological and epidemiological support in non-FH populations, and lower apoA1 is associated with cardiovascular risk across long prospective follow-up.[17]

The ratio apoB/LDL-C is nevertheless not a pure biological exposure. It is mathematically coupled to LDL-C, changes when treatment alters cholesterol content and particle composition, and may become especially high after intensive LDL-C lowering. In cross-sectional clinical data, an ASCVD event may precede both treatment intensification and the blood sample. A positive apoB/LDL-C association can therefore represent particle–cholesterol discordance, treatment response, reverse causation, or a mixture. A prior hypothesis-generating analysis in this same 424-person Welsh cohort reported an association between apoB/LDL-C discordance and ASCVD, but its small event count, mixed event timing, and subsequent correction require restraint.[19,20] The present study does not treat that association as independent evidence.

The analytic problem is equally important. Adding one laboratory variable at a time to a previously selected score gives that score an architectural advantage and encourages repeated outcome-guided testing. Conversely, fitting many flexible terms to fewer than 65 cases per cohort invites optimism and unstable signs. We therefore used a small, prespecified set of raw-variable architectures, ridge penalisation, cluster-aware validation, a coefficient-direction gate, and a maximin transport rule, with published instruments prohibited as inputs.

We set explicit negative stopping rules. CALON-N would not be described as universally superior unless its paired AUC interval exceeded zero against every comparator in both cohorts with no credible subgroup decrement; not as a prospective risk model, because biomarker timing did not establish a pre-event baseline; and not for absolute-risk decisions unless calibration transported without target recalibration. Our objectives were to develop a de novo low-dimensional classifier from raw clinical and apolipoprotein variables; quantify reciprocal transport between a specialist FH clinic and genotype-first UK Biobank carriers; compare performance against age plus sex and adapted published instruments; assess calibration, missingness, endpoint, genetic-definition, and subgroup robustness; and determine which claims survived independent computational and reporting quality control.

## Methods

### Study design and estimand

This was a retrospective cross-sectional case-identification and reciprocal-transport study. The estimand was the probability that established ASCVD was already recorded at the time represented by the available contemporary clinical and laboratory phenotype. It was not first-event incidence, five- or ten-year absolute risk, treatment benefit, or a causal effect of any biomarker. Contemporary lipid measurements could occur after ASCVD and after lipid-lowering treatment had been initiated or intensified. **This temporal structure is a defining property of the estimand rather than a correctable modelling detail.**

The analysis had two phases. Phase A tested whether discordance terms augmented a Montreal-based score architecture; after the investigators required a genuinely de novo model, Protocol Amendment 1 replaced score augmentation with ten raw-variable candidates. Phase A is retained only as a diagnostic, labelled `phase_a_score_augmentation`; its selected `montreal_ratio` architecture is **not** CALON-N and contributes no score or coefficient to Phase B. The canonical Phase B record is `scratch_selection.json`, containing exactly the ten candidates described below and selecting `calon_n_apoa1`.

### Why this is not external validation

The protocol, Phase B candidates, sign rules, outcomes, metrics, subgroup thresholds, and stopping rules were written before the Phase B run. However, earlier programme analyses had already examined outcomes and predictors in both cohorts, and the maximin selection rule deliberately consumed outcome performance in both directions. Each final transport application used frozen source preprocessing and coefficients, but the architecture itself was selected with knowledge of both datasets. The correct design label is target-informed reciprocal multi-cohort development, or exploratory internal–external validation.[38,39] It is not protected, independent external validation. Only a third cohort untouched by architecture development can provide that test.

### Data sources, dates, and participant flow

The DRAGON analytical file was obtained locally on 2 August 2026 and linked in memory to the canonical PASS registry during the locked analysis on 9 August 2026. The file contains a uniform administrative date but no validated recruitment window or upstream export timestamp; historical measurements span routine service care rather than a planned baseline visit. We therefore report analytical snapshot and lock dates rather than an unsupported recruitment period, and note the absence of a definitive source-data cut as a limitation requiring custodian confirmation.

The UK Biobank master file contained baseline assessments from 13 March 2006 to 1 October 2010; all 890 strict carriers had baseline dates between 19 April 2007 and 22 September 2010.[21,22] The local participant-to-variant call file was dated 19 March 2026 and the local ClinVar and VEP annotation exports 8 June 2026. Upstream UK Biobank genomic-release and ClinVar-release identifiers were not retained in the files, so reproducibility is anchored to SHA-256 hashes of the exact local snapshots; release-matched replication by another group requires the custodian to restore that metadata.

DRAGON contributed 424 exported records. All 424 linked to PASS: 412 family labels agreed directly and 12 were realigned using the canonical PASS identifier, producing 219 family clusters. No participant was removed for missing predictors, because missing values were completed using source-training data; all 424 entered every primary candidate and 62 had the primary outcome. The UK Biobank call file contained 6,597,041 carrier–variant rows for 468,965 participants. Coordinate linkage identified 890 participants with at least one local ClinVar P/LP *LDLR* call and no locally conflicting call; all linked to the master phenotype file, and 57 had prevalent ASCVD. Adding locally predicted loss-of-function calls produced a prespecified union of 1,264 participants and 80 cases. Participant flow is given in Supplementary Methods 0.

### Cohorts and genetic definitions

DRAGON comprised 424 genetically ascertained participants managed in a specialist Welsh FH service, with 202 columns spanning demographics, clinical history, routine lipids, apolipoproteins, Lp(a), treatment, family information, and recorded variants. The export contained clinically recorded variants or labels across *LDLR* (n=363), *APOB* (n=50), *PCSK9* (n=5), and other genes or labels; these describe the clinic export and do not constitute a newly adjudicated molecular classification. To test whether the broader clinic phenotype drove transport, we used a conservative archived exact-HGVS *LDLR* P/LP sensitivity in which local variant strings were matched to an archived ClinVar table only when a P/LP assertion with stated criteria was present and no uncertain, benign, or conflicting classification was recorded (164 participants, 20 cases, 79 families). This was not treated as the definitive clinic cohort, because unparseable and archive-absent variants cannot validly be reclassified as non-pathogenic.

The primary UK Biobank exposure was coordinate-verified local *LDLR* P/LP carrier status, with chromosome, position, reference, and alternate alleles normalised across the complete call file and local annotations. A participant was included if any qualifying P/LP call was present and no local conflicting call applied. ClinVar review status was unavailable locally, so "P/LP" denotes the study's local classification rather than an exact reproduction of current ClinVar or of blinded adjudication under the ACMG/AMP framework.[25–27] The union sensitivity added consequences consistent with predicted loss of function.

Dependence was represented by connected components of a participant–qualifying-variant bipartite graph, constructed separately for each definition. This matters because UK Biobank carriers commonly had many non-qualifying calls; using an arbitrary first call would create incorrect bootstrap clusters. The procedure yielded 62 components in the strict cohort and 66 in the union. Exact published *LDLR* variants from Patel and Fahed were evaluated in a separate concordance programme as benchmark controls, not substitute development cohorts.[23,24] The exploratory three-gene TUDOR label was excluded because its *APOB* and *PCSK9* entries provide gene labels without participant-level variant coordinates or pathogenicity provenance and overlap poorly with the coordinate-verified strict set.

### Outcome definition

The primary DRAGON outcome was the binary registry field `ASCVD_combined`. Among 424 participants, overlapping component fields recorded myocardial infarction or acute coronary syndrome in 34, percutaneous coronary intervention in 21, coronary artery bypass grafting in 30, angina in 24, transient ischaemic attack in 9, and peripheral vascular disease in 4. The union of these six fields identified 66 participants and a hard-coronary union identified 56; both were sensitivity outcomes because neither reproduced the registry flag exactly.

The UK Biobank outcome was the preconstructed binary field `prevalent_ascvd`, positive in 57 strict and 80 union carriers. In the strict cohort, 96 participants had any first-ASCVD date, of whom 57 were dated before baseline and 39 after. Individual coronary, cerebrovascular, revascularisation, and peripheral-arterial components were not fully recoverable from the local proxy. The common estimand is therefore recorded established ASCVD, not identical hard major adverse cardiovascular events. Outcome adjudication was not repeated blind to predictors.

### Candidate architectures, preprocessing, and selection

Candidate variables were clinically available measurements shared across cohorts, bounded to physiologically plausible ranges before modelling: age in years (5–105); sex; binary hypertension and ever smoking; HDL-C (0.2–5) and LDL-C (0.3–20) in mmol/L; apoB (0.2–4) and apoA1 (0.3–4) in g/L; Lp(a) in source units (0–1,000); and body mass index (12–70 kg/m²), used only by the SAFEHEART comparator. The discordance term was the natural logarithm of apoB divided by LDL-C. Because the ratio combines measurements with different conventional units, it has no unit-free clinical threshold; its purpose was ranking within the locked equation. Lp(a) was retained in source units because harmonisation was incomplete.

Ten low-dimensional candidates were prespecified: (1) age plus sex; (2) age, sex, and log(apoB/LDL-C); (3) age, sex, HDL-C, hypertension, and smoking; (4) candidate 3 plus log(apoB/LDL-C), termed CALON-N core; (5) core plus diabetes; (6) core plus log(TG/HDL-C); (7) core plus log Lp(a); (8) core plus log apoA1; (9) the five-variable clinical model plus log LDL-C and an apoB-on-LDL residual; and (10) age, sex, hypertension, and log(apoB/LDL-C). Published scores and fitted comparator values were prohibited as inputs. This set was intentionally small: with 62 and 57 cases, a high-dimensional learner or unrestricted subset search could obtain an attractive apparent AUC while estimating an unstable decision boundary. **The study used the available sample rather than an a priori model-development sample-size calculation.[34–36]** Applying the Riley criteria retrospectively, 62 and 57 events with seven candidate parameters fall below the recommended minimum for stable coefficient estimation, and the corresponding requirement for external validation of a binary-outcome model is likewise unmet.[37] Coefficient estimation and subgroup analysis are therefore exploratory.

For each source fit, missing raw predictors were replaced with source-training medians, and the same source values were applied in the target; no target distribution or outcome informed completion. Within grouped cross-validation, median estimation, transformation, scaling, residualisation, and penalty tuning were repeated inside the training partition. Median replacement was chosen for determinism and transport transparency, not because missingness was assumed completely at random. ApoA1 was observed in 322/424 DRAGON participants and 785/890 strict UK Biobank carriers; apoB in 323/424 and 837/890. Completion therefore affected a substantial minority, especially apoA1 in DRAGON. Multiple imputation and assay-calibration models were not implemented and remain required sensitivities.

Each candidate used L2-penalised logistic regression with columns standardised using source-training moments. The inverse regularisation parameter was chosen from C = {0.01, 0.03, 0.10, 0.30, 1.00, 3.00} by lowest grouped cross-validated Brier score, with family groups intact in DRAGON folds and qualifying-variant components intact in UK Biobank folds. Coefficient directions were prespecified as positive for age, male sex, hypertension, smoking, diabetes, apoB/LDL-C, TG/HDL-C, Lp(a), LDL-C, and positive apoB discordance, and negative for HDL-C and apoA1; a candidate was ineligible if any included term violated its direction in either source fit. Among eligible candidates, we selected the architecture with the largest minimum AUC across both transport directions, with mean reciprocal AUC as tie-breaker. This maximin rule prevents a strong result in one direction masking failure in the other, but directly consumes both outcome sets.

Candidate-specific internal performance used five repeats of nested five-fold grouped validation, with the penalty retuned and all preprocessing refitted within every outer-training partition, and predictions rank-aggregated. This nests preprocessing and tuning for a named candidate but does not nest the preceding ten-architecture cross-cohort choice; these AUCs are therefore not whole-process optimism-corrected estimates.

### Comparators

Comparators were age plus sex, adapted Montreal-FH-SCORE, adapted FH-Risk-Score, and adapted SAFEHEART, all calculated on the same target participants and compared by paired AUC differences. Montreal used its published coefficient pattern with age and HDL-C standardised to source-cohort anchors. FH-Risk-Score used the published categorical structure, with current LDL-C substituted where untreated LDL-C could not be recovered and the available Lp(a) variable used with the local threshold. SAFEHEART used available age, sex, hypertension, smoking, body mass index, LDL-C, and Lp(a), omitting previous ASCVD because it would be circular for a prevalent-ASCVD outcome.

These comparisons therefore test adapted implementations under the CALON-N cross-sectional estimand, not the exact published instruments under their intended prospective use. The adapted SAFEHEART AUC of 0.541 in UK Biobank is near chance; this reflects major endpoint and input adaptation, particularly removal of previous ASCVD, rather than intrinsic failure of SAFEHEART-RE. Comparator names are accompanied by "adapted" throughout.

### Contrast with matched non-FH participants

Published FH instruments are justified on the premise that general-population equations underestimate risk in FH, a claim usually supported by citation rather than demonstrated within the study reporting it.[9,11,41] We therefore tested it directly. In UK Biobank, each of the 890 strict carriers was matched to five participants with no *LDLR* variant call, exactly on sex and within a one-year age calliper, drawn without replacement from 498,396 eligible non-carriers using a fixed seed. All 890 carriers matched. Because *APOB* and *PCSK9* carriers were not excluded from the non-carrier pool, any residual FH contamination biases the contrast towards the null. In the Welsh clinic, participants who underwent genetic testing and had a mutation reported were matched 1:1 to participants tested through the same referral pathway in whom no mutation was reported, exactly on sex and within a two-year age calliper; ascertainment setting is thereby held constant and genotype is the contrast. We fitted CALON-N separately in each arm using identical preprocessing, transported each fit to the other arm, and compared discrimination, expected:observed ratios and coefficients. Expected:observed intervals used 2,000 bootstrap replicates. Matching was repeated across three ratios (1:1, 1:3, 1:5), three callipers (0.5, 1, 2 years) and two seeds. Because referral role is near-collinear with genotype in a specialist clinic — a relative of a mutation-negative index case is not cascade tested — the Welsh contrast was repeated with both arms restricted to probands.

### Performance, uncertainty, and calibration

Discrimination was measured by AUC. Reciprocal transport applied source-fitted median defaults, transformations, scaler, penalty, and coefficients without target refitting or recalibration. Target families or qualifying-variant components were sampled with replacement 4,000 times, and percentile 95% intervals calculated for CALON-N AUC and each paired difference. These intervals respect target dependence and pairing but condition on one fitted source model; they exclude source-sampling, candidate-selection, and annotation-release uncertainty.

Calibration was described using Brier score, Brier score relative to the target null prevalence model, calibration intercept, calibration slope, and expected:observed (E:O) ratio. A negative scaled Brier score indicates that transported probabilities were less accurate than assigning every target participant the observed target prevalence. No intercept or slope was updated in the target.

### Withdrawal of decision-curve analysis at quality control

A comparative decision-curve table was generated during development. Final quality control established that CALON-N and adapted SAFEHEART produced probabilities, whereas age plus sex, Montreal, and FH-Risk-Score were ranking scores or linear predictors not calibrated onto the same target probability scale. Applying identical probability thresholds to those quantities is invalid, because net benefit is defined only for calibrated probabilities on a common scale.[40] The analysis was marked `valid_for_comparator_inference=False`, all net-benefit claims were withdrawn, and no clinical threshold is proposed. This withdrawal preceded final manuscript interpretation.

### Subgroups, sensitivities, reproducibility, and governance

Prespecified subgroups were sex, age below versus at or above the cohort median, recorded lipid treatment, diabetes, and Lp(a) below versus at or above 143 source units. Subgroups did not influence selection. A stratum with fewer than 10 cases was non-estimable, 10–19 descriptive, and at least 20 evaluable. No interaction tests or subgroup-specific intervals were estimated, so subgroup results assess stress and sparsity rather than effect modification. Sensitivities included the P/LP-or-loss-of-function union, the archived exact-HGVS DRAGON subset, the DRAGON component-union and hard-coronary outcomes, and complete-case transport.

All analysis occurred locally, and no participant identifier, family identifier, variant coordinate, participant row, or participant-level prediction was written to the package. Synthetic scoring was invariant to repeated calls and row order. Reporting was mapped item by item to TRIPOD+AI and the STROBE cross-sectional checklist, with risk of bias appraised by PROBAST and its explanation-and-elaboration guidance; the CHARMS domains informed the descriptive framework.[28–33] UK Biobank analyses were conducted under Application 1002450, which holds NHS Research Ethics Service approval (11/NW/0382).

## Results

### Cohort flow and contrasts

All 424 DRAGON records were linked and analysed, including 62 cases across 219 families. The strict UK Biobank bridge contributed 890 eligible carriers, 57 cases, and 62 qualifying-variant components; the union contributed 1,264 carriers, 80 cases, and 66 components. Missing laboratory data changed values through source-median completion but did not change analysis denominators.

DRAGON participants were younger than strict UK Biobank carriers (mean 48.4±18.6 versus 57.3±8.0 years), were more frequently recorded as receiving lipid-lowering treatment (86.6% versus 40.6%), and had more than twice the prevalence of established ASCVD (14.6% versus 6.4%). These contrasts establish spectrum shift before any model is fitted (**Table 1**; Supplementary Table S1).

**Table 1. Cohort characteristics**

| Characteristic | DRAGON | UKB strict *LDLR* P/LP | UKB P/LP-or-LoF |
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

**Table 2. Locked candidate architectures, reciprocal transport, and sign-gate outcome**

| Candidate | Model terms | Clinic → UKB AUC | UKB → clinic AUC | Minimum | Sign gate |
|---|---|---:|---:|---:|---|
| age_sex | age, male | 0.7319 | 0.8950 | 0.7319 | pass |
| age_sex_ratio | age, male, log(apoB/LDL-C) | 0.7469 | 0.8319 | 0.7469 | pass |
| clinical5 | age, male, HDL-C, hypertension, smoking | 0.7452 | 0.8899 | 0.7452 | pass |
| calon_n_core | clinical5 + log(apoB/LDL-C) | 0.7567 | 0.8471 | 0.7567 | pass |
| calon_n_diabetes | core + diabetes | 0.7605 | 0.8488 | 0.7605 | pass |
| calon_n_tghdl | core + log(TG/HDL-C) | 0.7552 | 0.8410 | 0.7552 | **fail** — TG/HDL-C negative in clinic fit |
| calon_n_lpa | core + log Lp(a) | 0.7591 | 0.8424 | 0.7591 | pass |
| **calon_n_apoa1 (CALON-N)** | **core + log apoA1** | **0.7672** | **0.8481** | **0.7672** | **pass; selected** |
| calon_n_discordance | clinical5 + log LDL-C + apoB-on-LDL residual | 0.7586 | 0.8219 | 0.7586 | **fail** — LDL-C negative in both fits |
| calon_n_parsimonious | age, male, hypertension, log(apoB/LDL-C) | 0.7333 | 0.8322 | 0.7333 | pass |

AUC, area under the receiver-operating-characteristic curve; UKB, UK Biobank strict *LDLR* pathogenic/likely pathogenic cohort; TG, triglycerides. All candidates were prespecified before Phase B modelling and fitted by L2-penalised logistic regression, with the inverse penalty selected from C = {0.01, 0.03, 0.10, 0.30, 1.00, 3.00} by lowest grouped cross-validated Brier score. "Minimum" is the smaller of the two reciprocal-transport AUCs and was the selection criterion. A candidate was ineligible if any included term violated its prespecified coefficient direction in either source fit; both failing candidates are shown rather than omitted. Penalty-level tuning results and all source equations are provided in the analysis package.

### Candidate selection and internal validation

The sign-coherent maximin rule selected the clinical core plus log apoA1, named CALON-N. Its source-fitted transport AUCs were 0.7672 from DRAGON to strict UK Biobank and 0.8481 in reverse, giving a minimum of 0.7672 (**Table 2**; **Figure 1**). The next candidates were core plus diabetes (minimum 0.7605), core plus Lp(a) (0.7591), and the core alone (0.7567). The residual-discordance candidate reached 0.7586 and 0.8219 but failed the sign gate because LDL-C was negative in both source fits; the TG/HDL-C candidate failed because that term was negative in the DRAGON fit. Failed candidates are shown in **Table 2** rather than silently discarded.

Age plus sex produced the lowest minimum reciprocal AUC (0.7319), because its AUC into UK Biobank was 0.7319. Yet in reverse its AUC was 0.8950, higher than all ten fitted candidates. This contrast is central: a model can satisfy a transport-oriented maximin rule while a simpler predictor remains stronger in one receiving cohort.

Repeated nested grouped AUC for CALON-N was 0.8932 in DRAGON and 0.7943 in strict UK Biobank; for age plus sex, 0.8858 and 0.7104; for the five-variable clinical model, 0.8906 and 0.7500; and for age, sex plus ratio, 0.8881 and 0.7964. In UK Biobank the smaller age/sex/ratio candidate had a marginally higher internal AUC than CALON-N, whereas CALON-N had the better locked reciprocal minimum. Because architecture selection was not nested, these values describe candidate-specific resampling rather than unbiased estimates of the development procedure.

### Frozen pooled research equation

The following equation was fitted after transport by pooling both cohorts. **It has no untouched validation, must not be used for clinical care, and must not be interpreted as a five- or ten-year risk equation.** The reciprocal results used separate source-fitted models, not this pooled representation.

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

Coefficient signs matched the lock. Descriptively, the penalised pooled coefficients correspond to odds ratios of 3.07 per 10 years of age, 1.79 for male sex, 0.53 per 1 mmol/L higher HDL-C, 3.76 per doubling of apoB/LDL-C, and 0.31 per doubling of apoA1. These translations have no coefficient confidence intervals, mix cross-sectional association with treatment and ascertainment, and are not causal effect estimates.

### Reciprocal transport

With coefficients and preprocessing fitted in DRAGON, CALON-N achieved AUC 0.7672 (95% CI 0.7117–0.8282) in 890 strict UK Biobank carriers. Adapted Montreal achieved 0.7747, a difference of −0.0075 (−0.0365 to 0.0073); the data therefore establish neither superiority nor equivalence to Montreal. CALON-N exceeded age plus sex by 0.0353 (0.0179–0.0605), adapted FH-Risk-Score by 0.0710 (0.0237–0.1101), and adapted SAFEHEART by 0.2265 (0.1216–0.2936). The union produced nearly identical discrimination, 0.7673 (0.7187–0.8129), with Montreal at 0.7680 (difference −0.0007). Broadening the carrier definition changed sample size and precision more than point discrimination.

In the reverse direction, age plus sex alone ranked established ASCVD most strongly in DRAGON (AUC 0.8950), followed by adapted Montreal (0.8928), adapted FH-Risk-Score (0.8570), CALON-N (0.8481, 95% CI 0.7956–0.8963), and adapted SAFEHEART (0.7997). CALON-N was lower than age plus sex by −0.0469 (−0.1004 to 0.0025) and than Montreal by −0.0448 (−0.0927 to −0.0024), and was not separable from FH-Risk-Score or SAFEHEART (**Table 3**).

**Table 3. Reciprocal transport and paired comparisons**

| Target and source fit | CALON-N AUC (95% CI) | vs age+sex | vs Montreal | vs FH-RS | vs SAFEHEART |
|---|---:|---:|---:|---:|---:|
| UKB strict; DRAGON fit | 0.767 (0.712–0.828) | +0.035 (+0.018,+0.060) | −0.008 (−0.036,+0.007) | +0.071 (+0.024,+0.110) | +0.227 (+0.122,+0.294) |
| DRAGON; UKB strict fit | 0.848 (0.796–0.896) | −0.047 (−0.100,+0.003) | −0.045 (−0.093,−0.002) | −0.009 (−0.071,+0.050) | +0.048 (−0.030,+0.130) |
| UKB union; DRAGON fit | 0.767 (0.719–0.813) | +0.023 (+0.002,+0.046) | −0.001 (−0.025,+0.010) | +0.071 (+0.036,+0.100) | +0.240 (+0.154,+0.295) |

### Calibration and overall accuracy

Discrimination transported more successfully than probability (**Figure 2**). In strict UK Biobank, the DRAGON-fitted model had Brier score 0.0823 against a null of 0.0599, a scaled Brier of −37.3%, calibration intercept −1.446, slope 0.951, and E:O 3.004. On aggregate, an apparent CALON-N probability of 15% would correspond to roughly 5% observed prevalence, although dividing an individual probability by three is not a valid recalibration.

In DRAGON, the UK Biobank-fitted model had Brier 0.1115 against a null of 0.1248, scaled Brier +10.7%, intercept +0.657, slope 0.752, and E:O 0.447, predicting fewer than half the observed cases. The opposite intercept errors are consistent with differing case prevalence and ascertainment, while the slopes show that a single intercept update would not fully repair transport. Union results resembled the strict cohort (**Table 4**). No comparative decision-curve result is reported, and marked calibration drift independently prevents threshold recommendations.

### Sensitivity and subgroup analyses

In the conservative exact-HGVS *LDLR* P/LP DRAGON subset, UK Biobank-fitted CALON-N achieved AUC 0.8267 among 164 participants and 20 cases — lower than in full DRAGON but imprecise, and excluding unparseable and archive-absent clinic variants. The DRAGON component-union outcome produced 0.8473 with 66 cases and the hard-coronary outcome 0.8429 with 56, so the primary reverse-transport AUC was not driven by one outcome coding choice.

Complete-case transport was more sensitive. The DRAGON-to-UK Biobank complete-case analysis included 726 participants and 50 cases, yielding AUC 0.7530 against 0.7672 with completion. Reverse complete-case analysis included only 304 DRAGON participants and 45 cases but yielded 0.8910 against 0.8481. Missingness and assay availability therefore contributed materially to directional transport, particularly in DRAGON, although complete cases also select a smaller and potentially different clinic subset. Neither approach removes missing-not-at-random bias.

Twenty subgroup rows were attempted; six contained fewer than 10 cases and were non-estimable. Of the remaining 14, CALON-N exceeded the best comparator in one — UK Biobank women, by 0.0049 — and in no DRAGON subgroup. In strict UK Biobank it was below the best comparator among men (0.708 versus 0.715), those at or above median age (0.663 versus 0.667), treated carriers (0.659 versus 0.672), participants with diabetes (0.690 versus 0.708; descriptive), those without diabetes (0.767 versus 0.773), and Lp(a)<143 (0.740 versus 0.751). In DRAGON, deficits were larger among men (0.845 versus 0.914), women (0.842 versus 0.894), treated participants (0.837 versus 0.889), and those without diabetes (0.842 versus 0.896). The Lp(a)-high DRAGON stratum, where a discordance model might be expected to help, showed 0.869 versus 0.872. These sparse descriptive comparisons reject an all-subgroup claim but do not demonstrate effect modification (Supplementary Table S6).

**Table 4. Calibration, sensitivity, and subgroup summary**

| Analysis | n / cases | AUC | Brier | Calibration intercept | Calibration slope | Expected:observed |
|---|---:|---:|---:|---:|---:|---:|
| **Calibration** | | | | | | |
| Clinic → UKB strict | 890 / 57 | 0.767 | 0.0823 | −1.446 | 0.951 | **3.004** |
| UKB strict → clinic | 424 / 62 | 0.848 | 0.1115 | +0.657 | 0.752 | **0.447** |
| Clinic → UKB union | 1,264 / 80 | 0.767 | 0.0828 | −1.486 | 0.929 | 3.047 |
| **Sensitivity** | | | | | | |
| UKB P/LP-or-loss-of-function union | 1,264 / 80 | 0.767 | — | — | — | — |
| Archived exact-HGVS *LDLR* P/LP clinic subset | 164 / 20 | 0.827 | — | — | — | — |
| Clinic component-union endpoint | 424 / 66 | 0.847 | — | — | — | — |
| Clinic hard-coronary endpoint | 424 / 56 | 0.843 | — | — | — | — |
| Clinic → UKB, complete cases | 726 / 50 | 0.753 | — | — | — | — |
| UKB → clinic, complete cases | 304 / 45 | 0.891 | — | — | — | — |
| **Subgroups** | | | | | | |
| Rows attempted | 20 | — | — | — | — | — |
| Non-estimable (<10 cases) | 6 | — | — | — | — | — |
| Evaluable or descriptive | 14 | — | — | — | — | — |
| Rows in which CALON-N exceeded the best comparator | **1** | — | — | — | — | — |

AUC, area under the receiver-operating-characteristic curve; UKB, UK Biobank; P/LP, pathogenic or likely pathogenic; HGVS, Human Genome Variation Society nomenclature. Calibration was assessed without any target recalibration; the expected:observed ratio is mean predicted probability divided by observed prevalence. Scaled Brier scores relative to the target null-prevalence model were −37.3% (clinic → UKB strict), +10.7% (UKB strict → clinic), and −39.7% (clinic → UKB union); a negative value indicates that transported probabilities were less accurate than assigning every participant the observed target prevalence. Comparative decision-curve analysis was withdrawn at quality control because comparator outputs were not calibrated probabilities on a common scale. The single subgroup in which CALON-N exceeded the best comparator was UK Biobank women (0.784 versus 0.779). Full subgroup rows are given in Supplementary Table S6.

### Why an FH-specific model is needed: FH versus matched non-FH

Matching each UK Biobank carrier to five age- and sex-matched non-carriers produced arms identical in mean age (57.3 years) and sex (43% male). Prevalent ASCVD affected 57 of 890 carriers (6.4%) and 181 of 4,450 non-carriers (4.1%), an odds ratio of 1.61 (95% CI 1.19–2.19), attenuating only to 1.55 after adjustment for the model's own risk factors (**Table 5**).

Discrimination was largely genotype-independent. CALON-N fitted in carriers achieved an AUC of 0.840 (0.792–0.889) in carriers and 0.795 (0.763–0.824) when transported unchanged to matched non-carriers; fitted in non-carriers it achieved 0.802 (0.769–0.830) internally and 0.831 (0.782–0.877) in carriers. The published FH-specific scores behaved the same way: adapted Montreal-FH-SCORE reached 0.764 in carriers and 0.727 in matched non-carriers, and adapted FH-Risk-Score 0.709 and 0.684. Fitted coefficients were close in the two arms — log(apoB/LDL-C) +9.15 versus +9.43 per log unit and age +0.078 versus +0.088 per year — although hypertension and ever smoking changed sign in the non-carrier fit, where both are collinear with the far larger competing risk-factor burden of the general population.

Absolute risk behaved entirely differently. The carrier-fitted model transported to non-carriers predicted 6.13% against an observed 4.07%, an expected:observed ratio of 1.51 (1.32–1.75); the non-carrier-fitted model transported to carriers predicted 4.43% against an observed 6.40%, a ratio of 0.69 (0.55–0.90). Both intervals excluded unity. Across all 18 matching configurations the ratios remained 1.43–1.51 and 0.67–0.72 and the odds ratio 1.45–1.61; restricting to complete cases (726 carriers, 50 cases; 3,531 non-carriers, 138 cases) gave 1.68 and 0.60. A model built in non-FH participants therefore under-predicted risk in genetically defined FH by approximately 31%, which is the quantitative form of a claim the FH literature has generally asserted rather than measured.[9,11,41]

The Welsh clinic arm shows that this quantity is not a fixed property of the genotype. After 1:1 matching (2,213 per arm, both 60.1 years, 44% male), genotype-positive participants had *lower* prevalent ASCVD than genotype-negative participants from the same clinic (18.1% versus 28.2%; odds ratio 0.56, 0.49–0.65), and the transported expected:observed ratios reversed accordingly (0.63 and 1.60). The explanation is referral route, not biology: probands were 32% of the genotype-positive arm but 97% of the genotype-negative arm, because relatives of a mutation-negative index case are not cascade tested. Restricting both arms to probands moved the odds ratio to 0.86 (0.71–1.05), an interval including unity, and the expected:observed ratios to 0.88 and 1.13. Welsh risk factors are recorded as status at last contact rather than at a dated baseline, so this arm is reported as a directional check on ascertainment rather than as an effect estimate.

**Table 5. FH versus matched non-FH participants: discrimination transports, absolute risk does not**

| | UK Biobank | | Wales specialist clinic | |
|---|---:|---:|---:|---:|
| | **FH carriers** | **Matched non-FH** | **Genotype-positive** | **Genotype-negative** |
| Matching | 1:5, sex exact, age ±1 y | | 1:1, sex exact, age ±2 y | |
| Participants, n | 890 | 4,450 | 2,213 | 2,213 |
| Established ASCVD, n (%) | 57 (6.4) | 181 (4.1) | 400 (18.1) | 624 (28.2) |
| Age, years, mean | 57.3 | 57.3 | 60.1 | 60.1 |
| Male, % | 43 | 43 | 44 | 44 |
| Odds ratio for FH status (95% CI) | 1.61 (1.19–2.19) | | 0.56 (0.49–0.65) | |
| Adjusted for model risk factors | 1.55 | | 0.50 | |
| Probands, % of arm | not applicable | not applicable | 32 | 97 |
| Odds ratio, probands only (95% CI) | not applicable | | 0.86 (0.71–1.05) | |
| **Discrimination, AUC (95% CI)** | | | | |
| Model fitted and applied in same arm | 0.840 (0.792–0.889) | 0.802 (0.769–0.830) | 0.783 (0.761–0.805) | 0.728 (0.705–0.751) |
| Model transported from the other arm | 0.831 (0.782–0.877) | 0.795 (0.763–0.824) | 0.769 (0.746–0.793) | 0.715 (0.692–0.738) |
| Adapted Montreal-FH-SCORE | 0.764 | 0.727 | not evaluated | not evaluated |
| Adapted FH-Risk-Score | 0.709 | 0.684 | not evaluated | not evaluated |
| **Calibration on transport, expected:observed (95% CI)** | | | | |
| Receiving the other arm's model | 0.69 (0.55–0.90) | 1.51 (1.32–1.75) | 1.60 | 0.63 |
| Same, probands only | not applicable | | 1.13 | 0.88 |
| Range across 18 matching configurations | 0.67–0.72 | 1.43–1.51 | not evaluated | not evaluated |
| Complete cases only | 0.60 | 1.68 | not evaluated | not evaluated |

ASCVD, atherosclerotic cardiovascular disease; AUC, area under the receiver-operating-characteristic curve; CI, confidence interval; FH, familial hypercholesterolaemia. UK Biobank non-FH participants are those with no *LDLR* variant call, matched without replacement from 498,396 eligible participants; *APOB* and *PCSK9* carriers were not excluded, which biases the carrier contrast towards the null. Welsh arms comprise participants tested through the same specialist referral pathway with and without a reported mutation; 975 genotype-positive participants, predominantly younger cascade-detected relatives, had no age-eligible comparator and were not matched. Expected:observed is mean predicted probability divided by observed prevalence, with no target recalibration; intervals are 2,000-replicate bootstraps and are shown for the UK Biobank arm, which carries the primary contrast. Both models use the CALON-N variable set in UK Biobank; the Welsh registry records no apolipoprotein measurements, so the Welsh arm uses the reduced set age, sex, HDL-C and ever smoking, and its risk factors are recorded as status at last contact rather than at a dated baseline.

## Discussion

### Principal findings

CALON-N is de novo in the strict architectural sense: seven terms fitted from raw clinical and laboratory measurements, with no published risk score or fitted comparator in the equation. It retained moderate-to-high discrimination in both directions — AUC 0.767 from specialist clinic into strict UK Biobank carriers and 0.848 in reverse — and in UK Biobank ranked cases better than age plus sex and the adapted FH-Risk-Score and SAFEHEART implementations while remaining close to Montreal. It did not outperform all comparators in both directions. In DRAGON, age plus sex alone had the highest point AUC, Montreal was significantly higher on the conditional family bootstrap, absolute probabilities failed in opposite directions, and 13 of 14 estimable subgroup rows did not beat the best comparator.

The study supports a narrow conclusion: apoB/LDL-C and apoA1 can contribute to a coherent cross-sectional classifier across genetically defined FH settings, but additional laboratory detail does not guarantee better ranking than age and sex in a selected clinic. CALON-N is hypothesis-generating, not a validated clinical calculator.

### Interpreting apoB–LDL discordance

The selected positive apoB/LDL-C term is compatible with a particle–cholesterol discordance hypothesis: at a given measured LDL-C, higher apoB can indicate more atherogenic particles carrying less cholesterol each, which is relevant when LDL-C appears controlled but particle burden remains elevated.[13] The protective apoA1 coefficient is directionally consistent with long-term population evidence.[17]

The present data cannot isolate that biology. In DRAGON the blood phenotype is contemporary and may follow both disease and treatment. Intensive lipid lowering reduces LDL-C more than apoB, mechanically increasing the ratio, and individuals with established ASCVD are more likely to receive intensive therapy. The ratio may therefore identify people whose clinical history led to treatment rather than predict that history from a pre-event exposure. This is reverse causation and confounding by indication, not necessarily a false association; it means the association answers a different question — whether a contemporary phenotype helps identify already-recorded disease.

The ratio also shares LDL-C in its denominator with an important treatment target. A strong ratio coefficient does not show that apoB is superior to LDL-C in every representation. The residual-discordance candidate, which preserved LDL-C and represented apoB orthogonally to it, produced an incoherent negative LDL-C coefficient and failed the sign gate. That failure is informative: the data do not stably separate an LDL-C effect from discordance under this cross-sectional, treated design.

### Why transport was asymmetric

Five between-cohort differences can produce the observed asymmetry. First, **age and disease accumulation**: UK Biobank carriers were about nine years older on average, whereas all 62 DRAGON cases fell in the older half of that cohort, so age carried exceptional rank information in the clinic target and allowed age plus sex to reach 0.895. Second, **ascertainment**: DRAGON represents recognised specialist-clinic FH including phenotype-referred probands and family-linked relatives, whereas UK Biobank represents volunteer, population-based, genotype-first ascertainment, and the relation between measured phenotype and disease need not be invariant across those routes. Third, **treatment recognition**: recorded treatment was 86.6% versus 40.6%, with different source fields and uncertain timing, so a therapy-sensitive ratio shifts differently. Fourth, **genetic spectrum**: DRAGON contains clinically recorded *LDLR*, *APOB*, *PCSK9*, and other labels, whereas the primary UK Biobank analysis is coordinate-verified *LDLR* P/LP, differing in variant severity, provenance, and family sharing. Fifth, **phenotype and endpoint timing**: DRAGON biomarkers derive from routine service history, UK Biobank biomarkers are anchored to recruitment, and endpoint components are not identical.

These differences violate the conditional-invariance assumption required for simple transport — that disease status has the same relation to the included predictors in source and target. Reciprocal fitting reveals this rather than resolving it. The model that travels from clinic to biobank need not be the model that travels from biobank to clinic.

### Calibration failure is the clearest negative result

The most decisive result is not an AUC difference but the E:O reversal. Clinic-derived probabilities overpredicted UK Biobank cases threefold and had a Brier score worse than the constant target prevalence; UK Biobank-derived probabilities underpredicted clinic cases by more than half. Calibration slopes of 0.95 and 0.75 indicate that both baseline odds and predictor effects changed, so a local intercept correction might fix average prevalence without fixing risk spread or individual calibration.

This has direct clinical implications. A score can rank two people correctly while assigning both the wrong absolute probabilities. Any decision threshold — for imaging, treatment intensification, or specialist review — depends on calibrated probabilities and the consequences of false positives and negatives. Because those requirements were not met, target recalibration was deliberately not used to rescue the main result, and the invalid comparative decision curve was withdrawn. CALON-N cannot currently guide care.

### What is FH-specific is the level, not the ranking

The matched non-FH comparison converts the field's founding premise into a measurement. General-population and FH-specific instruments are routinely said to be non-interchangeable because population equations underestimate FH risk,[9,11,41] but the size of that error is rarely reported in the same data. Here a model fitted in age- and sex-matched non-carriers under-predicted prevalent ASCVD in genetically defined carriers by 31% (expected:observed 0.69, 0.55–0.90), while the same architecture fitted in carriers over-predicted in non-carriers by 51% (1.51, 1.32–1.75). Discrimination, by contrast, moved by 0.04 or less, and the fitted coefficient on log(apoB/LDL-C) was almost identical in the two populations. Montreal-FH-SCORE and FH-Risk-Score showed the same pattern, discriminating in matched non-carriers nearly as well as in carriers.

The practical reading is that an FH-specific instrument earns its label through its intercept rather than its slopes. This is the same conclusion the clinic-to-biobank transport reached from a different direction, and it is consistent with the only comparable published exercise: when SAFEHEART-RE was applied to an English routine-care FH population, discrimination fell from 0.85 in derivation to 0.67 and predicted risks required recalibration before they aligned with observed events, after which the model still offered limited clinical value.[42] Two independent contrasts in the present data — across ascertainment settings and across genotype — and one published external validation therefore point the same way. It also explains why our decision to leave the equation uncalibrated is not a defect to be patched: the quantity that fails to transport is exactly the quantity a threshold would act on.

The Welsh arm adds the necessary caution against reading this as a fixed genotype effect. There, genotype-positive patients had lower prevalent ASCVD than genotype-negative patients from the same clinic, and the difference largely disappeared once both arms were restricted to probands. Mutation-negative clinic attenders are almost entirely index cases referred for a severe phenotype, frequently after an event, whereas mutation-positive cohorts accumulate cascade-detected relatives who are identified through a family member rather than through their own disease. The FH-versus-non-FH risk difference is thus a property of the two ascertainment processes being compared, not a constant that a single equation can carry between health systems.

### The apoA1 term, missing data, and the exposure audit

Log apoA1 improved the prespecified minimum reciprocal AUC and retained a protective coefficient in both source fits, distinguishing CALON-N from conventional FH comparators. It should nonetheless be considered provisional. HDL-C and apoA1 overlap biologically and statistically, so their coefficients are conditional on each other and on ridge shrinkage, and approximately one quarter of DRAGON lacked apoA1, with source-median replacement assigning identical completed values. This preserves sample size and prevents target leakage but suppresses imputation uncertainty. The complete-case analyses show the choice matters: reverse transport rose from 0.848 to 0.891 in a much smaller subset with complete laboratory data, which could reflect better measurement, subgroup selection, or both. Multiple imputation with compatible transformations and full pipeline repetition across imputations are obvious untested sensitivities and should be prespecified in the next study rather than used now to choose a better-looking result.

The UK Biobank exposure audit establishes three things. The coordinate bridge is technically credible: the complete 6.6-million-row call file was linked to local annotations, all 890 strict and 1,264 union carriers linked to the phenotype master, and bootstrap dependence was reconstructed from shared qualifying variants rather than arbitrary calls. Exact published-variant benchmarks provided a positive control outside model selection — using externally listed Patel *LDLR* variants with a prevalent-inclusive covariate structure, the observed association was concordant with Patel's *LDLR*-specific estimate, supporting the participant identifier, variant-coordinate columns, and broad ASCVD fields.[23,24] Neither exercise validates the exploratory three-gene label, whose correct denominator is 426,731 participants with exposure records rather than the 501,936-person phenotype master, and whose *APOB* and *PCSK9* entries lack variant-level pathogenicity evidence.

### Clinical context: what a classifier of established disease can and cannot offer

Most FH instruments are risk calculators: they estimate the probability that a person free of disease will develop it. CALON-N is not that. It estimates the probability that ASCVD is *already recorded* at the time a contemporary phenotype is observed. The distinction is not semantic, and conflating the two is the principal way this work could be misused.

Three consequences follow for practice. First, **no treatment decision should rest on a CALON-N probability**. Lipid-lowering intensity in FH is governed by LDL-C targets and estimated future risk, not by the likelihood that disease has already occurred;[7] a patient with established ASCVD is already a very-high-risk secondary-prevention patient by guideline definition, and a classifier that recognises them adds nothing to that decision. Second, **the probabilities themselves are wrong outside the cohort in which they were fitted**. Expected:observed ratios of 3.00 and 0.45 mean that the same equation overstated prevalence threefold in one setting and understated it by more than half in the other. A clinician shown "15%" from a clinic-fitted model applied to a population-ascertained carrier would be reading a figure that corresponded to roughly 5% observed prevalence. Third, **discrimination and calibration failed independently**, and only the former transported: the model ranked patients acceptably in both directions while assigning both the wrong absolute numbers. Ranking without calibration cannot support any threshold-based action.

Where might such a classifier legitimately contribute? Two uses are defensible. The first is **service audit and case ascertainment**. FH registries are assembled over decades from heterogeneous sources, and cardiovascular history is frequently incomplete. A model that flags participants whose contemporary phenotype is atypical for their recorded disease status could prompt targeted record review, which is a data-quality activity rather than a clinical one. Even here the contribution is modest, because age and sex alone reached AUC 0.895 in the clinic cohort; the additional laboratory terms bought little.

The second is **hypothesis generation about particle burden**. The selected positive apoB/LDL-C coefficient, alongside a protective apoA1 term, is compatible with the clinical intuition that a patient whose LDL-C appears controlled may still carry a high atherogenic particle load.[13,17] Contemporary guidance already supports measuring apoB where discordance is plausible. What this study adds is not a threshold or a calculator but a demonstration that, in genetically defined FH, apoB/LDL-C carries information about disease status beyond conventional lipids in one direction of transport — and a clear statement of why that observation cannot yet be converted into prospective risk estimation.

The ascertainment finding also has an interpretive message. A specialist-clinic FH population and a population-sequenced carrier cohort are not interchangeable, even when both are genetically defined. They differed here in age by roughly nine years, in recorded treatment by more than twofold, and in prevalent disease by more than twofold, and the same equation behaved differently in each. Clinicians and guideline developers should therefore be cautious when a score derived in one ascertainment setting is applied in another — including when scores developed in phenotype-referred clinic populations are applied to relatives identified by cascade testing or to carriers found by population genomic screening. Our data do not establish how large that error is in any specific score, but they demonstrate that the assumption of invariance can fail substantially within a single disease and a single model.

For the present model the practical conclusion is unambiguous. CALON-N should be used to design the next study, not to see the next patient.

### Comparators and the information ceiling

Criticism must be symmetrical. CALON-N was developed under the current outcome, while Montreal, FH-Risk-Score, and SAFEHEART were adapted away from their original settings. Montreal's strong performance in DRAGON is unsurprising because its variables — especially age — map closely to prevalent disease in specialist FH cohorts.[8,9,12] The lower adapted FH-Risk-Score and SAFEHEART AUCs should not be read as evidence that those prospective tools fail clinically: untreated LDL-C was unavailable, Lp(a) units were not fully harmonised, previous ASCVD was removed from SAFEHEART, and the endpoint was prevalent rather than incident disease.

There is also an information asymmetry. FH-Risk-Score estimated its coefficients using 3,881 adults and 32,361 person-years, whereas each CALON-N source contained fewer than 65 cases.[10] A small new cohort cannot reliably out-estimate a large multi-registry derivation by changing algorithms. This study instead asks whether raw apolipoprotein terms survive a harsh reciprocal transport test. Their survival at 0.767 and 0.848 is scientifically interesting; their inability to dominate a strong age-based comparator is equally important.

### Novelty, confidence, and risk of bias

The biological premise — that apoB reflects particle number, that discordance may reveal residual risk, and that apoA1 is inversely associated with ASCVD — is not new.[13,17,19,20] The same DRAGON participants contributed to the earlier hypothesis-generating report, so this is not an independent biological replication.[19,20] Nor is CALON-N the first FH risk instrument.[8–11] The defensible novelty is methodological: a de novo raw-variable equation combining log(apoB/LDL-C) with log apoA1 without importing a published score; tested in reciprocal clinic-to-biobank and biobank-to-clinic transport; preserving family and shared-variant dependence; using a locked physiological sign gate; and reporting calibration and subgroup failure alongside discrimination. Targeted searches through August 2026 identified no clearly matching FH-specific raw-apolipoprotein model evaluated by reciprocal transport, but because this was not a formal systematic review we avoid an absolute "first" claim.

Confidence is high that the locked files reconstruct the stated cohorts, that family realignment and qualifying-variant clustering are correct, that the scorer is deterministic, and that the stated algorithm selects CALON-N: all canonical input hashes matched, primary counts reproduced, comparator deltas were arithmetically exact, and repeated or row-reversed synthetic scoring differed by zero. Confidence is moderate for conditional AUCs within these datasets, lower for adapted-comparator contrasts, very low for subgroups, absent for absolute-risk use, and low for a third registry. A non-significant Montreal difference is not equivalence. PROBAST risk of bias is high with high applicability concern for prospective prediction or deployment — a judgement not contradicted by reproducible computation, because reproducibility asks whether the same operations return the same answer whereas risk of bias asks whether that answer estimates the intended quantity.

### Strengths and limitations

Strengths include complete DRAGON-to-PASS linkage and family realignment; use of the full UK Biobank call file; explicit separation of local P/LP, P/LP-or-LoF, exact-published-variant, and exploratory gene-label definitions; corrected qualifying-variant components; raw-variable rather than score-stack development; fold-local preprocessing and tuning; nested grouped evaluation per candidate; reciprocal transport without target recalibration; conditional paired bootstrap intervals; prespecified sign and subgroup rules; complete reporting of failed candidates and negative subgroups; deterministic scoring; aggregate-only outputs; and withdrawal of an invalid decision-curve analysis at quality control.

Eight limitations define the interpretation. First, architecture selection was target-informed, so reciprocal transport cannot be presented as protected validation and performance is likely optimistic for a new setting. Second, event information was limited: 62 and 57 cases supported seven terms, penalty tuning, ten architecture comparisons, two directions, and 20 subgroup attempts; ridge shrinkage and event thresholds reduce but do not eliminate whole-process selection and multiplicity effects, and the target bootstrap omits source-development uncertainty. Third, missing data were handled by single source-median replacement, which is deterministic and avoids target leakage but assumes the source median is transportable, understates uncertainty, and is especially consequential for the 24.1% of DRAGON participants without apoA1. Fourth, the source populations have substantial spectrum and survivor bias: DRAGON is a treated specialist service and UK Biobank a volunteer cohort of middle-aged and older adults, so fatal early FH events are absent and selection may differ in both directions. Fifth, outcome definitions were not centrally adjudicated or perfectly harmonised, and misclassification could be differential by setting. Sixth, genetic definitions differed, and archived and published-variant sensitivities do not substitute for contemporary blinded molecular adjudication across all three canonical FH genes. Seventh, comparator fairness is limited by adaptation to available variables and a cross-sectional outcome. Eighth, ancestry, socioeconomic context, laboratory platforms, and treatment timing were insufficiently characterised; the cohorts are predominantly White European and fairness across ancestry or deprivation was not estimated.

### Next study

The next study should freeze CALON-N before accessing any third cohort and identify a prospective FH registry with dated pre-event apoB, LDL-C, apoA1, HDL-C, blood pressure, smoking, treatment, genotype, and ascertainment route. It should use adjudicated incident ASCVD, a stated time zero, censoring and competing death, and a prespecified horizon, with families and shared variants intact across resampling. Missing values should be addressed by multiple imputation inside the full validation pipeline, with uncertainty repeating imputation, preprocessing, fitting, and any updating within each cluster bootstrap. That study should compare frozen CALON-N transport, ordinary local recalibration, and a separately specified incident-risk model, with every comparator expressing probability at the same horizon before calibration or decision analysis. Only acceptable discrimination, calibration, and net benefit in that untouched setting would justify a simplified implementation or clinical impact trial.

## Conclusions

CALON-N is a novel, sign-coherent, raw-variable classifier for established ASCVD in genetically defined FH. It transported with AUCs of 0.767 and 0.848, but did not beat Montreal, age plus sex, or every comparator across directions and subgroups, and its absolute probabilities did not transport. The model should remain frozen as a research hypothesis for a prospective FH registry with pre-event apoB, LDL-C, apoA1, a dated baseline, and adjudicated follow-up — not promoted as a ten-year risk score or clinical tool.

## Figure legends

**Figure 1. Locked candidate reciprocal transport.** Area under the curve for each of the ten prespecified raw-variable architectures in both transport directions, with the minimum reciprocal AUC used for selection and sign-gate status indicated. CALON-N (`calon_n_apoa1`) has the highest minimum.

**Figure 2. External calibration in both directions.** Observed versus predicted probability by prediction quintile for the clinic-fitted model applied to UK Biobank and the UK Biobank-fitted model applied to the clinic, with the identity line and expected:observed ratios shown. Curves lie on opposite sides of identity.

## Declarations

**Ethics and data governance:** UK Biobank analyses were conducted under Application 1002450. UK Biobank has approval from the NHS National Research Ethics Service North West–Haydock Research Ethics Committee (11/NW/0382), and participants provided consent under UK Biobank governance. The authors must insert and verify the full Welsh PASS/DRAGON approval or service-evaluation determination, consent or waiver, UK GDPR legal basis, data controller, and R&D/information-governance reference before submission. Only aggregate, de-identified results are reported.

**Funding:** No dedicated external grant funding is declared. Cohort access, data governance, and analyses were supported through routine academic and clinical research activity within Cardiff and Vale University Health Board, the All-Wales Familial Hypercholesterolaemia Service, and UK Biobank Application 1002450. All authors must confirm this statement before submission.

**Conflicts of interest:** The authors declare no relevant conflicts of interest for this work. Each author must complete the journal's individual disclosure form before submission.

**Patient and public involvement:** Patient or public involvement was not documented in the supplied analysis records. The corresponding author must confirm that patients and the public were not involved in design, analysis, interpretation, or writing, or replace this statement with an accurate description before submission.

**Author contributions:** To be completed using the CRediT taxonomy before submission.

**Data availability:** Participant-level NHS Wales and UK Biobank data cannot be redistributed. Aggregate outputs, source code, deterministic model object, synthetic input, protocol, phase map, quality-control reports, and checksum manifest are available in the governed analysis package, subject to institutional and UK Biobank requirements.

**Generative-AI disclosure:** Generative-AI-assisted tools were used for code review, literature retrieval support, document structuring, and language editing. No participant-level data were transmitted to a generative-AI service. The authors verified the analyses, references, declarations, and final wording and accept responsibility for the manuscript.

## References

1. Beheshti SO, Madsen CM, Varbo A, Nordestgaard BG. Worldwide prevalence of familial hypercholesterolemia: meta-analyses of 11 million subjects. *J Am Coll Cardiol.* 2020;75:2553–2566. doi:10.1016/j.jacc.2020.03.057.
2. Nordestgaard BG, Chapman MJ, Humphries SE, et al. Familial hypercholesterolaemia is underdiagnosed and undertreated in the general population: guidance for clinicians to prevent coronary heart disease. Consensus statement of the European Atherosclerosis Society. *Eur Heart J.* 2013;34:3478–3490a. doi:10.1093/eurheartj/eht273.
3. Vallejo-Vaz AJ, Stevens CAT, Lyons ARM, et al. Global perspective of familial hypercholesterolaemia: a cross-sectional study from the EAS Familial Hypercholesterolaemia Studies Collaboration (FHSC). *Lancet.* 2021;398:1713–1725. doi:10.1016/S0140-6736(21)01122-3.
4. Wiegman A, Gidding SS, Watts GF, et al. Familial hypercholesterolaemia in children and adolescents: gaining decades of life by optimizing detection and treatment. *Eur Heart J.* 2015;36:2425–2437. doi:10.1093/eurheartj/ehv157.
5. Ference BA, Ginsberg HN, Graham I, et al. Low-density lipoproteins cause atherosclerotic cardiovascular disease. 1. Evidence from genetic, epidemiologic, and clinical studies. A consensus statement from the European Atherosclerosis Society Consensus Panel. *Eur Heart J.* 2017;38:2459–2472. doi:10.1093/eurheartj/ehx144.
6. Khera AV, Won HH, Peloso GM, et al. Diagnostic yield and clinical utility of sequencing familial hypercholesterolemia genes in patients with severe hypercholesterolemia. *J Am Coll Cardiol.* 2016;67:2578–2589. doi:10.1016/j.jacc.2016.03.520.
7. Mach F, Baigent C, Catapano AL, et al. 2019 ESC/EAS guidelines for the management of dyslipidaemias: lipid modification to reduce cardiovascular risk. *Eur Heart J.* 2020;41:111–188. doi:10.1093/eurheartj/ehz455.
8. Paquette M, Dufour R, Baass A. The Montreal-FH-SCORE: a new score to predict cardiovascular events in familial hypercholesterolemia. *J Clin Lipidol.* 2017;11:80–86. doi:10.1016/j.jacl.2016.10.004.
9. Paquette M, Brisson D, Dufour R, et al. Cardiovascular disease in familial hypercholesterolemia: validation and refinement of the Montreal-FH-SCORE. *J Clin Lipidol.* 2017;11:1161–1167.e3. doi:10.1016/j.jacl.2017.07.008.
10. Paquette M, Bernard S, Cariou B, et al. Familial Hypercholesterolemia-Risk-Score: a new score predicting cardiovascular events and cardiovascular mortality in familial hypercholesterolemia. *Arterioscler Thromb Vasc Biol.* 2021;41:2632–2640. doi:10.1161/ATVBAHA.121.316106.
11. Pérez de Isla L, Alonso R, Mata N, et al. Predicting cardiovascular events in familial hypercholesterolemia: the SAFEHEART Registry. *Circulation.* 2017;135:2133–2144. doi:10.1161/CIRCULATIONAHA.116.024541.
12. Tamehri Zadeh SS, Chan DC, Pang J, et al. Canadian and French risk scores are valid in identifying cardiovascular disease in Australian patients with familial hypercholesterolemia. *Can J Cardiol.* 2025;41:2244–2251. doi:10.1016/j.cjca.2025.07.042.
13. Sniderman AD, Thanassoulis G, Glavinovic T, et al. Apolipoprotein B particles and cardiovascular disease: a narrative review. *JAMA Cardiol.* 2019;4:1287–1295. doi:10.1001/jamacardio.2019.3780.
14. Sniderman AD, Thanassoulis G, Williams K, et al. Apo B versus cholesterol in estimating cardiovascular risk and in guiding therapy: report of the thirty-person/ten-country panel. *J Intern Med.* 2006;259:455–461. doi:10.1111/j.1365-2796.2006.01616.x.
15. Johannesen CDL, Mortensen MB, Langsted A, Nordestgaard BG. Apolipoprotein B and non-HDL cholesterol better reflect residual risk than LDL cholesterol in statin-treated patients. *J Am Coll Cardiol.* 2021;77:1439–1450. doi:10.1016/j.jacc.2021.01.027.
16. Mora S, Buring JE, Ridker PM. Discordance of low-density lipoprotein (LDL) cholesterol with alternative LDL-related measures and future coronary events. *Circulation.* 2014;129:553–561. doi:10.1161/CIRCULATIONAHA.113.005873.
17. Walldius G, de Faire U, Alfredsson L, et al. Long-term risk of a major cardiovascular event by apoB, apoA1, and the apoB/apoA1 ratio: experience from the Swedish AMORIS cohort. *PLoS Med.* 2021;18:e1003853. doi:10.1371/journal.pmed.1003853.
18. Sampson M, Ling C, Sun Q, et al. A new equation for calculation of low-density lipoprotein cholesterol in patients with normolipidemia and/or hypertriglyceridemia. *JAMA Cardiol.* 2020;5:540–548. doi:10.1001/jamacardio.2020.0013.
19. Genedy N, Zouwail S. ApoB/LDL-C discordance as a predictor of atherosclerotic cardiovascular disease in genetically confirmed heterozygous familial hypercholesterolemia: a hypothesis-generating cohort study. *J Clin Lipidol.* 2026;20:490–503. doi:10.1016/j.jacl.2025.11.008.
20. Correction to "ApoB/LDL-C discordance as a predictor of atherosclerotic cardiovascular disease in genetically confirmed heterozygous familial hypercholesterolemia: a hypothesis-generating cohort study." *J Clin Lipidol.* 2026. doi:10.1016/j.jacl.2026.03.024.
21. Sudlow C, Gallacher J, Allen N, et al. UK Biobank: an open access resource for identifying the causes of a wide range of complex diseases of middle and old age. *PLoS Med.* 2015;12:e1001779. doi:10.1371/journal.pmed.1001779.
22. Bycroft C, Freeman C, Petkova D, et al. The UK Biobank resource with deep phenotyping and genomic data. *Nature.* 2018;562:203–209. doi:10.1038/s41586-018-0579-z.
23. Patel AP, Wang M, Fahed AC, et al. Association of rare pathogenic DNA variants for familial hypercholesterolemia, hereditary breast and ovarian cancer syndrome, and Lynch syndrome with disease risk in adults according to family history. *JAMA Netw Open.* 2020;3:e203959. doi:10.1001/jamanetworkopen.2020.3959.
24. Fahed AC, Wang M, Patel AP, et al. Association of the interaction between familial hypercholesterolemia variants and adherence to a healthy lifestyle with risk of coronary artery disease. *JAMA Netw Open.* 2022;5:e222687. doi:10.1001/jamanetworkopen.2022.2687.
25. Richards S, Aziz N, Bale S, et al. Standards and guidelines for the interpretation of sequence variants: a joint consensus recommendation of the American College of Medical Genetics and Genomics and the Association for Molecular Pathology. *Genet Med.* 2015;17:405–424. doi:10.1038/gim.2015.30.
26. Tavtigian SV, Greenblatt MS, Harrison SM, et al. Modeling the ACMG/AMP variant classification guidelines as a Bayesian classification framework. *Genet Med.* 2018;20:1054–1060. doi:10.1038/gim.2017.210.
27. Brnich SE, Abou Tayoun AN, Couch FJ, et al. Recommendations for application of the functional evidence PS3/BS3 criterion using the ACMG/AMP sequence variant interpretation framework. *Genome Med.* 2019;12:3. doi:10.1186/s13073-019-0690-2.
28. Collins GS, Moons KGM, Dhiman P, et al. TRIPOD+AI statement: updated guidance for reporting clinical prediction models that use regression or machine learning methods. *BMJ.* 2024;385:e078378. doi:10.1136/bmj-2023-078378.
29. Collins GS, Reitsma JB, Altman DG, Moons KGM. Transparent reporting of a multivariable prediction model for individual prognosis or diagnosis (TRIPOD): the TRIPOD statement. *BMC Med.* 2015;13:1. doi:10.1186/s12916-014-0241-z.
30. Wolff RF, Moons KGM, Riley RD, et al. PROBAST: a tool to assess the risk of bias and applicability of prediction model studies. *Ann Intern Med.* 2019;170:51–58. doi:10.7326/M18-1376.
31. Moons KGM, Wolff RF, Riley RD, et al. PROBAST: a tool to assess risk of bias and applicability of prediction model studies: explanation and elaboration. *Ann Intern Med.* 2019;170:W1–W33. doi:10.7326/M18-1377.
32. Moons KGM, de Groot JAH, Bouwmeester W, et al. Critical appraisal and data extraction for systematic reviews of prediction modelling studies: the CHARMS checklist. *PLoS Med.* 2014;11:e1001744. doi:10.1371/journal.pmed.1001744.
33. von Elm E, Altman DG, Egger M, et al. The Strengthening the Reporting of Observational Studies in Epidemiology (STROBE) statement. *PLoS Med.* 2007;4:e296. doi:10.1371/journal.pmed.0040296.
34. Riley RD, Ensor J, Snell KIE, et al. Calculating the sample size required for developing a clinical prediction model. *BMJ.* 2020;368:m441. doi:10.1136/bmj.m441.
35. Riley RD, Snell KIE, Ensor J, et al. Minimum sample size for developing a multivariable prediction model: part II — binary and time-to-event outcomes. *Stat Med.* 2019;38:1276–1296. doi:10.1002/sim.7992.
36. van Smeden M, Moons KGM, de Groot JAH, et al. Sample size for binary logistic prediction models: beyond events per variable criteria. *Stat Methods Med Res.* 2019;28:2455–2474. doi:10.1177/0962280218784726.
37. Riley RD, Debray TPA, Collins GS, et al. Minimum sample size for external validation of a clinical prediction model with a binary outcome. *Stat Med.* 2021;40:4230–4251. doi:10.1002/sim.9025.
38. Ramspek CL, Jager KJ, Dekker FW, et al. External validation of prognostic models: what, why, how, when and where? *Clin Kidney J.* 2021;14:49–58. doi:10.1093/ckj/sfaa188.
39. Riley RD, Archer L, Snell KIE, et al. Evaluation of clinical prediction models (part 2): how to undertake an external validation study. *BMJ.* 2024;384:e074820. doi:10.1136/bmj-2023-074820.
40. Vickers AJ, van Calster B, Steyerberg EW. A simple, step-by-step guide to interpreting decision curve analysis. *Diagn Progn Res.* 2019;3:18. doi:10.1186/s41512-019-0064-7.
41. Gallo A, Charrière S, Vimont A, et al. SAFEHEART risk-equation and cholesterol-year-score are powerful predictors of cardiovascular events in French patients with familial hypercholesterolemia. *Atherosclerosis.* 2020;306:41–49. doi:10.1016/j.atherosclerosis.2020.06.011.
42. McKay AJ, Gunn LH, Ray KK. Assessing the external validity of the SAFEHEART risk prediction model in patients with familial hypercholesterolaemia in an English routine care cohort. *Atherosclerosis.* 2022;358:68–74. doi:10.1016/j.atherosclerosis.2022.07.011.

