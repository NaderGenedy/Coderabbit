# Next directions — winning the head-to-head without Lp(a) or apoB

**16 August 2026.** Goal restated by the investigator: a model that **beats the
published comparators, survives external validation, and uses neither Lp(a) nor
apoB**. This document sets the direction from what the panels and audits actually
established, not from what would be nice.

---

## 1. The scoreboard as it stands

From `CALON_FH_PROGRAMME_2026-08-09/01_results/`, already computed and audited.

**UK Biobank LDLR carriers, frozen published comparators** (`M12_FAITHFUL.json`,
n=2,952, 127 events):

| Score | C | 5-y AUC |
|---|---|---|
| **CALON** | **0.6428** | 0.6149 |
| FH-RS | 0.6287 | **0.6528** |
| Montreal | 0.6179 | 0.6309 |
| age + sex | 0.6083 | 0.6244 |

You win on C by +0.014 (FH-RS) and +0.025 (Montreal) — and **lose at 5 years** to
both. The 5-year column is the one a clinic uses.

**Three designs, same 2,061 Welsh patients** (`M13_THREEDESIGN.json`):

| Design | Best CALON | Best comparator | Result |
|---|---|---|---|
| Montreal's rules (prevalent) | 0.8785 | 0.8632 | **WIN +0.015** |
| SAFEHEART's rules (prior ASCVD in) | 0.7292 | 0.7483 | **LOSE −0.019** |
| FH-RS's rules (incident, prior out) | 0.7465 | **0.7642** | **LOSE −0.018** |

**The whole programme comes down to one number: −0.018 against FH-RS in the FH-RS
design.** Win that cell and everything else follows; lose it and no framing rescues
the paper.

## 2. Why it is now plausible — three things the audits changed

**2.1 The detection floor is four times smaller than the record says.**
`AUDIT_V2_AGENT_1_NUMBERS.md`, D10: the 0.085 floor assumed ρ = 0.5 between model and
comparator predictions. Measured ρ is **0.907 (Montreal), 0.884 (FH-RS), 0.869
(SAFEHEART)**. At the observed correlations the floors are **0.037 / 0.041 / 0.044**.
The auditor's words: *"all four wins clear them… the floor was set by assumption, not
measurement."*

The programme has been operating on "Wales cannot resolve below 0.15". **That is wrong
by roughly 4×.** You need to find +0.04, not +0.15.

**2.2 The gap is +0.018, and +0.033 of headroom is already demonstrated.**
`M13`: CALON-A alone scores 0.7135; CALON-A given the FH-RS variable set scores
**0.7465**. Adding hypertension and smoking to a model that lacked them bought +0.033.
FH-RS sits at 0.7642. **You are 0.018 short, having already banked 0.033.**

**2.3 Dropping Lp(a) and apoB is the enabling move, not the handicap.**
`CYCLE3_SYNTHESIS.md`, agreed by all four vendors: *"Promotion to confirmatory is
effectively blocked this programme. Wales lacks comparable apoB (and Lp(a) scale
differs). Without external transport of Stage-B, no universal-winner claim."*

`CALON_G_BIOSTAT_PROTOCOL.md` nonetheless puts `log_lpa` **in the primary spec**. That
single term makes Welsh external validation impossible. **The investigator's constraint
removes the exact blocker the panel identified.** Cycle-2's primary spec is wrong on
this point and should be changed.

## 3. What can close +0.018, transportable, without Lp(a) or apoB

No comparator contains any of these. All are computable in both cohorts from a single
dated lipid visit (`MeasurementDate.1` in Wales; baseline in UKB).

| Term | Construction | Why it can differentiate |
|---|---|---|
| `log_tghdl` | `log(TG / HDL)` | Insulin-resistance axis. Absent from all three scores. |
| `remnant_chol` | `TC − HDL − LDL` | Absent from all three. The programme's own construct. |
| `cum_nonhdl` | `log((TC − HDL) × age)` | Carries **duration**, which no comparator has. |
| `dm` | diabetes | Univariable-significant in both derivations (SAFEHEART HR 3.45; FH-RS 1.64) but **dropped from both multivariable models**. UKB has far more diabetes than a lipid clinic. |

Frozen candidate — 9 terms, no published score, no treatment flag, no Lp(a)/apoB:

```text
age, sp50, male, htn, dm, smoke, cum_nonhdl, log_tghdl, remnant_chol
```

EPV in UKB = 289/9 = **32.1**. In Wales = 92/9 = **10.2** (thin; ridge required).

## 4. The two things that will kill it — test BEFORE fitting

**4.1 Treatment flags are the retracted failure mode, and this would be the fourth.**
CALON-6D as recorded carries `on_statin_flag`. The 8 August retraction found `on_treat`
(HR 2.15) was *entirely* an artefact of undated post-event recording — the clean
visit-1 flag `Treatment1.1` shows cases **7.6%** treated vs controls **11.5%**, no
excess at all. Audit R8: the term alone discriminates at **C 0.510**, and removing it
costs −0.0057 (−0.0116, +0.0029), far below any floor.

