# Step 005 · Round 1 · Cycle-3 grey-zone adjunct (EXPLORATORY)

You are one member of the Cycle-3 grey-zone adjunct panel. Work independently.
Use the Julius Spec-kit evidence injected by the orchestrator **and** the
Cycle-2 R pilot artefacts under `debate/evidence/julius-spec-kit/cycle2_r_pilot/`.

## Decision lock (do not reopen)

1. **CALON-G primary remains confirmatory.** Frozen SPEC:
   `age, sp50, male, bpmed, dm, smoke_curr, cum_nonhdl, log_tghdl, log_lpa`
2. The Cycle-3 grey-zone design is **exploratory only**. It cannot replace the
   primary merely because a comparator cell improves.
3. Forbidden: adding predictors, moving risk-band boundaries, or swapping lipid
   terms **after** seeing WIN/TIE/LOSS. A comparator LOSS is a result, not a
   tuning signal.

## Cycle-2 R pilot facts (already on disk; quote these)

From `cycle2_r_pilot/calong_run_meta.json` and `calong_headtohead_full.csv`
(exploratory: B=300, `lpa_policy=exploratory_div215`, concordance polarity
fixed with `reverse=TRUE`):

- Frozen gates PASS: n=3209, events 289 / 97 (5y) / 194 (10y)
- OOF C ≈ **0.7047**
- Tally: **WIN=10, TIE=44** (no LOSS after polarity fix)
- Primary ALL cells: TIE vs SAFEHEART and FH-Risk-Score; **WIN vs Montreal**
  (full Δ≈+0.033; 5y Δ≈+0.048)
- Comparator evaluable sets (complete case on published inputs):
  SAFEHEART n=2470/221; FH-RS n=1913/146; Montreal n=2811/252
- SAFEHEART centred mean 5y risk ≈ 0.0101 (sane)

Pilot smoke on a split design (not confirmatory): primary **without** Lp(a)/apoB
kept WIN vs Montreal / TIE elsewhere; adding `log(apoB/LDL)+log_lpa` on the
**full cohort** did not flip to LOSS. That does **not** validate a grey-zone
adjunct; it only shows no catastrophic discrimination collapse.

## Clinical rationale for Cycle-3

Lp(a) and apoB are **not available in all labs**. Investigator preference:

- Keep a deployable **core** that can be scored from routine lipids + clinical
  factors.
- Use **Lp(a) and apoB/untreated-LDL** only as a **grey-zone enhancer** when
  those assays are available.
- If the adjunct does not improve decision-relevant performance in the
  intermediate band, **keep the locked primary alone**.

## Single pre-specified exploratory design (evaluate this, not alternatives)

**Stage A — Accessible core LP (no Lp(a), no apoB):**
`age, sp50, male, bpmed, dm, smoke_curr, cum_nonhdl, log_tghdl`

**Grey band — FIXED before any adjunct fit:**
Use Stage-A **OOF** predicted absolute risk (or OOF LP rank) on the frozen
cohort. Predeclare the band as the **middle tertile of Stage-A OOF risk**
(sensitivity, if and only if named now: middle quintile). Do **not** retune the
band after seeing enhancer results.

**Stage B — Grey enhancer (band only; each term once):**
`log1p(Lp(a)_nmol)` + `log(apoB / untreated_LDL)`  
Do not re-enter Stage-A variables. Do not add BMI, interactions, or HDL-apoB
swaps in this cycle.

**Deployment rule:** outside the band, or if assays missing → Stage-A (or
locked primary if that is the chosen confirmatory path). Inside the band with
assays present → Stage-A + Stage-B.

Note the tension with the locked confirmatory primary (which already includes
`log_lpa`). Your job is to say how the exploratory adjunct and the confirmatory
primary should co-exist in reporting and clinical use — not to silently demote
the primary.

## Mandatory evaluation constraints

1. Horizon: `t_h = pmin(time,H)`; `e_h = event & (time <= H)`; assert 97 at 5y.
2. OOF / nested CV only for any model LP used in claims; apparent labelled.
3. Reportable adjunct claims need B=2,000 paired bootstrap; B=300 is pilot only.
4. Comparators: PDF-faithful; common evaluable intersection per comparator;
   no survivor drop; native Lp(a) units for confirmatory comparator scoring —
   ÷2.15 remains exploratory.
5. Within the grey band report: ΔC vs Stage-A alone, calibration
   (slope/intercept), reclassification or DCA at pre-specified thresholds,
   assay missingness, and events in-band (fail if <10 events).
6. External Wales transport remains required before any “universal winner”
   language; Welsh Lp(a)/apoB may be unavailable → reduced model labelled.

## Deliverable

Answer under the mandatory four H2 headings. Cover:

1. **Methodology** — Is the Stage-A / grey-band / Stage-B estimand valid? How
   should it relate to the locked primary that already has `log_lpa`? What is
   the primary confirmatory claim vs exploratory adjunct claim?
2. **Implementation** — Exact band definition, fold structure, missing-assay
   policy, acceptance gates, and Julius/R cell outline. Name failure modes
   (self-fulfilling band, leakage from full-cohort enhancer fit, etc.).
3. **Adversarial audit** — Assume the adjunct “improves care” claim is wrong.
   How? Attack assay availability, multiplicity, transportability, and any
   temptation to outcome-tune the band.
4. **Clinical and publication reality** — Deployment recommendation with one of:
   - Keep primary alone (reject adjunct)
   - Deploy two-stage adjunct as exploratory/labelled
   - Promote adjunct only if named gates pass (state the gates)
   Be explicit: chasing WIN in every comparator direction is not a valid
   confirmatory goal.

File an objection (`step: 005`) only if a specific condition must be met before
any adjunct fit. Do not invent generic objections.

Do not claim the grey-zone adjunct wins before it is fitted under these rules.
