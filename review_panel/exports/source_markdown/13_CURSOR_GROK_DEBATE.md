I have the three reports, the manuscript tables, and local extracts that settle a few citation fights. The four seats will now challenge named claims without forcing agreement.

# GROK round 2 — cross-model four-seat debate

**Reviewed artefacts.** Blind round-1 reports from Kimi, Grok, and Claude in `ROUND_1_DOSSIER.md`; manuscript `outputs/manuscript_2026-08-16/CALON_C_MANUSCRIPT_HIGH_CALIBRE.md`; local Paquette 2021 extract; programme Gratton/ClinVar aggregate audit. No participant-level rows were opened. No other model’s *round-2* text was available.

**Research-tool status this session.** Scite, SciSpace, Elicit, Consensus: **NOT EXPOSED**. PubMed/Crossref/native web search: **NOT CALLED**. Local full-text extract of Paquette et al., *ATVB* 2021: **USED**. Programme Gratton/ClinVar aggregate file: **USED**. Manuscript tables: **USED**.

Convention: each seat answers first; the Editor-in-Chief adjudicates last. Disagreements are left standing unless the manuscript or in-window literature actually settles them.

---

## 1. Named claims under challenge

### Claim A — Kimi FATAL-3: “Reference 1 is unverified; do not cite; three load-bearing paragraphs collapse.”

**Biostatistician.** This is a *verification-status* claim, not a statistical one. Kimi’s runtime had no DOI resolution. That does not make the guideline disappear. Grok round 1 read a local publisher extract (*Circulation* 2026;153:e1154–e1276, DOI 10.1161/CIR.0000000000001423) and quoted COR 2b / COR 3: Harm. Claude resolved the same DOI and noted that Crossref lacks the printed page range. **I reject Kimi’s deletion order.** I accept Claude’s page-range caveat as MINOR bibliographic hygiene.

**Cardiologist.** The guideline sentence in the manuscript is clinically accurate *for heterozygous FH*. The error is juxtaposition: Abstract ¶1 and Introduction ¶1 apply HeFH guidance to an `ldlr_carrier` flag. That is Grok’s round-1 point, and I still hold it. Kimi wanted the citation deleted; I want the *population slide* deleted.

**Lipid-medicine specialist.** ACC/AHA 2026 is not a reason to write this paper. ESC/EAS 2025 already places FH in high / very-high risk pathways. Neither document licenses a new score as a treatment gate, and neither applies to a flag with untreated LDL-C IQR 3.32–4.68 mmol/L (manuscript Table 1).

**Editor-in-Chief.** **Resolved.** Do not delete ref 1 for non-existence. Keep the quotation only if it is labelled as HeFH guidance. Page range e1154–e1276 remains **unverified against Crossref in Claude’s session**; check the issue before submission. **Conflict class:** verification-scope (Kimi vs Grok/Claude), then **population/ascertainment-driven** (all three, once existence is granted). Kimi’s FATAL-3 is **overruled**.

---

### Claim B — Grok: “FH-Risk-Score derivation included 499 UK Biobank participants (verified).” Claude/Kimi: “UNVERIFIED from the abstract.”

**Biostatistician.** This is settled by the primary paper, not by abstracts. Local extract of Paquette et al., *ATVB* 2021, Methods: “the Montreal Clinical Research Institute FH cohort (n=482), the FH registry from British Columbia (n=335), **the UK Biobank (n=499)**, the Robarts Research Institute in Ontario (n=100), and the REFERCHOL FH registry from France (n=2465).” Claude’s UNVERIFIED tag was honest given abstract-only retrieval. It is no longer tenable.

**Cardiologist.** The overlap caveat stays. A TIE against a score that already saw 499 UK Biobank adults is even less of a victory, as Grok said. That does *not* prove those 499 sit inside the present 3,209; the manuscript correctly says no overlap file was supplied.

**Lipid-medicine specialist.** Paquette required DLCN ≥6 (74% molecularly confirmed) and age 18–65, with median untreated/imputed LDL-C about 6.65 mmol/L. This cohort’s median untreated-equivalent LDL-C is 3.95 mmol/L. Overlap of country is not overlap of phenotype.

**Editor-in-Chief.** **Resolved: 499 is in the primary paper.** Cite the Methods paragraph, not the abstract. Claude/Kimi “UNVERIFIED” is a **verification-scope** conflict, not a factual one. The stronger scientific point — phenotype non-equivalence — remains **population/ascertainment-driven** and is **not** resolved by verifying the 499.

---

### Claim C — Claude FATAL: “Carrier frequency 1 in 142 vs Gratton 1 in 288; the flag is not pathogenic FH.” Kimi: phenotype attenuation is only MAJOR. Grok: population–guideline mismatch is FATAL.

