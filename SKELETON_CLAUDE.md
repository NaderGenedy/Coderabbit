# Section-by-section skeleton — Claude's version
**Target 7,500 words body · *Atherosclerosis* primary · cardiology/lipid readership**

Each subsection lists: **the one idea it lands** → *the hinge that forces the next subsection*.

---

## ABSTRACT — 350 words (structured)

**Background** (2 sentences) FH scores are developed in one setting and applied in another; we identified no study testing both directions with both discrimination and calibration.
**Methods** (4) Reciprocal transport, DRAGON clinic (424/62/219 families) ↔ UK Biobank strict *LDLR* P/LP (890/57); matched non-carrier and referral-role auxiliaries; 4,000-replicate cluster bootstraps.
**Results** (5) AUC 0.767 (0.712–0.828) and 0.848 (0.796–0.896); E:O 3.00 and 0.45; across genotype 0.795/0.831 with E:O 1.51 (1.32–1.75) and 0.69 (0.55–0.90); referral role collapses the clinic contrast from OR 0.56 to 0.86; one out-of-fold intercept restores E:O to ~1.0.
**Conclusions** (2) Ranking transported more consistently than calibration; absolute risk requires local updating before any threshold use.

*Not here:* no "superior", no "predicts", no "first".

---

## INTRODUCTION — 800 words · 4 paragraphs

**¶1 (200) — The clinical problem.** FH risk is wide and heterogeneous; a cascade-detected 30-year-old and a referred index case with symptomatic disease are not interchangeable. Refs 1–6.
→ *So the field built scores to sort them.*

**¶2 (250) — What exists and how it differs.** Montreal (cross-sectional, prevalent CVD, **no LDL**), FH-RS (incident, untreated LDL + Lp(a)), SAFEHEART (incident, prior ASCVD weighted). Their differing endpoints, time origins and LDL bases make comparison a scientific question. Refs 8–12. **This paragraph answers senior-author comment 3 and pre-empts "why no LDL".**
→ *Each was built in one kind of cohort. None was tested in another kind.*

**¶3 (200) — The untested assumption, and the one warning shot.** SAFEHEART fell C 0.85→0.67 in English routine care and needed recalibration (McKay). Consensus Pro deep search + PubMed: **no study has tested transport reciprocally with both discrimination and calibration.** Bounded wording, never "first".
→ *That is the gap, and two genotype-defined cohorts with opposite ascertainment can close it.*

**¶4 (150) — Objectives and negative stopping rules.** State up front: classifier of *established* disease, not a risk model; pre-declared rules for what would and would not be claimed.

*Not here:* no results, no CALON-N branding, no de novo-versus-augmentation history (comment 5).

---

## METHODS — 2,100 words

| Subsection | Words | The one idea | Carried by |
|---|---:|---|---|
| Design, estimand, and what this is not | 250 | Cross-sectional classification of established ASCVD, declared in sentence one | — |
| Setting and cohorts | 350 | Two deliberately opposite ascertainment routes | `cohort_audit.json` |
| Genetic definitions | 250 | Strict ClinVar P/LP primary; LoF union pre-specified sensitivity, with the reason | audit A2 |
| Outcome definition | 200 | One table: component, code system, codes, source field, n (**comment 14**) | new table |
| Predictors and timing | 250 | Honest statement that predictors are not demonstrably pre-outcome | audit temporality |
| Model and comparators | 300 | Every comparator labelled **frozen** or **variable-set refit** (**comments 18, 3**) | provenance table |
| Transport, calibration, updating | 300 | Reciprocal fits, no target recalibration in the primary; updating pre-specified as secondary | R1, R2 |
| Auxiliary analyses | 250 | Matched non-carriers, referral role, ratio decomposition — all pre-declared auxiliary | R3, R4, R6 |
| Reporting, governance, reproducibility | 200 | TRIPOD+AI, RECORD/STROBE, PROBAST; hashes and dates → supplement (**comments 7, 8, 9**) | — |

→ *Hinge into Results: the design asks one question in two directions; here is what each direction gave.*

---

## RESULTS — 2,000 words · seven blocks that build

