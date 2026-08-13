# CALON-N consolidated rerun and scientific QC — 9 August 2026

## Executive verdict

The computational analysis reproduces, the selected architecture obeys its
locked rule, and the frozen scorer is deterministic. The model is scientifically
credible only as an exploratory cross-sectional classifier of already-recorded
ASCVD. It is not a prospective risk equation, does not have protected external
validation, does not transport absolute probabilities, and does not beat all
comparators or subgroups.

A new material QC finding was identified: the original decision-curve table
applied probability thresholds to age+sex, Montreal, and FH-Risk-Score ranking
scores/linear predictors. Those outputs were not calibrated probabilities on a
common scale. All comparative net-benefit claims are therefore invalid and have
been withdrawn from the manuscript.

## Rerun and provenance

Commands rerun successfully:

```bash
python3 code/02_from_scratch_model.py
python3 code/03_sensitivity_qc.py
python3 code/06_consolidated_qc.py
```

- All seven canonical raw-input SHA-256 hashes matched the lock.
- Cohort reconstruction matched the frozen counts.
- The maximin/sign-coherence selection rule independently reselected
  `calon_n_apoa1`.
- Every reported comparator delta equalled CALON-N AUC minus comparator AUC.
- The stored model and equation used the same features.
- Repeated and row-reversed synthetic scoring differed by 0.0.
- No prohibited UK Biobank hypertension first-occurrence field code was found.
- No participant-level output or identifier-bearing output filename was found.

Machine-readable audit: `outputs/consolidated_qc_2026_08_09.json`.

## Estimand and cohorts

The estimand is the probability that established ASCVD was already recorded at
the time represented by the available contemporary phenotype. It is not the
probability of a future event over five or ten years.

| Cohort | N | ASCVD cases | Prevalence | Resampling unit |
|---|---:|---:|---:|---|
| DRAGON | 424 | 62 | 14.62% | 219 canonical families |
| UKB strict local LDLR P/LP | 890 | 57 | 6.40% | 62 qualifying-variant connected components |
| UKB P/LP-or-LoF sensitivity | 1,264 | 80 | 6.33% | 66 qualifying-variant connected components |

DRAGON linkage retained 424/424 participants, including 412 direct family
agreements and 12 family realignments through the PASS family identifier.

## Variables in the final model

CALON-N contains seven model terms derived from eight raw measurements:

| Model term | Raw input and coding | Pooled coefficient | Descriptive interpretation only |
|---|---|---:|---|
| Age | years | +0.112263 | OR 3.07 per 10 years |
| Male | 1=yes, 0=no | +0.580373 | OR 1.79 |
| HDL-C | mmol/L | −0.629887 | OR 0.53 per mmol/L |
| Hypertension | 1=yes, 0=no | +0.105120 | OR 1.11 |
| Ever smoking | 1=yes, 0=no | +0.143724 | OR 1.15 |
| log(apoB/LDL-C) | apoB g/L divided by LDL-C mmol/L, then natural log | +1.910359 | OR 3.76 per doubling of the ratio |
| log(apoA1) | apoA1 g/L, natural log | −1.672421 | OR 0.31 per doubling of apoA1 |

These are penalised pooled-model coefficients, not causal effects, and no
coefficient confidence intervals were estimated. The odds-ratio translations
must not be used as biological effect estimates.

```text
logit(p) = -5.673054
           + 0.112263*age
           + 0.580373*male
           - 0.629887*HDL-C
           + 0.105120*hypertension
           + 0.143724*ever_smoker
           + 1.910359*log(apoB/LDL-C)
           - 1.672421*log(apoA1)
```

### Coverage of required raw variables

| Variable | DRAGON observed | UKB strict observed | UKB union observed |
|---|---:|---:|---:|
| Age | 424/424 | 890/890 | 1,264/1,264 |
| Male | 424/424 | 890/890 | 1,264/1,264 |
| HDL-C | 398/424 | 786/890 | 1,116/1,264 |
| Hypertension | 424/424 | 840/890 | 1,176/1,264 |
| Ever smoking | 424/424 | 890/890 | 1,264/1,264 |
| LDL-C | 402/424 | 850/890 | 1,208/1,264 |
| apoB | 323/424 | 837/890 | 1,194/1,264 |
| apoA1 | 322/424 | 785/890 | 1,114/1,264 |

