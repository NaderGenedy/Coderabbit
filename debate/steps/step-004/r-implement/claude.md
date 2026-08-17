# Step-004 — CALON-G Cycle-2, R track (Claude)

**Date:** 16 August 2026
**Deliverable:** `debate-teach/julius-cycle2-pack-R/` cells `00`–`06`, plus repo
entry `code/r_cycle2/16_CALON_G_CYCLE2.R`.
**Twin:** Codex is building the Python track against the same lock
(`debate-teach/julius-cycle2-pack/`). Same SPEC, same gates, same horizon maths.
**Status:** implementation complete and smoke-tested. **No fitted result.** No
cell has been run on UK Biobank or Welsh data in this session.

---

## Methodology

The protocol (`CALON_G_BIOSTAT_PROTOCOL.md`, 15 Aug lock) is implemented as
seven paste cells rather than one script, so that the artefact collaborators run
on Julius and the artefact in the repo are the same bytes. The repo entry point
holds no statistics; it preflights the session and sources the cells in order.

**Estimand.** Association of a pre-specified baseline score with time to first
incident *permitted* atherosclerotic event in UKB LDLR-variant carriers free of
prevalent disease. A prediction estimand: the model predicts, it does not cause.

**Specification, frozen before any head-to-head fit.**

```
primary     : age, sp50, male, bpmed, dm, smoke_curr, cum_nonhdl, log_tghdl, log_lpa
sensitivity : cum_nonhdl -> log(apoB/HDL)      # the only one, run before the matrix is seen
```

**Estimator.** Ridge Cox, λ by nested CV *inside* each training fold. 289 events
over ~9 terms puts EPV near 32, so L2 is mandatory. Discrimination claims use
the out-of-fold linear predictor; the apparent C is printed as a diagnostic and
labelled apparent.

**Horizon.** `t_h <- pmin(time, H)`; `e_h <- as.integer(event == 1 & time <= H)`.
The withdrawn Cycle-1 union mask is retained under the name
`horizon_risk_set_INVALID_DO_NOT_USE`, called once in cell 01 purely to print
its number next to 97, and never used to select a risk set.

**Missing data.** Train-fold median (continuous) and mode (binary), learned on
the training rows only. MCAR complete-case is not the primary and is only ever a
*named* sensitivity behind a printed Little's test. Cell 02 prints missingness
split by outcome status, which is the evidence for refusing MCAR rather than an
assertion of it.

**Uncertainty.** B = 2,000 paired cluster bootstrap on the confirmatory cells,
resampling clusters where a family key exists. Both scores are evaluated on the
same resample, so the interval is on the *difference*, not on two independent Cs.

**Beyond discrimination.** Cell 06 adds calibration slope, decile calibration
plot, observed-vs-expected, and a decision curve at 5% / 7.5% / 10% ten-year
thresholds — because a ΔC is not a clinical claim.

---

## Implementation

| Cell | What it does |
|---|---|
| `00_findings_lock.R` | Constants, gate ledger, `horizon_risk_set()`, disclosure guard, C-index sign-convention self-test, paired cluster bootstrap, explicit Breslow baseline |
| `01_horizon_prove.R` | Proves full = 289 and 5-y = 97, prints the invalid mask beside them, hard-stops otherwise |
| `02_calong_fit.R` | Design build with provenance, age-spike screen, collinearity report, missingness profile, ridge Cox with nested-CV λ, OOF LP, Schoenfeld PH, frozen coefficients, grey sensitivity |
| `03_comparators_pdf_faithful.R` | SAFEHEART-RE, FH-Risk-Score, Montreal-FH-SCORE, each with a self-test against published output; Lp(a) unit-policy sensitivity; patient-set audit |
| `04_headtohead_tripod.R` | 54-cell matrix, B=2,000 confirmatory, permutation null on the tally, mandatory warnings, honest headline |
| `05_wales_transport.R` | External geographical validation on frozen UKB coefficients **and** the frozen UKB imputation recipe |
| `06_calibration_dca.R` | Calibration, decile plot, decision curve, TRIPOD+AI checklist, `gate_report()` |