**Biostatistician.** Claude’s *direction* is right; the *arithmetic pairing* is slightly unclean. Gratton’s 488/140,439 is all-gene P/LP in a European WES subset, not LDLR-only in 501,936 rows. The cleaner manuscript-compatible facts are: 3,540/501,936 ≈ 1 in 142 for the flag; empty `variant_id`; untreated LDL-C excess +0.15 to +0.23 mmol/L (manuscript Discussion). Programme aggregate audit, not opened at participant level, reports ClinVar P/LP LDLR 890/501,936 and P/LP-or-LoF 1,264 — roughly one-quarter to one-third of the analysis flag. Eligibility is defined by the misclassified variable. That is a change of estimand, not a covariate bias. **I now side with Claude/Grok on FATAL for any HeFH claim.** Kimi’s “honest label” is honest in Methods and false in the title, keywords, and Key points.

**Cardiologist.** Table 1 is enough without genetics: median untreated-equivalent LDL-C 3.95 mmol/L (IQR 3.32–4.68) in people labelled as LDLR-variant carriers, 10-year observed risk 6.15%, 43% male, median age 57. That is not a clinic HeFH population I would treat from a score. Publishing S0(10)=0.949962 and a 6.20% worked example beside that label is a **patient-safety** problem, as I said in round 1. Claude’s “clinician would under-treat” is the same objection in stronger words. I adopt it.

**Lipid-medicine specialist.** Kimi buried the attenuation as a Discussion fact that “explains the SAFEHEART result.” That is backwards. The attenuation *is* the study. SAFEHEART-RE C=0.6308 here versus derivation 0.81 without prior ASCVD (Pérez de Isla 2017, in-window) is what you expect when you score a specialist HeFH equation in a mild, treated, volunteer flag. Claude’s 0.14–0.17 gap versus Tamehri 2026 is **population/ascertainment-driven** if those Australian C values hold; Grok/Kimi left Tamehri unverified. I will not bank 0.802 (primary prevention) until a publisher record is in *this* runtime. I *will* bank the derivation contrast and Table 1.

**Editor-in-Chief.** **Partially resolved.** FATAL to call this heterozygous FH or to let ACC/AHA HeFH recommendations frame the paper. **Not automatically FATAL** to a methods paper about a population-ascertained LDLR-coding-variant flag, if the title and abstract are rewritten. Kimi under-graded this. Claude slightly over-paired frequencies. Grok’s wording is the one I will keep: *not clinic HeFH*. **Conflict class:** population/ascertainment-driven. Named dissent: Lipid seat will not treat Tamehri’s 0.802 as verified in this runtime.

---

### Claim D — All three: Welsh 1,169/102 versus Table 3/5 1,159/92 is FATAL. Claude adds: Aalen–Johansen CIF 6.02% > Kaplan–Meier 5.40% is impossible in one risk set; inclusion was outcome-conditional.

**Biostatistician.** Frame mixing is confirmed in the manuscript itself (Table 3 status column; Table 5 footnote). Claude’s CIF>KM point is also confirmed: Table 5 prints Wales 5-year observed 5.40% beside CIF 6.02%, and 10-year 11.08% beside 11.97%. In one risk set, Aalen–Johansen for the event of interest cannot exceed 1−KM of that event, because KM censors competing deaths and inflates incidence. The footnote admits two frames. That is not a competing-risk subtlety; it is a broken table. Claude’s “rescue 10 events” objection is a **different** and valid point: keeping people without operational follow-up *if and only if* they had a dated event conditions membership on the outcome (Munafò et al., *Int J Epidemiol* 2018;47:226–235 — in window). Kimi treated this as STROBE-flagged censoring informativeness. That is too kind. Event rate moving 92/1,159 (7.9%) → 102/1,169 (8.7%) by construction is not a conservative correction.

**Cardiologist.** I concede Claude’s inclusion point, as Claude’s own cardiologist already did. I still dissent on *predictor dating*. Hypertension and diabetes in a national FH registry are chronic states. Demanding a timestamp before baseline for every comorbidity would empty most registries. Grok’s 55/92 events with blood pressure after the event is a real contamination bound (ΔC ≈ −0.030), not a reason to delete Wales. **Dissent preserved** against the biostatistician on predictor timing; **agreement** on outcome-conditional inclusion.

**Lipid-medicine specialist.** Wales is genotype-positive by a clinical field. That arm is closer to HeFH than UK Biobank. Ruining it with mixed frames and outcome-conditional rescue wastes the only molecular-looking cohort in the paper. Evaluability (SAFEHEART 40/1; FH-Risk-Score 132/6) survives even a messy risk set, because “cannot compute” is not a C-statistic.

