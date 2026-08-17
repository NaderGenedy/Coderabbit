Both native network tools were rejected and no literature connectors exist in this runtime, so every citation check below is classified honestly against that constraint. Here is the full blind round-1 review.

---

# CALON-C manuscript — independent blind review, round 1 (KIMI internal four-seat panel)

**Scope statement.** I read the complete manuscript at `outputs/manuscript_2026-08-16/CALON_C_MANUSCRIPT_HIGH_CALIBRE.md`. No participant-level data were opened. No source artefact (`RESULTS_FINAL_CORRECTED.md`, JSONs, CSVs) was opened; the consistency audit in section C is therefore *within-manuscript* only. No other model's output was inspected. No edit was made to any file.

**Panel.** Biostatistician (B), Cardiologist (Cl), Lipid-medicine specialist (L), Senior Editor-in-Chief (E). Each seat reports independently per paragraph; E adjudicates. Disagreements are preserved in section F and the closing debate.

---

## 1. Rejection-risk summary (one page)

**Overall verdict of the panel: major revision before submission is even technically possible; two FATAL items are logistical, one FATAL item is evidentiary.** The manuscript's scientific posture is unusually disciplined — comparator fidelity, multiplicity control, the tie rule, transport-not-validation language, and self-disclosure of frame mixing are all present and correct. That discipline is also its rejection defence: nothing here is dishonest. The rejection risk comes from three directions.

**FATAL-1 (logistical).** Sixteen bracketed placeholders remain, including ethics/legal basis, funding, conflicts, PPI, data-controller, and code/model availability. No high-impact cardiovascular or lipid journal will send this out for review in this state. This is acknowledged in the manuscript itself but must be stated plainly in any risk summary.

**FATAL-2 (internal coherence).** The Results knowingly mixes analytical frames: the corrected Welsh risk set (1,169/102) is the headline, yet Table 3, Table 5's Welsh rows, and all Welsh internal discrimination values derive from the pre-rescue frame (1,159/92), with no synchronised post-correction regeneration. A reviewer does not need to distrust the numbers to reject this; they only need to note that the Results section reports two different cohorts under one label. The corrected Welsh Table 1, follow-up table, calibration, and equation do not exist. This is the single most easily weaponised line in a review report.

**FATAL-3 (evidentiary).** Reference 1 — the 2026 ACC/AHA dyslipidaemia guideline — carries the entire framing of Introduction ¶1, Discussion—Comparison ¶4, and Discussion—Lp(a) ¶1, including a specific quotation-grade claim ("FH-specific risk scores may be useful for short-term ASCVD prediction, while standard general-population tools should not be used for 10- or 30-year risk in heterozygous FH"). I could not verify this reference against any primary bibliographic record in this session (network tools declined; no connector exposed). If it cannot be verified, or does not say what is quoted, three load-bearing paragraphs collapse. **UNVERIFIED — DO NOT CITE** until resolved against the publisher record. In-window alternatives exist (2018 AHA/ACC cholesterol guideline, published November 2018; 2019 ESC/EAS guideline; the 2025 ESC/EAS focused update already cited as ref 2).

**MAJOR cluster (rejection-probable if unaddressed).** (i) Both transport C-statistics (0.7252; 0.6600) are reported without confidence intervals anywhere in the manuscript, on 102 and 289 events respectively. (ii) The UK Biobank competing-risk analysis did not execute, yet absolute-risk worked examples and E:O ratios against Kaplan–Meier are printed; the Discussion concedes this but the Results still presents 5- and 10-year risks. (iii) Nineteen references (13, 14, 16, 17, 22, 23, 26–38) appear in the reference list but are never cited in the text — including the single most topically relevant ascertainment paper (Trinder 2020, ref 14) and the entire BMJ prediction-model evaluation series (refs 26–28) on which the reporting audit implicitly relies. (iv) Three cited references breach the evidence window (Tybjærg-Hansen 2005, ref 15, used as evidence for the clinic-vs-population phenotype claim; Sudlow 2015, ref 18; RECORD 2015, ref 39), and two listed references (Khera June 2016, ref 13; VOYAGER June 2016 print, ref 31) fall ~8 weeks before the window opens. (v) The phenotype-attenuation finding (untreated LDL-C excess over non-carriers of only +0.15 to +0.23 mmol/L) is the most scientifically consequential number in the paper and is buried in Discussion ¶2 of the ascertainment section: in a carrier population with near-normal lipid excess, the entire comparator exercise is testing FH instruments in a population unlike their derivation populations, which explains — and deflates — the headline SAFEHEART-RE result. (vi) Meta-language leaks ("The user-specified label 'MACE' was not adopted", "because the user requested explicit grey-zone treatment", "the later reviewer response judged") reveal pipeline authorship and read as a response-to-review document, not a de novo manuscript.

**What would survive review today:** the corrected common-data head-to-head design, the Holm discipline, the tie rule, the comparator-fidelity corrections disclosed in both directions, and the honest transport framing. The paper's problem is not integrity; it is completeness, frame synchrony, and a reference apparatus that does not yet match the quality of the analysis.

---

## 2. Paragraph-by-paragraph review

Convention: each seat's judgement is one line; E then adjudicates with the six protocol fields. Trivially administrative paragraphs receive compressed treatment.

### Key points

**Key points ¶1 (Question).** Claim: a routine-data model can rank first atherosclerotic events among LDLR-variant carriers at least as well as established FH instruments.
- B: Estimand is ranking (Harrell C), correctly framed; "at least as well" is a non-inferiority hypothesis the design never formally tests — the data answer a superiority question instead.
- Cl: Clinically coherent question; "established instruments" elides that one comparator (Montreal) was built for prevalent disease, a different clinical question.
- L: "LDLR-variant carriers" is the honest label given the empty `variant_id`; but the attenuated phenotype of these carriers is material to the question and absent here.
- E adjudication — Weakness: hypothesis phrased as non-inferiority, analysed as superiority/tie. Evidence check: FH-Risk-Score (Paquette et al., *ATVB* 2021;41:2632–2640, doi:10.1161/ATVBAHA.121.316106 — UNVERIFIED this session, high internal-knowledge prior) is the relevant incident-event benchmark. Required improvement: rephrase as a superiority/evaluability question. Suggested wording: "…whether a parsimonious model… can rank first atherosclerotic events among LDLR-variant carriers, and how its discrimination compares with published FH instruments on identical evaluable participants." Severity: MODERATE.

**Key points ¶2 (Findings).** Claim: moderate internal discrimination; wins over SAFEHEART-RE and Montreal after Holm; tie with FH-Risk-Score; transport C 0.725/0.660; grey-zone null.
- B: Numbers match Abstract/Table 4; no CIs on the transport C's here or anywhere — a reader cannot judge whether 0.725 vs 0.660 is even nominally distinct.
- Cl: The SAFEHEART-RE win is in a frame where its previous-ASCVD term is structurally zero and its LDL-C is treatment-suppressed; stating the win without that qualifier invites clinical misreading.
- L: Grey-zone null is from a *predecessor* model; giving it Key-points prominence overstates its standing (the Methods itself says it "cannot support a clinical reclassification claim").
- E adjudication — Weakness: result stated without its setting qualifier; transport C's without intervals. Evidence check: external SAFEHEART-RE performance decay is documented (McKay et al., *Atherosclerosis* 2022;358:68–74, doi:10.1016/j.atherosclerosis.2022.07.011 — UNVERIFIED this session, moderate-high prior; Gallo et al. *Atherosclerosis* 2020;306:41–49, doi:10.1016/j.atherosclerosis.2020.06.011 — UNVERIFIED, high prior). Required improvement: add "in an incident primary-prevention frame in which SAFEHEART-RE's secondary-prevention term is zero by design" and add transport CIs. Severity: MAJOR.

**Key points ¶3 (Meaning).** Claim: feasibility shown; no external validation, no clinical utility; lists what is required.
- B: Correct and complete; the requirement list (untouched cohort, external calibration, competing risk, comparative decision curves) is the right one and matches Riley et al. *BMJ* 2024 (refs 26–28, currently uncited orphans).
- Cl: Appropriately protective; "never de-risk a carrier" logic consistent with guideline-grade caution.
- L: No objection.
- E adjudication — Weakness: none substantive. Evidence check: standards cited are in-window (TRIPOD+AI, Collins et al. *BMJ* 2024;385:e078378 — UNVERIFIED this session, high prior). Required improvement: cite refs 26–28 here or in Discussion to cure the orphan problem. Severity: MINOR.

### Abstract

