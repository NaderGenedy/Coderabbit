# CALON-N full analytical methods and results compendium

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

Version: 9 August 2026

Purpose: This document is the traceable analytical companion to the CALON-N manuscript. It contains the complete methods and all aggregate numerical results used in the manuscript. It is not a clinical-use document and contains no participant-level rows, identifiers, variant coordinates, or predictions.

## 1. Analysis identity and estimand

CALON-N is a cross-sectional classifier of already-recorded atherosclerotic cardiovascular disease (ASCVD) among genetically defined familial hypercholesterolaemia (FH) participants. The estimand is the probability of established ASCVD at the time represented by the available contemporary phenotype. The analysis does not estimate first-event incidence, five- or ten-year risk, treatment benefit, or a causal biomarker effect.

Phase A evaluated score augmentation and selected `montreal_ratio`; it is diagnostic only. Phase B is the de novo analysis required by Protocol Amendment 1. Its canonical selection file is `outputs/scratch_selection.json`, and it selected `calon_n_apoa1` from ten raw-variable candidates. Published scores were comparators only.

## 2. Source snapshots and flow

| Stage | DRAGON | UKB strict local LDLR P/LP | UKB P/LP-or-LoF union |
|---|---:|---:|---:|
| Source records/calls | 424 exported participants | 6,597,041 carrier–variant call rows; 468,965 unique participants | Same call source |
| Qualifying exposure before phenotype linkage | Clinic genetic labels | 890 local P/LP participants after conflicting-class exclusion | 1,264 P/LP-or-LoF participants |
| Linked to phenotype master and eligible | 424/424 | 890/890 | 1,264/1,264 |
| Primary outcome cases | 62 | 57 | 80 |
| Analysis denominator | 424 | 890 | 1,264 |
| Resampling unit | 219 canonical families | 62 qualifying-variant connected components | 66 qualifying-variant connected components |

DRAGON linked to the canonical PASS family record for 424/424 participants. Family labels agreed directly in 412, while 12 were realigned using the canonical PASS family identifier. No participant was excluded for predictor missingness because completion was part of the source-training pipeline.

The DRAGON analytical file was obtained locally on 2 August 2026 and the analysis was locked on 9 August 2026. The file contains a uniform administrative `TodayDate` of 5 August 2024 but no validated recruitment window or upstream export timestamp. The local UKB call file was dated 19 March 2026, the local ClinVar/VEP exports 8 June 2026, and all strict-carrier baseline assessments fell between 19 April 2007 and 22 September 2010. The upstream UKB genomic-release and ClinVar-release identifiers were not preserved.

## 3. Carrier and outcome definitions

### DRAGON

The primary outcome was `ASCVD_combined>0`. Component fields overlapped:

| Component | Participants positive |
|---|---:|
| Myocardial infarction/acute coronary syndrome | 34 |
| Percutaneous coronary intervention | 21 |
| Coronary artery bypass grafting | 30 |
| Angina | 24 |
| Transient ischaemic attack | 9 |
| Peripheral vascular disease | 4 |
| Primary registry flag | 62 |
| Six-component union sensitivity | 66 |
| Hard-coronary union sensitivity | 56 |

The clinic export contained 363 *LDLR*, 50 *APOB*, 5 *PCSK9*, and 6 other/unspecified gene labels. A conservative archived exact-HGVS *LDLR* P/LP sensitivity contained 164 participants, 20 cases, and 79 families.

### UK Biobank

Chromosome, position, reference, and alternate alleles were normalised across the full call file and local annotations. The strict definition required a local ClinVar P/LP *LDLR* call and excluded locally conflicting calls. Review status was unavailable. The union added local ClinVar- or VEP-defined predicted loss of function.

Dependence was represented by connected components of a participant–qualifying-variant bipartite graph. Strict and union graphs were constructed separately. Non-qualifying calls could not join clusters.

