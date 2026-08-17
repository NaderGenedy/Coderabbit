# Julius Cycle 2 - CALON-G

This pack implements the locked 15 August 2026 protocol. It reads no files and
assumes participant DataFrames are already loaded inside Julius. It writes only
aggregate tables, plots and model metadata; OOF predictions remain in memory.

## Paste order and gates

Paste these files in exact order after the frozen cohort builder:

| Order | File | Gate/action |
|---:|---|---|
| 00 | `00_findings_lock.py` | Load the complete engine, constants, aggregate-output guard and SHA helper. |
| 01 | `01_horizon_prove.py` | Require the actual cohort SHA and 3,540 -> 207 -> 124 -> 3,209 flow; prove 289/97/194 events. |
| 02 | `02_calong_fit.py` | Fit frozen CALON-G with repeated grouped 5-fold OOF ridge Cox and nested training-fold penalty selection. |
| 03 | `03_comparators_pdf_faithful.py` | Score all three source equations with the same outer-fold imputation plan. |
| 04 | `04_headtohead_tripod.py` | Publish the complete matrix with paired cluster bootstrap `B=2000`. |
| 05 | `05_wales_transport.py` | Require a completed Welsh filter ledger and transport frozen UKB coefficients. |
| 06 | `06_calibration_dca.py` | Estimate censoring-aware OOF calibration and 10-year DCA at 5%, 7.5% and 10%. |

The non-negotiable cohort SHA is:

`8c3a1e0598770c1beefe29db28d42fb7074f233f382c25c19eb0c843b59f49b2`

Cell 01 compares an **actual upstream SHA** (`COHORT_HASH` or the reproducible
settlement signature) with that value. Merely copying the expected value into a
result does not pass the gate.

## Required Julius objects

Before cell 01:

```python
FROZEN = ...  # already-built frozen UKB DataFrame; do not load it in this pack
COHORT_HASH = ...  # actual hash emitted by the frozen builder
COHORT_LEDGER = {
    "n_carriers": 3540,
    "n_prevalent": 207,
    "n_undated": 124,
    "n_frozen": 3209,
}
```

`FROZEN` must carry `time_years`, `event`, `age`, `male`, `bpmed`, `dm`,
`smoke_curr`, `cum_nonhdl`, `log_tghdl`, and either `log_lpa` or native
`lpa_nmol`. `sp50` is deterministically rebuilt as `max(age - 50, 0)` and any
supplied copy is checked. The sole model sensitivity requires
`log_apob_hdl` and replaces, never supplements, `cum_nonhdl`.

Comparator inputs are `htn_any` (or a source-aligned `safeheart_hbp`), `bmi`,
measured `ldl` in mmol/L (or `ldl_mgdl`), untreated/imputed `ldl_unt` in
mmol/L, `hdl` in mmol/L, `smoke_ever`, and native `lpa_mgdl`. Individual
missing values are imputed with training-fold medians/modes. A predictor that
is wholly unavailable makes the relevant score `NOT_EVALUABLE`; it is never
replaced with a healthy default.

For cell 05, provide `WALES_START`, `WALES_FINAL`, `WALES_LEDGER`, and the
explicit investigator decision `WALES_LPA_COMPARABLE = True` or `False`.
`WALES_START.Positive1 == 1` must count 2,405. Every ledger row must contain
`step`, `status="COMPLETE"`, `n`, `criterion`, `source_fields`, and
`excluded_n`. It needs a Positive1 start row plus at least one eligibility or
analysis-set row; each `excluded_n` must reconcile adjacent counts. The last
row must also contain `events`, `filters_complete=True`, `analysis_set=True`,
`investigator_approved=True`, `endpoint` exactly equal to the locked endpoint,
and `i50_excluded=True`. Counts must be non-increasing and the last `n`/events
must match `WALES_FINAL`. `WALES_FINAL` must hold the locked predictors,
positive finite `time_years`, binary `event`, and `FamilyNumber`. Missing family
IDs become unique row clusters; they are never discarded or collapsed. Any
TODO, omitted attestation, missing filter detail, or count disagreement stops
before a Welsh C-index is printed.

`WALES_LPA_COMPARABLE=True` is an explicit assay/unit assertion, not something
inferred from column presence. `False` makes the primary frozen nine-term model
`NOT_EVALUABLE`; a frozen reduced no-Lp(a) model is run only when
`ALLOW_WALES_REDUCED_LPA_SENSITIVITY=True`, and remains exploratory.

## Locked analysis rules

- Primary endpoint: first incident `I21 | I25 | I63 | I70 | I73 | G45`.
  `I50` is out. This is primary ASCVD, not MACE. Any MACE analysis needs a
  separately written definition, flow and SHA.
- Primary SPEC: `age, sp50, male, bpmed, dm, smoke_curr, cum_nonhdl,
  log_tghdl, log_lpa`. Do not substitute `htn_any` for `bpmed` and do not
  retune after seeing WIN/TIE/LOSS.
- Missingness is not assumed MCAR. Continuous predictors use the training-fold
  median; binary predictors use the training-fold mode. Preprocessing and ridge
  penalty selection occur inside resampling folds.
- Five-year follow-up is administratively truncated; nobody is removed from
  the risk set. It must contain 97 events. Ten-year follow-up must contain 194.
- Confirmatory delta-C uses a paired family/cluster bootstrap with exactly
  2,000 valid draws. Sparse cells remain non-estimable.
- SAFEHEART is centred at `5.4078`. Montreal is a ranking-only point score:
  its intercept, horizon and absolute-risk mapping are `NOT-IN-PDF`, so it is
  excluded from calibration/DCA.
- Lp(a) nmol/L divided by 2.15 is available only when
  `RUN_EXPLORATORY_LPA_CONVERSION=True`; every resulting SAFEHEART/FH-RS row is
  labelled exploratory and cannot satisfy the native-unit confirmatory claim.
- Wales uses frozen UKB preprocessing and coefficients. A no-Lp(a) reduced
  model plus Wales recalibration is allowed only with
  `ALLOW_WALES_REDUCED_LPA_SENSITIVITY=True` and is labelled exploratory, not
  the primary external validation.
- MICE under MAR remains a separately invoked sensitivity (`m>=20`, outcome
  not imputed, pooling method declared before execution); this pack never
  mislabels complete-case analysis as MCAR.

## Dependencies and aggregate outputs

Python dependencies: `numpy`, `pandas`, `lifelines`, and `matplotlib`.

Outputs go to `calon_cycle2_out/` (override with `CYCLE2_OUT`) and include the
findings lock, horizon proof, model/fold summaries, comparator evaluability,
complete head-to-head table, calibration summary/bins/plot, DCA table, Welsh
ledger/transport status, explicit `tripod_ai_checklist.csv` and
`strobe_flow.csv`, and run metadata. No participant predictions,
identifiers, family labels, or source rows are written.

Use a new, empty `CYCLE2_OUT` for every execution. Cell 01/local orchestration
fails if it finds any prior Cycle-2 artefact; the engine does not delete old
evidence. A successful complete run ends by writing `run_meta.json` with
`run_complete=true`, preventing a partial rerun from masquerading as a clean
evidence package.

The local one-cell equivalent is
`code/16_CALON_G_CYCLE2.py`. Paste it to define the engine and call
`run_cycle2(FROZEN, COHORT_LEDGER, COHORT_HASH, ...)`, or run
`python3 code/16_CALON_G_CYCLE2.py --self-test` for coefficient/horizon smoke
tests that use constants only.