**Editor-in-Chief.** **Resolved as FATAL for any Welsh numerical discrimination/calibration/CIF juxtaposition until one pipeline is regenerated.** Claude’s CIF>KM finding is **adopted**; Kimi and Grok missed it. Outcome-conditional inclusion is **MAJOR-to-FATAL for the transport headline**, not for a clearly labelled stress test. **Conflict class:** methodological (inclusion) plus implementation/calibration-driven (mixed artefacts). Cardiologist–biostatistician split on predictor dating is **unresolved**.

---

### Claim E — Claude: “No confidence interval on any C-statistic.” Kimi/Grok: transport CIs missing; head-to-head *deltas* have CIs.

**Biostatistician.** Both are true. Table 4 gives ΔC intervals, not intervals on 0.7003 or 0.6308. Table 3 and both transport values (0.7252, 0.6600) have none. TRIPOD+AI requires uncertainty on performance measures. With 102 Welsh events, 0.725 versus 0.660 may be a TIE. Claude’s code check — transport routine returns a point estimate only — is the right explanation. Kimi’s request to “add transport CIs” is necessary but incomplete: every C in Tables 3–4 needs an interval, then the asymmetry paragraph must be allowed to die if the difference includes zero.

**Cardiologist.** A Key points box quoting 0.725 and 0.660 without intervals will be quoted as validation. That is the clinical harm.

**Lipid-medicine specialist.** No objection beyond the biostatistician’s.

**Editor-in-Chief.** **Resolved.** Claude’s stricter statement is correct. Kimi/Grok were not wrong about deltas. **Conflict class:** methodological / reporting. Severity: MAJOR (blocking for transport-as-finding); not independently FATAL if transport is demoted.

---

### Claim F — Grok: “Confirmatory superiority is at the wrong horizon; 5-year Holm p=0.0560 is a TIE; SAFEHEART win is off-label.” Claude: 10-year cells exist, do not reverse, and were omitted. Kimi: less emphasis.

**Biostatistician.** Grok is right on estimand. SAFEHEART-RE’s published job is short-term incident ASCVD, including prior disease, using measured LDL-C and Lp(a). Here prior ASCVD is structurally 0, LDL-C is treatment-suppressed, and the retained win is *full follow-up* after the native 5-year test failed Holm. Claude adds that 10-year — FH-Risk-Score’s native horizon — was analysed and not shown. That is a reporting failure, not concealment, if the CSV truly does not reverse. I cannot re-open that CSV in this seat without repeating Claude’s check; I accept it as a named, code-level claim to verify, not as gospel.

**Cardiologist.** Ranking Montreal (prevalent CVD, Paquette 2017 *J Clin Lipidol*) against incident events and calling it “higher discrimination” is a category error. Grok’s “take Montreal out of the Holm family” is the clinical repair. Kimi noted the prevalent origin and still left it in the confirmatory story. Too weak.

**Lipid-medicine specialist.** Measured-LDL correction moving ΔC from +0.032 to +0.070 (manuscript source note) is comparator-faithful and *helps* CALON-C. Kimi’s lesson stands: corrections that help you need more audit, not less. Claude’s Lp(a) ÷2.15 point compounds this: Kronenberg et al., *Eur Heart J* 2022;43:3925–3946 (in window) states mass and molar units are not interconvertible by a fixed factor. That error hits SAFEHEART-RE and FH-Risk-Score only. Kimi’s “2.15 lies in 2.0–2.5” is not a rebuttal.

**Editor-in-Chief.** **Resolved as MAJOR, estimand-driven plus implementation/calibration-driven.** Headline cannot be “out-discriminated SAFEHEART-RE” without the setting qualifier *in the same sentence*. Montreal remains a ranking benchmark across estimands, not a confirmatory superiority cell — I adopt Grok/Claude over Kimi. **Unresolved:** whether the Holm family should be rebuilt (Grok/Claude) or left and caveated (implicit Kimi). Lipid seat’s differential-error claim is **adopted as a required sensitivity**, not yet as proof that the win is entirely artefactual.

---

### Claim G — Grok: publishing S0(5)/S0(10) is FATAL for patient safety. Kimi: MAJOR. Claude: “did not execute” is not a result; fix the code.

**Biostatistician.** Internal slope 1.101 (0.884–1.318) includes both 1 and material miscalibration. E:O 1.008 against Kaplan–Meier, with no competing-risk baseline, is nearly tautological in development data (Van Calster et al., *BMC Med* 2019 — Claude; I agree). Publishing the equation with two-horizon S0 makes a deployable object. That is a reporting decision with clinical consequences. I grade it **MAJOR-to-FATAL depending on venue**, not a statistical impossibility.