**Comparator provenance — the substantive gain this session.** All three scores
are now page-pinned, closing protocol blocker #2, with two upgrades on the
Julius pilot. Full detail in `PROVENANCE_TABLE.md`.

- **SAFEHEART-RE** — Circulation 2017;135:2133–2144, Table 3 multivariable
  column, pp.2138–2139. All eleven β are `log(HR)` of that column to 2 dp, so
  the transcription checks itself. Centring 5.4078, S₀(5)=0.9532,
  S₀(10)=0.9025 from the formula text on p.2138. Gate 4 is enforced by
  recomputing **both** published worked examples (p.2139): 0.02%/0.05% and
  38.08%/64.15% reproduce to the paper's own rounding, and a mismatch stops
  the run.
- **FH-Risk-Score** — the pilot had chart points only. The full published
  equation is in Supplemental Table II, Data Supplement **p.9**:
  `10-y risk = 1 − 0.889^exp(Σβx − 3.00)` with all 21 β. The equation is now
  primary (it has no chart ceiling and yields absolute risk for calibration and
  DCA); the chart is kept as a cross-check.
- **Montreal-FH-SCORE** — was `CANDIDATE (no PDF)`. The derivation PDF is on
  this Mac; Table 3, p.84 transcribed in full. This also resolves protocol
  cosmetic finding #7. The existing `comparator_provenance.csv` cites
  11:1161–1167.e3, which is the *validation* paper; the point table is from the
  derivation paper, 11:80–86.

**Verification.** Every `.R` file parses. The full pipeline was executed end to
end on a **synthetic** frame constructed to hit the gate counts (n=3,209 / 289 /
97 / 194) — a code test only. Those numbers are not results and appear nowhere
in the deliverables. Real data was never loaded in this session.

---

## Adversarial audit

Findings against my own implementation and against the inherited pilot, worst
first.

1. **Gate 5 was self-fulfilling.** It compared each cell's `B_used` against
   `B_CONFIRMATORY`, a mutable variable — so lowering B for speed still passed.
   The smoke run passed it at B=200 while printing "B = 2000". Now checked
   against the literal 2,000 the protocol requires, and `UNVERIFIED` otherwise.
