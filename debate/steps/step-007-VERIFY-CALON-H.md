# Step 007 — Verify CALON-H. Agree or refute.

You are one voice on a four-model panel (Claude, Codex, Kimi, Grok). Round 1 is
blind. **A model has been built and run.** Your job is not to design it — it exists.
Your job is to decide, independently, whether the result is real.

**Default posture: assume it is wrong.** Three models in this programme have already
been retracted after looking exactly this good. Two were killed by a treatment leak,
one by a post-event lipid field. A fourth would be worse than a null result.

You have no data access. You are given the complete specification, the complete code
path, every number produced, and the raw column names. Verify by reasoning and by
writing checkable tests — never by requesting an extract.

---

## 1. WHAT WAS BUILT

`code/30_CALON_H.py`, run 16 August 2026. Seed 20260816. Cox PH, ridge penalty 0.02,
10 folds × 10 genuinely re-randomised repeats, family-clustered, out-of-fold linear
predictor. Paired cluster bootstrap B = 2,000.

**Specification, frozen before fitting:**

```text
age, sp50, male, htn, dm, smoke, cum_nonhdl, log_tghdl, remnant_chol
```

**Excluded by investigator decision, not by data:**

| Excluded | Why |
|---|---|
| statin / any treatment flag as a **predictor** | Retracted two prior models. Audit R8: the term alone discriminates at C 0.510 in Wales; the retraction proved HR 2.15 was entirely undated post-event recording |
| Lp(a) | Welsh assay is a different scale at 1.8–7.9% coverage — including it makes external validation impossible |
| apoB | absent from Wales entirely |
| any published score or derived linear predictor | binding programme rule; comparators are scored, never fitted |

Treatment enters **only** as the ÷0.70 back-correction producing untreated non-HDL-C,
using **dated** fields in both cohorts (`on_statin_self` at UKB baseline;
`Treatmentdate1 ≤ MeasurementDate.1` in Wales — *not* the undated `OnTreatment`).
FH-Risk-Score does the same thing, so this is symmetric with the comparators.

**Term constructions** (exact, from raw columns):

| Term | Construction |
|---|---|
| `age` | `age_exact_baseline` (UKB) / age at `MeasurementDate.1` (Wales) |
| `sp50` | `max(age − 50, 0)` |
| `male` | `1 − sex_F` / `Gender` starts "M" |
| `htn` | BP medication **or** SBP ≥ 140 **or** DBP ≥ 90 |
| `dm` | `diabetes_combined` / `Diabetes` ∈ {0,1} |
| `smoke` | `smoking_current` → `smoking_ever` fallback / `Smoking` ∈ {0,1} |
| `cum_nonhdl` | `log((TC − HDL)_untreated × age)`, non-HDL clipped to (0.3, 20) |
| `log_tghdl` | `log(TG / HDL)` where ratio > 0 |
| `remnant_chol` | `TC − HDL − LDL`, clipped to (−1, 6) |

## 2. GATES — all seven passed

| Gate | Required | Produced |
|---|---|---|
| LDLR carriers | 3,540 | **3,540** |
| Prevalent ASCVD excluded | 207 | **207** |
| Undated atherosclerotic excluded | 124 | **124** |
| Frozen risk set | 3,209 | **3,209** |
| Events, full follow-up | 289 | **289** |
| Events, 5 y | 97 | **97** |
| Events, 10 y | 194 | **194** |

Endpoint `I21|I25|I63|I70|I73|G45`; **I50 heart failure excluded**. Prevalent = event
date ≤ baseline. Undated atherosclerotic cases **excluded**, not counted as controls.

Horizon mask: `E_h = (E==1) & (T<=H)`, `T_h = min(T,H)`. The withdrawn form
`(T<=H)|(E==1)` returned 146 five-year events against 97.

Wales: risk set 1,159, events 92 full / 44 at 5 y / 66 at 10 y. Cox convergence
failures: **0** in all six cohort × horizon fits.

## 3. COMPARATOR UNIT TEST — passed against the paper's own worked examples

