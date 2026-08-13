# A de novo apolipoprotein-discordance classifier for established atherosclerotic cardiovascular disease in genetically defined familial hypercholesterolaemia: reciprocal transport between a specialist clinic and UK Biobank

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

- CALON-N is a new seven-variable classifier fitted from raw clinical and laboratory measurements; no published score is an input.
- Its selected predictors are age, sex, HDL-C, hypertension, smoking, log(apoB/LDL-C), and log(apoA1).
- Discrimination transported asymmetrically: AUC 0.767 from DRAGON to UK Biobank and 0.848 in the reverse direction.
- CALON-N exceeded adapted FH-Risk-Score and SAFEHEART in UK Biobank but did not exceed Montreal-FH-SCORE, age plus sex in DRAGON, or all comparators in subgroups.
- Contemporary post-event lipids, target-informed architecture selection, calibration drift, and few subgroup events prohibit prospective-risk or clinical-deployment claims.

## Abstract

**Background:** Familial hypercholesterolaemia (FH) risk equations were developed in clinically ascertained cohorts and use different lipid constructs. Whether apoB–LDL discordance supports a transportable, de novo model among genetically defined FH carriers is uncertain.

**Methods:** We performed a retrospective cross-sectional model-development and reciprocal-transport study. DRAGON comprised 424 genetically ascertained specialist-clinic participants (62 with established ASCVD; 219 family clusters). The primary UK Biobank cohort comprised 890 coordinate-linked *LDLR* carriers with a local ClinVar pathogenic/likely pathogenic classification (57 prevalent ASCVD cases; 62 qualifying-variant connected components); a P/LP-or-predicted-loss-of-function union of 1,264 carriers (80 cases) was secondary. Ten low-dimensional penalised-logistic candidates were locked using raw predictors only. Missing-value replacement, scaling, tuning, and apoB-on-LDL residualisation were restricted to training data. Ridge penalty was selected by grouped cross-validated Brier score. The architecture maximising the lower of the two reciprocal-transport AUCs after prespecified coefficient-sign checks was retained. Published scores were comparators, not model inputs. Uncertainty used target family- or variant-component bootstrap.

**Results:** CALON-N contained age, male sex, HDL-C, hypertension, ever smoking, log(apoB/LDL-C), and log(apoA1). Candidate-specific repeated nested grouped AUCs were 0.893 in DRAGON and 0.794 in UK Biobank. With DRAGON-fitted coefficients, UK Biobank AUC was 0.767 (95% CI 0.712–0.828), versus 0.775 for adapted Montreal-FH-SCORE (difference −0.008, 95% CI −0.036 to 0.007), 0.696 for adapted FH-Risk-Score, and 0.541 for adapted SAFEHEART. With UK Biobank-fitted coefficients, DRAGON AUC was 0.848 (0.796–0.896), below age plus sex (0.895; difference −0.047, −0.100 to 0.003) and Montreal (0.893; difference −0.045, −0.093 to −0.002). Calibration did not transport: expected:observed ratios were 3.00 in UK Biobank and 0.45 in DRAGON. Performance was not uniformly superior across evaluable subgroups.

**Conclusions:** A de novo apoB-discordance model was feasible and retained moderate-to-high discrimination across two genetically defined FH settings, but it did not outperform all comparators or transport absolute probabilities. The data reject universal-superiority and prospective-risk claims. CALON-N is a research classifier requiring validation using pre-event apolipoproteins in an independent FH registry.

Keywords: familial hypercholesterolaemia; apolipoprotein B; LDL cholesterol; cardiovascular disease; prediction model; transportability; UK Biobank

## Introduction

Heterozygous familial hypercholesterolaemia confers lifelong exposure to elevated LDL cholesterol and substantial heterogeneity in atherosclerotic cardiovascular disease (ASCVD).[1–3] Existing FH-specific instruments address that heterogeneity differently. Montreal-FH-SCORE was derived for prevalent cardiovascular disease using age, HDL-C, sex, hypertension, and smoking.[4] FH-Risk-Score predicts incident events using categorical age, untreated or imputed untreated LDL-C, HDL-C, sex, hypertension, smoking, and lipoprotein(a).[5] SAFEHEART-RE is an incident-event equation in which previous ASCVD is a major predictor.[6] Their distinct endpoints and ascertainment settings make comparative transport a scientific question rather than a simple leaderboard.

