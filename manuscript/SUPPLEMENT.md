# Online supplement: CALON-N

## Supplementary Methods 0. Analysis phases, dates, and participant flow

Phase A tested score augmentation and selected `montreal_ratio`; it is retained
only as a diagnostic and is now labelled `phase_a_score_augmentation`. Phase B
is the de novo analysis governed by Protocol Amendment 1. Its canonical record
is `outputs/scratch_selection.json`, which selects `calon_n_apoa1` from the ten
raw-variable candidates in Supplementary Methods 1. Published scores were never
Phase B model inputs.

The DRAGON file was obtained locally on 2 August 2026 and the analysis was
locked on 9 August 2026. A validated upstream DRAGON recruitment/data-cut was
not preserved. UK Biobank strict-carrier baseline dates ranged from 19 April
2007 to 22 September 2010. The local call file was dated 19 March 2026 and the
ClinVar/VEP exports 8 June 2026; upstream release identifiers were unavailable.

| Flow stage | DRAGON | UKB strict LDLR P/LP | UKB P/LP-or-LoF |
|---|---:|---:|---:|
| Source | 424 exported participants | 6,597,041 call rows/468,965 participants | same call source |
| Qualifying participants | 424 clinic records | 890 local P/LP | 1,264 P/LP-or-LoF |
| Linked and analysed | 424 | 890 | 1,264 |
| ASCVD cases | 62 | 57 | 80 |
| Family/variant components | 219 | 62 | 66 |

All 424 DRAGON records linked to PASS: 412 family labels agreed directly and 12
were realigned. No participant was excluded because of predictor missingness;
completion occurred inside the source-training pipeline.

## Supplementary Methods 1. Locked candidate set

All phase-B candidates were fitted from raw variables. Montreal-FH-SCORE,
FH-Risk-Score, and SAFEHEART were comparators only and were prohibited as model
inputs. Ridge penalty selection was based on grouped cross-validated Brier
score. Candidate selection used the highest lower reciprocal-transport AUC
after sign coherence in both source fits.

| Candidate | Raw model terms |
|---|---|
| age_sex | age, male |
| age_sex_ratio | age, male, log(apoB/LDL-C) |
| clinical5 | age, male, HDL-C, hypertension, smoking |
| calon_n_core | clinical5 + log(apoB/LDL-C) |
| calon_n_diabetes | CALON-N core + diabetes |
| calon_n_tghdl | CALON-N core + log(TG/HDL-C) |
| calon_n_lpa | CALON-N core + log Lp(a) |
| calon_n_apoa1 | CALON-N core + log apoA1 |
| calon_n_discordance | clinical5 + log LDL-C + apoB-on-LDL residual |
| calon_n_parsimonious | age, male, hypertension, log(apoB/LDL-C) |

## Supplementary Table S1. Cohort characteristics

Values are mean±SD, n (%), or median [Q1, Q3]. Percentages for partially
observed variables use all cohort members as the denominator and therefore
must be interpreted with the coverage row.

| Characteristic | DRAGON | UKB strict LDLR P/LP | UKB P/LP-or-LoF |
|---|---:|---:|---:|
| N | 424 | 890 | 1,264 |
| Established ASCVD | 62 (14.6%) | 57 (6.4%) | 80 (6.3%) |
| Family/variant components | 219 | 62 | 66 |
| Age, years | 48.4±18.6 | 57.3±8.0 | 57.0±8.1 |
| Male | 172 (40.6%) | 387 (43.5%) | 559 (44.2%) |
| Hypertension | 77 (18.2%) | 386 (43.4%; 840 observed) | 562 (44.5%; 1,176 observed) |
| Ever smoking | 98 (23.1%) | 428 (48.1%) | 612 (48.4%) |
| Diabetes | 21 (5.0%) | 88 (9.9%; 888 observed) | 126 (10.0%; 1,262 observed) |
| Recorded treatment | 367 (86.6%) | 361 (40.6%) | 458 (36.2%) |
| LDL-C, mmol/L | 4.70 [3.50, 6.00]; n=402 | 3.86 [3.12, 4.66]; n=850 | 3.76 [3.06, 4.52]; n=1,208 |
| HDL-C, mmol/L | 1.30 [1.10, 1.50]; n=398 | 1.42 [1.17, 1.66]; n=786 | 1.40 [1.16, 1.66]; n=1,116 |
| apoB, g/L | 1.28 [1.03, 1.57]; n=323 | 1.12 [0.94, 1.32]; n=837 | 1.09 [0.92, 1.29]; n=1,194 |
| apoA1, g/L | 1.44 [1.25, 1.64]; n=322 | 1.51 [1.34, 1.67]; n=785 | 1.50 [1.33, 1.66]; n=1,114 |
| Lp(a), source units | 45.0 [18.0, 154.0]; n=319 | 26.2 [10.6, 68.0]; n=672 | 24.9 [10.6, 66.3]; n=954 |

