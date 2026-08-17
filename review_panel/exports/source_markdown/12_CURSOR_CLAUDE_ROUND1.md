I have completed verification. All 39 manuscript DOIs resolve; one reference title does not match its record; 19 of 39 references are never cited in the text; and I checked the analysis code, which corrects one suspicion I had formed. Here is the review.

---

# CALON-C — independent four-seat panel review (blind round 1)

**Reviewed file:** `outputs/manuscript_2026-08-16/CALON_C_MANUSCRIPT_HIGH_CALIBRE.md` (536 lines, read in full)
**Evidence window enforced:** 17 August 2016 – 17 August 2026
**Blinding:** a sibling directory `outputs/manuscript_2026-08-16/multi_agent_review_2026-08-17/` exists and was **not opened**. No other reviewer output was consulted.
**Aggregate artefacts read (permitted):** `CALON_C_CONFLICT_AND_PROVENANCE_LEDGER.md`, `calon_c_corrected_headtohead.csv`, `METHODS_CALON_C.md`, `code/33_CALON_C.py`. No participant-level data were opened.

---

## Rejection-risk summary

**Overall verdict: reject in present form from any high-impact cardiovascular or lipid journal; potentially salvageable as a methods-and-limitations paper in a specialist journal after the population question is resolved.**

The manuscript is unusually honest. Its hedging is, in most places, better calibrated than the analysis it describes, and the correction log is genuinely creditable. That honesty is also what makes the central problem visible.

