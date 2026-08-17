# CALON-N final report

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

## Relation to the separate Welsh ascertainment idea — WITHDRAWN

An earlier version of this report described updating FH-Risk-Score with
proband/cascade-specific baseline hazards as a promising separate project. That
idea is **withdrawn**, for two reasons.

First, it is disallowed by the programme's binding rule: no published score, no
prior model from this programme, and no linear predictor derived from either may
enter a new model as a feature. Published scores are comparators, never inputs.

Second, its premise has since been falsified by measurement. The idea rested on
the claim that borrowing published relative effects would beat re-estimating a
model from a small number of events. A model estimated from raw variables alone
(CALON-F) subsequently tied FH-Risk-Score in Wales (+0.002) and beat it in UK
Biobank by +0.031 with a confidence interval excluding zero.

The accompanying claim of a 90% reduction in E:O error was never established.
Fitting a free intercept per ascertainment stratum forces the observed/expected
ratio towards one within that stratum by construction, so a calibration gain
measured that way is arithmetic rather than evidence.

## Release verdict

- Reproducibility package: **PASS** after final hashes/QC.
- Scientific manuscript: **exploratory, submission-draft ready after authors,
  ethics, funding, and endpoint adjudication details are completed**.
- Prospective risk claim: **FAIL**.
- Universal-superiority claim: **FAIL**.
- Clinical deployment: **FAIL**.

