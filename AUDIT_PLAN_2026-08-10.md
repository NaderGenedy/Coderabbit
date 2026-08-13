# Audit plan — HeFH ASCVD risk model, against 21 author comments
**Date:** 10 August 2026 · **Target:** CALON-N manuscript (`manuscript/MANUSCRIPT_FINAL.md`)
**Lenses applied:** cardiometabolic-biostatistician · preventive-cardio-epidemiologist · cardiometabolic-evidence-synthesis

---

## 0. The decisive feasibility finding

Before planning anything I checked what `FH_Dragon3 (1).csv` (424 × 202) actually holds. It changes the plan:

| Field group | Present | Consequence |
|---|---|---|
| `BirthDate`, `TodayDate` | 424/424 | time axis is constructible |
| `MeasurementDate_1…_4` + `LDL_1…_4`, `HDL_1…_4`, `Lpa_1…_4` | 424 rows, serial | **dated repeated lipids with treatment recorded at each visit** |
| `Treatment1_1…4_3` | per visit | treatment status at each dated measurement |
| `age_at_event`, `age_at_event_or_censoring` | 424/424 | event and censoring times exist |
| `MIACSYear`, `PTCAYear`, `CABGYear`, `ANGINAYear`, `TIAYear`, `PVDYear` | per event | age at each component event |
| `ApoB`, `ApoA1`, `MtachedLDLC`, `Lpa` | single draw | apoB is **one** time point only |

**Comment 15 is correct and I was wrong to treat cross-sectional as the only option.** A landmark design anchored at a dated lipid measurement, with events dated by age, is constructible. That single fact reorganises the whole audit — it is workstream W1 and everything else queues behind it.

**Limit to state honestly:** apoB exists at one draw only. Within-person Δ-apoB versus Δ-LDL (comments 1–2) is **not** constructible. Between-person apoB/LDL by treatment intensity is.

---

## 1. Verdict on each comment

Legend — **A** agree, act · **P** partly agree, reframe · **D** disagree, argue

| # | Comment | Verdict | What it becomes |
|---|---|---|---|
| 1 | Treatment response, apoB vs LDL-C | **P** | Between-person only (single apoB draw). W6 |
| 2 | At what level is statin alone not enough; LDL falls more than apoB | **P** | Real and quantifiable — but it makes apoB/LDL partly a *treatment* marker. W6 |
| 3 | Comparators differ (FH-RS untreated LDL+Lp(a); Montreal no LDL; SAFEHEART prevalent ASCVD) | **A** | Comparator provenance table. W7 |
| 4 | Definition of superiority is overstated | **P** | Keep strict rule as pre-specified; add conventional standard alongside. W8 |
| 5 | Drop "add-to-Montreal vs de novo" framing | **P** | Drop the narrative, keep the constraint as one Methods sentence. W8 |
| 6 | 2nd Methods paragraph / external-validation definition too tough | **P** | Keep the disclosure, retitle, shorten, cite the design's proper name. W8 |
| 7 | Too much detail on file-open dates | **A** | To supplement. W8 |
| 8 | Explain SHA-256 hashes | **A** | One line + supplement. W8 |
| 9 | Methods below bar for a cardio-lipid audience | **A** | Clinical framing paragraph first. W8 |
| 10 | Extend the external-validation-of-previous-models work | **A**, scope flag | Supplement here; own paper later. W7 |
| 11 | Run CALON-N + comparators in carriers vs non-carriers | **A** | Done for age/sex; extend. W4 |
| 12 | Verify all claims against online sources | **A** | Every attributed number. W7 |
| 13 | Don't reuse TUDOR file for APOB/PCSK9; more effort; prior work ignored | **A** | Purpose-built 3-gene call set. W3 |
| 14 | Too much outcome prose — use a table | **A** | Outcome-definition table. W8 |
| 15 | Incidence vs prevalence using event date and LDL.1 date | **A — highest value** | Landmark incident design. **W1** |
| 16 | Is discordance relevant only in specific scenarios (high apoB, T2DM, TG/HDL) | **A** | Effect-modification tests. W5 |
| 17 | Grey-zone model with Lp(a) and TG/HDL | **A** | W5 |
| 18 | What does "adapted" comparator mean; add ASCVD to SAFEHEART | **A** / **P** | "Adapted" = refit, must be stated. Adding prior ASCVD is circular in a prevalent design, **legitimate once W1 exists**. W7 |
| 18b | Near-complete matching incl. LDL and smoking; report sens/spec | **P / D** | Smoking yes; **LDL no** as primary — it is a mediator. Secondary analysis. W4 |
| 19 | Use UKB 1,264 P/LP-or-LoF instead of 890 | **A** | Swap primary/sensitivity if it passes W2 gate. W2 |
| 20 | Include all P/LP or LoF, validated against ClinVar definition | **A** | ACMG-consistency check. W2 |
| 21 | Prioritise what explains risk: cumulative LDL vs gene vs Lp(a) | **A** | Variance/attribution ranking. W5 |