**Cardiologist.** **FATAL.** A 6.20% 10-year predicted risk in a cohort labelled LDLR-variant carriers will be misread as HeFH risk. The Discussion forbids de-risking; Table 2 invites it. Claude and I are aligned. Kimi under-weighted harm.

**Lipid-medicine specialist.** Agree with the cardiologist. Also: `cum_nonhdl = log(non-HDL × age)` is not cholesterol-years (Domanski 2020, currently an orphan). Grok and Claude are right; Kimi under-played the naming error.

**Editor-in-Chief.** **Resolved as FATAL to print a usable absolute-risk equation in the main text until UK Biobank CIF exists.** “Did not execute” must vanish. **Conflict class:** implementation/calibration-driven plus patient safety. Severity dissent (Kimi MAJOR vs Grok/Claude FATAL) is **editorial**: I take FATAL.

---

### Claim H — Claude unique strengths: head-to-head used out-of-fold CALON-C predictions; Welsh comparisons used a 7-term refit, not the frozen equation.

**Biostatistician.** If the code check holds, this is the best design choice in the package and is invisible in the Methods. Kimi and Grok missed it because they did not open `code/33_CALON_C.py`. I adopt it *conditionally* on that code remaining as Claude described. The Welsh 7-term refit means “no Welsh head-to-head superiority” is **not** a test of the frozen UK Biobank equation. That is an identity error in the abstract.

**Cardiologist / Lipid-medicine specialist.** Defer. If true, it is a reporting defect, not a clinical one.

**Editor-in-Chief.** **Adopted as a named strength that must be written into Methods**, and as a named abstract error for Wales. **Conflict class:** implementation. Not a cross-model contradiction — an *omission* by Kimi/Grok.

---

### Claim I — Claude: specification-search optimism unquantified (CALON-N/F/H/H2/11/C). Kimi: penalty 0.02 provenance MODERATE. Grok: penalty not nested-CV selected.

**Biostatistician.** Claude is right and the others were too mild. Repeated CV corrects coefficient optimism inside a fixed specification. It does not correct the fact that the nine terms, the age-50 knot, ridge 0.02, and 0.70/0.80 divisors were chosen on these data across generations. Riley *Stat Med* 2019 (sample size) and TRIPOD+AI item 10 are the standards. Unquantified residual optimism is **MAJOR**, not FATAL.

**Editor-in-Chief.** **Adopted.** File names out of the manuscript; the *count of specifications* stays. **Conflict class:** methodological.

---

### Claim J — Citation apparatus: 19 orphans (all three); Claude: ref 9 title is wrong; ref 10 miscited; all 39 DOIs resolve. Kimi: ref 1 unverified; Grok: Tamehri/REFERCHOL/McKay UNVERIFIED.

**Lipid-medicine specialist.** Ref 9 in the manuscript reads “International validation of familial hypercholesterolaemia risk scores…”. Claude says the published title is “European and Canadian derived risk prediction equations…”. I cannot re-resolve DOI 10.1016/j.atherosclerosis.2026.120799 in this session. **If Claude’s PubMed PMID 42229222 is correct, this is a citation-integrity event**, not a typo. Kimi’s “UNVERIFIED C values” and Grok’s “UNVERIFIED — DO NOT CITE Tamehri” then become too conservative on *existence* and correctly cautious on *specific extra numbers* (0.802) that the manuscript does not even quote.

**Editor-in-Chief.** **Resolved on orphans (19/39): all three agree — cite or delete.** **Resolved on ref 10:** manuscript attaches it to “apoB, imaging, polygenic scores, or dozens of variables”; that paper is a Canadian/French score validation. **Mismatch adopted.** **Unresolved:** exact published title of ref 9, and McKay 0.67 / REFERCHOL 0.77–0.78, until a publisher record is opened in *this* runtime. Claude claims those C values 0.767/0.735 match the manuscript; Kimi/Grok did not verify. I will not order deletion of 0.767/0.735 on Kimi’s unverified status, nor will I treat Claude’s title correction as optional. **Conflict class:** citation fidelity / verification-scope.

**Out-of-window:** Tybjærg-Hansen 2005 (ref 15) used as evidence — all three agree, replace with in-window Gratton 2023 or Trinder 2020 (ref 14, currently orphan). Sudlow 2015 / RECORD 2015 as *evidence* out of window; as historical resource/checklist, tolerable. Khera June 2016 and VOYAGER June 2016 sit on the window edge; they are orphans anyway.

---

