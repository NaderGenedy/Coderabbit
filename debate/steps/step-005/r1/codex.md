# Step 005 · Round 1 · codex

## 1. Methodology

The two-stage design is valid as an **exploratory incremental-prediction policy**, provided Stage A, band selection, Stage B fitting, and fallback routing are validated as one nested pipeline. It does not validate or replace the locked CALON-G primary.

### What the Cycle-2 pilot establishes

The on-disk R pilot reports:

| Pilot result | Value |
|---|---:|
| Frozen cohort | n=3,209; 289 full, 97 five-year, 194 ten-year events |
| CALON-G OOF C | 0.7047 |
| Head-to-head tally | 10 WIN, 44 TIE, 0 LOSS |
| Bootstrap | B=300 only |
| Lp(a) comparator policy | `exploratory_div215` |
| SAFEHEART evaluable set | 2,470 / 221 events |
| FH-Risk-Score evaluable set | 1,913 / 146 |
| Montreal evaluable set | 2,811 / 252 |
| Centred SAFEHEART mean five-year risk | approximately 0.0101 |

For the ALL cells:

| Comparator | Full follow-up | Five years |
|---|---:|---:|
| SAFEHEART | ΔC +0.0260 (−0.0045, +0.0545), TIE | +0.0209 (−0.0283, +0.0703), TIE |
| FH-Risk-Score | +0.0098 (−0.0168, +0.0359), TIE | +0.0179 (−0.0215, +0.0538), TIE |
| Montreal | +0.0326 (+0.0127, +0.0521), WIN | +0.0478 (+0.0068, +0.0894), WIN |

The polarity correction using `reverse=TRUE` is therefore coherent. Nevertheless, B=300, exploratory Lp(a) conversion, and varying comparator populations make this smoke testing—not reportable adjunct evidence. Likewise, the split-design smoke showing no LOSS after adding Lp(a) and apoB/LDL on the full cohort establishes only that no catastrophic discrimination collapse was seen. It does not validate band selection, Stage-B calibration, or the deployed fallback policy.

### Separate models and claims

| Track | Specification and claim |
|---|---|
| **Confirmatory CALON-G** | Frozen nine-term model: `age, sp50, male, bpmed, dm, smoke_curr, cum_nonhdl, log_tghdl, log_lpa`. The claim is its prespecified OOF discrimination, calibration, and PDF-faithful comparator performance on the frozen endpoint/cohort, followed by Wales transport. No confirmatory WIN is established by the pilot. |
| **Exploratory CALON-GZ** | Stage-A accessible core plus conditional Stage-B assay terms. The claim is incremental performance over Stage A among grey-band assay-complete participants, and the performance of the whole availability-aware policy. |
| **Not licensed** | “CALON-GZ improves CALON-G”, “Lp(a) is useful only in the grey band”, “the adjunct improves patient outcomes”, or replacement of CALON-G because one comparator cell improves. |

The clean Stage-B predictor is:

\[
\eta_{AB}=\eta_A+\gamma_1z_{\mathrm{Lp(a)}}+\gamma_2z_{\mathrm{apoB/LDL}},
\]

where \(\eta_A\) is an offset with coefficient fixed at one. Only the two locked \(\gamma\) coefficients are estimated. Stage-A variables are neither re-entered nor re-estimated.

Two estimands must be reported:

1. **Conditional assay value:** Stage A+Stage B versus Stage A on identical held-out participants who are both grey-band and jointly assay-complete.
2. **Operational policy value:** across all held-out participants, apply Stage B only when in-band and jointly assay-complete; otherwise return the exact Stage-A prediction.

The second is the relevant estimand for an availability-aware deployment claim. Neither estimand is causal evidence that ordering assays improves care.

### Band lock

I predeclare:

- **Primary band:** middle tertile of Stage-A **10-year OOF absolute risk**.
- Interval convention: \(q_{1/3} < p_{A,10} \le q_{2/3}\).
- **Sole sensitivity:** middle quintile, \(q_{0.40} < p_{A,10} \le q_{0.60}\).
- The same 10-year-defined membership is used for full, five-year, and ten-year evaluation. It is not redefined separately by horizon.
- Primary DCA threshold: **7.5% ten-year risk**; 5% and 10% are supportive.
- OOF LP-rank banding is rejected as an alternative for this cycle. The quintile cannot rescue a failed tertile analysis.

## 2. Implementation

### Fold and fitting structure