ApoB measures the number of circulating atherogenic particles, whereas LDL-C measures their cholesterol content. Their ratio can therefore encode particle–cholesterol discordance, but it is also mathematically coupled to LDL-C and can be modified by treatment and reverse causation.[7] In prior analyses of the present data, log(apoB/LDL-C) added discrimination to age and sex in cross-sectional DRAGON and UK Biobank analyses, while apoB and LDL-C considered individually were inconsistent. However, LDL-C alone matched or exceeded the ratio in some UK Biobank carrier definitions; Lp(a) and apoA1 increments were not stable. Those findings required a de novo, whole-pipeline test rather than continued variable-by-variable addition to an already selected model.

We therefore developed CALON-N using raw clinical and laboratory variables only. Published scores were excluded from the candidate architecture and retained solely as comparators. Our objectives were to quantify reciprocal transport between a specialist lipid-clinic cohort and a population-biobank carrier cohort, test whether the same architecture retained physiologically coherent coefficients, and determine whether any claim of all-comparator or all-subgroup superiority was supported.

## Methods

### Study design and estimand

This was a retrospective cross-sectional case-identification study. The estimand was the probability that established ASCVD was already recorded at the time of the available contemporary clinical and laboratory phenotype. It was not first-event incidence, 5- or 10-year absolute risk, treatment benefit, or a causal effect of any biomarker. Contemporary lipid measurements could occur after ASCVD and treatment intensification.

The protocol, candidates, sign rules, outcomes, metrics, and stopping rule were written before phase-B modelling. Earlier programme analyses had already examined outcomes in both cohorts. Architecture selection is consequently target-informed, retrospective multi-cohort development—not protected external validation.

### DRAGON specialist-clinic cohort

The DRAGON export contained 424 participants and 202 columns. Every DRAGON record linked to the canonical PASS registry using participant identifiers in memory; 412 family labels agreed directly and 12 were realigned, producing 219 canonical family clusters. The registry ASCVD flag identified 62 cases. Component-union and hard-coronary definitions identified 66 and 56 cases, respectively, and were sensitivity outcomes.

DRAGON contained clinically recorded variants across *LDLR* (n=363), *APOB* (n=50), *PCSK9* (n=5), and other genes/labels. A conservative archived exact-HGVS *LDLR* P/LP sensitivity contained 164 participants and 20 cases; it is not treated as the full clinically adjudicated cohort because unparseable or locally absent variants cannot be inferred to be non-pathogenic.

### UK Biobank carrier cohorts

The primary UK Biobank analysis used the complete participant-to-variant call file. Calls were linked by genomic coordinate to the local ClinVar and VEP annotations. The primary set comprised 890 *LDLR* carriers with a local P/LP classification and 57 prevalent ASCVD cases. Review-status enforcement was unavailable in the local table; the cohort is therefore not described as an exact current-ClinVar or laboratory-adjudicated reproduction. Bootstrap clusters were connected components in the carrier–qualifying-variant bipartite graph, preventing non-qualifying calls from inducing dependence.

The prespecified union added predicted loss-of-function variants and contained 1,264 carriers and 80 cases. Exact Patel and Fahed published-variant sets were used in a separate column/phenotype concordance programme and were not substituted for the present model cohort. The current strict LDLR bridge (890 carriers) is distinct from the exploratory three-gene TUDOR flag, which lacks variant-level pathogenicity evidence for *APOB* and *PCSK9*.

### Outcome

DRAGON used `ASCVD_combined`; UK Biobank used `prevalent_ascvd`. Endpoint components are not perfectly harmonised. In particular, the local UK Biobank proxy does not reproduce all peripheral arterial disease and revascularisation components used by Patel et al. The common interpretation is therefore recorded established ASCVD, not exact hard MACE.