### Claim K — What the paper *is*. Kimi: common-data head-to-head after frame lock. Grok: comparator-coding audit; equation not supported. Claude’s editor: evaluability failure is the paper; superiority paper is unrecoverable.

**Biostatistician.** I can still see a methods paper: OOF paired bootstrap, Holm, tie rule, complete-input policy, corrections that moved both ways. That paper dies if the title stays FH. It also dies if transport C stays in Key points without intervals.

**Cardiologist.** I still offer **no clinical cardiology journal** until an untouched, variant-confirmed HeFH cohort exists. Evaluability (40/1, 132/6) is useful to lipid clinics and public-health implementers, not to a coronary-care reader deciding on PCSK9.

**Lipid-medicine specialist.** Claude’s editor is closest to the lipid truth: the clean finding is that Lp(a)-dependent specialist scores are often non-computable in a national registry, and that clinic-derived equations degrade in a mild population flag. CALON-C as index model is a supporting character. I dissent from deleting the grey-zone analysis (Kimi/Grok want it out of Key points — agreed — but Claude wants it kept as a *data* diagnostic that Lp(a) is inert here). That null is discordant with Kronenberg 2022 and with both comparators. It is a red flag about the frame, not a licence to skip Lp(a) in care.

**Editor-in-Chief.** **Unresolved on paper identity** — see closing. **Resolved:** grey-zone out of Key points (Kimi/Grok); grey-zone may remain in Results as a data diagnostic (Claude lipid seat). **Resolved:** “candidate first-line ranking layer” (manuscript Discussion) is utility language after DCA withdrawal — Grok was right; delete.

---

## 2. Agreement map (all three models)

These are not in dispute:

1. Governance placeholders (ethics, funding, COI, PPI, code availability) are desk-reject material.
2. Welsh numerical artefacts mix 1,169/102 with 1,159/92.
3. Wales is transport, not independent external validation.
4. FH-Risk-Score full-follow-up result is a TIE; 5-year family is null after Holm.
5. Endpoint is not MACE; that discipline should stay.
6. Nineteen references are never cited.
7. Meta-language (“user-specified”, “reviewer response”, file names as source of truth) must go.
8. No comparative decision-curve / net-benefit evidence; utility claims are unsupported.
9. UK Biobank competing-risk analysis did not run.
10. Not *Circulation* / *EHJ* / *JACC* / *JAMA Cardiology* in present form.

---

## 3. Contradiction ledger

| # | Named conflict | Kimi | Grok R1 | Claude | Class | Round-2 resolution |
|---|---|---|---|---|---|---|
| 1 | Does ACC/AHA 2026 exist / may it be cited? | UNVERIFIED, delete | Verified local extract | DOI resolves; pages not in Crossref | Verification-scope | **Cite as HeFH guidance; do not delete; check pages** |
| 2 | Is 499 UKB in FH-Risk-Score? | Unverified | Verified | Unverified (abstract) | Verification-scope | **Verified in primary Methods** |
| 3 | Is the cohort HeFH? | Honest carrier label; attenuation MAJOR | FATAL mismatch | FATAL (frequency + phenotype) | Population/ascertainment | **FATAL for HeFH claims; salvageable as flag study** |
| 4 | Gratton 1/288 vs 1/142 | Not used | Not used as FATAL arithmetic | FATAL arithmetic | Population (plus mixed denominators) | **Direction adopted; pairing refined** |
| 5 | Tamehri C 0.767/0.735/0.802 | UNVERIFIED | UNVERIFIED | Verified PubMed | Verification-scope | **0.802 not used here; 0.767/0.735 manuscript-quoted, Claude-supported, not re-resolved this runtime** |
| 6 | Ref 9 title | Not flagged | Not flagged | Wrong title | Citation fidelity | **Adopt Claude pending publisher title check** |
| 7 | Transport CIs | MAJOR | MAJOR | MAJOR + code cause | Methodological | **Agreement** |
| 8 | CIF > KM in Table 5 | Missed | Missed | MAJOR, impossible | Implementation | **Adopt Claude; confirmed in manuscript** |
| 9 | Welsh rescue | Limitation | File lock FATAL | Outcome-conditional FATAL | Methodological | **Both: lock files AND stop outcome-conditional inclusion** |
| 10 | Montreal in Holm family | Leave, caveat | Remove | Cross-estimand, do not claim win | Endpoint/estimand | **Cannot claim superiority for Montreal’s original task; family rebuild unresolved** |
| 11 | S0 / absolute risk | MAJOR | FATAL safety | MAJOR, fix code | Calibration + safety | **EIC: FATAL to print deployable equation** |
| 12 | “Cumulative” lipid term | Under-weighted | MAJOR/FATAL naming | Algebra = age + lipid | Substantive naming | **Rename; not cholesterol-years** |
| 13 | Lp(a) ÷2.15 | Sensitivity missing | Mentioned | Kronenberg: invalid; favours CALON-C | Implementation | **Adopt Claude; Kimi’s ‘plausible range’ overruled** |
| 14 | OOF head-to-head | Not seen | Not seen | Strength from code | Implementation | **Adopt conditionally** |
| 15 | Specification-search optimism | Penalty provenance | Nested-CV gap | Unquantified MAJOR | Methodological | **Adopt Claude** |
| 16 | Age HR 1.000–1.046 | Not flagged | Rounds over a TIE (0.99968) | Separate age terms uninterpretable | Reporting | **Adopt Grok rounding; adopt Claude collinearity** |
| 17 | Grey zone in Key points | Delete | Delete | Keep as data diagnostic | Substantive | **Out of Key points; may stay in Results** |
| 18 | Recoverable paper | Head-to-head after lock | Coding-audit methods paper | Evaluability negative paper | Novelty / journal fit | **Unresolved** |
| 19 | Ridge Wald CIs | Not flagged | Mentioned | Invalid under penalty | Methodological | **Unresolved severity; disclose penalty** |
| 20 | Ancestry/kinship/death “unavailable” | Kinship disclosed gap | Kinship anti-conservative CIs | Extraction choices, not data limits (Gratton did ancestry) | Implementation | **Adopt Claude’s wording: not extracted, not absent from UKB** |