**Abstract ¶1 (Background).** Claim: guidance supports FH-specific scores for short-term risk and warns against general-population equations in HeFH; comparator performance in population-ascertained carriers uncharacterised.
- B: "Incompletely characterised" is fair.
- Cl: The guidance claim is the paper's foundation; it must be verbatim-accurate.
- L: Correct that general-population 10-year tools underestimate FH risk; the window-eligible 2018 AHA/ACC guideline (Grundy et al., *Circulation* 2019;139:e1082–e1143 — UNVERIFIED this session, high prior) supports the spirit.
- E adjudication — Weakness: the entire paragraph depends on unverified ref 1. Evidence check: no in-session verification possible; ref 2 (2025 ESC/EAS focused update, *Eur Heart J* 2025;46:4359–4378, doi:10.1093/eurheartj/ehaf190 — UNVERIFIED, high prior) partially overlaps. Required improvement: verify ref 1 against the publisher record or re-anchor to refs 2 plus in-window 2018/2019 guidelines. Severity: FATAL (contingent on verification).

**Abstract ¶2 (Methods).** Claim: design, predictors, internal validation, comparator policy, multiplicity, reciprocal transport; "Decision-curve claims were withdrawn."
- B: Nine-term specification, ridge 0.02, repeated CV plus Harrell bootstrap — all reported; penalty selection mechanism absent here and in Methods.
- Cl: Endpoint label discipline correct ("first incident ASCVD", not MACE).
- L: Untreated-equivalent transformations named; fine at abstract granularity.
- E adjudication — Weakness: "Decision-curve claims were withdrawn" is revision-history prose, not methods prose. Suggested wording: "Decision-curve analysis was not performed because no comparative utility data were available." Severity: MODERATE.