The outcome was `prevalent_ascvd>0`. In strict carriers, 96 had any `first_ascvd` date: 57 before baseline and 39 after baseline. Only the 57 pre-baseline records entered the prevalent outcome. Component equivalence to DRAGON was not available.

## 4. Raw predictors, coding, and coverage

| Model term | Raw source | Coding/transformation | DRAGON observed | UKB strict observed | UKB union observed |
|---|---|---|---:|---:|---:|
| Age | age at phenotype/baseline | years; bounded 5–105 | 424 | 890 | 1,264 |
| Male | sex | 1 male, 0 female | 424 | 890 | 1,264 |
| HDL-C | routine chemistry | mmol/L; bounded 0.2–5 | 398 | 786 | 1,116 |
| Hypertension | source BP/medication definition | 1 yes, 0 no | 424 | 840 | 1,176 |
| Ever smoking | source smoking field | 1 ever, 0 never | 424 | 890 | 1,264 |
| LDL-C | routine chemistry | mmol/L; bounded 0.3–20 | 402 | 850 | 1,208 |
| apoB | immunoassay/chemistry field | g/L; bounded 0.2–4 | 323 | 837 | 1,194 |
| apoA1 | immunoassay/chemistry field | g/L; bounded 0.3–4 | 322 | 785 | 1,114 |
| log(apoB/LDL-C) | apoB and LDL-C | natural logarithm after completion | derived | derived | derived |
| Diabetes | source combined field | 1 yes, 0 no | 424 | 888 | 1,262 |
| log(TG/HDL-C) | triglycerides and HDL-C | natural logarithm | 398 | 786 | 1,116 |
| log Lp(a) | Lp(a) | log(1+Lp(a)); source units | 319 | 672 | 954 |
| Treatment subgroup | source treatment field | recorded yes/no; not a model term | 424 | 890 | 1,264 |

Missing values were replaced by source-training medians. Median estimation, bounding, transformation, scaling, and apoB-on-LDL residualisation occurred inside training folds. Target distributions were not used for source completion.

## 5. Locked candidates and fitting

| Candidate key | Terms |
|---|---|
| `age_sex` | age, male |
| `age_sex_ratio` | age, male, log(apoB/LDL-C) |
| `clinical5` | age, male, HDL-C, hypertension, ever smoking |
| `calon_n_core` | clinical5 plus log(apoB/LDL-C) |
| `calon_n_diabetes` | core plus diabetes |
| `calon_n_tghdl` | core plus log(TG/HDL-C) |
| `calon_n_lpa` | core plus log Lp(a) |
| `calon_n_apoa1` | core plus log apoA1 |
| `calon_n_discordance` | clinical5 plus log LDL-C plus apoB-on-LDL residual |
| `calon_n_parsimonious` | age, male, hypertension, log(apoB/LDL-C) |

Models used L2-penalised logistic regression. The inverse penalty C was chosen from 0.01, 0.03, 0.10, 0.30, 1.00, and 3.00 by the lowest grouped cross-validated Brier score. Families or qualifying-variant components remained intact.

Prespecified positive directions were age, male, hypertension, smoking, diabetes, apoB/LDL-C, TG/HDL-C, Lp(a), LDL-C, and apoB residual discordance. Prespecified negative directions were HDL-C and apoA1. A candidate with any violation in either source was ineligible. The selected architecture maximised the smaller of its two reciprocal-transport AUCs, then mean AUC if tied.

## 6. Full candidate-selection results

