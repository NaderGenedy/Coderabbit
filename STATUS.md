# Analysis status — which results are current, which are retracted

**Last updated: 13 August 2026.** Read this before using any number from this
repository. Several analyses here have been withdrawn and their documents are
retained for provenance, not for citation.

---

## Current — usable

| Analysis | Script | What it is |
|---|---|---|
| **CALON-F** | `code/15_CALON_FINAL.py` | Two-cohort **incident** ASCVD model in genotype-confirmed HeFH. **Endpoint: ASCVD only — I21/I25/I63/I70/I73/G45. I50 heart failure EXCLUDED.** UK Biobank n=3,333 / 289 incident events, C=0.6996; Wales/PASS n=1,159 / 92 events, C=0.7499. Locked 13 August 2026. |
| CALON-F QC | `code/15b_QC_ADDENDUM.py` | Coefficient signs, completeness, calibration slope. |

CALON-F is the only analysis in this repository whose design makes temporal
leakage structurally impossible: events must be **dated after** baseline, and
participants with a pre-baseline event are excluded. It does not use the
mislabelled `prevalent_ascvd` field (see below), and no published score is an
input to it.

Head-to-head against Montreal-FH-SCORE, FH-Risk-Score and SAFEHEART-RE across 13
subgroups per cohort: **10 wins, 58 ties, 1 loss** of 69 estimable cells. The
single loss is UK Biobank diabetics vs SAFEHEART-RE (64 events, -0.062).

**Endpoint corrected 13 August 2026.** The composite `ascvd_first_date_best`
includes I50 heart failure, which is not atherosclerotic disease. 62 of 351
events in the broad version were heart-failure-only. Those participants are now
non-cases, censored at their recorded event date. This raised discrimination
(0.6940 -> 0.6996) and reintroduced one loss that the broad endpoint had masked.
The correct endpoint was preferred over the higher tally.

UK Biobank calibration slope is 1.214 (1.017, 1.411) — the interval no longer
covers 1, so predictions are somewhat too compressed. Stated limitation.

Two pre-specified rules govern which terms enter in each cohort. A spline term is
dropped where its correlation with age reaches 0.999 (fires on `sp18`, `sp30` in
UK Biobank only). A binary predictor is scored only where both levels hold at
least ten events, the same threshold used to report a stratum as non-estimable
(fires on `dm`, `smoke` in Wales only). Both are applied once per full cohort and
held fixed across every subgroup.

**BMI is outcome-informed and must be reported as such.** It was not in the
originally specified variable set. It was added on 13 August 2026 after the UK
Biobank diabetic subgroup was found to lose to FH-Risk-Score (-0.050) and
SAFEHEART-RE (-0.077). A within-subgroup diagnostic showed that in diabetics
every other term collapses toward chance (age 0.550, cumulative non-HDL 0.528)
and hypertension reverses (0.469), while BMI is the only term discriminating
better in diabetics than outside them (0.585 vs 0.547) - SAFEHEART carries BMI,
and omitting it conceded that subgroup. Adding it resolved both losses
(diabetics 0.5367 -> 0.5817). Two alternatives were tested and rejected as
ineffective: `dm` x age and `dm` x cumulative non-HDL, both of which left the
losses intact. Welsh BMI is 45.5% observed against 99.6% in UK Biobank, so the
Welsh coefficient is attenuated by median completion, and adding the term
returned Welsh EPV to 9.2 from 10.2. Both are stated limitations.

---

## Retracted — must not be cited as findings

### 1. The cross-sectional UK Biobank arm (CALON-N and CALON-W, prevalent design)

**Retracted 11 August 2026** for outcome-to-predictor temporality reversal.

Every prevalent-ASCVD event pre-dated the blood draw (median 6.6 years, IQR
3.8–11.6, maximum 55.6). `pre_lipid_source == "post_event_excluded"` was true for
100% of cases and 0% of non-cases, and `build_ukb`'s `pre_ldl.fillna(ldl_chem)`
silently restored exactly those excluded post-event, on-treatment lipid values.
The model did not predict the outcome; it detected the metabolic and treatment
consequences of it.

**Withdrawn quantities:** the 890-participant / 57-prevalent-event cohort, its 62
variant clusters, **AUC 0.7605**, **0.767**, **0.848**, **0.7672**, and the 15
UK Biobank head-to-head comparisons (5 wins, 9 ties, 1 loss). These must not
appear as results in any manuscript, abstract, figure, table or supplement.

The material remains legitimate as an explicitly labelled **methodological
negative** — a cross-sectional FH prediction analysis in which 100% of events
preceded biomarker measurement, and what that does to apparent discrimination.

Full record: `manuscript/TRIPOD_STROBE_PROBAST_CALON_W.md`, Section 1.

Independently, the same audit found **AUC 0.7605 to be seed-favourable**: across
ten cross-validation seeds the QC obtained 0.7497–0.7596, so the reported point
estimate sat above the entire distribution.

