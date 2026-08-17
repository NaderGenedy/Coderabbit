# Cycle-2 comparator provenance

All coefficients below were re-read from the supplied primary PDFs and checked
against the supplied greppable extracts. “PDF page” is the physical PDF page;
journal page is included where useful. A `CANDIDATE` or `NOT-IN-PDF` entry is
deliberately not upgraded from an older code implementation.

## Source pins

| Model | Primary source | PDF SHA-256 | Greppable text |
|---|---|---|---|
| SAFEHEART-RE | `SAFEHEART-RE_PerezDeIsla_2017.pdf` | `2859d29d7b8e93bad83383f62108ba83fcc1008e34f89502545610ce3f0b02bd` | `SAFEHEART_RE_Circulation_2017_.txt` |
| FH-Risk-Score | `FH-Risk-Score_Paquette_2021.pdf`; `FH-Risk-Score_Paquette_2021_suppl.pdf` | main `9330f910f88794325e92cb81ef29442940d130a13b998052805ed3f3c8a28150`; supplement `7ba00a773cc9f5daf19925e1da79de409b1dc91d9354f2df06a373448742a23c` | `FH_RS_ATVB_2021_.txt` |
| Montreal-FH-SCORE | `Montreal-FH-SCORE_Paquette_2017_derivation.pdf` | `e679bd31950183257cbee103cc197862c4984a8802e1601c234e9f204bae177b` | `MONTREAL_orig_JCL_2017_.txt`; confirmed in `MONTREAL_validation_JCL_2017_.txt` |

PDF root: `/Users/nader85/Downloads/CALON-DeepResearch/papers/`  
Text root: `/Users/nader85/Downloads/CALON_FH_PROGRAMME_2026-08-09/04_papers/extracted_text/`

## SAFEHEART-RE

Source equation: Pérez de Isla et al., 2017, physical PDF pp5-7 (journal
pp2137-2139), Table 3 and worked cases. Text pins: categorisation lines 268-274,
equation 436-443, Table 3 at 486-521, worked equations 551-562.

| Predictor/term | Category/reference | Coefficient | Units | PDF page/table | Status/implementation note |
|---|---|---:|---|---|---|
| Male | male vs female | 0.70 | binary | p7, Table 3 worked equation | VERIFIED |
| Age 30-59 | age 30 to <60 vs <30 | 1.07 | years | p6 Table 3; p7 equation | VERIFIED |
| Age >=60 | age >=60 vs <30 | 1.45 | years | p6 Table 3; p7 equation | VERIFIED |
| High blood pressure | yes vs no | 0.69 | binary | p6 Table 3; definition in text extract 158-162 | VERIFIED; available-cohort mapping remains a transport limitation |
| Previous ASCVD | yes vs no | 1.42 | binary | p6 Table 3; p7 equation | VERIFIED; fixed to 0 by the incident-only Cycle-2 eligibility rule |
| Active smoking | current vs not current | 0.48 | binary | p6 Table 3; p7 equation | VERIFIED |
| BMI overweight | overweight vs normal | 0.88 | kg/m2 category | p6 Table 3; p7 equation | Coefficient VERIFIED; numeric 25/30 boundary is **CANDIDATE / NOT-IN-PDF** |
| BMI obesity | obesity vs normal | 0.98 | kg/m2 category | p6 Table 3; p7 equation | Coefficient VERIFIED; numeric 25/30 boundary is **CANDIDATE / NOT-IN-PDF** |
| Measured LDL-C 100-159 | 100 to <160 vs <100 | 0.92 | mg/dL | p6 Table 3; p7 equation | VERIFIED; measured baseline LDL-C, not calculated pretreatment LDL-C |
| Measured LDL-C >=160 | >=160 vs <100 | 1.57 | mg/dL | p6 Table 3; p7 equation | VERIFIED |
| Lp(a) >50 | >50 vs <=50 | 0.42 | mg/dL | p6 Table 3; p7 equation | VERIFIED |
| Centring constant | subtract from indicator sum | 5.4078 | LP units | p5 equation; p7 four worked equations | VERIFIED |
| Baseline survival, 5 y | risk = `1 - 0.9532^exp(LP-centre)` | 0.9532 | survival probability | p5 and p7 | VERIFIED |
| Baseline survival, 10 y | risk = `1 - 0.9025^exp(LP-centre)` | 0.9025 | survival probability | p5 and p7 | VERIFIED; paper cautions 10-y extrapolation (text 746-748) |
| Separate intercept | — | NOT-IN-PDF | — | — | No separate intercept beyond the published centring form |