| Candidate | Selected C: DRAGON fit | DRAGON→UKB AUC | Selected C: UKB fit | UKB→DRAGON AUC | Minimum | Sign gate |
|---|---:|---:|---:|---:|---:|---|
| age_sex | 1.00 | 0.731861 | 0.10 | 0.894983 | 0.731861 | pass |
| age_sex_ratio | 1.00 | 0.746930 | 0.30 | 0.831937 | 0.746930 | pass |
| clinical5 | 0.30 | 0.745224 | 0.10 | 0.889904 | 0.745224 | pass |
| calon_n_core | 0.30 | 0.756745 | 0.10 | 0.847086 | 0.756745 | pass |
| calon_n_diabetes | 0.30 | 0.760515 | 0.10 | 0.848824 | 0.760515 | pass |
| calon_n_tghdl | 0.30 | 0.755249 | 0.03 | 0.840982 | 0.755249 | fail: DRAGON TG/HDL negative |
| calon_n_lpa | 0.30 | 0.759104 | 0.03 | 0.842408 | 0.759104 | pass |
| **calon_n_apoa1** | **0.30** | **0.767191** | **0.10** | **0.848066** | **0.767191** | **pass; selected** |
| calon_n_discordance | 0.30 | 0.758598 | 0.03 | 0.821868 | 0.758598 | fail: LDL-C negative in both fits |
| calon_n_parsimonious | 0.30 | 0.733283 | 0.10 | 0.832205 | 0.733283 | pass |

All 120 penalty-level Brier/AUC results are retained in `outputs/scratch_source_tuning.csv`. All 20 source equations are retained in `outputs/scratch_candidate_transport.csv`.

## 7. Candidate-specific repeated nested grouped validation

| Cohort | Candidate | Rank-aggregated AUC | Mean repeated AUC±SD |
|---|---|---:|---:|
| DRAGON | age plus sex | 0.885849 | 0.885733±0.002716 |
| DRAGON | clinical five | 0.890572 | 0.888318±0.003528 |
| DRAGON | age plus sex plus ratio | 0.888144 | 0.886705±0.003287 |
| DRAGON | CALON-N | 0.893179 | 0.890866±0.004407 |
| UKB strict | age plus sex | 0.710442 | 0.707428±0.013336 |
| UKB strict | clinical five | 0.750037 | 0.745085±0.008307 |
| UKB strict | age plus sex plus ratio | 0.796424 | 0.791769±0.024551 |
| UKB strict | CALON-N | 0.794339 | 0.788265±0.016145 |

These estimates nest preprocessing and penalty tuning for the named candidate but do not nest the ten-architecture reciprocal selection. They are post-selection descriptive internal estimates.

## 8. Final pooled research equation

The pooled model was fitted after transport and has no untouched validation.

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

| Term | Coefficient | Descriptive odds-ratio translation |
|---|---:|---:|
| Age | +0.112263 | 3.07 per 10 years |
| Male | +0.580373 | 1.79 |
| HDL-C | −0.629887 | 0.53 per mmol/L |
| Hypertension | +0.105120 | 1.11 |
| Ever smoking | +0.143724 | 1.15 |
| log(apoB/LDL-C) | +1.910359 | 3.76 per ratio doubling |
| log(apoA1) | −1.672421 | 0.31 per apoA1 doubling |

These are penalised cross-sectional coefficients without confidence intervals. They are not causal effects.

## 9. Reciprocal transport and comparator results

| Target | CALON-N AUC (95% CI) | Age+sex AUC; paired difference | Montreal AUC; difference | FH-RS AUC; difference | SAFEHEART AUC; difference |
|---|---:|---:|---:|---:|---:|
| UKB strict | 0.767191 (0.711717–0.828183) | 0.731861; +0.035330 (0.017910–0.060460) | 0.774710; −0.007519 (−0.036486–0.007307) | 0.696163; +0.071028 (0.023690–0.110108) | 0.540648; +0.226543 (0.121624–0.293635) |
| DRAGON | 0.848066 (0.795610–0.896255) | 0.894983; −0.046917 (−0.100409–0.002537) | 0.892844; −0.044778 (−0.092665 to −0.002428) | 0.856999; −0.008933 (−0.070539–0.050465) | 0.799724; +0.048342 (−0.030463–0.129810) |
| UKB union | 0.767314 (0.718694–0.812947) | 0.743902; +0.023412 (0.001817–0.045727) | 0.768043; −0.000728 (−0.024659–0.009961) | 0.696311; +0.071003 (0.035794–0.100080) | 0.527743; +0.239571 (0.154266–0.295438) |