### Candidate predictors and model selection

Ten candidates were locked: age plus sex; age, sex, and log(apoB/LDL-C); a five-variable clinical model; the clinical model plus log(apoB/LDL-C); and prespecified additions of diabetes, log(TG/HDL-C), log Lp(a), log apoA1, a residualised apoB term with LDL-C retained, or a parsimonious hypertension model. No published score or fitted comparator was an input.

Continuous inputs were checked against clinical bounds. Missing values were replaced by source-training medians; preprocessing was repeated within resampling folds. Log ratios were derived after replacement. Models used L2-penalised logistic regression. The ridge penalty was selected from C={0.01, 0.03, 0.10, 0.30, 1.00, 3.00} by lowest grouped cross-validated Brier score. Families remained intact in DRAGON folds and qualifying-variant components remained intact in UK Biobank folds.

Prespecified directions were positive for age, male sex, hypertension, smoking, diabetes, apoB/LDL-C, TG/HDL-C, Lp(a), LDL-C, and apoB-discordance; negative for HDL-C and apoA1. A candidate with a sign violation in either source fit was ineligible. Among eligible models, the architecture with the highest minimum AUC across DRAGON→UK Biobank and UK Biobank→DRAGON was selected. This maximin rule tests transport but uses both outcome sets and is exploratory.

### Comparators

Comparators were age plus sex, Montreal-FH-SCORE, FH-Risk-Score, and SAFEHEART. They were calculated on the same target participants. Montreal used its published coefficient structure with source-cohort age and HDL anchors. FH-Risk-Score was adapted because untreated LDL-C and Lp(a) units were not uniformly recoverable. SAFEHEART was adapted by omitting prior ASCVD, which would be circular for a prevalent-ASCVD outcome, and by substituting available smoking and BMI inputs. These endpoint/input adaptations preclude a claim that the exact published instruments were externally validated.

### Performance and uncertainty

Discrimination used AUC. Candidate-specific internal estimates used five repeats of nested five-fold grouped validation, with penalty tuning inside each outer-training partition. External transport used source-fitted preprocessing and coefficients without target recalibration. Target families or qualifying-variant components were resampled 4,000 times for AUC and paired delta-AUC intervals. These intervals condition on the fitted source model and do not include source-development uncertainty.

Calibration was described by Brier score, calibration intercept, slope, and expected:observed ratio. A decision-curve analysis was generated during development but withdrawn at final QC because age plus sex, Montreal, and FH-Risk-Score were ranking scores/linear predictors rather than probabilities on the same absolute-risk scale as CALON-N. Prespecified subgroups were sex, age relative to the cohort median, recorded lipid treatment, diabetes, and Lp(a) above/below 143 in source units. Fewer than 10 cases was non-estimable; 10–19 was descriptive. Subgroups did not influence selection.

### Governance and reporting

All model construction occurred locally. Only aggregate tables, figures, code, and model objects were written. No participant identifier, family identifier, variant coordinate, participant row, or participant-level prediction was saved. Reporting was audited against TRIPOD+AI, STROBE, and PROBAST.[8–10]

## Results

### Cohorts and phenotype availability

DRAGON participants were younger than UK Biobank carriers (mean 48.4±18.6 versus 57.3±8.0 years) and more frequently recorded as treated (86.6% versus 40.6%). Established ASCVD prevalence was 14.6% and 6.4%, respectively. Median LDL-C was 4.70 mmol/L in DRAGON and 3.86 mmol/L in UK Biobank; apoB medians were 1.28 and 1.12 g/L. ApoB, apoA1, and Lp(a) were each available for approximately three quarters of DRAGON, compared with 94%, 88%, and 76% in UK Biobank.

### Candidate selection and internal validation