**Abstract ¶3 (Results).** Claim: full numeric summary.
- B: Internal arithmetic consistent (checked: 3,540−207−124=3,209; optimism subtractions reproduce; Holm-adjusted p's are reconstructable under m=6, e.g. 6×0.00005=0.0003, 5×0.00358=0.0179 — see §C). The identical adjusted p=0.5018 for both FH-Risk-Score horizons is explicable by Holm monotonicity but the 5-year raw p's are never printed.
- Cl: "No proportional-hazards violation in 16 tested terms" is fine; but absolute risks appear later without a UKB competing-risk analysis, conceded in the same paragraph — good.
- L: No lipid-term significance is honestly omitted from the abstract headline; consider whether that honesty should be *in* the abstract.
- E adjudication — Weakness: transport C's again without CIs; Welsh internal C (0.7653) absent from abstract though transport C present — asymmetry acceptable but note it. Required improvement: add CIs to both transport estimates; state 5-year raw p's in supplement. Severity: MAJOR (CIs), MINOR (p's).

**Abstract ¶4 (Conclusions).** Claim: development + transport evidence, not validation or utility.
- B/Cl/L: All concur; calibrated language.
- E adjudication — Weakness: none. Suggested wording: retain. Severity: MINOR (none required).

### Introduction

**Introduction ¶1.** Claim: FH is lifelong exposure; heterogeneity matters despite universal treatment indication; guideline support.
- B: No estimand issue.
- Cl: "May alter the urgency of treatment intensification… specialist review… phenotyping" is exactly right and safely worded — no de-risking implication.
- L: Correct biology; "lifelong exposure disorder" aligns with cumulative-exposure evidence (Domanski et al. *JACC* 2020;76:1507–1516 — UNVERIFIED, high prior — currently an orphan ref 22; cite it here).
- E adjudication — Weakness: ref 1 dependence (see Abstract ¶1). Required improvement: cure orphan refs 22, 23 by citing them at "cumulative exposure". Severity: FATAL (ref 1 contingency), MODERATE (orphans).

**Introduction ¶2.** Claim: accurate capsule descriptions of SAFEHEART-RE (2,404; mixed prevention), Montreal (prevalent, cross-sectional), FH-Risk-Score (3,881, incident), REFERCHOL transport dependence, English miscalibration, Australian rankings.
- B: Descriptions are estimand-aware (prevalent vs incident named) — exemplary.
- Cl: Correct that rankings change across settings; the Australian C-statistics (0.767/0.735) are quoted precisely and must be verified against ref 9.
- L: SAFEHEART's Lp(a) and measured LDL-C inputs correctly stated.
- E adjudication — Weakness: refs 8 and 9 unverified in this session; ref 9's exact C values are quoted with false confidence risk. Evidence check: REFERCHOL (*Atherosclerosis* 2020;306:41–49) and SAFEHEART-RE (*Circulation* 2017;135:2133–2144 — within window, May 2017) are consistent with internal knowledge. Required improvement: verify refs 8, 9 or hedge the specific numbers. Severity: MAJOR (verification), MINOR otherwise.

**Introduction ¶3.** Claim: three unresolved issues — cross-cohort quoting, specialised-input constraint, clinic-vs-population non-interchangeability; UKB volunteer selection (5.5% participation).
- B: Case-mix conflation point is methodologically correct and is the paper's raison d'être.
- Cl: The implementation argument is clinically persuasive for low-resource settings.
- L: The phenotype-severity claim is supported by ref 15 (Tybjærg-Hansen 2005) — outside the window; in-window support exists in Trinder 2020 (ref 14, orphan) showing monogenic carriers' phenotype in unselected cohorts.
- E adjudication — Weakness: window breach (ref 15 used as evidence); orphan ref 14 is the natural in-window substitute. Required improvement: move Tybjærg-Hansen 2005 to an Excluded historical context note; cite ref 14 here. Also refs 10/11 cited for "apoB, imaging, polygenic scores, or dozens of variables" — ref 10 (Australian validation of Canadian/French scores) does not obviously support that clause; citation-content mismatch. Severity: MAJOR (window + mismatch).

**Introduction ¶4.** Claim: CALON-C design philosophy — parsimony, routine panel, fixed untreated-equivalent transformations, deliberate Lp(a)/apoB exclusion.
- B: Exclusion-as-design is defensible; the model tests an implementation proposition, not a biological one — correctly framed.
- Cl: Fine; no treatment-deferral implication.
- L: The fixed ÷0.70 factor corresponds to moderate-intensity statin effect; in FH many patients take high-intensity ± ezetimibe (≥50% lowering), so untreated-equivalent LDL is systematically underestimated in the most treated — a differential error that will attenuate lipid HRs towards null. This must be stated where the design is introduced, not only in the audit numbers.
- E adjudication — Weakness: treatment-correction limitation acknowledged later but not flagged here. Suggested addition: "These fixed factors approximate average moderate-intensity effects and will misestimate untreated concentrations under high-intensity or combination therapy." Severity: MODERATE.

**Introduction ¶5.** Claim: aims; FH-Risk-Score derivation included 499 UKB participants; no independent-validation framing; contribution statement.
- B: The overlap disclosure is exactly right; "application within a source that partly contributed to development" is the correct label.
- Cl/L: Concur.
- E adjudication — Weakness: the 499 figure is load-bearing and unverified this session. Required improvement: verify against Paquette 2021 supplement. Severity: MAJOR (verification), MINOR (prose).

### Methods

**Methods—Study design ¶1.** Claim: two-cohort prognostic study; TRIPOD+AI/STROBE/RECORD; estimand stated.
- B: Estimand ("association of a baseline linear predictor with time to first incident atherosclerotic event") is precise and non-causal — commendable.
- Cl: No objection.
- L: No objection.
- E adjudication — Weakness: RECORD (ref 39, 2015) is outside the window; as a reporting standard rather than evidence this is tolerable, but protocol requires naming it in Excluded historical context. Severity: MINOR.

**Methods—Study design ¶2.** Claim: corrected source of truth; superseded generations; discrepancies retained, not resolved.
- B: Transparent; but "retained explicitly rather than resolved by calculation" means known-stale Welsh numbers stand — a policy choice that manufactures FATAL-2.
- Cl/L: Defer to B.
- E adjudication — Weakness: editorial honesty is good, but a journal expects one pipeline of record. Required improvement: regenerate the Welsh artefacts before submission; do not submit a knowingly mixed-frame Results. Severity: MAJOR.

**Methods—Data sources ¶1.** Claim: sources, linkage, governance; no participant-level export.
- B/Cl/L: Concur; governance compliant with UKB Application 1002450 constraints.
- E adjudication — Weakness: none within paragraph; placeholders live elsewhere. Severity: MINOR.

**Methods—Data sources ¶2.** Claim: `variant_id` empty in all 501,936 rows; population labelled by carrier flag, not P/LP confirmation; Welsh genotype-positive by clinical field.
- B: Honest; consequence: RECORD 1.3 non-compliance disclosed.
- Cl: Correct restraint.
- L: This is where the phenotype-attenuation caveat belongs: flag-defined population carriers are expected on average to be milder; the +0.15–0.23 mmol/L excess belongs here as a cohort-defining fact, not in the Discussion.
- E adjudication — Weakness: variant-level inadjudicability is disclosed, but its phenotypic consequence is deferred 200 lines. Required improvement: state the attenuation figure here. Severity: MODERATE.

**Methods—UK Biobank cohort ¶1.** Claim: eligibility, baseline, endpoint union (I21, I25, I63, I70, I73, G45; I50 excluded); prevalent and undated handling.
- B: Treating undated flags as unknown (exclusion) rather than disease-free is the conservative, correct choice.
- Cl: G45 (transient ischaemic attack) is not strictly atherosclerotic; its inclusion in "ASCVD" needs a hard-coronary sensitivity, which the Discussion promises for future work but the present data could partly support (147/289 unambiguous attribution).
- L: Endpoint is lipid-relevant (atherosclerotic), acceptable.
- E adjudication — Weakness: TIA inclusion undefended; angina exclusion asymmetry vs Wales noted later. Required improvement: justify G45 or show a coronary-only sensitivity. Severity: MODERATE.

**Methods—UK Biobank cohort ¶2.** Claim: flow 3,540→3,209; 289/97/194 events; censoring 31 Dec 2023; component-date attribution unambiguous in 147/289.
- B: 49% of events have ambiguous component attribution — a data-quality fact of the first rank; the sensitivity is correctly labelled "not clean" because censoring ambiguous cases at event date is informative.
- Cl: Half the endpoints being date-ambiguous would alarm an adjudication-minded reviewer; the honest handling mitigates but does not remove concern.
- L: No additional objection.
- E adjudication — Weakness: none of disclosure; severity inherent. Severity: MAJOR (as limitation; reporting itself adequate).

**Methods—All-Wales cohort ¶1.** Claim: 2,405 frame; baseline first dated lipid visit; outcome includes angina, TIA, PVD and procedures; 10 rescued events.
- B: Baseline at first lipid visit in a registry = prevalent-user-style survivor frame; acknowledged later under survivor bias.
- Cl: Angina and TIA are soft endpoints; the Welsh event count (102) therefore mixes hard and soft events, complicating the UKB–Wales asymmetry interpretation.
- L: No additional objection.
- E adjudication — Weakness: endpoint softness asymmetry under-caveated at definition site. Severity: MODERATE.

**Methods—All-Wales cohort ¶2.** Claim: corrected exclusions (344/185/58/649) → 1,169/102; family clustering; no administrative end date; comorbidities at last contact.
- B: Arithmetic verified (2,405−344−185−58−649=1,169). The 649 "no positive operational follow-up" exclusion is a censoring-informativeness hazard; STROBE item self-flagged. Last-contact comorbidities = predictor-timing leakage, honestly bounded later (ΔC ≈ −0.030 when undated removed).
- Cl: Last-contact smoking/diabetes could encode post-event care — same danger the authors themselves cite for excluding treatment flags in UKB; the asymmetry of tolerance (strict in UKB, lenient in Wales) is defensible only because Wales is downgraded to transport-stress-test.
- L: Concur with Cl.
- E adjudication — Weakness: none of disclosure. Severity: MAJOR (as limitation).

**Methods—Outcome terminology ¶1.** Claim: "MACE" declined; cohort-specific endpoint heterogeneity declared.
- All seats: correct decision; complies with the standing rule. E: the phrase "The user-specified label" is pipeline meta-language and must be rewritten ("Because the endpoint definitions supplied were broader and differed between cohorts, the label MACE was not adopted"). Severity: MAJOR (meta-language, here and wherever it recurs).

**Methods—Predictors ¶1 (list).** Nine terms.
- B: EPP ≈ 32 (289/9) — adequate; no development sample-size justification (Riley pmsampsize criteria) anywhere.
- Cl: All variables routinely available — claim holds.
- L: `tg_filter = log[LDL_u/(TG_u+0.1)]` — the +0.1 is arbitrary and unjustified; biologically this is an LDL-to-TG discordance ratio, interpretable as a remnant/discordance marker, and should be named as such.
- E adjudication — Weakness: no sample-size rationale; unexplained constant. Severity: MODERATE.

**Methods—Predictors ¶2 (transformations).** ÷0.70/÷0.80; clipping; audit MAE 1.20 mmol/L, r=0.32; factor sensitivity ΔC ≤0.0022.
- B: Sensitivity over 0.65–0.75 is reassuring for *ranking* but the r=0.32 reconstruction validity concedes the *exposure proxy* is weak — the manuscript says this; correct.
- Cl: Fine.
- L: This is the paragraph where differential error belongs: a fixed factor misestimates most in high-intensity-treated (usually highest-risk) carriers, biasing lipid coefficients towards null — a candidate explanation for the null lipid terms that the Discussion never explicitly connects.
- E adjudication — Weakness: failure to link r=0.32 to the null lipid findings. Severity: MODERATE.

**Methods—Predictors ¶3 (exclusions).** No treatment flag (post-event encoding risk); no specialised biomarkers or prior scores.
- All seats: correct and well-motivated. Severity: MINOR.

**Methods—Model specification ¶1.** Ridge 0.02; fold-wise median imputation; collinearity guard; ≥10-events-per-level rule; Welsh loses diabetes and smoking.
- B: Penalty 0.02 selection mechanism undisclosed (tuned? fixed by precedent?); single median imputation understates imputation uncertainty (self-flagged in TRIPOD items); mechanical retention rules are transparent but their effect on the Welsh fit is consequential — the two cohorts end up with different equations, which the transport section handles honestly.
- Cl: Losing diabetes and smoking from the Welsh model removes two clinically dominant predictors; reverse transport C=0.660 is thereby partly a variable-availability artefact, which is stated — good.
- L: No additional objection.
- E adjudication — Weakness: penalty provenance. Required improvement: one sentence on how 0.02 was chosen. Severity: MODERATE.

**Methods—Model specification ¶2.** Repeated 10-fold CV + 100 Harrell bootstraps; family-cluster resampling in Wales; participant-level in UKB (no kinship).
- B: Two concordant internal estimators (Δ ≤0.008) is a strength; UKB kinship absence is a genuine, disclosed gap — carrier cohorts plausibly contain relatives, so UKB intervals may be slightly narrow.
- Cl/L: Defer.
- E adjudication — Severity: MINOR (disclosed limitation, acceptable).

**Methods—Comparator ¶1–4 (intro, SAFEHEART, FHRS, Montreal).** Transcription from primary papers; worked-example reproduction; measured-LDL correction; age ≤65 gate; ever-smoking; ranking-only use of points charts.
- B: Comparator fidelity protocol (reproduce published worked examples before scoring) is best practice; the BMI cut-point inference and points-chart use (ties deflate C for comparators) are stated.
- Cl: FHRS age gate creates a younger evaluable subset — case-mix differs across comparator rows; cross-row ranking of comparators ("strongest") is then unsafe (returns in Discussion ¶3).
- L: SAFEHEART's measured-LDL correction is faithful to the primary paper; the sensitivity with untreated LDL (comparator-favourable) is the right guard.
- E adjudication — Weakness: points-chart ties penalise comparator C; BMI cut-points assumed. Both disclosed. Severity: MODERATE (chart-tie asymmetry deserves one sentence: "points-based comparators incur tied scores, attenuating their C relative to a continuous equation").

**Methods—Comparator ¶5 (Lp(a) conversion; strict policy).** nmol/L ÷ 2.15; no favourable imputation; Lp(a)-omitted labelled incomplete.
- B: Strict complete-input policy is right; but evaluability selection (SAFEHEART subset 2,470/221 vs full 3,209/289) may not be random — no comparison of included vs excluded participants.
- Cl: Fine.
- L: ÷2.15 is within the plausible 2.0–2.5 range but particle-size-dependent; a ±10% conversion sensitivity around the 50 mg/dL threshold would reclassify borderline participants and is absent.
- E adjudication — Weakness: no conversion sensitivity; no evaluability-selection characterisation. Severity: MODERATE.

**Methods—Head-to-head ¶1–2.** Paired cluster bootstrap B=2,000; CI-excludes-zero win rule; positive-with-crossing = tie; Holm over six confirmatory cells; everything else exploratory.
- B: Exemplary multiplicity discipline; the tie rule matches the output rule. Strata <10 events not estimated — fine. The six-cell family definition is post hoc-ish (why exclude 10-year?) but declared.
- Cl/L/E: Concur. E: declare the family definition timing ("defined after seeing results"?) — the pre-specification claim was withdrawn, so confirmatory/exploratory labelling is a judgement, not a verification. Severity: MINOR.

**Methods—Calibration/transport ¶1–3.** Raw-unit equation published with S0(5/10y); internal-only calibration after reviewer objection; frozen reciprocal transport; not untouched validation.
- B: Publishing S0 and the centring constant enables exact reproduction — TRIPOD 17 satisfied for UKB. Calibration is apparent/internal only — correctly downgraded. Transport without refitting is methodologically right.
- Cl: Absolute-risk worked examples are arithmetic checks only — labelled as such; safe.
- L: No objection.
- E adjudication — Weakness: "The later reviewer response judged…" is again revision-history prose inside Methods. Suggested wording: "Because baseline survival was estimated within the development data, all calibration reported here is internal/apparent; no transportable absolute-risk claim is made." Severity: MODERATE (prose), MINOR (methods).

**Methods—PH/competing/sensitivity ¶1–2.** Rank-transformed Schoenfeld; Aalen–Johansen where death indicator exists; UKB arm did not execute (column guard); sensitivity battery including the "not clean" attribution restriction.
- B: 16 PH tests at α=0.05 unadjusted — with 16 tests, one false positive expected 56% of the time; "no violation" is weak evidence of PH adequacy (low power per term), should be phrased as "no violation detected at nominal level, power limited". The UKB competing-risk non-execution is an engineering failure, not a design choice; it blocks the paper's own absolute-risk interpretation.
- Cl: With 289 events and meaningful competing mortality in older carriers, missing UKB CIF is a real clinical-interpretability gap.
- L: Defer.
- E adjudication — Severity: MAJOR.

**Methods—Grey-zone/subgroups ¶1–2.** Predecessor-model band analysis, ancillary; no corrected subgroup table; placeholder declared.
- B: Ancillary labelling correct; subgroup absence honest.
- Cl: Grey zone (5–20% 10-year) is the clinically actionable band — the question is right even if the vehicle is a predecessor model.
- L: The enhancer choice (Lp(a), apoB/LDL-C) is biologically apt.
- E adjudication — Weakness: "because the user requested explicit grey-zone treatment" — meta-language leak, must go. Severity: MAJOR (prose/provenance signal), MINOR (analysis placement).

**Methods—Literature verification ¶1.** Comparator PDFs checked; ledger/SciSpace/Elicit-derived tables; PubMed searches to 16 Aug 2026; Scite not callable; Perplexity auth error; not PRISMA.
- B/Cl/L: Defer to E.
- E adjudication — This is the manuscript's own tool-status disclosure and it is honest; my independent runtime agrees Scite/SciSpace/Elicit are not exposed here and network verification was declined in this session. Weakness: the claim "structured PubMed searches updated on 16 August 2026" is unverifiable from the manuscript alone — name the search strings/dates in supplement. Severity: MINOR.

### Results

**Results—Populations ¶1 (UKB).** 3,209; 289 events; 6.55/1,000 py (pre-correction descriptive); Table 1 differentials.
- B: Event rate implies ~44k person-years (mean ~13.7 y) — plausible to 31 Dec 2023; but median follow-up is never stated. Lipid SMDs (0.269) smaller than clinical-factor SMDs (0.38–0.48) — foreshadows the null lipid terms.
- Cl: Case-mix (older, male, hypertensive, diabetic) is clinically expected; smoking differential small (SMD 0.092) yet smoking enters the model — fine, age-adjusted.
- L: Untreated-equivalent non-HDL 5.12 vs 4.70 mmol/L among future cases vs non-cases — modest; consistent with attenuated carrier phenotype.
- E adjudication — Weakness: follow-up summary absent; "pre-correction descriptive output" inside primary Results muddies frame provenance. Severity: MODERATE.

**Results—Populations ¶2 (Wales).** 1,169/102; pre-correction descriptives withheld; corrected Welsh Table 1 absent.
- B: FATAL-2 lives here.
- Cl/L: Cannot clinically characterise the transport cohort — unacceptable for a journal.
- E adjudication — Required improvement: regenerate and insert corrected Welsh Table 1 and follow-up before any submission. Severity: FATAL.

**Results—Predictor-level ¶1.** Diabetes HR 2.120 (1.610–2.793); sex 1.702; hypertension 1.610; smoking NS; all three lipid terms NS.
- B: Table 2 arithmetic verified (exponentiated betas reproduce reported HRs; per-raw and per-SD intervals mutually consistent). Effect-before-p ordering respected. Correctly "associated with" throughout.
- Cl: Diabetes as dominant modifiable clinical factor in carriers is plausible and clinically actionable (aggressive risk-factor management), and no de-risking language appears.
- L: Null lipid terms in an FH-carrier model is *the* finding a lipid reviewer will interrogate; the differential-measurement-error explanation (fixed correction factor; r=0.32; treatment-suppressed measurements; restricted lipid range within a carrier stratum) belongs in Results-adjacent interpretation, not only Discussion.
- E adjudication — Severity: MINOR (reporting), MODERATE (interpretive adjacency).

**Results—Predictor-level ¶2.** Increment over age+sex +0.041; ≈+0.033 from hypertension/diabetes/smoking; ≈+0.008 lipid apparatus; model is a routine clinical-risk model, not proof of lipid construction.
- B: Decomposition honest; but increments on different… (assumed same data) — the +0.033/+0.008 split attribution method unstated (sequential? Shapley-ish? single-term removal?) — name the method.
- Cl: Fine.
- L: This concedes the cumulative-lipid framing is not load-bearing; the title/abstract wisely avoid it.
- E adjudication — Weakness: attribution method unspecified. Severity: MODERATE.

**Results—Internal discrimination ¶1 (UKB).** OOF 0.7081/0.7043/0.7254; apparent 0.7154/0.7152/0.7449; optimism 0.0059/0.0072/0.0113 → corrected 0.7095/0.7079/0.7336; estimators agree ≤0.008.
- B: Arithmetic verified (0.7154−0.0059=0.7095 ✓; 10-year 0.7152−0.0072=0.7080 vs printed 0.7079 — 0.0001 rounding, trivial). 5-year optimism largest as expected (97 events).
- Cl/L: No objection; C≈0.71 is "moderate", correctly labelled.
- E adjudication — Severity: MINOR.

**Results—Internal discrimination ¶2 (Wales).** Pre-rescue 0.7653/0.7605/0.7590 "stated unchanged" after rescue; no synchronised file; provisional.
- B: A claim of "unchanged" without a regenerated file is an assertion, not evidence — either regenerate or delete.
- Cl/L: Defer.
- E adjudication — Severity: FATAL (part of FATAL-2).

**Results—Head-to-head ¶1.** SAFEHEART +0.070 (0.036–0.104), Holm p=0.0003; Montreal +0.032 (0.011–0.055), p=0.0179; FHRS +0.015 (−0.011–0.040), p=0.5018 — tie.
- B: Subset arithmetic coherent (Montreal subset 2,811 ≈ HDL-complete; FHRS 1,913/146 consistent with age ≤65 + complete inputs). Effect-first reporting, correct tie language.
- Cl: The wins are real within their frame; the frame favours CALON-C structurally (SAFEHEART previous-ASCVD = 0 by design; suppressed measured LDL-C). The Discussion owns this; the Results sentence does not — one clause would fix it.
- L: Note the FHRS tie is the most decision-relevant result: parity without Lp(a).
- E adjudication — Suggested addition: "in an incident primary-prevention frame in which SAFEHEART-RE's previous-ASCVD term is zero and its LDL-C input is frequently treatment-suppressed". Severity: MAJOR.

**Results—Head-to-head ¶2 (SAFEHEART correction moved +0.032→+0.070).**
- B: Correct disclosure; but a correction that doubled the headline win must carry an audit note that blinded re-verification of the comparator transcription was performed after the direction of movement was known.
- Cl/L: The untreated-LDL sensitivity retained is the comparator-favourable guard — right.
- E adjudication — Required improvement: state who/when re-verified the corrected SAFEHEART transcription. Severity: MODERATE.

**Results—Head-to-head ¶3 (five-year nulls).** +0.081 (0.020–0.150) Holm p=0.0560; +0.044 (0.003–0.090) p=0.1413; FHRS +0.018 (−0.032–0.069) p=0.5018.
- B: CIs exclude zero nominally at 5 years yet Holm-adjusted p's >0.05 — coherent under Holm (multipliers 4–5 on raw p's ~0.014–0.047); raw 5-year p's not printed anywhere (supplement gap).
- Cl: 5-year is the clinically relevant near-term horizon the guideline quote invokes; nulls there are consequential and correctly not spun.
- E adjudication — Severity: MINOR (print raw p's in supplement).

**Results—Head-to-head ¶4 (Wales).** SAFEHEART 40/1 and FHRS 132/6 non-estimable; Montreal 750/60, +0.033 (−0.014–0.090) tie; Lp(a)-omitted all ties.
- B: Correct refusal to estimate 1-event and 6-event cells; implementability finding is genuinely informative.
- Cl: This is the most practice-relevant Welsh result: the scores cannot even be computed in a real national registry.
- L: Native Welsh Lp(a) mixed units — a classic real-world lipid-data failure; worth one clause naming the remediation (assay metadata).
- E adjudication — Severity: MINOR (well handled).

**Results—Head-to-head ¶5 (tally caveat).** No comparator beat CALON-C anywhere; explicitly not non-inferiority proof.
- All seats: correct; E: keep verbatim. Severity: MINOR.

**Results—Calibration ¶1–3.** 10-y slope 1.101 (0.884–1.318), E:O 1.008; 5-y slope 1.197, E:O 1.004; scaled Brier 3.3%/1.8%; internal-only framing; empty lowest 5-year decile; worked examples 0.78/1.62% and 15.99/30.42%.
- B: E:O against KM overstates observed risk under competing mortality (small here); slope CIs cross 1 — honest. Worked examples verify arithmetic only — correctly labelled. Welsh rows in Table 5 lack any textual interpretation and their provenance (which equation, which frame) is ambiguous.
- Cl: A 30.42% 10-year high-profile prediction in a model without competing-risk validation must not circulate as a threshold — labelled; good.
- L: No objection.
- E adjudication — Weakness: Welsh calibration rows orphaned from text; competing-risk caveat implicit. Severity: MODERATE.

**Results—Transport ¶1–2.** UKB→Wales C=0.7252; Wales→UKB C=0.6600; asymmetry interpretation; 7-term Welsh fit caveat; ΔC≈−0.030 dated-only bound.
- B: No CIs, no SEs, no test of the asymmetry — with 102 events the Welsh-side SE is ~0.03, so 0.725 (≈0.66–0.79) overlaps 0.66 substantially; the "asymmetry" narrative may be noise. This is the paragraph's central unquantified claim.
- Cl: Directionally plausible (clinic registry more severe phenotype → better ranking); but unquantified.
- L: Asymmetry attribution to lipid severity is speculative without the phenotype data presented side by side.
- E adjudication — Required improvement: add bootstrap CIs to both transport C's and soften the asymmetry attribution to "compatible with, not demonstrative of". Severity: MAJOR.

**Results—PH/competing ¶1–2.** 0/16 violations; Wales CIF 6.02%/11.97%, 35 competing deaths; UKB did not execute.
- B: See Methods PH power comment; "35 competing deaths among 102 events" is ambiguous wording (deaths among the 1,169, alongside 102 events) — Table 5's "in corrected frame" is clearer.
- Cl: Competing deaths at ~one-third of event count is substantial; UKB absolute-risk interpretation blocked — correctly escalated in Discussion as "not a cosmetic gap".
- E adjudication — Severity: MAJOR (the gap), MINOR (wording).

**Results—Missing data ¶1.** UKB missingness 12.4%/5.0%/22.5%, indicators not outcome-associated; Wales BMI 54.5%, diabetes 41.6%, smoking 26.4%, Lp(a) unusable; implementation-finding framing.
- B: Missingness-indicator outcome tests are underpowered reassurance; MAR assumption untestable — wording ("explains why… non-evaluable… not intrinsically inferior") is exactly right.
- Cl/L: Concur; the scientific-vs-operational distinction is well drawn.
- E adjudication — Severity: MINOR.

**Results—Grey-zone ¶1–2.** 3,333 scored (predecessor frame); 1,685/218 in band; Lp(a) −0.0038 (−0.0089–0.0018); apoB/LDL-C +0.0146 (−0.0050–0.0330); both +0.0118; apoB/LDL-C associated (HR 1.154 per SD, 1.027–1.295) without ranking gain; "association ≠ reclassification ≠ utility".
- B: Implied base C differs by row (0.5986/0.5980/0.5984), i.e. each delta computed on a different complete-input subset — undisclosed in Table 6's footnote; deltas therefore not strictly row-comparable. Negative teaching point correct.
- Cl: Clinically useful negative: do not order tests for reclassification without demonstrated band-specific gain.
- L: The apoB/LDL-C association-without-discrimination pattern is classic discordance biology and worth the explicit sentence it receives.
- E adjudication — Required improvement: footnote the per-row evaluable subsets. Severity: MODERATE.

**Results—Subgroups ¶1.** None supplied; declared gap.
- All seats: honest; acceptable only because declared. Severity: MINOR.

### Discussion

**Discussion—Principal findings ¶1–2.** Four defensible findings; "narrower than the initial hypothesis but more credible"; both-direction corrections.
- B: Accurate inventory.
- Cl: Appropriate restraint.
- L: Finding four (grey-zone) is predecessor-model output — repeating it as a "finding" of this study edges past its own caveat.
- E adjudication — Suggested wording: finding four should read "in an ancillary analysis of a predecessor model, specialised biomarkers did not significantly improve within-band discrimination". Severity: MODERATE.

**Discussion—Genuinely new ¶1–2.** Not first FH model/score/evaluation; defensible contribution = common-data comparator-faithful evaluation + parsimony; "first identified head-to-head application… in the present corrected frame"; priority to be rechecked.
- B: Novelty self-assessment matches the literature structure I know.
- Cl: Incremental-but-useful is the right register.
- L: Correct that population-frame head-to-head is uncommon.
- E adjudication — The narrowed priority sentence ("first identified… within the present corrected UK Biobank carrier frame") is so qualified it carries little priority value; that is honest, and should be kept exactly so. Overlap analysis: closest works are REFERCHOL (external SAFEHEART evaluation, different setting), McKay 2022 (single-model external validation), Tamehri Zadeh 2025/2026 (multi-score validation in Australia, genetically confirmed clinic patients). Residual novelty: same-participant scoring of three instruments plus a new routine-panel model in a population-ascertained carrier frame with reciprocal registry transport. Severity: MINOR.

**Discussion—Comparison ¶1 (SAFEHEART).** C=0.85 derivation → 0.77–0.78 REFERCHOL → 0.67 English care; +0.070 interpreted as setting-specific, not intrinsic superiority.
- B: Transport-decay narrative consistent with the cited pattern; the structural-zero and suppressed-LDL explanation is the correct interpretation.
- Cl: Excellent clinical contextualisation.
- L: Correct that specialist-visit measured LDL-C carries information this frame cannot supply.
- E adjudication — Verify the 0.85/0.81 derivation C's and 0.77–0.78/0.67 externals against refs 3,7,8 (unverified this session). Severity: MAJOR (verification), MINOR (prose).

**Discussion—Comparison ¶2 (Montreal).** Benchmark-across-estimands framing; age-as-exposure-proxy kinship.
- B: Correct that a prevalent-disease score vs incident ranking is an estimand-mismatched benchmark — and the paper says so.
- Cl/L: Concur; L: Montreal's off-treatment lipid measurement is the key design difference, correctly noted.
- E adjudication — Severity: MINOR.

**Discussion—Comparison ¶3 (FHRS "strongest comparator").**
- B: "Strongest" is inferred across *different evaluable subsets* (FHRS C 0.6836 on an age-≤65 subset vs SAFEHEART 0.6308 on all ages) — cross-subset C comparison is case-mix-confounded; the claim should rest on design features only, or on a same-subset three-way run.
- Cl: Agrees with B; the clinical conclusion (tie with the incident-designed score is the informative result) survives.
- L: FHRS's untreated/imputed LDL plus Lp(a) is the best lipid design; "strongest" is defensible on inputs, not on these C's.
- E adjudication — Suggested wording: "FH-Risk-Score was the most demanding comparator by design and evaluable-set; its statistical tie with CALON-C is more informative than either significant comparison." Severity: MAJOR.

**Discussion—Comparison ¶4 (guideline).** 2026 guideline caution; CALON-C below adoption threshold.
- B/Cl/L: Concur conditionally.
- E adjudication — Ref 1 verification dependency again (FATAL-3). In-window fallback framing available via ref 2 and the in-window 2018 AHA/ACC guideline. Severity: FATAL (contingent).

**Discussion—Parsimony ¶1–2.** Lower data requirement; scalability; "candidate first-line ranking layer"; not an argument against specialised biomarkers.
- B: Fine.
- Cl: The equity argument (inputs absent where gaps are largest) is the paper's best clinical paragraph.
- L: "At least once-in-adulthood Lp(a)" is guideline-consistent (ref 2, in-window; ref 1 unverified).
- E adjudication — Severity: MINOR.

**Discussion—Lipid terms ¶1–2.** Causal-vs-predictive distinction; restricted range, therapy-altered measurement, age-as-duration; +0.008 reported not hidden; "not a cumulative-lipid mechanism".
- B: Textbook-correct on within-stratum prediction; add regression-dilution from the fixed correction factor as a named mechanism.
- Cl: Reassuring and safe: no reader can mistake this for "LDL doesn't matter".
- L: The paragraph is right but incomplete: it omits the differential-error explanation the Methods data (r=0.32, MAE 1.20) directly supply. Also add: among carriers, treated LDL variance compresses upward risk gradient — Mendelian randomisation and cumulative-exposure literature (refs 22, 23, 34 — 23 and 34 are orphans; 23 Ference 2017 is in-window, cite it) support the causal framing.
- E adjudication — Required improvement: cite refs 22/23/34 here (cures three orphans) and add the differential-error sentence. Severity: MODERATE.

**Discussion—Ascertainment ¶1–3.** UKB not random sample; volunteer selection alters associations; carrier flag ≠ clinical FH; +0.15–0.23 mmol/L attenuation; calibration transport failure precedent.
- B: Selection-bias citations apt (refs 19–21, in-window); the point that volunteer selection can alter *associations* (not just rates) is the stronger and correct one.
- Cl: The attenuation sentence is the paper's most under-weighted fact: these carriers' untreated LDL-C barely exceeds non-carriers — external reviewers will ask whether the headline comparisons are even about FH.
- L: This is the tension centre: plausible explanations include flag breadth (hypomorphic/missense-heavy spectrum), early treatment, survivor attenuation; each has different implications and the data cannot separate them — say so explicitly, and elevate the number to Results/Table 1 (it is currently nowhere quantified in the cohort description itself).
- E adjudication — Weakness: the defining phenotype fact is buried and unquantified in Table 1; ref 14 (Trinder, in-window, orphan) is the natural citation here. Required improvement: surface the attenuation in Results ¶1 and Abstract ¶1; cite ref 14; move ref 18 (Sudlow 2015, out-of-window) to historical note. Severity: MAJOR.

**Discussion—Survivor bias ¶1–2.** Both cohorts survivor-selected; age spline models survivor hazard; needs left-truncated prospective family cohorts; "not a lifetime penetrance model".
- B: Correct and not correctable by adjustment — right.
- Cl: Clinically important against over-reading absolute risks in young carriers.
- L: Consistent with attenuation argument.
- E adjudication — Severity: MINOR.

**Discussion—Predictor timing ¶1–2.** 55/92 events had BP recorded post-event; attestation/plausibility/comparator-symmetry/ΔC≈0.030 bound; none proves baseline timing; dated-only model is a different specification.
- B: Exemplary epistemics: bound provided, claim refused.
- Cl: The 55/92 number is arresting; the refusal to over-claim saves the paper.
- L/E: Concur. Severity: MINOR (well handled), MAJOR as inherent limitation (already counted under FATAL-2 family).

**Discussion—Calibration drift ¶1–2.** Rank preserved, levels drift; no thresholds outside development data; tie ≠ adoption; adoption requires untouched validation + net benefit + decision impact.
- All seats: correct; the adoption checklist matches the BMJ series (refs 26–28 — cite them here, curing orphans). Severity: MINOR.

**Discussion—Lp(a)/apoB/grey zone ¶1–2.** Design choice not biology denial; CAC adds to SAFEHEART (ref 12, in-window); association ≠ reclassification ≠ utility; the standard a credible enhancer study must meet.
- B: The enhancer-study standard (frozen base, untouched cohort, movement in cases/non-cases, calibration + decision curves with intervals) is correctly specified.
- Cl: Safe: no test-ordering recommendation made.
- L: Correct on binary-Lp(a)-threshold critique implicit in the grey-zone null; CAC point accurate per ref 12 (UNVERIFIED this session, high prior).
- E adjudication — Ref 1 dependence again. Severity: MODERATE (verification), MINOR otherwise.

**Discussion—Competing risks/endpoint ¶1–2.** Missing UKB analysis "not a cosmetic gap; blocks definitive probability interpretation"; endpoint harmonisation agenda.
- B: Correct severity self-assessment.
- Cl: The hard-coronary sensitivity promise should be executable now on the 147 unambiguous cases — underpowered but informative; offering it would pre-empt a reviewer demand.
- E adjudication — Severity: MAJOR (gap), with a constructive note: run the coronary-only sensitivity on the unambiguous subset.

**Discussion—Ancestry/fairness ¶1–2.** European-ancestry derivation; ancestry unavailable in frame; multi-ancestry validation agenda; subgroup-C insufficiency.
- B: Correct that subgroup C's without interaction/paired-difference evidence and events are insufficient.
- Cl: Lp(a) distribution differences across ancestries make the Lp(a)-free design partly fairness-relevant — a point the paper could make but doesn't.
- L: Agrees with Cl — worth one sentence.
- E adjudication — Severity: MINOR.

**Discussion—Overlap/leakage ¶1–2.** FHRS 499-UKB overlap; programme-level prior examination of both cohorts; remedy = third cohort, locked protocol; "'external validation' is too strong".
- All seats: correct; complies with the no-Wales-as-external-validation rule. Severity: MINOR. (Verification of "499" remains open.)

**Discussion—Clinical implications ¶1–2.** Methodological implications; candidate ranking tool; never de-risk or defer guideline-directed treatment.
- Cl: The de-risking prohibition is exactly the safety sentence this field needs; keep verbatim.
- B/L/E: Concur. Severity: MINOR.

**Discussion—Strengths ¶1 / Limitations ¶1.** Accurate inventories; limitations list is complete and correctly ordered (external validation first).
- B: Limitation three (Welsh propagation) is FATAL-2 and correctly self-identified.
- E adjudication — The limitations are so complete they function as the reviewer's checklist; that is a strength for revision, not for acceptance. Severity: MINOR (as prose).

**Conclusion ¶1.** Matches evidence; no deployment/threshold/superiority claims.
- All seats: calibrated; keep. E: Severity: MINOR (none).

---

## 3. Whole-manuscript analyses

### A. Novelty map
- **Genuinely new (to my knowledge, pending ref verification):** same-participant, complete-input, multiplicity-controlled head-to-head of three published FH instruments in a population-ascertained LDLR-carrier frame; reciprocal frozen-equation transport between a population cohort and a national genotype-positive registry; quantified evaluability failure of Lp(a)-dependent scores in a real registry (40/1 and 132/6).
- **Incremental but useful:** a published raw-unit routine-panel equation with full reproduction constants; comparator-fidelity corrections (measured LDL-C; ever-smoking; age gate) with direction disclosure; the treatment-reconstruction audit (MAE 1.20 mmol/L, r=0.32) as empirical evidence against fixed-factor back-calculation.
- **Already established:** FH risk scores exist (refs 3,4,6); transport decay of SAFEHEART-RE (refs 7,8); multi-score validation in genetically confirmed patients (refs 9,10); cumulative-exposure rationale (refs 22,23); UKB selection bias (refs 19–21).
- **Unsupported priority claims:** none asserted beyond the heavily qualified "first identified head-to-head application… within the present corrected frame" — which is supportable only after the promised pre-submission recheck and should cite refs 9/10 as the nearest rivals. The closest overlapping work is Tamehri Zadeh et al. (refs 9/10): multi-instrument evaluation in genetically confirmed FH; residual CALON-C novelty is population ascertainment, same-participant pairing with multiplicity control, and reciprocal transport — but the overlap is close enough that the priority sentence must remain as narrowly worded as it currently is.

### B. Agreement/disagreement with recent evidence
- **REFERCHOL (ref 7):** agreement — transport depends on setting; CALON-C's asymmetric transport replicates the pattern. Classification of any tension: population/ascertainment-driven.
- **McKay 2022 (ref 8):** agreement — discrimination persists while calibration fails on transport; CALON-C pre-empts by making no transported-calibration claim. No conflict.
- **Tamehri Zadeh 2025/2026 (refs 9,10):** partial tension — their SAFEHEART-RE incident C (0.767) exceeds what CALON-C's frame yields for SAFEHEART (0.6308). Classification: population/ascertainment-driven (genetically confirmed clinic patients with specialist LDL-C/Lp(a) data vs attenuated population carriers) plus endpoint/estimand-driven (event mix differences). This comparison actually *supports* CALON-C's interpretation rather than threatening it — but only if the attenuation phenotype is surfaced (see MAJOR point).
- **Guideline position (refs 1,2):** agreement in principle; verification of ref 1 outstanding.
- **Cumulative-exposure literature (refs 22,23):** apparent tension — lipid causal centrality vs null lipid terms. Classification: methodological (restricted within-stratum range, treatment distortion, regression dilution from fixed correction factors), *not* substantive biological disagreement. The manuscript says this; add the dilution mechanism.

### C. Internal consistency audit (within-manuscript only; no recalculation from data)
Passed: cohort arithmetic (3,540−207−124=3,209; 2,405−344−185−58−649=1,169; 92+10=102; 1,159+10=1,169); event counts (289/97/194; 102/51/75) identical across Abstract, Results, Tables 3/5; Table 2 betas exponentiate to the printed HRs and per-raw/per-SD intervals are mutually consistent; optimism subtractions reproduce (trivial 0.0001 rounding at UKB 10-year); Holm-adjusted p's are exactly reconstructable as a six-cell family (6×0.00005=0.0003; 5×0.00358=0.0179; 4×0.0140=0.0560; 3×0.0471=0.1413; 2×0.2509=0.5018); subset sizes coherent with missingness (Montreal 2,811 ≈ HDL-complete; SAFEHEART 2,470 ≈ Lp(a)-complete); Welsh rescue counts (44→51 by 5 y; 66→75 by 10 y; ≤10 rescued) consistent; 16 PH terms = 9 UKB + 7 Welsh ✓; missingness percentages identical in text and Table 1; the 649-vs-659 Welsh exclusion discrepancy is self-flagged in the TRIPOD appendix.
Failed/flagged: (i) transport C's appear in four places, never with intervals; (ii) 5-year raw p's never printed; (iii) Table 6's implied base C differs by row (0.5986/0.5980/0.5984) without a subset footnote; (iv) "35 competing deaths among 102 events" wording vs Table 5's clearer phrasing; (v) Table 5 Welsh calibration rows lack any textual interpretation or equation provenance; (vi) Welsh internal C asserted "unchanged" post-rescue without a synchronised file; (vii) 19 uncited references vs citation of out-of-window refs 15, 18, 39; (viii) pre-correction descriptive figures (6.55/1,000 py) inside primary Results without a corrected follow-up table; (ix) identical Holm p=0.5018 for both FHRS horizons — consistent under Holm monotonicity, but worth a footnote since readers will suspect a copy error.

### D. Reporting and publication audit
- **TRIPOD+AI:** substantially addressed with self-audited open items; items 9 (imputation uncertainty), 13 (fairness), 14b (flow count 649/659), 17 (Welsh equation), 18 (external calibration/DCA/UKB competing risk), 20/21 (overlap), 24–27 (governance) unresolved — the manuscript says so itself. Source-of-truth discipline is exemplary.
- **PROBAST:** predictor-timing risk in Wales (high, disclosed); outcome date attribution (moderate-high, disclosed); analysis (penalty selection undisclosed; confirmatory family defined post hoc); participants (selection bias, disclosed). Overall: high transparency, residual high RoB in transport arm.
- **STROBE/RECORD:** flow, eligibility, and missing-data reporting good; RECORD 1.3 variant validation impossible (disclosed); Welsh linkage-quality/end-date absent.
- **Citation fidelity:** the weakest audit domain — 19 orphan references, 3 cited out-of-window, 2 marginally out-of-window (June 2016), 1 load-bearing unverified guideline, several quoted C-statistics unverified.
- **Journal fit:** as written, fits *J Clin Lipidol*, *Atherosclerosis*, or *Eur J Prev Cardiol* after revision. Not yet credible at *Circulation*/*JACC*/*Eur Heart J* tier: no untouched external validation, no competing-risk complete absolute risks, no decision-analytic utility. The paper's own honesty makes the mid-tier specialist fit a feature, not a failure.

### E. Top ten revisions (ranked)
1. **(FATAL)** Regenerate the full corrected Welsh artefact set (Table 1, follow-up, discrimination, calibration, equation) from one pipeline of record; remove "stated unchanged" assertions.
2. **(FATAL)** Supply governance front-matter: ethics/legal basis, funding, conflicts, PPI, data controller, code/model availability.
3. **(FATAL)** Verify ref 1 against the publisher record; if unverifiable or misquoted, reframe Introduction ¶1, Discussion—Comparison ¶4 and Discussion—Lp(a) ¶1 around ref 2 and the in-window 2018 AHA/ACC and 2019 ESC/EAS guidelines.
4. **(MAJOR)** Add bootstrap 95% CIs to both transport C-statistics; soften asymmetry attribution.
5. **(MAJOR)** Execute the UKB competing-risk analysis (fix the `death`-column guard); report CIF beside the KM-based calibration and the worked examples.
6. **(MAJOR)** Repair the reference apparatus: cite or delete the 19 orphans (refs 22, 23, 26–28, 34 have natural homes identified above); move refs 15, 18, 39 to an Excluded historical context note; verify refs 8, 9, 10 and all quoted C-statistics; correct the ref-10 content mismatch at Introduction ¶3.
7. **(MAJOR)** Surface the phenotype attenuation (+0.15–0.23 mmol/L) into cohort description and Abstract framing; state explicitly that comparator tests here are applicability tests in an attenuated carrier population.
8. **(MAJOR)** Purge meta-language ("user-specified", "the user requested", "the later reviewer response judged"); convert revision-history prose into neutral methodological prose; move the traceability note and unresolved-items register to supplement.
9. **(MAJOR)** Reword "FH-Risk-Score was the strongest comparator" to a design-based claim or supply a same-subset three-way comparison; add one sentence on points-chart tie attenuation of comparator C.
10. **(MODERATE)** Methods completions: ridge-penalty provenance; tg_filter +0.1 justification; Lp(a) ÷2.15 conversion sensitivity; increment-decomposition method; 5-year raw p's and per-row grey-zone subsets in supplement; hard-coronary sensitivity on the 147 unambiguous cases.

### F. Inter-panel tension memo
- **B predicts strongest disagreement with L:** B reads the null lipid terms as expected within-stratum behaviour plus measurement error and considers the matter closed; L considers the null partly *manufactured* by the fixed ÷0.70 correction (differential error in high-intensity-treated carriers) and wants that mechanism named as a first-class limitation, not a passing audit statistic. Neither has data to settle it; the honest output is to print both mechanisms.
- **Cl predicts strongest disagreement with B:** Cl wants a hard-coronary sensitivity now; B counters that 147 unambiguous events with component heterogeneity yields an underpowered, still-contaminated analysis. Resolution: run it, report as exploratory with interval-first language.
- **E predicts disagreement with all three:** the scientists treat the orphan-reference/window/meta-language problems as cosmetic; E treats them as trust-destroying at editorial triage — a paper that narrates its own pipeline ("user-specified") invites desk rejection before methodology is ever read.
- **All three vs E on timing:** B/Cl/L would accept submission after FATAL-2/3 fixes; E insists the attenuation reframing (rev. 7) changes the paper's *claim identity* and must precede any submission decision.

---

## 4. Research-tool status table

| Tool | Status | Detail |
|---|---|---|
| Scite | **NOT EXPOSED/NOT CONFIGURED** | No Scite tool exists in this runtime's tool catalogue (only Google Drive MCP tools are exposed). The manuscript's own Methods agrees ("Scite was not callable in the local runtime"). |
| SciSpace | **NOT EXPOSED/NOT CONFIGURED** | No SciSpace tool callable in this runtime. |
| Elicit | **NOT EXPOSED/NOT CONFIGURED** | No Elicit tool callable in this runtime. |
| PubMed / NCBI Entrez (skill script) | **AVAILABLE BUT FAILED** | `scripts/pubmed_search.py` exists in the `ai-literature-connectors` skill but requires outbound HTTPS; network access was declined in this session, so no record was retrieved. |
| Crossref / DOI.org validation (skill script) | **AVAILABLE BUT FAILED** | Same network constraint; a direct Crossref `api.crossref.org/works/...` fetch was attempted twice and rejected by the user. |
| Native web search | **AVAILABLE BUT FAILED** | Two targeted searches (2026 ACC/AHA guideline; Tamehri Zadeh Australian validation) were attempted and rejected by the user. |
| Native URL fetch | **AVAILABLE BUT FAILED** | Two Crossref API fetches rejected by the user (10.1161/CIR.0000000000001423; 10.1161/CIRCULATIONAHA.116.024541). |
| `/academic`-style skill (`ai-literature-connectors`) | **USED — instructions read, no results returned** | The skill file was read and its routing rules applied; every route it prescribes terminates in a connector or network call unavailable in this runtime. |

Consequence: per protocol, no reference is treated as verified. Classifications below use model-internal bibliographic knowledge, flagged as prior strength, and every load-bearing item is marked accordingly.

## 5. Eligible evidence ledger (window 17 Aug 2016 – 17 Aug 2026)

| # | Reference | In window? | Verification status this session | Role in manuscript |
|---|---|---|---|---|
| 1 | 2026 ACC/AHA dyslipidaemia guideline, *Circulation* 2026;153:e1154–e1276 | If real, yes | **UNVERIFIED — DO NOT CITE** (cannot corroborate existence, volume, pages, DOI 10.1161/CIR.0000000000001423, or the quoted FH passage) | Load-bearing ×3 paragraphs |
| 2 | 2025 ESC/EAS focused update, *Eur Heart J* 2025;46:4359–4378 (ehaf190) | Yes | UNVERIFIED — high internal prior | Guideline support |
| 3 | SAFEHEART-RE, Pérez de Isla et al., *Circulation* 2017;135:2133–2144 | Yes (May 2017) | UNVERIFIED — high prior; description internally consistent | Comparator |
| 4/5 | Montreal-FH-SCORE, Paquette et al., *J Clin Lipidol* 2017;11:80–86 and 1161–1167 | Yes | UNVERIFIED — high prior | Comparator |
| 6 | FH-Risk-Score, Paquette et al., *ATVB* 2021;41:2632–2640 | Yes | UNVERIFIED — high prior; the 3,881-n and 499-UKB claims need supplement-level confirmation | Comparator + overlap claim |
| 7 | REFERCHOL, Gallo et al., *Atherosclerosis* 2020;306:41–49 | Yes | UNVERIFIED — high prior | Transport precedent |
| 8 | McKay et al., *Atherosclerosis* 2022;358:68–74 | Yes | UNVERIFIED — moderate-high prior; quoted C=0.67 and miscalibration must be checked | Calibration-failure precedent |
| 9 | Tamehri Zadeh et al., *Atherosclerosis* 2026;418:120799 | Yes (if real) | **UNVERIFIED — DO NOT CITE** specific C values (0.767/0.735) until confirmed | Priority-adjacent rival |
| 10 | Tamehri Zadeh et al., *Can J Cardiol* 2025;41:2244–2251 | Yes | UNVERIFIED — moderate prior; cited for a clause it may not support | Priority-adjacent rival |
| 11 | Zamora et al., *Eur Heart J Digit Health* 2025;6:1113–1123 | Yes | UNVERIFIED — moderate prior | "Dozens of variables" clause |
| 12 | Gallo et al., CAC in FH, *JACC Cardiovasc Imaging* 2021;14:2414–2424 | Yes | UNVERIFIED — high prior | Imaging enhancer |
| 14 | Trinder et al., *JAMA Cardiol* 2020;5:390–399 | Yes | UNVERIFIED — high prior; **uncited orphan**, natural home Discussion—Ascertainment | Ascertainment |
| 19–21 | Fry 2017 *Am J Epidemiol*; van Alten 2024 *Int J Epidemiol* 53:dyae054; Schoeler 2023 *Nat Hum Behav* 7:1216–1227 | Yes | UNVERIFIED — high prior | Selection bias |
| 22/23 | Domanski 2020 *JACC* 76:1507–1516; Ference 2017 *Eur Heart J* 38:2459–2472 | Yes | UNVERIFIED — high prior; **both uncited orphans** | Cumulative exposure |
| 24–28 | TRIPOD+AI (*BMJ* 2024;385:e078378); PROBAST (*Ann Intern Med* 2019;170:51–58); BMJ evaluation series (*BMJ* 2024;384:e074819/e074820/e074821) | Yes | UNVERIFIED — high prior; 26–28 **uncited orphans** | Methods standards |
| 34–38 | Ference 2016 NEJM (Dec 2016, in window); Sniderman 2019; Boot 2019; Garg 2020; Akyea 2020 | Yes | UNVERIFIED — high prior; **all uncited orphans** | Various |
| Suggested additions | 2018 AHA/ACC cholesterol guideline (Grundy et al., *Circulation* 2019;139:e1082–e1143, published Nov 2018); 2019 ESC/EAS guideline (Mach et al., *Eur Heart J* 2020;41:111–188) | Yes | UNVERIFIED — high prior | Fallback anchors if ref 1 fails |

**Excluded historical context (may be named as history, never as evidence):** Tybjærg-Hansen 2005 (ref 15 — currently load-bearing in Introduction ¶3; must be demoted); Sudlow 2015 (ref 18); RECORD/Benchimol 2015 (ref 39 — acceptable only as a reporting-standard citation); Debray 2015 (ref 29, also an orphan); Law & Wald 2003 (ref 30); Jansen 2004 (ref 32); Cohen 2006 (ref 33); Khera et al., *JACC* 2016;67:2578–2589 (ref 13 — 7 June 2016, ~10 weeks before the window; orphan regardless); VOYAGER (ref 31 — June 2016 print issue, marginally pre-window; orphan regardless).

---

## 6. Internal-panel debate (explicitly labelled exchange)

**L:** Your "strongest comparator" sentence and the SAFEHEART headline both dodge the same fact — in a carrier population with +0.2 mmol/L untreated LDL-C excess, no lipid-weighted score can shine, including CALON-C's own lipid terms. The paper's two headline wins are, in part, a phenotype statement wearing a methods costume.
**B:** Granted the estimand is applicability, not intrinsic quality — the manuscript already concedes this for SAFEHEART. But the tie with FH-Risk-Score survives your argument only if the FHRS subset's age gate isn't itself flattering FHRS. The correct summary is: within an attenuated population frame, routine clinical variables dominate ranking; no score demonstrated superiority in Wales. Everything else is commentary.
**Cl:** And clinically the safest sentence in the paper is the de-risking prohibition. My fear is quotation drift: "CALON-C out-discriminated SAFEHEART-RE" will travel without its qualifier. Put the qualifier inside the Abstract Results sentence itself, not three sections later.
**E:** All three of you are arguing about a paper that, today, would be desk-rejected for missing ethics and funding statements and for saying "the user-specified label" in Methods. Fix the provenance voice and the reference apparatus first; your scientific dispute is real but it is round two.
**B:** Conceded on order of operations; not conceded that the Welsh frame mixing is "logistical" — asserting estimates are "unchanged" after adding 10 events without showing the regenerated estimate is a statistical claim without evidence.
**L:** And the fixed-factor correction deserves a named place in the limitations as a mechanism of attenuation for the lipid coefficients — regression dilution is not a footnote.
**Cl:** I will trade: accept the exploratory hard-coronary sensitivity even if underpowered, in exchange for keeping the grey-zone analysis out of the Key points. A predecessor-model null does not belong in the paper's three-sentence public summary.
**E:** Adjudication: Cl's trade accepted; B's Welsh-regeneration demand is revision #1; L's dilution mechanism enters Limitations; the attenuation figure enters the cohort description. Disagreement recorded on whether the FHRS tie can be called "the most informative result" — B and Cl say yes on design grounds, L says only with the attenuation caveat attached. That disagreement should be visible in the revised Discussion, not smoothed.

## 7. Teaching section for Dr Genedy — the methodological lesson behind each major criticism

1. **Frame synchrony (FATAL-2).** A result asserted to be "unchanged" after a data correction is a new claim requiring new evidence, not a carry-over. Lesson: corrections propagate or they did not happen; the unit of reproducibility is the pipeline run, not the narrative. Encode the invariant as a test: every displayed Welsh number must trace to one run of one script.
2. **Comparator fidelity cuts both ways.** The SAFEHEART measured-LDL correction moved the result in your favour (+0.032 → +0.070). Corrections that help you require *more* audit than corrections that hurt, because reviewer suspicion is asymmetric. Lesson: document who re-verified the transcription, when, and against which primary artefact.
3. **A positive estimate with an interval crossing zero is a tie — and a tie is information.** The FHRS tie is your most decision-relevant finding because it prices the Lp(a) requirement: parity in ordering without a specialised assay. Lesson: report ties with the same prominence as wins; pre-register the non-inferiority margin if you ever want to claim more.
4. **Internal calibration is not transportable calibration, and KM is not competing-risk truth.** E:O against Kaplan–Meier ignores competing mortality; the UKB CIF failure blocks absolute-risk interpretation. Lesson: discrimination transports more easily than calibration — plan validation around calibration-in-the-large and slope first, not C.
5. **Within-stratum prediction ≠ aetiology.** Null lipid terms in a carrier cohort do not contradict LDL causality: restricted range, treatment distortion, and regression dilution from fixed correction factors each attenuate coefficients. Lesson: name the measurement-error mechanism explicitly or reviewers will name it for you.
6. **Evaluability is a scientific result.** SAFEHEART/FHRS being non-computable in Wales (40/1, 132/6) is a finding about data requirements, not a flaw in those scores. Lesson: report implementability alongside performance as a first-class endpoint.
7. **Citation apparatus is part of the evidence.** Nineteen orphan references, three out-of-window load-bearing citations, and one unverifiable guideline undo the trust your methods section earns. Lesson: every claim gets a verifiable, in-window, content-matched citation; every listed reference earns its place or is deleted.
8. **Provenance voice.** "The user-specified label…" tells an editor a pipeline wrote the paper. Lesson: manuscripts describe decisions ("the endpoint label MACE was not adopted because…"), not conversations.

## Claims that must be deleted unless new evidence is produced

1. **Every sentence quoting or paraphrasing ref 1's FH-specific guidance** (Abstract ¶1; Introduction ¶1; Discussion—Comparison ¶4; Discussion—Lp(a) ¶1) unless the 2026 ACC/AHA guideline's existence, authorship, DOI, and the quoted passage are verified against the publisher record. In-window replacements exist; use them if verification fails.
2. **The Australian C-statistics (0.767 SAFEHEART-RE; 0.735 FH-Risk-Score)** in Introduction ¶2 unless ref 9 is verified against *Atherosclerosis* 2026;418:120799.
3. **"FH-Risk-Score itself included 499 UK Biobank participants during derivation"** (Introduction ¶5; Discussion—New ¶1; Discussion—Overlap ¶1) unless verified against the Paquette 2021 primary paper/supplement. The overlap *caveat* should stay regardless; the number must be exact.
4. **All Welsh internal discrimination/calibration values (0.7653/0.7605/0.7590; Table 5 Welsh rows)** unless regenerated from the corrected 1,169/102 frame; the assertion "unchanged after the 10 rescued events" must be deleted or evidenced.
5. **The transport estimates as quantitative claims (C=0.7252; C=0.6600)** unless accompanied by 95% intervals; without them the asymmetry narrative ("compatible with differences in age range, clinical ascertainment…") is unquantified speculation and should be deleted or softened to direction-only language.
6. **"FH-Risk-Score was the strongest comparator"** as a performance claim, unless a same-subset three-way comparison is produced; otherwise replace with the design-based formulation.
7. **The clinic-vs-population phenotype claim resting on ref 15 (Tybjærg-Hansen 2005)** — out of window; delete as evidence or re-anchor to in-window ref 14 (Trinder 2020), keeping Tybjærg-Hansen only in an explicitly labelled Excluded historical context note.
8. **The Key-points grey-zone sentence** unless the analysis is rerun on the corrected CALON-C base model; a predecessor-model null cannot headline the paper's public summary.
9. **Any residual implication that absolute 5/10-year risks are interpretable in UK Biobank** (including the worked examples beyond arithmetic verification) until the competing-risk analysis executes and calibration is reconciled against cumulative incidence.
10. **The uncited reference block (refs 13, 14, 16, 17, 22, 23, 26–38 in their current orphan state)** — each must be either cited at a specific claim it genuinely supports within the window, or deleted from the reference list before submission.