Intervals are 4,000-replicate target family/component percentile bootstraps conditional on the fitted source model. They omit source-development and architecture-selection uncertainty.

Comparator caveats: Montreal used source-specific age/HDL anchors; FH-Risk-Score used current rather than uniformly untreated LDL-C and locally available Lp(a); SAFEHEART omitted prior ASCVD and substituted available BMI/smoking inputs. These are adapted implementations.

## 10. Calibration and Brier results

| Transport | Brier | Null Brier | Scaled Brier | Intercept | Slope | E:O |
|---|---:|---:|---:|---:|---:|---:|
| DRAGON→UKB strict | 0.082286 | 0.059923 | −37.3% | −1.446 | 0.951 | 3.004 |
| UKB strict→DRAGON | 0.111459 | 0.124832 | +10.7% | +0.657 | 0.752 | 0.447 |
| DRAGON→UKB union | 0.0828 | 0.0593 | −39.7% | −1.486 | 0.929 | 3.047 |

No target recalibration was performed. Comparative decision analysis is withdrawn because age+sex, Montreal, and FH-Risk-Score outputs were not calibrated probabilities on the same scale.

## 11. Full subgroup stress test

| Cohort | Subgroup | N/cases | Status | CALON-N AUC | Best comparator | Best AUC | Difference |
|---|---|---:|---|---:|---|---:|---:|
| UKB strict | Male | 387/37 | evaluable | 0.707954 | Montreal | 0.715212 | −0.007259 |
| UKB strict | Female | 503/20 | evaluable | 0.784058 | Montreal | 0.779193 | +0.004865 |
| UKB strict | Age below median | 445/8 | non-estimable | — | — | — | — |
| UKB strict | Age at/above median | 445/49 | evaluable | 0.662750 | Montreal | 0.666667 | −0.003917 |
| UKB strict | Treated | 361/54 | evaluable | 0.659488 | Montreal | 0.672216 | −0.012728 |
| UKB strict | Untreated | 529/3 | non-estimable | — | — | — | — |
| UKB strict | Diabetes | 88/14 | descriptive | 0.690154 | Montreal | 0.708494 | −0.018340 |
| UKB strict | No diabetes | 800/43 | evaluable | 0.766582 | Montreal | 0.772879 | −0.006298 |
| UKB strict | Lp(a)≥143 | 57/4 | non-estimable | — | — | — | — |
| UKB strict | Lp(a)<143 | 615/35 | evaluable | 0.739951 | Montreal | 0.750887 | −0.010936 |
| DRAGON | Male | 172/35 | evaluable | 0.844838 | Age+sex | 0.914286 | −0.069447 |
| DRAGON | Female | 252/27 | evaluable | 0.842469 | Montreal | 0.894156 | −0.051687 |
| DRAGON | Age below median | 212/0 | non-estimable | — | — | — | — |
| DRAGON | Age at/above median | 212/62 | evaluable | 0.717742 | Age+sex | 0.752151 | −0.034409 |
| DRAGON | Treated | 367/61 | evaluable | 0.836923 | Age+sex | 0.888782 | −0.051859 |
| DRAGON | Untreated | 57/1 | non-estimable | — | — | — | — |
| DRAGON | Diabetes | 21/9 | non-estimable | — | — | — | — |
| DRAGON | No diabetes | 403/53 | evaluable | 0.842372 | Age+sex | 0.895795 | −0.053423 |
| DRAGON | Lp(a)≥143 | 85/22 | evaluable | 0.869408 | Montreal | 0.871573 | −0.002165 |
| DRAGON | Lp(a)<143 | 234/26 | evaluable | 0.877404 | Age+sex | 0.908839 | −0.031435 |

Six rows were non-estimable, leaving 14 evaluable/descriptive rows. CALON-N exceeded the best comparator in one and did not do so in 13. No subgroup confidence interval or interaction test was estimated.

