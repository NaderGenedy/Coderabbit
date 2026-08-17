# CALON Spec-Kit Execution Report

**Execution date** — 15 August 2026  
**Scope** — `00_governance_header.py` through `05_wales_filter_ledger.py`, followed by settlement `cell_05.py` through `cell_13.py`.

## Executive verdict

The spec-kits were executed. The fail-loud settlement pack successfully reproduced the frozen UKB cohort after one necessary endpoint correction:

- LDLR carriers — 3,540
- prevalent permitted ASCVD excluded — 207
- undated permitted ASCVD excluded — 124
- frozen risk set — 3,209
- full-follow-up events — 289
- five-year events — 97
- ten-year events — 194

The confirmatory head-to-head output is **not publication-confirmatory**. All three comparators remain unverified candidate implementations, the Lp(a) analysis required a declared fixed-factor sensitivity conversion, only 300 rather than 2,000 bootstrap repetitions were used for this execution pilot, and the supplied five-year horizon mask is incorrect.

## Defects identified

### Compact UKB ledger

`01_cohort_ledger_ukb.py` counted any dated outcome as prevalent rather than requiring one of the permitted atherosclerotic components. It therefore returned 235 prevalent exclusions and a 3,181-person risk set. The correct permitted-component ledger is 207 prevalent, 124 undated and 3,209 eligible.

### Settlement event definition

The original `cell_06.py` correctly failed because it counted 351 full-follow-up events rather than the reference 289. The line defining `event_full` did not require a permitted ASCVD component. Adding the permitted-component flag reproduced all reference counts exactly.

### Compact SAFEHEART experiment

`02_obj001_dual_safeheart.py` retained only 429 complete cases and 269 events because survivors without a death date were dropped. Its concordance estimates are not comparable with results from the 3,209-person frozen cohort.

### Lp(a) policy

Under the native `NOT_EVALUABLE` policy, SAFEHEART and FH-Risk-Score cannot be scored. An explicitly declared nmol/L divided by 2.15 sensitivity conversion was therefore used only for exploratory execution.

### Fixed-horizon mask

The supplied mask in `cell_09.py` and `cell_13.py` uses:

`(time <= horizon) OR (event == 1)`

This includes events occurring after the horizon and preferentially selects early-censored non-events. The resulting “five-year” common set contained 146 events rather than the frozen 97. These horizon-specific rows must be withdrawn and rerun with correctly truncated follow-up.

## Valid exploratory findings

The centred SAFEHEART implementation produced substantially more plausible calibration than the uncentred implementation. At five years, the centred mean predicted risk was 1.22%, compared with 77.0% when uncentred. The centred calibration slope was 0.871, compared with 0.166 when uncentred.

Age and cholesterol-years were correlated at 0.606, below the 0.999 automatic-drop threshold but high enough to require interpretation. The age hazard ratio was 1.043 per year with age plus cholesterol-years, 1.052 with age plus untreated total cholesterol, 1.033 with age plus cumulative non-HDL, and 1.055 with age alone.

## Mechanical confirmatory tally

`cell_13.py` completed mechanically with 68 TIE cells, nine LOSS cells and one WIN cell. This tally must not be quoted as confirmatory because:

1. SAFEHEART and FH-Risk-Score were not independently verified against their source PDFs.
2. Montreal lacked its source PDF and was labelled a candidate implementation.
3. The horizon mask is invalid.
4. The execution pilot used 300 rather than 2,000 bootstrap repetitions.
5. Seventy-eight dependent subgroup cells create major multiplicity.
6. The model predictions were loaded from a previously fitted five-year pipeline and used beyond their native horizon.

## Frozen provenance

The corrected frozen cohort SHA-256 is:

`8c3a1e0598770c1beefe29db28d42fb7074f233f382c25c19eb0c843b59f49b2`

The frozen specification SHA-256 is:

`dff51da99bb72ea82d54634658fc399604182225d58a61eb1dfa0224ba1303f9`

## Required corrections before rerunning confirmatory analyses

The event definition must require a permitted ASCVD component. Five- and ten-year follow-up must be truncated correctly. Comparator coefficients and score charts must be independently verified from the source PDFs. An Lp(a) policy must be frozen before scoring. The final model linear predictor must be generated inside the same frozen cohort pipeline. The requested 2,000 bootstrap repetitions and a multiplicity assessment must then be run.
