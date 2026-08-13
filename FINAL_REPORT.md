# CALON-N final report

## Bottom line

A genuinely new model was built from raw variables only. The result is CALON-N:

`age + sex + HDL-C + hypertension + smoking + log(apoB/LDL-C) + log(apoA1)`

It is the highest **sign-coherent from-scratch** architecture under the locked
maximin reciprocal-transport rule. It is not the highest unconstrained model:
models using a negative LDL coefficient scored slightly higher in UK Biobank
and were rejected as treatment/reverse-causation signatures.

CALON-N reached AUC 0.767 in strict UK Biobank and 0.848 in reverse transport to
DRAGON. It beat adapted FH-Risk-Score and SAFEHEART in UK Biobank, but it did not
beat Montreal there and lost to Montreal and age+sex in DRAGON. Calibration
failed in both directions. The requested claim—best in every direction and
subgroup—is therefore false in these data.

## What is new

- no published score is embedded in the architecture;
- simultaneous particle-cholesterol discordance and apoA1 protection terms;
- family- and qualifying-variant-component-aware reciprocal transport;
- sign-coherence gate that rejected higher-AUC negative-LDL models;
- an explicit analysis of why clinical and population carrier settings yield
  different rankings.

## Primary performance

| Target | CALON-N | Age+sex | Montreal | FH-RS | SAFEHEART |
|---|---:|---:|---:|---:|---:|
| UKB strict (890/57) | **0.767** | 0.732 | **0.775** | 0.696 | 0.541 |
| DRAGON (424/62) | **0.848** | **0.895** | **0.893** | 0.857 | 0.800 |
| UKB union (1,264/80) | **0.767** | 0.745 | **0.768** | 0.697 | 0.527 |

The model is close to Montreal in UK Biobank and below it in DRAGON. That is a
scientifically useful transport result, not universal superiority.

## Why it cannot be a 10-year model

DRAGON laboratory phenotypes commonly post-date established disease and
treatment. The analysis outcome is prevalent/established ASCVD. Re-labelling
the output as 10-year incidence would introduce reverse causation and temporal
leakage. The pooled probability is a cross-sectional research score only.

## Relation to the separate Welsh ascertainment idea

Updating FH-Risk-Score with proband/cascade-specific baseline hazards is a
promising **separate prospective model-updating project**. It can borrow stable
published coefficients and address an absolute-risk calibration gap. It is not
de novo and is not part of CALON-N. Its reported 90% reduction in E:O error must
be re-estimated with family-disjoint out-of-fold baselines, censoring and
competing death, shrinkage, ordinary-intercept recalibration as a comparator,
and external registry validation.

## Release verdict

- Reproducibility package: **PASS** after final hashes/QC.
- Scientific manuscript: **exploratory, submission-draft ready after authors,
  ethics, funding, and endpoint adjudication details are completed**.
- Prospective risk claim: **FAIL**.
- Universal-superiority claim: **FAIL**.
- Clinical deployment: **FAIL**.