**R1 (250) Cohorts.** The two populations differ in age, treatment and event frequency exactly as ascertainment predicts. *Table 1.*
→ *Different populations — so does a model built in one work in the other?*

**R2 (300) Ranking transports.** 0.767 (0.712–0.828) and 0.848 (0.796–0.896). Full 12-comparison tally: **6 win, 5 tie, 1 loss**. *Table 2, Figure 2.* **Corrects the current manuscript's overstated "age+sex exceeded".**
→ *Ranking survived. Did the probabilities?*

**R3 (250) Calibration does not.** E:O 3.00 and 0.45; scaled Brier negative in one direction. *Table 3, Figure 3.*
→ *Is this about the two settings, or about FH itself?*

**R4 (300) Same pattern across genotype.** Matched non-carriers: 0.795/0.831, E:O 1.51 (1.32–1.75) and 0.69 (0.55–0.90), stable over 18 matching configurations. *Table 4.*
→ *So the level is setting-specific. What sets it?*

**R5 (250) Referral role does.** Probands 32% vs 97%; OR 0.56 (0.49–0.65) → **0.86 (0.71–1.05)** proband-only. *Figure 4.*
→ *If ascertainment moves the outcome, does it also move the predictors?*

**R6 (350) It moves the predictors too.** Measured LDL carries a *negative* coefficient in all three cohorts (−2.84 / −7.21 / −7.25); the ratio correlates with LDL (−0.57/−0.50/−0.39) far more than with apoB (−0.03/−0.24/−0.11); four LDL specifications, all reported, none clearing the bar. *Table 5, Figure 5.* **Answers comments 1, 2, 16 as negatives.**
→ *If both outcome level and predictor meaning are setting-specific, is the model usable at all?*

**R7 (300) Yes — after one parameter.** Out-of-fold intercept update: E:O → ~1.0 in all three transports, AUC essentially unchanged. *Table 3.*

*Not here:* no interpretation, no mechanism, no "therefore clinicians should".

---

## DISCUSSION — 2,200 words

**¶1 (200) Principal findings**, three sentences, no new numbers.

**¶2 (350) Why ranking travels and level does not.** Ordering depends on *relative* position; probability depends on baseline hazard, which ascertainment sets. This is the paper's mechanism.

**¶3 (300) What it means for the published scores.** Reconciles Montreal winning in the clinic (built cross-sectionally, excludes LDL deliberately) and SAFEHEART collapsing in English routine care. Our AUCs (0.767–0.848) sit within the published external range (0.67–0.78).

**¶4 (300) Our own negative.** apoB/LDL-C in cross-section is *compatible with* treatment and reverse causation — not proven to be either. The withdrawn apoB interaction stated openly.

**¶5 (250) What we could not do.** The incident design: 50 of 62 events predated the first dated lipid; 17 events in a 0.9-year work-up window. Publishable as a methods finding, and it names the data request (**comment 15**).

**¶6 (300) Limitations**, unflinching: cross-sectional, target-informed selection, predictors not demonstrably pre-outcome, 57–62 events, post hoc LDL search.

**¶7 (300) Perspective and practice** — the two sentences the paper exists to earn:

> **Perspective:** an FH risk estimate is not a property of the variant or the patient alone, but of the route by which that patient came to attention — the same person carries a different absolute risk depending on whether they were found by cascade testing, by clinic referral, or by population sequencing.

> **Practice:** before any FH risk score is used for a threshold decision in a new setting, its intercept should be re-estimated against that setting's observed event rate — one parameter was sufficient here — while its ranking may be used as published.

**¶8 (200) Future work.** Linked-outcome refresh → the incident cohort paper.

---

## CONCLUSIONS — 150 words
Ranking transported more consistently than calibration, across settings and across genotype. Recalibrate before you threshold.

---

## Open decision blocking Results
The directional finding — UKB-fitted ties-or-beats every comparator in the clinic in **4/4** specifications (AUC 0.895–0.902, zero losses) — goes in R2 as a labelled post hoc result, or is left out. My recommendation: **include**, labelled post hoc, with all four specifications shown, because the deployment direction it supports (biobank-developed → clinic-applied) is the clinically useful one.