SAFEHEART-RE implemented as published (Circulation 2017;135:2139–40):
`risk = 1 − S0^exp(Σβx − 5.4078)`, S0(5y) = 0.9532, S0(10y) = 0.9025.

| Published case | Paper | Produced |
|---|---|---|
| Case 1, 5 y | 0.02% | **0.0215%** |
| Case 1, 10 y | 0.05% | **0.0460%** |
| Case 2, 5 y | 38.1% | **38.067%** |
| Case 2, 10 y | 64.15% | **64.137%** |

The script **aborts before scoring anything** if this test fails. The previous local
implementation (`code/15_CALON_FINAL.py:278`) cannot pass it — it is a continuous
linear form in mmol/L with invented weights, no centring and no baseline survival.

FH-RS scored from the ATVB 2021 Table 3 chart (points = 10 × β). Montreal from the
J Clin Lipidol 2017 Table 3 integer chart.

## 4. RESULTS

**Discrimination (out-of-fold, family-clustered):**

| | UK Biobank | Wales |
|---|---|---|
| full follow-up | **0.7065** (n 3,209 / 289 ev) | **0.7527** (n 1,159 / 92 ev) |
| 10 year | 0.7036 (194 ev) | 0.7522 (66 ev) |
| 5 year | **0.7217** (97 ev) | 0.7441 (44 ev) |

**Head-to-head.** Δ = C(model) − C(comparator), paired cluster bootstrap B = 2,000,
computed on each comparator's own evaluable set. `floor` = 1.96 × bootstrap SE, i.e.
the minimum detectable difference at the **measured** ρ, not an assumed one.

*UK Biobank*

| Horizon | Comparator | n_eval | ev | C_comp | Δ | 95% CI | ρ | floor | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| full | SAFEHEART-RE | 3,209 | 289 | 0.6576 | +0.0489 | 0.0232, 0.0765 | 0.707 | 0.027 | **WIN** |
| full | FH-Risk-Score | 2,808 | 252 | 0.6869 | +0.0182 | −0.0019, 0.0371 | 0.845 | 0.020 | TIE |
| full | Montreal | 2,811 | 252 | 0.6698 | +0.0356 | 0.0152, 0.0563 | 0.852 | 0.021 | **WIN** |
| full | age + sex | 3,209 | 289 | 0.6675 | +0.0390 | 0.0194, 0.0595 | 0.820 | 0.020 | **WIN** |
| 10y | SAFEHEART-RE | 3,209 | 194 | 0.6506 | +0.0530 | 0.0201, 0.0885 | 0.700 | 0.034 | **WIN** |
| 10y | FH-Risk-Score | 2,808 | 172 | 0.6853 | +0.0182 | −0.0059, 0.0419 | 0.855 | 0.024 | TIE |
| 10y | Montreal | 2,811 | 172 | 0.6668 | +0.0369 | 0.0110, 0.0639 | 0.849 | 0.026 | **WIN** |
| 10y | age + sex | 3,209 | 194 | 0.6664 | +0.0372 | 0.0129, 0.0624 | 0.818 | 0.025 | **WIN** |
| 5y | SAFEHEART-RE | 3,209 | 97 | 0.6481 | +0.0736 | 0.0227, 0.1281 | 0.675 | 0.053 | **WIN** |
| 5y | FH-Risk-Score | 2,808 | 84 | 0.6928 | +0.0200 | −0.0206, 0.0587 | 0.810 | 0.040 | TIE |
| 5y | Montreal | 2,811 | 84 | 0.6671 | +0.0458 | 0.0035, 0.0900 | 0.809 | 0.044 | **WIN** |
| 5y | age + sex | 3,209 | 97 | 0.6513 | +0.0704 | 0.0284, 0.1097 | 0.741 | 0.042 | **WIN** |

*Wales*

