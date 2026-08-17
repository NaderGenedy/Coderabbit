# Step 008 — Verify CALON-C. Agree or refute.

**Supersedes step-007 (CALON-H), which is withdrawn.** An independent adversarial
audit of CALON-H reproduced every number and then dismantled the interpretation.
CALON-C is the rebuild. Your job is to decide whether it survives the same
treatment.

You are one voice on a four-model panel (Claude, Codex, Kimi, Grok). Round 1 is
blind; there will be **one exchange round only**. Say everything that matters in
your first turn.

**Default posture: assume it is wrong.** Four models in this programme have been
retracted after looking this good. Two died of a treatment leak, one of a
post-event lipid field, one of comparator misscoring. A fifth would be worse than
a null result.

You have no data access. You are given the complete specification, every column
name, every number, the full source with SHA-256, and a list of the analyst's own
errors. Verify by reasoning and by naming runnable tests — never by requesting an
extract.

---

## 1. WHAT CHANGED FROM CALON-H, AND WHY

The audit's central finding was **D1**: when comparators were refitted on their
own variable sets in the same data, 11 of 12 comparisons collapsed to TIEs and
all six SAFEHEART wins died. Three fixes were made:

1. **Every lipid-derived term is now on the untreated scale.** In CALON-H,
   `remnant_chol` and `log_tghdl` were raw *treated* values for 24.7% of UK
   Biobank and 7.1% of Wales, while the docstring claimed otherwise. That claim
   was false and the audit caught it (D6a).
2. **`log(TG/HDL)` replaced by the Triglyceride Filter**
   `log(LDL_untreated / (TG_untreated + 0.1))` — from the investigator's own
   published model (TUDOR, JCLINLIPID-D-25-01142_R2, Table 4).
3. **Comparator missing-input policy** is now strict `NOT_EVALUABLE` rather than
   silent reference-category filling (D5), with a labelled Lp(a)-omitted
   sensitivity.

## 2. SPECIFICATION

```text
PRIMARY:      age, sp50, male, htn, dm, smoke, cum_nonhdl, tg_filter, remnant_unt
SENSITIVITY:  age, sp50, male, cum_nonhdl, tg_filter, remnant_unt   (dated fields only)
```

Cox PH, ridge 0.02, 10 folds × 10 re-randomised repeats, family-clustered,
out-of-fold LP, paired cluster bootstrap B = 2,000. Seed 20260816.

**Excluded by investigator decision:** any statin/treatment flag as a predictor;
Lp(a) and apoB as model terms; any published score or derived linear predictor.
Full methods and column-level provenance: `outputs/METHODS_CALON_C.md`.

**`htn`, `dm`, `smoke` are RETAINED** — chronic conditions that precede events,
and all three comparators carry hypertension and smoking as baseline covariates.
Removing them costs **−0.0334** in UK Biobank. Do not propose removing them; that
question is closed. Index-event bias is bounded and reported (§6).

## 3. GATES — all pass

3,540 carriers · 207 prevalent excluded · 124 undated excluded · 3,209 risk set ·
289 / 97 / 194 events. Wales: `Positive1` 2,405 → 1,159, events 92 / 44 / 66,
711 families. Cox convergence failures: 0.

Horizon mask `E_h = (E==1) & (T<=H)`, `T_h = min(T,H)`; returns exactly 97 / 194.

**SAFEHEART unit test passes against its own published worked examples** —
0.0215% / 0.0460% / 38.067% / 64.137% against 0.02% / 0.05% / 38.1% / 64.15%.
The script aborts before scoring anything if it fails.

## 4. DISCRIMINATION — two independent estimators

| Cohort | Horizon | EPV | Corrected | Out-of-fold |
|---|---|---|---|---|
| UK Biobank | full | 32.1 | **0.7095** | 0.7081 |
| UK Biobank | 10y | 21.6 | **0.7079** | 0.7043 |
| UK Biobank | 5y | 10.8 | **0.7336** | 0.7254 |
| Wales | full | 13.1 | **0.7653** | 0.7565 |
| Wales | 10y | 9.4 | **0.7605** | 0.7552 |
| Wales | 5y | 6.3 | **0.7590** | 0.7504 |

"Corrected" = apparent minus Harrell bootstrap optimism, 100 resamples — the
identical procedure SAFEHEART (0.003) and FH-RS (0.002) applied to themselves.
Ours is 0.006–0.023, scaling with EPV. Welsh optimism uses a family-cluster
bootstrap. The two estimators agree within 0.008 in all twelve arms.

## 5. HEAD-TO-HEAD

**Published equations, strict Lp(a) — 4 WIN / 8 TIE**