**The single fatal issue is population validity.** The cohort is 3,540 `ldlr_carrier` participants drawn from 501,936 rows, a carrier frequency of about 1 in 142 (0.71%). Gratton, Humphries and Futema (*Arterioscler Thromb Vasc Biol* 2023;43:1737–1742, [10.1161/ATVBAHA.123.319438](https://doi.org/10.1161/ATVBAHA.123.319438)) estimated the prevalence of a likely-pathogenic or pathogenic FH-causing variant in UK Biobank European-ancestry participants at 1 in 288 (95% CI 1/316 to 1/264) using whole-exome sequencing across *all three* FH genes. The manuscript's LDLR-only flag is therefore roughly twice as frequent as all-gene pathogenic FH, and about 2.5 times as frequent as LDLR-only pathogenic FH would be. The manuscript's own reported phenotype corroborates this: untreated LDL-C excess over non-carriers of only +0.15 to +0.23 mmol/L, against a "significantly higher" and clinically substantial excess in every ancestry group in Gratton et al. A 10-year observed event risk of 6.15% at median age 57 is likewise not an FH-cohort risk. The most probable explanation is that the flag captures variants of uncertain or benign significance, or derives from array-based calls rather than sequence data. Until this is resolved, every comparator claim, the guideline framing, the title, and the abstract describe a population that the data do not support.

**This directly explains the headline result.** SAFEHEART-RE returns C = 0.6308 here — the lowest value reported anywhere. In genotype-confirmed heterozygous FH, Tamehri Zadeh et al. (*Atherosclerosis* 2026;418:120799, [10.1016/j.atherosclerosis.2026.120799](https://doi.org/10.1016/j.atherosclerosis.2026.120799)) obtained C = 0.767 (95% CI 0.706 to 0.827) overall and 0.802 (0.711 to 0.888) in primary prevention. A 0.14–0.17 discrimination deficit relative to a contemporaneous genotype-confirmed cohort is a signal about the data, not about SAFEHEART-RE. Reinforcing this, Lp(a) is essentially unassociated with events in this cohort (standardised mean difference 0.054; grey-zone hazard ratio 1.033, 95% CI 0.923 to 1.157 per SD — a TIE). Two of the three comparators depend on Lp(a). A model that omits Lp(a) will beat models that use it whenever Lp(a) is non-informative, and that is an artefact of the frame rather than evidence of better modelling.

**Second-order rejection triggers.**

1. **No confidence interval is reported for any C-statistic.** Not the six internal values in Table 3, not the comparator or index values in Table 4, not the two transport estimates. The transport asymmetry (0.7252 versus 0.6600) is the paper's structural claim and I confirmed from `code/33_CALON_C.py` that the transport routine computes a point estimate only. With 102 Welsh events the two directions may not be distinguishable.
2. **Specification-search optimism is unquantified.** The Methods disclose that CALON-C supersedes CALON-N, CALON-F, CALON-H, CALON-H2 and CALON-11 on the same data. Cross-validation is nested over coefficient estimation only, not over specification selection, so the out-of-fold C carries residual optimism of unknown size.
3. **Outcome-conditional cohort construction in Wales.** Participants lacking operational follow-up were excluded unless they had a dated event, "rescuing 10 events". Inclusion conditioned on the outcome is a selection mechanism of exactly the kind described by Munafò et al. (*Int J Epidemiol* 2018;47:226–235, [10.1093/ije/dyx206](https://doi.org/10.1093/ije/dyx206)). This is not a conservative choice; it is a bias of unknown direction in the target cohort of the transport claim.
4. **Selective horizon reporting.** The confirmatory family excludes the 10-year horizon — the native horizon of FH-Risk-Score and the standard clinical horizon — without justification, and no 10-year comparator delta appears anywhere. In fairness, I checked `calon_c_corrected_headtohead.csv`: the omitted 10-year cells do *not* reverse any conclusion. The omission is a reporting failure, not concealment.
5. **The document is not yet a manuscript.** Sixteen bracketed placeholders including ethics approval; internal audit vocabulary throughout ("The corrected source of truth was `RESULTS_FINAL_CORRECTED.md`"; "the reviewer response explicitly withdrew"); source files cited in table footnotes; and an instruction addressed to the authors inside the Discussion ("This priority claim should be rechecked immediately before submission"). Any editor will desk-reject on sight.
6. **Citation fidelity.** Nineteen of 39 references (49%) are never cited in the text. Reference 9's title is not the published title. Reference 10 is cited for a claim it does not make.

**One correction to an expectation I formed while reading.** The manuscript never states whether the head-to-head CALON-C C-statistic is in-sample. I therefore inspected `code/33_CALON_C.py`: the linear predictor passed to the paired bootstrap is the out-of-fold predictor from repeated cross-validation, so the comparisons are *not* index-model-in-sample against comparator-out-of-sample. This is the correct design and it materially strengthens the paper. That it must be recovered from source code rather than read in the Methods is itself a reporting defect.

**Estimated outcome by venue.** *Circulation* / *European Heart Journal* / *JAMA Cardiology*: desk reject. *Atherosclerosis* / *Journal of Clinical Lipidology* / *European Journal of Preventive Cardiology*: reject with invitation to resubmit if the carrier definition is rebuilt from sequence data and reframed. *Diagnostic and Prognostic Research* or a methods journal, reframed as a study of comparator transportability failure in a population-ascertained frame: plausible major revision.

---

## Paragraph-by-paragraph review

Seats: **BS** Biostatistician · **CA** Cardiologist · **LM** Lipid-medicine specialist · **ED** Senior Editor-in-Chief (adjudicates last).

### Key points

**Key points ¶1 (Question)**

1. *Current claim.* A parsimonious routine-data model can rank first atherosclerotic events among LDLR-variant carriers at least as well as established FH risk instruments.
2. *Weakness.* "At least as well" is a non-inferiority framing, but the Methods specify no non-inferiority margin, and the Results explicitly disclaim one. The question as posed cannot be answered by the design used.
3. *Evidence check.* Non-inferiority requires a pre-specified margin; Riley et al. (*BMJ* 2024;384:e074820, [10.1136/bmj-2023-074820](https://doi.org/10.1136/bmj-2023-074820)) set out the design requirements for comparative model evaluation, none of which include an unmargined superiority tally.
4. *Required improvement.* Restate as a descriptive comparative-discrimination question.
5. *Suggested wording.* "How does a model restricted to routine clinical variables and a standard lipid panel compare, on common evaluable subsets, with three published familial-hypercholesterolaemia risk instruments for ranking first incident atherosclerotic events among UK Biobank participants carrying an LDLR-variant flag?"
6. **Severity: MODERATE.**

- **BS:** the framing implies an equivalence claim the analysis cannot support; delete "at least as well".
- **CA:** "rank events" is not a clinical question. Clinicians ask whether the ranking changes management. No objection to the wording as science, but it has no clinical yield as stated.
- **LM:** "established familial-hypercholesterolaemia risk instruments" presupposes the cohort is an FH cohort. It is the presupposition, not the comparison, that fails.
- **ED:** LM's objection is the governing one and recurs in nearly every paragraph. Adopted.

**Key points ¶2 (Findings)**

1. *Current claim.* In 3,209 participants with an LDLR-carrier flag, discrimination was higher than SAFEHEART-RE and Montreal-FH-SCORE after Holm correction, did not differ from FH-Risk-Score, and frozen transport gave C = 0.725 versus 0.660 in reverse.
2. *Weakness.* Four defects. C values carry no intervals. The Montreal comparison is against a cross-sectional prevalent-disease instrument, so "higher discrimination" compares different estimands. The transport asymmetry is asserted without uncertainty. And the SAFEHEART-RE value is a far outlier against contemporaneous evidence.
3. *Evidence check.* Montreal-FH-SCORE was derived in an explicitly "cross-sectional cohort study" of 670 LDLR-mutation carriers (638 analysed) with AUC 0.840 (0.808 to 0.872) for *prevalent* CVD (Paquette, Dufour, Baass, *J Clin Lipidol* 2017;11:80–86, [10.1016/j.jacl.2016.10.004](https://doi.org/10.1016/j.jacl.2016.10.004), verified via PubMed PMID 28391914). SAFEHEART-RE achieved C = 0.85 in derivation and 0.81 in participants without established ASCVD, with bootstrap optimism 0.003 (Pérez de Isla et al., *Circulation* 2017;135:2133–2144, [10.1161/CIRCULATIONAHA.116.024541](https://doi.org/10.1161/CIRCULATIONAHA.116.024541)), and C = 0.767 (0.706 to 0.827) in genotype-confirmed Australian HeFH (Tamehri Zadeh et al. 2026, above).
4. *Required improvement.* Attach 95% confidence intervals to every C. Label the Montreal comparison as cross-estimand. State the SAFEHEART-RE outlier explicitly here, not only in the Discussion.
5. *Suggested wording.* "…discrimination was higher than that of SAFEHEART-RE (ΔC +0.070, 95% CI 0.036 to 0.104) and of the Montreal-FH-SCORE, which was developed for prevalent disease and is used here only as a ranking instrument; discrimination did not differ from FH-Risk-Score (TIE). SAFEHEART-RE discriminated substantially less well here than in any previously published cohort, which we interpret as a property of this frame rather than of the instrument."
6. **Severity: MAJOR.**

- **BS:** intervals or nothing. A key-points panel quoting three C values without a single interval breaches the journal's own reporting norms and TRIPOD+AI.
- **CA:** ranking a prevalent-disease score against incident events and calling the result "higher discrimination" is a category error that will read to a clinical readership as a like-for-like defeat of Montreal.
- **LM:** the SAFEHEART-RE figure is the tell. Two of three comparators are Lp(a)-dependent and Lp(a) is inert in this dataset. That is a lipid-measurement finding masquerading as a modelling result.
- **ED:** all three objections are sustained and they compound. This paragraph, as written, is the sentence a press office would quote, and it would be wrong.

**Key points ¶3 (Meaning)**

1. *Current claim.* CALON-C supports feasibility but does not establish external validation, clinical utility, or superiority to every instrument; further work is required.
2. *Weakness.* Well calibrated to the evidence, and the strongest paragraph in the manuscript. It nonetheless omits the population caveat, which is the binding limitation.
3. *Evidence check.* No challenging literature required.
4. *Required improvement.* Add one clause on carrier-definition uncertainty.
5. *Suggested wording.* Append: "Because carrier status could not be confirmed at variant level, these findings may not transfer to clinically ascertained familial hypercholesterolaemia."
6. **Severity: MINOR.**

- **BS, CA, LM:** no independent objection beyond the addition.
- **ED:** the honesty here is real and should be preserved verbatim in revision.

### Abstract

**Abstract ¶1 (Background)**

1. *Current claim.* Guidance recognises FH-specific scores for short-term risk while general-population equations should not be used for 10- or 30-year risk in heterozygous FH; existing instruments differ and their performance in population-ascertained carriers is incompletely characterised.
2. *Weakness.* Accurate, but "population-ascertained LDLR-variant carriers" is doing quiet work: it is offered as a *gap* when it is in fact the study's principal *vulnerability*.
3. *Evidence check.* The 2026 ACC/AHA dyslipidaemia guideline (*Circulation* 2026;153, issue 17, [10.1161/CIR.0000000000001423](https://doi.org/10.1161/CIR.0000000000001423)) is verified as a real record with the stated first authors; the printed page range e1154–e1276 is not present in the Crossref record and should be checked against the issue. The 2025 ESC/EAS focused update (*Eur Heart J* 2025;46:4359–4378, [10.1093/eurheartj/ehaf190](https://doi.org/10.1093/eurheartj/ehaf190)) verifies exactly as cited.
4. *Required improvement.* Convert the gap statement into a bounded statement of what a population-ascertained frame can and cannot test.
5. *Suggested wording.* "…their performance within population-ascertained carriers is incompletely characterised, and such carriers differ systematically from clinic-ascertained patients in lipid phenotype and event rate."
6. **Severity: MINOR.**

- **BS:** no objection. **CA:** no objection. **LM:** the phenotype gradient between clinic and population ascertainment is the paper's real subject and should be named in the first two sentences.
- **ED:** LM's reframing would improve the paper's honesty and its novelty simultaneously. Adopt.

**Abstract ¶2 (Methods)**

1. *Current claim.* Development, internal performance, comparator implementation, reciprocal transport; "Decision-curve claims were withdrawn."
2. *Weakness.* The final sentence is provenance bookkeeping, not method. Two substantive omissions matter more: the abstract does not state that head-to-head comparisons used out-of-fold predictions (they did — verified in source), and it does not state that the Welsh head-to-head used a Wales-refitted seven-term model rather than the frozen equation (it did — verified in source and implied by Welsh CALON-C C values of 0.75–0.79 against a transport C of 0.7252).
3. *Evidence check.* Blanche, Kattan and Gerds (*Biostatistics* 2019;20:347–357, [10.1093/biostatistics/kxy006](https://doi.org/10.1093/biostatistics/kxy006)) show Harrell's C is not a proper measure for *t*-year predicted risk, which bears on "over full follow-up" as the primary horizon.
4. *Required improvement.* Delete the withdrawal sentence. State the out-of-fold basis of the comparisons and the identity of the model used in each Welsh comparison.
5. *Suggested wording.* "Comparator differences were estimated against out-of-fold CALON-C predictions on each instrument's complete-input subset by paired bootstrap (B = 2,000), with Holm correction across six confirmatory comparisons."
6. **Severity: MAJOR** (for the omissions, not the withdrawal sentence).

- **BS:** the out-of-fold basis is the most defensible feature of the analysis and it is invisible. Stating it converts a suspicion of circularity into a strength.
- **CA:** no clinical objection.
- **LM:** the treatment-correction divisors belong in the abstract; a reader cannot judge a lipid model without knowing that treated values were divided by a fixed 0.70.
- **ED:** all adopted. The withdrawal sentence is deleted; provenance belongs in a data-availability statement.

**Abstract ¶3 (Results)**

1. *Current claim.* 3,209 participants, 289 events, optimism-corrected C 0.7095; three comparator deltas; Welsh 1,169/102; transport 0.725/0.660; 0/16 PH violations; Welsh cumulative incidence 6.02% and 11.97%; the UK Biobank competing-risk analysis "did not execute"; internal 10-year slope 1.101 and expected:observed 1.008.
2. *Weakness.* Reporting that a planned analysis "did not execute" is not a result. The cause given in the Methods is a guard on a `death` column absent from the processed frame — a fixable software defect, not a data limitation. Separately, the Welsh Aalen–Johansen cumulative incidence (6.02% at 5 years) *exceeds* the Kaplan–Meier observed risk in Table 5 (5.40%), which is impossible within one risk set; the table note reveals the two derive from different frames.
3. *Evidence check.* Austin and Fine (*Stat Med* 2017;36:4391–4400, [10.1002/sim.7501](https://doi.org/10.1002/sim.7501)) set the reporting standard for competing-risk analyses. Van Calster et al. (*BMC Med* 2019;17:230, [10.1186/s12916-019-1466-7](https://doi.org/10.1186/s12916-019-1466-7)) establish why an internally estimated calibration slope near unity carries little information.
4. *Required improvement.* Run the UK Biobank competing-risk analysis and report it, or remove the sentence. Never juxtapose estimates from two risk sets in one row.
5. *Suggested wording.* Delete "the UK Biobank competing-risk analysis did not execute" and report the estimate.
6. **Severity: MAJOR.**

- **BS:** a slope of 1.101 estimated with an internally derived baseline is close to uninformative, and its interval (0.884 to 1.318) admits meaningful miscalibration in both directions. It should not appear in an abstract.
- **CA:** competing mortality is not optional in a cohort with median age 57 followed nearly 14 years. Thirty-five competing deaths against 102 events in Wales makes the point; the UK Biobank gap blocks any absolute-risk reading.
- **LM:** no independent objection.
- **ED:** an abstract that reports its own failed analysis will not survive an editor's first pass. Fix the code.

**Abstract ¶4 (Conclusions)**

1. *Current claim.* Moderate ranking from routine measurements, favourable comparisons with two instruments, tying the third; evidence of development and transport, not external validation or utility.
2. *Weakness.* "Showed favourable full-follow-up comparisons" survives only if the population is what the title says. It is not established that it is.
3. *Evidence check.* As for Key points ¶2.
4. *Required improvement.* Make the conclusion conditional on the carrier definition.
5. *Suggested wording.* "Within a UK Biobank frame defined by an unvalidated LDLR-carrier flag, CALON-C ranked first incident atherosclerotic events with moderate discrimination. Whether these comparisons transfer to variant-confirmed familial hypercholesterolaemia is untested."
6. **Severity: MAJOR.**

- **BS, CA, LM:** concur.
- **ED:** adopted without dissent.

### Introduction

**Introduction ¶1** — FH as a lifelong exposure disorder; heterogeneity; guideline positions.
Accurate, well written, and correctly cited to the two verified guidelines. The one substantive gap is that the paragraph asserts clinical consequences of heterogeneity ("urgency of treatment intensification, frequency of specialist review") without citation, and no evidence within the window demonstrates that FH risk scores change these decisions. **Severity: MINOR.**
**BS:** no objection. **CA:** the three named consequences are plausible but unevidenced; label them as rationale, not established practice. **LM:** "Pathogenic variants affecting LDL-receptor biology" is precisely the claim the cohort cannot support — the tension between this sentence and the Methods is unresolved from the first page. **ED:** CA and LM both sustained; LM's is the deeper one.

**Introduction ¶2** — the three comparators and their prior external evaluations.
Descriptions are faithful. I verified each: SAFEHEART-RE's 2,404 molecularly defined patients with primary and secondary prevention and the stated predictor list; FH-Risk-Score's 3,881 adults with heterozygous FH and no prior ASCVD across five registries in Europe and North America, 32,361 person-years, C = 0.75 against SAFEHEART-RE 0.69; Montreal's cross-sectional derivation. The Australian figures (0.767 and 0.735) are correct.
Two defects. First, **reference 9's title is wrong.** The manuscript gives "International validation of familial hypercholesterolaemia risk scores in Australian patients with genetically confirmed heterozygous familial hypercholesterolaemia". The published title is "European and Canadian derived risk prediction equations for atherosclerotic cardiovascular disease are valid in Australian patients with genetically confirmed familial hypercholesterolaemia" (verified, PMID 42229222). Second, the manuscript's specific external C values for REFERCHOL (0.77–0.78) and English routine care (0.67) were **not verifiable from the abstracts I retrieved** and must be checked against the full texts before resubmission. **Severity: MAJOR** (citation fidelity).
**BS:** the Australian paper also evaluated a fourth instrument, the Combined-FH-Score (C = 0.698, 95% CI 0.627 to 0.766), which this manuscript neither evaluates nor mentions. **CA:** the omission matters because the Australian primary-prevention estimate (SAFEHEART-RE 0.802) is the closest published analogue to this study's design and is the number a reviewer will hold against it. **LM:** all three comparators were built in treated clinic populations with off-treatment or imputed lipids; FH-Risk-Score used LDL-C "untreated (57%) or imputed (43%)". That is a different lipid construct from a fixed ÷0.70 correction. **ED:** the fabricated title is the most serious individual finding in this paragraph and, in a journal with integrity screening, is the kind of error that triggers a fuller citation audit.

**Introduction ¶3** — three unresolved issues: cross-cohort comparison, specialised measurements, clinic versus population ascertainment.
This is the strongest paragraph in the manuscript and states the population problem correctly, citing Tybjærg-Hansen for the phenotype gradient and Fry and the reweighting literature for volunteer selection. **But reference 10 is miscited**: it is attached to "other contemporary approaches use apoB, imaging, polygenic scores, or dozens of variables", whereas reference 10 is "Canadian and French Risk Scores Are Valid in Identifying Cardiovascular Disease in Australian Patients With Familial Hypercholesterolemia" (*Can J Cardiol* 2025;41:2244–2251, verified) — a comparator-validation study, not a multi-biomarker approach. Reference 11 (Zamora et al., AI algorithms) does support the claim. **Severity: MODERATE.**
**BS:** the paragraph identifies the correct methodological gap and the study then partly fails to fill it, because "full follow-up" is not a clinically interpretable horizon. **CA:** the argument that a routine-data model has value even at equal discrimination is sound and is the paper's best clinical idea. **LM:** the Tybjærg-Hansen citation is pre-window for my purposes and is flagged in the excluded-context note; the same point can be made within the window from Gratton et al. 2023 and from the EAS FH Studies Collaboration (*Atherosclerosis* 2018;277:234–255, verified, currently uncited in the text). **ED:** LM's substitution should be made; it converts a 2005 anchor into a 2023 UK Biobank anchor that is directly on point for this cohort.

**Introduction ¶4** — design rationale: parsimony, ordinary lipid panel, treatment via fixed transformations, deliberate exclusion of Lp(a) and apoB.
1. *Current claim.* CALON-C tests whether routine information recovers useful ordering without advanced assays.
2. *Weakness.* Deliberate exclusion of Lp(a) is presented as a design virtue. In this dataset Lp(a) is uninformative, so the exclusion costs nothing here and cannot be shown to be virtuous. The claim and the evidence are confounded.
3. *Evidence check.* Kronenberg et al. (*Eur Heart J* 2022;43:3925–3946, [10.1093/eurheartj/ehac361](https://doi.org/10.1093/eurheartj/ehac361)) establish Lp(a) as a causal, independently predictive risk factor and — directly relevant to the Methods — that mass and molar units are not interconvertible by a fixed factor.
4. *Required improvement.* Separate the design rationale (scalability) from the empirical finding (Lp(a) added nothing *in this frame*), and state that the latter is discordant with the FH literature.
5. *Suggested wording.* "Lp(a) and apoB were excluded from the core equation for scalability. We note that Lp(a) was only weakly associated with events in this cohort, which is discordant with established FH evidence and may reflect the carrier definition or the unit conversion applied."
6. **Severity: MAJOR.**

- **BS:** an exclusion cannot be validated by a dataset in which the excluded variable is inert.
- **CA:** clinically the reverse is true — Lp(a) should be measured once in every carrier, and a paper that appears to license omitting it is a patient-safety concern.
- **LM:** this is my strongest objection in the manuscript and I dissent from any framing that presents Lp(a) omission as a feature. In FH, Lp(a) is among the most important modifiers of risk. A null Lp(a) signal is a red flag to be investigated, not a design licence.
- **ED:** LM and CA prevail. The paper may argue scalability; it may not argue that Lp(a) is dispensable.

**Introduction ¶5** — aims, and the refusal to frame FH-Risk-Score application as independent external validation because its derivation included 499 UK Biobank participants.
1. *Current claim.* Aims are stated; the FH-Risk-Score comparison is not an independent external validation because of participant overlap.
2. *Weakness.* The 499-participant claim is load-bearing, is repeated three times, and is attributed to reference 6. **I could not verify it.** The published abstract describes "5 registries in Europe and North America" and does not mention UK Biobank. The claim is plausible — Trinder and Brunham are co-authors and have published UK Biobank FH work — but it is currently unverifiable from the bibliographic record.
3. *Evidence check.* FH-Risk-Score derivation as published: 3,881 patients, five registries, 32,361 person-years ([10.1161/ATVBAHA.121.316106](https://doi.org/10.1161/ATVBAHA.121.316106), PMID 34433300). **UNVERIFIED — the specific figure of 499 UK Biobank participants must be cited to a page, table or supplement.**
4. *Required improvement.* Cite the exact location in the primary paper, or delete the number and retain the generic overlap caveat.
5. *Suggested wording.* "Because the FH-Risk-Score derivation drew on multiple registries and participant-level overlap with the present cohort cannot be excluded, we do not frame its application here as independent external validation."
6. **Severity: MAJOR.**

- **BS:** an unverifiable number used to constrain the paper's own claims is still an unverifiable number.
- **CA:** no objection.
- **LM:** no objection.
- **ED:** note the asymmetry — the manuscript uses this figure to be *more* modest. That is admirable but does not exempt it from verification. If the figure is wrong, the paper has understated its own novelty on a false premise.

### Methods

**Methods — Study design and reporting framework**
Estimand is clearly stated and correctly framed as association of a baseline linear predictor with time to first event. **But the second paragraph is not publishable prose:** "The corrected source of truth was `RESULTS_FINAL_CORRECTED.md`, generated from `code/38_CALON_C_CORRECTED.py`. This superseded earlier CALON-N, CALON-F, CALON-H, CALON-H2, CALON-11, and June 2026 manuscript outputs." **Severity: MAJOR.**
**BS:** this sentence is the most statistically consequential in the Methods, because it discloses at least six prior model generations developed on the same data. Repeated cross-validation corrects coefficient optimism, not specification-search optimism. The disclosure is welcome; the quantification is absent and probably unobtainable.
**CA:** no clinical objection.
**LM:** no objection.
**ED:** I disagree with any instinct to simply delete this paragraph. The *fact* must survive; the *file names* must not. Replace with: "The model specification reported here is the final member of a series developed iteratively within the same programme using these data. Estimates of internal performance should be read as optimistic to an unquantified degree."

**Methods — Data sources and governance**
Governance is properly handled and no identifiers appear anywhere in the manuscript. The paragraph correctly records that `variant_id` was empty in all 501,936 rows. **Severity: MINOR** as prose; the underlying issue is escalated at "UK Biobank cohort" below.
**BS:** no objection. **CA:** no objection. **LM:** stating that pathogenicity could not be confirmed is necessary but not sufficient — the observed phenotype should be reported here as positive evidence *against* uniform pathogenicity. **ED:** LM sustained.

**Methods — UK Biobank cohort** *(the pivotal paragraph)*
1. *Current claim.* Participants with `ldlr_carrier==1` were eligible; ASCVD was the union of I21, I25, I63, I70, I73 and G45, excluding I50; 3,540 carriers yielded 3,209 after exclusions and 289 events; component-date attribution was unambiguous for 147 of 289.
2. *Weakness.* Three separate problems. (a) The carrier definition is quantitatively inconsistent with published pathogenic-variant prevalence (see Rejection-risk summary). (b) The endpoint mixes hard events (I21) with I25 chronic ischaemic heart disease, I70 atherosclerosis, I73 peripheral vascular disease and G45 transient ischaemic attack; I25 and I70 dates reflect first coded contact rather than incident event onset, and the manuscript concedes coronary weighting. (c) Only 51% of events have unambiguous component dates, in a design whose entire inferential machinery is event timing.
3. *Evidence check.* Gratton, Humphries and Futema 2023 ([10.1161/ATVBAHA.123.319438](https://doi.org/10.1161/ATVBAHA.123.319438)): 488 European P/LP carriers among 140,439 sequenced, prevalence 1 in 288, with significantly higher LDL-C in carriers in every ancestry group. Hu et al. (*Circulation* 2020;141:1742–1759, [10.1161/CIRCULATIONAHA.119.044795](https://doi.org/10.1161/CIRCULATIONAHA.119.044795)) place general-population FH prevalence near 1 in 311. The manuscript's 1 in 142 is incompatible with both.
4. *Required improvement.* Rebuild the cohort from whole-exome sequence data with an explicit ClinVar or ACMG classification step and report the resulting LDL-C distribution against non-carriers. Report the endpoint by component with counts, and pre-specify a hard-coronary sensitivity analysis (I21 plus I25 with procedure confirmation only).
5. *Suggested wording.* If the flag cannot be rebuilt: "Participants were identified by an `ldlr_carrier` flag of unverified provenance whose frequency (1 in 142) substantially exceeds published estimates of pathogenic FH-variant prevalence in UK Biobank (1 in 288), and whose associated untreated LDL-C excess (+0.15 to +0.23 mmol/L) is far smaller than expected for monogenic FH. This cohort should therefore be regarded as an LDLR-variant-enriched population sample rather than a familial-hypercholesterolaemia cohort."
6. **Severity: FATAL.**

- **BS:** measurement error in the exposure defining eligibility is not a limitation to be disclosed; it changes the target population and therefore the estimand. Every downstream comparison inherits it.
- **CA:** as a clinician I would not accept I70 or G45 as adjudicated first atherosclerotic events, and I25 as an *incident* event is unreliable. The event count of 289 is not 289 hard events.
- **LM:** the phenotype is decisive and independent of the genetics. A +0.15 to +0.23 mmol/L untreated LDL-C excess is roughly a tenth of what heterozygous LDLR carriage produces. Either the flag is not pathogenicity-restricted, or the untreated-equivalent reconstruction has destroyed the signal. Both possibilities are fatal to the FH framing, and they are distinguishable with the data described.
- **ED:** unanimous, from three independent directions, on the paper's foundation. This is the finding on which the review turns.

**Methods — All-Wales cohort**
1. *Current claim.* 2,405 genotype-positive participants reduced to 1,169 with 102 events; 649 excluded for lacking positive operational follow-up *or* a qualifying dated event; 10 events reinstated; family number as clustering unit; no administrative ascertainment end date; hypertension, diabetes and smoking incompletely dated.
2. *Weakness.* Inclusion is conditioned on the outcome. A participant with no operational follow-up is retained if and only if they had a dated event. The event rate is thereby inflated by construction (92/1,159 = 7.9% before, 102/1,169 = 8.7% after), and the non-case denominator is ascertained by a different rule from the case numerator. The absence of an administrative end date compounds this: censoring times are not defined by a common calendar rule.
3. *Evidence check.* Munafò et al. ([10.1093/ije/dyx206](https://doi.org/10.1093/ije/dyx206)) on selection conditioned on outcome-related variables. The RECORD statement (*PLoS Med* 2015;12:e1001885, verified; pre-window and therefore used only as a reporting instrument, not as evidence) requires an explicit end-of-recording date.
4. *Required improvement.* Define one calendar censoring rule applied identically to cases and non-cases, obtain an administrative end date, and re-derive the risk set without outcome-conditional rescue. Report the transport estimate under both rules.
5. *Suggested wording.* "Participants lacking documented follow-up were retained only where a dated post-baseline event was recorded. Because this rule conditions inclusion on the outcome, the Welsh event rate and the transport estimate derived from it are biased by an unknown amount and direction."
6. **Severity: FATAL for the transport claim** (MAJOR for the manuscript overall).

- **BS:** this is the second fatal finding and it is independent of the first. The rescue of 10 events is described in the manuscript as a *correction*. It is the introduction of a bias, and the direction cannot be signed without the excluded records.
- **CA:** clinically I understand the impulse — a documented event is real information and discarding it feels wasteful. But the fix is symmetric ascertainment, not asymmetric retention.
- **LM:** the Welsh Lp(a) field was unusable owing to mixed units and BMI was missing in 54.5%, so the registry could not score two of three comparators. That is the honest headline of the Welsh work.
- **ED:** I record a genuine disagreement between BS and CA on tone but not on substance. BS's framing governs: the rescue must be undone or shown to be inconsequential.

**Methods — Outcome terminology**
Correctly refuses the MACE label and states cohort heterogeneity. Exemplary. **Severity: MINOR.**
**CA:** the Welsh endpoint includes angina and coronary revascularisation while UK Biobank has no procedure data. Revascularisation is indication-dependent: patients under specialist FH care are investigated more, so the Welsh endpoint is partly a healthcare-utilisation endpoint. Transporting a coronary-weighted UK Biobank predictor into it is not a transport of the same estimand. **BS:** agreed — this should appear in the transport section, not only here. **LM:** agreed. **ED:** CA's point is currently absent from the manuscript and is one of the more important missing limitations.

**Methods — Predictors and treatment correction**
1. *Current claim.* Nine routine terms; treated non-HDL-C and LDL-C divided by 0.70 and triglycerides by 0.80; non-HDL-C clipped to 0.3–20 mmol/L and remnant cholesterol to −1–6 mmol/L; audit mean absolute error 1.20 mmol/L (95% CI 1.13 to 1.28) with correlation 0.32 against observed pre-treatment LDL-C in 649 Welsh patients; varying the divisor 0.65–0.75 changed C by 0.0022.
2. *Weakness.* Four defects, the first two serious. (a) `cum_nonhdl = log(non-HDL-C_untreated × age)` is algebraically log(non-HDL-C) + log(age); it is a function of age, entered alongside age and an age-above-50 spline. The collinearity guard triggers only at |r| ≥ 0.999 and cannot detect this. The construct is presented as cumulative exposure but is an age term with a lipid offset, and it multiplies the *current* corrected concentration by *total* age, ignoring years on treatment. (b) A correlation of 0.32 between reconstructed and observed pre-treatment LDL-C means the untreated-equivalent scale carries little information about untreated concentration; the sensitivity analysis varies the divisor but never the *structure*, although statin-intensity information exists in the programme's data holdings. (c) Permitting remnant cholesterol down to −1 mmol/L carries a non-physiological derivation error into a predictor. (d) `tg_filter` is a log ratio, not a filter, and its hazard ratio is 0.996 per SD (95% CI 0.884 to 1.122) — no information.
3. *Evidence check.* Karlson et al. (*Eur J Prev Cardiol* 2016;23:744–747, verified) provide intensity-specific LDL-C and non-HDL-C reductions and are **listed as reference 31 but never cited in the text** — the very evidence that would justify an intensity-specific correction is present in the bibliography and unused. (Note: this paper's May 2016 print date places it outside my eligible window, so I raise it as an internal citation-fidelity observation rather than as evidence.) For remnant biology within the window, Ginsberg et al. (*Eur Heart J* 2021;42:4791–4806, [10.1093/eurheartj/ehab551](https://doi.org/10.1093/eurheartj/ehab551)).
4. *Required improvement.* Rename or remove `cum_nonhdl`; report its correlation with age; refit without it and report the change in C. Replace the fixed divisor with an intensity-specific correction, or report a sensitivity analysis over *structures*. Floor remnant cholesterol at 0. Delete `tg_filter`.
5. *Suggested wording.* "`cum_nonhdl` is defined as log(non-HDL-C × age) and is therefore a monotone function of age as well as of lipid concentration; it should not be interpreted as a measure of lifetime cumulative exposure."
6. **Severity: MAJOR.**

- **BS:** entering three age-containing terms and then reporting individual hazard ratios for each (age 1.022, 95% CI 1.000 to 1.046; age-above-50 1.021, 0.994 to 1.049) yields coefficients that are not separately interpretable. Table 2 invites exactly the misreading it should prevent.
- **CA:** a clinician reading Table 2 will conclude that age barely matters in FH carriers, which is false and would be harmful.
- **LM:** the cumulative-exposure construct is the paper's principal biological claim and it does not survive inspection. True cumulative LDL exposure requires serial measurements and treatment duration; multiplying one treated-then-inflated value by chronological age is not that quantity. I would delete the cumulative framing entirely rather than defend it.
- **ED:** LM's deletion is the correct editorial call, and it is consistent with the manuscript's own Discussion, which already concedes that the lipid apparatus contributes about +0.008 of +0.041. The paper should follow its own evidence.

**Methods — Model specification and estimation**
1. *Current claim.* Ridge-penalised Cox (penalty 0.02); the specification "was fixed before the CALON-C fit, although the repository did not contain a verifiable pre-result specification file and the authors therefore withdrew a formal pre-specification claim"; fold-wise median imputation; collinearity guard; a rule retaining binary terms only when both levels carry ≥10 events, which removed diabetes and smoking in Wales; 10×10 repeated cross-validation with family clustering "where available"; 100-resample Harrell optimism; UK Biobank used participant-level resampling because no kinship field was available.
2. *Weakness.* (a) The pre-specification sentence asserts and retracts the same claim in one breath; it must be one or the other. (b) Table 2 reports 95% confidence intervals from a *penalised* model without acknowledging that penalisation invalidates nominal coverage. (c) Fold-wise **single median imputation** for 12.4% missing lipid values attenuates precisely the lipid associations the Discussion then interprets substantively; the null lipid finding is partly an artefact of the imputation method. (d) The ≥10-event retention rule is data-driven variable selection entangled with 41.6% missing diabetes in Wales — the Welsh model dropped diabetes for a reason that is as much missingness as event count. (e) "No kinship field was available" is not the same as unavailable: kinship is a standard UK Biobank resource, and a carrier cohort is enriched for relatives by construction, so ignoring relatedness understates both optimism and interval width. (f) Averaging out-of-fold linear predictors across 10 repeats (confirmed at `code/33_CALON_C.py`) behaves partly like an ensemble and is not the out-of-fold performance of the single final model.
3. *Evidence check.* Nijman et al. (*J Clin Epidemiol* 2022;142:218–229, [10.1016/j.jclinepi.2021.11.023](https://doi.org/10.1016/j.jclinepi.2021.11.023)) on inadequate missing-data handling in prediction-model studies. Riley et al. (*Stat Med* 2019;38:1276–1296, [10.1002/sim.7992](https://doi.org/10.1002/sim.7992)) on minimum sample size — with 97 five-year events and nine parameters, events per parameter is about 11 at that horizon.
4. *Required improvement.* Resolve the pre-specification sentence. Report bootstrap or penalisation-aware intervals in Table 2, or remove the intervals. Use multiple imputation with uncertainty propagation and re-report the lipid terms. Obtain kinship and re-estimate with family-clustered resampling. Report a single-pass out-of-fold C alongside the 10-repeat average.
5. *Suggested wording.* "No pre-specification document could be located; the specification is therefore reported as post hoc and no pre-specification claim is made."
6. **Severity: MAJOR.**

- **BS:** item (c) is the one I want on the record most firmly. The Discussion builds a substantive argument — "why the lipid terms did not dominate" — on estimates that a single median imputation is expected to bias towards the null. That argument cannot be made until the imputation is fixed.
- **CA:** no independent objection.
- **LM:** BS's point is mine as well from the other side: I cannot accept a biological conclusion about LDL in FH that rests on median-imputed, divisor-corrected lipids with a reconstruction correlation of 0.32.
- **ED:** this is the clearest convergence between the statistical and lipid seats and it should be revision priority two, behind the population question.

**Methods — Comparator implementation**
1. *Current claim.* Three instruments transcribed from primary papers; SAFEHEART-RE used measured rather than back-calculated LDL-C, with previous ASCVD zero by design and WHO-inferred BMI cut-points, and reproduced both published worked examples; FH-Risk-Score restricted to age ≤65; Montreal used ever smoking; UK Biobank Lp(a) in nmol/L divided by 2.15 to approximate mg/dL; strict complete-input evaluability; no missing input assigned to a favourable category.
2. *Weakness.* The comparator fidelity work is the best-executed part of the study — reproducing both SAFEHEART worked examples before scoring is exactly right, and refusing to impute favourable categories is exactly right. Two problems remain. (a) **The Lp(a) unit conversion is not a defensible fixed operation.** Kronenberg et al. state that molar and mass units are not interconvertible by a constant, because the relationship depends on apolipoprotein(a) isoform size; dividing by 2.15 to dichotomise at 50 mg/dL therefore misclassifies participants non-randomly. This misclassification degrades *only* the two Lp(a)-dependent comparators and never CALON-C, producing a systematic bias in the index model's favour. (b) Zeroing SAFEHEART-RE's previous-ASCVD term removes the strongest predictor in its published equation. The manuscript treats this as a neutral design consequence, but it guarantees degraded comparator performance.
3. *Evidence check.* Kronenberg et al. ([10.1093/eurheartj/ehac361](https://doi.org/10.1093/eurheartj/ehac361)) on non-interconvertibility of Lp(a) units. Tamehri Zadeh et al. 2026 obtained SAFEHEART-RE C = 0.802 (0.711 to 0.888) in genotype-confirmed *primary prevention*, where the previous-ASCVD term is likewise inert — which shows that zeroing that term does not by itself explain a fall to 0.6308.
4. *Required improvement.* Replace the fixed divisor with a threshold sensitivity analysis over the plausible molar range (105 and 125 nmol/L in addition to 50 mg/dL ÷ 2.15) and report every comparator delta under each. State that the resulting misclassification biases comparisons towards CALON-C.
5. *Suggested wording.* "Because molar and mass Lp(a) units are not interconvertible by a fixed factor, the 2.15 divisor introduces non-random misclassification of the Lp(a) term in SAFEHEART-RE and FH-Risk-Score but not in CALON-C, and therefore biases these comparisons in favour of CALON-C by an unquantified amount."
6. **Severity: MAJOR.**

- **BS:** any measurement-error mechanism that operates on the comparator and not on the index model is a differential bias and must be quantified, not merely disclosed.
- **CA:** no independent objection.
- **LM:** this is my second principal objection. Lp(a) unit handling is a well-known trap in lipidology and the manuscript walks into it while explicitly flagging that the divisor is not printed in the source papers — it identifies the hazard and proceeds anyway.
- **ED:** the Australian comparison in point 3 above is the most damaging single juxtaposition available to a reviewer, because it removes the previous-ASCVD explanation from the table.

**Methods — Head-to-head comparisons and multiplicity**
1. *Current claim.* Comparisons on each comparator's complete-input subset with CALON-C recomputed on the same set; paired cluster bootstrap (B = 2,000); WIN requires an interval excluding zero, a positive estimate with an interval crossing zero is a TIE; strata with fewer than 10 events not estimated; the confirmatory family comprises three comparators at full and five-year follow-up (six comparisons) with Holm correction; ten-year comparisons, Lp(a)-omitted implementations, Welsh comparisons and variable-set refits are exploratory.
2. *Weakness.* (a) The paragraph does not state that CALON-C's predictor is out-of-fold. It is — I verified this at `code/33_CALON_C.py`, where the out-of-fold linear predictor from the cross-validation routine is what enters the paired bootstrap. This is the single most important methodological reassurance in the paper and it is unstated. (b) **The ten-year horizon is excluded from the confirmatory family without justification**, although it is FH-Risk-Score's native horizon and the standard clinical horizon, while "full follow-up" — a censoring-determined, non-clinical quantity — is made primary. (c) In UK Biobank the "cluster bootstrap" is a participant bootstrap, since the Methods elsewhere state clusters are singletons; the two descriptions conflict. (d) The three comparisons are conducted in three different populations (2,470, 2,811 and 1,913 participants), so the deltas are not mutually comparable and a Holm family spanning them is a family of non-exchangeable tests.
3. *Evidence check.* Blanche et al. ([10.1093/biostatistics/kxy006](https://doi.org/10.1093/biostatistics/kxy006)) on the impropriety of Harrell's C for *t*-year risk. Riley et al. (*BMJ* 2024;384:e074820, verified) on comparative evaluation design.
4. *Required improvement.* State the out-of-fold basis explicitly. Make ten years the primary horizon or justify its exclusion in one sentence. Report all nine cells. Correct the cluster-bootstrap description for UK Biobank.
5. *Suggested wording.* "CALON-C was represented by its out-of-fold cross-validated linear predictor; each published instrument was applied unchanged. Both were therefore evaluated out of sample with respect to coefficient estimation, although CALON-C's specification was selected using these data."
6. **Severity: MAJOR.**

- **BS:** I want the record to show that the design here is better than the manuscript makes it appear, and that the horizon selection is worse. Having examined `calon_c_corrected_headtohead.csv`, the omitted ten-year cells do **not** reverse any conclusion: SAFEHEART-RE +0.070 (95% CI 0.028 to 0.114), Montreal +0.028 (0.003 to 0.056), FH-Risk-Score +0.011 (−0.020 to 0.045, TIE). The omission is therefore selective reporting without a self-serving motive — which is still selective reporting, and an editor cannot verify the absence of motive.
- **CA:** ten years is the horizon in which cardiology thinks and in which every guideline threshold is expressed. Making "full follow-up" primary renders the result clinically unusable.
- **LM:** agreed with CA.
- **ED:** adopted. I note this is the one place where the panel's finding *improves* the paper's standing, and it should be reported as such rather than buried.

**Methods — Calibration, model equation, and transport**
1. *Current claim.* The equation is published in raw units with baseline survival; calibration is reported as internal only, following a reviewer judgement that an out-of-fold or external baseline is required before any transportable absolute-risk claim; for transport, source-cohort equation and preprocessing were frozen and applied without refitting, nine terms to Wales and seven to UK Biobank; these are transport estimates, not untouched independent validations.
2. *Weakness.* (a) The transport estimates have **no uncertainty quantification whatsoever** — confirmed in source, where the transport function returns a point estimate. The asymmetry claim (0.7252 versus 0.6600) is unfalsifiable as reported. (b) The reviewer-response provenance ("The later reviewer response judged…") is unpublishable prose. (c) Publishing the full equation is a genuine strength and should be foregrounded rather than buried mid-Methods.
3. *Evidence check.* Riley et al. (*BMJ* 2024;384:e074821, [10.1136/bmj-2023-074821](https://doi.org/10.1136/bmj-2023-074821)) on sample size for external validation; Van Calster et al. ([10.1186/s12916-019-1466-7](https://doi.org/10.1186/s12916-019-1466-7)) on the primacy of calibration; Austin and Steyerberg (*Stat Med* 2019;38:4051–4065, [10.1002/sim.8281](https://doi.org/10.1002/sim.8281)) for calibration metrics with intervals.
4. *Required improvement.* Bootstrap both transport C values and report intervals; formally test the asymmetry or withdraw the claim. Remove reviewer-process language.
5. *Suggested wording.* "Transport discrimination was C = 0.725 (95% CI …) from UK Biobank to Wales and C = 0.660 (95% CI …) in the reverse direction; the intervals overlap/do not overlap, so the asymmetry is/is not supported."
6. **Severity: MAJOR.**

- **BS:** a bare point estimate carrying a structural claim is the most straightforwardly correctable major defect in the paper. Two hundred lines of bootstrap code already exist in the repository.
- **CA:** no independent objection.
- **LM:** the two directions differ in age range, treatment intensity, lipid severity and endpoint composition. Even with intervals, "asymmetry" will not be attributable to any one of these.
- **ED:** LM is right that the interval will not identify the mechanism, but BS is right that without it there is no finding at all. Both go in.

**Methods — Proportional hazards, competing risk, and sensitivity analyses**
1. *Current claim.* Schoenfeld tests globally and by term; Aalen–Johansen where a usable death indicator existed; the Welsh arm executed and the UK Biobank arm did not because the script guarded on a `death` column present only in the Welsh frame; six sensitivity analyses, with the endpoint-date restriction acknowledged as informative by construction.
2. *Weakness.* A software guard is not a scientific limitation. The programme's own data inventory records a death date field in the UK Biobank survival extract, so this is a fixable defect being reported as a result. Separately, absence of a detected proportional-hazards violation with 289 events is weak evidence of proportionality, and "16 tested terms" conflates the nine UK Biobank and seven Welsh terms into a single count across two different models.
3. *Evidence check.* Austin and Fine ([10.1002/sim.7501](https://doi.org/10.1002/sim.7501)) on competing-risk reporting.
4. *Required improvement.* Fix the guard, run the analysis, report UK Biobank Aalen–Johansen cumulative incidence at five and ten years with competing-death counts. Report proportional-hazards tests separately by cohort.
5. *Suggested wording.* Report per cohort: "Nine terms were tested in UK Biobank and seven in Wales; no term violated the assumption at p < 0.05, although power to detect non-proportionality was limited."
6. **Severity: MAJOR.**

- **BS:** the honesty is admirable and the remedy is one line of code. There is no defensible reason to submit without it.
- **CA:** with 35 competing deaths against 102 events in Wales, competing mortality is quantitatively material, and the missing UK Biobank estimate blocks every absolute-risk statement in the paper.
- **LM:** no independent objection.
- **ED:** unanimous.

**Methods — Grey-zone and subgroup analyses**
Correctly labelled as a predecessor-model ancillary analysis that cannot support a reclassification claim, and correctly refuses to import superseded subgroup outputs. This is the manuscript at its best. **Severity: MINOR.**
**BS:** if it cannot support a claim about CALON-C, ask what it is doing in the paper; the stated reason — "because the user requested explicit grey-zone treatment" — is not a scientific reason and must not appear in a submitted manuscript. **CA:** agreed; it dilutes the paper. **LM:** I dissent in part. The negative Lp(a) and apoB/LDL-C result is the most interesting finding in the manuscript, because it is discordant with FH literature and therefore diagnostic of a problem with the frame. Keep it, and reinterpret it as evidence about the data rather than about the biomarkers. **ED:** LM's dissent is upheld over BS and CA. Retain the analysis, delete the justification, and reframe it as a data-quality signal.

**Methods — Literature verification**
Transparent about tool availability: Scite was not callable and a Perplexity connector returned an authentication error; no PRISMA claim is made. Appropriate. **Severity: MINOR.**
**ED:** the reference-list defects documented in this review — a wrong title at reference 9, a miscitation at reference 10, and 19 of 39 references never cited — indicate that whatever verification was performed did not include a citation-fidelity pass. The paragraph should not claim source verification until it has.

### Results

**Results — Study populations**
1. *Current claim.* 3,209 participants and 289 events, "corresponding to 6.55 events per 1,000 person-years in the available pre-correction descriptive output"; baseline characteristics; cases were older, more often male, hypertensive and diabetic, with higher untreated-equivalent non-HDL-C; the corrected Welsh risk set was 1,169/102 and a corrected Welsh Table 1 is absent.
2. *Weakness.* The event rate is taken from a pre-correction output and attached to a corrected event count in the same sentence. A rate of 6.55 per 1,000 person-years implies roughly 44,000 person-years and about 13.8 years of mean follow-up, which is plausible, but the reader cannot tell which numerator and denominator produced it. Median follow-up and person-years for the corrected frame are never reported for either cohort.
3. *Evidence check.* No literature needed.
4. *Required improvement.* Report person-years, median follow-up with interquartile range, and the incidence rate with a 95% confidence interval for the corrected frames in both cohorts.
5. *Suggested wording.* Remove the pre-correction rate until it is regenerated.
6. **Severity: MODERATE.**

- **BS:** a survival paper that does not report follow-up duration for its analysed cohort is incomplete on its face.
- **CA:** the clinically arresting number is buried: 52.4% hypertensive and 9.8% diabetic at median age 57 in a putative FH cohort, with only 10.2% current smokers. That profile is a general middle-aged population profile, and it is the reason the clinical risk factors dominate the model.
- **LM:** untreated-equivalent LDL-C median 3.95 mmol/L (IQR 3.32 to 4.68) is the decisive figure. Untreated heterozygous LDLR carriers should sit far higher. Table 1 refutes the FH framing on its own.
- **ED:** CA and LM independently reach the population verdict from Table 1 alone, without genetics. That is the most economical form of the argument and should open the Discussion.

**Results — Predictor-level associations in UK Biobank**
1. *Current claim.* Diabetes had the largest adjusted association (HR 2.120, 95% CI 1.610 to 2.793), then male sex (1.702, 1.372 to 2.111) and hypertension (1.610, 1.279 to 2.028); current smoking 1.329 (0.959 to 1.842); none of the three lipid terms was independently significant; CALON-C added +0.041 in C over age and sex, of which about +0.033 came from hypertension, diabetes and smoking, leaving about +0.008 for the lipid apparatus.
2. *Weakness.* The interpretation is admirably candid, but three of the reported associations are TIEs by the review's own convention (smoking 1.329, 0.959 to 1.842; cumulative non-HDL-C 1.119, 0.954 to 1.334; remnant cholesterol 1.113, 0.970 to 1.296) and should be described as such rather than as ordered contributions. The decomposition into +0.033 and +0.008 is reported without intervals, and increments in C are not additive, so the partition is illustrative rather than estimated.
3. *Evidence check.* Insufficient validated evidence within the window bears directly on variance decomposition of C in FH cohorts.
4. *Required improvement.* Label TIEs. Attach intervals to both increments, or present them as a single ΔC over age and sex with an interval and describe the partition qualitatively.
5. *Suggested wording.* "Relative to age and sex, CALON-C added ΔC +0.041 (95% CI …). Most of this increment was attributable to hypertension, diabetes and smoking; the three lipid-derived terms contributed little and none was individually associated with the outcome."
6. **Severity: MODERATE.**

- **BS:** decomposing a concordance difference into additive parts is not a defined operation. Say so, or bootstrap the nested comparisons.
- **CA:** the finding itself is clinically credible and important — in a high-LDL stratum, near-term risk is driven by diabetes, hypertension, sex and smoking. That is a publishable message in its own right.
- **LM:** the finding is credible *only* if the lipid measurements are sound, and I have argued they are not: 12.4% median-imputed, divided by a fixed 0.70, with reconstruction correlation 0.32. The null lipid result is at least partly measurement-induced.
- **ED:** a substantive disagreement between CA and LM, and it should not be smoothed. CA reads the null lipid finding as biology; LM reads it as measurement error. The manuscript currently adopts CA's reading without acknowledging LM's. Both must be stated, and the multiple-imputation reanalysis is what would adjudicate between them.

**Results — Internal discrimination**
1. *Current claim.* Out-of-fold C 0.7081 full, 0.7043 at ten years, 0.7254 at five years; apparent 0.7154, 0.7152, 0.7449; optimism 0.0059, 0.0072, 0.0113; corrected 0.7095, 0.7079, 0.7336; estimators differed by no more than 0.008. Welsh pre-correction values 0.7653, 0.7605, 0.7590 are provisional pending regenerated artefacts.
2. *Weakness.* Six C values to four decimal places, none with a confidence interval, from 289, 194 and 97 events. Four-decimal precision is unsupportable at these event counts. The close agreement of the two estimators is presented as reassurance, but both share the same specification and both are blind to specification-search optimism.
3. *Evidence check.* TRIPOD+AI (*BMJ* 2024;385:e078378, [10.1136/bmj-2023-078378](https://doi.org/10.1136/bmj-2023-078378)) requires uncertainty for all performance measures. Riley et al. ([10.1002/sim.7992](https://doi.org/10.1002/sim.7992)) on events per parameter.
4. *Required improvement.* Report every C as three decimals with a 95% confidence interval. Add a sentence stating that neither estimator captures specification-selection optimism.
5. *Suggested wording.* "Optimism-corrected C over full follow-up was 0.710 (95% CI …). Because the specification was selected using these data across several model generations, both internal estimators remain optimistic to an unquantified degree."
6. **Severity: MAJOR.**

- **BS:** this is the paragraph where the absence of intervals is least defensible, because the whole paper rests on these six numbers.
- **CA:** a C of 0.71 is moderate and the manuscript says so. No objection to the honesty.
- **LM:** the Welsh values (0.765) exceed the UK Biobank values (0.710) substantially, which is worth explaining — a narrower, more severely affected, more homogeneously treated clinic cohort behaving differently is itself informative.
- **ED:** LM identifies an unexploited finding. The cohort contrast is more interesting than the comparator tally.

**Results — Head-to-head comparison with published FH instruments** *(five paragraphs, taken together)*
1. *Current claim.* SAFEHEART-RE +0.070 (0.036 to 0.104), Holm p = 0.0003 on 2,470/221; Montreal +0.032 (0.011 to 0.055), p = 0.0179 on 2,811/252; FH-Risk-Score +0.015 (−0.011 to 0.040), p = 0.5018 on 1,913/146, a TIE; the measured-LDL-C correction increased the SAFEHEART delta from +0.032 to +0.070; five-year differences did not survive Holm correction; Wales was non-estimable for two instruments and produced only ties; no comparator significantly outperformed CALON-C anywhere.
2. *Weakness.* I verified every reported figure against `calon_c_corrected_headtohead.csv` and **all reported numbers are faithful**. Three reporting failures nonetheless stand. (a) The **UK Biobank Lp(a)-omitted results are never reported numerically**, although one is a WIN against FH-Risk-Score (+0.020, 95% CI 0.0002 to 0.041) and one against SAFEHEART-RE (+0.070, 0.042 to 0.100 on 3,041/268); the Discussion alludes to "a marginal Lp(a)-omitted interval above zero" without the number. (b) The Welsh comparisons used a **Wales-refitted seven-term out-of-fold model**, not the frozen transported equation — evident from Welsh CALON-C C values of 0.754 to 0.793 against a transport C of 0.725, and confirmed in source. The manuscript never says which model was compared. (c) Comparator C values carry no intervals.
3. *Evidence check.* SAFEHEART-RE reached C = 0.767 (0.706 to 0.827) overall and 0.802 (0.711 to 0.888) in primary prevention in genotype-confirmed HeFH (Tamehri Zadeh et al. 2026, [10.1016/j.atherosclerosis.2026.120799](https://doi.org/10.1016/j.atherosclerosis.2026.120799)), against 0.6308 here. Montreal-FH-SCORE was derived cross-sectionally against prevalent disease ([10.1016/j.jacl.2016.10.004](https://doi.org/10.1016/j.jacl.2016.10.004)).
4. *Required improvement.* Report all nine strict cells and all Lp(a)-omitted cells in one table with n, events, C values, intervals and verdicts. State explicitly which CALON-C model entered each Welsh comparison.
5. *Suggested wording.* "In Wales, comparisons used a Wales-developed seven-term CALON-C model evaluated out of fold, not the frozen UK Biobank equation; the Welsh comparisons therefore do not test transport."
6. **Severity: MAJOR.**

- **BS:** point (b) has a consequence the manuscript misses, and it favours the sceptic. Because the Welsh comparisons gave CALON-C a locally refitted model and still returned only ties, the honest reading is stronger than "no external head-to-head win" — it is that CALON-C could not beat these instruments in Wales *even with a local refit*.
- **CA:** the SAFEHEART-RE value of 0.63 is the number I disbelieve. In a genotype-confirmed primary-prevention cohort the same equation reaches 0.80. Either this cohort is not comparable or the implementation is degraded, and the manuscript should investigate rather than bank the win.
- **LM:** I concur with CA and add the mechanism: the Lp(a) term is inert here, by measurement or by conversion, and it is a load-bearing term in SAFEHEART-RE.
- **ED:** the paragraph reporting that the SAFEHEART correction "moved in CALON-C's favour" and framing this as evidence of good faith is rhetorically effective and substantively beside the point. The relevant question is not the direction of the correction but why the absolute value is a global outlier.

**Results — Calibration and model equation**
1. *Current claim.* Ten-year slope 1.101 (0.884 to 1.318), expected 6.20% against Kaplan–Meier observed 6.15%, expected:observed 1.008 (0.883 to 1.153); five-year slope 1.197 (0.900 to 1.494), expected:observed 1.004 (0.832 to 1.235); scaled Brier 3.3% and 1.8%; internal only; the lowest five-year decile contained no events; worked examples verify arithmetic and no risk category is validated.
2. *Weakness.* (a) A **scaled Brier score of 3.3%** indicates that the model explains very little outcome variation, and the manuscript reports it without comment while describing calibration as acceptable. This is the single most under-interpreted number in the paper. (b) The calibration slope exceeding unity is the expected consequence of ridge shrinkage and should be explained rather than presented as agreement. (c) Both slopes have intervals spanning clinically meaningful miscalibration. (d) No Brier interval is given.
3. *Evidence check.* Van Calster et al. ([10.1186/s12916-019-1466-7](https://doi.org/10.1186/s12916-019-1466-7)) on calibration hierarchy and why aggregate expected:observed ratios are the weakest level; Austin and Steyerberg ([10.1002/sim.8281](https://doi.org/10.1002/sim.8281)) for integrated calibration index reporting.
4. *Required improvement.* Interpret the scaled Brier explicitly. Report calibration at Van Calster's moderate level with a flexible curve and an integrated calibration index with intervals. Explain the slope above unity as a shrinkage consequence.
5. *Suggested wording.* "The scaled Brier score of 3.3% at ten years indicates that the model accounts for only a small fraction of outcome variation, consistent with moderate discrimination and a low absolute event rate."
6. **Severity: MAJOR.**

- **BS:** an expected:observed ratio of 1.008 computed in the development data is very nearly a tautology and should carry the least weight of anything in this section, yet it is the number quoted in the abstract.
- **CA:** a predicted ten-year risk of 6.20% in a putative FH cohort at median age 57 is clinically implausible and would, if believed, justify *less* intensive treatment than guidelines require. This is where a mis-specified population becomes a patient-safety issue.
- **LM:** CA's point is the one I would put to an editor. A calibrated model on the wrong population is more dangerous than an uncalibrated one.
- **ED:** CA's framing elevates this from a statistical to a safety finding, and it belongs in the Discussion's clinical-implications paragraph, which currently does not contain it.

**Results — Reciprocal transport**
1. *Current claim.* Frozen nine-term UK Biobank equation ranked Welsh participants at C = 0.7252; frozen seven-term Welsh equation ranked UK Biobank participants at C = 0.6600; the asymmetry is compatible with differences in age range, ascertainment, lipid severity, predictor timing and endpoint measurement, and argues against treating either direction as simple geographic replication.
2. *Weakness.* No intervals, so the asymmetry may be noise; the manuscript then builds an interpretation on it. The listed explanations are all plausible and none is testable with the data described, which should be stated rather than left as a list.
3. *Evidence check.* Debray et al. (*J Clin Epidemiol* 2015;68:279–289) provide the standard framework for interpreting validation across settings but fall outside my eligible window and are recorded in the excluded-context note; within the window, Riley et al. (*BMJ* 2024;384:e074820, verified) serve the same purpose.
4. *Required improvement.* Bootstrap both estimates and report the difference with an interval. If the interval includes zero, describe the directions as indistinguishable.
5. *Suggested wording.* "The two transport estimates differed by 0.065 (95% CI …). We cannot attribute this difference to any single cohort characteristic."
6. **Severity: MAJOR.**

- **BS:** with 102 Welsh events, a difference of 0.065 in C is well within plausible sampling variation, and the manuscript's central structural claim may not survive its own interval.
- **CA:** the endpoints differ — Wales includes angina and revascularisation, UK Biobank has no procedure data — so the two directions predict materially different things. This alone can generate the asymmetry.
- **LM:** the Welsh cohort is clinic-ascertained with more severe lipid phenotype and different treatment intensity; a model trained on an attenuated-phenotype population may transport into a severe-phenotype population more easily than the reverse.
- **ED:** CA and LM offer two distinct and untested mechanisms and BS argues there may be nothing to explain. That disagreement should be visible in the revised paragraph rather than resolved by assertion.

**Results — Proportional hazards and competing risk**
Covered under Methods above; the same defects appear here. The phrase "35 competing deaths among 102 events" is incoherent, since competing deaths are not among the events. **Severity: MAJOR** (for the unexecuted UK Biobank arm), **MINOR** (for the phrasing).
**BS:** as displayed, Table 5 pairs a Welsh Aalen–Johansen cumulative incidence of 6.02% with a Kaplan–Meier observed risk of 5.40%. Within one risk set the Aalen–Johansen estimate cannot exceed the Kaplan–Meier complement. The table note discloses that the two come from different frames, which means the row is not internally interpretable and must not be published in that form. **CA, LM:** concur. **ED:** unanimous; this is the clearest single internal-consistency defect in the manuscript.

**Results — Missing data and comparator evaluability**
1. *Current claim.* Missingness 12.4% for non-HDL-C/HDL-C-derived terms, 5.0% for the triglyceride filter, 22.5% for Lp(a); missingness indicators not significantly associated with outcome; in Wales, BMI 54.5%, diabetes 41.6%, smoking 26.4% missing and the native Lp(a) field unusable owing to mixed units; the inability to apply full instruments in Wales is an implementation finding, not evidence of inferiority.
2. *Weakness.* The final sentence is exactly right and is one of the paper's best contributions. But the missingness-indicator test is weak evidence of ignorability and is treated as though it licensed single imputation, and the strict complete-input rule creates three different evaluable populations whose selection is itself associated with assay completeness and attendance.
3. *Evidence check.* Nijman et al. ([10.1016/j.jclinepi.2021.11.023](https://doi.org/10.1016/j.jclinepi.2021.11.023)).
4. *Required improvement.* Compare characteristics of evaluable and non-evaluable participants for each comparator. Replace single imputation with multiple imputation.
5. *Suggested wording.* "Complete-input evaluability differed across instruments (2,470, 2,811 and 1,913 participants), so the three comparisons are not conducted in the same population."
6. **Severity: MODERATE.**

- **BS:** an absent association between a missingness indicator and the outcome does not establish that data are missing at random conditional on the model.
- **CA:** the operational finding is genuinely useful — a score that cannot be computed cannot be used.
- **LM:** that a national FH registry cannot supply usable Lp(a) is itself a publishable observation about FH care quality, and the EAS FH Studies Collaboration (*Atherosclerosis* 2018;277:234–255, verified, currently uncited) is the natural anchor for it.
- **ED:** LM's suggestion converts an apologetic passage into a contribution. Adopt.

**Results — Grey-zone analysis**
1. *Current claim.* 3,333 carriers scored, 1,685 with 218 events in the 5–20% band; adding Lp(a) changed C by −0.0038 (−0.0089 to 0.0018), apoB/LDL-C by +0.0146 (−0.0050 to 0.0330), both by +0.0118 (−0.0088 to 0.0324); none significant; apoB/LDL-C was associated with outcome (HR 1.154 per SD, 1.027 to 1.295) whereas Lp(a) was not (1.033, 0.923 to 1.157).
2. *Weakness.* The cohort is 3,333, not 3,209, and the base model differs, so this analysis is not comparable with anything else in the paper. The three reported base C values are mutually inconsistent by small amounts (implying 0.5986, 0.5980 and 0.5984), presumably because Lp(a) missingness changes the evaluable subset — but no base C and no subset size is reported for each row. Within-band C near 0.60 is barely above chance and goes unremarked.
3. *Evidence check.* Kronenberg et al. ([10.1093/eurheartj/ehac361](https://doi.org/10.1093/eurheartj/ehac361)) establish that Lp(a) is causal and independently predictive, which makes a null here a signal about the data.
4. *Required improvement.* State the base C and evaluable n for each row. Reconcile the three implied base values.
5. *Suggested wording.* "Within-band discrimination of the base model was approximately 0.60, close to chance, as expected when a narrow predicted-risk band is selected."
6. **Severity: MODERATE.**

- **BS:** the closing sentence — "an associated biomarker need not improve ranking" — is correct and well made.
- **CA:** the negative Lp(a) result must not be allowed to read as clinical permission to omit Lp(a) testing.
- **LM:** this is my central evidentiary point restated. Lp(a) returning HR 1.033 (0.923 to 1.157) in a supposed LDLR-carrier cohort is discordant with the entire FH literature and should trigger an audit of the Lp(a) field and its unit handling, not a conclusion about biomarkers.
- **ED:** LM's reinterpretation is adopted, and it is the single most constructive redirection available to this manuscript.

**Results — Subgroups**
Reports the absence of corrected subgroup outputs rather than substituting older ones. Correct conduct. **Severity: MINOR.** No seat raises an independent objection, though **BS** notes that absent subgroup analyses cannot be reported as a Results subsection and belong in the limitations.

### Discussion

**Discussion — Principal findings**
1. *Current claim.* Four defensible findings: moderate internal discrimination; better than SAFEHEART-RE and Montreal after correction, tying FH-Risk-Score; frozen equation retained ranking information in Wales though asymmetrically; specialised biomarkers did not improve discrimination in an intermediate band.
2. *Weakness.* Finding two rests on an outlier comparator value and a cross-estimand comparison; finding four rests on a predecessor model in a cohort where Lp(a) appears non-informative. Neither is as defensible as claimed. The second paragraph's argument that corrections "moved in both directions" is presented as evidential support; it is evidence of process integrity, not of validity.
3. *Evidence check.* As above.
4. *Required improvement.* Reduce to two defensible findings — moderate discrimination from routine data, and comparator non-estimability in a real registry — and reclassify the rest as observations requiring a variant-confirmed cohort.
5. *Suggested wording.* "Two findings are robust to the limitations of this frame: a routine-data model achieved moderate discrimination, and two of three published instruments could not be computed in a national registry. The comparator differences require confirmation in a variant-confirmed cohort with validated Lp(a) measurement."
6. **Severity: MAJOR.**

- **BS:** process integrity is not evidence. The corrections paragraph should be a supplementary changelog.
- **CA:** "retained ranking information" is fair; "asymmetric" is asserted without an interval.
- **LM:** finding four should be inverted, as argued above.
- **ED:** adopted in full.

**Discussion — What is genuinely new**
1. *Current claim.* Novelty is incremental and methodological; the defensible contribution is a common-data, comparator-faithful evaluation of four models in a population-based UK LDLR-carrier frame plus a parsimonious model requiring no specialised assay; the precise wording is the first identified head-to-head application of CALON-C and three named instruments within the present corrected UK Biobank carrier frame.
2. *Weakness.* The priority claim is qualified into near-tautology — "within the present corrected UK Biobank carrier frame" is a set defined by this study, so first-ness is guaranteed and uninformative. Separately, the paragraph contains an instruction to the authors ("This priority claim should be rechecked immediately before submission") which must be deleted. And the Combined-FH-Score, evaluated in the same Australian paper the manuscript cites, is neither assessed nor mentioned.
3. *Evidence check.* Tamehri Zadeh et al. 2026 evaluated SAFEHEART-RE, FH-Risk-Score *and* the Combined-FH-Score head-to-head in 655 genotype-confirmed patients with 53 events over a median 6 years — the closest overlapping work, and a genuine three-way head-to-head on common participants ([10.1016/j.atherosclerosis.2026.120799](https://doi.org/10.1016/j.atherosclerosis.2026.120799)).
4. *Required improvement.* Delete the self-addressed instruction. Restate novelty as the *population* being novel (population-ascertained rather than clinic-ascertained) rather than the comparison being first. Acknowledge the Combined-FH-Score omission.
5. *Suggested wording.* "Head-to-head comparison of these instruments on common participants has been reported in clinic-ascertained genotype-confirmed cohorts. The contribution here is the shift of setting to a population-ascertained frame, in which two of the three instruments proved non-estimable and all performed less well than previously reported."
6. **Severity: MAJOR.**

- **BS:** a first-ness claim indexed to a self-defined analysis set is not a priority claim.
- **CA:** no independent objection.
- **LM:** the honest novelty is the setting shift and the demonstration that clinic-derived FH instruments degrade in a population frame. That is a real and interesting result which the manuscript nearly states and then obscures with a tally.
- **ED:** LM's reframing is the most valuable single suggestion in this review for the paper's publishability. The comparator tally is not the paper; the setting-transfer failure is.

**Discussion — Comparison with established FH risk instruments** *(four paragraphs)*
These are the manuscript's most careful pages. The SAFEHEART discussion correctly notes that two of its strongest design features carry less information here; the Montreal discussion correctly notes the estimand difference; the FH-Risk-Score discussion correctly treats the TIE as more informative than either significant comparison and states that a tie neither proves equivalence nor justifies replacement; the guideline paragraph is appropriately cautious. **Severity: MODERATE**, for one omission: nowhere is it acknowledged that SAFEHEART-RE's C of 0.6308 is the lowest value reported in any published cohort, nor that the contemporaneous genotype-confirmed Australian estimate of 0.802 in primary prevention removes the "inert previous-ASCVD term" explanation.
**BS:** the paper reasons about *why* SAFEHEART-RE should perform less well and never asks whether it should perform *this much* less well. That is the difference between explaining a result and auditing it.
**CA:** the sentence "FH diagnosis itself remains an indication for intensive risk-factor management" appears later and is the most important clinical sentence in the manuscript; it should appear here too.
**LM:** the observation that FH-Risk-Score used untreated or imputed LDL-C in a 57/43 split is in the project's methods artefact but not in the manuscript, and it is directly relevant, because it shows the comparator's authors solved the treatment-correction problem differently and more transparently.
**ED:** BS's distinction between explanation and audit is the intellectual centre of this review and should be quoted to the authors verbatim.

**Discussion — Routine-panel parsimony and global scalability**
Well argued and appropriately hedged, ending with the correct statement that parsimony is not automatically superiority. **Severity: MINOR.**
**LM:** one substantive objection. The paragraph contrasts routine panels with Lp(a) and apoB availability, but a standard lipid panel measures total cholesterol, HDL-C and triglycerides directly and *calculates* LDL-C, so the model's inputs inherit Friedewald limitations at high triglycerides, and the paper never states which LDL-C derivation was used. **CA:** the equity argument is genuine and is the paper's best clinical case. **BS:** no independent objection. **ED:** LM's question about the LDL-C derivation should be answered explicitly in the Methods.

**Discussion — Why the lipid terms did not dominate**
1. *Current claim.* Weak adjusted lipid associations do not contradict LDL causality; causal and within-cohort predictive importance differ; in a high-exposure stratum with restricted range, therapy-altered measurements and age proxying duration, clinical factors can dominate near-term ranking.
2. *Weakness.* The reasoning is correct in general and is the right argument to make. It is however offered as a complete explanation when three measurement artefacts remain unexcluded: 12.4% single median imputation, a fixed ÷0.70 correction with reconstruction correlation 0.32, and — decisively — the fact that the lipid range in this cohort is *not* restricted to a high-exposure stratum, because the carrier flag appears not to select monogenic FH.
3. *Evidence check.* Ference et al. (*Eur Heart J* 2017;38:2459–2472, [10.1093/eurheartj/ehx144](https://doi.org/10.1093/eurheartj/ehx144), verified but **never cited in the text**) is the correct anchor for LDL causality and is sitting unused in the reference list. Gratton et al. 2023 ([10.1161/ATVBAHA.123.319438](https://doi.org/10.1161/ATVBAHA.123.319438)) undermines the restricted-range premise for this cohort.
4. *Required improvement.* Add the measurement-artefact explanation alongside the range-restriction explanation and state which analyses would distinguish them.
5. *Suggested wording.* "Three explanations are not mutually exclusive: genuine range restriction in a high-exposure stratum; attenuation by single median imputation and by a fixed treatment-correction factor whose reconstruction correlation was 0.32; and a carrier definition that did not in fact select a high-exposure stratum. Multiple imputation and a variant-confirmed cohort would distinguish them."
6. **Severity: MAJOR.**

- **BS:** the range-restriction argument requires a restricted range. Table 1 shows untreated-equivalent LDL-C with an interquartile range of 3.32 to 4.68 mmol/L, which is an ordinary population spread.
- **CA:** I hold to my earlier reading that the clinical-factor dominance is real and clinically familiar, but I accept it cannot be established here.
- **LM:** this is where the manuscript's central biological claim collapses, and BS's observation about the interquartile range is the cleanest demonstration of it.
- **ED:** BS supplies the decisive evidence for LM's position, and CA concedes. Recorded as a resolved disagreement, not a manufactured one.

**Discussion — Ascertainment, selection, and UK Biobank representativeness**
Two well-constructed paragraphs correctly citing Fry et al. and the reweighting literature, and correctly stating that the carrier population cannot be assumed to represent clinically recognised FH, that the untreated LDL-C excess was only +0.15 to +0.23 mmol/L, and that apparent internal calibration cannot establish calibration in routine care. **Severity: MODERATE**, only because the paragraph lists carrier-definition breadth as one of four equally weighted possible explanations for the attenuated phenotype when published prevalence data make it much the most likely.
**LM:** the manuscript states the fatal fact and then dilutes it across four candidate explanations. Given a carrier frequency of 1 in 142 against a published 1 in 288, definition breadth is not one hypothesis among four.
**BS:** and it is testable — report the LDL-C distribution in carriers against non-carriers and compare with Gratton et al.
**CA:** if the cohort is not FH, the paper is a different paper, not a hedged version of this one.
**ED:** CA states the editorial consequence precisely. This is why the population issue is FATAL rather than MAJOR.

**Discussion — Survivor bias and age**
Correct, appropriately limited, and rightly notes that the age spline may model changing hazard among survivors and that left truncation is needed. **Severity: MINOR.** No seat raises an independent objection. **BS** adds that the survivor-selection argument strengthens the case against interpreting the two age terms separately in Table 2.

**Discussion — Predictor timing in Wales**
1. *Current claim.* The timing objection is substantive; 55 of 92 events in the earlier frame had blood pressure recorded after the event and medication had no date; attestation and plausibility support that chronic conditions predated events; comparator symmetry matters; removing undated fields cost about 0.030 in C; none of this demonstrates baseline timing, and the dated-only model is a different specification, not a repair.
2. *Weakness.* The reasoning is exemplary and the concession is correct. The one gap is that the concession is not carried through: having accepted that timing cannot be demonstrated, the manuscript still reports the Welsh transport C as a headline result in the abstract and Key points without the qualifier.
3. *Evidence check.* Insufficient validated evidence within the window addresses index-event bias in FH registries specifically.
4. *Required improvement.* Propagate the qualifier to every place the Welsh transport figure appears.
5. *Suggested wording.* In the abstract: "Transport to the All-Wales registry gave C = 0.725 (95% CI …), in a cohort where predictor timing relative to baseline could not be established for hypertension, diabetes or smoking."
6. **Severity: MODERATE.**

- **BS:** with 55 of 92 events having post-event blood pressure, this is not a minor timing imperfection but a plausible reversal of the causal ordering of predictor and outcome for a majority of cases.
- **CA:** clinically, chronic hypertension almost certainly did precede these events, and I would accept the investigators' attestation as reasonable. I part company with BS on how much this matters.
- **LM:** I side with BS. Attestation is not data, and the same fields scored the comparators.
- **ED:** a genuine two-against-one split, and it must be reported as such. CA's clinical judgement is reasonable and BS and LM are right that it is not evidence. The revised text should present the attestation and its insufficiency side by side, which the Discussion already nearly does.

**Discussion — Calibration drift and directional but non-significant differences**
Correctly states that rank can be preserved while absolute risk is mis-estimated, that no threshold should be applied outside the development data, and that a positive but non-significant difference is a TIE requiring more than directional consistency. Among the strongest paragraphs. **Severity: MINOR.**
**BS:** the requirements listed for adoption — untouched validation, satisfactory calibration, net benefit over comparators and simple policies, usability, and preferably evidence of changed decisions — are exactly right and should be moved to the abstract's conclusion.
**CA, LM:** concur. **ED:** adopted.

**Discussion — Lp(a), apoB, and the grey zone**
Correctly states that exclusion was a scalability choice rather than a judgement on relevance, cites the guideline recommendation for once-in-adulthood Lp(a) measurement, notes that coronary calcium adds substantially to SAFEHEART discrimination, and sets out a rigorous standard for a future enhancer study. **Severity: MODERATE**, for the omission already noted: no acknowledgement that the null Lp(a) result in this cohort is discordant with FH evidence and may reflect the unit conversion or the carrier definition.
**LM:** the paragraph's list of requirements for a credible enhancer study is excellent, and the paper should apply the same scepticism to its own null. A null with a misconverted unit is not a null.
**CA:** the sentence recommending Lp(a) measurement must not be undercut by the surrounding discussion.
**BS:** no independent objection. **ED:** LM's symmetry argument is adopted — the standard the paper sets for others must apply to itself.

**Discussion — Competing risks and endpoint definition**
Correctly states that the missing UK Biobank analysis blocks definitive probability interpretation and that the endpoint was not uniform. **Severity: MAJOR**, because the correct diagnosis is followed by no remedy when the remedy is a one-line code fix.
**CA:** the recommendation for future work — harmonised myocardial infarction, ischaemic stroke, cardiovascular death and procedures, with component-specific dates and a hard-coronary sensitivity analysis — is exactly right and could largely be implemented now for UK Biobank.
**BS, LM:** concur. **ED:** unanimous.

**Discussion — Ancestry and fairness**
1. *Current claim.* Cohorts were predominantly European; ancestry was not available in the analysis frame for a formal fairness assessment; performance in White European volunteers cannot be extrapolated; external validation should be multi-ancestry with subgroup reporting and adequate event counts.
2. *Weakness.* "Not available in the CALON-C analysis frame" is the same construction as "lacked kinship data": UK Biobank records self-reported ethnicity and genetic principal components, so this is a frame-construction choice, not a data limitation. Presenting it as the latter is misleading.
3. *Evidence check.* Gratton et al. 2023 ([10.1161/ATVBAHA.123.319438](https://doi.org/10.1161/ATVBAHA.123.319438)) demonstrate that this analysis is feasible in UK Biobank, reporting FH-variant prevalence and statin-adjusted LDL-C separately for 140,439 European, 4,067 South Asian and 3,906 African-ancestry participants, and finding similar prevalence across groups.
4. *Required improvement.* Add ancestry to the analysis frame and report discrimination and calibration by ancestry group, or state plainly that ancestry was available in UK Biobank but not extracted.
5. *Suggested wording.* "Ancestry was not extracted into the analysis frame, although it is available in UK Biobank; no fairness assessment was therefore performed."
6. **Severity: MAJOR.**

- **BS:** TRIPOD+AI item 13 is not satisfied by explaining why a feasible analysis was not done.
- **CA:** the clinical stakes are concrete — Lp(a) distribution, variant spectrum and competing mortality all differ by ancestry.
- **LM:** and Gratton et al. show that South Asian-ancestry FH-variant carriers had the highest statin use (55.6%) with similar LDL-C, so treatment correction may not behave identically across groups.
- **ED:** the pattern of describing extractable variables as unavailable now appears three times — kinship, ancestry, death indicator. A reviewer will notice the pattern and it will damage the paper's credibility more than any single omission.

**Discussion — Overlap and leakage**
Correctly handles temporal leakage, states the FH-Risk-Score dependence, states that freezing now cannot retroactively create an untouched cohort, and concludes that "external validation" is too strong. **Severity: MODERATE**, contingent on the unverified 499-participant figure.
**BS:** the sentence "Freezing the CALON-C equation now prevents further drift but cannot retroactively create a cohort untouched by all development decisions" is the most sophisticated methodological statement in the manuscript and should be preserved exactly.
**CA, LM:** concur. **ED:** endorsed.

**Discussion — Clinical implications**
1. *Current claim.* The immediate implication is methodological; clinically CALON-C is a candidate routine-data ranking tool, attractive where specialised data are unavailable, not ready to guide escalation; FH diagnosis remains an indication for intensive management; a score should refine urgency only after local calibration and demonstrated net benefit and must never de-risk a carrier or defer guideline-directed treatment.
2. *Weakness.* Clinically responsible and correctly refuses a utility claim. The single omission is the safety consequence of the calibration finding: a model predicting 6.20% ten-year risk in a cohort labelled as FH could, if deployed, license under-treatment.
3. *Evidence check.* Vickers, van Calster and Steyerberg (*Diagn Progn Res* 2019;3:18, [10.1186/s41512-019-0064-7](https://doi.org/10.1186/s41512-019-0064-7)) on the decision-curve evidence that a utility claim would require.
4. *Required improvement.* State the under-treatment hazard explicitly.
5. *Suggested wording.* "Because predicted absolute risks in this cohort are low relative to expectations for familial hypercholesterolaemia, any deployment that used these probabilities to triage treatment intensity would risk systematic under-treatment."
6. **Severity: MODERATE.**

- **CA:** this is my most important addition to the manuscript and I want it recorded as a patient-safety point rather than a statistical one.
- **BS, LM:** concur. **ED:** adopted; it also strengthens the case for the population rebuild.

**Discussion — Strengths**
1. *Current claim.* Incident design with explicit exclusions, a published raw-unit equation, two internal estimators, paired common-subset analyses, primary-source comparator corrections, an age gate, a strict missing-input policy, Holm correction, proportional-hazards diagnostics, and explicit withdrawal of unsupported decision-curve claims; corrections moved in both directions and were disclosed even when they strengthened CALON-C.
2. *Weakness.* Several items are process artefacts rather than study strengths. Withdrawing an unsupported claim is the correction of an error. Disclosing that corrections moved in both directions describes conduct, not design. A Strengths paragraph listing audit actions signals to an editor that the document is an audit response.
3. *Evidence check.* None required.
4. *Required improvement.* Retain the four genuine strengths — incident design with explicit prevalent and undated exclusions; a fully published equation with baseline survival; comparator implementations reproduced against published worked examples; out-of-fold evaluation of the index model in every comparison — and delete the rest.
5. *Suggested wording.* "The study's principal strengths are an incident design with explicit exclusion of prevalent and undated outcomes, a fully published equation, comparator implementations verified against published worked examples, and out-of-fold evaluation of the index model in all comparisons."
6. **Severity: MAJOR** (as a publication-readiness matter).

- **ED:** note that the fourth strength in my replacement wording is one the manuscript never claims, because it never states that the comparisons were out-of-fold. The paper is understating its best feature while overstating its process.
- **BS:** concur, emphatically.
- **CA, LM:** no independent objection.

**Discussion — Limitations**
Eleven limitations, comprehensive and frank, correctly leading with the absence of independent external validation. **Severity: MODERATE**, for three defects: the limitations are ranked by discovery order rather than by consequence, so the carrier-definition problem appears second rather than first; three items ("UK Biobank lacked kinship data", the competing-risk failure, and ancestry unavailability) describe extraction choices as data limitations; and the list is a single dense paragraph of eleven numbered items, which is not readable.
**BS:** limitation two should be limitation one, and it should be stated as a threat to the target population rather than as an inability to adjudicate variants.
**CA:** the endpoint limitations — 147 of 289 events with unambiguous dates, no procedure data — deserve their own sentence rather than a clause.
**LM:** the treatment-correction audit (mean absolute error 1.20 mmol/L, correlation 0.32) does not appear in the limitations at all, although it is among the most consequential.
**ED:** all three adopted. Reformat as a short list ordered by consequence.

### Conclusion

**Conclusion ¶1**
1. *Current claim.* Moderate internal discrimination from routine variables; out-discriminated two instruments after correction and tied the third; a frozen equation retained ranking information in Wales as transport rather than independent external validation; findings support further validation but not deployment, thresholds, or universal superiority.
2. *Weakness.* Faithful to the Results and correctly bounded, but inherits the population problem and the absence of intervals, and does not mention the carrier-definition uncertainty at all.
3. *Evidence check.* As above.
4. *Required improvement.* Add the population conditional and at least one interval.
5. *Suggested wording.* "Within a UK Biobank frame defined by an unvalidated LDLR-carrier flag whose frequency and lipid phenotype are both discordant with published pathogenic-variant data, CALON-C ranked first incident atherosclerotic events with moderate discrimination (optimism-corrected C 0.710, 95% CI …). Comparisons with published instruments require confirmation in a variant-confirmed cohort before any interpretation."
6. **Severity: MAJOR.**

- **BS, CA, LM, ED:** unanimous.

### Tables and figure legends (audited, not paragraph-reviewed)

Table 1 is well constructed with standardised mean differences and missingness, and its footnote correctly refuses to present the superseded Welsh table. Table 2 publishes the full equation with baseline survival — a real strength — but reports penalised-model intervals without qualification and presents two age terms as separately interpretable. Table 3 reports six C values without intervals and mixes current and pre-rescue frames in one table, labelled in a Status column. Table 4 is faithful to the source artefact but omits comparator intervals and covers only one of three horizons. Table 5 mixes two Welsh risk sets within single rows, producing an Aalen–Johansen estimate exceeding the Kaplan–Meier complement. Table 6 reports three differences against an unstated and internally inconsistent base C. All five figure legends correctly state their limitations and their sources, and Figure 1's note that "arrows denote model application, not an untouched independent-validation sequence" is a model of honest display. The legends' citation of internal source files must be moved to a data-availability statement.

---

## A. Novelty map

**Genuinely new.**
- Demonstration that two of three established FH instruments are **non-estimable** in a national genotype-positive registry because required inputs do not co-occur in enough participants with events (SAFEHEART-RE 40 participants/1 event; FH-Risk-Score 132/6). I found no comparable published quantification within the window. This is the manuscript's most defensible original contribution and it is currently a subsection of the Results rather than a headline.
- Publication of a complete raw-unit equation with baseline survival at two horizons and worked examples. Uncommon and reproducible.
- Reciprocal application of frozen equations in both directions between a population cohort and a clinical registry. The *design* is novel; the *estimates* are uninterpretable without intervals.

**Incremental but useful.**
- Head-to-head comparison of published FH instruments on common participants with complete-input matching and multiplicity control. The closest overlapping work is Tamehri Zadeh et al. 2026 ([10.1016/j.atherosclerosis.2026.120799](https://doi.org/10.1016/j.atherosclerosis.2026.120799)), which compared SAFEHEART-RE, FH-Risk-Score and the Combined-FH-Score head-to-head in 655 genotype-confirmed HeFH patients with intervals on every C-statistic. **Precise overlap:** same three-plus instruments, same incident ASCVD estimand, same common-participant design, same primary-prevention subsetting. **Residual novelty:** population-ascertained rather than clinic-ascertained frame; larger n (3,209 versus 655) and more events (289 versus 53); addition of an index model; explicit missing-input policy. **Residual deficit:** no intervals, no Combined-FH-Score, and a carrier definition that is not genotype-confirmed — so the Australian study is methodologically superior on the axis that matters most for a comparator paper.
- Demonstration that clinical risk factors dominate lipid terms within a high-LDL-flagged stratum. Related to Jansen et al. 2004 (pre-window, excluded-context note) but the quantified concordance decomposition (+0.033 versus +0.008) is a useful addition, subject to the imputation caveat.

**Already established.**
- That FH-specific scores outperform general-population equations in FH: SAFEHEART-RE derivation ([10.1161/CIRCULATIONAHA.116.024541](https://doi.org/10.1161/CIRCULATIONAHA.116.024541)).
- That SAFEHEART-RE discrimination falls on transport: REFERCHOL ([10.1016/j.atherosclerosis.2020.06.011](https://doi.org/10.1016/j.atherosclerosis.2020.06.011)) and English routine care ([10.1016/j.atherosclerosis.2022.07.011](https://doi.org/10.1016/j.atherosclerosis.2022.07.011)).
- That FH-Risk-Score outperforms SAFEHEART-RE in some settings and not others: derivation C 0.75 versus 0.69 ([10.1161/ATVBAHA.121.316106](https://doi.org/10.1161/ATVBAHA.121.316106)) reversed in Australia (0.735 versus 0.767).
- That UK Biobank volunteer selection distorts associations: [10.1093/aje/kwx246](https://doi.org/10.1093/aje/kwx246), [10.1093/ije/dyae054](https://doi.org/10.1093/ije/dyae054), [10.1038/s41562-023-01579-9](https://doi.org/10.1038/s41562-023-01579-9).
- That cumulative LDL exposure predicts events: [10.1016/j.jacc.2020.07.059](https://doi.org/10.1016/j.jacc.2020.07.059) (reference 22, uncited in text).

**Unsupported priority claims.**
1. "The first identified head-to-head application of CALON-C and the three named published instruments within the present corrected UK Biobank carrier frame." Indexed to a self-defined set; true by construction; carries no priority information.
2. "This combination… appears uncommon in the available literature." Not supportable without a systematic search, which the manuscript disclaims.
3. Implicit in the abstract and Key points: that CALON-C's discrimination advantage over SAFEHEART-RE is a property of the models. Confounded by Lp(a) non-informativeness, unit conversion, and an outlier comparator value.

---

## B. Agreement and disagreement with recent evidence

| Paper (verified) | Relation | Conflict type | Substance |
|---|---|---|---|
| Tamehri Zadeh 2026, *Atherosclerosis* 418:120799 | **Contradictory** | Population/ascertainment | SAFEHEART-RE C 0.767 (0.706–0.827) overall and 0.802 (0.711–0.888) in primary prevention in 655 genotype-confirmed HeFH, against 0.6308 here. The primary-prevention figure removes the inert previous-ASCVD explanation. Most damaging single comparison. |
| Gratton 2023, *ATVB* 43:1737–1742 | **Contradictory** | Population/ascertainment | UK Biobank European FH-variant prevalence 1 in 288 against this cohort's 1 in 142; carriers had significantly higher LDL-C in every ancestry group against +0.15–0.23 mmol/L here. Undermines the carrier definition. |
| Paquette 2017, *J Clin Lipidol* 11:80–86 | **Supportive of the manuscript's caveat; contradictory to its headline** | Endpoint/estimand | Confirms cross-sectional prevalent-CVD derivation (670 carriers, AUC 0.840). The manuscript's caveat is correct; its abstract nonetheless reports "exceeded Montreal-FH-SCORE" as a discrimination result. |
| Paquette 2021, *ATVB* 41:2632–2640 | **Mixed** | Methodological | Confirms the 3,881-patient primary-prevention 10-year design and C 0.75. Does **not** mention UK Biobank in the abstract, leaving the load-bearing 499-participant claim unverified. |
| Pérez de Isla 2017, *Circulation* 135:2133–2144 | **Contradictory** | Methodological | C 0.85 derivation, 0.81 without established ASCVD, optimism 0.003 over 100 resamples on 134 events. Establishes that 0.63 here is anomalous. |
| Kronenberg 2022, *Eur Heart J* 43:3925–3946 | **Contradictory** | Implementation/calibration | Molar and mass Lp(a) units are not interconvertible by a fixed factor; the ÷2.15 divisor introduces differential misclassification affecting only the Lp(a)-dependent comparators. Also establishes Lp(a) as independently predictive, making the null here a data signal. |
| Blanche 2019, *Biostatistics* 20:347–357 | **Challenging** | Methodological | Harrell's C is not proper for *t*-year predicted risk; "full follow-up" C as the primary metric is not the right estimand for a 5- or 10-year clinical decision. |
| Van Calster 2019, *BMC Med* 17:230 | **Challenging** | Implementation/calibration | Aggregate expected:observed ratios are the weakest calibration level; an internally derived slope near unity carries little information. |
| Austin & Fine 2017, *Stat Med* 36:4391–4400 | **Challenging** | Methodological | Reporting standards the unexecuted UK Biobank competing-risk arm fails. |
| Nijman 2022, *J Clin Epidemiol* 142:218–229 | **Challenging** | Methodological | Single median imputation without uncertainty propagation is a documented deficiency; bears directly on the null lipid finding. |
| Munafò 2018, *Int J Epidemiol* 47:226–235 | **Challenging** | Methodological | Outcome-conditional inclusion in the Welsh frame is a selection mechanism of the kind described. |
| Zamora 2025, *Eur Heart J Digit Health* 6:1113–1123 | **Supportive** | — | Supports the manuscript's claim that contemporary FH approaches use many-variable and machine-learning methods, and hence that parsimony is a distinguishable design position. |
| ACC/AHA 2026, *Circulation* 153 | **Supportive** | — | Supports the guideline framing as quoted, including the caution that FH-specific scores "may" be useful. |
| ESC/EAS 2025, *Eur Heart J* 46:4359–4378 | **Supportive** | — | Supports the cumulative-exposure and high-risk-pathway framing. |

**Substantive biological or clinical disagreement.** One, and it is important. The manuscript's position that specialised biomarkers "should not be added merely because they are biologically plausible" is methodologically sound but, as applied to Lp(a) in an FH-adjacent population, conflicts with the EAS consensus position and with both Lp(a)-containing comparators. The panel's lipid seat holds that the null Lp(a) result here is a measurement finding; the manuscript presents it as a biomarker finding. This is a genuine scientific disagreement, not a reporting quibble.

---

## C. Internal manuscript consistency audit

Contradictions found within the manuscript, without recalculation from participant data.

1. **Welsh risk set stated two ways without a single reconciling statement.** Corrected 1,169/102 appears in the abstract, Methods, Results and Table 5's note; pre-rescue 1,159/92 appears in Table 3 and as the n/events in Table 5's own rows. Both appear five times. **MAJOR.**
2. **Table 5 rows are internally impossible as displayed.** Wales five-year: Aalen–Johansen cumulative incidence 6.02% against Kaplan–Meier observed 5.40%; ten-year: 11.97% against 11.08%. With competing events the Aalen–Johansen estimate cannot exceed the Kaplan–Meier complement in one risk set. The footnote reveals different frames, so the rows are not interpretable. **MAJOR.**
3. **Welsh horizon-specific event counts unreconciled.** Methods state 51 events by five years and 75 by ten in the corrected frame; Table 3 and Table 5 give 44 and 66. This implies 7 of the 10 rescued events fell within five years and 9 within ten — arithmetically possible, never stated. **MODERATE.**
4. **Cluster bootstrap described inconsistently for UK Biobank.** "Paired cluster bootstrap resampling with 2,000 draws" (head-to-head Methods) against "UK Biobank used participant-level resampling because no kinship or relatedness field was available" (estimation Methods). **MODERATE.**
5. **Pre-specification asserted and withdrawn in one sentence.** "The specification was fixed before the CALON-C fit, although the repository did not contain a verifiable pre-result specification file and the authors therefore withdrew a formal pre-specification claim." **MAJOR.**
6. **"16 tested terms" conflates two models.** Nine UK Biobank plus seven Welsh terms reported as a single proportional-hazards tally. **MODERATE.**
7. **Event rate from a pre-correction output attached to a corrected event count** in one sentence (6.55 per 1,000 person-years with 289 events). **MODERATE.**
8. **Grey-zone cohort inconsistent with the study cohort** (3,333 against 3,209) and its three implied base C values mutually inconsistent (0.5986, 0.5980, 0.5984). **MODERATE.**
9. **Ten-year comparator deltas absent entirely** although the horizon is named as analysed and declared exploratory. **MAJOR.**
10. **UK Biobank Lp(a)-omitted comparator results absent numerically**, though one is referred to obliquely in the Discussion as "a marginal Lp(a)-omitted interval above zero". **MODERATE.**
11. **Welsh head-to-head model identity never stated.** Reported Welsh CALON-C C values are not given at all in the manuscript; the comparisons used a Wales-refitted model, not the frozen equation. **MAJOR.**
12. **No confidence interval on any C-statistic anywhere** — Tables 3, 4 and 5, both transport estimates, and all abstract values. **MAJOR.**
13. **Nineteen of 39 references never cited in the text**: 13, 14, 16, 17, 22, 23, 26–38. Several are the very sources needed for uncited claims (23 for LDL causality; 31 for statin-intensity correction; 26–28 for validation methodology). **MAJOR.**
14. **Reference 9 title does not match the published record.** **MAJOR.**
15. **Reference 10 attached to a claim it does not support.** **MODERATE.**
16. **Reference 1 page range (e1154–e1276) not corroborated** by the Crossref record, which lists volume 153, issue 17, without pages. Verify against the issue. **MINOR.**
17. **"Decision-curve claims were withdrawn" in the abstract Methods** and the same withdrawal listed as a study strength. **MODERATE.**
18. **Internal process language and self-addressed instructions** in Methods, Results, Discussion, table footnotes and figure legends, including "This priority claim should be rechecked immediately before submission". **MAJOR.**
19. **Excess precision throughout** — C to four decimals, p to four decimals, on 289, 194 and 97 events. **MINOR.**
20. **Reporting framework listed as "TRIPOD+AI; STROBE; RECORD"** while PROBAST is also applied in the Methods. **MINOR.**

Numerical faithfulness to source, where checkable, was good: every comparator delta and interval reported in the Results matches `calon_c_corrected_headtohead.csv` exactly, and the headline values match the provenance ledger. The consistency failures are of *selection*, *frame-mixing* and *citation*, not of arithmetic.

---

## D. Reporting and publication audit

**TRIPOD+AI ([10.1136/bmj-2023-078378](https://doi.org/10.1136/bmj-2023-078378)) — not met.** The manuscript's own closing section lists twelve unresolved items, which is commendable. Beyond those: no uncertainty interval for any discrimination measure (items 12, 16); model-development history across at least six generations not reflected in the performance estimates (item 10); calibration reported only at the weakest level (item 16); fairness assessment feasible but not performed (item 13); the out-of-fold basis of the comparisons unstated (items 10, 16). **Judgement: fails.**

**PROBAST ([10.7326/M18-1376](https://doi.org/10.7326/M18-1376)) — high risk of bias.** *Participants:* high — carrier definition unverified and quantitatively discordant with published prevalence; Welsh inclusion conditioned on outcome. *Predictors:* high — Welsh predictors undated with 55 of 92 events having post-event blood pressure; fixed treatment correction with reconstruction correlation 0.32. *Outcome:* high — 147 of 289 events with unambiguous component dates; heterogeneous composite including I70 and G45; no procedure data. *Analysis:* high — single median imputation; penalised-model intervals; unquantified specification-search optimism; no competing-risk analysis in the development cohort; no intervals on performance. *Applicability:* high — population-ascertained volunteers with attenuated phenotype against clinic-ascertained FH. **Judgement: high risk of bias in all four bias domains and high concern for applicability.**

**STROBE — partially met.** Design, setting, participants and flow are well reported; the corrected flow figure is supplied. Follow-up duration and person-years for the corrected cohorts are absent; subgroup analyses absent; the Welsh censoring rule is not a calendar rule.

**RECORD — not met.** No administrative end-of-recording date for Wales; linkage-quality metrics absent; carrier status not validated against a variant-level classification source; differing linkage completeness across UK nations unaddressed.

**Calibration — internal only, correctly labelled, insufficiently interpreted.** The distinction between internal and transported calibration is drawn carefully and repeatedly, which is a genuine strength. But no flexible calibration curve, no integrated calibration index, no interval on either Brier score, and a scaled Brier of 3.3% left uninterpreted.

**Clinical utility — correctly not claimed.** The withdrawal of decision-curve claims is appropriate and the requirement for comparative decision curves is correctly stated. No utility claim survives in the text. **Judgement: compliant.**

**Competing risks — not met in the development cohort.** Available in Wales, unexecuted in UK Biobank owing to a software guard, with the failure reported as a result.

**Missing data — not met.** Single median imputation within folds, no uncertainty propagation, ignorability argued only from missingness-indicator associations with outcome, and three different complete-input populations whose selection is uncharacterised.

**Family clustering — not met in UK Biobank.** Welsh family-cluster resampling is properly done. UK Biobank used participant-level resampling, in a carrier cohort that is enriched for relatives by construction, with kinship described as unavailable when it is an extractable standard resource.

**Fairness — not met.** Feasible in UK Biobank, as Gratton et al. demonstrate; not performed; described as unavailable.

**Reproducibility — mixed, and better than typical.** The full equation with baseline survival is published; source files, script names and SHA-256 hashes exist in the package; the provenance ledger is exemplary internal practice. But no code or model availability statement, no repository, and internal file paths used as manuscript citations. The reproducibility apparatus is real and is pointed in the wrong direction — inwards to the project rather than outwards to a reader.

**Citation fidelity — fails.** One incorrect title, one miscitation, 19 of 39 references uncited, and a "Literature verification" paragraph that claims source verification not evidenced by the reference list.

**Journal fit.** The claimed contribution — a routine-data model with moderate discrimination, no external validation, no utility evidence, and a comparator advantage confounded by population and measurement — does not meet the bar for *Circulation*, *European Heart Journal*, *JAMA Cardiology* or *Nature Medicine*. Reframed around the two genuinely novel findings (comparator non-estimability in a national registry; degradation of clinic-derived FH instruments in a population-ascertained frame), with the carrier definition rebuilt from sequence data, it would be competitive at *Atherosclerosis*, the *Journal of Clinical Lipidology* or the *European Journal of Preventive Cardiology*.

---

## E. Top ten revisions, ranked

**Rejection-level.**

1. **Rebuild the cohort from a verifiable variant classification.** Extract LDLR variants from whole-exome sequence data, classify by ACMG or ClinVar, and report carrier frequency and untreated LDL-C against non-carriers alongside the published benchmark of 1 in 288 with significantly higher LDL-C (Gratton et al. 2023). If the flag cannot be rebuilt, retitle and reframe the entire manuscript as a study of an LDLR-variant-enriched population sample and delete every FH-cohort claim.
2. **Attach 95% confidence intervals to every C-statistic**, including both transport estimates, all six internal values, and all comparator values; then state whether the transport asymmetry survives its own interval.
3. **Undo or bound the outcome-conditional Welsh inclusion.** Apply one calendar censoring rule identically to cases and non-cases, obtain the administrative end-of-recording date, and report the transport estimate under both rules.
4. **Quantify or bound specification-search optimism.** Report the number of specifications evaluated across model generations on these data and state that neither internal estimator accounts for it. If feasible, nest specification selection inside the resampling.
5. **Run the UK Biobank competing-risk analysis** and report cumulative incidence at five and ten years with competing-death counts. Remove every statement that an analysis "did not execute".

**Major.**

6. **Report all nine head-to-head cells plus all Lp(a)-omitted cells** in a single table with n, events, both C values with intervals, deltas with intervals, and verdicts. Make ten years the primary horizon or justify its exclusion. State explicitly that CALON-C entered every comparison as an out-of-fold predictor, and state which model was used in each Welsh comparison.
7. **Replace single median imputation with multiple imputation** and re-report the three lipid terms and the concordance decomposition. Until this is done, the Discussion's argument about why lipid terms did not dominate is not supportable.
8. **Fix the Lp(a) unit handling.** Report all comparator deltas under at least three Lp(a) thresholds spanning the plausible molar range, and state that fixed-factor conversion biases these comparisons in CALON-C's favour.

**Moderate.**

9. **Repair the reference list and the internal frame-mixing.** Correct reference 9's title, reattach reference 10, cite or remove the 19 orphan references, and never present two risk sets within one table row.
10. **Convert the document into a manuscript.** Supply the sixteen placeholders including ethics approval; remove all internal file names, reviewer-response provenance, model-generation labels and self-addressed instructions; move source traceability to a data-availability statement; delete process items from the Strengths paragraph and add the four genuine strengths, including the out-of-fold design the paper currently fails to claim.

**Cosmetic.** Reduce C-statistics to three decimals and p values to two significant figures; replace "win"/"tie" with "higher discrimination"/"no difference"; restructure the eleven-item limitations paragraph as a short ordered list.

---

## F. Inter-panel tension memo

Each seat's prediction of where it will most strongly disagree with the others.

**Biostatistician.** My sharpest disagreement will be with the **Cardiologist** over the Welsh predictor timing. CA will argue that chronic hypertension and diabetes almost certainly predated the events and that investigator attestation plus clinical plausibility make the Welsh analysis usable. I will not concede. Fifty-five of ninety-two events had blood pressure recorded after the event, medication had no date at all, and the same fields scored the comparators. Clinical plausibility is not a measurement. I expect CA to call this statistical purity that discards real information; I will call it the difference between an estimate and a belief. I also expect to disagree with **LM** on whether the null lipid finding is interpretable at all — LM will say it is contaminated beyond use, whereas I hold that it can be recovered with proper imputation.

**Cardiologist.** My sharpest disagreement will be with the **Biostatistician** over what threshold of data quality warrants abandoning an analysis. BS treats the Welsh frame as unusable; I treat it as imperfect but informative, because in real clinical registries hypertension and diabetes are chronic states rather than dated events, and a standard that rejects all such data rejects all registry research. I will also press both other seats on a point neither has foregrounded: the safety consequence. A model predicting 6.20% ten-year risk in a cohort labelled FH is not merely mis-calibrated, it is potentially harmful, because it could license deferring treatment in a population for whom diagnosis alone mandates intensive management. I expect BS to regard this as outside the statistical remit and LM to agree with me.

**Lipid-medicine specialist.** My sharpest disagreement will be with **both** other specialist seats over whether this cohort is an FH cohort at all, and therefore whether the comparator analysis is worth repairing. BS and CA will both want to fix the analysis — intervals, imputation, competing risks, censoring rules. I contend that every one of those repairs is premature, because a carrier frequency of 1 in 142 with an untreated LDL-C excess of +0.15 to +0.23 mmol/L means the exposure that defines eligibility is misclassified, and no downstream statistical repair addresses a mis-defined population. I expect to be told that this is defeatist. I will also dissent, alone, from any move to delete the grey-zone analysis: the null Lp(a) result is the most diagnostically valuable number in the manuscript precisely because it is discordant with everything known about Lp(a) in FH.

**Senior Editor-in-Chief.** My sharpest disagreement will be with all three specialists over what the paper *is*. Each seat wants to repair the paper as written — a comparator-superiority study. I judge that the comparator tally is not the paper and cannot be made into one, because its central positive finding is confounded by population and by Lp(a) measurement in ways no revision within this frame can resolve. The publishable paper is the one the authors have already written without recognising it: clinic-derived FH risk instruments degrade badly, and two of three become non-computable, when moved from specialist registries into population-ascertained data and a national clinical registry. That is a genuine, well-evidenced, and useful negative result. I expect resistance, because it means the index model becomes a supporting character in its own manuscript.

---

## Internal panel debate

**ED:** We have three fatal or near-fatal findings and they are not independent in their consequences. Let us establish precedence. LM, you claim the population issue dominates everything.

**LM:** It does, and the argument does not depend on genetics. Table 1 reports untreated-equivalent LDL-C with an interquartile range of 3.32 to 4.68 mmol/L. Untreated heterozygous LDLR carriers do not have that distribution. The manuscript's own text reports a carrier-versus-non-carrier excess of 0.15 to 0.23 mmol/L. Gratton and colleagues found significantly higher LDL-C in carriers in every ancestry group in this same cohort, at a prevalence half as common. Two independent lines converge: the flag is not selecting monogenic FH.

**BS:** I accept the finding and I want to state its statistical form precisely, because the manuscript treats it as an applicability limitation. It is not. Eligibility is defined by the misclassified variable, so this is not bias in an estimate of a well-defined quantity — it is that the quantity being estimated is not the one named. Correcting the standard errors, the imputation, the censoring rule, all of it, leaves the target population wrong.

**CA:** I agree on the science and I want to add the consequence, because it is the one an editor will feel. If this cohort is not FH, the model's predicted ten-year risk of 6.20% is being offered as an FH risk. A clinician who applied that number would under-treat. The paper's own Discussion says a score "must never be used to de-risk a carrier", and then reports absolute risks that would do exactly that.

**BS:** Which is why I resist the framing that the calibration section is a reporting problem. An expected-to-observed ratio of 1.008 in the development data is nearly tautological, and it is the number promoted to the abstract, while the scaled Brier score of 3.3% — which says the model explains very little — is reported without a word of interpretation. The paper's own numbers rank its findings correctly; its prose does not.

**ED:** CA, you and BS have a real disagreement on Wales. Let us have it.

**CA:** In a national FH registry, hypertension and diabetes are chronic states. They are recorded when someone happens to write them down. Demanding a dated diagnosis preceding baseline for every predictor would end registry research. The investigators attest that these conditions predated the events; that is clinically almost certainly true.

**BS:** It is probably true and it is not evidence. But that is not the part I will not concede. The part I will not concede is the inclusion rule. Participants without operational follow-up were kept if and only if they had a dated event. That is not imperfect measurement of a predictor; that is conditioning cohort membership on the outcome. The event rate moved from 7.9% to 8.7% by construction, and the manuscript calls it a correction that "rescued" events.

**CA:** …That I cannot defend. Retaining a documented event feels like honesty, but if the same rule does not retain the corresponding non-cases, it is not honesty, it is asymmetry.

**BS:** And it sits underneath the transport estimate, which is the paper's structural claim, and which is reported without an interval at all. With 102 Welsh events, 0.7252 against 0.6600 may be indistinguishable. The code computes a point estimate and stops. Two hundred lines of bootstrap machinery already exist in that repository.

**LM:** Then I will press my disagreement with both of you. You are itemising repairs — intervals, imputation, censoring, competing risks. Every one is correct and every one is premature. Repairing the inference on a mis-defined population produces a precisely quantified answer to the wrong question.

**BS:** That is where I part from you. The repairs are not premature, they are conditional. If the cohort is rebuilt and turns out to contain, say, twelve hundred genuine pathogenic carriers, the same analytical defects will still be there, and they will still need fixing. Sequencing the work does not mean skipping it.

**CA:** And some repairs are worth doing regardless, because they change what we know rather than how precisely we know it. The competing-risk analysis is one line of code guarding on a column the programme's own inventory says exists. Thirty-five competing deaths against 102 events in Wales tells you the effect is material.

**ED:** Let me record a correction that runs the other way, because it matters for fairness. I formed the view while reading that the head-to-head comparisons were index-model-in-sample against comparator-out-of-sample, which would have been fatal. BS, you checked.

**BS:** I did, and it is not. The linear predictor entering the paired bootstrap is the out-of-fold predictor from repeated cross-validation. The comparisons are properly out of sample with respect to coefficient estimation. That is the correct design and it is the best-executed thing in the paper. It also cannot be learned from the manuscript. I had to read `code/33_CALON_C.py`. A paper that leaves its strongest methodological feature to be discovered in source code, while listing "explicit withdrawal of unsupported decision-curve claims" among its strengths, has inverted its own priorities.

**LM:** The same inversion runs through the comparator work. Reproducing both SAFEHEART worked examples before scoring anything is exactly right. Refusing to assign missing inputs to favourable categories is exactly right. And then the Lp(a) conversion divides nanomoles by 2.15 to reach milligrams, which the EAS consensus states cannot be done with a fixed factor, and the manuscript flags the divisor as unprinted in the source papers and proceeds anyway. That error degrades only the two Lp(a)-dependent comparators. It never touches CALON-C.

**CA:** Which brings us to the number I simply do not believe. SAFEHEART-RE at 0.6308. The same equation reaches 0.802 in genotype-confirmed primary prevention in the Australian cohort published this year — and primary prevention is precisely where the previous-ASCVD term is inert, so the manuscript's own explanation is unavailable.

**BS:** That is the distinction I want on the record. The manuscript reasons carefully about *why* SAFEHEART-RE should perform less well here. It never asks whether it should perform *this much* less well. Explaining a result and auditing a result are different activities, and a comparator value that is the lowest ever published warrants the second.

**ED:** Then here is my adjudication. The population finding is fatal and takes precedence, and the fact that CA and LM reach it from Table 1 alone, without genetics, makes it unanswerable. The outcome-conditional Welsh inclusion is separately fatal for the transport claim, and CA has conceded that point. BS's absent intervals and unquantified specification-search optimism are major and remediable. CA's safety framing of the calibration finding is adopted and is currently absent from the manuscript.

On LM's dissent about sequencing: overruled in part. The rebuild comes first, but the analytical repairs are conditional, not premature. On LM's dissent about the grey-zone analysis: upheld against BS and CA. Keep it, delete its justification, and reinterpret it as evidence about the data rather than about biomarkers.

And I record my own disagreement with all three of you. Each of you has reviewed the paper as a comparator-superiority study and produced a repair list. I do not think that paper is recoverable, because its positive finding is confounded in ways no revision within this frame resolves. The recoverable paper is already inside this manuscript: clinic-derived FH instruments degrade sharply, and two of three become non-computable, when moved into population-ascertained data and a national registry. Forty participants and one event for SAFEHEART-RE in an entire national genotype-positive registry is a striking, publishable, useful negative result, and it is currently a subsection of the Results. That is the paper. The index model becomes a supporting character in it.

---

## Teaching section for Dr Genedy

Each lesson is stated as the general principle, then the specific instance, then what to do differently next time.

**1. Misclassification of the variable that defines eligibility is not bias — it is a change of subject.**
When measurement error affects a predictor, you get a biased estimate of a well-defined quantity. When it affects the *eligibility criterion*, you get an unbiased estimate of a quantity nobody asked about. Your `ldlr_carrier` flag defines who is in the study, so its validity is prior to every other question. The diagnostic is cheap and you can run it this week: carrier frequency against published prevalence, and carrier-versus-non-carrier LDL-C against published effect sizes. Both flagged the problem immediately, and both numbers were already in your manuscript. **Habit to build:** for every study, identify the one variable that defines the population, and benchmark it against external published data before fitting anything.

**2. Cross-validation corrects coefficient optimism, not specification optimism.**
This is the most commonly misunderstood point in prediction modelling and your manuscript is on the right side of it in code and the wrong side in prose. Your out-of-fold estimate is honest about the coefficients: each fold's model never sees its test data. But the *choice* of nine terms, the knot at fifty, the ridge penalty of 0.02, the divisors of 0.70 and 0.80 — those were selected using all the data, across CALON-N, F, H, H2, 11 and C. No amount of resampling inside a fixed specification detects that. **Habit to build:** keep a specification log with a count of distinct specifications evaluated, report the count, and where feasible nest the selection step inside the resampling loop so the optimism is measured rather than assumed absent.

**3. Never let inclusion depend on the outcome.**
The Welsh rescue of ten events is the most instructive error in the package because it was well intentioned. You had participants with a documented, dated event and no operational follow-up record, and discarding real events felt like throwing away truth. But you kept them *because* they had events, while the corresponding people without follow-up and without events stayed excluded. Your cases and non-cases were then ascertained by different rules, and the event rate rose from 7.9% to 8.7% by construction. **Habit to build:** write the inclusion rule as a function of baseline information only, and test it by asking whether you could apply it on the day of baseline, knowing nothing about what happened next. If the answer is no, the rule is contaminated.

**4. A point estimate without an interval is not a finding.**
Your transport asymmetry — 0.7252 against 0.6600 — carries the paper's structural argument, and neither number has an interval. With 102 Welsh events they may be indistinguishable, in which case there is no asymmetry to explain, and three paragraphs of the Discussion explain something that may not exist. The same applies to all six internal C values and every comparator C. **Habit to build:** treat an interval as part of the number, not as an optional adornment. If your code returns a bare estimate, that is a bug report.

**5. When a comparator performs like an outlier, audit before you bank the win.**
SAFEHEART-RE returned 0.6308 in your data, against 0.85 in derivation, 0.81 in its own primary-prevention subset, roughly 0.77 in France, roughly 0.67 in English routine care, and 0.802 in genotype-confirmed Australian primary prevention. You are the lowest by a wide margin. Your Discussion explains why it *should* be lower and never asks whether it should be *this* much lower. **Habit to build:** before reporting any comparative advantage, plot your comparator's value against every published value for that instrument. If you are an outlier, the burden shifts to you, and the most likely explanation is your data, not the instrument.

**6. Differential measurement error is the subtlest way to win an unfair contest.**
Your Lp(a) conversion divides nanomoles per litre by 2.15. The EAS consensus statement explains why that cannot be done with a fixed factor: the mass-to-molar relationship depends on apolipoprotein(a) isoform size. The consequence is that your conversion adds noise to SAFEHEART-RE and FH-Risk-Score, both of which use Lp(a), and adds none to CALON-C, which does not. You spotted the hazard — the manuscript says the divisor is not printed in the comparator papers — and proceeded anyway. **Habit to build:** for every comparison, list the measurement errors and ask which arm each one touches. Any error touching only the comparator is a thumb on the scale, and must be quantified in a sensitivity analysis, not merely disclosed.

**7. A constructed variable is not the construct you named it after.**
`cum_nonhdl = log(non-HDL-C × age)` equals log(non-HDL-C) + log(age). It is an age term with a lipid offset, entered beside age and an age spline, and it cannot represent lifetime cumulative exposure because it multiplies a *currently measured, divisor-corrected* concentration by *total years lived*, ignoring years on treatment. Your treatment reconstruction correlated 0.32 with observed pre-treatment LDL-C. **Habit to build:** write out the algebra of every derived variable and ask what it would equal for two people who differ in only one input. Then name it for what the algebra says, not for what you hoped to capture.

**8. Do not build a substantive argument on an estimate your methods attenuate.**
Your finding that lipid terms contribute little is genuinely interesting and may be true. But those terms were median-imputed for 12.4% of participants, treatment-corrected by a fixed divisor with reconstruction correlation 0.32, and — as it turns out — measured in a population whose LDL-C range was never restricted, because the carrier flag did not select monogenic FH. Single median imputation biases associations towards the null, which is the direction of your finding. **Habit to build:** before interpreting a null, list every analytical choice that could have produced it, and fix the ones that are fixable. Multiple imputation here, then interpret.

**9. Choose the horizon before you see the results, and report every horizon you analysed.**
Your confirmatory family was full follow-up and five years, and ten years was declared exploratory with no numbers reported at all — although ten years is FH-Risk-Score's native horizon, the horizon of every guideline threshold, and the horizon a clinician thinks in. I checked your artefact: the ten-year cells do not reverse anything, so you concealed nothing. But a reader cannot verify that, and "full follow-up" is a censoring-determined quantity with no clinical meaning. **Habit to build:** pre-specify one primary horizon on clinical grounds, report every horizon analysed with equal completeness, and never let the primary horizon be one determined by your data's administrative end.

**10. State your strongest methodological feature; do not list your corrections as strengths.**
Your Strengths paragraph includes "explicit withdrawal of unsupported decision-curve claims" and notes that corrections moved in both directions. Withdrawing an unsupported claim is fixing an error; disclosing it is integrity, not design. Meanwhile the genuinely strong feature — that every comparator comparison used out-of-fold CALON-C predictions, so the contest was fair — appears nowhere, and I had to read your source code to establish it. **Habit to build:** a Strengths paragraph lists design choices that make the inference more credible than the alternatives. Process integrity belongs in a changelog. And if a reviewer must read your code to find your best decision, your Methods has failed.

**11. Separate the document that manages your project from the document you submit.**
Your provenance ledger, source-precedence hierarchy, conflict table and SHA-256 manifest are better project hygiene than most groups achieve, and you should keep all of it. But `RESULTS_FINAL_CORRECTED.md`, "the later reviewer response judged", the CALON-N/F/H/H2/11 lineage, table footnotes citing JSON files, and the sentence "This priority claim should be rechecked immediately before submission" are internal artefacts. One fact from that layer must survive into the manuscript — that several model generations preceded this one, because it bears on optimism. Everything else moves to a data-availability statement. **Habit to build:** before submission, read the manuscript as a stranger with no access to your file system, and delete every sentence that only makes sense to someone who has.

**12. When your positive finding is confounded, look for the negative finding that is not.**
This is the most valuable lesson available from this package. Your comparator advantage is confounded by population and by Lp(a) measurement. But your observation that SAFEHEART-RE could be computed for forty participants with one event in an entire national genotype-positive registry, and FH-Risk-Score for one hundred and thirty-two with six, is clean, quantitative, unconfounded, and genuinely useful to anyone trying to implement FH risk stratification. It currently sits in a subsection called "Missing data and comparator evaluability". **Habit to build:** when a paper's headline claim weakens under scrutiny, do not defend it harder. Reread your own Results for the finding that survives, and consider whether it is the better paper.

---

## Research-tool status table

| Tool | Status | Detail |
|---|---|---|
| **Scite AI** | **NOT EXPOSED/NOT CONFIGURED** | Tool discovery returned one MCP server only (`plugin-google-drive-google-drive`, status `ready`). No Scite tool was callable. No citation-context, supporting or disputing counts were obtained, and none are reported. |
| **SciSpace** | **NOT EXPOSED/NOT CONFIGURED** | Not present in the MCP catalogue. No paper tables or enriched columns retrieved. |
| **Elicit** | **NOT EXPOSED/NOT CONFIGURED** | Not present in the MCP catalogue. No systematic search or trial search performed. |
| **Consensus** | **NOT EXPOSED/NOT CONFIGURED** | Not present in the MCP catalogue. |
| **`/academic` skills** | **AVAILABLE — used as guidance, not as a data source** | `~/.codex/skills/ai-literature-connectors/SKILL.md` was read and its Step 0 routing protocol followed: connector availability was verified before routing, and the documented Crossref/PubMed fallback path was used. Its bundled `scripts/pubmed_search.py` and `scripts/validate_dois.py` were not executed; equivalent E-utilities and Crossref queries were issued directly. |
| **Crossref REST API** | **USED — results returned** | All 39 manuscript DOIs queried individually and all 39 resolved with title, journal, date, volume and pages. Established that reference 9's title does not match its record, that reference 1 is a genuine record whose page range is not in the Crossref metadata, and that references 2 and 10 match exactly. Also verified 12 additional DOIs used in this review. One DOI I attempted for UK Biobank cohort documentation (`10.1038/s41586-018-0579-1`) returned no record on two attempts and is marked **UNVERIFIED — DO NOT CITE**; it is not cited anywhere in this review. |
| **PubMed E-utilities (NCBI)** | **USED — results returned** | `esearch` and `efetch` returned full abstracts for the three comparator papers (PMIDs 28391914, 34433300, 28275165) and the 2026 Australian validation (PMID 42229222), plus `esummary` records for a targeted search on UK Biobank FH-variant carriers that surfaced PMID 37409534. These abstracts are the primary evidence for the Montreal cross-sectional design, the SAFEHEART derivation C values, the FH-Risk-Score derivation description, the Australian C-statistics, and the UK Biobank prevalence benchmark. An initial batch failed with `Supplied+id+parameter+is+empty` owing to unencoded DOI query strings; re-issued with URL encoding and succeeded. |
| **Native web search** | **AVAILABLE BUT FAILED** | Two queries issued (FH-Risk-Score derivation cohort composition; UK Biobank LDLR carrier LDL-C differences). Both returned `Web search rejected: User Rejected`. Consequently the 499-UK-Biobank-participant claim could not be checked against publisher pages or supplementary material and is marked **UNVERIFIED**. |
| **Google Drive MCP** | **AVAILABLE — not used** | The only exposed MCP server. Not relevant to this review; no calls made. |
| **Local aggregate artefacts** | **USED — results returned** | `CALON_C_CONFLICT_AND_PROVENANCE_LEDGER.md`, `calon_c_corrected_headtohead.csv`, `METHODS_CALON_C.md`, `code/33_CALON_C.py`. These established that the head-to-head used out-of-fold predictions, that Welsh comparisons used a Wales-refitted model, that transport C has no interval computed, that ten-year and Lp(a)-omitted cells exist but are unreported, and that the manuscript's reported deltas are numerically faithful to source. No participant-level data were opened. |

Search snippets were treated as discovery aids only. No paper is cited in this review unless its Crossref record, PubMed record, or both were retrieved in this session.

---

## Eligible evidence ledger (17 August 2016 – 17 August 2026)

All entries verified in this session against Crossref, PubMed, or both.

| # | Citation | Population / design | Relevant finding | Role | Identifier |
|---|---|---|---|---|---|
| E1 | Tamehri Zadeh SS, Chan DC, Pang J, Mata P, Watts GF. European and Canadian derived risk prediction equations for atherosclerotic cardiovascular disease are valid in Australian patients with genetically confirmed familial hypercholesterolaemia. *Atherosclerosis*. 2026;418:120799. | 655 genotype-confirmed HeFH; 53 incident ASCVD events; median 6 y | SAFEHEART-RE C 0.767 (0.706–0.827); primary prevention 0.802 (0.711–0.888); FH-Risk-Score 0.735 (0.667–0.801); Combined-FH-Score 0.698 (0.627–0.766) | Challenges the SAFEHEART-RE value and the novelty claim | [10.1016/j.atherosclerosis.2026.120799](https://doi.org/10.1016/j.atherosclerosis.2026.120799) · PMID 42229222 |
| E2 | Gratton J, Humphries SE, Futema M. Prevalence of FH-causing variants and impact on LDL-C concentration in European, South Asian, and African ancestry groups of the UK Biobank. *Arterioscler Thromb Vasc Biol*. 2023;43:1737–1742. | 140,439 European, 4,067 South Asian, 3,906 African UK Biobank participants with lipids and WES | P/LP FH-variant prevalence 1 in 288 (95% CI 1/316–1/264) in Europeans; carriers had significantly higher LDL-C in every ancestry group | Challenges the carrier definition; demonstrates feasibility of ancestry-stratified analysis | [10.1161/ATVBAHA.123.319438](https://doi.org/10.1161/ATVBAHA.123.319438) · PMID 37409534 |
| E3 | Pérez de Isla L, Alonso R, Mata N, et al. Predicting cardiovascular events in familial hypercholesterolemia: the SAFEHEART Registry. *Circulation*. 2017;135:2133–2144. | 2,404 molecularly defined FH; mean 5.5 y; 12 fatal and 122 non-fatal ASCVD | C 0.85 derivation; 0.81 without established ASCVD; bootstrap optimism 0.003 over 100 resamples | Comparator primary source; challenges the 0.6308 value | [10.1161/CIRCULATIONAHA.116.024541](https://doi.org/10.1161/CIRCULATIONAHA.116.024541) · PMID 28275165 |
| E4 | Paquette M, Bernard S, Cariou B, et al. Familial Hypercholesterolemia-Risk-Score. *Arterioscler Thromb Vasc Biol*. 2021;41:2632–2640. | 3,881 adult HeFH without prior ASCVD; 5 registries in Europe and North America; 32,361 person-years | 7 variables; C 0.75 for 10-y ASCVD, superior to SAFEHEART-RE 0.69 | Comparator primary source; abstract does **not** mention UK Biobank | [10.1161/ATVBAHA.121.316106](https://doi.org/10.1161/ATVBAHA.121.316106) · PMID 34433300 |
| E5 | Paquette M, Dufour R, Baass A. The Montreal-FH-SCORE. *J Clin Lipidol*. 2017;11:80–86. | **Cross-sectional** cohort; 670 LDLR-mutation carriers (638 analysed) | AUC 0.840 (0.808–0.872) for prevalent CVD; age, HDL-C, sex, hypertension, smoking | Confirms the manuscript's estimand caveat; challenges its "higher discrimination" framing | [10.1016/j.jacl.2016.10.004](https://doi.org/10.1016/j.jacl.2016.10.004) · PMID 28391914 |
| E6 | Paquette M, Brisson D, Dufour R, et al. Validation and refinement of the Montreal-FH-SCORE. *J Clin Lipidol*. 2017;11:1161–1167. | FH validation cohort | Refinement of E5 | Comparator context | [10.1016/j.jacl.2017.07.008](https://doi.org/10.1016/j.jacl.2017.07.008) |
| E7 | Kronenberg F, Mora S, Stroes ESG, et al. Lipoprotein(a) in atherosclerotic cardiovascular disease and aortic stenosis: a EAS consensus statement. *Eur Heart J*. 2022;43:3925–3946. | Consensus statement | Molar and mass Lp(a) units are not interconvertible by a fixed factor; Lp(a) is causal and independently predictive | Challenges the ÷2.15 conversion and the null Lp(a) interpretation | [10.1093/eurheartj/ehac361](https://doi.org/10.1093/eurheartj/ehac361) |
| E8 | Blanche P, Kattan MW, Gerds TA. The c-index is not proper for the evaluation of *t*-year predicted risks. *Biostatistics*. 2019;20:347–357. | Methodological | Harrell's C is improper for *t*-year risk evaluation | Challenges "full follow-up" C as primary | [10.1093/biostatistics/kxy006](https://doi.org/10.1093/biostatistics/kxy006) |
| E9 | Van Calster B, McLernon DJ, van Smeden M, et al. Calibration: the Achilles heel of predictive analytics. *BMC Med*. 2019;17:230. | Methodological | Hierarchy of calibration; aggregate expected:observed is weakest | Challenges the calibration reporting | [10.1186/s12916-019-1466-7](https://doi.org/10.1186/s12916-019-1466-7) |
| E10 | Vickers AJ, van Calster B, Steyerberg EW. A simple, step-by-step guide to interpreting decision curve analysis. *Diagn Progn Res*. 2019;3:18. | Methodological | Requirements for net-benefit evidence | Supports the withdrawal of utility claims | [10.1186/s41512-019-0064-7](https://doi.org/10.1186/s41512-019-0064-7) |
| E11 | Austin PC, Fine JP. Practical recommendations for reporting Fine–Gray model analyses for competing risk data. *Stat Med*. 2017;36:4391–4400. | Methodological | Competing-risk reporting standards | Challenges the unexecuted UK Biobank arm | [10.1002/sim.7501](https://doi.org/10.1002/sim.7501) |
| E12 | Nijman SWJ, Leeuwenberg AM, Beekers I, et al. Missing data is poorly handled and reported in prediction model studies using machine learning. *J Clin Epidemiol*. 2022;142:218–229. | Literature review | Documents inadequate single-imputation practice | Challenges fold-wise median imputation | [10.1016/j.jclinepi.2021.11.023](https://doi.org/10.1016/j.jclinepi.2021.11.023) |
| E13 | Munafò MR, Tilling K, Taylor AE, Evans DM, Davey Smith G. Collider scope: when selection bias can substantially influence observed associations. *Int J Epidemiol*. 2018;47:226–235. | Methodological | Selection conditioned on outcome-related variables distorts associations | Challenges the Welsh outcome-conditional inclusion | [10.1093/ije/dyx206](https://doi.org/10.1093/ije/dyx206) |
| E14 | Riley RD, Snell KIE, Ensor J, et al. Minimum sample size for developing a multivariable prediction model: PART II. *Stat Med*. 2019;38:1276–1296. | Methodological | Sample-size requirements for time-to-event models | Bears on 97 five-year events with nine parameters | [10.1002/sim.7992](https://doi.org/10.1002/sim.7992) |
| E15 | Riley RD, Archer L, Snell KIE, et al. Evaluation of clinical prediction models (part 2): how to undertake an external validation study. *BMJ*. 2024;384:e074820. | Methodological | External validation design requirements | Supports the manuscript's refusal of an external-validation claim | [10.1136/bmj-2023-074820](https://doi.org/10.1136/bmj-2023-074820) |
| E16 | Riley RD, Snell KIE, Archer L, et al. Evaluation of clinical prediction models (part 3): sample size for external validation. *BMJ*. 2024;384:e074821. | Methodological | Event requirements for validation | Bears on 102 Welsh events | [10.1136/bmj-2023-074821](https://doi.org/10.1136/bmj-2023-074821) |
| E17 | Collins GS, Moons KGM, Dhiman P, et al. TRIPOD+AI statement. *BMJ*. 2024;385:e078378. | Reporting standard | Requires uncertainty for all performance measures | Reporting audit basis | [10.1136/bmj-2023-078378](https://doi.org/10.1136/bmj-2023-078378) |
| E18 | Wolff RF, Moons KGM, Riley RD, et al. PROBAST. *Ann Intern Med*. 2019;170:51–58. | Risk-of-bias tool | Four bias domains plus applicability | Risk-of-bias audit basis | [10.7326/M18-1376](https://doi.org/10.7326/M18-1376) |
| E19 | Austin PC, Steyerberg EW. The Integrated Calibration Index (ICI). *Stat Med*. 2019;38:4051–4065. | Methodological | Calibration metrics with intervals | Recommended addition | [10.1002/sim.8281](https://doi.org/10.1002/sim.8281) |
| E20 | Hu P, Dharmayat KI, Stevens CAT, et al. Prevalence of familial hypercholesterolemia among the general population and patients with ASCVD. *Circulation*. 2020;141:1742–1759. | Systematic review and meta-analysis | General-population FH prevalence approximately 1 in 311 | Corroborates E2 against the 1 in 142 carrier frequency | [10.1161/CIRCULATIONAHA.119.044795](https://doi.org/10.1161/CIRCULATIONAHA.119.044795) |
| E21 | McKay AJ, Gunn LH, Ray KK. External validity of the SAFEHEART risk prediction model in an English routine care cohort. *Atherosclerosis*. 2022;358:68–74. | English routine care FH | Discrimination and calibration on transport | Supports the transport-degradation argument; the specific C of 0.67 was **not** verified from the abstract | [10.1016/j.atherosclerosis.2022.07.011](https://doi.org/10.1016/j.atherosclerosis.2022.07.011) |
| E22 | Gallo A, Charrière S, Vimont A, et al. SAFEHEART risk-equation and cholesterol-year-score in French FH patients. *Atherosclerosis*. 2020;306:41–49. | REFERCHOL | External evaluation of SAFEHEART-RE and a cholesterol-year score | Supports the transport-degradation argument; the specific 0.77–0.78 values were **not** verified from the abstract | [10.1016/j.atherosclerosis.2020.06.011](https://doi.org/10.1016/j.atherosclerosis.2020.06.011) |
| E23 | 2026 ACC/AHA/AACVPR/ABC/ACPM/ADA/AGS/APhA/ASPC/NLA/PCNA Guideline on the Management of Dyslipidemia. *Circulation*. 2026;153(17). | Guideline | Position on FH-specific scores and on general-population equations in HeFH | Supports the framing; **page range e1154–e1276 not in the Crossref record — verify** | [10.1161/CIR.0000000000001423](https://doi.org/10.1161/CIR.0000000000001423) |
| E24 | Mach F, Koskinas KC, Roeters van Lennep JE, et al. 2025 focused update of the 2019 ESC/EAS Guidelines for the management of dyslipidaemias. *Eur Heart J*. 2025;46:4359–4378. | Guideline | Cumulative-exposure reduction and FH risk pathways | Supports the framing; verifies exactly as cited | [10.1093/eurheartj/ehaf190](https://doi.org/10.1093/eurheartj/ehaf190) |
| E25 | Zamora A, Masana L, Civeira F, et al. Prognostic stratification of familial hypercholesterolaemia patients using AI algorithms. *Eur Heart J Digit Health*. 2025;6:1113–1123. | FH cohort, machine learning | Many-variable FH prognostic modelling | Supports the parsimony contrast | [10.1093/ehjdh/ztaf092](https://doi.org/10.1093/ehjdh/ztaf092) |
| E26 | Gallo A, Pérez de Isla L, Charrière S, et al. The added value of coronary calcium score in FH. *JACC Cardiovasc Imaging*. 2021;14:2414–2424. | FH imaging cohort | Coronary calcium adds to SAFEHEART discrimination | Supports the enhancer discussion | [10.1016/j.jcmg.2021.06.011](https://doi.org/10.1016/j.jcmg.2021.06.011) |
| E27 | Ginsberg HN, Packard CJ, Chapman MJ, et al. Triglyceride-rich lipoproteins and their remnants. *Eur Heart J*. 2021;42:4791–4806. | Consensus review | Remnant biology and measurement | Bears on the remnant-cholesterol clipping to −1 mmol/L | [10.1093/eurheartj/ehab551](https://doi.org/10.1093/eurheartj/ehab551) |
| E28 | Vallejo-Vaz AJ, De Marco M, Stevens CAT, et al. Overview of FH care in over 60 countries. *Atherosclerosis*. 2018;277:234–255. | EAS FH Studies Collaboration | Global gaps in FH detection and care | Supports the scalability argument; manuscript reference 17, **currently uncited in text** | [10.1016/j.atherosclerosis.2018.08.051](https://doi.org/10.1016/j.atherosclerosis.2018.08.051) |
| E29 | Ference BA, Ginsberg HN, Graham I, et al. Low-density lipoproteins cause atherosclerotic cardiovascular disease. *Eur Heart J*. 2017;38:2459–2472. | EAS consensus | LDL causality | Correct anchor for the causal-versus-predictive argument; manuscript reference 23, **currently uncited in text** | [10.1093/eurheartj/ehx144](https://doi.org/10.1093/eurheartj/ehx144) |
| E30 | Fry A, Littlejohns TJ, Sudlow C, et al. Comparison of sociodemographic and health-related characteristics of UK Biobank participants with the general population. *Am J Epidemiol*. 2017;186:1026–1034. | UK Biobank | Healthy-volunteer selection | Supports the representativeness discussion | [10.1093/aje/kwx246](https://doi.org/10.1093/aje/kwx246) |
| E31 | van Alten S, Domingue BW, Faul J, Galama T, Marees AT. Reweighting UK Biobank corrects for pervasive selection bias due to volunteering. *Int J Epidemiol*. 2024;53:dyae054. | UK Biobank | Volunteer selection alters associations | Supports the representativeness discussion | [10.1093/ije/dyae054](https://doi.org/10.1093/ije/dyae054) |
| E32 | Schoeler T, Speed D, Porcu E, et al. Participation bias in the UK Biobank distorts genetic associations and downstream analyses. *Nat Hum Behav*. 2023;7:1216–1227. | UK Biobank | Participation bias distorts genetic associations | Particularly relevant to a genetically defined cohort | [10.1038/s41562-023-01579-9](https://doi.org/10.1038/s41562-023-01579-9) |
| E33 | Tamehri Zadeh SS, Chan DC, Pang J, Watts GF. Canadian and French risk scores are valid in identifying cardiovascular disease in Australian patients with FH. *Can J Cardiol*. 2025;41:2244–2251. | 
Australian FH | Validation of Montreal and FH-Risk-Score | Comparator context; **miscited in the manuscript** at reference 10 | [10.1016/j.cjca.2025.07.042](https://doi.org/10.1016/j.cjca.2025.07.042) |
| E34 | Domanski MJ, Tian X, Wu CO, et al. Time course of LDL cholesterol exposure and cardiovascular disease event risk. *J Am Coll Cardiol*. 2020;76:1507–1516. | Pooled cohorts | Cumulative LDL exposure predicts events | Correct anchor for the cumulative-exposure construct; manuscript reference 22, **currently uncited in text** | [10.1016/j.jacc.2020.07.059](https://doi.org/10.1016/j.jacc.2020.07.059) |

**Unverified / do not cite.** (i) The claim that FH-Risk-Score derivation included **499 UK Biobank participants** — attributed to E4, absent from its abstract, and not checkable because web search was unavailable. (ii) `10.1038/s41586-018-0579-1` — no Crossref record returned on two attempts; not cited in this review. (iii) The specific external C values of 0.77–0.78 (E22) and 0.67 (E21) as quoted in the manuscript — the articles are verified, the specific figures are not.

**Excluded historical context (published before 17 August 2016; not used as evidence for any claim in this review).** Tybjærg-Hansen et al., *ATVB* 2005;25:211–215 (manuscript reference 15, cited in the Introduction for the clinic-versus-population phenotype gradient — should be replaced by E2, which makes the same point within the window and in this very cohort). Khera et al., *JACC* 2016;67:2578–2589 (print June 2016, reference 13). Karlson et al., *Eur J Prev Cardiol* 2016;23:744–747 (print May 2016, reference 31 — the natural source for intensity-specific treatment correction, and unusable within this window; an in-window equivalent must be found). Sudlow et al., *PLoS Med* 2015 (reference 18). Debray et al., *J Clin Epidemiol* 2015;68:279–289 (reference 29). Benchimol et al., RECORD, *PLoS Med* 2015 (reference 39 — used here only as a reporting instrument, not as evidence). Law et al., *BMJ* 2003 (reference 30). Jansen et al., *J Intern Med* 2004 (reference 32). Cohen et al., *NEJM* 2006 (reference 33). Note that references 15, 18 and 39 are cited in the manuscript's text and support manuscript claims; the manuscript is not bound by this review's window, but the reviewer's evidence is, and in-window substitutes exist for each.

---

## Claims that must be deleted unless new evidence is produced

Each claim is quoted or closely paraphrased from the manuscript, with the evidence that would be required to retain it.

**Population and framing.**

1. **"LDLR-variant carriers" as an unqualified population descriptor** — in the title, short title, keywords, Key points, abstract, and throughout. *Requires:* variant-level classification from sequence data, plus a reported carrier frequency and carrier-versus-non-carrier LDL-C distribution consistent with published pathogenic-variant data (E2, E20). *Otherwise:* replace with "participants carrying an unvalidated LDLR-variant flag" and remove all FH-cohort framing.
2. **Framing the study as an evaluation of "established familial-hypercholesterolaemia risk instruments" in an FH population.** *Requires:* the same rebuild. *Otherwise:* reframe as evaluation of FH instruments transported into a population-ascertained frame.
3. **"Pathogenic variants affecting LDL-receptor biology elevate LDL-C from early life"** as a description of *this cohort* (Introduction ¶1, read against the Methods). *Requires:* variant confirmation. *Otherwise:* restrict the sentence to general FH biology and state explicitly that it does not describe the study population.

**Comparative claims.**

4. **"Discrimination was higher than SAFEHEART-RE"** as a property of the models (Key points, abstract, Discussion, Conclusion). *Requires:* the population rebuild; demonstration that Lp(a) is informative in the cohort or that the comparison is robust across Lp(a) thresholds spanning the plausible molar range; and an explanation of why the observed C of 0.6308 is 0.14–0.17 below the contemporaneous genotype-confirmed primary-prevention estimate (E1). *Otherwise:* report as "SAFEHEART-RE discriminated less well in this frame than in any published cohort, for reasons we cannot resolve".
5. **"Exceeded the Montreal-FH-SCORE"** as a discrimination comparison. *Requires:* nothing that can be produced — Montreal-FH-SCORE was derived cross-sectionally against prevalent disease (E5), so this is a cross-estimand comparison by construction. *Delete* and replace with a statement that a prevalent-disease instrument was used only as a ranking benchmark across estimands.
6. **The tally "Across every strict and Lp(a)-omitted horizon/cohort cell, no comparator significantly outperformed CALON-C."** *Requires:* pre-specified non-inferiority margins, adequate power in each cell, and a common evaluable population across cells. None exists; the manuscript concedes as much in the next sentence. *Delete* the tally and retain only the pre-specified confirmatory comparisons.
7. **"The first identified head-to-head application of CALON-C and the three named published instruments within the present corrected UK Biobank carrier frame."** *Requires:* a priority claim indexed to something other than a self-defined set. *Delete*, and replace with the setting-transfer novelty claim (E1 is the closest overlapping work and must be named as such).

**Transport.**

8. **The transport asymmetry (C = 0.7252 versus 0.6600) and the three paragraphs interpreting it.** *Requires:* bootstrap intervals for both estimates and a formal comparison. If the interval for the difference includes zero, the asymmetry is a TIE and all interpretation must be deleted.
9. **The Welsh transport estimate as a valid ranking assessment.** *Requires:* re-derivation of the Welsh risk set without outcome-conditional inclusion, and an administrative end-of-recording date. *Otherwise:* report as a stress test with an explicit statement that inclusion was conditioned on the outcome and the bias direction is unknown.
10. **"No Welsh head-to-head comparison showed superiority" as evidence about the frozen equation.** The Welsh comparisons used a Wales-refitted seven-term model, not the frozen equation. *Requires:* rerunning the Welsh comparisons with the frozen UK Biobank equation. *Otherwise:* state which model was used and note that ties arose despite a local refit.

**Statistical claims.**

11. **Every C-statistic reported without a confidence interval** — all six in Table 3, all six in Table 4, both transport values, all abstract values. *Requires:* intervals. *Otherwise:* the numbers cannot support any claim.
12. **The hazard ratios and 95% confidence intervals in Table 2 as reported.** *Requires:* intervals valid under penalisation (bootstrap or a penalisation-aware method), and a statement that the two age terms are not separately interpretable. *Otherwise:* remove the intervals and present coefficients only.
13. **"Internal 10-year calibration… slope 1.101 and expected:observed ratio 1.008"** as evidence of acceptable agreement. *Requires:* out-of-fold or external baseline estimation, a flexible calibration curve, an integrated calibration index with intervals, and interpretation of the 3.3% scaled Brier score. *Otherwise:* report as apparent calibration with no interpretive weight.
14. **"None of 16 tested model terms violated the proportional-hazards assumption."** *Requires:* separate reporting by cohort and a statement of power. *Otherwise:* delete the combined count.
15. **The claim that lipid terms contribute little as a substantive biological finding.** *Requires:* multiple imputation with uncertainty propagation, an intensity-specific treatment correction, and demonstration that the cohort's lipid range is genuinely restricted. *Otherwise:* report as an observation confounded by imputation, treatment correction and carrier-definition breadth.
16. **The +0.033 versus +0.008 concordance decomposition.** *Requires:* intervals on both increments and acknowledgement that concordance increments are not additive. *Otherwise:* present qualitatively.
17. **"The specification was fixed before the CALON-C fit."** *Requires:* a timestamped pre-specification document. *Otherwise:* delete the assertion entirely; the retraction in the same sentence does not repair it.

**Grey zone and biomarkers.**

18. **The framing of Lp(a) and apoB exclusion as a validated design advantage.** *Requires:* demonstration that Lp(a) is measured and informative in the cohort. Given the null association here against established evidence (E7), *delete* the validation framing and retain scalability as a design rationale only, with an explicit statement that the null Lp(a) result is discordant with FH evidence and may reflect measurement or unit conversion.
19. **The three grey-zone differences as reported.** *Requires:* a single stated base C, per-row evaluable n, and reconciliation of the three implied base values. *Otherwise:* report the analysis qualitatively.

**Reporting and process.**

20. **"The UK Biobank competing-risk analysis did not execute"** and every equivalent statement. *Requires:* running the analysis. *Otherwise:* delete; a software failure is not a result.
21. **All internal process language** — `RESULTS_FINAL_CORRECTED.md`, `code/38_CALON_C_CORRECTED.py`, the CALON-N/F/H/H2/11 lineage as file provenance, "the later reviewer response judged", "the reviewer response explicitly withdrew", "because the user requested explicit grey-zone treatment", and "This priority claim should be rechecked immediately before submission". *Delete.* One fact must survive in reworded form: that several model generations preceded this one on these data, because it bears on optimism.
22. **Process items in the Strengths paragraph** — "explicit withdrawal of unsupported decision-curve claims" and "The corrections moved results in both directions and were disclosed even when they strengthened CALON-C". *Delete*, and add the out-of-fold design of all comparator comparisons, which is a genuine strength the manuscript does not currently claim.
23. **Reference 9 as cited.** The title is not the published title. *Correct or delete.*
24. **Reference 10 as attached to the multi-biomarker claim.** *Reattach or delete.*
25. **"Comparator coefficients were checked… Background and novelty claims were cross-checked… The literature review is therefore structured and source-verified."** *Requires:* a citation-fidelity pass resolving the incorrect title, the miscitation, and the 19 uncited references. *Otherwise:* delete the source-verification claim.
26. **"Ancestry was not available in the CALON-C analysis frame", "UK Biobank lacked kinship data", and the death-field explanation.** All three describe extraction choices as data limitations, and E2 demonstrates that ancestry-stratified FH analysis is feasible in this very cohort. *Requires:* performing the analyses. *Otherwise:* state plainly that the variables were available in UK Biobank but not extracted.

**Bottom line.** Claims 1 to 5, 8 to 11 and 20 are rejection-level and cannot be retained in any form without new work. Claims 6, 7, 12 to 19 and 21 to 26 are remediable by reanalysis or rewriting within the existing data. The manuscript's own hedging already anticipates a substantial fraction of this list, which is to its credit; the difficulty is that the hedged claims are also the claims in the title, the abstract and the Key points, and hedging in the Discussion does not neutralise assertion in the abstract.
