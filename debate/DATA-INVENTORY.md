# Data inventory — everything needed to plan analysis code

**Read this before writing a line of code.** Every column name below was verified
against the actual file headers on 15 August 2026, not recalled from memory.

**You will never see participant data.** This inventory gives you file shapes,
column names and derivation rules. That is enough to write correct code and is
all you are permitted. Never request a data extract, a row, or an identifier.

---

## Files

| Key | File | Rows × Cols | Role |
|---|---|---|---|
| `ukb_master` | `ukb_master.csv` | 501,936 × 179 | Exposures, covariates, baseline date, carrier flag. **Its own outcome columns are unusable — see traps.** |
| `ukb_outcomes` | `corrected_ascvd_outcomes.csv` | 501,936 × 14 | **The outcome source.** Join on `eid`. |
| `ukb_bpmeds` | `04a_meds_touch.csv` | 501,936 × 13 | Touchscreen BP medication. Columns prefixed `participant.` |
| `wales` | `WALES_FH_CLEANED.csv` | 7,253 × 190 | The Welsh analysis cohort |
| `pass` | `pass_master.csv` | 7,253 × 141 | Same registry, different column naming. Zero shared column names with `wales`. |
| `dragon` | `FH_Dragon3 (1).csv` | 424 × 202 | Complete subset of `wales` (424/424 on `DatabaseNumber`) |

All in one folder: `CALON_DATA_PACKAGE_2026-08-13/raw/all_inputs/`.
SHA-256 for each is in `SHA256SUMS.txt`.

---

## UK Biobank columns

**Cohort and time**
`eid` · `ldlr_carrier` (1 = carrier; 3,540 of 501,936) · `date_baseline` ·
`age_exact_baseline` · `sex_F` (1 = female) · `death_date` · `death_cause`

**Lipids** — `tc_chem` · `ldl_chem` · `hdl_chem` · `tg_chem` · `apob` ·
`apob_chem` · `nmr_apob` · `lpa_chem` · `pre_lpa` · `lpa_i0`

**Risk factors** — `sbp` · `dbp` · `diabetes_combined` · `diabetes_any` ·
`smoking_ever` · `smoking_current` · `smoking_status` · `bmi_direct`

**Treatment** — `on_statin_self` · `statin_ever` · `statin_duration_years` ·
`age_at_statin_start`

**BP medication** (separate file) — `participant.p6153_i0` (women),
`participant.p6177_i0` (men). Code `2` in either means BP medication. Baseline
instance `_i0` only.

**Outcomes** (`ukb_outcomes`) — `ascvd_first_date_best` · `ascvd_first_date_dated`
· component flags `i21_event` `i25_event` `i50_event` `i63_event` `i70_event`
`i73_event` `g45_event`

---

## Welsh columns

**Cohort** — `Positive1` (**the genotype flag**) · `Mutation1` (**not** the flag)
· `DatabaseNumber` · `FamilyNumber` · `Gender` · `Proband`

**Outcome** — `ascvd_combine` (**the outcome flag**) · event ages `MIACSAge`
`PCIStentsAge` `CABGAge` `ANGINAAge` `TIAAge` `PVDAge`

**Time** — `DOB`, `DOB_1` · `MeasurementDate.1` … `.4` · `BMIDate` ·
`AGE_AT_DECEASED` · `Treatmentdate1`

**Lipids, serial** — `TC.1–.4` · `LDL.1–.4` · `HDL.1–.4` · `TRG.1–.4` · `Lpa.1–.4`

**Risk factors** — `Smoking` · `Diabetes` · `BloodPressureMedication` ·
`BloodPressureSystolic` · `BloodPressureDiastolic`

## DRAGON columns — what it adds to Wales

Join `dragon` onto `wales` on `DatabaseNumber` (424/424). It contributes:

- **`ApoB`** — the *only* apoB anywhere in the Welsh data
- Serial lipids `TC_1–4`, `LDL_1–4`, `HDL_1–4`, `TRG_1–4`, `Lpa_1–4` with
  `MeasurementDate_1–4`