| Horizon | Comparator | n_eval | ev | C_comp | Δ | 95% CI | ρ | floor | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| full | SAFEHEART-RE | 853 | 80 | 0.6510 | +0.0924 | 0.0431, 0.1414 | 0.772 | 0.049 | **WIN** |
| full | FH-Risk-Score | 734 | 54 | 0.7468 | +0.0330 | −0.0010, 0.0648 | 0.905 | 0.033 | TIE |
| full | Montreal | 746 | 56 | 0.7458 | +0.0335 | −0.0095, 0.0823 | 0.861 | 0.047 | TIE |
| full | age + sex | 1,159 | 92 | 0.7036 | +0.0490 | 0.0117, 0.0872 | 0.859 | 0.038 | **WIN** |
| 10y | SAFEHEART-RE | 853 | 57 | 0.6525 | +0.0910 | 0.0375, 0.1455 | 0.768 | 0.054 | **WIN** |
| 10y | FH-Risk-Score | 734 | 41 | 0.7466 | +0.0283 | −0.0078, 0.0602 | 0.902 | 0.034 | TIE |
| 10y | Montreal | 746 | 42 | 0.7440 | +0.0310 | −0.0158, 0.0832 | 0.862 | 0.050 | TIE |
| 10y | age + sex | 1,159 | 66 | 0.7039 | +0.0484 | 0.0056, 0.0909 | 0.855 | 0.043 | **WIN** |
| 5y | SAFEHEART-RE | 853 | 39 | 0.6347 | +0.0861 | 0.0193, 0.1527 | 0.742 | 0.067 | **WIN** |
| 5y | FH-Risk-Score | 734 | 29 | 0.7394 | +0.0109 | −0.0355, 0.0566 | 0.885 | 0.045 | TIE |
| 5y | Montreal | 746 | 29 | 0.7403 | +0.0084 | −0.0448, 0.0586 | 0.861 | 0.052 | TIE |
| 5y | age + sex | 1,159 | 44 | 0.6969 | +0.0472 | 0.0041, 0.0925 | 0.829 | 0.045 | **WIN** |

**Tally: 15 WIN / 9 TIE / 0 LOSS.**

**External transport, no refitting:**

| Development | Validation | C |
|---|---|---|
| UK Biobank (9 terms) | Wales (n 1,159, 92 ev) | **0.7310** |
| Wales (7 terms) | UK Biobank (n 3,209, 289 ev) | **0.6770** |

## 5. WHAT CHANGED VERSUS EVERY PRIOR ATTEMPT

| | Prior | CALON-H |
|---|---|---|
| UKB C, full | 0.6428 (`M12_FAITHFUL.json`) | **0.7065** |
| **UKB 5-y** | **0.6149 — LOST to FH-RS 0.6528** | **0.7217 — TIE, positive point estimate** |
| Wales, FH-RS design | 0.7465 vs FH-RS **0.7642 — LOSS −0.018** | 0.7527 vs 0.7468 — **TIE +0.033** |
| Treatment flag | in the model | **removed** |
| SAFEHEART equation | invented, continuous, mmol/L | **published, categorical, unit-tested** |
| 5-year risk set | 146 events (mask bug) | **97 events** |

## 6. DEFECTS THE ANALYST DECLARES AGAINST HIMSELF

Do not treat this list as exhaustive. Find more.

1. **`C_model` and `delta` are different estimators.** The `C_model` column is computed
   on the full cohort; `delta` is computed on each comparator's evaluable set. For UKB
   full vs FH-RS: 0.7065 − 0.6869 = 0.0196, but the reported Δ is 0.0182. They do not
   subtract. This is the same OBJ-028 two-estimator defect Codex found in the previous
   pipeline. **The deltas are the correct paired quantity; the `C_model` column must be
   restated per evaluable set.**
2. **The Welsh model is 7 terms, not 9.** `dm` and `smoke` are dropped there by the
   minimum-information rule (<10 events in one level). **So the Welsh result is a
   7-term model beating comparators that all use smoking.** Is that a strength (wins
   with less) or a fairness problem (different model in each cohort)? Decide.
3. **Welsh `Smoking`, `Diabetes` and `BloodPressureMedication` are undated status
   fields.** The 8 August retraction quantified the severity: BP record post-dates the
   event in 55/69 (80%) of dated cases. This contaminates **the comparators too** —
   all three need smoking and hypertension — so the head-to-head is symmetric, but the
   Welsh numbers are not a clean external validation. No dated-fields-only frame has
   been run.