Use six prespecified repetitions of grouped, event-balanced five-fold outer CV, matching the reusable Cycle-2 engine. Use three grouped inner folds and the locked ridge grid `(0.001, 0.01, 0.05, 0.10, 0.50, 1.00)`; exact ties select the stronger penalty.

For every outer split:

1. Learn Stage-A median/mode imputation, scaling, penalty, and baseline survival using outer-training data only.
2. Within outer training, generate inner-cross-fitted Stage-A ten-year risks.
3. Compute \(q_{1/3}\) and \(q_{2/3}\) from those training-only risks and identify the Stage-B training band.
4. Count all in-band events and jointly assay-complete in-band events before fitting. Fewer than 10 at a claimed horizon is a hard stop for that horizon.
5. Derive only:

   - `log1p(lpa_nmol)`
   - `log(apob_mgdl / untreated_ldl_mgdl)`

   Both concentrations must be baseline, positive, and in compatible mass units. Centre/scale using training-band values only and retain those constants.
6. Fit Stage B among assay-complete training-band members with Stage-A LP fixed as an offset. No band-specific baseline recalibration may masquerade as biomarker improvement.
7. Score the outer validation fold using training-derived cutpoints. Missing either assay, an invalid denominator, or being outside the band returns the unchanged Stage-A prediction.
8. Assemble OOF metrics separately within each repeat, then use the prespecified mean across repeats. Apparent full-cohort fits are deployment artefacts only and must be labelled apparent.

After internal evaluation is locked, refit on all UKB data and freeze the numerical UKB cutpoints, coefficients, centring constants, and baseline risks. Wales must not be re-tertiled.

### Horizon gate

```r
horizon_data <- function(time, event, H) {
  list(
    time  = pmin(time, H),
    event = as.integer(event == 1L & time <= H)
  )
}

h5  <- horizon_data(FROZEN$time_years, FROZEN$event, 5)
h10 <- horizon_data(FROZEN$time_years, FROZEN$event, 10)

stopifnot(
  nrow(FROZEN) == 3209L,
  sum(FROZEN$event == 1L) == 289L,
  sum(h5$event) == 97L,
  sum(h10$event) == 194L
)
```

No participant is dropped merely for surviving beyond a horizon. Post-horizon events become censored at \(H\), not events at \(H\).

### Missingness and metrics

| Item | Locked handling |
|---|---|
| Stage-A routine predictors | Training-fold median for continuous variables and mode for binary variables |
| Lp(a), apoB, untreated LDL | No operational imputation; any missing/invalid input invokes Stage A |
| Assay audit | Joint availability overall and in-band, by Stage-A risk, outcome, age, sex, treatment, centre and calendar period |
| Conditional comparison | Same assay-complete held-out participants for A and A+B |
| Operational comparison | All 3,209 participants, explicitly encoding missing assay → A |
| Within-band metrics | Paired ΔC, calibration intercept/slope and plot, Brier/ICI, categorical reclassification, IPCW DCA |
| Bootstrap | B=2,000 family-cluster paired replicates, rerunning preprocessing, band selection, fitting, and prediction; require `B_effective=2000` |
| Comparators | Separate `model ∩ comparator` intersection for each comparator; never one three-comparator intersection |
| Lp(a) comparator scoring | Native published units or `NOT_EVALUABLE`; ÷2.15 remains exploratory |

The Cycle-2 pilot already shows why `B_requested` is insufficient: five rows had fewer than 300 effective draws, including a nominal WIN with only 193.

### Julius/R cells

| Proposed cell | Purpose |
|---|---|
| `00_cycle3_lock.R` | Hash cohort/spec/folds; freeze band horizon, intervals, terms, units, ridge grid, DCA thresholds and B=2,000 |
| `01_stage_a_oof_band.R` | Nested Stage-A OOF risks, training-only tertiles, middle-quintile sensitivity, membership stability and event/assay audit |
| `02_stage_b_crossfit.R` | Exact assay transformations, offset fit, missing-assay fallback and hybrid OOF predictions |
| `03_grey_policy_metrics.R` | Conditional and whole-policy ΔC, calibration, reclassification, DCA and boundary-discontinuity audit |
| `04_comparators_bootstrap.R` | PDF-faithful comparators, per-comparator intersections and exactly 2,000 effective paired draws |
| `05_wales_transport.R` | Frozen UKB coefficients/cutpoints; assay-complete adjunct or explicitly reduced Stage-A result |
| `06_gate_report.R` | Fail-loud promotion ledger and full exploratory output table |