No **substantive biological** disagreement with LDL causality is required. All three models agree null lipid terms ≠ LDL retired. The fight is whether that null is interpretable (Kimi: expected within-stratum; Grok: mild phenotype + weak reconstruction; Claude: imputation + conversion + wrong population). That remains a **named dissent**.

---

## 4. Internal-panel debate

**Lipid-medicine specialist.** Kimi’s panel treated +0.2 mmol/L LDL-C excess as a caveat that explains the SAFEHEART headline. That is the wrong order. You do not test SAFEHEART, FH-Risk-Score, and Montreal in a sample that is not FH and then tell lipid clinics the routine panel “recovers similar ordering without Lp(a).” Claude’s editor is right that evaluability is cleaner than ΔC. Grok is right that `log(non-HDL × age)` is not cumulative exposure. I will not sign a title that says familial hypercholesterolaemia.

**Biostatistician.** I grant the population point as a change of estimand. I do not grant that every repair is therefore premature. Claude’s lipid seat said that; I said the opposite in spirit and I still do. If you rebuild to ClinVar P/LP (programme audit: 890 people, sparse events), you will still need intervals on C, a calendar censoring rule, competing-risk CIF, and nested or at least counted specification search. Sequencing is not skipping. Kimi was right that Holm, the tie rule, and complete-input policy are real strengths. Claude was right that the OOF linear predictor is the strength the Methods forgot to claim.

**Cardiologist.** I am not negotiating a methods appendix into *Heart*. My patients with HeFH are not this Table 1. Grok’s safety point on Table 2 is the one I will not trade. Claude’s 6.20% ten-year risk labelled as carrier/FH risk is how people get under-treated. Kimi praised the de-risking sentence and then left the equation in place. That is a contradiction. On Wales I will not pretend last-contact hypertension is a timestamp, but I also will not pretend chronic diabetes appeared after the infarct in most of these patients. The inclusion rule is the part I cannot defend.

**Editor-in-Chief.** You are arguing three different papers. Kimi wants Paper A: lock the Welsh files, verify ref 1, add CIs, submit to *Atherosclerosis*. Grok wants Paper A minus the equation and minus HeFH framing. Claude wants Paper C: specialist scores fail to compute and degrade in population data; CALON-C is demoted. I will not manufacture consensus among those three. I will say this: Paper B — “a new FH risk equation that beats SAFEHEART” — is not recoverable in this frame. Kimi’s optimism that the head-to-head “would survive review today” is the sentence I reject. Honesty of hedging does not rescue a title, an abstract Findings box, and a printed S0.

**Lipid-medicine specialist.** Then we still disagree on grey zone. Delete it from Key points, yes. Delete it from the paper, no. An Lp(a) SMD of 0.054 in an FH-adjacent cohort is diagnostic of the frame.

**Biostatistician.** Keep it only with one base C, per-row n, and the predecessor label. Table 6’s three implied bases (0.5986 / 0.5980 / 0.5984) are a mess. Kimi caught that; Claude caught it; it is not optional.

**Cardiologist.** And take “at least as well as” out of the Question. All three models said it. Non-inferiority without a margin is theatre.