4. **The specification was not chosen blind.** `remnant_chol` and `log_tghdl` were
   selected knowing from prior work that no comparator contains them. That is
   literature reverse-engineering, which the Cycle-2 protocol permits — but the
   selection is not free of the programme's accumulated knowledge and must be disclosed.
5. **No calibration is reported.** No E:O, no calibration slope, no decision curve,
   no ascertainment-stratified baselines. Discrimination alone is not a prediction
   model. `M06_CALON_A_FINAL.json` shows stratified baselines achieve E:O 1.011 where
   the pooled model runs E:O 0.36–3.82; that has not been redone here.
6. **Multiplicity.** 24 reported cells. No pre-declared primary family, no Holm
   adjustment. At α = 0.05, ~1 spurious WIN is expected.
7. **Welsh complete-case attrition.** 999 of 1,159 (86.2%) have all three lipid terms,
   carrying 61 of 92 events. Fold-wise median imputation fills the rest.
8. **Lp(a) is filled to the low-risk group** for SAFEHEART and FH-RS where missing
   (all of Wales, ~22% of UKB). This handicaps both comparators by up to 4 FH-RS chart
   points and β 0.42 in SAFEHEART.
9. **The endpoint is coronary-weighted.** Date completeness: I21 100%, I25 100%,
   I63 40.9%, I70 64.3%, I73 52.8%, G45 37.0%.
10. **UK Biobank LDLR carriers are not clinically ascertained FH** — untreated LDL-C
    excess is +0.15 to +0.23 mmol/L median, ~1–2% above 6.5 mmol/L.

## 7. WHAT YOU MUST DECIDE — answer each explicitly

1. **Is the 15/9/0 tally real, or is there a leak?** Name the single most likely
   leak given that no treatment flag is present, and the test that would expose it.
2. **Does defect 2 (7 terms in Wales) invalidate the Welsh WINs, strengthen them, or
   neither?**
3. **Is `remnant_chol` genuinely adding information, or is it re-encoding
   `cum_nonhdl`?** Both derive from TC, HDL, LDL. State the expected correlation and
   the ablation that settles it.
4. **FH-Risk-Score ties in all six cells** with lower bounds of −0.0019 and −0.0010.
   Is there any legitimate analysis that converts those to WINs, or is the honest
   answer permanently TIE? **Do not propose adding a term.**
5. **What is the pre-declared primary family**, and what does the tally become after
   multiplicity adjustment?
6. **Is the Welsh result external validation, or internal validation in a second
   cohort?** Defect 3 bears on this.

## 8. RULES

- Effect size + 95% CI + absolute risk. A positive point estimate whose interval
  crosses zero is a **TIE**. Label it one.
- Any stratum under 10 events is `<10, non-estimable`.
- Do **not** propose adding Lp(a), apoB, or any treatment flag. Those are closed by
  investigator decision.
- Do **not** propose adding a term after seeing this matrix. That is the
  outcome-informed selection already on the Cycle-1 record.
- Never invent a citation, coefficient or published performance figure.
- Aggregate output only.
- If you cannot verify something, say so. Do not substitute a weaker check silently.

## 9. ARTEFACTS

| Path | Contents |
|---|---|
| `code/30_CALON_H.py` | The whole analysis, self-contained |
| `outputs/calon_h.json` | Ledgers, gates, unit test, terms, transport |
| `outputs/calon_h_headtohead.csv` | All 24 cells |
| `debate/NEXT_DIRECTIONS.md` | Why this specification |
| `CALON_FH_PROGRAMME_2026-08-09/05_reports/` | The two prior independent audits and the retraction — read the retraction before you accept any Welsh number |

## 10. DELIVERABLE

All four lenses under their own headings — **1. Methodology · 2. Implementation ·
3. Adversarial audit · 4. Clinical and publication reality** — then your answer to
each of the six questions in §7, one sentence each.

**End with one line: AGREE, AGREE WITH CONDITIONS, or REFUTE — and the single
finding that most nearly changed your verdict.**

File disagreements as `objection` blocks. An objection whose `settled_by` is not a
runnable test will be rejected by `consensus.mjs`.