Do not reuse `code/17_grey_zone_enhancers.py`: it uses a 5–20% band, tests alternative enhancer combinations, and refits Stage-A variables inside the band.

Specific pre-fit objection:

```objection
id: OBJ-032
step: 005
raised_by: codex
claim: The current Cycle-2 input contract exposes log_apob_hdl and untreated LDL but does not expose the raw baseline apoB input needed for the locked log(apoB/untreated_LDL) term. An immediate Stage-B fit could therefore substitute the forbidden apoB/HDL term or silently mix incompatible units. Before fitting, the exact apoB and untreated-LDL sources, timing, units, positivity rule, joint missingness, and assay-complete in-band event counts must be frozen.
settled_by: Run debate-teach/julius-cycle3-grey-pack-R/00_cycle3_lock.R and 01_stage_a_oof_band.R; require their aggregate lock output to show the literal formula log(apob_mgdl/untreated_ldl_mgdl), baseline provenance, nonpositive-value counts, joint assay-complete n, and at least 10 jointly complete in-band events at every claimed horizon. Hash that output before 02_stage_b_crossfit.R can run.
status: OPEN
```

## 3. Adversarial audit

Assume the claim “the adjunct improves care” is false. The likely failure mechanisms are:

| Attack | How the claim becomes wrong | Required defence |
|---|---|---|
| Selective assay availability | Testing may depend on risk, centre, treatment, calendar time or clinician suspicion. Complete cases are not the whole grey band. | Conditional and whole-policy analyses; missingness table; prespecified MAR/IPW sensitivity. Do not operationally impute assays. |
| Incompatible ratio components | Measured apoB may be combined with reconstructed untreated LDL, creating treatment-correction and denominator artefacts. | Freeze timing, untreated-LDL derivation, compatible units and positivity checks. Invalid values trigger Stage A. |
| Self-fulfilling band | Selecting where Stage A residuals are worst manufactures apparent enhancer opportunity. | Training-only fixed tertiles; no residual inspection, fold reseeding, band widening or threshold movement. |
| Full-cohort Stage-B leakage | OOF Stage A plus an apparent Stage B is still an apparent two-stage model. | Stage B, transformations, penalties and baseline risk remain wholly inside outer training. |
| Restricted-range discrimination | C is naturally compressed in a middle-risk band and may be unstable. | Treat ΔC as supportive; make whole-policy DCA and calibration central. |
| Recalibration masquerading as biomarker value | A new band-specific baseline can improve calibration without Lp(a) or apoB contributing information. | Keep Stage-A LP coefficient fixed and Stage-A baseline risk unchanged in the primary adjunct analysis. |
| Multiplicity | Tertile/quintile × horizons × thresholds × metrics × subgroups can nearly guarantee something favourable. | One primary band, horizon and threshold. The quintile and 5%/10% thresholds remain supportive regardless of result. |
| NRI inflation | Continuous NRI can look impressive without changing a decision. | Use censored categorical reclassification at the locked thresholds; NRI cannot rescue failed DCA or calibration. |
| Boundary discontinuity | A patient just inside the band may leap above someone just outside it. | Report prediction jumps and whole-policy calibration/ranking around both cutpoints. |
| DCA overclaim | Net benefit assumes a valid action/threshold and does not show improved patient outcomes. | Define the action—such as treatment intensification—and report assay tests per net correct decision. Use “potential utility” absent an impact study. |
| Transport failure | Recomputing Welsh tertiles would hide calibration and case-mix drift. Missing Welsh assays prevent adjunct validation. | Apply frozen UKB cutpoints and coefficients. If assays are unavailable, report only a reduced Stage-A model; that is not validation of Stage B. |
| Comparator-directed tuning | A LOSS may prompt a new band, predictor, or lipid definition. | Publish the LOSS. Comparator WIN/TIE/LOSS is contextual and never an adjunct selection criterion. |

The comparator complete-case fractions in the pilot—approximately 77%, 60%, and 88% of the frozen cohort—already demonstrate how evaluability changes case mix. They do not estimate joint Lp(a)/apoB availability and cannot substitute for the Cycle-3 assay-flow audit.

## 4. Clinical and publication reality

**Recommendation: Promote adjunct only if the named gates pass.** Until then, CALON-G remains the sole confirmatory specification and CALON-GZ remains a labelled research prototype or shadow-mode workflow.

