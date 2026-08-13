# CALON-DISC protocol lock

Locked before the new candidate analysis was run: 2026-08-09.

## Scientific question and estimand

Among people with genetically defined familial hypercholesterolaemia in two
retrospective cohorts, estimate the probability that established ASCVD is
already recorded at the time of the available contemporary lipid and
apolipoprotein phenotype.

This is a cross-sectional **case-identification** estimand. It is not incident
risk, a 10-year prediction, a causal effect of apoB or LDL-C, or a treatment
decision rule. Contemporary lipids may have been measured after ASCVD and after
lipid-lowering treatment.

## Cohorts

- DRAGON specialist-clinic cohort: 424 participants, 62 registry ASCVD cases,
  clustered by 219 canonical PASS-linked families. DRAGON is the primary
  clinical cohort.
- UK Biobank primary transport cohort: coordinate-linked LDLR carriers with a
  local ClinVar P/LP classification, 890 participants and 57 prevalent ASCVD
  cases, clustered by connected components induced only by qualifying shared
  variants. ClinVar review status is unavailable in the local table.
- UK Biobank P/LP-or-predicted-LoF union: 1,264 participants and 80 cases;
  prespecified sensitivity only.

The programme has previously examined outcomes in both cohorts. Therefore,
reciprocal transport and candidate comparison are explicitly labelled
retrospective, target-informed model development/internal-external validation,
not pristine independent external validation.

## Locked outcome and data handling

- DRAGON outcome: `ASCVD_combined`; component-union and hard-coronary outcomes
  are sensitivity analyses.
- UK Biobank outcome: `prevalent_ascvd`.
- No participant identifier, family identifier, variant coordinate,
  participant-level prediction, or participant row is written.
- Missing predictor values are imputed inside each training fold. Scaling,
  apoB-on-LDL residualisation, model fitting, and penalty selection also occur
  inside the training data only.

## Predictors and the discordance test

All candidate models are deliberately low-dimensional because each primary
cohort has fewer than 65 cases. The clinical core uses the published
Montreal-FH-SCORE linear predictor. The apoB discordance residual is the
training-data residual from `log(apoB) ~ log(LDL-C)`; LDL-C remains in the model.
This separates LDL concentration from apoB information more transparently than
claiming that a ratio is intrinsically superior.

Locked candidates:

1. age + sex;
2. published Montreal-FH-SCORE;
3. Montreal + log LDL-C;
4. Montreal + log apoB;
5. Montreal + log(apoB/LDL-C);
6. Montreal + log LDL-C + apoB discordance residual (CALON-DISC core);
7. CALON-DISC core + log(TG/HDL-C);
8. CALON-DISC core + log Lp(a);
9. Montreal + FH-Risk-Score + CALON-DISC core (score-stack sensitivity).

The ratio and discordance parameterisations span the same two-predictor linear
space when both LDL-C and apoB information are present. Their predictions must
therefore be numerically checked for equivalence; residualisation is an
interpretability choice, not a claim of additional mathematical information.

Lp(a), apoA1 and treatment are not eligible for the primary model: Lp(a) and
apoA1 did not transport incrementally in the prior UK Biobank carrier analysis,
and available treatment flags cannot establish pre-phenotype treatment timing.

## Model fitting and selection

- Penalised logistic regression is primary.
- Ridge penalty `C` is chosen within grouped inner cross-validation from
  `{0.01, 0.03, 0.1, 0.3, 1.0, 3.0}` by Brier score, with AUC as a secondary
  descriptor.
- Whole-pipeline repeated nested 5-fold grouped CV is reported within each
  cohort.
- Reciprocal transport (DRAGON to UKB strict; UKB strict to DRAGON) is reported
  for every locked candidate.
- The primary architecture is chosen by the highest minimum reciprocal-transport
  AUC, provided calibration and sign coherence are not materially worse. This
  outcome-informed multi-cohort choice is exploratory and cannot be represented
  as protected validation.
- A pooled final equation may be frozen for future testing, but its apparent or
  resampled performance is not external validation.

## Comparators

- published/adapted Montreal-FH-SCORE;
- published/adapted FH-Risk-Score;
- adapted SAFEHEART score without prior-ASCVD as a predictor, because that term
  would be circular for established ASCVD;
- age + sex.

All comparisons use identical participants and outcomes. Comparator adaptations
and missing inputs are stated explicitly.

## Metrics and uncertainty

- AUC with family- or qualifying-variant-component bootstrap 95% CI;
- paired delta-AUC against each comparator with the same clustered bootstrap;
- Brier score, calibration intercept, slope and E:O without target recalibration;
- decision-curve net benefit is exploratory and interpreted only as referral or
  case-finding utility, not preventive treatment benefit;
- calibration plots and ROC plots.

## Subgroups and stopping rule

Prespecified subgroups are sex, age below/above cohort median, recorded lipid
treatment, diabetes, and Lp(a) below/above 143 in source units. No architecture
or coefficient is selected using subgroup results. A subgroup with fewer than
10 cases is tabulated as non-estimable; 10--19 cases is descriptive only. Group
differences require interaction/paired-difference evidence, not contrasting
within-group significance.

The model will not be called universally superior unless the paired interval is
above zero against every comparator in both primary cohorts and no evaluable
subgroup shows a credible decrement. If that condition fails, the manuscript
will report the strongest supported result rather than continue outcome-guided
searching.

## Reporting target

The initial manuscript is written for the *Journal of Clinical Lipidology* and
audited item-by-item against TRIPOD+AI, STROBE and PROBAST. Clinical deployment
is prohibited without a new cohort with pre-event biomarkers and prospective
outcomes.

## Amendment 1: from-scratch architecture (2026-08-09, before phase-B run)

The investigator rejected any architecture that adds new terms to a published
score. Accordingly, candidates 2--9 above are retained only as a completed
diagnostic showing what score augmentation can and cannot achieve. They are not
eligible as the novel model.

The phase-B primary candidates are fitted solely from raw clinical variables:

1. age + male sex;
2. age + male sex + log(apoB/LDL-C);
3. age + male sex + HDL-C + hypertension + smoking;
4. candidate 3 + log(apoB/LDL-C) (CALON-N core);
5. CALON-N core + diabetes;
6. CALON-N core + log(TG/HDL-C);
7. CALON-N core + log Lp(a);
8. CALON-N core + log apoA1;
9. age + male sex + HDL-C + hypertension + smoking + log LDL-C + apoB
   discordance residual;
10. age + male sex + hypertension + log(apoB/LDL-C), a parsimonious
    specialist-clinic candidate.

Published scores are comparators only. Coefficients must have the prespecified
directions: age, male sex, hypertension, smoking, diabetes, TG/HDL, Lp(a),
apoB/LDL and discordance non-negative; HDL-C and apoA1 non-positive. The same
grouped tuning, reciprocal transport, calibration, subgroup and stopping rules
apply. This amendment narrows the primary scientific claim; it does not alter
outcomes, cohorts or metrics after inspection.
