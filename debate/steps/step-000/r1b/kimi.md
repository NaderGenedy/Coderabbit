---
agent: kimi
step: "000"
round: "1"
protocol: full-matrix-blind
status: round-1-complete
source: debate/steps/step-000/r1b/kimi.txt
---

# Step 000 · Round 1 · KIMI

> Blind resource audit. This agent did **not** see other agents' outputs.
> Four lenses required: Methodology · Implementation · Adversarial · Clinical/publication.

# Step 000, Round 1 — Kimi, resource audit (blind)

  ## Resource ledger — what I examined, what it establishes, what it does not

  **Provided and read in full:** the step-000 brief; `mandates/ROLES.md`; `state/open-questions.md`; `DATA-INVENTORY.md` (lines 1–120 only); `STATUS.md`; `steps/step-002-QC-BRIEF.md`; excerpts of `code/15_CALON_FINAL.py` (SPEC/comparator/`usable()`/tally sections); `CALON_JULIUS_SPECKIT/scripts/comparators.py` (truncated mid-`fhrs_chart_points`); headline aggregates of `outputs/calon_final.json`.

  **Listed as permitted but NOT in my context, therefore unexamined:** `mandates/AGENT.md` (the prompt header substitutes for it) and `ORCHESTRATOR.md`; `bin/panel.mjs` and `bin/consensus.mjs` — so I cannot verify that register rules 1–5 (no self-closure, evidence-must-name-artefact, two-agent minimum, MAX_ROUNDS) are actually enforced in code rather than merely asserted in `open-questions.md`; `state/transcript.md` and `locked-decisions.md`; `tests/test_comparators.py` — so I cannot verify the Spec Kit tests pin coefficients to an external source rather than round-tripping the same constants; `research.md`; `checklists/comparator-fidelity.md`; `outputs/calon_final_qc.json`; and every comparator source PDF. **No coefficient in this turn is verified against a PDF.** Everything I say about provenance is about internal contradiction, which is all a blind audit can establish.

  What the provided material does establish: the locked local output (`calon_final.json`), the register state, and at least one hard internal contradiction in comparator code (below). What it does not establish: which of the two pipelines' comparator C-indices is right, and whether any comparator constant on disk matches its source publication.

  ---

  ## 1. METHODOLOGY

  **The step-002 brief conflates two estimands in one AGREE/DISAGREE frame.** Section A lists "Incident events, 5-year: 97 / 10-year: 194 / risk set 3,209" as agreed, but the locked local output is a full-follow-up survival analysis — `ukb.qc.median_followup` 14.55 years, 289 events (`calon_final.json`). Horizon-restricted risk classification and full-follow-up survival ranking are different estimands; "which numbers are trustworthy" is partly unanswerable until the debate fixes which estimand the WINs refer to. The brief never states this.

  **The strict-horizon Welsh construction is case-enriching by design.** Brief D5: "event before horizon OR documented follow-up to horizon" admits every event but only documented event-free survivors. Event rate inflates 7.4% (n=529) → 20.4% (n=289) as the sample shrinks 45%. A C-index from that construction is not transportable; the Welsh arm of the Julius run is measuring ascertainment, not risk.

  **Montreal is misclassified as an incident-event comparator.** `comparators.py::montreal_fh_score` docstring: "ranking/prevalent-CVD use only." Yet both pipelines score it against incident outcomes and it occupies one third of the tally cells (13 subgroups × 2 cohorts). The Spec Kit's own provenance warning is ignored downstream — a claim propagating past its own docstring, this project's signature failure shape.

  **Minimum event-to-baseline lag of 1 day** (brief A) means near-prevalent events enter the "incident" endpoint. No landmark sensitivity (e.g., exclude <6 months) is reported anywhere I was shown.

  **The three live objections are well-formed**: each `settled_by` names a runnable test. OBJ-003's settlement, however, has a code-level obstacle — see Implementation.

  ## 2. IMPLEMENTATION

  **Two irreconcilable "SAFEHEART" implementations coexist, both claiming published provenance.** `code/15_CALON_FINAL.py:278-279` scores SAFEHEART as a *continuous* LP (`0.045·age + 0.6·male + 0.4·htn + 0.3·smoke + 0.02·bmi + 0.15·ldl + 0.25·lpa_hi`) under the docstring "Published equations, scored not fitted" (line 257). `comparators.py::safeheart_linear_predictor` implements the *categorical* published form (age bands 1.07/1.45; male 0.70; prior-ASCVD 1.42; LDL mg/dL bands 0.92/1.57; Lp(a)>50 → 0.42), citing Pérez de Isla 2017 Table 3. The local version omits the prior-ASCVD term entirely and takes LDL as a continuous variable in unstated units — UK Biobank `ldl_chem` is mmol/L (`DATA-INVENTORY.md`), the Spec Kit expects mg/dL. At most one of these is the published score. This is decisive for OBJ-001: the local SAFEHEART C of 0.6944 — the number that converts both Julius WINs to TIEs — comes from the unverified implementation.

  **`comparators()` silently imputes every missing input** (`15_CALON_FINAL.py:258-262`): `hdl→1.35`, `htn→0`, `smoke→0`, `ldl→` cohort median, `lpa→0` (so the 22.5% missing Lp(a) become `lpa_hi=0`), `bmi→` median or 27.0. No imputation count is printed per input. The comparator C-indices in `calon_final.json` are of silently completed variants, not the published scores, and imputation burden differs by cohort (Welsh BMI 45.5% observed, STATUS.md).

  **The collinearity guard cannot see OBJ-003's failure mode.** `usable()` line 300: `if f.startswith("sp") and abs(corrcoef(age, f)) >= 0.999` — the check only inspects spline features against age. A non-spline term built from age (cholesterol-years = age × TC) is never correlated-checked by anything. The docstring (lines 285–294) presents F3 as a general collinearity guard; the code is a spline-deduplication rule. A check structurally incapable of catching the failure it is cited against.

  **Unverified magic constants in the Spec Kit:** `safeheart_risk` uses centering `5.4078` and baseline survivals `{5: 0.9532, 10: 0.9025}` with no provenance I was shown. If `tests/test_comparators.py` (not provided) merely asserts these same numbers, provenance is circular — exactly how invented weights shipped last time.

  ## 3. ADVERSARIAL AUDIT

  Assume the strongest claim — "the local pipeline's comparator values are correct and both Julius WINs are artefacts" — is wrong. **Most likely way it is wrong:** the local continuous SAFEHEART is accidentally well-tuned to UK Biobank, manufacturing ties. The asymmetry argument in OBJ-001 cuts both ways: Montreal — the one comparator whose published form is integer points anyone can transcribe — reproduces across pipelines to 0.003. SAFEHEART and FH-RS disagree precisely where implementation freedom is greatest (Lp(a) threshold, LDL units/bands, missing-data handling). That pattern is consistent with *either* side being wrong, and only the PDFs arbitrate. If the local SAFEHEART were wrong, what would have failed? The PDF extraction in OBJ-001's `settled_by` — which is why that test, run over both in-repo implementations, is the single computation that settles the WIN dispute.

  **An exactly-zero delta.** `calon_final.json`: `wales.subgroups."no diabetes".vs.Montreal.delta == 0.0` with 63 events and a continuous model LP. Exact 0.0 in floating point between two independently computed C-indices is arithmetically improbable; it suggests a degenerate path in `delta_ci` or the comparator vector being the model's own LP somewhere. Nothing downstream checks for this — the cell counts as a "tie" and moves on.

  **The Welsh tally hides consistently negative point estimates.** Wales hypertensive subgroup: model C 0.5585, all three deltas negative (−0.056, −0.039, −0.027), yet `wales.tally.LOSS = 0` because every CI crosses zero. "Zero losses in Wales" is mechanically true and substantively misleading.

  **The register's one closed objection rests on a disputed number.** OBJ-000 (worked example) closed on "median excess +0.226 mmol/L" — the value brief section B attributes to Julius, against the local pipeline's +0.15 and the spec's +0.55. If OBJ-000 is a real closure rather than an illustration, its evidence belongs to the pipeline currently under QC. Three values for one quantity, unreconciled.

  **OBJ-002 candidate mechanism, named:** `15_CALON_FINAL.py:272-274` z-standardizes Montreal's age and HDL terms *using the validation cohort's own mean/std*. A calibration slope fitted on a cohort-standardized LP is not on the log-HR scale and cannot be compared to 1.0; if the Julius run standardized all four LPs the same way before slope estimation, slopes of β·SD(LP) clustering at 0.52–0.57 would be an artefact of the transform, not of biology. OBJ-002's settlement should therefore require slopes reported on the raw, unstandardized LP scale.

  ## 4. CLINICAL AND PUBLICATION REALITY

  **All ten wins are internal.** `calon_final.json`: `ukb.tally` = 10/28/1; `wales.tally` = **0/30/0** with 9 non-estimable. The pooled "10 wins, 58 ties, 1 loss" in STATUS.md is entirely a UK Biobank result; in the external genotype-confirmed registry the model wins zero cells. A lipidologist reads that as: parity externally, superiority only where the model was built. Any abstract citing the pooled tally without the split over-claims.

  **The model is near-chance exactly where decisions bite:** Welsh hypertensives C 0.5585 (52 events); UKB diabetics C 0.5593 (64 events, the one declared loss); grey-zone 5–10% band AUC 0.489 (brief D3) — below chance in the band where a score must earn its keep — and both enhancers null (STATUS.md grey-zone section: apoB/LDL-C ΔC +0.0146 [−0.0050, +0.0330], Lp(a) HR 1.033).

  **The endpoint is coronary-weighted** (I63 date completeness 40.9%, G45 37.0% — brief A) but is sold as ASCVD. A hostile reviewer opens at: (1) comparator provenance — "show me SAFEHEART's coefficients and your scoring code, side by side"; (2) "your wins vanish in your external cohort"; (3) "your cerebrovascular component is 40–60% undated." What honestly survives today: an incident-ASCVD model in HeFH with C≈0.70/0.75 that ties published scores externally and loses nothing it pre-specified. That is publishable; "10 wins" as currently pooled is not.

  ---

  ## Discrepancy ledger

  1. **SAFEHEART ×2** — `15_CALON_FINAL.py:278-279` (continuous, no prior-ASCVD term, LDL units unstated) vs `comparators.py::safeheart_linear_predictor` (categorical, Pérez de Isla 2017 Table 3). Both claim published provenance. → OBJ-004.
  2. **Risk set** — step-002 brief A: 3,209 after excluding 207 prevalent + 124 undated. STATUS.md/`calon_final.json`: n=3,333 = 3,540 − 207 exactly, implying the 124 undated cases remain in the local risk set. → OBJ-006.
  3. **Montreal ×2** — local standardized-continuous LP (lines 272–274, cohort-dependent scale) vs Spec Kit integer points; Spec Kit docstring restricts it to prevalent-CVD ranking, yet both pipelines evaluate it on incident events.
  4. **FH-RS ×2** — local continuous band weights (`ab`/`lb`/`hb`, lines 275–277) vs Spec Kit integer `fhrs_chart_points`; excerpt truncated, equivalence unconfirmable.
  5. **Silent comparator imputation** — lines 258–262; no counts reported. → OBJ-005.
  6. **Diabetic loss magnitude** — STATUS.md says −0.062 in one paragraph and −0.064 two later; JSON: −0.0644. Trivial, symptomatic.
  7. **Carrier LDL-C excess ×3** — +0.15 (local) vs +0.226 (Julius, also OBJ-000's closing evidence) vs +0.55 (spec). Unreconciled.
  8. **Cosmetic** — ROLES.md "four lenses" vs "Fifth lens" naming; no scientific consequence.

  ## Evidence still needed before closure

  - **OBJ-001:** PDF-extracted SAFEHEART-RE and FH-RS coefficients from the PDFs on disk (not provided to me); a ruling on which in-repo implementation matches; one frozen cohort extract; both deltas recomputed with ≥2,000 bootstrap replicates (brief D6: FH-RS lower CI 0.001 is the 7.5th order statistic of 300 draws).
  - **OBJ-002:** Slopes recomputed on raw, unstandardized LPs, centred and uncentred, at 5- and 10-year baseline survival, with the `5.4078`/`0.9532`/`0.9025` constants verified against the PDF; plus a statement of whether Julius z-standardized LPs before slope estimation.
  - **OBJ-003:** Pearson r(age, cholesterol-years) printed from the analysis cohort — noting the guard at `15_CALON_FINAL.py:300` structurally cannot produce it — and the refit with untreated TC alone, reporting age HR both ways.

  ## Proposed objections (text only — not filed, per step instructions)

  ```objection
  id: OBJ-004
  step: 000
  raised_by: kimi
  claim: Two irreconcilable SAFEHEART implementations coexist, both claiming published provenance. code/15_CALON_FINAL.py:278-279 scores a continuous LP (0.045*age + 0.6*male + 0.4*htn + 0.3*smoke + 0.02*bmi + 0.15*ldl + 0.25*lpa_hi, no prior-ASCVD term, LDL units unstated) while CALON_JULIUS_SPECKIT/scripts/comparators.py::safeheart_linear_predictor implements the categorical Pérez de Isla 2017 Table 3 form (age bands 1.07/1.45, prior_ascvd 1.42, LDL mg/dL bands 0.92/1.57, Lp(a)>50 -> 0.42). At most one is the published score, and the local SAFEHEART C of 0.6944 that converts both Julius WINs to TIEs (OBJ-001) comes from the unverified one.
  settled_by: Extract the SAFEHEART-RE coefficients from the Pérez de Isla 2017 PDF on disk, score one identical frozen UKB carrier cohort extract with both implementations plus the PDF-verified form, and publish the three C-indices and pairwise LP correlations. The implementation matching the PDF within 0.003 on Montreal-style reproduction grounds is the comparator of record; recompute both OBJ-001 deltas with it.
  status: OPEN
  ```

  ```objection
  id: OBJ-005
  step: 000
  raised_by: kimi
  claim: code/15_CALON_FINAL.py:258-262 silently imputes every missing comparator input (hdl->1.35, htn->0, smoke->0, ldl->cohort median, lpa->0 making 22.5% missing Lp(a) into lpa_hi=0, bmi->median/27.0) and prints no per-input imputation counts. The comparator C-indices in outputs/calon_final.json are therefore not of the published scores but of silently completed variants, with imputation burden differing by cohort (Welsh BMI 45.5% observed vs 99.6% UKB per STATUS.md).
  settled_by: Patch comparators() to print per-input missingness counts per cohort, recompute all comparator C-indices complete-case on the identical frozen cohort extract, and publish the delta between complete-case and imputed values alongside outputs/calon_final.json.
  status: OPEN
  ```

  ```objection
  id: OBJ-006
  step: 000
  raised_by: kimi
  claim: The step-002 brief section A asserts both pipelines agree on a 3,209 risk set after excluding 207 prevalent plus 124 undated atherosclerotic cases, but STATUS.md and outputs/calon_final.json report UKB n=3,333 = 3,540 - 207 exactly, implying the 124 undated cases remain in the local risk set. If retained as event-free, 3.7% of the local cohort are misclassified cases attenuating every local C-index, including the comparator values at the centre of OBJ-001.
  settled_by: Instrument build_ukb() in code/15_CALON_FINAL.py to print each exclusion count and the disposition (excluded / censored / event-free) of the 124 undated atherosclerotic cases, and reconcile the printed arithmetic to either 3,209 or 3,333.
  status: OPEN
  ```

  ```objection
  id: OBJ-007
  step: 000
  raised_by: kimi
  claim: The headline "10 wins, 58 ties, 1 loss" in STATUS.md pools two cohorts, but outputs/calon_final.json shows all 10 wins are UK Biobank (ukb.tally 10/28/1) while the external Welsh cohort is 0/30/0 with 9 non-estimable (wales.tally). Any manuscript or abstract text citing the pooled tally without the per-cohort split overstates external performance: externally the model wins zero cells.
  settled_by: grep manuscript/ for the pooled tally; wherever it appears, the per-cohort tallies from outputs/calon_final.json (ukb.tally, wales.tally) must appear alongside it. Verified by re-running the grep after edits.
  status: OPEN
  ```

  ```objection
  id: OBJ-008
  step: 000
  raised_by: kimi
  claim: outputs/calon_final.json records wales.subgroups."no diabetes".vs.Montreal.delta as exactly 0.0 with 63 events. An exactly-zero floating-point delta between two independently computed C-indices is arithmetically improbable and suggests a degenerate path in delta_ci (code/15_CALON_FINAL.py:440) or the comparator LP being the model's own LP in that cell. No downstream check flags an exact zero; the cell is silently counted as a tie.
  settled_by: Recompute concordance_index for the model LP and Montreal LP on the Wales no-diabetes subgroup, print both C values to 6 decimal places, and show the delta_ci inputs. If the zero reproduces from genuinely equal C-indices, withdraw; otherwise fix the degenerate path and recompute the Welsh tally.
  status: OPEN
  ```