## Supplementary Table S2. Locked candidate reciprocal transport

| Candidate | DRAGON→UKB strict AUC | UKB strict→DRAGON AUC | Minimum | Sign gate |
|---|---:|---:|---:|---|
| age_sex | 0.7319 | 0.8950 | 0.7319 | pass |
| age_sex_ratio | 0.7469 | 0.8319 | 0.7469 | pass |
| clinical5 | 0.7452 | 0.8899 | 0.7452 | pass |
| calon_n_core | 0.7567 | 0.8471 | 0.7567 | pass |
| calon_n_diabetes | 0.7605 | 0.8488 | 0.7605 | pass |
| calon_n_tghdl | 0.7552 | 0.8410 | 0.7552 | fail in DRAGON source (TG/HDL negative) |
| calon_n_lpa | 0.7591 | 0.8424 | 0.7591 | pass |
| **calon_n_apoa1** | **0.7672** | **0.8481** | **0.7672** | **pass; selected** |
| calon_n_discordance | 0.7586 | 0.8219 | 0.7586 | fail in both sources (LDL negative) |
| calon_n_parsimonious | 0.7333 | 0.8322 | 0.7333 | pass |

The source equations and all penalty-level tuning results are retained in
`outputs/scratch_candidate_transport.csv` and
`outputs/scratch_source_tuning.csv`.

## Supplementary Table S3. Candidate-specific repeated nested grouped validation

| Cohort | Candidate | Rank-aggregated AUC | Mean repeat AUC±SD |
|---|---|---:|---:|
| DRAGON | age + sex | 0.8858 | 0.8857±0.0027 |
| DRAGON | clinical5 | 0.8906 | 0.8883±0.0035 |
| DRAGON | age + sex + ratio | 0.8881 | 0.8867±0.0033 |
| DRAGON | CALON-N | 0.8932 | 0.8909±0.0044 |
| UKB strict | age + sex | 0.7104 | 0.7074±0.0133 |
| UKB strict | clinical5 | 0.7500 | 0.7451±0.0083 |
| UKB strict | age + sex + ratio | 0.7964 | 0.7918±0.0246 |
| UKB strict | CALON-N | 0.7943 | 0.7883±0.0161 |

These are candidate-specific nested estimates: preprocessing and penalty tuning
were nested, but the final architecture was chosen using reciprocal target AUCs.
They must not be described as optimism-free validation of the selection process.

## Supplementary Table S4. Reciprocal transport and paired comparisons

| Target | Model AUC (95% CI) | vs age+sex | vs Montreal | vs FH-RS | vs SAFEHEART |
|---|---:|---:|---:|---:|---:|
| UKB strict | 0.767 (0.712–0.828) | +0.035 (+0.018,+0.060) | −0.008 (−0.036,+0.007) | +0.071 (+0.024,+0.110) | +0.227 (+0.122,+0.294) |
| DRAGON | 0.848 (0.796–0.896) | −0.047 (−0.100,+0.003) | −0.045 (−0.093,−0.002) | −0.009 (−0.071,+0.050) | +0.048 (−0.030,+0.130) |
| UKB union | 0.767 (0.719–0.813) | +0.023 (+0.002,+0.046) | −0.001 (−0.025,+0.010) | +0.071 (+0.036,+0.100) | +0.240 (+0.154,+0.295) |