CALON-N was selected after the sign gate. It contained age, male sex, HDL-C, hypertension, ever smoking, log(apoB/LDL-C), and log(apoA1). Candidate-specific nested grouped AUC was 0.893 in DRAGON and 0.794 in strict UK Biobank. The corresponding values for age plus sex were 0.886 and 0.710, and for the five-variable clinical model 0.891 and 0.750.

The raw transformed-unit representation of the pooled penalised research equation was:

```text
logit(p) = -5.673054
           + 0.112263 × age_years
           + 0.580373 × male
           - 0.629887 × HDL_C_mmol_L
           + 0.105120 × hypertension
           + 0.143724 × ever_smoker
           + 1.910359 × log(apoB_g_L / LDL_C_mmol_L)
           - 1.672421 × log(apoA1_g_L)
```

This pooled equation was fitted after the transport analyses and has no untouched validation. It is supplied only as a frozen candidate for future research; the reciprocal-transport results below used separate source-fitted equations.

### DRAGON to UK Biobank transport

With coefficients fitted in DRAGON, CALON-N achieved AUC 0.767 (95% CI 0.712–0.828) in 890 strict UK Biobank carriers. AUC was 0.732 for age plus sex, 0.775 for Montreal, 0.696 for FH-Risk-Score, and 0.541 for SAFEHEART. Paired differences were +0.035 (0.018–0.060) versus age plus sex, −0.008 (−0.036 to 0.007) versus Montreal, +0.071 (0.024–0.110) versus FH-Risk-Score, and +0.227 (0.122–0.294) versus SAFEHEART.

The P/LP-or-LoF union yielded AUC 0.767 (0.719–0.813). CALON-N remained similar to Montreal (difference −0.001, −0.025 to 0.010) and above the adapted FH-Risk-Score and SAFEHEART implementations.

### UK Biobank to DRAGON transport

With coefficients fitted in strict UK Biobank carriers, CALON-N achieved AUC 0.848 (0.796–0.896) in DRAGON. Age plus sex achieved 0.895, Montreal 0.893, FH-Risk-Score 0.857, and SAFEHEART 0.800. CALON-N was below Montreal by −0.045 (−0.093 to −0.002), was imprecisely below age plus sex by −0.047 (−0.100 to 0.003), and was not separable from FH-Risk-Score or SAFEHEART.

In the conservative archived exact-HGVS LDLR P/LP DRAGON subset (164 participants, 20 cases), UK Biobank-fitted CALON-N had AUC 0.827. AUCs for the component-union and hard-coronary outcomes in all DRAGON were 0.847 and 0.843.

### Calibration and missingness sensitivity

Absolute probabilities failed to transport. In UK Biobank, the DRAGON-fitted model overpredicted cases approximately threefold (E:O 3.00), with calibration intercept −1.45 and slope 0.95. In DRAGON, the UK Biobank-fitted model underpredicted (E:O 0.45), with intercept 0.66 and slope 0.75.

No comparative decision-curve claim is reported. The generated table applied probability thresholds to comparator outputs that were not all calibrated probabilities, so its net-benefit contrasts were not valid. The marked calibration drift also precludes recommending a clinical threshold for CALON-N.

Complete-case transport contained 726 UK Biobank participants/50 cases and 304 DRAGON participants/45 cases. AUCs were 0.753 and 0.891, respectively, indicating that missing-value transport contributed to—but did not fully explain—the directional difference.

### Subgroups

No all-subgroup claim was supported. In UK Biobank, CALON-N was close to but below the best comparator among men (0.708 versus 0.715), treated carriers (0.659 versus 0.672), participants without diabetes (0.767 versus 0.773), and those below the Lp(a) threshold (0.740 versus 0.751). In DRAGON, age plus sex or Montreal was higher in most evaluable subgroups. Untreated, younger, diabetic, and Lp(a)-high strata were frequently non-estimable because they contained fewer than 10 cases. No interaction claim was made.

## Discussion