| Cohort | Horizon | Comparator | n | ev | Δ (95% CI) | |
|---|---|---|---|---|---|---|
| UKB | full | SAFEHEART-RE | 2,470 | 221 | +0.032 (0.004, 0.061) | **WIN** |
| UKB | full | FH-Risk-Score | 2,282 | 207 | +0.021 (−0.001, 0.043) | TIE |
| UKB | full | Montreal | 2,811 | 252 | +0.033 (0.012, 0.056) | **WIN** |
| UKB | 5y | Montreal | 2,811 | 84 | +0.047 (0.006, 0.092) | **WIN** |
| Wales | full | Montreal | 746 | 56 | +0.032 (−0.016, 0.090) | TIE |
| Wales | all | SAFEHEART-RE | **40** | **1** | — | **not estimable** |
| Wales | all | FH-Risk-Score | **133** | **6** | — | **not estimable** |

**Refit variable sets — the audit's decisive test — 15 WIN / 9 TIE / 0 LOSS**

| Cohort | Horizon | vs SAFEHEART | vs FH-RS | vs Montreal | vs age+sex |
|---|---|---|---|---|---|
| UKB | full | **+0.014 W** | **+0.015 W** | **+0.019 W** | **+0.041 W** |
| UKB | 10y | +0.017 T | **+0.022 W** | **+0.022 W** | **+0.038 W** |
| UKB | 5y | **+0.029 W** | +0.028 T | +0.026 T | **+0.074 W** |
| Wales | full | +0.019 T | +0.015 T | +0.014 T | **+0.053 W** |
| Wales | 10y | **+0.020 W** | +0.016 T | +0.014 T | **+0.051 W** |
| Wales | 5y | **+0.031 W** | **+0.029 W** | +0.023 T | **+0.054 W** |

ρ runs 0.91–0.96. **CALON-H failed this test; CALON-C passes it.**

**Transport (frozen equation, no refitting):** UKB → Wales **0.7252**;
Wales → UKB **0.6600**. Verified by a third independent implementation using
explicit β·X (agreement 3×10⁻⁵).

## 5b. CALIBRATION AND NET BENEFIT

Absolute risk from the Breslow baseline of a Cox model on the **out-of-fold** LP.
Observed risk by Kaplan–Meier. E:O interval from a 500-draw family-cluster
bootstrap. No recalibration, no ascertainment-stratified baseline.

| Arm | Slope (95% CI) | E:O (95% CI) | Pred | Obs | Scaled Brier |
|---|---|---|---|---|---|
| UKB 5y | 1.197 (0.900, 1.494) | **1.004** (0.832, 1.235) | 3.06% | 3.05% | +1.8% |
| UKB 10y | 1.101 (0.884, 1.318) | **1.008** (0.883, 1.153) | 6.20% | 6.15% | +3.3% |
| Wales 5y | 1.442 (0.888, 1.996) | **0.975** (0.757, 1.324) | 5.27% | 5.40% | +2.3% |
| Wales 10y | 1.341 (0.966, 1.717) | **0.914** (0.725, 1.225) | 10.12% | 11.08% | +6.6% |

Slope and E:O both include 1.0 in all four primary arms. An earlier model in this
programme ran E:O 0.36–3.82 across four populations (`M10_EXTERNAL.json`) and
needed stratified baselines; this one calibrates as fitted.

**Decision curves**, thresholds pre-declared at 2/5/7.5/10/15/20%. Model beats
both treat-all and treat-none at 2–15% (UKB 10y), 5–20% (Wales 10y) and 2–10%
(both 5y arms). At the conventional 10% ten-year threshold: UKB **+0.0080** vs
treat-all **−0.0428**; Wales **+0.0475** vs **+0.0120**.

**Attack this.** The E:O results are the most favourable numbers in the analysis
and the least externally checked. Specific questions: does using the out-of-fold
LP to fit the Breslow baseline leak, given the same data supplies both the LP and
the baseline? Is a scaled Brier of +1.8% meaningful or is it noise? Does the
censoring-aware net benefit handle informative censoring in Wales, where 1,118 of
1,159 are censored at last clinic contact?

## 6. LP(a) PROVENANCE — resolved against raw data

DRAGON `Lpa` is **nmol/L**. Confirmed two ways: the paired median ratio to the
WALES column is **4.652** against the exact nmol/L→mg/L conversion 10/2.15 =
**4.651**; and 32.6% exceed 105 nmol/L (=50 mg/dL), matching the 20–30% reported
for FH, whereas reading it as mg/dL gives an implausible 47.3%.

**WALES `Lpa.1–4` is mixed units** — paired ratios bimodal at 1.00 and 4.65, no
per-row label — and is not used.

**Lp(a) was not the barrier to Welsh evaluation.** It covers 191 participants and
14 events. The barrier is the *conjunction*: FH-RS additionally needs HDL,
untreated LDL, hypertension and smoking (→133, 6 events); SAFEHEART needs all of
that plus BMI (→40, 1 event). Montreal, requiring neither Lp(a) nor LDL-C, is
evaluable in 746 with 56 events.

