# Step 004 · Round 1 · Claude

**CALON-G — Cycle-2 pre-specified model protocol.** Written before any fit. No performance claim is made anywhere in this document.

Three things happened while writing this that change the inputs I was given, and I state them up front because they alter the protocol rather than decorate it:

1. **All three comparator PDFs are on disk, including Montreal (both papers).** `comparator_provenance.csv` records Montreal as `pdf_present=False`, `source_pinpoint=UNOBTAINABLE`. That row is stale. I have read the points chart.
2. **I reconstructed and arithmetically verified the full SAFEHEART-RE equation from the source text, including four published worked-example test vectors.** It is no longer a candidate implementation pending verification; it is verifiable today against exact published numbers.
3. **The withdrawn 5-year rows are worse than "an invalid mask".** In `headtohead_full.csv` every 5-year cell carries *exactly* the full-follow-up event count (ALL: n=163, events=146 — an 89.6% event rate). The mask did not merely leak late events; it produced a case-only set. That is the mechanical reason every 5-year C-index in that file sits at ≈0.55, and it has a consequence for what Cycle-2 can deliver at 5 years (§4).

I verified one thing that could have sunk everything and did not: `00_governance_header.py:15` and `01_cohort_ledger_ukb.py:22–26` build the ledger from `corrected_ascvd_outcomes` / `ascvd_first_date_best`, **not** from `prevalent_ascvd`. The frozen cohort is not running on the 31%-under-ascertained endpoint documented in the project record.

---

## 1. Methodology

### 1.1 The primary formula

**CALON-G (primary) — Cox proportional hazards, ridge-penalised, 9 degrees of freedom:**

```
h(t | X) = h₀(t) · exp(
    β₁·rcs₁(age; knots 50, 58, 65)
  + β₂·rcs₂(age; knots 50, 58, 65)
  + β₃·male
  + β₄·smoke_curr
  + β₅·htn_med
  + β₆·dm
  + β₇·log(TG/HDL)
  + β₈·cum_nonhdl            [ = log(non-HDL_untreated × age) ]
  + β₉·lpa_hi                [ = 1 if Lp(a) ≥ 125 nmol/L, native UKB units ]
)
```

Estimand: hazard of first incident permitted-ASCVD event (`i21|i25|i63|i70|i73|g45`; I50 excluded) from baseline, in LDLR variant carriers free of prevalent ASCVD. The model **identifies** carriers at higher event rate. It does not establish that any term causes events.

### 1.2 Why each term stays or goes