Worked-case checks in `16_CALON_G_CYCLE2.py --self-test` reproduce the published
5-year risks (~0.02% and ~38.1%) using the displayed rounded coefficients.

## FH-Risk-Score

Source equation: Paquette et al., 2021 supplement physical/numbered p9,
Supplemental Table II. The main PDF p6 (journal p2637), Tables 3-4, supplies the
point chart and rounded risk lookup. The main text extract points to the exact
supplement equation at lines 216-230 and documents current smoking at 112-114
and untreated/imputed LDL at 345-356.

| Predictor/term | Category/reference | Coefficient | Units | PDF page/table | Status/implementation note |
|---|---|---:|---|---|---|
| Male | male vs female | 0.721 | binary | supplement p9, Table II | VERIFIED |
| Age | 18-30 reference | 0 | years | supplement p9, Table II | VERIFIED; model cohort range 18-65 |
| Age | 31-35 / 36-40 / 41-45 | 0.938 / 1.383 / 1.621 | years | supplement p9, Table II | VERIFIED |
| Age | 46-50 / 51-55 / 56-60 / >60 | 1.738 / 1.804 / 1.964 / 2.256 | years | supplement p9, Table II | VERIFIED; Cycle 2 makes age >65 `NOT_EVALUABLE` rather than extrapolating |
| HDL-C | >1.30 reference | 0 | mmol/L | supplement p9, Table II | VERIFIED |
| HDL-C | 1.01-1.30 / 0.85-1.00 / <0.85 | 0.298 / 0.712 / 0.752 | mmol/L | supplement p9, Table II | VERIFIED |
| Untreated/imputed LDL-C | <=5.50 reference | 0 | mmol/L | supplement p9, Table II | VERIFIED; treated measured LDL-C is not substituted |
| Untreated/imputed LDL-C | 5.51-7.50 / 7.51-8.50 | 0.315 / 0.718 | mmol/L | supplement p9, Table II | VERIFIED |
| Untreated/imputed LDL-C | 8.51-9.50 / >9.50 | 0.918 / 1.136 | mmol/L | supplement p9, Table II | VERIFIED |
| Hypertension | yes vs no | 0.644 | binary | supplement p9, Table II | VERIFIED |
| Active smoking | current vs not current | 0.625 | binary | supplement p9, Table II | VERIFIED |
| Lp(a) >=50 | >=50 vs <50 | 0.434 | mg/dL | supplement p9, Table II | VERIFIED |
| Centring constant | subtract from indicator sum | 3.00 | LP units | supplement p9 equation | VERIFIED |
| Baseline survival, 10 y | risk = `1 - 0.889^exp(LP-3.00)` | 0.889 | survival probability | supplement p9 equation | VERIFIED |
| Baseline survival, 5 y | — | NOT-IN-PDF | — | — | No 5-y FH-Risk-Score probability is generated |
| Paper missing-Lp(a) instruction | set unavailable Lp(a) to 0 | 0 | binary | supplement p9 instruction | Source VERIFIED but **not used**: locked Cycle 2 forbids healthy-default imputation |

The implementation uses the regression equation for absolute 10-year risk. The
alternative integer point chart (main PDF p6, Table 3) is not mixed into that
equation.