**Any treatment term is banned from the primary spec.** Treatment enters only through
the ÷0.70 untreated back-correction of the lipid terms.

**4.2 Welsh smoking and hypertension are undated status fields.**
Retraction §5: all three published scores need smoking + hypertension, and both are
recorded as status-at-last-contact. **This inflates the comparators too** — so a
head-to-head on registry fields is *fair*, but it is not a clean external validation.

Resolution, and it is a strong Methods position rather than a concession: **report both
frames.** (a) Registry-fields frame — every published external validation of these
scores has used it, so the comparison is like-for-like with the literature. (b)
Dated-fields-only frame — model and comparators both stripped to fields with a date
preceding the event. If the ranking survives both, the win is bulletproof. If it does
not, that difference is itself the finding.

## 5. Pre-flight gates — one day, no model fitted

Run these three before writing any fitting code. Each can cancel the plan.

| Gate | Test | Kills the plan if |
|---|---|---|
| **G1 — leak** | Refit the CALON-6D spec in Wales with and without `on_statin_flag`, dated fields only | Welsh C collapses from ~0.84 toward 0.75 → the term was the leak, and the 0.8443 was never real |
| **G2 — census** | Of 1,159 Welsh at-risk, how many have TC, HDL, TG **and** LDL at `MeasurementDate.1`? | Complete-case n falls below ~800 or events below ~70 → `remnant_chol` is not estimable and the spec must shrink |
| **G3 — floor** | Recompute the paired-bootstrap floor at **measured** ρ for each comparator, per audit D10 | Floors come back near 0.085 rather than 0.037–0.044 → the target reverts to +0.09 and is out of reach |

## 6. Development direction — run both, pre-specified

The record conflicts and must be resolved by running it, not by choosing.

- Project memory (2 August): *developing in UKB is strictly worse — 0 wins/1 loss vs
  2 wins/0; Wales-frozen 0.6850 beat UKB-internal CV 0.6766.*
- Against that: the frozen SHA cohort is UKB, EPV is 3× better there (32 vs 10), and
  `M10_EXTERNAL.json` shows a UKB-developed equation transporting to Welsh
  genotype-positives at **C 0.7404, E:O 0.815** — good discrimination, honest calibration.

**Pre-specify internal–external cross-validation both ways**, report both, and name the
primary before seeing either. Recommended primary: **develop UKB → validate Wales**, on
EPV grounds, with Wales → UKB as the declared co-primary.

## 7. Calibration is the harder half, and it is already solved once

`M10_EXTERNAL.json` — the same equation across four populations:

| Population | C | E:O |
|---|---|---|
| Wales genotype-positive | 0.7404 | 0.815 |
| Wales genotype-negative | 0.6644 | 0.359 |
| UKB carriers | 0.6428 | 3.478 |
| UKB non-carriers | 0.6725 | 3.824 |

Discrimination transports; **absolute risk does not — a 10.6-fold spread**. But
`M06_CALON_A_FINAL.json` shows the fix already works: **ascertainment-stratified
baseline hazards** (S₀ proband-gneg 0.883 / proband-gpos 0.928 / cascade-gpos 0.963)
give **E:O 1.011**.

Carry that forward. A model that ties on C but recalibrates to E:O ≈ 1.0 where the
comparators run at E:O 0.36–3.8 is a defensible clinical claim in its own right, and it
is the part of this programme nobody else has done.

## 8. Sequence

| # | Action | Gate |
|---|---|---|
| 1 | Run G1, G2, G3 | Any failure → re-scope before fitting |
| 2 | Remove `log_lpa` from the CALON-G primary; freeze the §3 spec; hash it | Spec SHA written before any fit |
| 3 | Score all three comparators PDF-faithfully; ship the SAFEHEART worked-case test (38.08% / 64.15%) | Test fails on the old function, passes on the new |
| 4 | Fix the horizon mask everywhere | 5-year risk set returns exactly 97 events |
| 5 | Fit in one frame, out-of-fold, family-clustered; IECV both directions | Gates print 3,209 / 289 / 97 / 194 and cohort SHA matches |
| 6 | Head-to-head, B=2,000, floors at **measured** ρ | Primary family pre-declared: ALL × 3 comparators × {full, 5y} |
| 7 | Ascertainment-stratified recalibration; E:O and DCA in both cohorts | E:O with CI, not point estimate |
| 8 | Report both field frames (§4.2) | Ranking stable, or the instability is the finding |

## 9. Honest odds

Beating Montreal: **likely** — already done in two frames.
Beating SAFEHEART-RE on discrimination: **plausible** — the gap is −0.019 and SAFEHEART
spans C 0.55–0.85 across cohorts, so it is unstable rather than strong.
Beating FH-RS in its own design in Wales: **the real test, roughly even odds.** You are
0.018 short with 0.033 of headroom already banked and three untried transportable terms.

If G1 shows the Welsh 0.8443 was `on_statin_flag`, the odds drop sharply and the
honest output becomes a TIE with superior calibration — which is still publishable, and
is what the panel independently recommended not to chase past.