Source-fold medians were used for missing values. This avoids direct target
distribution leakage but does not model missing-data uncertainty and assumes
transportability of the source median.

## Selection results

Ten raw-variable architectures were compared in both transport directions. The
locked choice was the sign-coherent candidate with the highest minimum AUC
across directions.

| Candidate | DRAGON→UKB | UKB→DRAGON | Minimum | Sign coherent in both? |
|---|---:|---:|---:|:---:|
| CALON-N + apoA1 | 0.7672 | 0.8481 | **0.7672** | yes |
| CALON-N + diabetes | 0.7605 | 0.8488 | 0.7605 | yes |
| CALON-N + Lp(a) | 0.7591 | 0.8424 | 0.7591 | yes |
| Residual-discordance form | 0.7586 | 0.8219 | 0.7586 | no: negative LDL-C |
| CALON-N core | 0.7567 | 0.8471 | 0.7567 | yes |
| CALON-N + TG/HDL | 0.7552 | 0.8410 | 0.7552 | no in one source |
| Age+sex+ratio | 0.7469 | 0.8319 | 0.7469 | yes |
| Clinical five-variable model | 0.7452 | 0.8899 | 0.7452 | yes |
| Parsimonious model | 0.7333 | 0.8322 | 0.7333 | yes |
| Age+sex | 0.7319 | 0.8950 | 0.7319 | yes |

The selection arithmetic is correct. It is nevertheless target-informed: both
cohort outcomes were used to choose the architecture. This is reciprocal
multi-cohort development, not protected external validation.

## Discrimination

### DRAGON-fitted model evaluated in strict UK Biobank

| Model | AUC | CALON-N difference (95% cluster-bootstrap CI) |
|---|---:|---:|
| CALON-N | **0.7672** (0.7117–0.8282) | reference |
| Age+sex | 0.7319 | +0.0353 (0.0179–0.0605) |
| Montreal adapted | **0.7747** | −0.0075 (−0.0365–0.0073) |
| FH-Risk-Score adapted | 0.6962 | +0.0710 (0.0237–0.1101) |
| SAFEHEART adapted | 0.5406 | +0.2265 (0.1216–0.2936) |

CALON-N ranks cases better than age+sex and the adapted FH-Risk-Score and
SAFEHEART implementations in this target. It is not statistically separable
from Montreal and its point estimate is lower.

### UK Biobank-fitted model evaluated in DRAGON

| Model | AUC | CALON-N difference (95% family-bootstrap CI) |
|---|---:|---:|
| CALON-N | **0.8481** (0.7956–0.8963) | reference |
| Age+sex | **0.8950** | −0.0469 (−0.1004–0.0025) |
| Montreal adapted | **0.8928** | −0.0448 (−0.0927 to −0.0024) |
| FH-Risk-Score adapted | 0.8570 | −0.0089 (−0.0705–0.0505) |
| SAFEHEART adapted | 0.7997 | +0.0483 (−0.0305–0.1298) |

Montreal is significantly higher on the conditional family bootstrap. Age+sex
is also higher by point estimate, although its interval includes zero.

### UK Biobank union sensitivity

CALON-N AUC was 0.7673 (0.7187–0.8129), almost identical to Montreal 0.7680
(difference −0.0007, −0.0247–0.0100), and above the adapted FH-Risk-Score and
SAFEHEART implementations.

## Internal grouped validation

Candidate-specific repeated nested grouped AUCs were 0.8932 in DRAGON and
0.7943 in strict UK Biobank. These values correctly nest preprocessing and
penalty tuning for that candidate, but they do not nest the ten-candidate
cross-cohort architecture choice. They are consequently expected to be
optimistic for the whole development process.

## Calibration and overall accuracy

| Transport | Brier | Null Brier | Scaled Brier | Intercept | Slope | E:O |
|---|---:|---:|---:|---:|---:|---:|
| DRAGON→UKB strict | 0.0823 | 0.0599 | **−37.3%** | −1.446 | 0.951 | **3.004** |
| UKB strict→DRAGON | 0.1115 | 0.1248 | +10.7% | +0.657 | 0.752 | **0.447** |
| DRAGON→UKB union | 0.0828 | 0.0593 | **−39.7%** | −1.486 | 0.929 | **3.047** |