2. **Gate 8 passed while the Welsh claim was inadmissible.** Frozen coefficients
   were used, which is what gate 8 says — but the Welsh filter ledger is
   incomplete (blocker #3), so a transport onto that risk set cannot support a
   confirmatory claim. Gate 8 now reports `UNVERIFIED` until
   `WALES_LEDGER_COMPLETE` is set, and the cell refuses to emit a confirmatory
   Welsh C either way.
3. **SAFEHEART was being fed the wrong LDL-C.** Circulation Table 3 carries two
   LDL rows: `LDL-C, mg/dL` (multivariable, HR 2.50/4.80 → the 0.92/1.57
   coefficients) and `Calculated pretreatment LDL-C` (**univariable column
   only**). The published model uses *measured* LDL-C; the pilot's
   `03_comparators_centred.py` passed `ldl_unt`. The R track passes measured
   LDL-C to SAFEHEART and untreated to FH-RS, which is what that paper requires.
   Worth mirroring in the Python twin.
4. **`glmnet` tie handling was unpinned** — the Cox default changes from
   `breslow` to `efron` at v5.1, so the same script would return different
   coefficients on different machines (644 warnings in the smoke run). Pinned to
   `efron`, matching `survival::coxph` and lifelines so the two tracks stay
   comparable; the version and setting are recorded with the coefficients.
5. **The disclosure guard cried wolf.** It banned any column called `name`,
   which killed the gate ledger. Rescoped to the identifiers governance actually
   names (eid, NHS, DOB, FamilyNumber, DatabaseNumber, LSOA). A guard that
   misfires on legitimate output gets switched off, which is worse than a
   narrower one.
6. **Calibration-in-the-large is not evidence here.** CALON-G's baseline hazard
   is estimated from the same rows that produced the OOF LP, so O:E is
   near-perfect by construction. Printed with that caveat attached; the
   informative quantities are the slope, the decile shape, and the comparators'
   O:E, which use genuinely external baselines. Their O:E and CALON-G's are not
   like-for-like and the table says so.
7. **The Lp(a) unit conversion is invented, unavoidably.** No nmol/L → mg/dL
   factor appears in any of the three PDFs, yet SAFEHEART and FH-RS both
   threshold at 50 mg/dL. Marked `CANDIDATE` and run under three policies
   (nmol threshold 105, ÷2.15, `NOT_EVALUABLE`) so a head-to-head cannot be a
   conversion artefact.
8. **FH-RS's own missing-Lp(a) rule contradicts the protocol.** The Data
   Supplement says *"If Lp(a) value is not available, 0 should be used"* — a
   healthy-default constant, which the protocol bans for comparators. Both the
   published rule and the protocol-strict `NOT_EVALUABLE` are run; neither is
   hidden.
9. **Every comparator is attenuated by definition mismatches** — hypertension
   diagnosis vs `bpmed`, Montreal's "prior or current" smoking vs UKB
   current-only, SAFEHEART's prior-ASCVD coefficient inert on an incident-only
   cohort. Each is printed at run time by `build_comparator_inputs()`. A ΔC that
   only survives because the comparator was fed a weaker variable is not a win.
10. **The cohort SHA cannot be verified across languages.** Julius's digest
    recipe is not in the spec-kit dump. `check_cohort_sha()` reports
    `UNVERIFIED`, never a silent PASS; `assert_counts()` is the identity check
    that does work in both languages.
11. **Subgroup cells are dependent and unadjusted.** The permutation null bounds
    the *tally*, not any individual cell. Every subgroup cell is labelled
    exploratory.
12. **No UKB family key exists on the drive**, so UKB variance is
    individual-level and precision may be mildly overstated. Disclosed rather
    than papered over. Wales clusters on FamilyNumber where present (converted
    immediately to an anonymous integer, never printed).
13. **Observed risks are Kaplan–Meier**, which ignores competing death and so
    overstates absolute risk and net benefit. An Aalen–Johansen version is on
    the gap list.

**Known gaps, printed by the run itself:** MICE (m≥20) under MAR with Rubin's
rules not yet implemented; Little's test absent; competing-risk absolute risks
absent; Welsh ledger incomplete; UKB kinship missing.

---

## Clinical reality

None of this is a clinical claim yet, and the structure is built to keep it that
way until it earns one.

**What the population actually is.** UK Biobank LDLR variant carriers are not
clinic-diagnosed heterozygous FH. They are milder, ascertained by genotype
rather than by presenting cholesterol or tendon xanthomata, and they were never
referred to a lipid clinic. Every comparator here was derived in a clinic
registry. Applying them out of case-mix compresses their discrimination for
reasons that have nothing to do with CALON-G being better, and a ΔC that comes
from that compression is a statement about sampling, not about the score. This
belongs in the title and abstract, not the limitations paragraph.

**What the endpoint is.** The permitted atherosclerotic composite with I50 out.
That is the defensible endpoint, and it is coronary-weighted: date completeness
runs 100% for I21 and I25 but 37–64% for the cerebrovascular and peripheral
components. A model tuned on this endpoint is closer to a coronary-event model
than the word "ASCVD" suggests.

**What would make it clinically real.** Three things, in order. First,
calibration that holds without recalibration — a slope near 1 in Wales on frozen
coefficients, not an O:E fixed by re-estimating the baseline there. Second, net
benefit above both treat-all and treat-none at a threshold a lipid clinic would
actually use; at a 10% ten-year threshold treat-all is already negative in a
cohort with this event rate, so the bar is whether the model beats treat-none by
enough to justify measuring Lp(a) and apoB. Third, the decision that would
change: in practice that is escalation to ezetimibe or a PCSK9 inhibitor, and
the honest question is whether reordering these patients moves anyone across a
threshold that alters therapy. A ΔC of a few hundredths usually does not.

**The weak link, conceded first.** The one comparison that matters — CALON-G
against scores built for a different population, on an endpoint that is
partially ascertained, with an Lp(a) unit conversion nobody has published — is
structurally tilted toward the model that was fitted here. The out-of-fold LP,
the frozen specification, the full uncensored matrix and the permutation null
are there to stop that tilt becoming a claim. If the confirmatory cells come
back TIE, that is the result.