- `MtachedLDLC` — **already pre-treatment**
- `age_at_event`, `age_at_event_or_censoring`, `Smoking_binary`,
  `Diabetes_binary`, `onBPtreat`, `eGFR`, `BMI`

Note the naming difference: Wales uses dots (`TC.1`), DRAGON uses underscores
(`TC_1`). Do not assume one from the other.

---

## Traps — each of these has already produced a wrong result

**1. `first_angina` is hypertension.** Flags 41.7% of UK Biobank, mean SBP 148.9
vs 139.7, no male excess. It encodes I10. **Never use it.**

**2. `first_ascvd` is not MACE.** 93.4% accounted for by `first_other_ihd` alone;
the MI field holds 1,293 people and stroke 321, of 501,936. **Use
`ukb_outcomes`, never the master's outcome columns.**

**3. `has_hf` / `i50_event` is heart failure.** Not atherosclerotic. **Exclude
from the endpoint.** 62 of 351 carrier events were heart-failure-only.

**4. `Positive1`, not `Mutation1`.** Positive1 gives 2,405; Mutation1-present
gives 3,562. Using the wrong one changes the cohort by 1,157 people.

**5. `ascvd_combine`, not "has a dated event age".** Different risk set and
different event count.

**6. Welsh dates need `format="mixed"`.** `MeasurementDate.2` parses 3,783 values
under mixed and only 1,597 under `dayfirst=True`, with 1,417 genuine
disagreements. It feeds the censor age, so a day-first parser silently changes
the cohort from 1,159/92 to 948/82.

**7. `MtachedLDLC` is already pre-treatment.** Do **not** apply the ÷0.70 statin
back-correction to it — that double-corrects the treated majority.

**8. `on_statin_self` is populated for carriers and missing for every
non-carrier.** Any back-calculated carrier-vs-non-carrier comparison is
one-sided. Keep such comparisons symmetric and uncorrected as primary.

**9. DRAGON `eGFR` and `BMI` hold empty strings and values like `">90"`.** Parse
as text before coercing.

**10. Comparing dates:** use `a.notna() & b.notna() & (a != b)`. A bare `a != b`
counts NaT vs NaT as a difference and invents disagreements.

---

## Derivations the analysis needs

| Quantity | Rule |
|---|---|
| Untreated lipid | Divide by 0.70 where on treatment — **except** `MtachedLDLC` |
| Cumulative non-HDL-C | `log((TC − HDL) × age)`, on the untreated scale |
| TG/HDL-C | `log(TG / HDL)` |
| Hypertension | BP medication **or** SBP ≥140 **or** DBP ≥90 |
| Endpoint | `i21 | i25 | i63 | i70 | i73 | g45` — **I50 excluded** |
| Prevalent | event date ≤ baseline → **exclude** |
| Incident | event date > baseline |
| Undated case | atherosclerosis-positive, no usable date → **exclude**, not a non-case |
| Welsh exit | event age for cases, else `AGE_AT_DECEASED` or last contact |

---

## Reference counts — your code must reproduce these

| | Value |
|---|---|
| UK Biobank carriers | 3,540 |
| Prevalent excluded | 207 |
| Undated excluded | 124 |
| Risk set | 3,209 |
| Events — 5 y / 10 y / full | 97 / 194 / 289 |
| Welsh genotype-positive | 2,405 |
| Welsh risk set / events | 1,159 / 92 |
| DRAGON matched into Wales | 424 / 424 |

**If your code produces different numbers, your code is wrong** — or you have
found something, in which case file an objection saying which number and why.

## Known limitations to carry, not fix

Event-date completeness: I21 100%, I25 100%, I63 40.9%, I70 64.3%, I73 52.8%,
G45 37.0%. The endpoint is coronary-weighted; the dates cannot be recovered.

The UK Biobank cohort is **LDLR variant carriers, not FH** — untreated LDL-C
excess +0.15 to +0.23 mmol/L median, ~1–2% above 6.5 mmol/L, `variant_id` empty
in all 501,936 rows, and high-confidence loss-of-function carriers show no
stronger phenotype. Write "LDLR variant carriers" throughout.

Wales cannot resolve concordance differences below roughly 0.15. Ties there are
a power statement, not equivalence.