The ranking signal transports better than the absolute probability. In UK
Biobank, the model predicts approximately three times the observed number of
cases and performs worse on Brier score than a constant-prevalence prediction.
In DRAGON it underpredicts by more than half. Absolute-risk use fails.

Comparative decision-curve analysis is withdrawn because comparator scores
were not calibrated probabilities. No treatment or referral threshold is
supported.

## Sensitivities

- Archived exact-HGVS LDLR P/LP DRAGON subset: 164 participants/20 cases,
  UKB-fitted AUC 0.8267. This is small and misses unparseable/absent variants.
- DRAGON component-union outcome: 66 cases, AUC 0.8473.
- DRAGON hard-coronary outcome: 56 cases, AUC 0.8429.
- Complete-case DRAGON→UKB: 726/50, AUC 0.7530.
- Complete-case UKB→DRAGON: 304/45, AUC 0.8910.

The outcome-definition sensitivities are stable. The large complete-case shift
in reverse transport shows that missingness and assay availability materially
affect performance.

## Subgroups

Twenty subgroup rows were attempted. Six had fewer than ten cases and were
non-estimable. Of 14 estimable/descriptive rows, CALON-N exceeded the best
comparator in one (UKB women, +0.0049) and was at or below the best comparator
in 13. DRAGON had zero subgroup wins. No subgroup confidence intervals or
interaction tests were estimated. These analyses cannot support effect
modification or fairness claims.

## Confidence assessment

| Claim | Confidence | Reason |
|---|---|---|
| Cohort counts/linkage and deterministic scoring | High | Independently rerun; hashes and exact counts match |
| Selected architecture under the stated algorithm | High | Maximin/sign rule independently reproduced |
| Conditional AUCs in these two datasets | Moderate | Cluster-aware intervals, but only 57/62 cases |
| Superiority to age+sex in UKB | Moderate within this dataset | Conditional delta CI excludes zero, but target-informed selection |
| Superiority to adapted FH-RS/SAFEHEART in UKB | Low–moderate | Intervals exclude zero, but comparator and estimand adaptations are substantial |
| Equivalence to Montreal | Low | A non-significant difference is not proof of equivalence |
| Subgroup superiority | Very low/none | One of 14 rows wins; sparse cases; no interaction tests |
| Absolute-risk calibration or clinical utility | None | E:O 3.00/0.45; invalid comparative DCA |
| Prospective 5- or 10-year prediction | None | Predictors can follow disease/treatment; prevalent outcome |
| Generalisation to a new registry | Low | No untouched third-cohort validation |

## Bias assessment

1. **Reverse causation/temporal leakage:** apoB, LDL-C, HDL-C, apoA1,
   hypertension and smoking status may be recorded after ASCVD and treatment.
2. **Target-informed selection:** both outcomes helped choose among ten models;
   transport is not independent validation.
3. **Sparse-event optimism:** only 57 and 62 primary cases support seven terms,
   tuning, candidate selection and subgroup exploration.
4. **Multiplicity:** ten architectures, two directions and twenty subgroup rows
   were examined without whole-process multiplicity adjustment.
5. **Missing-data bias:** median completion ignores imputation uncertainty;
   apoA1 is missing in 24.1% of DRAGON and 11.8% of strict UKB.
6. **Spectrum/ascertainment bias:** specialist-clinic DRAGON and population UKB
   differ in age, treatment, disease prevalence and referral mechanisms.
7. **Survivor/prevalence bias:** only living, measured participants with
   established disease are represented; fatal early events may be absent.
8. **Outcome misclassification:** registry and UKB endpoint components/timing
   are not centrally adjudicated or perfectly harmonised.
9. **Genetic-definition mismatch:** UKB primary carriers are local LDLR P/LP;
   DRAGON includes a broader genetically confirmed clinic population. Local
   ClinVar review-status enforcement is unavailable.
10. **Comparator bias:** Montreal, FH-Risk-Score and SAFEHEART are adapted; the
    current cross-sectional endpoint, current/treated lipids and missing inputs
    differ from their intended implementations.