**Editor-in-Chief.** Adjudication for this round: population reframing and Welsh source-lock precede journal choice. Absolute-risk equation out of the main text. Transport out of Key points until intervals exist. Montreal not a confirmatory win. Ref 1 may stay as HeFH guidance. 499 stays, cited to Paquette Methods. Tamehri title check is mandatory. Paper identity remains dissent.

---

## 5. Consensus

1. This is not a submission-ready HeFH risk-equation paper.
2. Desk-reject triggers: placeholders; mixed Welsh frames; pipeline voice.
3. Like-for-like incident result versus FH-Risk-Score is a TIE; 5-year confirmatory family is null after Holm.
4. Transport is not external validation; C=0.725/0.660 cannot be a finding without intervals.
5. “Cumulative untreated-equivalent” is a misnomer; lipid HRs are TIEs; that is not a causal null.
6. De-risking prohibition stays; “candidate first-line ranking layer” goes.
7. Ref 1 exists as a 2026 *Circulation* guideline record and applies to **HeFH**, not to this flag.
8. The 499 UK Biobank figure in FH-Risk-Score is real (primary Methods).
9. Table 5’s CIF>KM juxtaposition is internally impossible as displayed.
10. High-impact clinical cardiology journals are the wrong target.

---

## 6. Unresolved disputes (named dissent)

1. **Paper identity.** Methods/coding-audit paper (Grok biostatistician; Kimi) versus evaluability-failure paper with CALON-C demoted (Claude editor; this lipid seat) versus no clinical journal at all until a third HeFH cohort (this cardiologist).
2. **Whether Montreal belongs in any confirmatory Holm family**, or only as a cross-estimand ranking footnote.
3. **Welsh predictor timing:** usable chronic-disease attestation (cardiologist) versus unusable post-event measurement (biostatistician).
4. **Tamehri 2026 extra numbers** (primary-prevention C=0.802; Combined-FH-Score 0.698) and **ref 9 exact title** — Claude vs unverified Grok/Kimi; not re-resolved here.
5. **McKay 0.67 and REFERCHOL 0.77–0.78** — manuscript quotes; Claude could not verify from abstracts; Kimi/Grok UNVERIFIED.
6. **Whether null lipid terms can be interpreted at all** before multiple imputation and intensity-specific correction (Claude) versus already explained by restricted range and r=0.32 (Kimi/Grok).
7. **Grey-zone retention** beyond Key points (lipid seat / Claude: keep as data diagnostic; others: demote hard).
8. **Ridge Wald intervals** in Table 2: disclose vs suppress.
9. **Hard-coronary sensitivity on 147 unambiguous events** now (Kimi cardiologist) versus underpowered contamination (Kimi/Grok biostatistician).

---

## 7. Required manuscript actions

**Do before any journal is named**

1. Rebuild or relabel the population. Either classify LDLR from sequence/ClinVar and report frequency and LDL-C excess against Gratton/Patel, or retitle as an unvalidated `ldlr_carrier` flag study and remove FH-cohort claims from title, keywords, Key points, and abstract.
2. Regenerate every Welsh table from one risk set; never print 1,159/92 beside 1,169/102; never print CIF and KM from different frames in one row.
3. Redefine Welsh inclusion from baseline information only (no event-conditional rescue), or bound the transport claim as a contaminated stress test.
4. Attach 95% CIs to every C, including transport; if the transport difference includes 0, delete the asymmetry narrative.
5. Remove S0 and worked-example percentages from the main text until UK Biobank competing-risk CIF is actually run.
6. Fill or do not submit: ethics, legal basis, funding, COI, PPI, data controller, code/model availability.

**Do in the same revision**

7. Rewrite the Question without “at least as well as.” Put the FH-Risk-Score TIE and the 5-year Holm-null in the Findings box. Qualify any SAFEHEART ΔC as an incident primary-prevention, prior-ASCVD=0, treatment-suppressed-LDL application.
8. State that head-to-head used out-of-fold CALON-C predictions, and that Welsh comparisons used a 7-term local refit.
9. Rename `cum_nonhdl`; report r=0.32 / MAE 1.20 mmol/L next to the lipid TIEs; stop calling the transform cumulative exposure.
10. Lp(a): sensitivity across a molar-range threshold; stop presenting omission as a validated design virtue; keep COR 1 “measure once” as care, not as a model input requirement for historical scoring.
11. Repair references: correct or verify ref 9 title; reattach ref 10; cite or delete 19 orphans; move Tybjærg-Hansen 2005 to historical context; cite Gratton 2023 and/or Trinder 2020 for the phenotype gradient; cite Paquette Methods for n=499.
12. Purge pipeline voice. Keep one sentence: several specifications were fit on these data, so internal C has unquantified specification-search optimism.
13. Delete “candidate first-line ranking layer,” stealth non-inferiority tally, and “first head-to-head of CALON-C with these instruments.”