| Promotion gate | Pass rule |
|---|---|
| Frozen integrity | SHA `8c3a1e0598770c1beefe29db28d42fb7074f233f382c25c19eb0c843b59f49b2`; n=3,209; events 289/97/194 |
| Specification | Exact Stage-A and two Stage-B terms; ten-year middle tertile primary; middle quintile sole sensitivity; no alternative lipid term |
| Estimability | At least 10 jointly assay-complete in-band events at every claimed horizon; otherwise that claim stops without widening the band |
| Honest prediction | All claimed risks outer OOF; grouped 6×5 outer CV, three-fold inner tuning, training-only preprocessing/cutpoints |
| Bootstrap | Exactly 2,000 effective paired cluster replicates of the complete pipeline |
| Decision value | Whole-policy Δ net benefit at 7.5% ten-year risk ≥0.005 and paired lower 95% bound >0; no negative point estimate at 5% or 10% |
| Discrimination | Report paired within-band ΔC; say “improved discrimination” only if its 95% lower bound exceeds zero. ΔC alone cannot promote the model |
| Calibration | Ten-year slope 0.8–1.2, absolute cloglog calibration intercept ≤0.10, and no worse Brier/ICI than Stage A for both the in-band and whole-policy predictions |
| Availability | Complete-case and prespecified availability-weighted estimates agree in direction; broad service labelling requires prospective joint-assay return of at least 80%, otherwise restrict the label to assay-complete patients |
| Transport | Same-direction decision benefit and acceptable calibration in Wales or another independent assay-complete cohort with at least 10 in-band events, using frozen UKB components |
| Reporting | Full primary, sensitivity, missingness and failed results published; no selective comparator or subgroup narrative |

A coherent clinical pathway must be chosen. It is invalid to use locked CALON-G outside the band and a differently calibrated Stage-A+Stage-B model inside it without validating that mixed policy. Where Lp(a) is unavailable, Stage A is a separately labelled reduced exploratory model—not CALON-G scored by bedside imputation.

Even if every gate passes, the appropriate publication claim is that targeted assays showed **incremental predictive and decision value in a prespecified intermediate-risk subgroup**. “Improves care” requires an impact study, and “universal winner” requires external transport. Chasing a WIN against every comparator is not a valid confirmatory objective; a comparator LOSS is an admissible final result.

## Artefacts

Existing evidence reviewed:

- [calong_run_meta.json](/Users/nader85/Documents/CALON/calon_discordance_model_2026_08_09/debate/evidence/julius-spec-kit/cycle2_r_pilot/calong_run_meta.json)
- [calong_headtohead_full.csv](/Users/nader85/Documents/CALON/calon_discordance_model_2026_08_09/debate/evidence/julius-spec-kit/cycle2_r_pilot/calong_headtohead_full.csv)
- [comparator_patient_set_audit.csv](/Users/nader85/Documents/CALON/calon_discordance_model_2026_08_09/debate/evidence/julius-spec-kit/cycle2_r_pilot/comparator_patient_set_audit.csv)
- [CALON_G_BIOSTAT_PROTOCOL.md](/Users/nader85/Documents/CALON/calon_discordance_model_2026_08_09/debate/evidence/julius-spec-kit/CALON_G_BIOSTAT_PROTOCOL.md)
- [16_CALON_G_CYCLE2.py](/Users/nader85/Documents/CALON/calon_discordance_model_2026_08_09/code/16_CALON_G_CYCLE2.py)
- [17_grey_zone_enhancers.py](/Users/nader85/Documents/CALON/calon_discordance_model_2026_08_09/code/17_grey_zone_enhancers.py)

Proposed new artefacts:

- `code/r_cycle3/17_CALON_G_GREY_ADJUNCT.R`
- `debate-teach/julius-cycle3-grey-pack-R/00_cycle3_lock.R` through `06_gate_report.R`
- `debate/evidence/julius-spec-kit/cycle3_grey/cycle3_lock.json`
- `debate/evidence/julius-spec-kit/cycle3_grey/stage_a_band_audit.csv`
- `debate/evidence/julius-spec-kit/cycle3_grey/stage_b_assay_flow.csv`
- `debate/evidence/julius-spec-kit/cycle3_grey/cycle3_oof_metrics.csv`
- `debate/evidence/julius-spec-kit/cycle3_grey/cycle3_bootstrap_summary.csv`
- `debate/evidence/julius-spec-kit/cycle3_grey/wales_transport.json`
- `debate/evidence/julius-spec-kit/cycle3_grey/gate_report.json`