## Montreal-FH-SCORE

Source: Paquette et al., 2017 derivation PDF physical p4/journal p83 Table 2 and
physical p5/journal p84 Table 3. Greppable pins: `MONTREAL_orig_JCL_2017_.txt`
lines 363-371 (reported betas) and 429-441 (point chart); the original chart is
also confirmed in `MONTREAL_validation_JCL_2017_.txt` lines 250-280.

| Predictor/term | Category/reference | Coefficient/points | Units | PDF page/table | Status/implementation note |
|---|---|---:|---|---|---|
| Reported multivariable beta: age | per derivation standardisation | +0.75 | standardised age | p4, Table 2 | VERIFIED reported beta; not treated as a complete probability equation |
| Reported multivariable beta: HDL-C | per derivation standardisation | -0.27 | standardised HDL-C | p4, Table 2 | VERIFIED reported beta; fixed standardisation constants are NOT-IN-PDF |
| Reported multivariable betas | male / hypertension / smoking | +0.25 / +0.19 / +0.12 | binary | p4, Table 2 | VERIFIED reported betas |
| Age chart | <=21 / 22-28 / 29-35 / 36-42 | 0 / 4 / 8 / 12 | years | p5, Table 3 | VERIFIED |
| Age chart | 43-49 / 50-56 / 57-63 / >63 | 16 / 20 / 24 / 28 | years | p5, Table 3 | VERIFIED |
| HDL-C chart | <=0.60 / 0.61-0.90 / 0.91-1.20 | 12 / 9 / 6 | mmol/L | p5, Table 3 | VERIFIED |
| HDL-C chart | 1.21-1.50 / >1.50 | 3 / 0 | mmol/L | p5, Table 3 | VERIFIED |
| Male | male vs female | 3 points | binary | p5, Table 3 | VERIFIED |
| Hypertension | yes vs no | 2 points | binary | p5, Table 3 | VERIFIED |
| Smoking | prior or current vs never | 1 point | binary | p5, Table 3 footnote | VERIFIED |
| Logistic intercept | — | NOT-IN-PDF | — | — | No published absolute-risk probability is calculated |
| Baseline survival / time horizon | — | NOT-IN-PDF | — | — | Original model predicts prevalent CVD; use for ranking/discrimination only |
| Calibration/DCA mapping | — | NOT-IN-PDF | — | — | Montreal is excluded from absolute-risk calibration and DCA |

## Unit and missingness decisions imposed by the locked protocol

| Item | Decision | Status |
|---|---|---|
| Cholesterol mmol/L to mg/dL | multiply measured LDL-C by 38.67 when SAFEHEART mg/dL input is not already present | Labelled unit conversion; no coefficient invented |
| Lp(a) nmol/L to mg/dL | divide by 2.15 only when `RUN_EXPLORATORY_LPA_CONVERSION=True` | **EXPLORATORY sensitivity; NOT-IN-PDF for either comparator** |
| Native Lp(a) mg/dL absent | SAFEHEART-RE and FH-Risk-Score are `NOT_EVALUABLE` for the confirmatory native-unit run | Locked protocol |
| Individual missing comparator values | outer-training-fold median for continuous values and mode for binary values | Locked protocol; not MCAR |
| Wholly unavailable predictor | score remains `NOT_EVALUABLE`; no healthy reference/default | Locked protocol |

## CALON-G coefficients

CALON-G has no published PDF coefficient table. Its nine coefficients are
`FITTED_ON_JULIUS` under nested-CV-selected ridge and are written only after the
cohort SHA gate passes. The predictor units are: age/sp50 years; male, bpmed,
diabetes and current smoking binary; cumulative non-HDL, log(TG/HDL), and
log1p(native UKB Lp(a) nmol/L) on their locked transformed scales. Any numerical
CALON-G coefficient before a real Julius run is **NOT-IN-PDF / NOT YET FITTED**.
