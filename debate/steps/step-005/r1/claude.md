# Step 005 · Round 1 · claude

## 1. Methodology

### The weak link first

The design as written cannot support the claim it is being built to test. Its stated primary contrast — ΔC of Stage-A+B versus **Stage-A alone, inside a band defined by Stage-A's own risk** — is close to tautological. Restricting to the middle tertile of Stage-A OOF risk deliberately truncates Stage-A's discriminating range, so Stage-A's in-band C collapses toward 0.5 by construction, while a genuinely informative new term keeps whatever signal it has. Any variable with independent prognostic content will look like it "adds" in that cell. That is a property of the band, not evidence that the adjunct improves care.

So the estimand is valid **only if re-specified as a policy estimand**, not a model estimand.

### What is actually being estimated

A two-stage rule is not a model; it is a deployment policy that produces one composite risk vector per participant. The evaluable object is that composite vector. Four policies are on the table and must be named before any fit:

| Policy | Rule | Assays needed |
|---|---|---|
| **P0** | Locked CALON-G primary (`…, log_lpa`); `NOT_EVALUABLE` where Lp(a) missing | Lp(a) in all |
| **P1** | Stage-A accessible core everywhere | none beyond routine |
| **P2** | Stage-A everywhere; **+ Stage-B inside the band when assays present** — *the Cycle-3 adjunct* | Lp(a)+apoB in ~⅓ |
| **P3** | Locked primary wherever scoreable; recalibrated Stage-A fallback elsewhere | Lp(a) wherever available |

The decision-relevant contrasts are **P2 vs P1** (does triage buy anything?) and **P2 vs P3** (is triage as good as simply measuring whenever the lab can?). P3 is the strongest realistic competitor and it is currently unnamed in the design. If P3 ≥ P2, the whole grey-zone construct is redundant — a lab that *can* run Lp(a) would just run it. That possibility must be pre-declared as a live outcome, not discovered later.

### The honest framing: this is an assay-economy claim, not a discrimination claim

The locked primary already carries `log_lpa`. Therefore the adjunct cannot, even in principle, out-predict the primary in participants with a full assay panel — it uses a subset of the same information plus one ratio term. Its only defensible claim is:

> Restricting Lp(a)/apoB measurement to the intermediate band retains X% of the primary model's net benefit while requiring those assays in ~33% of patients.

That is a **non-inferiority / resource-triage** claim, tested against P3, at a pre-specified non-inferiority margin. It is genuinely useful, publishable, and — critically — it cannot be read as demoting the confirmatory primary. Framed as superiority-over-Stage-A it is both statistically near-rigged and clinically uninteresting.

### Primary confirmatory claim vs exploratory adjunct claim

| Object | Status | Faces comparators? | Reporting home |
|---|---|---|---|
| CALON-G primary (frozen SPEC, `log_lpa` in base) | **Confirmatory** | **Yes — and only this** | Main results table, TRIPOD+AI complete, Wales transport |
| Stage-A accessible core | **Labelled reduced model** | No | Named table; own recalibration slope/intercept; "use when Lp(a)/apoB unavailable" |
| P2 two-stage adjunct | **Exploratory** | No | Supplement; net-benefit figure; "exploratory, not externally validated" |

**Firm rule:** only the confirmatory primary is scored against SAFEHEART / FH-RS / Montreal. Re-running the 54-cell head-to-head for Stage-A and again for P2 would triple an already-flagged multiplicity problem and is exactly the "chase a WIN in every direction" failure the lock forbids.

### The estimand also fails on precision, and that must be declared now

Projecting from the frozen counts and the Cycle-2 pilot fractions (middle-tertile event share computed under a normal-LP approximation at OOF C = 0.7047 → 25.4% of events):

| Cell | In-band n | In-band events | × assay-complete (0.60–0.77) |
|---|---|---|---|
| Full follow-up | ~1,070 | ~73 | **44–56** |
| 10-year | ~1,070 | ~49 | **30–38** |
| 5-year | ~1,070 | ~25 | **15–19** |