| Term | df | Stays / goes | Reason |
|---|---|---|---|
| `rcs(age, 3 knots @ 50/58/65)` | 2 | **Stays** | Age is the dominant predictor (HR 1.055 [1.037–1.072] alone, `obj003_collinearity.json` fit D). Knots are **pre-specified clinical values, not percentiles** — nothing is learned, so the transform is identical in every fold and immune to the fold-leakage rule. |
| *`age_sp18` (the programme's existing "spike")* | — | **Goes — cannot be transported** | `code/12_welsh_prospective_model.py:96` defines `age_sp18 = max(age − 18, 0)`. UK Biobank's minimum baseline age is ~40, so the clip never binds and `age_sp18 ≡ age − 18`: correlation with age exactly 1.000. Carrying the Welsh spike into UKB would insert a perfectly collinear duplicate. This is precisely the r≈1 case the 0.999 rule was written for — and it is the one term that would have tripped it. |
| `male` | 1 | **Stays** | In the exploratory frame, 93 events/828 men vs 53/1,076 women. All three comparators carry sex (SAFEHEART β=0.70; Montreal 3 points; FH-RS 7 points). Omitting it would be a self-inflicted handicap. |
| `smoke_curr` | 1 | **Stays** | In all three comparators. Definition deliberately *narrower* than Montreal's (see §2.2). |
| `htn_med` | 1 | **Stays** | Investigator-specified. Antihypertensive medication is a durable dated field; single-visit SBP is one measurement with heavy regression to the mean. An ICD-derived alternative would risk touching p131286, whose label/content mismatch is documented in the project record. |
| `dm` | 1 | **Stays** | Type 2 diabetes. Note honestly: it was **not** an independent multivariable predictor in either derivation cohort (SAFEHEART Table 3 univariable HR 3.45, dropped from the multivariable model; FH-RS Table 2 univariable HR 1.64, p=0.054, dropped). CALON-G retains it on prior clinical grounds and because UKB has substantially more diabetes than a lipid-clinic FH registry. If it earns nothing, that must be reported, not quietly dropped. |
| `log(TG/HDL)` | 1 | **Stays** | The metabolic/insulin-resistance axis, orthogonal to the LDL-burden path. Justified by the programme's own T16 finding that remnant mediation explains only 11% — remnants do *not* work through the cumulative-cholesterol term, so this is added information rather than a second lipid path. |
| `cum_nonhdl` | 1 | **Stays — the single permitted lipid-burden path** | Chosen over apoB/HDL for the primary because it is the term already frozen in `spec_frozen.json`, is defined in existing code (`code/14:101–103`), and is the only one carrying a *duration* component. |
| `lpa_hi` | 1 | **Stays, with a frozen native-unit policy** | See §1.4. |
| **apoB/HDL** | — | **Goes to sensitivity** | Constraint 1. Declared sensitivity below. |
| **Any interaction** | 0 | **Goes** | With 289 development events, interactions are the standard route to optimism. Subgroup performance is **evaluated**, never fitted. |
| **Statin / treatment status as a predictor** | 0 | **Goes** | Not in the supplied ingredient list, and it enters through the untreated back-correction of `cum_nonhdl` instead. Including both would double-count treatment and invite the treatment paradox. |

**Total: 9 df.** Events-per-parameter at full follow-up in the frozen cohort = 289/9 = 32.1.

### 1.3 The single sensitivity formula

**CALON-G-B:** identical in every respect, with `cum_nonhdl` replaced by `log(apoB/HDL)`. Same 9 df, same folds, same seeds, same penalty grid. Reported alongside the primary in every cell it is run in. It is a sensitivity, not a second entrant: it cannot be promoted to primary after seeing results.

That is the only alternative formula in this protocol. Two preprocessing *constants* carry declared robustness reruns (§2.2); a constant rerun is not a new model and cannot replace the primary whatever it shows.

### 1.4 Lp(a): a frozen unit policy in three layers

The critical asymmetry, which the record has not yet stated: **CALON-G's Lp(a) term needs no conversion at all.** UKB measures Lp(a) in nmol/L; a threshold in nmol/L is a modelling choice in native units. Only the *comparators* need mg/dL, because SAFEHEART and FH-RS both dichotomise at 50 mg/dL.

It also matters that **Montreal has no Lp(a) term at all** (points chart: age, HDL-C, gender, HTN, smoking — nothing else). So one fully assumption-free comparison exists.

| Layer | CALON-G Lp(a) | SAFEHEART / FH-RS | Montreal | Status |
|---|---|---|---|---|
| **L0 — strict, PDF-faithful** | ≥125 nmol/L, native | **NOT-EVALUABLE** (no mg/dL measurement exists) | Fully evaluable | **The only assumption-free cell. Reported first.** |
| **L1 — primary, declared assumption** | ≥125 nmol/L, native | 50 mg/dL → **107.5 nmol/L** under a declared 2.15 nmol/L per mg/dL factor | Fully evaluable | Named as *"declared-conversion application"*, never as *"as published"* |
| **L2 — mandatory invariance band** | ≥125 nmol/L, native | comparator cut at 100 and 125 nmol/L | Fully evaluable | Verdict must be invariant across L1/L2 or the cell is flagged conversion-sensitive |

CALON-G's own cut is **frozen at 125 nmol/L before fitting and never varied**, so no tuning is possible on this term. Note it is *stricter* than the comparators' primary cut of 107.5 — it confers no prevalence advantage.

Two further points that keep this honest:

- **The LDL mg/dL↔mmol/L conversion is a fact; the Lp(a) one is not.** SAFEHEART's LDL bands (100–159, ≥160 mg/dL) and FH-RS's mmol/L bands convert exactly by the cholesterol molar mass (×0.02586). That conversion is applied without caveat. Lp(a) mass-vs-particle-number is isoform-dependent and assay-dependent; 2.15 is a convention, not a measurement. Objecting to one while accepting the other is not unit-phobia.
- **The threshold form is deliberately chosen for fairness, not power.** A continuous log-Lp(a) term would give CALON-G a richer functional form on the one variable whose units are contested, and would additionally be distorted by the UKB assay's upper reportable limit. A binary term matches the comparators structurally.

### 1.5 Metrics, horizons and the multiplicity discipline

| | Specification |
|---|---|
| Sign convention | Δ = C(CALON-G) − C(comparator); positive favours CALON-G (inherited from `spec_frozen.json`) |
| Primary metric | Harrell's C, full follow-up — the metric both derivation papers report (SAFEHEART C=0.78; FH-RS C=0.75) |
| Co-primary | Uno's IPCW C at 5 years — administrative censoring is heavy, and Harrell's C is censoring-dependent |
| Disagreement rule | If Harrell and Uno disagree in a primary cell, **both are reported and the cell is declared indeterminate**. No selection. |
| Absolute-risk metrics | Brier / calibration only where a comparator publishes absolute risk: SAFEHEART (5 y and 10 y), FH-RS (10 y only, banded). **Montreal: ranking only** — COMP-08, now confirmed by its own text |
| **Primary confirmatory cells** | **Exactly 3**: CALON-G vs each comparator, subgroup ALL, full follow-up, layer L1. Holm-adjusted across the three. |
| All other cells | Secondary/exploratory. Full 78-cell matrix published; nothing suppressed; no cell may be quoted as confirmatory |
| Multiplicity statement (mandatory in every output) | 3 comparators × 2 horizons × 13 subgroups = 78 dependent cells. At nominal 95% coverage, **≈4 spurious "wins" are expected by chance alone**. The single Montreal female-5y WIN in the withdrawn tally is exactly the size of that expectation. |

---

## 2. Implementation

### 2.1 Fold structure and the leakage the kinship gap actually creates

Kinship/KING is unavailable (project record, T20/SPEC-FAM-01). The substitute is not a fudge, it is a *stricter* one:

**Cluster key = LDLR variant identifier (chr:pos:ref:alt).** Carriers of the same rare LDLR variant are enriched for relatedness, so the variant is a **superset of family** — clustering on it is conservative relative to true kinship, and it additionally blocks the leakage that actually threatens a carrier cohort: the same variant appearing in both training and held-out folds.

| Element | Specification |
|---|---|
| Outer CV | Grouped 5-fold, groups = variant ID, event-count balanced across folds; **10 repeats** |
| Fold guard | If any single variant cluster holds >20% of events, fall back to grouped 4-fold with that cluster held whole. Report which applied. |
| Primary C-index | Computed per repeat on that repeat's pooled out-of-fold linear predictor, then averaged over 10 repeats. **Between-repeat SD reported.** LPs are *not* averaged across repeats — that would bag the predictions and inflate performance. |
| λ selection | Nested grouped 5-fold CV of the partial log-likelihood, **inside each training fold only**. The outer fold never contributes to λ. |
| Seeds | Frozen and recorded in the results file |
| Disclosure | Family-level clustering is approximated by variant-level clustering; where a variant is carried by unrelated individuals the CIs are mildly conservative, where relatives carry different variants they are mildly anti-conservative. Stated, not hidden. |

### 2.2 Preprocessing — what is frozen, what is fold-learned

| Step | Frozen constant (identical in every fold) | Fold-learned |
|---|---|---|
| non-HDL | `TC − HDL`, valid range [0.3, 20] mmol/L | — |
| Untreated back-correction | `nonhdl_unt = nonhdl / 0.70` if on lipid-lowering therapy — the **existing project convention** (`code/14:101`, `code/15:228`) | — |
| Cumulative burden | `cum_nonhdl = log(nonhdl_unt × age)` | — |
| Age spline | RCS, knots **50, 58, 65** (clinical, pre-specified) | — |
| Lp(a) | `lpa_hi = Lp(a) ≥ 125 nmol/L` | — |
| Standardisation | — | Mean/SD of **every** design column (binaries included, so the ridge penalty is scale-equivariant), computed in the training fold and applied unchanged to the held-out fold |
| Ridge λ | — | Nested CV within training fold |

**Declared constant-robustness rerun (not a new model):** 0.70 is the LDL-C correction factor applied to non-HDL-C; the conventional total-cholesterol factor is 0.80, so the frozen convention slightly over-corrects treated participants. A single rerun at 0.80 is pre-authorised and **must be reported whatever it shows**. It cannot replace the primary.

### 2.3 Missing data — one rule, applied identically to all four models

`spec_frozen.json` leaves this as `TODO`. It is the single decision that determines whether the comparison is fair.

> **Rule: complete-case on the union of inputs required by CALON-G and all three comparators. One frozen common evaluable set. No imputation anywhere, for any model. CALON-G is developed and evaluated on that same set.**

This is deliberately the restrictive option, and it costs us:

| | |
|---|---|
| Frozen cohort | n = 3,209; 289 full / 97 five-year / 194 ten-year events |
| **Projected** common evaluable set | n ≈ 1,900; ≈146 full events (the frame size Julius reached) |
| **Projected** 5-year events in that set | ≈ 146 × (97/289) ≈ **49** |
| CALON-G EPP for development | ≈ 146/9 ≈ 16 |
| Riley (2019) criterion, p=9, assumed R²<sub>CS,app</sub>=0.06, target shrinkage 0.9 | n<sub>min</sub> ≈ 1,300 → **1,900 passes, with less margin than 3,209 would give** |

These are projections from the Julius frame, labelled as such, and they are the reason for objection OBJ-004-A.

Why complete-case rather than imputation, given it costs events: fold-internal MICE for CALON-G while comparators are scored complete-case creates exactly the asymmetry constraint 6 forbids — our model would get an information advantage on the very participants the comparators cannot score. Losing 40% of events is the price of not having that argument in peer review.

Three consequences, all pre-declared:

1. **CALON-G is not refitted at 5 years.** One model is fitted on full follow-up; 5-year absolute risk comes from the Breslow baseline S₀(5) of that same fit. With ≈49 five-year events, a refitted 5-year model would run at EPP ≈ 5.5. This also fixes Julius defect 6 (predictions imported from a different pipeline and used beyond their native horizon): here the 5-year evaluation is native to the fit.
2. **Selection must be visible.** A table comparing evaluable vs non-evaluable participants on age, sex, statin use and crude event rate ships with the results. FH-RS's >65 exclusion is *not* random with respect to risk — it removes the oldest, highest-risk participants — and that must be shown, not asserted.
3. **A declared secondary** develops CALON-G on the full 3,209 with fold-internal MICE (m=10, imputation model fitted in training folds only), solely to demonstrate that the complete-case restriction did not select a peculiar subgroup. **It never produces a head-to-head verdict.**

### 2.4 Comparator implementations — now PDF-locked

I extracted these from the source text. Every number below is transcribed, not remembered.

**SAFEHEART-RE — Circulation 2017;135:2133–2144, Table 3 (p.2139) and the worked examples immediately following.**

```
5-y risk  = 1 − 0.9532^exp(ΣβX − 5.4078)
10-y risk = 1 − 0.9025^exp(ΣβX − 5.4078)
```

| Term | β (published equation) | Multivariable HR (Table 3) | ln(HR) | Reconciles |
|---|---|---|---|---|
| Male | 0.70 | 2.01 | 0.698 | ✓ |
| Age 30–59 | 1.07 | 2.92 | 1.072 | ✓ |
| Age ≥60 | 1.45 | 4.27 | 1.452 | ✓ |
| Hypertension | 0.69 | 1.99 | 0.688 | ✓ |
| History of ASCVD | 1.42 | 4.15 | 1.423 | ✓ |
| Active smoking | 0.48 | 1.62 | 0.482 | ✓ |
| BMI 25–30 | 0.88 | 2.40 | 0.876 | ✓ |
| BMI ≥30 | 0.98 | 2.67 | 0.982 | ✓ |
| LDL 100–159 mg/dL | 0.92 | 2.50 | 0.916 | ✓ |
| LDL ≥160 mg/dL | 1.57 | 4.80 | 1.569 | ✓ |
| Lp(a) >50 mg/dL | 0.42 | 1.52 | 0.419 | ✓ |

All eleven coefficients equal ln(published HR) to rounding. **Four published test vectors** must be reproduced before the implementation may be used:

| Vector | Published | Reproduced by the locked form |
|---|---|---|
| All risk factors 0, 5 y | 0.02% | 0.0215% |
| All risk factors 0, 10 y | 0.05% | 0.046% |
| Published high-risk vector, 5 y | 38.1% | 38.07% |
| Published high-risk vector, 10 y | 64.15% | 64.14% |

The −5.4078 sits **inside** the exponent. The uncentred implementation that produced a 77% mean 5-year risk was not a defensible variant of anything; it was arithmetically wrong, and these test vectors would have caught it in one line.

`History of ASCVD` (β=1.42) is fixed at 0 for every participant. That is **not** healthy-default imputation — prevalent ASCVD is an exclusion criterion, so the value is *known* to be 0 by design. Labelled: restricted primary-prevention application (COMP-06).

**Montreal-FH-SCORE — J Clin Lipidol 2017;11(1):80–86, Table 3, p.84 (the *derivation* paper).**

| Age (y) | pts | HDL-C (mmol/L) | pts | Other | pts |
|---|---|---|---|---|---|
| ≤21 | 0 | ≤0.60 | 12 | Men | 3 |
| 22–28 | 4 | 0.61–0.90 | 9 | Women | 0 |
| 29–35 | 8 | 0.91–1.20 | 6 | HTN yes | 2 |
| 36–42 | 12 | 1.21–1.50 | 3 | HTN no | 0 |
| 43–49 | 16 | >1.50 | 0 | Smoking **ever** | 1 |
| 50–56 | 20 | | | Never | 0 |
| 57–63 | 24 | | | | |
| >63 | 28 | | | | |

Maximum 46. No Lp(a), no LDL, no diabetes. Smoking is **ever** (prior or current) — deliberately *not* harmonised to CALON-G's `smoke_curr`; each score keeps its published definition.

**FH-Risk-Score — ATVB 2021;41:2632–2640, Table 3 (chart points) and Table 4 (points → 10-y risk).**

Sex: man 7. Age: 18–30:0, 31–35:9, 36–40:14, 41–45:16, 46–50:17, 51–55:18, 56–60:20, >60:23. HDL-C (mmol/L): >1.30:0, 1.01–1.30:3, 0.85–1.00:7, <0.85:8. LDL-C (mmol/L): ≤5.50:0, 5.51–7.50:3, 7.51–8.50:7, 8.51–9.50:9, >9.50:11. Hypertension yes: 6. Active smoking yes: 6. Lp(a) ≥50 mg/dL: 4.

Three implementation facts that must be pre-specified:

- **Chart maximum is 65 points; Table 4 stops at "53–55 → >75%".** Scores of 56–65 are off-chart. Rule: **use raw points for the C-index** (monotone, so discrimination is unaffected) and the banded risk *only* for calibration, with off-chart scores assigned the >75% band and flagged.
- **Eligibility: "primary prevention FH between 18 and 65 years of age"; participants over 65 at baseline were excluded from derivation.** UKB recruits to 69, so a real slice of the cohort is outside native range → NOT-EVALUABLE per the frozen policy. Survivors are never dropped for any other reason.
- **Its LDL-C is untreated** ("untreated (57%) or imputed (43%)", Table 2 footnote), so our 0.70 back-correction is required for FH-RS scoring too — and matches its derivation.

**Variable mapping — each model keeps its own published definition:**

| Concept | CALON-G | SAFEHEART | Montreal | FH-RS |
|---|---|---|---|---|
| Hypertension | antihypertensive medication | "high blood pressure" → htn_any | "clinical diagnosis of HTN" → htn_any | "hypertension" → htn_any |
| Smoking | current | active | **ever** | active |
| Lipid | log(non-HDL<sub>unt</sub> × age) | LDL<sub>unt</sub> mg/dL bands | HDL mmol/L bands | LDL<sub>unt</sub> + HDL mmol/L bands |
| Lp(a) | ≥125 nmol/L native | >50 mg/dL (L1: 107.5 nmol/L) | — | ≥50 mg/dL (L1: 107.5 nmol/L) |

No ICD-derived hypertension definition may touch p131286 in any of the four.

### 2.5 Calibration strategy

Out-of-fold LP + training-fold Breslow S₀(H) → out-of-fold predicted risk at 5 and 10 years. Report calibration-in-the-large, calibration slope, and a flexible calibration curve (RCS of complementary log-log predicted risk), with observed risk from Kaplan–Meier within predicted-risk decile.

**No recalibration of the primary.** Any intercept- or slope-recalibrated version is a labelled secondary and must appear alongside the uncalibrated figure, never instead of it. Comparators are reported at their native calibration — that is the entire point of the SAFEHEART centring finding, and hiding a comparator's miscalibration behind a recalibration would be as dishonest as hiding our own.

### 2.6 Julius-ready fit-and-evaluate pseudocode

```python
# ============================================================================
# CALON-G — Cycle-2 fit & evaluate.  Aggregate outputs only (UKB App 1002450).
# ============================================================================
import numpy as np, pandas as pd, hashlib
from sksurv.linear_model import CoxPHSurvivalAnalysis
from sksurv.metrics import concordance_index_censored, concordance_index_ipcw
from sklearn.model_selection import GroupKFold

SEED, B, N_REPEATS, MIN_EVENTS = 20260815, 2000, 10, 10
COHORT_SHA = "8c3a1e0598770c1beefe29db28d42fb7074f233f382c25c19eb0c843b59f49b2"

# ---- GATE 1 -----------------------------------------------------------------
df = load_frozen_cohort()
assert sha256_of_frozen(df) == COHORT_SHA,  "G1 cohort hash"
assert len(df) == 3209 and int(df.event.sum()) == 289, "G1 ledger"

# ---- GATE 2 : CORRECTED HORIZON TRUNCATION ----------------------------------
def truncate(time, event, H):
    """The ONLY permitted horizon rule.  NEVER (time<=H)|(event==1)."""
    t_h = np.minimum(np.asarray(time, float), H)
    e_h = (np.asarray(event).astype(bool) & (np.asarray(time, float) <= H))
    return t_h, e_h.astype(int)

_, e5  = truncate(df.time, df.event,  5.0)
_, e10 = truncate(df.time, df.event, 10.0)
assert e5.sum()  ==  97, f"G2 five-year events {e5.sum()} != 97"
assert e10.sum() == 194, f"G2 ten-year events {e10.sum()} != 194"

# ---- Frozen common evaluable set (ONE rule, all four models) ----------------
need = CALONG_INPUTS | SAFEHEART_INPUTS | MONTREAL_INPUTS | FHRS_INPUTS
ev   = df[df[list(need)].notna().all(1) & (df.age <= 65)].copy()   # FH-RS native range
publish_evaluable_ledger(ev, df)          # OBJ-004-A: BEFORE any fit
_, ev_e5 = truncate(ev.time, ev.event, 5.0)
log(f"evaluable n={len(ev)} full_events={int(ev.event.sum())} 5y_events={int(ev_e5.sum())}")

# ---- Frozen preprocessing (constants) + fold-learned (scaling, lambda) ------
def design(d, mu=None, sd=None):
    X = pd.DataFrame(index=d.index)
    X[["age_s1","age_s2"]] = rcs_basis(d.age, knots=(50, 58, 65))   # FROZEN knots
    X["male"], X["smoke_curr"] = d.male, d.smoke_curr
    X["htn_med"], X["dm"]      = d.htn_med, d.dm
    X["log_tghdl"]  = np.log(d.tg / d.hdl)
    nonhdl_unt      = np.where(d.on_llt, (d.tc - d.hdl) / 0.70, d.tc - d.hdl)
    X["cum_nonhdl"] = np.log(nonhdl_unt * d.age)
    X["lpa_hi"]     = (d.lpa_nmol >= 125).astype(float)             # FROZEN, native
    if mu is None: mu, sd = X.mean(), X.std(ddof=0)                 # TRAIN FOLD ONLY
    return (X - mu) / sd, mu, sd

def oof_lp(d, groups, lam, seed):
    """Out-of-fold LP. lambda re-selected inside each training fold."""
    lp = np.full(len(d), np.nan)
    for tr, te in GroupKFold(5).split(d, groups=groups):
        Xtr, mu, sd = design(d.iloc[tr])
        lam_tr = select_lambda_nested(Xtr, d.iloc[tr], groups[tr]) if lam is None else lam
        fit = CoxPHSurvivalAnalysis(alpha=lam_tr).fit(Xtr, surv(d.iloc[tr]))
        Xte, *_ = design(d.iloc[te], mu, sd)      # train-fold scaling applied
        lp[te]  = fit.predict(Xte)
    return lp

groups = ev.ldlr_variant_id.values                 # cluster = variant (⊇ family)
LP = {r: oof_lp(ev, groups, None, SEED + r) for r in range(N_REPEATS)}
lam_star = median_selected_lambda()                # frozen for the bootstrap

# ---- Comparators: PDF-locked, unit-tested against published worked examples --
assert safeheart(zero_vector, 5)  == approx(0.000215, rel=0.02)   # published 0.02%
assert safeheart(zero_vector, 10) == approx(0.000460, rel=0.02)   # published 0.05%
assert safeheart(pub_high, 5)     == approx(0.3808,   rel=0.01)   # published 38.1%
assert safeheart(pub_high, 10)    == approx(0.6415,   rel=0.01)   # published 64.15%
for c in COMPARATORS:
    assert c.verified_against_pdf and c.source_pinpoint, "G3 provenance"

# ---- Evaluate: full matrix, corrected truncation everywhere -----------------
rows = []
for lpa_layer in ("L0", "L1", "L2_100", "L2_125"):
    sc = score_comparators(ev, lpa_layer)                   # NOT-EVALUABLE at L0
    for comp in ("SAFEHEART-RE", "Montreal-FH-SCORE", "FH-Risk-Score"):
        for H in ("full", 5.0, 10.0):
            for sg, m in SUBGROUPS.items():
                s = ev[m]
                t_h, e_h = ((s.time, s.event) if H == "full"
                            else truncate(s.time, s.event, H))
                if e_h.sum() < MIN_EVENTS:
                    rows.append(dict(comparator=comp, subgroup=sg, horizon=H,
                                     layer=lpa_layer, events=int(e_h.sum()),
                                     verdict="<10, non-estimable")); continue
                if sc[comp][m].isna().all():
                    rows.append(dict(comparator=comp, subgroup=sg, horizon=H,
                                     layer=lpa_layer, verdict="NOT-EVALUABLE")); continue
                cm = mean_over_repeats(lambda r: C(t_h, e_h, LP[r][m], H))
                cc = C(t_h, e_h, sc[comp][m], H)
                # paired cluster bootstrap: refit inside each resample (lambda frozen)
                d  = paired_cluster_bootstrap(s, groups[m], comp, lam_star, B=B, seed=SEED)
                rows.append(dict(comparator=comp, subgroup=sg, horizon=H, layer=lpa_layer,
                                 n=len(s), events=int(e_h.sum()), C_model=cm, C_comp=cc,
                                 delta=cm - cc, lo=d.lo, hi=d.hi, B_effective=d.B,
                                 verdict=("TIE" if d.lo <= 0 <= d.hi
                                          else "WIN" if d.lo > 0 else "LOSS")))

out = pd.DataFrame(rows)
assert (out.B_effective.dropna() == B).all(), "G4 every reported cell needs B=2000"
assert len(out) == 78 * 4,                    "G5 full matrix, all four Lp(a) layers"
out.attrs["multiplicity"] = ("78 dependent cells per layer; ~4 spurious wins expected "
                             "at nominal 95% coverage. Confirmatory cells: 3 "
                             "(ALL, full follow-up, L1), Holm-adjusted.")
out.attrs["spec_sha256"] = hashlib.sha256(FROZEN_SPEC_JSON.encode()).hexdigest()
write_aggregate_only(out, "calon_g_headtohead_full.csv")
```

Runtime estimate: 10 repeats × 5 folds (+ nested λ) plus 2,000 bootstraps × 5 fits ≈ 10⁴ Cox fits at 9 df on n≈1,900 — minutes, not hours, and trivially parallel. There is no computational excuse for B=300.

---

## 3. Adversarial audit

### 3.1 Acceptance gates — a result that misses any of these is not reportable

| # | Gate | Assertion |
|---|---|---|
| **G1** | Cohort hash | `sha256 == 8c3a1e05…f49b2`; ledger 3,540 → 207 prevalent → 124 undated → **3,209**; 289 full events. Fail-loud, before any fit. |
| **G1b** | Prevalence reconciliation | The project record measures **235** true prevalent ASCVD in 3,540 LDLR carriers; the frozen ledger excludes **207** dated + 124 undated. The 28-case gap must be reconciled in writing (I50 exclusion + undated handling) and published in the ledger. Unreconciled → prevalent cases may sit in the risk set as incident events. |
| **G2** | Corrected truncation | `t_h = min(time, H)`, `e_h = event & (time ≤ H)`. `assert e5.sum()==97` and `e10.sum()==194` on the frozen cohort. Any file containing a 5-year cell whose event count equals its full-follow-up event count is void on sight. |
| **G3** | PDF provenance | Every comparator row carries `pdf_present=True`, a page + table pinpoint, `verified_against_pdf=True`, a SHA-256 of the transcribed coefficient table, and **double data entry by two independent transcribers**. SAFEHEART must additionally reproduce all four published worked-example test vectors. Montreal must carry `ranking_only=True`. |
| **G4** | B=2,000 | `B_effective == 2000` in every reported cell. Any cell below is void, not "preliminary". |
| **G5** | Full matrix | All 78 cells × 4 Lp(a) layers published. `n_events < 10` → `"<10, non-estimable"`. Unscoreable comparator → `NOT-EVALUABLE`. **Survivors are never dropped.** |
| **G6** | Multiplicity | The warning above appears in the results file and in any manuscript text. Three pre-declared confirmatory cells, Holm-adjusted. No "wins in N of 78 subgroups" claim, ever. |
| **G7** | Lp(a) | L0 (strict) reported first; L1 named as a declared assumption; L2 invariance run; conversion-sensitive cells flagged. |
| **G8** | Pre-registration | `spec_sha256` of this protocol frozen **before** the fit and embedded in the results file. Post-hoc changes require a new hash and a visible amendment log. |
| **G9** | Governance | Aggregate outputs only. No eids, no participant rows, no Welsh identifiers. |

### 3.2 Assume CALON-G is wrong. How?

**Most likely failure — the comparison is a transportability experiment wearing a model-comparison costume.** Both external scores were derived in clinically ascertained FH with much higher LDL-C. In UKB genotype-first LDLR carriers, FH-RS's LDL term starts its first non-zero band at **5.51 mmol/L** and Montreal's age chart tops out at **>63**, where most of a 40–69 UKB cohort sits. Their strongest predictors lose dynamic range. A CALON-G advantage would then measure *cohort mismatch*, not model quality. **The discriminating test:** report each comparator's C-index in its own derivation cohort (SAFEHEART 0.78, FH-RS 0.75) next to its C in ours, and report the observed variance of each comparator's score in our cohort. If a comparator's score is compressed, say so before reporting the Δ.

**Second — Montreal is not an incident-risk model.** Its own limitations state it "was developed to predict prevalent and not incident CVD" and it has no time horizon. Beating it on an incident endpoint is close to a category error. Any Montreal WIN must carry that sentence in the same paragraph, and the withdrawn tally's single WIN (female, 5 y) was in the comparator least entitled to be beaten and the subgroup with fewest events.

**Third — the honesty tax is asymmetric, in our disfavour, and should be stated as such.** CALON-G is evaluated out-of-fold; the comparators are fully external, fixed functions that pay no optimism penalty at all. Any CALON-G advantage survives a penalty they never pay. That is the correct framing of a WIN — and equally, a CALON-G *loss* is a real loss.

**Fourth — variant clustering may be too coarse or too fine.** If one common LDLR variant carries >20% of events, grouped folds become unbalanced. The guard is specified; the realised cluster-size distribution must be published.

**Fifth — 5-year subgroup cells will mostly be empty.** With ≈49 projected 5-year events in the evaluable set spread over 13 subgroups, most 5-year cells will be `<10, non-estimable`. The withdrawn matrix looked full only because the broken mask inflated 5-year events from ~49 to 146. **A sparser Cycle-2 matrix is the correct result, not a regression.**

**Sixth — `dm` may earn nothing.** It was dropped from both derivation multivariable models. If its coefficient is null, report it; do not drop it post hoc, because dropping it after seeing the fit converts a pre-specified model into a searched one.

### 3.3 Objections

```objection
id: OBJ-004-A
step: 004
round: 1
raised_by: claude
lens: methodology
severity: blocking-before-fit
title: The frozen common evaluable set and its truncated 5-year event count must
       be published BEFORE CALON-G is fitted.
claim: Constraint 6 requires one frozen evaluable set across all comparators, and
  constraint 7 makes any cell with <10 events non-estimable. Two independent
  restrictions bite hard: the FH-Risk-Score native range excludes participants
  over 65 at baseline (ATVB 2021 — "over 65 years of age at baseline were
  excluded"; "primary prevention FH between 18 and 65 years of age"), which
  removes the oldest and highest-risk slice of a 40-69 UKB cohort, and Lp(a) is
  incompletely measured in UKB. Projecting from the Julius frame (n=1,904,
  146 full events) and the frozen 97/289 ratio, the evaluable set is expected to
  hold roughly 49 five-year events. Spread over 13 subgroups, most 5-year cells
  will be non-estimable.
why_it_must_precede_the_fit: If this is discovered after the fit, the decision to
  report or not report the 5-year matrix becomes a post-hoc choice made with
  knowledge of the results. Declared in advance, it is a design constraint.
condition: Run the ledger step alone and publish evaluable_ledger.csv giving, for
  each Lp(a) layer (L0/L1/L2) and each of the 13 subgroups: n_evaluable, full
  events, 5-year events and 10-year events under t_h=min(time,H),
  e_h=event&(time<=H); plus the reason-for-exclusion tally (age>65 / Lp(a)
  missing / lipids missing / other); plus a comparison of evaluable vs
  non-evaluable on age, sex, statin use and crude event rate.
test: If the ALL-subgroup 5-year evaluable event count is <10, the 5-year
  confirmatory comparison is pre-declared non-estimable and full follow-up is the
  sole confirmatory horizon. This declaration is made from the ledger only,
  before any model is fitted.
blocks: fitting CALON-G
```

```objection
id: OBJ-004-B
step: 004
round: 1
raised_by: claude
lens: implementation
severity: blocking-before-comparator-lock
title: comparator_provenance.csv is stale and cites the wrong Montreal paper for
       the points chart.
claim: The provenance row records Montreal as pdf_on_disk="" , pdf_present=False,
  source_pinpoint="UNOBTAINABLE - cited only as ref 15 inside
  FH_Risk_Score_2021.pdf". Both facts are now false, and the citation points at
  the wrong article.
  (1) Two Montreal PDFs are on disk:
      /Users/nader85/Downloads/CALON-DeepResearch/papers/
      Montreal-FH-SCORE_Paquette_2017_derivation.pdf and
      Montreal-FH-SCORE_Paquette_2017_validation.pdf
  (2) The cited "J Clin Lipidol 2017;11:1161-1167.e3" is the VALIDATION paper
      (Vol 11, No 5, October 2017 - confirmed from its running heads). The
      Montreal-FH-SCORE points chart (Table 3) is in the DERIVATION paper,
      Vol 11, No 1, February 2017, page 84. Locking coefficients against the
      cited reference would mean transcribing a table that is not in it.
  (3) SAFEHEART and FH-Risk-Score pinpoints are also still "TODO" while both
      tables are readable today: SAFEHEART Table 3, Circulation 2017;135:2133-
      2144 at p.2139 with worked examples following; FH-RS Table 3 (chart points)
      and Table 4 (points -> 10-y risk), ATVB 2021;41:2632-2640.
condition: Rewrite comparator_provenance.csv with, per comparator: correct
  citation, on-disk path, page + table number, transcribed coefficient/points
  table, SHA-256 of that transcription, and verified_against_pdf=True only after
  two independent transcriptions agree. Montreal must carry ranking_only=True and
  the derivation-paper citation for its chart.
test: SAFEHEART's implementation must reproduce all four published worked
  examples - 0.02% and 0.05% for the all-zero vector, 38.1% and 64.15% for the
  published high-risk vector - before it may be scored. I have verified the
  locked form reproduces 0.0215%, 0.046%, 38.07% and 64.14%. Any implementation
  failing these vectors is void; the uncentred variant that produced a 77% mean
  5-year risk fails the first vector by three orders of magnitude.
blocks: naming any comparator as published; scoring the head-to-head
```

I file no other objection. I checked the endpoint provenance specifically because it is the largest latent risk in this programme, and it held: the ledger is built from `corrected_ascvd_outcomes` / `ascvd_first_date_best` (`00_governance_header.py:15`, `01_cohort_ledger_ukb.py:22–26`), not from the 31%-under-ascertained `prevalent_ascvd`. I checked the age/cholesterol-years collinearity claim and it holds: r=0.606 and r=0.577 are shared information, not duplication, and the condition number of 2.02 is unremarkable — the term that *would* have tripped a collinearity rule is `age_sp18`, and §1.2 removes it.

---

## 4. Clinical and publication reality

**Would a lipidologist believe it?** The variable set is one they would recognise and could compute at a clinic desk: age, sex, smoking, blood-pressure treatment, diabetes, TG/HDL, a cumulative cholesterol-exposure term, and a single Lp(a) threshold. Nine degrees of freedom, one ridge penalty, no forest, no ensemble. That is the right shape for 289 events and it is the shape that gets adopted.

**The weak link, conceded first.** This is a **genotype-first UK Biobank LDLR-carrier cohort, not clinically ascertained FH** — already stated in `spec_frozen.json`. It is healthier, older at entry, and less severely hypercholesterolaemic than SAFEHEART or the Montreal/FH-RS clinic cohorts. Both external scores lose dynamic range here (FH-RS's LDL bands begin at 5.51 mmol/L; Montreal's age chart saturates above 63). So the most defensible reading of any CALON-G advantage is *"published clinic-derived FH scores transport poorly to genotype-first carriers"* — a genuinely useful finding — and **not** *"CALON-G is a better FH risk model"*. I would write the paper around the first claim. It is the one the data can carry, and it is more interesting.

**Second concession.** The endpoint is coronary-weighted: date completeness is 100% for I21 and I25 but 40.9% (I63), 64.3% (I70), 52.8% (I73) and 37.0% (G45). A model tuned on this endpoint predicts coronary events better than cerebrovascular or peripheral ones. It goes in Limitations, in those words.

**Where a hostile reviewer opens, in the order they will do it:**

1. *"You fitted and evaluated in the same data; they didn't."* — Answer: out-of-fold, variant-clustered, 10 repeats, and the comparators pay no optimism penalty at all. Our estimate is the pessimistic one.
2. *"Seventy-eight subgroups."* — Answer: three pre-declared confirmatory cells, Holm-adjusted; full matrix published; ~4 spurious wins expected by chance and stated in the results file. This is why the withdrawn 1-WIN tally could never have been quoted.
3. *"Your Lp(a) units don't match theirs."* — Answer: three declared layers, a strictly assumption-free L0 against Montreal, an invariance band across 100–125 nmol/L, and CALON-G's own cut frozen in native units at a *stricter* threshold than the comparators'. The LDL mg/dL↔mmol/L conversion is exact and used without caveat; the Lp(a) one is not, and is labelled.
4. *"Montreal predicts prevalent disease."* — They are right, it says so in its own limitations, and we say it first.
5. *"Small subgroups."* — Answer: `<10, non-estimable`, printed, not quietly omitted. The Cycle-2 5-year matrix will be visibly sparser than the withdrawn one, because the withdrawn one's 5-year rows had an 89.6% event rate.

**Does it change practice?** Not on its own, and the paper should not pretend otherwise. The honest ceiling on this analysis is: *in genotype-first LDLR carriers, published clinic-derived FH risk scores discriminate less well than in their derivation cohorts, and a simple pre-specified nine-parameter model built for this population performs at least comparably.* Whether that is a WIN, a TIE or a LOSS is unknown, will remain unknown until the fit is run under the gates above, and is not claimed here.

---

## Artefacts

| Path | Contents |
|---|---|
| `debate/steps/step-004/r1/claude.md` | This protocol (orchestrator-saved) |
| `specs/CALON_G_SPEC.json` | Frozen spec: 9 terms, RCS knots 50/58/65, Lp(a) 125 nmol/L, ridge, folds, seeds, gates. Hashed to `spec_sha256` **before** fitting (G8) |
| `code/23_calon_g_evaluable_ledger.py` | **Runs first, alone.** Resolves OBJ-004-A. Emits `qc/evaluable_ledger.csv` + selection table. No model fitted. |
| `code/24_comparator_lock.py` | Resolves OBJ-004-B. Transcribes SAFEHEART Table 3 (Circulation 2017;135:2139), Montreal Table 3 (J Clin Lipidol 2017;11(1):84, **derivation**), FH-RS Tables 3–4 (ATVB 2021;41:2632–2640). Emits `qc/comparator_provenance_v2.csv` with pinpoints + transcription hashes. |
| `code/24b_comparator_testvectors.py` | Unit tests. Asserts SAFEHEART 0.02% / 0.05% / 38.1% / 64.15%; asserts FH-RS off-chart handling; asserts Montreal ranking-only. Blocks scoring on failure. |
| `code/25_calon_g_fit.py` | Grouped repeated CV, nested λ, out-of-fold LP, Breslow S₀(5) and S₀(10). Contains the G1/G2 fail-loud assertions. |
| `code/26_calon_g_headtohead.py` | Full 78-cell × 4-layer matrix, paired cluster bootstrap B=2,000. Emits `qc/calon_g_headtohead_full.csv` |
| `code/27_calon_g_calibration.py` | CITL, slope, flexible curves; CALON-G vs SAFEHEART (5 y, 10 y) and vs FH-RS (10 y, banded). Montreal excluded by COMP-08. |
| `qc/calon_g_gates.csv` | G1–G9 pass/fail ledger; any FAIL blocks reporting |
| `qc/calon_g_sensitivity.csv` | CALON-G-B (apoB/HDL) — the single declared sensitivity formula; plus the 0.70→0.80 constant rerun |
| `debate/state/objections.md` | OBJ-004-A, OBJ-004-B appended |