---

## 2. Workstreams, in dependency order

### W1 — Incident design (comments 15, and unlocks 18)
Anchor time-zero at `MeasurementDate_1`; derive age at anchor from `BirthDate`; classify each component event as before (prevalent) or after (incident) the anchor using its age-at-event field; censor at `age_at_event_or_censoring`. Report the flow: n with usable anchor, prevalent-at-anchor, incident, person-years, events.
**Gate:** if incident events ≥ 40, the paper is re-cast as incident with prevalent as sensitivity. If < 25, prevalent stands and we state the count that made it impossible. Between 25–40: report both, neither as primary.
*Epi lens:* this removes the paper's single biggest reviewer target (index-event/reverse causation). *Biostat lens:* Cox with family-clustered SE, Fine–Gray for competing non-CV death.

### W2 — Genetic definition (19, 20)
Re-adjudicate the 1,264 P/LP-or-LoF set against ACMG/AMP and current ClinVar; report how many LoF calls lack an independent P/LP assertion.
**Gate:** union becomes primary (80 events vs 57 = +40% power) only if ≥80% of the added carriers carry a defensible P/LP or unambiguous LoF consequence. Otherwise strict stays primary and union is the pre-specified sensitivity.

### W3 — Three-gene cohort, built properly (13)
Purpose-built LDLR + APOB + PCSK9 call set with per-participant variant coordinates and pathogenicity provenance — not the TUDOR feature file. If PCSK9 yields <10 carriers, say so and drop it explicitly rather than silently.

### W4 — Carrier vs non-carrier, extended (11, 18b)
Add to the completed age/sex-matched analysis: (a) smoking to the matching set; (b) sensitivity, specificity, PPV, NPV at a stated threshold for CALON-N and each comparator in both arms; (c) an explicitly-labelled LDL-matched secondary estimating the genotype effect *not* mediated by LDL-C.

### W5 — Where the risk actually lives (16, 17, 21)
Cholesterol-years from serial dated LDL; variant class; Lp(a). Rank by adjusted contribution with CIs. Test discordance × {high apoB, T2DM, high TG/HDL} interactions. Fit the grey-zone model.

### W6 — Treatment and the ratio (1, 2)
Quantify apoB/LDL by treatment intensity at the matched draw, and LDL trajectory on treatment from serial visits. **Report even if it undermines the ratio** — that is the point of the test.

### W7 — Evidence grounding (3, 10, 12, 18)
Comparator provenance table: predictors, coefficients, endpoint, LDL basis (treated/untreated), derivation cohort, published C — and **frozen vs refit** stated for each. Every attributed number re-verified.

### W8 — Manuscript surgery (4, 5, 6, 7, 8, 9, 14)
Clinical framing first; dates/hashes/outcome prose to tables and supplement; superiority reported against both the strict pre-specified rule and the conventional standard; external-validation disclosure kept but named properly and shortened.

---

## 3. Where I disagree, and how it gets settled

**Matching on LDL-C (18b).** LDL-C is how FH causes ASCVD. Matching carriers to non-carriers on LDL matches away the exposure and conditions on a mediator, which biases the carrier contrast toward null by construction. Settled by running both and labelling them as different estimands — total genotype effect (age/sex/smoking-matched) versus non-LDL-mediated genotype effect (LDL-matched). Both are reportable; only the first answers "does FH carry excess risk".

**Relaxing the superiority rule (4).** Loosening a threshold after seeing the results is the definition of a moving goalpost, and a reviewer will find it. Settled by reporting both standards side by side and letting the reader apply either.

**Adding prior ASCVD to SAFEHEART (18).** Circular while the outcome is prevalent ASCVD. Settled by W1: once there is an incident endpoint, prior ASCVD becomes a legitimate predictor and SAFEHEART is finally scored the way it was designed to be.

**"LDL falls more than apoB" as support for the ratio (2).** The phenomenon is real, but it makes the ratio partly a marker of being treated. Settled by W6 measuring it — and by accepting the answer whichever way it goes.

---

## 4. Independent audit

W1, W2 and the re-derivation of the locked numbers are being run as an **independent adversarial audit by Codex CLI**, natively on this Mac (`--sandbox danger-full-access`), so the feasibility verdicts are not solely mine. Firewall unchanged: aggregate outputs only, no participant rows, identifiers, family IDs or variant coordinates in any model context.