11. **Calibration transport bias:** case prevalence and baseline odds differ;
    the pooled and source-specific intercepts cannot be assumed portable.
12. **Coefficient instability/collinearity:** HDL-C and apoA1 overlap
    biologically and statistically; ridge shrinkage reduces but does not remove
    uncertainty.
13. **Limited population diversity:** predominantly White-European settings;
    ancestry and socioeconomic fairness were not evaluated.
14. **Reporting/governance gaps:** exact approvals, recruitment dates,
    laboratory platforms, outcome adjudication, funding, conflicts and patient
    involvement remain incomplete.

## Novelty appraisal

The biology of apoB/LDL-C discordance in this DRAGON cohort is not new: Genedy
and Zouwail reported a hypothesis-generating analysis of the same 424-person
Welsh cohort in 2026. Published FH tools also already use conventional age,
sex, HDL-C, hypertension, smoking, LDL-C and Lp(a) predictors.

The defensible novelty is therefore methodological and incremental:

- a genuinely de novo raw-variable equation with no published score as an input;
- the simultaneous use of log(apoB/LDL-C) and a protective log(apoA1) term;
- reciprocal transport between family-clustered specialist FH and
  qualifying-variant-clustered UK Biobank carriers;
- a locked sign-coherence gate that rejects better-looking but physiologically
  incoherent negative-LDL candidates;
- a documented negative result showing that discrimination, calibration and
  subgroup ranking do not transport in the same way.

Safe wording: **“We developed an exploratory de novo apoB-discordance classifier
and evaluated reciprocal transport across two genetically defined FH settings.”**
Do not claim the first apoB/LDL-C model, the first FH risk score, a new causal
mechanism, or a universally superior tool.

## TRIPOD+AI audit

The revised local granular mapping contains 40 rows: 30 addressed, 7 partial
and 3 not addressed. These counts are a gap profile, not a validated compliance
score.

### Addressed

Title/abstract, clinical context, estimand/intended non-use, settings, outcome
and predictor definitions, missingness and fold-local completion, candidate
set, tuning, family/variant grouping, candidate-specific internal validation,
AUC/calibration/Brier reporting, conditional paired intervals, calibration
plot, subgroup stopping rules, equation/scorer, synthetic example, no target
recalibration, limitations, protocol, code/model and data-governance statement,
and AI-use disclosure.

### Partial

- Exact DRAGON dates/recruitment windows and some upstream release metadata.
- Original outcome-adjudication details.
- Formal sample-size justification.
- Reciprocal transport is target-informed, not protected validation.
- Fairness/effect-modification inference is descriptive and incomplete.
- Adapted rather than exact comparator implementations.
- Welsh governance and patient/public-involvement confirmation remain author
  completion items.

### Not addressed / failed

- Predictor availability before the prediction time for prospective use.
- Source-development and architecture-selection uncertainty in intervals.
- Valid comparative decision-curve analysis.

## STROBE cross-sectional audit

STROBE itself contains 22 official numbered items; the local mapping expands
statistical item 12 into four rows and therefore has 25 rows: 20 addressed and
5 partial. STROBE is a reporting checklist, not a risk-of-bias score.

### Addressed

Design, rationale, objectives, variable definitions, quantitative handling,
statistical methods, missingness, descriptive and outcome data, main and
sensitivity results, balanced interpretation, limitations and
generalisability.

### Partial

- Exact dates and recruitment setting details.
- Original clinic referral/invitation pathway.
- Laboratory platforms and outcome adjudication details.
- Formal study-size calculation.
- Interaction inference for subgroups was not performed.

## PROBAST conclusion

Overall risk of bias is **HIGH**, with **HIGH applicability concern** for
prospective risk prediction or clinical deployment. Participant selection,
post-event predictors, outcome harmonisation and target-informed analysis all
contribute. Group-aware validation and deterministic scoring are genuine
strengths, but they cannot convert this into low-risk external validation.

## Required next study

Freeze CALON-N before accessing a third cohort; require pre-event apoB, LDL-C,
apoA1 and routine predictors; use adjudicated incident ASCVD with competing
death; keep families/variants intact; use multiple imputation and full-pipeline
cluster bootstrap; report time-specific calibration and valid decision curves
only after every model has been placed on the same absolute-risk scale.