*(Projection, not measurement. Assay-complete range bracketed by the pilot's own evaluable fractions: FH-RS 1913/3209 = 59.6% at the low end, SAFEHEART 2470/3209 = 77.0% at the high end — the latter almost exactly the complement of the 22.5% Lp(a) missingness recorded in `debate/state/open-questions.md:275`.)*

Empirical precision anchors from `cycle2_r_pilot/calong_headtohead_full.csv` at comparable event counts:

| Pilot cell | events | ΔC 95% CI | half-width |
|---|---|---|---|
| FH-RS · smoker · 5y | 10 | −0.0559 to 0.0583 | 0.057 |
| Montreal · diabetes · 5y | 24 | −0.0402 to 0.0740 | 0.057 |
| SAFEHEART · smoker · 5y | 11 | 0.0213 to 0.1735 | 0.076 |

So the in-band ΔC will land with a half-width of roughly **±0.04 (full follow-up) to ±0.06 (5-year)**. The programme's own measured apoB increment is **ΔC +0.011** (CLAUDE.md §3). The design is powered to detect approximately **four times** the effect the programme has already measured. That is the single most important fact to fix in writing before the fit, because it makes both a null and a "positive" ΔC uninterpretable in isolation.

**Consequence:** the in-band primary metric must be **net benefit + calibration**, not ΔC. The 5-year in-band cell should be pre-declared descriptive-only.

---

## 2. Implementation

### Band definition (fixed here, before any adjunct fit)

- **Scale:** Stage-A OOF absolute risk at **H = 10 years** (194 events; the 5-year set is too thin to define a band on).
- **Band:** middle tertile of Stage-A OOF risk. **Sensitivity named now:** middle quintile.
- **Second sensitivity named now:** absolute band **5–20% 10-year risk**, matching `code/17_grey_zone_enhancers.py:54`. This is not band-tuning — it is the clinically interpretable band, and pre-registering both prevents a later "we moved to tertiles because 5–20% didn't work". Report both regardless of direction.
- **Cut-points are estimated in training folds only** and applied to test folds. A cut-point taken from the full-cohort OOF distribution inherits outcome information through the Stage-A fit.
- **Band-membership stability** must be printed: % of participants who change band across the 6 CV repeats. If instability exceeds ~15%, the band is a coin-toss for those people and the policy claim weakens accordingly.

### Fold structure (leakage-free, nested)

```r
## cell 07a — Stage-A OOF risk, training-derived band, offset Stage-B
## Governance: aggregates only. No eid / FamilyNumber / DOB written or printed.
SEED <- 20260813; REPEATS <- 6; K <- 5; H <- 10
SPEC_A <- c("age","sp50","male","bpmed","dm","smoke_curr","cum_nonhdl","log_tghdl")
SPEC_B <- c("log1p_lpa_nmol","log_apob_ldl_unt")     # each term once; no Stage-A re-entry

for (r in seq_len(REPEATS)) {
  fold <- make_folds(FROZEN, K, seed = SEED + r, cluster = FROZEN$family_id)
  for (k in seq_len(K)) {
    tr <- fold != k; te <- fold == k

    ## 1. Stage-A: ridge Cox, penalty by INNER CV on tr only; fold-wise median/mode impute
    fitA  <- ridge_cox(FROZEN[tr, ], SPEC_A, inner_cv = TRUE)
    riskA <- breslow_risk(fitA, FROZEN, H, baseline_from = tr)

    ## 2. Band cut-points from TRAINING-fold OOF risk only
    cuts  <- quantile(oof_risk_inner(FROZEN[tr, ], SPEC_A), c(1/3, 2/3))
    inband <- riskA >= cuts[1] & riskA <= cuts[2]

    ## 3. Stage-B fitted on tr & inband & assay-complete, with Stage-A LP as OFFSET
    ##    -> Stage-A is FROZEN, exactly as deployed. This enforces "no Stage-A re-entry".
    sub   <- tr & inband & assay_complete
    fitB  <- ridge_cox(FROZEN[sub, ], SPEC_B, offset = lp_A[sub], inner_cv = TRUE)

    ## 4. Composite policy vector P2 on the TEST fold
    riskP2[te] <- ifelse(inband[te] & assay_complete[te],
                         breslow_risk(fitB, FROZEN[te, ], H, offset = lp_A[te]),
                         riskA[te])
  }
}
```

The `offset()` construction is the point: it makes Stage-B an increment on a *frozen deployed* Stage-A, which is what the deployment rule actually specifies. **Named sensitivity:** Stage-A LP entered as a single freely-estimated covariate instead of an offset (allows recalibration in-band).

**This differs materially from `code/17_grey_zone_enhancers.py:150`**, which re-fits the base model *inside* the band (`cf.cv(s, base)` on `s = d.loc[grey]`). That answers "does B add to a band-specific refit of A", not "does B add to the A you deployed". Script 17 is prior exploratory work, **not** the Cycle-3 artefact.

### Missing-assay policy

Identical to the Cycle-2 lock, with one addition: **missing assay is a policy branch, not a missing value.** Do not impute Lp(a) or apoB to enable Stage-B. A participant without the assays receives Stage-A — that is the clinical reality being modelled. Print, in-band: n with Lp(a), n with apoB, n with untreated LDL, n with all three; and the event rate in assay-complete vs assay-incomplete in-band participants (an MNAR tell).

### Acceptance gates

| # | Gate | Fail action |
|---|---|---|
| G1 | Cohort SHA `8c3a1e05…`; 289 / 97 / 194 | abort |
| G2 | `t_h = pmin(time,H)`; `e_h = event & time<=H`; **assert 97 at 5y** | abort |
| G3 | In-band **assay-complete** events ≥ 10 at the reported horizon | cell = NON-ESTIMABLE, printed, not omitted |
| G4 | B = 2,000 paired cluster bootstrap for every reported adjunct claim | label PILOT |
| G5 | Band cut-points training-derived; band-membership stability printed | abort |
| G6 | Stage-A entered as offset (primary) | abort |
| G7 | Calibration slope + CITL for P1, P2, P3 in-band | claim withheld |
| G8 | Net benefit at pre-specified 5%, 7.5%, 10% 10-year thresholds | claim withheld |
| G9 | No comparator head-to-head is run for Stage-A or P2 | abort |
| G10 | Pre-declared precision statement printed beside every ΔC | abort |

### Named failure modes

| Failure mode | Mechanism | Guard |
|---|---|---|
| **Self-fulfilling band** | Band defined on Stage-A risk → Stage-A range-restricted → anything beats it | Primary in-band comparator is **P3 / locked primary**, not Stage-A |
| **Cut-point leakage** | Tertile boundary from full-cohort OOF risk | Training-fold cut-points (G5) |
| **Enhancer leakage** | Stage-B fitted on the full cohort then evaluated in-band | Stage-B fitted on `tr & inband & assay-complete` only |
| **Stage-A drift** | Band-specific refit of Stage-A | `offset()` (G6) |
| **Boundary churn** | Unstable band membership across repeats | Stability % printed |
| **Silent horizon shopping** | 5y reported when 10y is null | 5y pre-declared descriptive-only |
| **Assay-availability confounding** | Assay-complete participants differ in risk | In-band event rate by assay status printed |

---

## 3. Adversarial audit

**Premise: the "adjunct improves care" claim is wrong. Here is how.**

**1. The improvement is range restriction, not information.** Covered above; it is the most likely explanation for any positive in-band ΔC vs Stage-A. The only way to falsify it is the P3 comparison, which is currently missing from the design.

**2. `log(apoB / untreated_LDL)` is partly a statin-tier indicator.** apoB (p30640) is measured **on treatment**. Untreated LDL is back-calculated by dividing measured LDL by a tier-specific de-treatment factor. Therefore, in treated participants:

```
log(apoB / LDL_unt) = log(apoB) − log(LDL_meas) + log(factor),   log(factor) < 0
```

The term is shifted downward by a deterministic function of statin tier. Statin tier is strongly associated with outcome by indication. Any in-band gain may be a treatment-status proxy dressed as a particle-discordance marker — and it would transport catastrophically to a cohort with a different prescribing distribution. This is not hypothetical: the programme's own treatment-era caveat (T24/T29, in-stratum never-treated HR 1.25 [0.89–1.76], NS) is the same wound.

**3. Assay availability is not missing-at-random and it is the binding constraint.** SAFEHEART's evaluable set (2,470/3,209 = 77.0%) is essentially the Lp(a)-complete set. FH-RS's (1,913/3,209 = 59.6%) has an event rate of 7.6% against the cohort's 9.0% — its evaluable set is *depleted of events*, consistent with the native 18–65 age restriction excluding older, higher-risk participants. A Stage-B requiring Lp(a) **and** apoB **and** untreated LDL will be scoreable in roughly 60–77% of the band. A policy that only fires in the assay-rich two-thirds of an intermediate band is a policy for well-resourced clinics — the opposite of the deployability rationale that motivated it.

**4. Multiplicity.** 2 band definitions × 2 horizons × 4 policies × {ΔC, slope, CITL, NRI, NB at 3 thresholds} is >100 cells on ~50 events. With half-widths of ±0.04–0.06, several will look "significant" by chance. **One primary exploratory cell must be named now:** *in-band, 10-year, net benefit of P2 vs P3 at the 10% threshold.* Everything else is secondary and labelled.

**5. Transportability is not merely weak — it is absent.** Wales carries Lp(a) on a different assay scale and has **no apoB** (`code/17_grey_zone_enhancers.py` docstring). Stage-B is therefore **unscoreable in the only external cohort this programme has**. There is no path from "exploratory adjunct" to "validated adjunct" within the current data. That is decisive for §4.

**6. The temptation to outcome-tune the band.** The pressure point is precisely G3: if the 10-year assay-complete in-band cell returns ~30 events and a null, the next move will be "widen to the middle two quintiles" or "use 5–20% instead". Both are pre-registered here, both must be reported, and no third band may be introduced. If a fourth band appears in any output, the analysis is outcome-informed and the whole adjunct reverts to hypothesis-generating.

**7. The self-serving asymmetry.** A LOSS for the adjunct is a clean result: it says measure Lp(a) in everyone you can, and use the accessible core where you cannot. That is a *better* clinical message than a marginal WIN, and the panel should say so out loud before the fit so that a null is not experienced as a failure to be engineered around.

---

## 4. Clinical and publication reality

**Recommendation: deploy the two-stage adjunct as exploratory and labelled — option 2 — with promotion foreclosed in this programme.**

Reasoning, in order:

1. **The confirmatory primary does not move.** CALON-G with the frozen SPEC remains the single model facing SAFEHEART / FH-RS / Montreal. Nothing in Cycle-3 can promote or demote it.
2. **Stage-A is worth publishing in its own right**, independent of whether Stage-B adds. A recalibrated accessible core that needs no Lp(a) and no apoB is a real deliverable for labs that cannot run those assays, and it is the honest answer to the investigator's clinical rationale. Report it with its own calibration slope and intercept and an explicit "reduced model" label — the SCORE2-style precedent.
3. **P2 is a supplementary, exploratory, assay-economy analysis.** Its claim is non-inferiority to P3 at a pre-specified margin, not superiority over P1. Its figure is a decision curve, not a C-index table.
4. **Promotion gates cannot be met, and saying so now is the honest move.** For completeness, the gates that *would* be required are: (i) in-band assay-complete events ≥ 50 at the reported horizon; (ii) P2 non-inferior to P3 in net benefit at 10% with B=2,000; (iii) in-band calibration slope 0.8–1.2 for P2; (iv) the statin-tier sensitivity showing the apoB ratio is not a treatment proxy; (v) **external transport of Stage-B in a cohort with both assays.** Gate (v) is unreachable — Wales has no apoB and an incomparable Lp(a) assay. So the adjunct cannot be promoted with the data this programme holds, and the manuscript should state that as a limitation rather than leaving the reader to infer a pathway that does not exist.

**On the WIN-chasing point, explicitly:** a comparator LOSS is a result. The Cycle-2 pilot's WIN=10 / TIE=44 already carries a multiplicity warning in its own `calong_run_meta.json`; adding two more model variants to that tally would convert a defensible tally into a fishing expedition. The confirmatory goal is a well-specified, calibrated, externally-transported model reported in full — not a matrix with no red cells.

**Publication shape:** primary paper = CALON-G confirmatory + Wales transport. Stage-A and P2 = one supplementary section titled "Deployability under restricted assay availability (exploratory)", with the precision statement, the projection table above replaced by measured counts, and the transport limitation stated in the same paragraph as the result.

---

```objection
step: 005
id: OBJ-005-A
title: In-band comparator must be the locked primary, not Stage-A alone
raised_by: claude
severity: blocking
claim: The pre-specified in-band contrast (Stage-A+B vs Stage-A) is confounded by construction. Restricting to the middle tertile of Stage-A OOF risk range-restricts Stage-A's own scale, so its in-band C is driven toward 0.5 and any informative added term will show a positive delta. This cannot distinguish "the adjunct improves care" from "the band was drawn on the comparator's scale".
condition_before_fit: Add the locked CALON-G primary (and the P3 fallback policy) as the primary in-band comparator, evaluated on the identical in-band, assay-complete set. Pre-declare the primary exploratory cell as net benefit of P2 vs P3 at the 10% 10-year threshold. Stage-A remains a secondary reference only.
falsifies_if: The panel can show that in-band C for Stage-A is not materially compressed relative to full-cohort C (e.g. in-band C_A >= 0.65), in which case the range-restriction concern is quantitatively minor.
```

```objection
step: 005
id: OBJ-005-B
title: log(apoB/untreated_LDL) is partly a statin-tier indicator
raised_by: claude
severity: blocking
claim: apoB (p30640) is measured on treatment while untreated LDL is back-calculated by a tier-specific de-treatment factor, so log(apoB/LDL_unt) = log(apoB) - log(LDL_meas) + log(factor), shifted deterministically by statin tier in every treated participant. Any in-band gain may be a treatment-status proxy, which would not transport to a cohort with different prescribing. The programme already carries an unresolved treatment-era caveat (T24/T29, never-treated in-stratum HR 1.25 [0.89-1.76]).
condition_before_fit: Pre-specify NOW, in writing, (i) the on-treatment form log(apoB/LDL_measured) as a co-reported measurement-scale sensitivity, and (ii) mandatory printing of the correlation between log(apoB/LDL_unt) and statin_tier, plus the in-band adjunct delta stratified by never-treated vs treated. Naming these after the fit is forbidden.
falsifies_if: The correlation between log(apoB/LDL_unt) and statin_tier is negligible and the two measurement forms give concordant in-band results.
```

```objection
step: 005
id: OBJ-005-C
title: Precision floor must be declared before the fit, and the in-band primary metric must not be Delta-C
raised_by: claude
severity: blocking
claim: Projected in-band assay-complete events are ~44-56 (full follow-up), ~30-38 (10y) and ~15-19 (5y). Pilot cells at comparable event counts (Montreal diabetes 5y, 24 events, CI half-width 0.057; FH-RS smoker 5y, 10 events, half-width 0.057) imply an in-band Delta-C half-width of roughly +/-0.04 to +/-0.06. The programme's own measured apoB increment is Delta-C +0.011. The design can therefore only detect an effect about four times larger than the one already measured, making both a null and a positive Delta-C uninterpretable in isolation.
condition_before_fit: Print a pre-declared precision statement in the run meta; designate net benefit and calibration (slope/CITL) as the in-band primary metrics with Delta-C secondary; pre-declare the 5-year in-band cell as descriptive-only; and pre-register both band definitions (middle tertile, middle quintile) plus the absolute 5-20% band, with all three reported whatever the direction.
falsifies_if: Measured in-band assay-complete events exceed 100 at the reported horizon, in which case Delta-C becomes estimable to a useful precision.
```

---

## Artefacts

| Path | Status | Purpose |
|---|---|---|
| `debate/steps/step-005/r1/claude.md` | this file | Panel Round-1 response |
| `julius-cycle2-pack-R/07a_stagea_band_oof.R` | proposed | Stage-A ridge Cox, training-fold band cut-points, band-membership stability |
| `julius-cycle2-pack-R/07b_stageb_offset_fit.R` | proposed | Stage-B on `tr & inband & assay-complete` with Stage-A LP as `offset()`; free-slope sensitivity |
| `julius-cycle2-pack-R/07c_policy_vectors.R` | proposed | Composite risk vectors P1 / P2 / P3; P0 evaluability audit |
| `julius-cycle2-pack-R/07d_inband_nb_calibration.R` | proposed | In-band net benefit at 5/7.5/10%, calibration slope + CITL, B=2,000 paired cluster bootstrap |
| `julius-cycle2-pack-R/07e_assay_missingness_audit.R` | proposed | In-band assay completeness, event rate by assay status, statin-tier correlation (OBJ-005-B) |
| `code/23_greyzone_twostage.py` | proposed | Python twin of 07a–07e, same SPEC and gates |
| `code/17_grey_zone_enhancers.py` | **superseded for Cycle-3** | Prior exploratory work; refits base inside the band at `:150` — not the deployment rule |
| `outputs/cycle3_greyzone_run_meta.json` | proposed | SHA + 289/97/194 gate, band cut-points, stability %, precision statement (OBJ-005-C) |
| `outputs/cycle3_policy_headtohead.csv` | proposed | P1/P2/P3 in-band only — **no comparator cells** (G9) |