## 12. Sensitivity results

| Sensitivity | N/cases | CALON-N AUC | Interpretation |
|---|---:|---:|---|
| UKB P/LP-or-LoF union | 1,264/80 | 0.767314 | Primary discrimination unchanged |
| Archived exact-HGVS LDLR P/LP DRAGON | 164/20 | 0.826736 | Smaller conservative subset; imprecise |
| DRAGON component-union outcome | 424/66 | 0.847257 | Stable to broader visible component union |
| DRAGON hard-coronary outcome | 424/56 | 0.842877 | Stable to hard-coronary definition |
| DRAGON→UKB complete cases | 726/50 | 0.752959 | Lower than completed-data transport |
| UKB→DRAGON complete cases | 304/45 | 0.891034 | Higher in selected complete clinic subset |

## 13. QC and confidence

### Reproduced computational checks

- Seven canonical raw-input SHA-256 hashes matched the lock.
- Cohort counts, event counts, and cluster counts reproduced exactly.
- The maximin/sign gate reselected `calon_n_apoa1`.
- Every comparator difference equalled CALON-N AUC minus comparator AUC.
- The stored feature list and equation matched.
- Repeated and row-reversed synthetic scoring differed by 0.0.
- No participant-level result, identifier, family label, or variant coordinate was written.
- Phase A and Phase B selection files are now unambiguously named and documented.

### Claim confidence

| Claim | Confidence | Basis |
|---|---|---|
| Counts, linkage, deterministic scoring | High | Exact independent rerun and hash checks |
| Selection under the declared algorithm | High | Exact re-selection from ten candidates |
| Conditional AUCs in these datasets | Moderate | Cluster-aware intervals; only 57/62 cases |
| Superiority to age+sex in UKB | Moderate within these data | Conditional paired interval above zero; selection target-informed |
| Superiority to adapted FH-RS/SAFEHEART in UKB | Low–moderate | Intervals above zero; comparator adaptations substantial |
| Equivalence to Montreal | Not established | Non-significance is not equivalence |
| Subgroup superiority | None | One of 14 rows wins; no interaction tests |
| Absolute-risk accuracy/clinical utility | None | E:O 3.00 and 0.45; DCA withdrawn |
| Prospective risk prediction | None | Cross-sectional outcome and post-event biomarkers |
| Generalisation to a third registry | Low | No untouched validation cohort |

Overall PROBAST judgement is high risk of bias and high applicability concern for prospective prediction or clinical use. TRIPOD+AI and STROBE item-level mappings are provided separately; remaining hard blockers are the exact Welsh approval/governance reference, confirmed patient/public-involvement statement, upstream genomic/ClinVar release metadata, and full laboratory/outcome-adjudication metadata.

## 14. Reproducibility map

| Purpose | Canonical artefact |
|---|---|
| Protocol and Phase B amendment | `PROTOCOL_LOCK.md` |
| Phase map | `outputs/README.md` |
| Cohort counts | `outputs/cohort_audit.json` |
| Candidate selection | `outputs/scratch_selection.json` |
| All candidate source equations/transport | `outputs/scratch_candidate_transport.csv` |
| All penalty results | `outputs/scratch_source_tuning.csv` |
| Internal grouped results | `outputs/scratch_nested_grouped_internal.csv` |
| Primary AUCs/deltas/calibration | `outputs/scratch_external_performance.json` |
| Union result | `outputs/scratch_union_sensitivity.json` |
| All subgroup rows | `outputs/scratch_subgroups.csv` |
| Sensitivities | `outputs/scratch_sensitivity_qc.json` |
| Pooled equation | `model/calon_n_equation.json` |
| Deterministic model | `model/calon_n_from_scratch.joblib` |
| Consolidated independent QC | `qc/CONSOLIDATED_QC_2026_08_09.md` |
| Package checksums | `MANIFEST.json` |