CALON-N is genuinely de novo: its predictors and coefficients were fitted from raw clinical measurements, and no published risk score enters the equation. It retained moderate-to-high discrimination in reciprocal transport and had physiologically coherent coefficients. Nevertheless, it did not become the requested universal champion. Montreal remained higher in one direction; age plus sex was exceptionally strong in DRAGON; calibration reversed across settings; and subgroup point estimates were heterogeneous.

The result explains why repeated optimisation did not solve the problem. The cohorts differ not only in case prevalence but in age distribution, clinical ascertainment, treatment recognition, variant definition, and timing of biomarkers relative to ASCVD. DRAGON is a specialist-clinic export in which contemporary lipids commonly follow disease and treatment. UK Biobank is older and population ascertained. The apoB/LDL term may therefore encode both particle discordance and treatment-related depletion of LDL cholesterol. Its positive coefficient is biologically interpretable, but cross-sectional discrimination cannot establish prospective or causal meaning.

The apoA1 term improved the locked maximin criterion and was directionally protective. However, HDL-C and apoA1 are correlated, and approximately one quarter of DRAGON lacked apoA1. Ridge shrinkage limits coefficient instability but does not turn missing post-event phenotypes into baseline predictors. The complete-case sensitivity improved reverse transport but did not create a universal win.

The UK Biobank exposure audit is reassuring but bounded. Coordinate-verified local LDLR P/LP carriers are the primary auditable cohort. Exact published LDLR SNVs reproduced Patel-like lipid phenotypes and yielded an ASCVD association concordant with Patel's LDLR-specific estimate in a separate analysis, supporting column and variant linkage. They do not make the present endpoint or cohort an exact Patel replication. The exploratory three-gene TUDOR flag has a different denominator and lacks variant-level pathogenicity evidence for APOB and PCSK9; it was not used here.[11,12]

Our findings also support separating model development from model updating. A prospective Welsh programme with few events is unlikely to re-estimate all FH-Risk-Score coefficients more precisely than the original multi-registry study. A distinct, potentially valuable project is to update a validated incident-risk score using ascertainment-specific baseline hazards for probands and cascade-detected relatives. Such an update is not CALON-N, is not de novo, and should be assessed with family-disjoint out-of-fold baseline estimation, censoring and competing-death methods, shrinkage, comparison with ordinary intercept recalibration, and external registry validation. We did not merge that prospective calibration question with the present cross-sectional classifier.

### Strengths and limitations

Strengths include complete family realignment, full coordinate-level UK Biobank carrier bridging, qualifying-variant connected-component resampling, raw-variable rather than score-stack development, fold-local preprocessing and penalty tuning, reciprocal transport, sign checks, and explicit negative stopping rules.

Limitations dominate the interpretation. First, biomarkers were contemporary and often post-event; CALON-N is not a prospective risk model. Second, architecture selection used both cohorts after extensive prior programme work, so no result is independent external validation. Third, only 62 and 57 cases were available, candidate comparison was multiplicity-prone, and conditional target bootstraps omit source-training uncertainty. Fourth, missing values used median replacement; multiple imputation and measurement-error models could change coefficients. Fifth, endpoint components, treatment, smoking, hypertension, Lp(a) units, and variant classifications were not perfectly harmonised. Sixth, the comparator implementations were adapted and therefore do not test exact published tools. Seventh, comparative decision analysis was not possible because comparator outputs were not calibrated onto a common probability scale. Eighth, most subgroups were underpowered. Finally, the pooled equation has no untouched validation and absolute probabilities were substantially miscalibrated.

## Conclusions

CALON-N is a novel, sign-coherent, raw-variable classifier for established ASCVD in genetically defined FH. It transported with AUCs of 0.767 and 0.848, but did not beat Montreal, age plus sex, or every comparator across directions and subgroups, and its probabilities did not transport. It should be frozen as a hypothesis for a third cohort with pre-event apoB, LDL-C and apoA1—not promoted as a 10-year risk score or clinical tool.

## Declarations

**Ethics and data governance:** To be completed from the governing PASS/DRAGON and UK Biobank approvals and application number before submission.

**Funding:** To be completed by the corresponding author.