---

## 8. Plain-language lesson for Dr Genedy

Three reviewers looked at the same paper and did not disagree that you were honest. They disagreed about **what you were honest *about***.

Kimi saw a careful methods paper with unfinished tables and an unchecked citation. Grok saw a flag cohort wearing HeFH clothes and an equation that looks safer than it is. Claude saw a population that is not FH, a comparator win that may be an artefact of that population, and a buried finding that specialist scores often cannot even be computed in Wales.

The methodological lesson is: **eligibility is part of the estimand.** If the variable that decides who is in the study is not the disease named in the title, every downstream C-statistic is an answer to a different question. No amount of Holm correction, tie rules, or self-disclosure in the limitations list can relabel the sample. Lock one Welsh pipeline, put intervals on every C, and take the deployable equation out until competing death is modelled — but first decide, in the title, whether this is familial hypercholesterolaemia or a population LDLR-flag study. Those are different papers. The three models are still arguing because the manuscript is still trying to be both.

---

## Teaching section (why each major criticism exists)

**1. Population is not a limitation; it is the question.**  
Measurement error in a predictor biases an estimate. Measurement error in *who is eligible* changes the quantity. Your empty `variant_id`, +0.15–0.23 mmol/L excess, and 3,540-flag versus ~890 ClinVar P/LP are diagnostics of eligibility, not footnotes. Kimi graded this MAJOR; that grade is how HeFH papers get written about volunteer flags.

**2. A TIE is not non-inferiority, and a 5-year TIE is not a full-follow-up win.**  
SAFEHEART was built for short-term risk in molecular FH, including prior disease. Holm p=0.0560 at 5 years is a TIE. Headlining full follow-up ΔC=+0.070 is scoring the exam the comparator did not sit. Grok named this; Kimi under-weighted it.

**3. Disclosure does not licence contradiction.**  
Writing “Welsh Table 1 is uncorrected” and then printing Table 3 as 1,159/92 next to a corrected 1,169/102 is two results sections. Claude’s CIF 6.02% versus KM 5.40% is the same sin in one row: competing-risk theory says that cannot happen in one risk set.

**4. Rescuing events because they are events is selection.**  
Keeping people without follow-up only if they already had the outcome raises the event rate by construction. That sits under the transport C you put in the Key points. Good intentions do not define the risk set.

**5. An interval is part of the number.**  
0.725 versus 0.660 with 102 events may be noise. Three Discussion paragraphs explaining “asymmetric transport” are then fiction. TRIPOD+AI is not optional decoration.

**6. Internal calibration plus a printed S0 is a clinical object.**  
Readers will type Table 2 into a spreadsheet. Kaplan–Meier E:O≈1 in the development set does not mean 6.20% is a 10-year HeFH risk. Grok’s safety FATAL is the right category.

**7. Name the algebra, not the biology.**  
`log(non-HDL × age)` = log(non-HDL)+log(age), sitting beside age and an age spline, after dividing treated LDL by 0.70 (r=0.32 with true pre-treatment LDL). That is not cholesterol-years. Null lipid HRs then cannot be sold as a biological finding.

**8. Differential error is how a comparison becomes unfair without anyone cheating.**  
÷2.15 nmol/L to mg/dL is exactly the conversion Kronenberg 2022 says you cannot do with a fixed factor. It noisies only the Lp(a)-using comparators. Faithful coefficient transcription does not cancel that.

**9. Cross-validation does not undo specification search.**  
OOF C is honest about coefficients. It is silent about CALON-N→F→H→H2→11→C. Claude found the OOF head-to-head (a real strength) in the code; the manuscript instead lists “we withdrew DCA” as a strength. That inversion is the reporting lesson.

**10. Citation is a claim.**  
Nineteen uncited references, a possible wrong title on the closest overlapping paper, and HeFH-guideline text applied to a flag are how editors stop reading. Verifying 499 in Paquette’s Methods is the model of what the rest of the list still needs.

**11. When the positive finding is confounded, publish the negative one that is not.**  
“We beat SAFEHEART by 0.07” depends on population and Lp(a) handling. “SAFEHEART was computable for 40 people and 1 event in a national genotype-positive registry” does not. Claude’s editor and this lipid seat think that is the paper. This cardiologist thinks even that belongs in a lipid/implementation journal, not a clinical cardiology one. That dissent is left standing on purpose.