## 7. INDEX-EVENT BIAS — bounded, not assumed

Of 92 Welsh events, **55 (59.8%) have BP dated after the event**; only 94 of
1,159 have BP dated on or before baseline; `BloodPressureMedication` has no date
column. Removing all undated fields costs **0.030** in Wales.

Isolated singly, `htn` contributes **+0.030 in Wales** against **+0.013 to
+0.036 in UK Biobank**, where it is baseline-measured. The Welsh value sits
inside the clean range, so its magnitude is not anomalous — but the ratio is
~2× at the long horizons and the Welsh contribution is oddly flat across horizons
(0.030 / 0.029 / 0.028) where UK Biobank's varies 2.7-fold. **Attack this if you
can.**

## 8. THE ANALYST'S OWN ERRORS, DECLARED

Not exhaustive. Find more.

1. Claimed the refit estimand "produced zero rows" — it was a truncated
   diagnostic (`head -90`), not a defect. 24 rows existed.
2. Claimed the transport disagreed with a prior run and both numbers were
   unusable — the prior run (CALON-H2) was the wrong one; CALON-C verified.
3. Claimed S1 "recodes events as non-events instead of censoring" — false; the
   original was correct, because follow-up already ends at the event date.
4. Set Welsh Lp(a) to `NaN` on an inherited comment without checking; the
   investigator corrected this.
5. Predicted cluster bootstrap would raise Welsh optimism; it lowered it.
6. Asserted the Welsh `htn` contribution was inflated relative to UK Biobank
   before the horizon-matched comparison was available; it isn't, cleanly.

## 9. WHAT YOU MUST DECIDE — answer each explicitly

1. **Is 15/9/0 real, or is there a leak?** No treatment flag is present. Name the
   most likely remaining leak and the test that exposes it.
2. **Is `remnant_unt` re-encoding `cum_nonhdl`?** Both derive from TC, HDL, LDL.
   State the expected correlation and the ablation that settles it.
3. **Is `tg_filter` legitimate?** It comes from the investigator's own published
   model. Does importing a construct from a prior paper by the same group breach
   the "no prior model as input" rule, or is a *variable definition* categorically
   different from a *fitted linear predictor*?
4. **Wales full follow-up is 3 TIEs on the refit estimand; Wales 5y is 2 WINs.**
   Is the horizon-dependence mechanistic (§7 of `PRESPEC_HORIZON.md`) or noise at
   44 events, EPV 6.3?
5. **Does the strict/Lp(a)-omitted duality favour the model?** Under strict rules
   the model wins 4 cells; under the relaxed rule 7. Is reporting both honest, or
   is it two chances at the same claim?
6. **What survives multiplicity?** 24 reported cells, 6 pre-declared confirmatory.

## 10. RULES

- Effect size + 95% CI + absolute risk. A positive point estimate whose interval
  crosses zero is a **TIE**.
- Any stratum under 10 events is `<10, non-estimable`.
- Do **not** propose adding Lp(a), apoB, a treatment flag, or removing
  `htn`/`dm`/`smoke`. Those are closed by investigator decision.
- Do **not** propose adding any term after seeing this matrix.
- Never invent a citation, coefficient or published performance figure.
- Aggregate output only.

## 11. ARTEFACTS

| Path | Contents |
|---|---|
| `outputs/METHODS_CALON_C.md` | Full methods, exact columns, justifications, complete source with SHA-256 |
| `outputs/RESULTS_SUMMARY_2026-08-16.md` | Every result in one place |
| `outputs/PRESPEC_HORIZON.md` | Horizon pre-specification and its evidence |
| `outputs/calon_c_headtohead.csv` | All 60 head-to-head rows |
| `outputs/calon_apparent.json` | Apparent / optimism / corrected, 12 arms |
| `outputs/calon_c_calibration.csv` | Calibration slope, E:O, scaled Brier, deciles |
| `outputs/calon_c_dca.csv` | Net benefit at six pre-specified thresholds |
| `CALON_FH_PROGRAMME_2026-08-09/05_reports/` | The two prior independent audits and the retraction — **read the retraction before accepting any Welsh number** |

## 12. DELIVERABLE

All four lenses under their own headings — **1. Methodology · 2. Implementation ·
3. Adversarial audit · 4. Clinical and publication reality** — then your answer to
each of the six questions in §9, one sentence each.

**End with one line: AGREE, AGREE WITH CONDITIONS, or REFUTE — and the single
finding that most nearly changed your verdict.**

File disagreements as `objection` blocks. An objection whose `settled_by` is not
a runnable test will be rejected by `consensus.mjs`.