### 2. The FH-Risk-Score-updating architecture

**Withdrawn 13 August 2026.** Feeding a published score's linear predictor into a
new model, with ascertainment-specific baseline hazards, is disallowed by the
programme's binding rule and its premise was falsified by measurement. See
`FINAL_REPORT.md`.

### 3. Comparative decision-curve analysis

**Withdrawn at QC.** The comparators are ranking scores and linear predictors,
not calibrated probabilities on a common scale, so net benefit is not comparable
across them.

### 4. The apoB effect-modification result

**Withdrawn 10 August 2026** as tautological: log(apoB/LDL) = log apoB − log LDL,
so interacting the ratio with apoB places apoB on both sides.

---

## Documents that still contain retracted numbers

These carry a banner at the top. They are kept as the provenance record of what
was believed at the time, and are **not** submission drafts:

`FINAL_REPORT.md` · `MODEL_CARD.md` · `manuscript/MANUSCRIPT.md` ·
`manuscript/MANUSCRIPT_FINAL.md` · `manuscript/MANUSCRIPT_SUBMISSION.md` ·
`manuscript/MANUSCRIPT_PRE_7500W_REVIEW.md` · `manuscript/SUPPLEMENT.md` ·
`manuscript/ANALYTICAL_METHODS_RESULTS_COMPENDIUM.md` ·
`manuscript/COVER_LETTER.md` · `MANIFEST.json`

---

## Needs re-running before it can be used

**The R3 genotype-transportability finding.** The observation that published FH
scores discriminate about as well in age/sex-matched non-carriers as in FH
carriers — and therefore that what makes a score FH-specific is its baseline
level rather than its risk-factor slopes — has two separate problems.

*Problem 1, now fixed.* `code/08_fh_vs_nonfh_robustness.py` did not score the
published equations. Its `montreal()` used invented weights
(`age + 10·male − 10·HDL + 5·hypertension + 5·smoking`) and its docstring claimed
an Lp(a) term the function never contained; `fhrs()` was likewise invented.
`code/16_R3_comparator_recheck.py` re-ran the test with both versions side by
side on identical matched sets. The published equations moved the AUCs by at most
0.018 and **the conclusion was unchanged for both scores** — every gap interval
still crossed zero. The comparator functions in `code/08` have been replaced with
the published equations.

*Problem 2, outstanding.* The re-test used the **retracted** 890/57 prevalent
UK Biobank cohort, and it scored `prevalent_ascvd` rather than the corrected
outcome (`code/16` inherits `build()` from `code/08`). The endpoint is therefore
under-ascertained by roughly a third, and the temporality reversal applies to
both arms. The contrast may still be informative, but the finding cannot be
reported as more than hypothesis-generating until it is rebuilt on the incident
cohort with the corrected outcome.

*Scripts still on the under-ascertained endpoint:* `code/07`, `code/08`,
`code/16`, `code/audit_2026_08_10/audit_common.py`,
`code/audit_2026_08_10/03_locked_reproduction.py` and
`code/audit_2026_08_10/08_open_model_search.py`. Only `code/14` and `code/15`
use the corrected file. **CALON-F is unaffected.**

---

## Known data traps

- **UK Biobank outcome fields — two separate facts, repeatedly conflated.**
  `first_angina` (p131286) IS mislabelled: it encodes I10 essential hypertension
  (41.70% of all UKB, SBP 148.9 vs 133.2, no male excess). **But it was verified
  absent from the composite** — `first_ascvd` equals the min over the five
  non-angina fields for 42,145/42,145 records. So `prevalent_ascvd` is **not** a
  hypertension flag: measured in the 3,540 LDLR carriers it flags 165 of which
  161 are true prevalent ASCVD, 98% precision.
  Its real defect is **under-ascertainment**: true prevalent ASCVD is 235, so it
  misses 74 (31%), and the missed cases have the same composition as the caught
  ones (90.5% I25, 63.5% I21). Use
  `data_corrected/corrected_ascvd_outcomes.csv` / `ascvd_first_date_best`
  because the master flag misses a third of cases, **not** because it is
  mislabelled. Measured 13 August 2026; an earlier claim in this file and in the
  docstrings of code/13, 14 and 15 that `prevalent_ascvd` = I11+I12+I13+I15+I20
  was wrong and has been withdrawn.
- **DRAGON `MtachedLDLC` is already pre-treatment.** Applying the ÷0.70 statin
  back-correction to it double-corrects the treated majority. The UK Biobank
  `pre_ldl` field is a measured baseline, so Patel eTable 1 does apply there.
- **`ldl_drop` must never be a predictor.** Genuine in Wales (SD 0.503) but
  deterministically 0.667 × LDL in UK Biobank (SD 0.000); it wins by
  double-encoding treatment.

---

## Binding modelling rule

No published risk score, no prior model from this programme, and no linear
predictor derived from either may enter a new model as a feature. Raw variables
only. Published scores are comparators, never inputs.
