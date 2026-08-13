# Manuscript specification — the ascertainment paper
**Author side: Claude · 10 August 2026 · to be reconciled with Codex's `MANUSCRIPT_SPEC.md`**

---

## 0. Honest calibration on ambition

These data cannot produce a prize-calibre paper, and no amount of writing will change that: 62 and 57 events, a cross-sectional outcome, predictors not demonstrably pre-outcome, and architecture selection that touched both targets. Codex's verdict — mid-tier specialist journal — is correct *for the paper as currently framed*.

But the framing is the problem, not the data. The current manuscript asks "is CALON-N a good FH risk model?" and the answer is a shrug. The programme has independently produced **six** convergent observations about something else entirely, and that question has a clean, important, defensible answer. Reframed around it, this is a genuine contribution to how FH risk is estimated — and it sets up a second paper that could be high-impact once outcomes are linked.

Ambition, honestly placed: **one strong specialist paper now, one potentially major cohort paper after the refresh.**

---

## 1. The thesis

> **In familial hypercholesterolaemia, ascertainment sets the *level* — of LDL-C, of measured risk, and of treatment — while the risk *ordering* is broadly stable. FH risk instruments therefore transport as rankings and fail as absolute-risk instruments, and publishing an FH score without a setting-specific intercept is the field's error.**

This is falsifiable, it is supported from six directions, it explains prior published failures, and it carries a concrete practical implication.

**Title (working):** *Ascertainment sets the level, not the ranking: risk-score transportability in genetically defined familial hypercholesterolaemia*

**Central claim, one sentence:** Across two ascertainment settings and across genotype, discrimination transported to within 0.05 AUC while absolute risk was wrong by factors of 0.45 to 3.0, so FH risk scores require setting-specific recalibration before any threshold use.

---

## 2. Evidence map — six pillars

| # | Pillar | Numbers | Source file | Gap to close |
|---|---|---|---|---|
| i | Clinic ↔ biobank transport within FH | AUC 0.767 (0.712–0.828) / 0.848 (0.796–0.896); E:O 3.00 / 0.45 | `scratch_external_performance.json` | none — reproduced independently by audit |
| ii | FH ↔ age/sex-matched non-FH | 0.840→0.795, 0.802→0.831; E:O 1.51 (1.32–1.75) / 0.69 (0.55–0.90); OR 1.61 (1.19–2.19) | `fh_vs_nonfh.json`, `fh_vs_nonfh_robustness.json` | fix matched-set-naive CI; fix transductive median imputation |
| iii | Published precedent | SAFEHEART-RE in English routine care: C 0.85 → 0.67, recalibration required | McKay 2022, doi:10.1016/j.atherosclerosis.2022.07.011 | none |
| iv | Referral role, not genotype, drives the clinic contrast | genotype− are 97% probands vs 32%; OR 0.56 (0.49–0.65) → **0.86 (0.71–1.05)** proband-only | `fh_vs_nonfh.json` | none |
| v | Same variant, different phenotype by route | +1.11 mmol/L untreated LDL at matched *LDLR* residues | Paper 14 (under review, JCL) | cite as companion; do not re-derive |
| vi | Cross-sectional lipid measures carry a treatment signature | log LDL coefficient −2.84 / −7.21 / −7.25; ratio–LDL correlation −0.57 / −0.50 / −0.39 | computed 10 Aug, needs a durable script | promote from scratch to a numbered script |

Pillar vi is new and is the honest counterweight: it tells the reader why the cross-sectional apoB/LDL association must not be read as physiology.

---

## 3. Figures and tables that carry the argument

**F1** Design schematic — the two transports (across setting; across genotype), with n and events on each arm.
**F2** Discrimination transports, calibration does not — paired panel: ΔAUC forest on the left, E:O with CIs on the right, all four transports.
**F3** Calibration plots, four panels, no recalibration applied.
**F4** The ascertainment ladder — proband vs cascade vs population: LDL-C and ASCVD prevalence, showing the OR 0.56→0.86 collapse.
**F5** The treatment signature — unconstrained log apoB and log LDL coefficients across the three cohorts.

**T1** Cohort characteristics (existing Table 1).
**T2** Reciprocal transport and paired comparisons (existing Table 3).
**T3** Calibration and sensitivity (existing Table 4).
**T4** FH vs matched non-FH (existing Table 5, after defect fixes).

Existing Table 2 (candidate architectures) demotes to supplement — under the new thesis, model selection is not the story.

---

## 4. What must be recomputed before submission

| Fix | Why | Gate |
|---|---|---|
| Matched-set-aware CI for the carrier OR | current Wald CI ignores 1:5 matched sets and variant clustering | conditional logistic or cluster bootstrap on matched sets; report whichever is wider |
| Source-frame imputation in transport | target-frame medians make transport transductive | refit using source-frame medians only; E:O direction must survive |
| Pillar vi as a numbered script | currently scratch | reproduces the three coefficient pairs to 3 dp |
| Withdraw apoB effect-modification | tautological (apoB on both sides) | removed from all outputs, stated in limitations |
| Comparator provenance | "adapted" is ambiguous | every comparator labelled *frozen* or *variable-set refit* |

---

## 5. Staging

**Paper 1 — now, from frozen data.** The thesis above. No new data, no new selection cycle. Target: *Circulation: Genomic and Precision Medicine* → *Journal of Clinical Lipidology* → *Atherosclerosis*.

**Paper 2 — contingent on the outcome refresh.** A genuine incident cohort study in genetically confirmed Welsh FH. Feasibility forecast: ~287 at risk × ~10 unlinked years ≈ 2,870–4,194 person-years; at the observed rate ≈ 48–70 first events — clearing the ≥40 gate. *This is the paper with real impact potential, and it is blocked only on a data request.*

**The refresh request (one page, to whoever governs DRAGON/PASS):** SAIL/PEDW hospital-episode linkage plus ONS death registration; fields = first-occurrence dates for I20/I21/I25, OPCS-4 revascularisation, stroke/TIA, PVD, and all-cause death with cause; one declared administrative end date; delivered as dated events, not ages. Everything else already exists.

---

## 6. Division of labour

| Task | Owner | Handoff artefact |
|---|---|---|
| Thesis, narrative spine, all prose | Claude | `MANUSCRIPT_v2.md` |
| Evidence map maintenance, claim→source ledger | Claude | `CLAIMS_LEDGER.csv` |
| Figures F1–F5 | Claude | `figures/*.pdf` + generating script |
| Literature grounding, frozen-vs-refit provenance | Claude | `COMPARATOR_PROVENANCE.md` |
| The four recomputations in §4, each with its gate | Codex | `outputs/spec_fixes/*.json` |
| Independent re-derivation of every abstract number | Codex | `VERIFICATION.md` |
| Adversarial pre-submission review | Codex | findings list |
| Refresh specification, technical fields | Codex | `REFRESH_REQUEST.md` |
| Final reconciliation and submission package | Claude | `.docx` + cover letter |

---

## 7. Kill list — claims that must not appear

- "superior to" / "outperforms" any comparator
- "predicts", "risk model", "prospective" — it classifies *established* disease
- any absolute-risk, threshold, or clinical-deployment recommendation
- "externally validated" without the target-informed-selection qualifier
- apoB/LDL-C discordance as a treatment-independent biological marker
- the apoB effect-modification result (withdrawn 10 Aug)
- "first" anything
- decision-curve/net-benefit comparisons (withdrawn at QC; comparators are not calibrated probabilities)