Intervals are conditional target-cluster bootstraps and do not incorporate
source-model development uncertainty.

## Supplementary Table S5. Calibration

| Transport | Brier | Intercept | Slope | E:O |
|---|---:|---:|---:|---:|
| DRAGON→UKB strict | 0.0823 | −1.446 | 0.951 | 3.004 |
| UKB strict→DRAGON | 0.1115 | +0.657 | 0.752 | 0.447 |
| DRAGON→UKB union | 0.0828 | −1.486 | 0.929 | 3.047 |

No target recalibration was performed.

## Supplementary Table S6. Subgroup stress test

The comparator shown is the highest AUC among age+sex, Montreal, adapted FH-RS,
and adapted SAFEHEART. No interaction tests were performed; rows are descriptive.

| Cohort | Subgroup | N/cases | CALON-N AUC | Best comparator AUC | Difference | Status |
|---|---|---:|---:|---:|---:|---|
| UKB strict | male | 387/37 | 0.708 | 0.715 | −0.007 | evaluable |
| UKB strict | female | 503/20 | 0.784 | 0.779 | +0.005 | evaluable |
| UKB strict | age ≥median | 445/49 | 0.663 | 0.667 | −0.004 | evaluable |
| UKB strict | treated | 361/54 | 0.659 | 0.672 | −0.013 | evaluable |
| UKB strict | diabetes | 88/14 | 0.690 | 0.708 | −0.018 | descriptive |
| UKB strict | no diabetes | 800/43 | 0.767 | 0.773 | −0.006 | evaluable |
| UKB strict | Lp(a)<143 | 615/35 | 0.740 | 0.751 | −0.011 | evaluable |
| DRAGON | male | 172/35 | 0.845 | 0.914 | −0.069 | evaluable |
| DRAGON | female | 252/27 | 0.842 | 0.894 | −0.052 | evaluable |
| DRAGON | age ≥median | 212/62 | 0.718 | 0.752 | −0.034 | evaluable |
| DRAGON | treated | 367/61 | 0.837 | 0.889 | −0.052 | evaluable |
| DRAGON | no diabetes | 403/53 | 0.842 | 0.896 | −0.053 | evaluable |
| DRAGON | Lp(a)≥143 | 85/22 | 0.869 | 0.872 | −0.002 | evaluable |
| DRAGON | Lp(a)<143 | 234/26 | 0.877 | 0.909 | −0.031 | evaluable |

Younger, untreated, diabetic, and/or high-Lp(a) strata omitted from the table
had fewer than 10 cases and were classified non-estimable. Exact counts remain
in `outputs/scratch_subgroups.csv`.

## Supplementary Methods 2. Complete-case and outcome sensitivities

- UKB strict complete-case transport: 726 participants, 50 cases, AUC 0.753.
- DRAGON complete-case reverse transport: 304 participants, 45 cases, AUC 0.891.
- Conservative archived exact-HGVS LDLR P/LP DRAGON sensitivity: 164/20,
  UKB-fitted AUC 0.827.
- DRAGON component-union endpoint: 66 cases, AUC 0.847.
- DRAGON hard-coronary endpoint: 56 cases, AUC 0.843.

## Supplementary Note. UK Biobank exposure hierarchy

1. **Primary model cohort:** coordinate-verified local LDLR P/LP, n=890.
2. **Sensitivity:** local LDLR P/LP-or-predicted-LoF, n=1,264.
3. **Published-variant concordance controls:** exact Patel/Fahed LDLR variants;
   useful for verifying columns and lipid phenotypes, not substitutes for the
   current cohort.
4. **Exploratory only:** three-gene TUDOR label, because APOB/PCSK9 records lack
   participant-level variant coordinates/pathogenicity provenance and have only
   16.6% overlap with strict local LDLR P/LP.

The TUDOR prevalence denominator is 426,731 participants with an exposure
record, not the 501,936-person master. The all-gene label is 1,622/426,731
(0.3801%); within the genetic White-British TUDOR subset it is
1,212/355,225 (0.3412%). These cohort-cleaning results do not alter CALON-N,
which uses the coordinate-verified LDLR cohort.