**Conflicts of interest:** To be completed by all authors.

**Data availability:** Participant-level NHS Wales and UK Biobank data cannot be redistributed. Aggregate outputs, code, model object, synthetic input, and checksum manifest are available in the analysis package subject to institutional governance.

**Generative-AI disclosure:** Generative-AI-assisted tools were used for code review, document structuring, and language editing. No participant-level data were transmitted to a generative-AI service. The authors must verify the analysis, references, and final wording and accept responsibility for the manuscript.

## References

1. Beheshti SO, Madsen CM, Varbo A, Nordestgaard BG. Worldwide prevalence of familial hypercholesterolemia: meta-analyses of 11 million subjects. *J Am Coll Cardiol.* 2020;75:2553–2566. doi:10.1016/j.jacc.2020.03.057.
2. Ference BA, Ginsberg HN, Graham I, et al. Low-density lipoproteins cause atherosclerotic cardiovascular disease. *Eur Heart J.* 2017;38:2459–2472. doi:10.1093/eurheartj/ehx144.
3. Khera AV, Won HH, Peloso GM, et al. Diagnostic yield and clinical utility of sequencing familial hypercholesterolemia genes in patients with severe hypercholesterolemia. *J Am Coll Cardiol.* 2016;67:2578–2589. doi:10.1016/j.jacc.2016.03.520.
4. Paquette M, Dufour R, Baass A. The Montreal-FH-SCORE: a new score to predict cardiovascular events in familial hypercholesterolemia. *J Clin Lipidol.* 2017;11:80–86. doi:10.1016/j.jacl.2016.10.004.
5. Paquette M, Bernard S, Cariou B, et al. Familial Hypercholesterolemia-Risk-Score. *Arterioscler Thromb Vasc Biol.* 2021;41:2632–2640. doi:10.1161/ATVBAHA.121.316106.
6. Pérez de Isla L, Alonso R, Mata N, et al. Predicting cardiovascular events in familial hypercholesterolemia: the SAFEHEART Registry. *Circulation.* 2017;135:2133–2144. doi:10.1161/CIRCULATIONAHA.116.024541.
7. Sniderman AD, Thanassoulis G, Glavinovic T, et al. Apolipoprotein B particles and cardiovascular disease: a narrative review. *JAMA Cardiol.* 2019;4:1287–1295. doi:10.1001/jamacardio.2019.3780.
8. Collins GS, Moons KGM, Dhiman P, et al. TRIPOD+AI statement. *BMJ.* 2024;385:e078378. doi:10.1136/bmj-2023-078378.
9. Wolff RF, Moons KGM, Riley RD, et al. PROBAST: a tool to assess risk of bias and applicability of prediction model studies. *Ann Intern Med.* 2019;170:51–58. doi:10.7326/M18-1376.
10. von Elm E, Altman DG, Egger M, et al. The STROBE statement. *PLoS Med.* 2007;4:e296. doi:10.1371/journal.pmed.0040296.
11. Patel AP, Wang M, Fahed AC, et al. Association of rare pathogenic DNA variants for familial hypercholesterolemia, hereditary breast and ovarian cancer syndrome, and Lynch syndrome with disease risk in adults according to family history. *JAMA Netw Open.* 2020;3:e203959. doi:10.1001/jamanetworkopen.2020.3959.
12. Fahed AC, Wang M, Patel AP, et al. Association of the interaction between familial hypercholesterolemia variants and adherence to a healthy lifestyle with risk of coronary artery disease. *JAMA Netw Open.* 2022;5:e222687. doi:10.1001/jamanetworkopen.2022.2687.
13. Sudlow C, Gallacher J, Allen N, et al. UK Biobank: an open access resource for identifying causes of disease. *PLoS Med.* 2015;12:e1001779. doi:10.1371/journal.pmed.1001779.
14. Bycroft C, Freeman C, Petkova D, et al. The UK Biobank resource with deep phenotyping and genomic data. *Nature.* 2018;562:203–209. doi:10.1038/s41586-018-0579-z.
