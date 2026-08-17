I accidentally hit another model’s review file while searching transport values; that content is ignored. The review below is from the manuscript, aggregate artefacts, and locally held publisher extracts only.

---

# CALON-C independent manuscript review — Blind Round 1

**Reviewer:** Cursor Grok 4.6, internal four-seat panel  
**Source:** `outputs/manuscript_2026-08-16/CALON_C_MANUSCRIPT_HIGH_CALIBRE.md` (16 August 2026; READ_ME_FIRST reports 7,348 main-narrative words)  
**Mode:** text-plus-aggregate review. No participant-level data were opened. Other models’ round-1 outputs were not used.

**Seats (kept distinct throughout):**  
1. Biostatistician  
2. Cardiologist  
3. Lipid-medicine specialist  
4. Senior Editor-in-Chief  

---

## Rejection-risk summary

This is a **prediction-model development paper with reciprocal setting-transport**, not an independent external validation, not a clinical-utility study, and not a demonstration that a cumulative-lipid construction ranks events among people with heterozygous familial hypercholesterolaemia (HeFH). The prose is unusually self-restrained for this programme: Wales is not called independent validation, the endpoint is not called MACE, decision-curve claims are withdrawn, and the FH-Risk-Score comparison is correctly called a **TIE**. Those concessions do not make the paper submission-ready.

**Editorial verdict.** **Reject at *Circulation*, *European Heart Journal*, and *JACC*.** At *Atherosclerosis* or *Journal of Clinical Lipidology* the realistic outcome is **reject and invite resubmission** after source regeneration, not “major revision while the numbers stand”. The manuscript itself states that it is not submission-ready. An editor who reads that sentence, then the ethics/funding/conflict placeholders, then Table 3 still showing Wales 1,159/92 beside a “corrected” 1,169/102, will stop.

**Fatal barriers (any one is sufficient):**

1. **Governance placeholders.** Ethics, legal basis, funding, conflicts, patient and public involvement, data-controller, and model-availability statements are absent. That is a desk-reject at every journal named above.
2. **Population–guideline mismatch.** The development cohort is a UK Biobank `ldlr_carrier` flag with empty `variant_id` and a reported untreated LDL-C excess of only **+0.15 to +0.23 mmol/L**. That is not clinic HeFH. The 2026 ACC/AHA HeFH recommendations (Class 2b for FH-specific scores; Class 3: Harm against general-population 10- and 30-year calculators) apply to **HeFH**, not to this flag. Framing the paper as an FH-score problem therefore overstates both the clinical question and the guideline gap.
3. **Absolute-risk equation without competing-risk or out-of-fold baseline in UK Biobank.** Table 2 publishes `S0(5)` and `S0(10)` while the UK Biobank competing-risk analysis did not execute and calibration is internal/apparent. Publishing usable 5- and 10-year percentages in that state is unsafe.
4. **Confirmatory superiority is at the wrong horizon for SAFEHEART-RE.** SAFEHEART-RE is a 5-year (and derived 10-year) specialist-registry equation. After Holm correction, the 5-year UK Biobank comparison is a **TIE** (Holm-adjusted p=0.0560). The retained “win” is full follow-up against a score whose previous-ASCVD term is structurally zero and whose measured LDL-C is treatment-suppressed. That is a real common-data delta, not a clinical verdict.
5. **Unsynchronised Welsh source files.** Corrected risk set 1,169/102 sits beside discrimination, calibration, and Table 3 values from 1,159/92. The paper discloses this and still presents the older numbers in tables. Disclosure does not convert unsynchronised outputs into results.

**What would remain after those are fixed.** An incremental, methodologically useful common-data ranking comparison in a genotype-first UK Biobank carrier frame, with honest ties to FH-Risk-Score and no Welsh head-to-head win. That is a specialist-journal paper, not a priority claim.

---

## Paragraph-by-paragraph review

Evidence reused across paragraphs is listed once in the Eligible evidence ledger. Papers without a publisher PDF extract or live PubMed/Crossref return **in this runtime** are marked **UNVERIFIED — DO NOT CITE** when used to support or challenge a claim.

---

### Key points — Question

**Current claim.** A parsimonious routine-lipid model can rank first atherosclerotic events among LDLR-variant carriers at least as well as established FH instruments.

**Biostatistician.** “At least as well as” is a non-inferiority estimand. No margin was pre-specified. The later FH-Risk-Score result is a TIE, not non-inferiority. Severity: **MAJOR**.

**Cardiologist.** The question assumes the readers’ patients are the same as `ldlr_carrier` participants. They are not. Severity: **MAJOR**.

**Lipid-medicine specialist.** Established FH instruments were built for molecularly defined or Dutch Lipid Clinic Network (DLCN) HeFH, not for a flag with ~0.2 mmol/L LDL-C excess. Severity: **MAJOR**.

**Evidence check.** ACC/AHA 2026 applies FH-score language to **adults with HeFH** (COR 2b B-NR), not to unadjudicated carrier flags. Local publisher extract: *Circulation* 2026;153:e1154–e1276, 28 April 2026. DOI [10.1161/CIR.0000000000001423](https://doi.org/10.1161/CIR.0000000000001423).

**Required improvement.** Recast the question as ranking in population-ascertained LDLR-carrier-flag adults, not as a substitute for FH instruments in HeFH clinics.

**Suggested replacement wording.** “In UK Biobank adults identified only by an `ldlr_carrier` flag and free of prevalent atherosclerotic disease, can a model restricted to a standard lipid panel and routine clinical variables rank first incident atherosclerotic events on the same evaluable subsets as published FH scores?”

**Editor-in-Chief adjudication.** **MAJOR.** The question already over-promises the population.

---

### Key points — Findings

**Current claim.** In 3,209 UK Biobank carrier-flag participants, CALON-C had moderate internal discrimination; full-follow-up discrimination was higher than SAFEHEART-RE and Montreal-FH-SCORE after Holm correction, and did not differ from FH-Risk-Score; frozen transport C=0.725 to Wales and C=0.660 in reverse; a predecessor grey-zone analysis showed no significant gain from Lp(a), apoB/LDL-C, or both.

**Biostatistician.** Headline omits that the 5-year confirmatory family is null after Holm, that Welsh head-to-head is uniformly a TIE, and that grey-zone C in the band is ~0.59–0.61. Transport C is reported without the 9-term versus 7-term asymmetry. Severity: **MAJOR**.

**Cardiologist.** “Moderate internal discrimination” (C≈0.71) will not change intensification decisions in true HeFH, where treatment is already indicated. Severity: **MODERATE**.

**Lipid-medicine specialist.** Grey-zone “no gain” is from CALON-F, not CALON-C, and cannot support a lipid-assay policy sentence even as a key point. Severity: **MODERATE**.

**Evidence check.** Numbers match `calon_c_corrected.json` / `RESULTS_FINAL_CORRECTED.md` for the UK Biobank deltas. Grey-zone values match `grey_zone_enhancers.json` (n scored=3,333; band 1,685/218).

**Required improvement.** Put the Holm-null 5-year result and the FH-Risk-Score TIE in the same breath as the two wins. Label grey-zone as predecessor.

**Suggested replacement wording.** “Optimism-corrected C was 0.7095 over full follow-up. On complete-input subsets, full-follow-up C was higher than SAFEHEART-RE and Montreal-FH-SCORE after Holm correction and was a TIE versus FH-Risk-Score. No five-year comparison survived Holm correction. Frozen UK Biobank-to-Wales ranking C was 0.725; reverse transport of a seven-term Welsh equation gave C=0.660. A predecessor grey-zone analysis did not show a significant C gain from Lp(a) or apoB/LDL-C.”

**Editor-in-Chief adjudication.** **MAJOR** if the 5-year null stays out of the Findings box.

---

### Key points — Meaning

**Current claim.** CALON-C supports feasibility of routine-data ranking but does not establish independent external validation, clinical utility, or superiority to every FH instrument; further validation, external calibration, UK Biobank competing-risk analysis, and comparative decision curves are required before clinical use.

**Biostatistician.** This is the correct inferential ceiling. Severity: **MINOR** (keep).

**Cardiologist.** “Before clinical use” is still too weak: the model must not be used to defer therapy in anyone who meets HeFH criteria. Severity: **MODERATE**.

**Lipid-medicine specialist.** Agree with the cardiologist; also state that the cohort is not a treatment-decision population for FH guidelines. Severity: **MODERATE**.

**Evidence check.** ACC/AHA 2026: CAC=0 may not de-risk FH or defer statin; LLT is recommended in HeFH. Same local extract as above.

**Required improvement.** Add an explicit non-de-risking sentence.

**Suggested replacement wording.** “These results support only further methodological evaluation of routine-data ranking in carrier-flag cohorts. They do not establish independent external validation, calibration in care, net benefit, or any basis to delay guideline-directed lipid-lowering in HeFH.”

**Editor-in-Chief adjudication.** **MODERATE.** The Meaning box is the strongest paragraph in the front matter; it still needs the de-risking prohibition.

---

### Abstract — Background

**Current claim.** Guidance recognises that FH-specific scores may help short-term ASCVD risk, while general-population 10- or 30-year equations should not be used in heterozygous FH; existing instruments differ and are incompletely characterised in population-ascertained LDLR-variant carriers.

**Biostatistician.** “Incompletely characterised” is fair; the paragraph does not state an estimand. Severity: **MINOR**.

**Cardiologist.** The guideline sentence is accurate **for HeFH**, then the paper studies a different population. That slide is the abstract’s main clinical error. Severity: **MAJOR**.

**Lipid-medicine specialist.** Same. Population-ascertained LDLR carriage is a different phenotype from clinic HeFH. Ref 15 (2005) is outside the evidence window and should not underwrite this contrast. Severity: **MAJOR**.

**Evidence check.** Supporting, in-window, locally extracted: ACC/AHA 2026 HeFH section (COR 2b / COR 3: Harm). Challenging: the same guideline’s object is HeFH, not UK Biobank carrier flags. ESC/EAS 2025 still places FH without other major risk factors in the **high-risk** category and FH with ASCVD or another major risk factor in **very-high-risk** (*Eur Heart J* 2025;46:4359–4378, DOI [10.1093/eurheartj/ehaf190](https://doi.org/10.1093/eurheartj/ehaf190)).

**Required improvement.** Separate the HeFH guideline statement from the study population in one sentence.

**Suggested replacement wording.** “In adults with heterozygous FH, 2026 ACC/AHA guidance states that FH-specific scores may be useful for short-term risk prediction and that general-population 10- or 30-year equations should not be used. Performance of those scores among population-ascertained LDLR-carrier-flag adults, who are not equivalent to clinic HeFH, is incompletely characterised.”

**Editor-in-Chief adjudication.** **MAJOR.** Do not let the guideline apply by juxtaposition.

---

### Abstract — Methods

**Current claim.** Ridge-penalised Cox model in UK Biobank `ldlr_carrier` participants free of prevalent/undated ASCVD; routine predictors including cumulative untreated-equivalent non-HDL-C, triglyceride filter, and remnant cholesterol; internal OOF C and bootstrap optimism; published comparators on complete-input subsets with paired bootstrap and Holm correction across six comparisons; reciprocal frozen transport; decision-curve claims withdrawn.

**Biostatistician.** Honest on DCA withdrawal and Holm family. Does not say the ridge penalty was not nested-CV selected, that missingness was median-imputed, or that the confirmatory family is full plus 5-year rather than the SAFEHEART native 5-year primary. Severity: **MODERATE**.

**Cardiologist.** “Cumulative untreated-equivalent non-HDL cholesterol” will be read as cholesterol-years. It is `log(non-HDL_untreated × age)` at one visit. Severity: **MAJOR** (shared with lipid seat).

**Lipid-medicine specialist.** Agree: this is not cumulative exposure. Treatment correction is a fixed 0.70/0.80 factor. Severity: **MAJOR**.

**Evidence check.** SAFEHEART-RE derivation used enrolment variables, family-clustered Cox, and bootstrap ×100 (*Circulation* 2017;135:2133–2144, 30 May 2017, DOI [10.1161/CIRCULATIONAHA.116.024541](https://doi.org/10.1161/CIRCULATIONAHA.116.024541)). FH-Risk-Score: 3,881 primary-prevention adults, age 18–65, C=0.75 for 10-year ASCVD (*ATVB* 2021;41:2632–2640, DOI [10.1161/ATVBAHA.121.316106](https://doi.org/10.1161/ATVBAHA.121.316106)). Cholesterol-years as used in REFERCHOL is **UNVERIFIED — DO NOT CITE** in this runtime (no local full text / no live Crossref).

**Required improvement.** Rename the lipid terms in the abstract; state complete-case comparator subsets and median imputation.

**Suggested replacement wording.** “A ridge-penalised Cox model (penalty 0.02) used age, an age-above-50 term, sex, hypertension, diabetes, smoking, a single-visit log product of untreated-equivalent non-HDL-C and age, a triglyceride-ratio term, and untreated-equivalent remnant cholesterol. Continuous missing predictors were median-imputed. Comparators were scored only on complete-input subsets. Decision-curve claims were withdrawn.”

**Editor-in-Chief adjudication.** **MAJOR** for the word “cumulative”.

---

### Abstract — Results

**Current claim.** 3,540 → 207 prevalent + 124 undated excluded → 3,209/289; optimism-corrected C 0.7095; vs SAFEHEART +0.070 (0.036 to 0.104; Holm p=0.0003); vs Montreal +0.032 (0.011 to 0.055; p=0.0179); vs FH-Risk-Score +0.015 (−0.011 to 0.040; p=0.5018) TIE; no 5-year comparison significant after Holm; Wales 1,169/102 with no head-to-head superiority; transport C=0.725 and 0.660; 0/16 PH violations; Welsh CIF 6.02%/11.97%; UK Biobank competing-risk analysis did not execute; internal 10-year slope 1.101 (0.884 to 1.318), E:O 1.008 (0.883 to 1.153).

**Biostatistician.** The numerical ledger is internally consistent with `calon_c_corrected.json`. Two problems: (i) C=0.725 is rounded from 0.7252 while other C values keep four decimals; (ii) “0/16 PH violations” pools 9 UK Biobank + 7 Welsh terms. Five-year Holm p=0.0560 is a TIE, correctly not claimed as a win. Severity: **MODERATE**.

**Cardiologist.** Publishing Welsh CIF beside a failed UK Biobank competing-risk analysis invites readers to treat 6% and 12% as the UK Biobank absolute risks. They are not. Severity: **MAJOR**.

**Lipid-medicine specialist.** Event rate and case mix (43% male, median age 57, modest lipid separation) read as a treated volunteer sample, not untreated HeFH. Severity: **MODERATE**.

**Evidence check.** Aggregate artefacts confirm the deltas. Insufficient validated in-window evidence that C≈0.71 is “clinically moderate” in HeFH care; SAFEHEART derivation C=0.85/0.81 is a different population and estimand.

**Required improvement.** Keep four decimals or state rounding. Label 16 terms as cross-cohort. Do not juxtapose Welsh CIF with UK Biobank calibration as if they were one absolute-risk story.

**Suggested replacement wording.** “Optimism-corrected C was 0.7095 over full follow-up. Full-follow-up differences favoured CALON-C versus SAFEHEART-RE and Montreal-FH-SCORE and were a TIE versus FH-Risk-Score. No five-year difference survived Holm correction. Welsh competing-risk CIF was 6.02% at 5 years and 11.97% at 10 years; the UK Biobank competing-risk analysis did not execute. Internal UK Biobank 10-year calibration slope was 1.101 (0.884 to 1.318); this is not external calibration.”

**Editor-in-Chief adjudication.** **MAJOR** for the absolute-risk juxtaposition; numbers themselves are not the failure.

---

### Abstract — Conclusions

**Current claim.** Moderate ranking from routine data; favourable full-follow-up comparisons with SAFEHEART-RE and Montreal-FH-SCORE; TIE with FH-Risk-Score; evidence of development and setting transport, not independent external validation or clinical utility.

**Biostatistician.** Matches the design. Severity: **MINOR**.

**Cardiologist.** “Favourable comparisons” will be quoted without the setting caveat. Severity: **MODERATE**.

**Lipid-medicine specialist.** Does not say the lipid terms were individually **TIE**s. That omission lets “routine lipid profile” sound mechanistic. Severity: **MAJOR**.

**Evidence check.** Equation file: `cum_nonhdl` HR per SD 1.119 (0.954–1.334), remnant 1.113 (0.970–1.296), triglyceride filter 0.996 (0.884–1.122) — all TIEs.

**Required improvement.** One clause that the lipid-derived terms were not independently associated with events after adjustment.

**Suggested replacement wording.** “CALON-C provided moderate internal risk ranking from routine variables. Full-follow-up discrimination was higher than SAFEHEART-RE and Montreal-FH-SCORE and a TIE versus FH-Risk-Score. Adjusted lipid-derived terms were TIEs. These results are model development and setting transport, not independent external validation or clinical utility.”

**Editor-in-Chief adjudication.** **MAJOR** if the lipid TIE stays out of the abstract while “standard lipid measurements” stays in.

---

### Introduction ¶1 (guideline and heterogeneity)

**Current claim.** FH is lifelong LDL-receptor-pathway exposure with heterogeneous expression; 2026 ACC/AHA says FH-specific scores may help short-term prediction and general-population 10-/30-year tools should not be used in HeFH; European guidance keeps FH in high- or very-high-risk pathways.

**Biostatistician.** Heterogeneity is not an estimand. Severity: **MINOR**.

**Cardiologist.** Guideline quotations are accurate for HeFH and are then used to justify a carrier-flag model. Urgency of intensification is a treatment-decision claim the design cannot test. Severity: **MAJOR**.

**Lipid-medicine specialist.** ESC 2025 does retain FH in high/very-high-risk categories; that supports treating FH, not building a new score. “Polygenic background” is named but absent from CALON-C. Severity: **MODERATE**.

**Evidence check.** ACC/AHA 2026 local extract supports the two quoted recommendations. ESC/EAS 2025 local extract supports high-risk (FH without other major risk factors) and very-high-risk (FH with ASCVD or another major risk factor).

**Required improvement.** End the paragraph on the **carrier-flag gap**, not on HeFH treatment urgency.

**Suggested replacement wording.** “Those recommendations apply to heterozygous FH. Whether the same instruments rank events among population-ascertained LDLR-carrier-flag adults is a separate question.”

**Editor-in-Chief adjudication.** **MAJOR.** This paragraph currently licenses the wrong paper.

---

### Introduction ¶2 (established instruments)

**Current claim.** SAFEHEART-RE, Montreal-FH-SCORE, and FH-Risk-Score answer non-identical questions; REFERCHOL and English routine care show transport/calibration failure; an Australian genetically confirmed cohort reported incident C=0.767 (SAFEHEART-RE) and 0.735 (FH-Risk-Score).

**Biostatistician.** Correct that instruments are not interchangeable. Australian C-statistics **UNVERIFIED — DO NOT CITE** in this runtime (ref 9; no local full text; live Crossref/PubMed did not return). Severity: **MAJOR** for the unverified 2026 paper.

**Cardiologist.** SAFEHEART included primary and secondary prevention; Montreal is prevalent disease; FH-Risk-Score is incident 10-year primary prevention aged ≤65. The paper later compares all three to one incident primary-prevention ranking estimand. Severity: **MAJOR**.

**Lipid-medicine specialist.** SAFEHEART n=2,404 molecularly defined Spanish patients and C=0.85/0.81 are supported by the local *Circulation* extract. FH-Risk-Score n=3,881, UK Biobank n=499, C=0.75, and superiority to SAFEHEART C=0.69 in that derivation are supported by the local *ATVB* extract. REFERCHOL/McKay remain **UNVERIFIED — DO NOT CITE** here. Severity: **MODERATE** (verified core is solid; unverified external numbers are not).

**Evidence check.** SAFEHEART 2017 and FH-Risk-Score 2021 as above. Montreal derivation/refinement: **UNVERIFIED — DO NOT CITE** (DOI in list only). Tamehri 2026: **UNVERIFIED — DO NOT CITE**.

**Required improvement.** Keep only locally verified comparator facts in the introduction; move unverified external C-statistics out until DOI resolution succeeds.

**Suggested replacement wording.** “SAFEHEART-RE was derived for incident ASCVD in a molecularly defined Spanish registry that included prior ASCVD (Harrell C 0.85 overall; 0.81 without prior ASCVD). The FH-Risk-Score was derived for incident 10-year ASCVD in 3,881 primary-prevention adults aged 18–65 years, including 499 UK Biobank participants (C=0.75). Montreal-FH-SCORE was derived against prevalent disease.”

**Editor-in-Chief adjudication.** **MAJOR** until ref 9 is verified or deleted.

---

### Introduction ¶3 (three unresolved issues)

**Current claim.** (i) Cross-cohort quoting conflates model quality with case mix; (ii) Lp(a)/apoB/imaging/PRS constrain implementation, citing [10,11]; (iii) clinic FH and population LDLR carriage are not interchangeable, citing Tybjærg-Hansen 2005 [15] and UK Biobank volunteer selection [19–21].

**Biostatistician.** Point (i) is the paper’s real methodological contribution. Point (ii) citations appear mismatched. Severity: **MAJOR**.

**Cardiologist.** Implementation constraints are real, but once-in-lifetime Lp(a) is now Class 1 in ACC/AHA 2026; arguing parsimony against a Class 1 test is a policy fight, not a data gap. Severity: **MAJOR**.

**Lipid-medicine specialist.** Phenotype attenuation in population ascertainment is true and important, but [15] is 2005 and **outside the window**. In-window genotype-first work must carry this claim. Volunteer selection [19] is in-window if Fry 2017 is accepted; this runtime did not re-resolve that DOI. Severity: **MAJOR**.

**Evidence check.** Ref 10 (Tamehri *Can J Cardiol* 2025) and ref 11 (Zamora AI algorithms) do not, on their titles, support “apoB, imaging, polygenic scores, or dozens of variables.” **UNVERIFIED — DO NOT CITE** plus likely citation–claim mismatch. Ref 15: 2005 — excluded historical context only. ACC/AHA 2026: Lp(a) measurement in all adults is COR 1.

**Required improvement.** Replace [10,11] with in-window papers that actually use those inputs, or drop the examples. Move [15] to an excluded-historical note. Cite an in-window genotype-first FH paper after DOI verification.

**Suggested replacement wording.** “Clinically ascertained HeFH and population-detected LDLR-variant carriage are not interchangeable, and UK Biobank participation is volunteer-selected. A common-data comparison in the carrier-flag frame is therefore not a clinic-FH validation.”

**Editor-in-Chief adjudication.** **FATAL** if [15] remains as evidence for a scientific claim; **MAJOR** for [10,11].

---

### Introduction ¶4 (CALON-C design proposition)

**Current claim.** CALON-C tests whether routinely available information can recover useful near-term ASCVD ordering among LDLR-variant carriers without assuming advanced assays.

**Biostatistician.** “Useful” is undefined (no decision threshold, no DCA). Severity: **MAJOR**.

**Cardiologist.** Near-term ordering without absolute risk or net benefit is not a clinic proposition. Severity: **MAJOR**.

**Lipid-medicine specialist.** Excluding Lp(a) after a Class 1 measurement recommendation needs to be labelled as an availability experiment, not as lipidology. Severity: **MODERATE**.

**Evidence check.** Insufficient validated evidence within the window that routine-panel parsimony improves FH outcomes.

**Required improvement.** Replace “useful” with “discriminant ranking as Harrell C”.

**Suggested replacement wording.** “The model tests whether a standard lipid panel plus routine clinical variables can produce incident-event ranking among LDLR-carrier-flag adults, not whether specialised assays lack biological value.”

**Editor-in-Chief adjudication.** **MAJOR** for “useful”.

---

### Introduction ¶5 (aims)

**Current claim.** Develop and internally assess CALON-C; apply three comparators head-to-head; assess reciprocal transport; because FH-Risk-Score included 499 UK Biobank participants, that comparison is not independent external validation.

**Biostatistician.** The 499 overlap caveat is mandatory and correctly placed. Aims still omit competing risk, calibration type, and multiplicity family. Severity: **MODERATE**.

**Cardiologist.** Agree the overlap sentence is essential. Severity: **MINOR**.

**Lipid-medicine specialist.** “LDLR-variant carriers” in the aim still overstates the flag. Severity: **MODERATE**.

**Evidence check.** FH-Risk-Score local extract: UK Biobank n=499 in derivation.

**Required improvement.** Say `ldlr_carrier` flag; name the six-cell Holm family; name transport as non-independent.

**Suggested replacement wording.** “We aimed to develop CALON-C in UK Biobank participants with an `ldlr_carrier` flag and no prevalent or undated ASCVD; compare ranking with three published instruments on each instrument’s complete-input subset, with Holm correction across six confirmatory cells; and apply frozen equations reciprocally to the All-Wales genotype-positive registry. Because FH-Risk-Score included 499 UK Biobank participants, that comparison is not an independent external validation.”

**Editor-in-Chief adjudication.** **MODERATE.** This is the best paragraph in the Introduction.

---

### Methods — Study design and reporting framework ¶1

**Current claim.** Two-cohort prognostic prediction-model study; TRIPOD+AI, STROBE, RECORD; PROBAST to identify bias; estimand is association of a baseline linear predictor with time to first incident atherosclerotic event among LDLR-variant carriers free of prevalent ASCVD.

**Biostatistician.** Estimand is ranking/association, not a risk difference, not a treatment effect. RECORD 2015 [39] is **outside the window**. STROBE is asserted but not cited. PROBAST 2019 is in-window but **UNVERIFIED** here. Transport of a different 7-term Welsh fit is not in the estimand sentence. Severity: **MAJOR**.

**Cardiologist.** Time-to-first-ASCVD in volunteers with a mild lipid phenotype is not the clinical estimand of HeFH care. Severity: **MODERATE**.

**Lipid-medicine specialist.** “LDLR-variant carriers” in the estimand repeats the pathogenicity over-read. Severity: **MAJOR**.

**Evidence check.** TRIPOD+AI Collins 2024: **UNVERIFIED — DO NOT CITE** this runtime. RECORD 2015: excluded historical context. ACC/AHA/SAFEHEART/FH-RS as above for population mismatch.

**Required improvement.** Rewrite estimand onto the flag; cite an in-window reporting statement for STROBE or drop the name; move RECORD to historical note.

**Suggested replacement wording.** “The estimand was the association between a baseline linear predictor and time to first incident atherosclerotic event among adults with an `ldlr_carrier` flag and no prevalent or undated ASCVD, with Harrell C as the primary ranking metric.”

**Editor-in-Chief adjudication.** **MAJOR.**

---

### Methods — Study design ¶2 (source of truth)

**Current claim.** `RESULTS_FINAL_CORRECTED.md` from `code/38_CALON_C_CORRECTED.py` supersedes earlier CALON versions; no new analysis for this manuscript; unsynchronised artefacts retained explicitly.

**Biostatistician.** Retaining contradictory machine-readable files while publishing tables from the old frame is not a reporting solution. Severity: **FATAL**.

**Cardiologist.** Readers cannot know which Welsh n to believe. Severity: **FATAL**.

**Lipid-medicine specialist.** Agree. Severity: **FATAL**.

**Evidence check.** Ledger and Table 3/5 confirm the split frame (1,169/102 vs 1,159/92).

**Required improvement.** Regenerate every Welsh descriptive, discrimination, calibration, and equation artefact from the 1,169/102 frame **before** submission. Until then, remove Welsh numerical tables.

**Suggested replacement wording.** “Welsh discrimination, calibration, and baseline tables from the pre-rescue 1,159/92 frame are not reported as CALON-C results. Only flow, head-to-head, and competing-risk outputs from the corrected 1,169/102 frame are shown.”

**Editor-in-Chief adjudication.** **FATAL.**

---

### Methods — Data sources and governance ¶1

**Current claim.** UK Biobank predictors from a 501,936-row master linked to corrected ASCVD and BP-medication data; All-Wales 7,253 records, genotype-positive via `Positive1`, DRAGON Lp(a); governed local storage; no identifiers exported.

**Biostatistician.** Linkage quality metrics are absent (RECORD 6.2). Severity: **MAJOR**.

**Cardiologist.** “Corrected ASCVD” is necessary given known UK Biobank outcome-field hazards, but the abstract still has to say what events were captured. Severity: **MODERATE**.

**Lipid-medicine specialist.** DRAGON Lp(a) for comparator scoring is appropriate; mixed units in the native Welsh field are a real implementation finding. Severity: **MINOR**.

**Evidence check.** Programme rule: use `corrected_ascvd_outcomes.csv`. Methods file confirms that source. No participant rows inspected.

**Required improvement.** Add linkage coverage and date-completeness summary (already in METHODS: I21/I25 100%; I63 40.9%; G45 37.0%) to the manuscript methods, not only the internal methods file.

**Suggested replacement wording.** “UK Biobank events were taken from the corrected linked outcome file. Component-date completeness was 100% for I21 and I25, and lower for I63, I70, I73, and G45. Procedure extracts were empty.”

**Editor-in-Chief adjudication.** **MAJOR** for missing linkage metrics in the paper that claims RECORD.

---

### Methods — Data sources ¶2 (carrier flag and placeholders)

**Current claim.** `variant_id` empty in all 501,936 rows, so the UK Biobank population is a carrier flag, not uniformly P/LP HeFH; Wales is genotype-positive by a clinical field; ethics/funding/COI/PPI are placeholders.

**Biostatistician.** The flag limitation is correctly stated. Placeholders make the paper non-submissible. Severity: **FATAL**.

**Cardiologist.** Agree. No ethics sentence, no journal. Severity: **FATAL**.

**Lipid-medicine specialist.** “Genotype-positive by its clinical data field” is still not variant-class (LDLR vs APOB vs PCSK9; P/LP vs VUS). Severity: **MAJOR**.

**Evidence check.** Insufficient validated evidence in-window to equate an unspecified “Positive1” field with ClinVar P/LP HeFH.

**Required improvement.** Supply governance text or do not submit. State that Welsh genotype-positive status was not re-adjudicated at variant level in this package.

**Suggested replacement wording.** “UK Biobank analyses used the available `ldlr_carrier` flag only. Pathogenic or likely pathogenic status was not confirmed. Welsh analyses used the registry genotype-positive field without variant-level re-adjudication in this package. Ethics, funding, and conflict statements were not available in the source package and are not invented here.”

**Editor-in-Chief adjudication.** **FATAL.**

---

### Methods — UK Biobank cohort ¶1

**Current claim.** Eligibility `ldlr_carrier==1`; baseline = assessment date; ASCVD = union of I21, I25, I63, I70, I73, G45; I50 excluded; prevalent = event on or before baseline; undated flag = unknown, not disease-free.

**Biostatistician.** Undated-as-unknown is the correct missing-data decision. I20 angina and revascularisation are absent; I22/I24 not listed. Composite is coronary-weighted by date completeness, not by definition. Severity: **MAJOR**.

**Cardiologist.** Excluding I50 is reasonable; omitting procedures and unstable angina/I20 makes this a softer/harder hybrid that is **not** aligned with SAFEHEART or FH-Risk-Score MACE-style charts (and must not be called MACE — the paper correctly does not). Transport to a Welsh endpoint that **includes angina and revascularisation** is an estimand change. Severity: **MAJOR**.

**Lipid-medicine specialist.** Peripheral codes I70/I73 in FH are relevant but poorly dated. Severity: **MODERATE**.

**Evidence check.** Insufficient verified in-window evidence that this six-code union matches any comparator’s endpoint. SAFEHEART incident ASCVD definition: local extract discusses incident ASCVD including prior-ASCVD patients; exact code list not re-extracted here.

**Required improvement.** Print a comparator-endpoint mismatch table. Do not transport C as if endpoints were the same.

**Suggested replacement wording.** “The UK Biobank endpoint was the earliest dated I21, I25, I63, I70, I73, or G45 event after baseline. Revascularisation could not be captured. This composite is not identical to the All-Wales or published FH-score endpoints.”

**Editor-in-Chief adjudication.** **MAJOR.**

---

### Methods — UK Biobank cohort ¶2

**Current claim.** 3,540 carriers; 207 prevalent and 124 undated excluded; 3,209 remaining; 289/97/194 events; follow-up to event, death, or 31 December 2023; unambiguous component dates in 147/289.

**Biostatistician.** 124 undated exclusions are a selection, not a sensitivity. 147/289 unambiguous dates means **49%** of events have attribution ambiguity; the paper later correctly refuses a “clean” restriction because it is informative censoring. 5-year events=97 for 9 terms is EPV≈10.8, barely conventional. Severity: **MAJOR**.

**Cardiologist.** Administrative censoring on 31 December 2023 without a competing-risk death analysis in this cohort blocks absolute risk. Severity: **MAJOR**.

**Lipid-medicine specialist.** n=3,209 looks large; the phenotype is mild. Event counts, not n, govern power. Severity: **MODERATE**.

**Evidence check.** Counts match `ledger_ukb` in `calon_c_corrected.json`. Riley external-validation sample-size papers [26–28] are unused in the body and **UNVERIFIED** here.

**Required improvement.** State EPV at each horizon. Keep the 147/289 limitation in the abstract.

**Suggested replacement wording.** “There were 289 events over full follow-up (EPV 32), 194 by 10 years (EPV 22), and 97 by 5 years (EPV 11). Component-date attribution was unambiguous for 147 of 289 events.”

**Editor-in-Chief adjudication.** **MAJOR.**

---

### Methods — All-Wales cohort ¶1

**Current claim.** Frame began at 2,405 genotype-positive participants; baseline = first dated lipid visit; outcome = earliest post-baseline MI/ACS, PCI, CABG, angina, TIA, or PVD; correction retained dated post-baseline events regardless of later operational contact, rescuing 10 events.

**Biostatistician.** Changing the follow-up rule after seeing discarded events is a correction, not a pre-specified sensitivity. Rescuing 10 events (92→102) can move Welsh head-to-head from a fragile win to a TIE, which is exactly what happened versus FH-Risk-Score in the results file. Severity: **MAJOR**.

**Cardiologist.** Including angina in Wales but not UK Biobank is clinically material. Severity: **MAJOR**.

**Lipid-medicine specialist.** First dated lipid visit as time zero in a cascade registry risks mixing incident diagnosis with long-standing treated disease. Severity: **MAJOR**.

**Evidence check.** Insufficient validated in-window literature that first lipid visit is a valid time zero for FH registry prediction without left truncation.

**Required improvement.** Call the 10-event rescue a post-hoc ascertainment correction. Harmonise endpoints or stop calling transport a test of the same outcome.

**Suggested replacement wording.** “After a follow-up-rule correction that reinstated 10 dated post-baseline events, the Welsh risk set was 1,169 participants with 102 events. The Welsh endpoint included angina and coronary procedures, which were not captured in UK Biobank.”

**Editor-in-Chief adjudication.** **MAJOR.**

---

### Methods — All-Wales cohort ¶2

**Current claim.** Exclusions: 344 no baseline date, 185 prevalent, 58 outcome-positive without event age, 649 without operational follow-up or qualifying dated event; risk set 1,169/102 (51 at 5 years, 75 at 10 years); family number = clustering unit; no administrative end date; HTN/DM/smoking often last-contact status.

**Biostatistician.** 649 last-contact exclusions are informative censoring. 5-year events=51, EPV≈7 if 7 terms, below 10. Family clustering is used in Welsh optimism, which is correct. Predictor timing is a PROBAST predictor-definition failure. Severity: **FATAL** for any validation claim; **MAJOR** even for “transport”.

**Cardiologist.** Last-contact hypertension after an event is post-event phenotype, possibly treatment intensification, not baseline risk. Severity: **FATAL** if used as validation; **MAJOR** as stress test.

**Lipid-medicine specialist.** In FH registries, post-event lipid-lowering and BP treatment are expected. Using last-contact status ranks who was treated after disease. Severity: **MAJOR**.

**Evidence check.** `calon_c.json` itself records: of 92 Welsh events, 55 (59.8%) have BP dated after the event; only 94/1,159 have BP dated on or before baseline. That is an internal aggregate finding, not a literature claim.

**Required improvement.** Do not present UK Biobank-to-Wales C as evidence that ranking “transports” until a dated-baseline extract exists. Report the 55/92 figure in the manuscript body.

**Suggested replacement wording.** “Hypertension, diabetes, and smoking were not demonstrably baseline. In the pre-rescue frame, 55 of 92 events had blood pressure dated after the event. The UK Biobank-to-Wales C is a stress test of ranking under contaminated predictors, not a validation of baseline risk.”

**Editor-in-Chief adjudication.** **FATAL** if transport remains in the Findings box without this sentence; **MAJOR** if demoted.

---

### Methods — Outcome terminology ¶1

**Current claim.** “MACE” was rejected; primary outcome is first incident ASCVD; UK Biobank coronary-weighted with incomplete non-coronary dates and empty procedure extracts; Wales includes procedures and angina.

**Biostatistician.** Correct refusal of MACE. Heterogeneity is then ignored in the transport metric, which is a single C. Severity: **MAJOR**.

**Cardiologist.** This paragraph should have killed a pooled transport headline. It did not. Severity: **MAJOR**.

**Lipid-medicine specialist.** Angina in clinic FH is a different ascertainment process from I21/I25 in UK Biobank. Severity: **MODERATE**.

**Evidence check.** Insufficient validated evidence that Harrell C is comparable across these composites.

**Required improvement.** Report transport only as a secondary, endpoint-mismatched ranking experiment.

**Suggested replacement wording.** Keep the MACE refusal. Add: “Because the composites differ, reciprocal C values do not estimate performance for a common clinical endpoint.”

**Editor-in-Chief adjudication.** **MAJOR.**

---

### Methods — Predictors and treatment correction ¶1 (specification)

**Current claim.** Nine UK Biobank terms: age, sp50, male, hypertension (medication or ≥140/90), diabetes, current smoking, `cum_nonhdl=log(non-HDL_untreated × age)`, `tg_filter=log[LDL_untreated/(TG_untreated+0.1)]`, untreated-equivalent remnant cholesterol.

**Biostatistician.** Age and `sp50=max(age−50,0)` are collinear by construction; the collinearity guard only drops |r|≥0.999, so both stay. Ridge 0.02 is the only shrinkage. `cum_nonhdl` contains age again, so age is in the linear predictor three times. Severity: **MAJOR**.

**Cardiologist.** Hypertension defined with a single-visit BP plus undated medication is not a diagnosis. Severity: **MODERATE**.

**Lipid-medicine specialist.** `log(non-HDL × age)` is not cholesterol-years. Remnant clipped to −1 to 6 mmol/L admits negative remnant. `tg_filter` is not a standard remnant or TG-rich lipoprotein metric. Severity: **FATAL** for any cumulative-exposure claim; **MAJOR** for the specification as published.

**Evidence check.** Domanski *JACC* 2020 time-course of LDL exposure is listed as ref 22 but **not cited in the body** and **UNVERIFIED** here. SAFEHEART used categorical measured LDL-C, not a log product with age.

**Required improvement.** Rename terms. Report VIF/correlation of age, sp50, and cum_nonhdl. Forbid negative remnant (clip at 0).

**Suggested replacement wording.** “The lipid terms were a single-visit log product of untreated-equivalent non-HDL-C and chronological age, a log ratio of untreated-equivalent LDL-C to triglycerides, and untreated-equivalent remnant cholesterol (non-HDL-C minus LDL-C), with remnant values below 0 set to 0.”

**Editor-in-Chief adjudication.** **MAJOR** (FATAL if “cumulative” remains).

---

### Methods — Predictors ¶2 (treatment transformation)

**Current claim.** In treated participants, non-HDL-C and LDL-C divided by 0.70 and triglycerides by 0.80; clips applied; MAE 1.20 mmol/L (1.13 to 1.28), r=0.32 in 649 Welsh patients; varying 0.65–0.75 changed C by 0.0022/0.0019.

**Biostatistician.** r=0.32 means the “untreated-equivalent” covariate is mostly noise plus treatment status. Sensitivity showing C movement of 0.002 is expected if the term carries little ranking information, which the later HRs confirm. Severity: **MAJOR**.

**Cardiologist.** A reconstruction with MAE 1.2 mmol/L cannot support treatment decisions or cholesterol-year analogies. Severity: **MAJOR**.

**Lipid-medicine specialist.** A single 30% LDL reduction ignores intensity, ezetimibe, PCSK9 inhibition, inclisiran, bempedoic acid, adherence, and time on therapy. That is not pharmacologically defensible in 2026 FH care. Severity: **MAJOR**.

**Evidence check.** In-window dose-response literature (Karlson 2016 print date may predate 17 August 2016; Law 2003 is excluded historical). **Insufficient validated in-window evidence** in this runtime for a universal 0.70 factor as individual pre-treatment LDL. Internal MAE/r are programme aggregates, not a published reconstruction trial.

**Required improvement.** Call these operational rescalings, not untreated equivalents. Put MAE and r in the abstract if the terms remain.

**Suggested replacement wording.** “Treated lipid values were rescaled by fixed factors (LDL/non-HDL ÷0.70; triglycerides ÷0.80). In a programme audit of 649 Welsh patients, the LDL rescaling had mean absolute error 1.20 mmol/L (1.13 to 1.28) and correlation 0.32 with observed pre-treatment LDL-C. These are not validated individual untreated concentrations.”

**Editor-in-Chief adjudication.** **MAJOR.**

---

### Methods — Predictors ¶3 (exclusions from the core model)

**Current claim.** Statin/treatment flags excluded because undated treatment could encode post-event care; Lp(a), apoB, imaging, PRS, published scores, and prior CALON predictors excluded.

**Biostatistician.** Excluding a collider-like post-event treatment flag is correct. Excluding Lp(a) from the **model** while using it in **comparators** is a fair parsimony test only if comparators are complete-input. Severity: **MINOR**.

**Cardiologist.** Clinically, omitting treatment intensity removes the main actionable exposure in FH. Severity: **MODERATE**.

**Lipid-medicine specialist.** Omitting Lp(a) from the core equation after Class 1 measurement guidance is a design choice that must not be sold as evidence against measuring Lp(a). The later grey-zone paragraph tries to do that work with a predecessor model. Severity: **MODERATE**.

**Evidence check.** ACC/AHA 2026 Lp(a) COR 1.

**Required improvement.** Keep the leakage rationale; delete any implication that Lp(a) is optional in HeFH care.

**Suggested replacement wording.** “Treatment flags were excluded to avoid encoding post-event care. Lp(a) and apoB were excluded from the core equation to test a routine-panel specification, not because they lack clinical indication.”

**Editor-in-Chief adjudication.** **MODERATE.**

---

### Methods — Model specification ¶1

**Current claim.** Cox with ridge 0.02; specification “fixed before the CALON-C fit” but no verifiable pre-result file, so pre-specification withdrawn; median imputation within training fold; collinearity guard |r|≥0.999; binary terms need ≥10 events per level; Wales drops diabetes and smoking, leaving seven terms.

**Biostatistician.** Withdrawing pre-specification is mandatory (`RESULTS_FINAL_CORRECTED.md` still says “pre-specified” — do not copy that). Median imputation understates uncertainty. Dropping two prognostic terms in Wales because of a mechanical event-count rule produces a **different model**, so reverse transport is not reciprocal application of CALON-C. Ridge 0.02 without nested tuning is arbitrary. Severity: **MAJOR**.

**Cardiologist.** A 7-term Welsh model without diabetes or smoking is not a clinical FH model. Severity: **MODERATE**.

**Lipid-medicine specialist.** Diabetes dropped in the clinic cohort, where diabetes is a major amplifier of residual risk in HeFH, is biologically the wrong omission. Severity: **MAJOR**.

**Evidence check.** TRIPOD+AI requires handling of missing data and specification transparency — **UNVERIFIED** this runtime as a citation, but the reporting gap is visible in the text.

**Required improvement.** Never call the 7-term fit CALON-C. Use multiple imputation or complete-case sensitivity. State that reverse transport is a different equation.

**Suggested replacement wording.** “The CALON-C equation is the nine-term UK Biobank fit. The Welsh cohort-specific fit is a seven-term re-estimation after diabetes and smoking failed a ≥10-event rule, and is not CALON-C.”

**Editor-in-Chief adjudication.** **MAJOR.**

---

### Methods — Model specification ¶2 (internal validation)

**Current claim.** 10×10 OOF Harrell C with family clustering where available; 100 Harrell bootstrap resamples, matching SAFEHEART-RE and FH-Risk-Score; UK Biobank participant-level resampling because no kinship field.

**Biostatistician.** Matching B=100 to SAFEHEART is defensible for comparability; paired comparator deltas used B=2,000, so precision is inconsistent. Ignoring relatedness in UK Biobank likely understates variance, not necessarily C. OOF and optimism-corrected C agreeing within 0.008 is reassuring for **internal** discrimination. Severity: **MODERATE**.

**Cardiologist.** Internal validation cannot support clinic use. Severity: **MINOR** (already conceded later).

**Lipid-medicine specialist.** Family clustering in Wales is the right unit. Severity: **MINOR**.

**Evidence check.** SAFEHEART local extract: bootstrap resampling of the original set (100…). FH-Risk-Score optimism 0.002 is **UNVERIFIED** beyond the manuscript’s own `calon_apparent.json` note.

**Required improvement.** Report relatedness limitation as possibly anti-conservative CIs. Do not imply B=100 is adequate because a 2017 paper used it.

**Suggested replacement wording.** “Optimism correction used 100 bootstrap resamples to match the SAFEHEART-RE internal-validation method. UK Biobank CIs are not family-robust.”

**Editor-in-Chief adjudication.** **MODERATE.**

---

### Methods — Comparator implementation (SAFEHEART-RE)

**Current claim.** Published equation: age, sex, previous ASCVD, hypertension, active smoking, BMI category, measured LDL-C category, Lp(a)>50 mg/dL; measured not back-calculated LDL-C because pretreatment LDL multivariable cells are blank; previous ASCVD=0 by design; BMI 25/30 inferred from WHO; worked examples reproduced.

**Biostatistician.** Faithful to Table 3 of the 2017 paper. Setting previous ASCVD=0 for everyone **inactivates the strongest predictor** (multivariable HR 4.15). That is specification-faithful and setting-unfair. Headline superiority at full follow-up, not 5 years, adds a second mismatch. Severity: **MAJOR**.

**Cardiologist.** Comparing a primary-prevention volunteer cohort with prior ASCVD forced to zero against a score built to use prior ASCVD is not a test of the score in its intended use. Severity: **MAJOR**.

**Lipid-medicine specialist.** Measured on-treatment LDL-C in UK Biobank is not the specialist-visit LDL-C of SAFEHEART. The paper later admits this; the methods should say “strawman-by-design, not by coding error.” BMI: the paper says cut-points follow overweight/obesity definitions; 25/30 is a reasonable inference, not a hidden invention. Severity: **MODERATE**.

**Evidence check.** Local SAFEHEART Table 3: History of ASCVD multivariable HR 4.15 (2.55–6.75); measured LDL-C ≥160 mg/dL HR 4.80 (1.15–20.01); calculated pretreatment LDL-C multivariable cells blank; BMI as Normal/Overweight/Obesity; “Cut points for body mass index were selected according the definition of overweight and obesity.” Worked examples match the extract (≈0.02% and ≈38.1% 5-year).

**Required improvement.** State that two high-weight terms are structurally uninformative in this frame. Move the 5-year comparison to the primary confirmatory family **or** stop calling full-follow-up the SAFEHEART test.

**Suggested replacement wording.** “SAFEHEART-RE was applied with published coefficients. Previous ASCVD was 0 for every participant by the incident-cohort design, inactivating a term with published HR 4.15. LDL-C was the measured on-treatment value. This is a specification-faithful application in a setting that removes two of the score’s main information sources.”

**Editor-in-Chief adjudication.** **MAJOR.** This is the comparator-fairness problem, distinct from comparator-fidelity (which the authors largely got right).

---

### Methods — Comparator implementation (FH-Risk-Score)

**Current claim.** Table 3 points chart; age >65 not evaluated; ranking only, not absolute risk; untreated/imputed LDL-C.

**Biostatistician.** Age gate is correct (derivation excluded >65). Restricting to ≤65 and complete inputs yields 1,913/146 — a different population than the SAFEHEART subset 2,470/221. Head-to-head C’s are not on a common three-way sample. Severity: **MAJOR**.

**Cardiologist.** Dropping those over 65 removes the group in whom near-term events concentrate. Severity: **MODERATE**.

**Lipid-medicine specialist.** Using untreated/imputed LDL-C here while SAFEHEART uses measured LDL-C is faithful to each paper and makes the two comparisons non-exchangeable. Severity: **MODERATE**.

**Evidence check.** FH-Risk-Score local extract: excluded under 18 and over 65; LDL-C untreated 57% or imputed 43%; UKB n=499.

**Required improvement.** Add a three-way complete-input subset or explicitly forbid ranking the three deltas against each other.

**Suggested replacement wording.** “Each comparator was scored on its own complete-input subset. The three UK Biobank deltas are therefore not a single paired contest on identical participants.”

**Editor-in-Chief adjudication.** **MAJOR.**

---

### Methods — Comparator implementation (Montreal-FH-SCORE)

**Current claim.** Points chart with ever smoking; designed for prevalent CVD; used here only as incident ranking, not as a probability model.

**Biostatistician.** This is an estimand mismatch. Discrimination can still be computed; “higher C” is not “better Montreal.” Severity: **MAJOR**.

**Cardiologist.** Using a prevalent-disease score as an incident comparator will systematically flatter any incident Cox model that includes age and sex. Severity: **MAJOR**.

**Lipid-medicine specialist.** Montreal omitted LDL-C because off-treatment lipids and age were thought to capture exposure. Evaluating it on treated UK Biobank lipids for **incident** events is not the Montreal experiment. Severity: **MAJOR**.

**Evidence check.** ACC/AHA 2026 local extract: Montreal derived from cross-sectional LDLR-variant French-Canadians, identifying **prevalent** ASCVD. Primary Montreal papers: **UNVERIFIED — DO NOT CITE** this runtime.

**Required improvement.** Demote Montreal to a secondary, different-estimand benchmark. Remove it from the confirmatory Holm family.

**Suggested replacement wording.** “Montreal-FH-SCORE was evaluated only as an incident-ranking benchmark. It was not a like-for-like incident-ASCVD model, and a difference in C is not evidence that CALON-C outperforms Montreal for Montreal’s original task.”

**Editor-in-Chief adjudication.** **MAJOR.** I would take Montreal out of the six-cell family.

---

### Methods — Comparator implementation (Lp(a) conversion and missingness)

**Current claim.** UK Biobank Lp(a) nmol/L divided by 2.15 to approximate mg/dL; divisor not in comparator papers; strict complete-input; Lp(a)-omitted labelled incomplete; no missing input assigned to a favourable category.

**Biostatistician.** Strict complete-input is the correct missing-data policy for published scores. Conversion 2.15 is an unvalidated measurement-error model. Severity: **MODERATE**.

**Cardiologist.** Complete-input subsets select for people who received Lp(a) testing, a possible collider. Severity: **MODERATE**.

**Lipid-medicine specialist.** nmol/L to mg/dL is isoform-dependent; 2.15 is not a gold standard (2.4 and particle-specific conversions are commonly discussed). Threshold 50 mg/dL after crude division can misclassify. The results file says the delta moves only 0.0005 — that bounds **this dataset’s** sensitivity, not the measurement claim. Severity: **MODERATE**.

**Evidence check.** **Insufficient validated in-window evidence** in this runtime for 2.15 as a universal factor. SAFEHEART/FH-RS thresholds are in mg/dL in the local extracts.

**Required improvement.** Keep the assumption flag. Do not call the strict implementation “PDF-faithful” without the conversion caveat (the results file already forbids this).

**Suggested replacement wording.** “Lp(a) in nmol/L was divided by 2.15 to apply mg/dL thresholds. That divisor is not printed in the comparator papers and is an assumption.”

**Editor-in-Chief adjudication.** **MODERATE.** This paragraph is one of the better methods disclosures.

---

### Methods — Head-to-head and multiplicity ¶1

**Current claim.** Common complete-input subset; paired cluster bootstrap B=2,000; win only if CI excludes 0; positive point estimate with CI crossing 0 is a TIE; strata with <10 events not estimated.

**Biostatistician.** Sign convention and TIE rule are correct. Cluster bootstrap in UK Biobank without a cluster variable is just a paired bootstrap. Severity: **MINOR**.

**Cardiologist.** A C difference of 0.03–0.07 without net benefit is not a clinical win. Severity: **MODERATE**.

**Lipid-medicine specialist.** Agree with the TIE rule; later text mostly obeys it. Severity: **MINOR**.

**Evidence check.** Methodological standards for paired C differences: **UNVERIFIED** this runtime.

**Required improvement.** Say UK Biobank bootstrap is paired, not clustered.

**Suggested replacement wording.** “A comparison was a win only when the 95% interval excluded 0. A positive point estimate with an interval crossing 0 was a TIE.”

**Editor-in-Chief adjudication.** **MINOR.** Keep the TIE rule exactly as written.

---

### Methods — Head-to-head and multiplicity ¶2

**Current claim.** Confirmatory family = three UK Biobank comparators × full and 5-year = six cells, Holm-controlled; 10-year, Lp(a)-omitted, Welsh, and variable-set refits exploratory; refits are ablations not validations.

**Biostatistician.** Holm on six cells is coherent. The family still includes Montreal (wrong estimand) and full-follow-up SAFEHEART (wrong horizon). Variable-set refits correctly labelled. Severity: **MAJOR**.

**Cardiologist.** Five-year should have been the SAFEHEART primary, not an equal sibling of full follow-up. Severity: **MAJOR**.

**Lipid-medicine specialist.** Ablations that refit CALON variables versus comparator variables will favour whichever specification was tuned in this programme. Severity: **MODERATE**.

**Evidence check.** No in-window verified paper requires Holm rather than another FWER method; Holm is acceptable. The issue is family membership, not the algorithm.

**Required improvement.** Re-declare the confirmatory family as FH-Risk-Score (incident, 10-year, ≤65) plus SAFEHEART at 5 years, with Montreal exploratory.

**Suggested replacement wording.** “The confirmatory family should be restricted to incident-ASCVD instruments at their published horizons. Montreal and off-horizon comparisons are exploratory.”

**Editor-in-Chief adjudication.** **MAJOR.**

---

### Methods — Calibration, equation, and transport ¶1–2

**Current claim.** Raw-unit equation with S0(5)=0.975645 and S0(10)=0.949962; internal slope, E:O, Brier, deciles; reviewer response required out-of-fold/external baseline before transportable absolute risk; calibration reported as internal only.

**Biostatistician.** Withdrawing external-calibration language is correct. Publishing the baseline survival **in the main equation table** still invites use. Apparent calibration with slope CI 0.884–1.318 is compatible with both modest overfitting and modest underfitting — a **TIE** around 1, not “acceptable agreement” later in Results. Severity: **MAJOR**.

**Cardiologist.** An equation that emits 30% 10-year risk for a worked “high-risk” profile, without competing death, will be misused. Severity: **FATAL**.

**Lipid-medicine specialist.** S0 from a volunteer cohort will understate clinic-FH absolute risk even if ranking holds (McKay-type failure). McKay 2022 remains **UNVERIFIED** here. Severity: **MAJOR**.

**Evidence check.** Equation JSON matches the printed S0 and lp_mean 4.217739. Age term HR 1.022, CI 0.99968–1.0458, p=0.053 — Table 2 rounds the lower bound to 1.000.

**Required improvement.** Move the absolute-risk formula to a supplement labelled “internal arithmetic only.” Unround Table 2 CIs. Do not say “acceptable internal agreement.”

**Suggested replacement wording.** “Absolute-risk formulae are internal arithmetic checks. They are not for clinical use and are not competing-risk estimates.”

**Editor-in-Chief adjudication.** **FATAL** if Table 2 remains presented as a usable risk equation.

---

### Methods — Calibration, equation, and transport ¶3

**Current claim.** Frozen source-cohort equation and preprocessing applied without refitting; UK Biobank nine-term → Wales; Wales seven-term → UK Biobank; these are transport estimates, not untouched independent validations.

**Biostatistician.** Asymmetric term sets mean this is not reciprocal transport of one model. Prior programme use of both datasets is leakage of design, not of rows. Severity: **MAJOR**.

**Cardiologist.** Agree it is not validation. Severity: **MINOR** (label is honest).

**Lipid-medicine specialist.** Applying a volunteer-derived baseline-free ranking to a treated clinic registry tests case mix more than biology. Severity: **MODERATE**.

**Evidence check.** TRIPOD+AI external validation items: **UNVERIFIED** as citation; the text already avoids the banned phrase.

**Required improvement.** Title the section “asymmetric frozen-equation application,” not reciprocal transport, unless the same nine terms are used both ways.

**Suggested replacement wording.** “The nine-term UK Biobank equation was applied frozen to Wales. Separately, a seven-term Welsh re-estimation was applied frozen to UK Biobank. These are not reciprocal tests of one model and not independent external validation.”

**Editor-in-Chief adjudication.** **MAJOR.**

---

### Methods — Proportional hazards, competing risk, and sensitivity ¶1–2

**Current claim.** Rank-transformed Schoenfeld tests; Aalen–Johansen where death exists; Welsh CIF executed; UK Biobank arm did not because `death` was absent; sensitivities listed; ambiguous-date restriction is not a clean sensitivity.

**Biostatistician.** Failed UK Biobank competing-risk analysis is a code-guard error, not a data absence in the raw UK Biobank death fields known to this programme. Schoenfeld p>0.05 in 16 terms does not prove PH; Wales `sp50` p=0.080 is a near miss. Severity: **MAJOR**.

**Cardiologist.** In middle-aged FH, competing death is smaller than in older unselected cohorts, but still required for 10-year percentages. Severity: **MAJOR**.

**Lipid-medicine specialist.** Cause-specific ranking can remain meaningful; absolute risk cannot. Severity: **MODERATE**.

**Evidence check.** `calon_c_corrected.json` PH list: 9 UK Biobank + 7 Wales terms, none with p<0.05. CIF 6.02%/11.97%, 35 competing deaths, n_events=102.

**Required improvement.** Run the UK Biobank competing-risk analysis before any absolute-risk display. Describe 16 tests as two models, not one.

**Suggested replacement wording.** “No term in the nine-term UK Biobank model or the seven-term Welsh model had a Schoenfeld p<0.05. The UK Biobank competing-risk analysis did not execute and is outstanding.”

**Editor-in-Chief adjudication.** **MAJOR.**

---

### Methods — Grey-zone and subgroup analyses ¶1–2

**Current claim.** Predecessor CALON-F 5–20% 10-year band tested Lp(a) and log(apoB/LDL-C); ancillary only; no CALON-C subgroup table; no interactions.

**Biostatistician.** Grey-zone selection on predicted risk truncates linear-predictor variance; C≈0.59 is expected, and “no gain” is weakly informative. Absence of corrected subgroups is a TRIPOD fairness failure. Severity: **MAJOR**.

**Cardiologist.** 5–20% is not a validated FH decision band. Severity: **MAJOR**.

**Lipid-medicine specialist.** Testing apoB/LDL-C in a predecessor model with `log_tghdl` rather than CALON-C’s `tg_filter` is a different specification (`grey_zone_enhancers.json`). Severity: **MODERATE**.

**Evidence check.** JSON: base terms include `htn_any` and `log_tghdl`, not the CALON-C set; n_scored=3,333 vs development 3,209.

**Required improvement.** Move grey-zone to supplement or delete. Do not put it in Key points.

**Suggested replacement wording.** “No corrected CALON-C grey-zone or subgroup analysis exists. The predecessor analysis is not reported as a CALON-C result.”

**Editor-in-Chief adjudication.** **MAJOR** as currently placed in Key points/Results; **MINOR** if demoted.

---

### Methods — Literature verification ¶1

**Current claim.** Coefficients checked against primary PDFs; background checked against a deep-research ledger, SciSpace/Elicit tables, DOI records, PubMed on 16 August 2026; Scite not callable; Perplexity authentication error; not a systematic review.

**Biostatistician.** A methods paragraph cannot certify literature that this submission does not reproduce. Severity: **MODERATE**.

**Cardiologist.** Irrelevant to care. Severity: **MINOR**.

**Lipid-medicine specialist.** If SciSpace/Elicit tables are not in the package, the sentence is unauditable. Severity: **MODERATE**.

**Evidence check.** This runtime: Scite/SciSpace/Elicit **NOT EXPOSED**; PubMed/Crossref/WebSearch **did not return** (calls rejected). Local PDFs verify a subset only.

**Required improvement.** Cite only papers with a packaged PDF or a resolved DOI log in the submission.

**Suggested replacement wording.** “Comparator coefficients were checked against the primary PDFs in the local extract set. No PRISMA claim is made.”

**Editor-in-Chief adjudication.** **MODERATE.**

---

### Results — Study populations ¶1 (UK Biobank)

**Current claim.** 3,209 participants, 289 events, 6.55/1,000 person-years from **pre-correction** descriptive output; Table 1 demographics; cases older, more male, hypertensive, diabetic; untreated-equivalent non-HDL-C 5.12 vs 4.70 mmol/L.

**Biostatistician.** Mixing a corrected risk set with a pre-correction event rate is a provenance error. SMDs are unadjusted. Severity: **MAJOR**.

**Cardiologist.** 10.2% current smoking and 9.8% diabetes are plausible; 52.4% hypertension by the loose definition is high and will dominate ranking. Severity: **MODERATE**.

**Lipid-medicine specialist.** Median untreated-equivalent LDL-C 3.95 mmol/L is incompatible with untreated HeFH and compatible with a treated, loosely defined carrier flag. That is the central phenotypic fact. Severity: **FATAL** for HeFH translation.

**Evidence check.** Table 1 source `desc_table1.csv` as claimed. Phenotype contrast with FH-Risk-Score derivation LDL-C 6.65 mmol/L (untreated/imputed) is from the local *ATVB* extract.

**Required improvement.** Do not report 6.55/1,000 PY until regenerated. State LDL-C against clinic-FH benchmarks.

**Suggested replacement wording.** “Median untreated-equivalent LDL-C was 3.95 mmol/L. This lipid distribution does not resemble untreated heterozygous FH derivation cohorts.”

**Editor-in-Chief adjudication.** **FATAL** for any remaining HeFH framing in Results.

---

### Results — Study populations ¶2 (Wales)

**Current claim.** Corrected 1,169/102 after reinstating 10 events; preceding descriptive output not presented as corrected; corrected Welsh Table 1 required before submission.

**Biostatistician.** Correct disclosure. Tables 3 and 5 then violate it. Severity: **MAJOR**.

**Cardiologist.** A clinical paper without a corrected Table 1 for the transport cohort is incomplete. Severity: **MAJOR**.

**Lipid-medicine specialist.** Without corrected lipids, readers cannot judge whether Wales is true FH and UK Biobank is not. Severity: **MAJOR**.

**Evidence check.** Internal consistency only.

**Required improvement.** Either regenerate Table 1 or omit all Welsh numerical performance.

**Suggested replacement wording.** “A corrected Welsh Table 1 was not available. No Welsh baseline lipid or comorbidity distribution is reported as a CALON-C result.”

**Editor-in-Chief adjudication.** **MAJOR.**

---

### Results — Predictor-level associations ¶1

**Current claim.** Diabetes HR 2.120 (1.610–2.793); male 1.702 (1.372–2.111); hypertension 1.610 (1.279–2.028); smoking 1.329 (0.959–1.842) **TIE**; all three lipid terms **TIE**s.

**Biostatistician.** Correct that lipids are not independently significant. Age is also a TIE: 1.022 (0.9997–1.046), p=0.053; Table 2’s 1.000–1.046 conceals this. Ridge HRs are shrunk; Wald-type CIs after ridge are not fully honest. Severity: **MAJOR**.

**Cardiologist.** Diabetes dominating near-term ranking in a lipid disorder is clinically expected once everyone is lipid-selected. It does not reduce the indication for LDL lowering. Severity: **MINOR** if verbs stay associational.

**Lipid-medicine specialist.** This is the paper’s most important scientific result and should lead the Results, not sit as an embarrassment. Within a high-LDL-ascertainment stratum, classical risk factors rank events; on-treatment lipid mass does not. That is **not** evidence against LDL causality. Severity: **MODERATE** (interpretation later).

**Evidence check.** `calon_c_equation.json` confirms all quoted HRs; age lower bound 0.99968.

**Required improvement.** Unround age. State ridge CIs are approximate. Do not call diabetes “largest clinical association” without noting age/sp50 splitting.

**Suggested replacement wording.** “After ridge penalisation, diabetes, male sex, and hypertension were associated with incident ASCVD. Current smoking and all three lipid-derived terms were TIEs. Age per year was 1.022 (0.9997 to 1.046), also a TIE.”

**Editor-in-Chief adjudication.** **MAJOR** for the rounded age CI.

---

### Results — Predictor-level associations ¶2 (incremental C)

**Current claim.** Versus age-and-sex, CALON-C added +0.041; hypertension, diabetes, and smoking ~+0.033; lipid apparatus ~+0.008.

**Biostatistician.** `htn_isolation.json` is a **different** decomposition: 6-term base (age, sp50, male, three lipids) C=0.676, then +htn 0.0148, +dm 0.0214, +smoke 0.0032 (=+0.0394). Sequential increments are path-dependent. “Approximately +0.033 / +0.008” is not uniquely recoverable from the cited file. Severity: **MAJOR**.

**Cardiologist.** If true, the model is a clinical-risk score, which is still potentially useful — but then stop branding it as a lipid-exposure model. Severity: **MODERATE**.

**Lipid-medicine specialist.** +0.008 is a TIE-sized increment and should be labelled as such unless it has a CI. Severity: **MAJOR**.

**Evidence check.** File mismatch as above. No CI on the +0.008.

**Required improvement.** Publish one pre-specified nested-model table with CIs on delta C, or delete the 0.033/0.008 split.

**Suggested replacement wording.** “Nested-model increments were not accompanied by confidence intervals in the corrected package and are not reported as primary results.”

**Editor-in-Chief adjudication.** **MAJOR.**

---

### Results — Internal discrimination ¶1–2

**Current claim.** UK Biobank OOF C 0.7081 / 0.7043 / 0.7254; optimism-corrected 0.7095 / 0.7079 / 0.7336; Welsh pre-rescue optimism-corrected 0.7653 / 0.7605 / 0.7590, stated unchanged after 10 rescued events but not resynchronised.

**Biostatistician.** UK Biobank internal C is coherent across estimators. Higher 5-year C with only 97 events is the usual short-horizon artefact. Welsh “unchanged” without a new file is an unverifiable assertion. Severity: **MAJOR**.

**Cardiologist.** C 0.71 is modest for individual counselling. Severity: **MODERATE**.

**Lipid-medicine specialist.** Welsh C 0.76 with contaminated predictors is not a better model; it may be leakage. Severity: **MAJOR**.

**Evidence check.** `calon_apparent.json` matches UK Biobank figures.

**Required improvement.** Delete Welsh C from Table 3 until regenerated. Call 5-year C exploratory because of EPV.

**Suggested replacement wording.** “UK Biobank optimism-corrected C was 0.7095 over full follow-up. Welsh internal C from the pre-rescue frame is not reported as a corrected result.”

**Editor-in-Chief adjudication.** **MAJOR.**

---

### Results — Head-to-head ¶1 (UK Biobank full follow-up)

**Current claim.** SAFEHEART subset 2,470/221: 0.7003 vs 0.6308, +0.070 (0.036–0.104; Holm p=0.0003); Montreal 2,811/252: 0.7070 vs 0.6746, +0.032 (0.011–0.055; p=0.0179); FH-Risk-Score 1,913/146: 0.6983 vs 0.6836, +0.015 (−0.011 to 0.040; p=0.5018) TIE.

**Biostatistician.** Arithmetic and Holm labels match the corrected JSON. Different subsets; CALON-C C itself moves (0.7003 vs 0.7070 vs 0.6983), so part of each delta is sample composition. FH-Risk-Score is a TIE. Severity: **MODERATE**.

**Cardiologist.** SAFEHEART C=0.6308 is poor because the score is being used off-label (no prior ASCVD, treated LDL, volunteer FH-flag). The +0.070 is not a reason to replace SAFEHEART in Spanish molecular FH. Severity: **MAJOR**.

**Lipid-medicine specialist.** The only like-for-like incident primary-prevention comparator is FH-Risk-Score, and it is a TIE — including 499 overlapping UK Biobank participants that should, if anything, **help** FH-Risk-Score. A TIE despite that overlap is not a win. Severity: **MAJOR**.

**Evidence check.** SAFEHEART derivation C 0.81 in primary prevention (local extract) versus 0.6308 here: population/ascertainment/endpoint-driven disagreement, not a proof that SAFEHEART was miscoded.

**Required improvement.** Lead with the FH-Risk-Score TIE. Report a three-way complete-case subset. State overlap may bias the TIE toward FH-Risk-Score.

**Suggested replacement wording.** “On the incident primary-prevention instrument designed for this task, FH-Risk-Score, the difference was a TIE: +0.015 (−0.011 to 0.040). Larger differences versus SAFEHEART-RE and Montreal-FH-SCORE were observed on different evaluable subsets and different estimands.”

**Editor-in-Chief adjudication.** **MAJOR.** Abstract order currently buries the TIE.

---

### Results — Head-to-head ¶2 (SAFEHEART LDL correction)

**Current claim.** Switching SAFEHEART from untreated to measured LDL-C moved the delta from +0.032 to +0.070, i.e. against CALON-C’s earlier implementation; untreated LDL retained as comparator-favourable sensitivity.

**Biostatistician.** Direction is the right honesty test. Both numbers cannot be “the” SAFEHEART result; the published specification is measured LDL. Severity: **MINOR**.

**Cardiologist.** Even the comparator-favourable sensitivity is not the clinical SAFEHEART use-case. Severity: **MODERATE**.

**Lipid-medicine specialist.** Measured on-treatment LDL-C **should** weaken SAFEHEART if the original coefficient was estimated in a differently treated registry. That is pharmacology, not a win. Severity: **MODERATE**.

**Evidence check.** Local Table 3 supports measured LDL-C as the multivariable term.

**Required improvement.** Keep both deltas in a supplement table. Do not let +0.070 become the only remembered number.

**Suggested replacement wording.** “Applying the published measured-LDL-C input increased the SAFEHEART difference from +0.032 to +0.070. The larger difference therefore reflects specification fidelity in a treated volunteer sample, not discovery of hidden superiority.”

**Editor-in-Chief adjudication.** **MODERATE.**

---

### Results — Head-to-head ¶3 (five-year)

**Current claim.** Nominal 5-year differences versus SAFEHEART +0.081 (0.020–0.150) and Montreal +0.044 (0.003–0.090) did not survive Holm (p=0.0560 and 0.1413); FH-Risk-Score +0.018 (−0.032 to 0.069); no 5-year superiority retained.

**Biostatistician.** Correct. Holm p=0.0560 is a TIE, not “borderline significance.” Severity: **MINOR** (keep).

**Cardiologist.** This is the horizon that matches SAFEHEART; it is a TIE. The abstract still headlines full-follow-up SAFEHEART. Severity: **MAJOR**.

**Lipid-medicine specialist.** Agree with the cardiologist. Severity: **MAJOR**.

**Evidence check.** `RESULTS_FINAL_CORRECTED.md` confirmatory table.

**Required improvement.** If SAFEHEART remains a confirmatory comparator, the 5-year TIE is the primary SAFEHEART result.

**Suggested replacement wording.** “At five years, the published SAFEHEART-RE horizon, all three comparisons were TIEs after Holm correction.”

**Editor-in-Chief adjudication.** **MAJOR.**

---

### Results — Head-to-head ¶4 (Wales)

**Current claim.** Strict SAFEHEART 40/1 and FH-RS 132/6 not estimable; Montreal 750/60 +0.033 (−0.014 to 0.090) TIE; Lp(a)-omitted all TIEs; no external head-to-head win.

**Biostatistician.** <10 events correctly blocked strict scores. Montreal TIE is the only strict Welsh number. Severity: **MINOR**.

**Cardiologist.** Non-evaluability is an implementation finding, not inferiority of SAFEHEART. The paper says this later; keep it here. Severity: **MINOR**.

**Lipid-medicine specialist.** BMI missingness 54.5% killing SAFEHEART is a registry data-quality result. Severity: **MINOR**.

**Evidence check.** Corrected results file.

**Required improvement.** None beyond keeping “not estimable ≠ worse score.”

**Suggested replacement wording.** Already adequate if the later missingness paragraph stays.

**Editor-in-Chief adjudication.** **MINOR.**

---

### Results — Head-to-head ¶5 (tally / non-inferiority)

**Current claim.** Across every strict and Lp(a)-omitted cell, no comparator significantly outperformed CALON-C; this is not proof of universal non-inferiority.

**Biostatistician.** The first sentence is a stealth non-inferiority claim; the second sentence tries to retract it. Absence of a significant loss is not a finding. Multiple exploratory cells inflate the tally. Severity: **MAJOR**.

**Cardiologist.** Agree; delete the tally sentence from Results. Severity: **MAJOR**.

**Lipid-medicine specialist.** Agree. Severity: **MAJOR**.

**Evidence check.** No non-inferiority margin exists in the methods.

**Required improvement.** Delete the tally. Report the six confirmatory cells only.

**Suggested replacement wording.** “Formal non-inferiority was not tested.”

**Editor-in-Chief adjudication.** **MAJOR.** Delete.

---

### Results — Calibration and model equation ¶1–3

**Current claim.** Internal 10-year slope 1.101 (0.884–1.318), E:O 1.008 (0.883–1.153), predicted 6.20% vs KM 6.15%; 5-year slope 1.197 (0.900–1.494); scaled Brier 3.3%/1.8%; lowest 5-year decile had 0 events; worked examples 0.78%/1.62% and 15.99%/30.42%; no validated risk category.

**Biostatistician.** Slope CIs include 1 and also include 0.88 and 1.32 — **inconclusive**, not “acceptable.” Decile 1 with 0/321 events at 5 years makes a 10-decile plot theatre. Brier scaled 3.3% needs the unscaled Brier beside it (JSON unscaled 5-year Brier ≈0.029). Severity: **MAJOR**.

**Cardiologist.** A worked example of 30% 10-year risk without competing death is a patient-safety problem if printed as an equation. Severity: **FATAL**.

**Lipid-medicine specialist.** KM 6.15% 10-year in “FH” adults aged 57 is far below clinic HeFH expectations and is the healthy-volunteer plus treatment signature. Severity: **MAJOR**.

**Evidence check.** Calibration JSON matches. FH-Risk-Score derivation had substantial 10-year event separation by score group (local extract HRs 5.52 for ASCVD-free survival) in a higher-risk lipid distribution.

**Required improvement.** Remove “acceptable.” Move worked examples to supplement as arithmetic tests. Do not print 30% as a headline.

**Suggested replacement wording.** “Internal calibration slope CIs included 1 and were wide. These plots do not establish transported calibration or clinically usable absolute risks.”

**Editor-in-Chief adjudication.** **FATAL** for the usable-equation presentation; **MAJOR** for “acceptable.”

---

### Results — Reciprocal transport ¶1–2

**Current claim.** Frozen nine-term UK Biobank equation: C=0.7252 in Wales; frozen seven-term Welsh equation: C=0.6600 in UK Biobank; not the same equation independently validated; removing undated fields reduced Welsh C by ~0.030 in an earlier frame.

**Biostatistician.** Asymmetry is partly mechanical (9 vs 7 terms, different endpoints, contaminated predictors). The ~0.030 bound is from an earlier frame and is not a CI. Transport C source includes `calon_c.json` (pre-correction pipeline) while n is corrected — synchronisation risk. Severity: **MAJOR**.

**Cardiologist.** C=0.725 under post-event BP in 55/92 events is not transport of baseline risk. Severity: **MAJOR**.

**Lipid-medicine specialist.** Reverse C=0.660 says a clinic-derived 7-term model ranks volunteer carriers poorly, which is expected if lipids and diabetes prevalence differ. Severity: **MODERATE**.

**Evidence check.** `transport_s1_fixed.json` C_independent 0.725204. Welsh dated-only 0.030 from methods file, not regenerated.

**Required improvement.** Do not put 0.725 in the abstract Findings without the timing bound. Apply the same nine terms both directions or stop saying reciprocal.

**Suggested replacement wording.** “The nine-term UK Biobank equation ranked Welsh participants with C=0.7252 under incompletely dated predictors. This is not independent external validation.”

**Editor-in-Chief adjudication.** **MAJOR.**

---

### Results — Proportional hazards and competing risk ¶1–2

**Current claim.** 0/16 PH violations; Welsh AJ CIF 6.02%/11.97% with 35 competing deaths among 102 events; UK Biobank competing-risk analysis did not execute; absolute-risk interpretation in UK Biobank incomplete.

**Biostatistician.** “35 competing deaths among 102 events” is easy to misread as 35 of the 102 being deaths; they are competing deaths **in the cohort**, not a subset of ASCVD events. Severity: **MAJOR** (wording).

**Cardiologist.** Incomplete UK Biobank absolute risk is correctly stated and should have blocked Table 2. Severity: **MAJOR**.

**Lipid-medicine specialist.** CIF 12% at 10 years in a genotype-positive clinic registry is clinically more plausible than UK Biobank KM 6%. That gap is ascertainment, not model quality. Severity: **MODERATE**.

**Evidence check.** JSON: n_competing_deaths=35, n_events=102, separate fields.

**Required improvement.** Rephrase competing deaths. Delete UK Biobank S0 until CIF exists.

**Suggested replacement wording.** “There were 35 competing deaths in the Welsh risk set used for Aalen–Johansen estimates, alongside 102 first ASCVD events. UK Biobank competing-risk cumulative incidence is not available.”

**Editor-in-Chief adjudication.** **MAJOR.**

---

### Results — Missing data ¶1

**Current claim.** UK Biobank missingness limited for age/clinical variables; 12.4% non-HDL/HDL-derived, 5.0% tg_filter, 22.5% Lp(a); missingness indicators not associated with outcome; Wales BMI 54.5%, diabetes 41.6%, smoking 26.4%, native Lp(a) unusable; non-evaluability is implementation, not intrinsic inferiority.

**Biostatistician.** “Indicators not significantly associated with outcome” does not prove MCAR and does not justify median imputation. Welsh missingness from pre-correction descriptive output. Severity: **MODERATE**.

**Cardiologist.** Implementation non-evaluability is the one result that could matter to health systems — if Wales were a typical clinic EHR. Severity: **MINOR**.

**Lipid-medicine specialist.** Mixed-unit Lp(a) is a laboratory-governance finding. Severity: **MINOR**.

**Evidence check.** Table 1 missingness column matches these UK Biobank percentages.

**Required improvement.** Label Welsh missingness as pre-correction. Do not over-interpret null missingness–outcome tests.

**Suggested replacement wording.** Keep the implementation sentence; add “Welsh missingness percentages predate the 10-event correction.”

**Editor-in-Chief adjudication.** **MODERATE.**

---

### Results — Grey-zone ¶1–2

**Current claim.** Predecessor analysis, 3,333 scored, 1,685/218 in band; Lp(a) delta C −0.0038 (−0.0089 to 0.0018); apoB/LDL-C +0.0146 (−0.0050 to 0.0330); both +0.0118 (−0.0088 to 0.0324); apoB/LDL-C HR 1.154 (1.027–1.295); Lp(a) HR 1.033 (0.923–1.157); not a CALON-C enhancer validation.

**Biostatistician.** All C deltas are TIEs. Association without ranking gain is correctly described. Band restriction biases against detecting incremental C. Severity: **MODERATE**.

**Cardiologist.** Cannot inform whether to order Lp(a) — guideline already says measure once. Severity: **MAJOR** if used translationally.

**Lipid-medicine specialist.** Lp(a) HR TIE in a mild-phenotype volunteer carrier flag does not challenge Lp(a) risk in HeFH or in the general population. Severity: **MAJOR**.

**Evidence check.** JSON matches. ACC/AHA 2026 still COR 1 for Lp(a) measurement.

**Required improvement.** If retained, state that a TIE for incremental C in a truncated band is not evidence against measuring Lp(a).Continuing from the grey-zone result, then the remaining Discussion, whole-manuscript analyses, tool status, evidence ledger, and claims that must be deleted.

---

### Results — Grey-zone ¶2 (translational reading)

**Current claim.** The predecessor analysis does not validate a CALON-C enhancer; specialised biomarkers should not be added merely because they are biologically plausible.

**Biostatistician.** The second sentence is a general methods slogan, not a result. Incremental C TIEs in a variance-truncated band cannot support a biomarker policy. Severity: **MODERATE**.

**Cardiologist.** ACC/AHA 2026 already recommends measuring Lp(a) once in all adults. This paragraph must not be quoted against that. Severity: **MAJOR**.

**Lipid-medicine specialist.** ApoB/LDL-C was associated with events (HR 1.154 per SD, 1.027–1.295) but did not move C. That is expected when the base model already contains correlated lipid information. It is not evidence that particle number is irrelevant in HeFH. Severity: **MAJOR**.

**Evidence check.** Local ACC/AHA 2026 extract: Lp(a) measurement in all adults, COR 1. Grey-zone JSON matches the numeric TIEs.

**Required improvement.** Delete the policy sentence. If the analysis is kept, say only that incremental C was a TIE in a predecessor band.

**Suggested replacement wording.** “Within a predecessor 5–20% predicted-risk band, adding Lp(a) or log(apoB/LDL-C) did not change C (all intervals crossed 0). This is not a test of whether those assays should be measured in heterozygous FH.”

**Editor-in-Chief adjudication.** **MAJOR.**

---

### Results — Subgroups ¶1

**Current claim.** No corrected CALON-C subgroup dataset was supplied; earlier files cannot be merged; no interactions were tested; absence is reported as a source gap.

**Biostatistician.** Honest. TRIPOD+AI still fails on fairness/subgroups. Severity: **MAJOR** as a reporting gap, not as spin.

**Cardiologist.** Sex and diabetes interactions are clinically obligatory in an FH-adjacent score. Severity: **MAJOR**.

**Lipid-medicine specialist.** Treatment-by-lipid interaction is the question the lipid terms need, and it was not done. Severity: **MAJOR**.

**Evidence check.** Insufficient validated evidence in-window is not required; this is an internal omission.

**Required improvement.** Either produce corrected subgroups or state in the abstract that none exist.

**Suggested replacement wording.** Keep as written, and add the same sentence to the abstract limitations.

**Editor-in-Chief adjudication.** **MAJOR.**

---

### Discussion — Principal findings ¶1

**Current claim.** Four findings: moderate internal discrimination; better full-follow-up C than SAFEHEART-RE and Montreal after Holm, TIE with FH-Risk-Score; ranking retained on transport to Wales, not independent validation; specialised biomarkers did not significantly improve grey-zone C.

**Biostatistician.** Finding 2 still privileges full follow-up over the 5-year TIE. Finding 3 overstates “retained ranking” given predictor timing. Finding 4 is not a CALON-C result. Severity: **MAJOR**.

**Cardiologist.** Four findings is too many for the evidence. The only defensible pair is modest internal C plus an FH-Risk-Score TIE. Severity: **MAJOR**.

**Lipid-medicine specialist.** Finding 1 should include that lipid terms were TIEs. Severity: **MAJOR**.

**Evidence check.** Same ledger as Results. ACC/AHA 2026 does not license clinical adoption (the next paragraph partly says this).

**Required improvement.** Reorder: internal C; lipid terms TIE; FH-Risk-Score TIE; off-estimand comparator deltas; transport as a stress test; grey-zone demoted.

**Suggested replacement wording.** “CALON-C showed moderate internal discrimination in a UK Biobank `ldlr_carrier` cohort. Adjusted lipid-derived terms were TIEs. On the incident primary-prevention comparator designed for this task, the difference versus FH-Risk-Score was a TIE. Larger full-follow-up differences versus SAFEHEART-RE and Montreal-FH-SCORE were observed on different subsets and estimands. Frozen application to Wales is not independent external validation.”

**Editor-in-Chief adjudication.** **MAJOR.**

---

### Discussion — Principal findings ¶2

**Current claim.** Findings are narrower but more credible; CALON-C does not beat every comparator, has no confirmatory 5-year superiority, and has no Welsh head-to-head advantage; comparator corrections moved in both directions.

**Biostatistician.** This is the correct credibility paragraph. Severity: **MINOR** (keep).

**Cardiologist.** Agree. Severity: **MINOR**.

**Lipid-medicine specialist.** Agree, provided “more credible” is not used as a novelty claim. Severity: **MINOR**.

**Evidence check.** Internal corrections documented in `RESULTS_FINAL_CORRECTED.md`.

**Required improvement.** None beyond not letting paragraph 1 undo this one.

**Suggested replacement wording.** Keep.

**Editor-in-Chief adjudication.** **MINOR.** This is the paper’s best discussion paragraph.

---

### Discussion — What is genuinely new ¶1

**Current claim.** Novelty is incremental: not first FH model, not first cumulative cholesterol, not first UK Biobank contribution, not first SAFEHEART external evaluation; cites FH-Risk-Score UKB n=499, REFERCHOL, English routine care, Australian genetically confirmed evaluation.

**Biostatistician.** Correctly rejects paradigm-shift language. Australian paper remains **UNVERIFIED — DO NOT CITE** in this runtime. Severity: **MODERATE**.

**Cardiologist.** Agree it is not clinically new. Severity: **MINOR**.

**Lipid-medicine specialist.** “Not the first use of cumulative cholesterol exposure” is still too generous to CALON-C, because `log(non-HDL × age)` is not cumulative exposure. Severity: **MAJOR**.

**Evidence check.** FH-Risk-Score UKB n=499 verified from local *ATVB* extract. REFERCHOL, McKay, Tamehri: **UNVERIFIED — DO NOT CITE** here.

**Required improvement.** Delete unverified C-statistics. Do not call the CALON-C term cumulative exposure even in a negative novelty sentence.

**Suggested replacement wording.** “CALON-C is not the first FH-adjacent risk model and not an independent UK Biobank validation of FH-Risk-Score, which already included 499 UK Biobank participants.”

**Editor-in-Chief adjudication.** **MAJOR** for residual “cumulative” language and unverified ref 9.

---

### Discussion — What is genuinely new ¶2

**Current claim.** Defensible contribution is common-data, comparator-faithful evaluation in a population-based UK LDLR-carrier frame, plus a parsimonious no-Lp(a) model; priority claim is first identified head-to-head of CALON-C and the three instruments in the present corrected UK Biobank carrier frame, to be rechecked before submission.

**Biostatistician.** “First identified head-to-head of CALON-C and the three instruments” is tautological: CALON-C did not exist elsewhere. Residual novelty is a three-score common-data comparison in a carrier-flag cohort, which is incremental. Severity: **MAJOR**.

**Cardiologist.** Parsimony is not novelty once FH-Risk-Score already exists as a 7-variable chart. Severity: **MODERATE**.

**Lipid-medicine specialist.** Population-based LDLR-carrier frame is the actual setting novelty — and it is a **limitation** for translating to HeFH, not a selling point. Severity: **MAJOR**.

**Evidence check.** Local novelty note from 10 August 2026 (programme search, not this runtime) already forbade “first” language for reciprocal clinic–biobank validation. That older search also claimed reciprocal validation with calibration; the present manuscript does **not** report transported calibration, so even that bounded claim is stronger than the data.

**Required improvement.** Delete “first identified.” State: common-data ranking comparison in a carrier-flag cohort, with explicit non-independence.

**Suggested replacement wording.** “The contribution is a complete-input, multiplicity-controlled ranking comparison of a routine-variable Cox model with three published FH instruments in a UK Biobank `ldlr_carrier` frame. It is not a first external validation of those instruments and not a clinic-HeFH model.”

**Editor-in-Chief adjudication.** **MAJOR.** Tautological priority claims are rejected as unsupported.

---

### Discussion — Comparison with established instruments ¶1 (SAFEHEART)

**Current claim.** SAFEHEART derivation C=0.85/0.81; external C 0.77–0.78 REFERCHOL and 0.67 English routine care; +0.070 is specification-faithful in a setting where prior ASCVD and specialist LDL-C carry less information, not a general verdict of superiority.

**Biostatistician.** The caveat is correct. Derivation C is verified. External C values are **UNVERIFIED — DO NOT CITE** in this runtime. Severity: **MODERATE**.

**Cardiologist.** This is the right clinical reading. Keep it, and make it the abstract’s SAFEHEART sentence. Severity: **MINOR** if unverified numbers drop.

**Lipid-medicine specialist.** Treatment-suppressed LDL-C plus prior-ASCVD=0 is an off-label stress test. Severity: **MINOR** (paragraph already says this).

**Evidence check.** SAFEHEART C=0.85 and 0.81 verified. Gallo 2020 and McKay 2022: **UNVERIFIED — DO NOT CITE**.

**Required improvement.** Keep the interpretation; remove unverified external C until DOI resolution.

**Suggested replacement wording.** “The +0.070 difference is a common-data ranking result in a primary-prevention volunteer carrier-flag cohort in which SAFEHEART’s previous-ASCVD term is structurally zero. It is not evidence that CALON-C should replace SAFEHEART-RE in molecularly defined specialist FH.”

**Editor-in-Chief adjudication.** **MODERATE.** Interpretation good; citation fidelity not yet earned for [7] and [8].

---

### Discussion — Comparison ¶2 (Montreal)

**Current claim.** Montreal is a prevalent-disease score; comparison is a benchmark across estimands; most of CALON-C’s increment over age and sex came from diabetes, hypertension, and smoking.

**Biostatistician.** Estimand caveat is correct. The +0.033/+0.008 split remains un-intervalled. Severity: **MODERATE**.

**Cardiologist.** Then Montreal should not be in the confirmatory family. Severity: **MAJOR**.

**Lipid-medicine specialist.** Montreal’s scientific point (age capturing exposure when LDL is omitted) is not tested by CALON-C’s weak lipid terms. Severity: **MODERATE**.

**Evidence check.** ACC/AHA 2026 local extract supports prevalent-disease derivation. Primary Montreal papers **UNVERIFIED**.

**Required improvement.** Move Montreal out of confirmatory comparisons in both Methods and Discussion.

**Suggested replacement wording.** “The Montreal comparison is a different-estimand ranking benchmark and is not a confirmatory test of an incident-ASCVD model.”

**Editor-in-Chief adjudication.** **MAJOR.**

---

### Discussion — Comparison ¶3 (FH-Risk-Score)

**Current claim.** FH-Risk-Score is the strongest comparator; TIE is more informative than the significant comparisons; a routine-data model may recover similar ordering without Lp(a); that does not justify replacement.

**Biostatistician.** A TIE is not evidence of similar ordering. It is failure to demonstrate a difference on n=1,913/146, with possible overlap of 499 derivation participants. Severity: **MAJOR**.

**Cardiologist.** “May recover similar ordering without Lp(a)” will be quoted as licence not to measure Lp(a). Severity: **MAJOR**.

**Lipid-medicine specialist.** FH-Risk-Score uses untreated/imputed LDL-C and Lp(a) in DLCN-probable/definite FH. A TIE in a milder carrier-flag subset with on-treatment lipids does not show that Lp(a) is dispensable in HeFH. Severity: **MAJOR**.

**Evidence check.** Local *ATVB* extract: 74% molecular diagnosis; LDL-C 6.65 mmol/L; C=0.75. Present cohort median untreated-equivalent LDL-C 3.95 mmol/L.

**Required improvement.** State population mismatch. Delete “similar ordering without Lp(a)” or recast as a hypothesis.

**Suggested replacement wording.** “The difference versus FH-Risk-Score was a TIE in a milder, treated, carrier-flag subset and cannot exclude participant overlap with the score’s UK Biobank derivation sample. It does not show that Lp(a) can be omitted in heterozygous FH care.”

**Editor-in-Chief adjudication.** **MAJOR.**

---

### Discussion — Comparison ¶4 (guideline caution)

**Current claim.** 2026 ACC/AHA: FH-specific scores **may** be useful for short-term prediction; long-term validation and evidence that scores guide lipid-lowering remain limited; CALON-C adds to that evidence base but does not cross the threshold to clinical adoption.

**Biostatistician.** “Adds to that evidence base” overstates a development study without independent validation, calibration-in-care, or DCA. Severity: **MAJOR**.

**Cardiologist.** Correct that it does not cross adoption. The Class 2b recommendation is for **HeFH**, not this cohort. Severity: **MAJOR**.

**Lipid-medicine specialist.** Agree. CALON-C does not fill the guideline’s stated gap (long-term validation in diverse FH cohorts; evidence that scores guide LLT). Severity: **MAJOR**.

**Evidence check.** Local ACC/AHA 2026: COR 2b for FH-specific scores in adults with HeFH; FH-Risk-Score “has not yet been validated in diverse populations… nor assessed as a clinical tool to guide LLT.”

**Required improvement.** Replace “adds to that evidence base” with “does not meet the guideline’s stated evidence gaps.”

**Suggested replacement wording.** “CALON-C does not provide long-term validation in diverse heterozygous-FH cohorts and does not test whether a score changes lipid-lowering decisions.”

**Editor-in-Chief adjudication.** **MAJOR.**

---

### Discussion — Routine-panel parsimony ¶1–2

**Current claim.** Clinical advantage is lower data requirement; Lp(a) and apoB remain inconsistently measured despite once-in-adulthood Lp(a) and selective apoB guidance; Welsh non-evaluability shows implementation failure; parsimony is not automatically superiority; CALON-C is a candidate first-line ranking layer pending calibration and decision impact.

**Biostatistician.** “Candidate first-line ranking layer” is a clinical-utility claim without DCA. Severity: **MAJOR**.

**Cardiologist.** In 2026 US guidance, Lp(a) is COR 1, not an optional extra. Building a score to avoid a Class 1 test is the wrong implementation story. Severity: **MAJOR**.

**Lipid-medicine specialist.** Global scalability is a real issue for imaging and PRS, not for a once-in-lifetime Lp(a). Welsh BMI missingness is not an Lp(a) problem. Severity: **MAJOR**.

**Evidence check.** ACC/AHA 2026: Lp(a) in all adults COR 1; apoB reasonable when residual particle risk may be underestimated.

**Required improvement.** Recast parsimony as a historical-registry constraint, not as a preferred care pathway.

**Suggested replacement wording.** “A routine-panel specification can be scored in registries that lack Lp(a) or BMI. That is an implementation fact. It is not a reason to omit indicated Lp(a) testing or to adopt CALON-C as a first-line clinical layer.”

**Editor-in-Chief adjudication.** **MAJOR.**

---

### Discussion — Why the lipid terms did not dominate ¶1–2

**Current claim.** Weak adjusted lipid associations do not contradict LDL causality; within an LDLR-selected stratum, range restriction, therapy, and age-as-duration leave diabetes, hypertension, smoking, and sex to dominate near-term ranking; ~+0.008 lipid contribution should be reported; do not name the model as a cumulative-lipid mechanism.

**Biostatistician.** Causal-versus-predictive distinction is correct. The +0.008 still lacks a CI. Severity: **MODERATE**.

**Cardiologist.** This paragraph is the one that prevents harm if a reader thinks lipids “don’t matter.” Keep it high. Severity: **MINOR** (keep).

**Lipid-medicine specialist.** Range restriction is overstated: untreated-equivalent non-HDL IQR is 3.93–5.65 mmol/L, not a razor-thin band. The likelier explanations are treatment misclassification (MAE 1.20 mmol/L, r=0.32), age already in the lipid term, and a carrier flag that is not HeFH. Severity: **MAJOR**.

**Evidence check.** Ference 2017 LDL causality consensus is ref 23, **not cited in this paragraph**, and needs in-window verification; the 2017 EHJ consensus is inside the window but **UNVERIFIED** here. Do not use Cohen 2006 or pre-2016 FH classical-risk-factor papers as evidence.

**Required improvement.** Lead with measurement error and phenotype mildness, not “LDL still causes atherosclerosis” without a verified citation.

**Suggested replacement wording.** “The lipid-derived terms were TIEs. Possible explanations include a mild carrier-flag phenotype, a weak treatment-rescaling (correlation 0.32 with observed pre-treatment LDL-C), and triple counting of age. These predictive TIEs are not tests of LDL causality.”

**Editor-in-Chief adjudication.** **MAJOR** for mechanism special pleading; **MINOR** for the “do not name it as a lipid mechanism” conclusion, which is right.

---

### Discussion — Ascertainment and UK Biobank representativeness ¶1–3

**Current claim.** UK Biobank is not a random sample; volunteer selection can change associations; `ldlr_carrier` is not clinically recognised FH; LDL-C excess +0.15 to +0.23 mmol/L; internal calibration cannot establish calibration in care; next study needs calibration-in-the-large, slope, Brier, and net benefit in an untouched clinical cohort.

**Biostatistician.** Correct. Fry 2017 is in-window; van Alten 2024 and Schoeler 2023 are in-window but **UNVERIFIED** this runtime. Net benefit is named as future work, which is the only legitimate DCA language. Severity: **MODERATE**.

**Cardiologist.** This should have governed the title and abstract population. Severity: **MAJOR**.

**Lipid-medicine specialist.** +0.15 to +0.23 mmol/L is the single most important lipid fact in the paper and is buried. Genotype-first HeFH in population cohorts is repeatedly milder than clinic FH; that is why guideline scores cannot be transplanted by assertion. Severity: **MAJOR**.

**Evidence check.** Ref 15 (2005) is used earlier for the same point and is **outside the window**. In-window replacements must be verified before citation (Trinder 2020, Gidding 2023 are listed but unused in the body and **UNVERIFIED** here).

**Required improvement.** Move the LDL excess into the abstract. Replace [15] with an in-window verified genotype-first paper.

**Suggested replacement wording.** “Median untreated LDL-C excess versus non-carriers was only +0.15 to +0.23 mmol/L. The cohort is a volunteer carrier-flag sample, not clinic heterozygous FH.”

**Editor-in-Chief adjudication.** **MAJOR.**

---

### Discussion — Survivor bias and age ¶1–2

**Current claim.** Both cohorts are survivor-selected; age captures exposure and resilience; not a lifetime penetrance model.

**Biostatistician.** Left truncation is real and unmodelled. Severity: **MODERATE**.

**Cardiologist.** Correct clinically; CALON-C must not be used in children or young adults. Severity: **MODERATE**.

**Lipid-medicine specialist.** Agree; cumulative-exposure interpretation is especially invalid under late enrolment. Severity: **MODERATE**.

**Evidence check.** Insufficient need for extra papers; this is a design limitation.

**Required improvement.** State that the model is not for people younger than the UK Biobank recruitment window.

**Suggested replacement wording.** “CALON-C ranks middle-aged and older survivors and is not a lifetime penetrance or paediatric model.”

**Editor-in-Chief adjudication.** **MODERATE.**

---

### Discussion — Predictor timing in Wales ¶1–2

**Current claim.** Timing objection is substantive; 55/92 events had BP after the event in the earlier frame; investigator attestation is not data; dated-only model is a different specification; transport is a stress test.

**Biostatistician.** This is the correct PROBAST reading. It contradicts any abstract Findings emphasis on C=0.725. Severity: **MAJOR**.

**Cardiologist.** Post-event BP as a “predictor” is reverse causation. Severity: **MAJOR**.

**Lipid-medicine specialist.** Comparator symmetry (they use the same dirty fields) does not sanitise the bias; it only keeps the comparison equally dirty. Severity: **MODERATE**.

**Evidence check.** Internal aggregate in `calon_c.json`.

**Required improvement.** Promote this to a primary limitation in the abstract.

**Suggested replacement wording.** Already strong; copy one sentence into the abstract.

**Editor-in-Chief adjudication.** **MAJOR** (content good; placement too late).

---

### Discussion — Calibration drift and non-significant differences ¶1–2

**Current claim.** Ranking can survive while absolute risk fails; no threshold outside development data; FH-Risk-Score directional estimate is still a TIE; adoption needs untouched validation, calibration, net benefit, usability, and preferably outcome evidence.

**Biostatistician.** Correct TIE language. “Preferably evidence that model-guided care changes decisions or outcomes” is the right ceiling and is unmet. Severity: **MINOR**.

**Cardiologist.** Agree; this is the safety paragraph. Severity: **MINOR**.

**Lipid-medicine specialist.** Agree. Severity: **MINOR**.

**Evidence check.** None required beyond the paper’s own CIs.

**Required improvement.** Keep. Delete any earlier sentence that conflicts.

**Suggested replacement wording.** Keep.

**Editor-in-Chief adjudication.** **MINOR.**

---

### Discussion — Lp(a), apoB, and the grey zone ¶1–2

**Current claim.** Exclusion of Lp(a)/apoB was for scalability, not biology; 2026 guideline recommends Lp(a) once and apoB when residual particle risk may be missed; CAC can add to SAFEHEART; grey-zone did not improve C; association is not reclassification is not utility.

**Biostatistician.** The hierarchy association ≠ reclassification ≠ utility is correct. Grey-zone still cannot bear this weight. Severity: **MODERATE**.

**Cardiologist.** CAC “not indicated to de-risk FH” in ACC/AHA 2026 sits awkwardly beside citing CAC as an enhancer [12]. Severity: **MAJOR**.

**Lipid-medicine specialist.** Keep the guideline sentences; demote grey-zone. Ref 12 Gallo CAC 2021 is **UNVERIFIED** here. Severity: **MODERATE**.

**Evidence check.** ACC/AHA 2026: CAC=0 may not de-risk FH. Lp(a) COR 1.

**Required improvement.** If CAC is mentioned, quote the de-risking prohibition in the same sentence.

**Suggested replacement wording.** “Lp(a) measurement remains indicated at least once in adults. This study did not test that indication. Coronary calcium is not a tool to defer lipid-lowering in heterozygous FH.”

**Editor-in-Chief adjudication.** **MAJOR** for CAC/de-risking tension.

---

### Discussion — Competing risks and endpoint definition ¶1–2

**Current claim.** Death competes with first ASCVD; missing UK Biobank analysis blocks probability interpretation; endpoints are not uniform MACE; future work needs harmonised MI, ischaemic stroke, CV death, and procedures.

**Biostatistician.** Correct, and fatal to Table 2 as a risk equation. Severity: **MAJOR**.

**Cardiologist.** Harmonised hard endpoints should have been the primary, not future work. Severity: **MAJOR**.

**Lipid-medicine specialist.** Procedure-inclusive Welsh endpoint will inflate clinic incidence relative to UK Biobank. Severity: **MODERATE**.

**Evidence check.** Internal METHODS date-completeness figures.

**Required improvement.** Do not publish S0 until UK Biobank CIF exists.

**Suggested replacement wording.** Keep the limitation; act on it by removing the usable equation.

**Editor-in-Chief adjudication.** **MAJOR.**

---

### Discussion — Ancestry and fairness ¶1–2

**Current claim.** Predominantly European ancestry; no fairness assessment; cannot extrapolate; future validation must be multi-ancestry with more than subgroup C.

**Biostatistician.** Correct TRIPOD+AI failure. Severity: **MAJOR** as reporting, not as spin.

**Cardiologist.** Lp(a) distribution differs by ancestry; a no-Lp(a) model may be especially unfair. Severity: **MAJOR**.

**Lipid-medicine specialist.** Agree; LDLR variant spectrum also differs. Severity: **MODERATE**.

**Evidence check.** Insufficient validated in-window fairness results in this package.

**Required improvement.** Put “no ancestry-stratified performance” in the abstract.

**Suggested replacement wording.** Keep, and add Lp(a)-by-ancestry as a specific reason a no-Lp(a) model may not travel.

**Editor-in-Chief adjudication.** **MAJOR.**

---

### Discussion — Overlap and leakage ¶1–2

**Current claim.** Temporal leakage addressed by excluding prevalent/undated events; FH-Risk-Score overlap unknown; programme previously examined both datasets; freezing now cannot create an untouched cohort; “external validation” is too strong until a third locked cohort.

**Biostatistician.** This is accurate and should have killed residual novelty/priority language. Severity: **MINOR** (keep).

**Cardiologist.** Agree. Severity: **MINOR**.

**Lipid-medicine specialist.** Agree. Severity: **MINOR**.

**Evidence check.** FH-Risk-Score UKB n=499 verified.

**Required improvement.** Use this paragraph to police the rest of the paper.

**Suggested replacement wording.** Keep.

**Editor-in-Chief adjudication.** **MINOR.**

---

### Discussion — Clinical implications ¶1–2

**Current claim.** Immediate implication is methodological (common-data comparison, exact reconstruction, no favourable missingness, multiplicity); CALON-C is a candidate routine-data ranking tool, not ready to guide escalation; FH diagnosis remains an indication for intensive management; never de-risk a carrier or defer guideline-directed treatment.

**Biostatistician.** Paragraph 1 is earned. Paragraph 2’s “candidate tool” is not. Severity: **MAJOR**.

**Cardiologist.** The de-risking prohibition is the essential clinical sentence. “Candidate ranking tool” should go. Severity: **MAJOR**.

**Lipid-medicine specialist.** Agree; also, this cohort is often not an FH diagnosis. Severity: **MAJOR**.

**Evidence check.** ACC/AHA 2026: LLT recommended in HeFH; do not use CAC to defer.

**Required improvement.** Delete “candidate.” Keep the prohibition.

**Suggested replacement wording.** “CALON-C is not ready to guide intensification or de-intensification. Heterozygous FH remains an indication for intensive risk-factor management regardless of this score.”

**Editor-in-Chief adjudication.** **MAJOR.**

---

### Discussion — Strengths ¶1

**Current claim.** Incident design; published equation; two internal C estimators; paired common-subset comparisons; comparator corrections; age gate; strict missing-input policy; Holm; PH diagnostics; DCA withdrawn; corrections moved both ways.

**Biostatistician.** These are real strengths of **reporting**, not of **validation**. Severity: **MINOR**.

**Cardiologist.** Strengths do not offset the population mismatch. Severity: **MINOR**.

**Lipid-medicine specialist.** Comparator fidelity is the genuine methodological strength. Severity: **MINOR**.

**Evidence check.** Internal.

**Required improvement.** Call them reporting strengths.

**Suggested replacement wording.** “The main strength is comparator-faithful reporting with corrections that were allowed to move against the new model.”

**Editor-in-Chief adjudication.** **MINOR.**

---

### Discussion — Limitations ¶1

**Current claim.** Eleven limitations: no independent external validation; no variant-level UKB confirmation; Welsh artefacts unsynchronised; UKB competing-risk failed; 147/289 unambiguous dates; no UKB kinship; internal calibration only; no corrected subgroups; Lp(a) conversion and BMI assumptions; volunteer European sample; missing governance.

**Biostatistician.** This list is unusually complete. It should have changed the title, abstract Findings, and Table 2. A limitations dump does not mitigate claims placed earlier. Severity: **MAJOR** as placement, not as content.

**Cardiologist.** Agree. Severity: **MAJOR**.

**Lipid-medicine specialist.** Missing from the list: treatment-rescaling MAE/r=0.32; negative remnant clip; triple age-counting; endpoint mismatch. Severity: **MAJOR**.

**Evidence check.** Internal.

**Required improvement.** Add the missing lipid/endpoint items. Move the first four limitations into the abstract.

**Suggested replacement wording.** Add: “Untreated-equivalent LDL-C reconstruction had correlation 0.32 with observed pre-treatment values. UK Biobank and Welsh endpoints were not the same composite.”

**Editor-in-Chief adjudication.** **MAJOR.**

---

### Conclusion ¶1

**Current claim.** Moderate internal discrimination from routine variables; out-discriminated SAFEHEART-RE and Montreal after Holm; tied FH-Risk-Score; frozen equation retained ranking in All-Wales, but reciprocal transport not independent validation; supports further validation, not deployment, thresholds, or superiority to every FH instrument.

**Biostatistician.** Still leads with the off-horizon/off-estimand wins. Severity: **MAJOR**.

**Cardiologist.** “Supports further validation” is acceptable; “retained ranking in All-Wales” is not, given timing contamination. Severity: **MAJOR**.

**Lipid-medicine specialist.** Still omits lipid-term TIEs and the mild phenotype. Severity: **MAJOR**.

**Evidence check.** Same as abstract.

**Required improvement.** Rewrite around carrier-flag development, FH-Risk-Score TIE, and non-deployment.

**Suggested replacement wording.** “In UK Biobank adults identified by an `ldlr_carrier` flag, a routine-variable ridge Cox model showed moderate internal discrimination. The difference versus FH-Risk-Score was a TIE. Full-follow-up differences versus SAFEHEART-RE and Montreal-FH-SCORE were not tests of those scores in their intended clinic-HeFH, published-horizon uses. Application to the All-Wales registry was setting transport under incompletely dated predictors, not independent external validation. CALON-C should not be used to guide treatment or to de-risk carriers.”

**Editor-in-Chief adjudication.** **MAJOR.**

---

## Whole-manuscript analyses

### A. Novelty map

**Genuinely new**
- A documented, multiplicity-controlled, complete-input ranking comparison of one routine-variable Cox specification with three published FH instruments **inside this UK Biobank `ldlr_carrier` frame**, with comparator coding errors corrected in both directions.
- Explicit withdrawal of DCA/utility language and of independent-external-validation language.

**Incremental but useful**
- Showing that a treated volunteer carrier-flag cohort yields SAFEHEART-RE C far below derivation (0.63 versus 0.81 in primary prevention), consistent with the broader lesson that specialist-registry scores degrade when case mix and lipid handling change.
- Showing that Lp(a)-requiring scores can be operationally non-evaluable in a national registry with missing BMI/Lp(a).

**Already established**
- Heterogeneity of ASCVD risk in HeFH.
- Inadequacy of general-population 10-/30-year equations in HeFH (ACC/AHA 2026, local extract).
- SAFEHEART-RE derivation performance and the need for external calibration checks.
- FH-Risk-Score as an incident 10-year primary-prevention chart that already used 499 UK Biobank participants (local *ATVB* extract).
- Volunteer selection in UK Biobank.
- Association ≠ incremental C ≠ clinical utility.

**Unsupported priority claims**
- “First identified head-to-head of CALON-C and the three named instruments” (tautology).
- Any implication of first UK evaluation of published FH scores (FH-Risk-Score already used UK Biobank).
- Reciprocal transport as a novel validation design **with calibration** (this paper reports transport C only; internal calibration only).
- Cumulative-exposure modelling (the term is a single-visit log product).
- A parsimonious model that can stand in for Lp(a)-containing scores in care.

**Closest overlapping work**
1. **Paquette et al., *ATVB* 2021 (FH-Risk-Score)** — closest estimand (incident 10-year ASCVD, primary prevention, age ≤65, includes UK Biobank). Overlap: same country source, similar clinical covariates, Lp(a) threshold. Residual: CALON-C omits Lp(a), uses a different lipid construction, and is not DLCN-defined FH.
2. **Pérez de Isla et al., *Circulation* 2017 (SAFEHEART-RE)** — closest named specialist equation. Overlap: age, sex, hypertension, smoking, LDL-C, Lp(a). Residual: SAFEHEART includes prior ASCVD and BMI and was derived in molecular Spanish FH.
3. **Programme-cited REFERCHOL (Gallo 2020) and English routine-care SAFEHEART (McKay 2022)** — closest **transport/calibration** story, but **UNVERIFIED — DO NOT CITE** in this runtime. If verified, they already own “SAFEHEART does not travel without recalibration.”
4. **Tamehri Zadeh et al., *Atherosclerosis* 2026 / *Can J Cardiol* 2025** — closest recent multi-score evaluation in genetically confirmed HeFH. **UNVERIFIED — DO NOT CITE** here. If verified, they own genetically confirmed head-to-head ranking; CALON-C would be a milder, flag-based, UK-specific complement, not a scoop.

---

### B. Agreement and disagreement with recent evidence

| Paper / source | Relation | Conflict class |
|---|---|---|
| ACC/AHA 2026 dyslipidaemia guideline (local extract) | Supports caution on FH scores (COR 2b) and forbids general-population 10-/30-year calculators in **HeFH**. Conflicts with using that gap to justify a carrier-flag model, omitting Lp(a) as a care pathway, and any de-risking use of scores/CAC. | Population/ascertainment-driven, plus implementation |
| ESC/EAS 2025 focused update (local extract) | Supports treating FH as high or very-high risk. Does not support a new ranking tool as a prerequisite to LLT. | Population/ascertainment-driven |
| SAFEHEART-RE 2017 (local extract) | Supports the authors’ measured-LDL coding. Conflicts with treating a full-follow-up C win, with prior ASCVD fixed at 0, as a test of SAFEHEART in intended use. | Endpoint/estimand-driven and implementation/calibration-driven |
| FH-Risk-Score 2021 (local extract) | Supports age ≤65 gate, untreated/imputed LDL, UKB n=499, incident 10-year estimand. Conflicts with implying a no-Lp(a) model is exchangeable: derivation LDL-C ~6.7 mmol/L versus 3.95 mmol/L here. | Population/ascertainment-driven |
| Montreal-FH-SCORE (ACC/AHA description; primary papers UNVERIFIED) | Supports prevalent-disease origin. Conflicts with confirmatory “superiority” for incident ranking. | Endpoint/estimand-driven |
| REFERCHOL / McKay SAFEHEART external evaluations | Would support “registry scores miscalibrate in new settings” **if verified**. Not used as evidence in this review. | Implementation/calibration-driven (provisional) |
| Grey-zone Lp(a) TIE versus ACC/AHA Lp(a) COR 1 | Not a biological disagreement with Lp(a) risk; a truncated incremental-C experiment in the wrong population. | Methodological and population/ascertainment-driven |
| LDL causality consensus (Ference 2017 listed, unused/unverified here) | No substantive biological disagreement if the paper keeps “predictive TIE ≠ causal null.” Risk is readers inferring the latter. | Methodological |

No verified in-window source shows that a routine-panel model has **comparative net benefit** over FH-Risk-Score in HeFH care.

---

### C. Internal manuscript consistency audit

Checked against the manuscript and aggregate artefacts only. No participant rows.

| Item | Finding |
|---|---|
| UKB flow 3,540 → 207 → 124 → 3,209; 289 / 97 / 194 | Consistent (abstract, methods, Table 3, JSON). |
| Wales 1,169/102; 51 at 5 y; 75 at 10 y | Consistent in prose/JSON. **Contradicted** by Table 3 and Table 5 (1,159/92, 44/66 events). |
| Transport C 0.725 / 0.660 vs 0.7252 / 0.6600 | Rounding inconsistency. Source includes `calon_c.json` (pre-correction pipeline). |
| Head-to-head deltas and Holm p | Consistent with `RESULTS_FINAL_CORRECTED.md`. |
| “No 5-year superiority” vs abstract full-follow-up SAFEHEART win | Not a numeric contradiction, but a **rhetorical** contradiction: SAFEHEART’s native horizon is the null family. |
| Optimism-corrected C 0.7095 / 0.7079 / 0.7336 | Matches `calon_apparent.json`. |
| Equation S0 and lp_mean | Match `calon_c_equation.json`. |
| Age HR 1.022 (1.000–1.046) | **Does not match** the equation file lower bound 0.99968 (a TIE, p=0.053). |
| Lipid HRs | Match equation JSON; all TIEs. |
| Incremental +0.041 / +0.033 / +0.008 | **Not uniquely recovered** from `htn_isolation.json` (different nested base; no CIs). |
| Grey-zone 1,685/218; deltas | Match JSON. n_scored 3,333 ≠ development 3,209; different predictor names. |
| “0/16 PH violations” | 9 UKB + 7 Wales terms, not 16 terms in one model. |
| “35 competing deaths among 102 events” | Easy to misread; JSON stores deaths and ASCVD events as separate counts. |
| Calibration “acceptable agreement” vs slope CI 0.884–1.318 | Interpretive contradiction: CI includes 1 **and** material miscalibration. |
| Table 5 mixes pre-rescue calibration with corrected CIF | Frame contradiction, disclosed but still printed. |
| Person-years 6.55/1,000 | Labelled pre-correction, reported in the corrected Results population paragraph. |
| Pre-specification | Withdrawn in Methods; older results file still says “pre-specified.” Manuscript mostly obeys the withdrawal. |
| Wales as validation | Prose consistently says transport. Key points/Conclusion still headline C=0.725 as a finding. |
| MACE | Correctly avoided. |
| Clinical utility / DCA | Withdrawn, then partially reintroduced as “candidate first-line ranking layer.” |
| Unused references | Body cites [1]–[12], [15], [18]–[21], [24], [25], [39]. Unused padding includes [13], [14], [16], [17], [22], [23], [26]–[38]. |
| STROBE | Named, not cited. RECORD [39] is 2015 (outside window). Ref [15] and [18] also outside window. |

---

### D. Reporting and publication audit

| Standard | Verdict |
|---|---|
| **TRIPOD+AI** | Title and structure are closer than earlier CALON drafts. Failures: no independent validation (item 20); internal-only calibration and no comparative DCA (18); fold-wise median imputation without uncertainty (9); no fairness/subgroups (13); no validated risk strata (11); analyst blinding undocumented (6b/7b); Welsh flow 649 vs 659 unconfirmed (14b); governance 24–27 empty; overlap with FH-Risk-Score unknown (20/21). |
| **PROBAST** | High risk of bias in analysis (imputation, penalty not nested-tuned, programme-level predictor exploration) and in Welsh predictors (timing). High applicability concern: volunteers with a mild flag, not HeFH. |
| **STROBE** | Design and limitations are described. Missing: corrected Welsh Table 1, interactions, fully modelled informative censoring. |
| **RECORD** | Carrier status not validated against variant-level data; linkage-quality metrics and Welsh administrative end date incomplete. RECORD itself is 2015 (excluded as evidential support). |
| **Calibration** | Internal/apparent only. Slope CIs include 1 and are wide. No transported calibration. |
| **Clinical utility** | Not shown. DCA withdrawn. Any “candidate tool” sentence should go. |
| **Competing risks** | Wales only. UK Biobank missing. Absolute-risk equation therefore not reportable. |
| **Missing data** | Policy for comparators is strict and good. Model imputation is crude. Welsh missingness unsynchronised. |
| **Family clustering** | Wales: yes for optimism. UK Biobank: impossible from the available file; CIs may be anti-conservative. |
| **Fairness** | Not assessed. |
| **Reproducibility** | Equation JSON exists; Welsh artefacts do not match the corrected n; no ethics/code-availability statement. |
| **Citation fidelity** | Strong for SAFEHEART Table 3 and FH-Risk-Score age gate. Weak for [10], [11], unused pile, out-of-window [15]/[18]/[39], and unverified [7]–[9]. |
| **Journal fit** | Not *Circulation* / *EHJ* / *JACC*. After source lock and claim cuts, possibly *Atherosclerosis* or *Journal of Clinical Lipidology* as a methods/implementation paper. Even then, ethics placeholders are desk-reject material. |

---

### E. Top revisions

1. **Supply ethics, funding, conflicts, PPI, data-controller, and model-availability statements, or do not submit.** (FATAL)
2. **Regenerate every Welsh descriptive, discrimination, calibration, and equation artefact on the 1,169/102 frame; until then remove Welsh tables.** (FATAL)
3. **Retitle and reframe as a UK Biobank `ldlr_carrier`-flag development study, not an HeFH risk-score paper.** Put LDL-C excess +0.15 to +0.23 mmol/L in the abstract. (FATAL for translation; MAJOR for novelty)
4. **Remove the usable 5-/10-year equation from the main text until a UK Biobank competing-risk baseline and out-of-fold calibration exist.** (FATAL for patient safety)
5. **Make the FH-Risk-Score TIE, the 5-year Holm-null family, and Welsh predictor timing the headline comparative results; demote full-follow-up SAFEHEART and Montreal.** (MAJOR)
6. **Rename or delete “cumulative” lipid language; report treatment-rescaling MAE 1.20 mmol/L and r=0.32; clip remnant at 0; unround the age CI to show a TIE.** (MAJOR)
7. **Delete tautological “first” claims, “candidate first-line ranking layer,” “adds to the evidence base,” and the stealth non-inferiority tally.** (MAJOR)
8. **Take Montreal out of the confirmatory Holm family; do not compare the three UK Biobank deltas as if they shared one sample.** (MAJOR)
9. **Replace or delete out-of-window citations used as evidence ([15], [18], [39]); verify or delete [7]–[11]; remove unused refs [13], [14], [16], [17], [22], [23], [26]–[38].** (MAJOR)
10. **Cosmetic last: consistent C decimals, “16 terms across two models,” competing-deaths wording, STROBE citation, word-count insertion.** (MINOR)

---

### F. Inter-panel tension memo

**Biostatistician vs Cardiologist.** The biostatistician can accept a specialist-journal methods paper if Welsh files are regenerated, the Holm family is redesigned, and absolute-risk formulae are withdrawn. The cardiologist still rejects clinic translation: even a perfectly analysed C=0.71 TIE versus FH-Risk-Score in volunteers should not change intensification, referral, or de-risking. **Do not smooth this.** A clean methods paper can be true and still be clinically inert.

**Cardiologist vs Lipid-medicine specialist.** Both reject HeFH labelling. They split on parsimony. The cardiologist sees a no-Lp(a) model as a guideline-discordant care pathway (Lp(a) COR 1). The lipid specialist is willing to score historical registries without Lp(a), but insists that a TIE against FH-Risk-Score in a 3.95 mmol/L LDL-C flag cohort is not evidence that Lp(a) or apoB can be dropped in true HeFH. **The lipid seat is less interested in C deltas and more interested in the phenotype being too mild for the question.**

**Lipid-medicine specialist vs Biostatistician.** The biostatistician treats `log(non-HDL × age)` as just another covariate whose HR is a TIE. The lipid specialist treats calling it cumulative untreated-equivalent exposure as a scientific error even if C is unchanged. **Renaming the term is non-negotiable for the lipid seat; it is cosmetic for the statistician.**

**Editor-in-Chief vs all three.** All three would allow a cut-down methods paper. The editor would still desk-reject today for placeholders, unsynchronised tables, an equation that looks deployable, and a title that says LDLR-variant carriers. **Journal-fit disagreement: statistician might try *Diagnostic and Prognostic Research* or *Atherosclerosis*; cardiologist sees no clinical journal until a third untouched HeFH cohort exists; lipid specialist would consider *JCL* only after the phenotype is in the title; the editor agrees with the lipid specialist.**

Predicted strongest cross-lens fight in later rounds: **whether C=0.725 UK Biobank-to-Wales is reportable at all.** Cardiologist and lipid specialist: not as a finding, only as a contaminated stress test. Biostatistician: reportable with a 0.030 timing bound. Editor: if it stays in the abstract Findings, the paper keeps a validation halo the discussion already disowns.

---

## Internal-panel debate

**Biostatistician.** The authors did the rare thing of letting corrections move against themselves. That is why I will not call the analysis fraudulent or uninterpretable. I will call it unfinished. Holm on a badly chosen family, median imputation, an unpublished penalty, a 7-term reverse “transport,” and Table 3 still showing 1,159/92 are enough to stop a statistical reviewer. Fix the family and the files, and a methods paper remains.

**Cardiologist.** I am not reviewing a methods appendix. The abstract still offers a tool for first atherosclerotic events in LDLR-variant carriers. My patients with HeFH are not this cohort. I will not use C=0.71, a TIE with FH-Risk-Score, and a Welsh C built on post-event blood pressure to escalate or delay PCSK9 inhibition. The de-risking sentence in the discussion is correct and is contradicted by Table 2’s 30% worked example. That table is a safety issue.

**Lipid-medicine specialist.** The carrier flag with +0.2 mmol/L LDL-C excess is the paper. Everything else is commentary. You cannot test FH instruments in a sample that is not FH, then tell lipid clinics the routine panel “recovers similar ordering without Lp(a).” The lipid terms are TIEs because the phenotype is mild, the untreated reconstruction is weak, and age is counted three times — not because LDL has retired. If the authors want a lipid paper, they must say that in the title: population-ascertained LDLR-carrier flag, not familial hypercholesterolaemia.

**Editor-in-Chief.** I have two papers in one file. Paper A is an honest comparator-coding audit. Paper B is a new risk equation. Paper B is not supported. Paper A is publishable only after governance, source lock, and a title that matches the flag. I will not send this to *Circulation*. I would not send it to *Atherosclerosis* this week. The authors already wrote “not submission-ready.” I agree.

**Unresolved disagreement (left standing).** Whether, after revisions, the primary destination should be a prediction-methods journal (Biostatistician) or a lipid journal with an explicitly negative translational message (Lipid specialist / Editor). The Cardiologist does not offer a clinical cardiology journal at all.

---

## Teaching section for Dr Genedy

**1. Estimand before comparator.** SAFEHEART-RE’s published job is short-term incident ASCVD in molecular FH, including prior disease, using measured LDL-C and Lp(a). If you force prior ASCVD to 0, use treated volunteer LDL-C, and headline full follow-up after the 5-year Holm test is a TIE, you have not beaten SAFEHEART. You have scored it off-label. **Lesson:** a faithful coefficient table is not a faithful question.

**2. A TIE is a TIE.** FH-Risk-Score +0.015 (−0.011 to 0.040) is not “similar ordering,” “non-inferior,” or “may recover.” With possible overlap of 499 UK Biobank derivation participants, the TIE is even less of a victory. **Lesson:** do not narrate the point estimate when the interval includes 0.

**3. Population is part of the estimand.** HeFH guideline text (ACC/AHA 2026 COR 2b/3) does not transfer to an `ldlr_carrier` flag with empty `variant_id` and +0.2 mmol/L LDL-C excess. **Lesson:** if the phenotype is not FH, the title cannot be FH.

**4. Cumulative exposure has a definition.** Cholesterol-years need time under exposure. `log(non-HDL × age)` at one visit, after dividing treated LDL by 0.70 (r=0.32 with true pre-treatment LDL), is not that. **Lesson:** name the transform you computed, not the biology you wished for.

**5. Transport is not validation.** Applying a frozen equation to a second dataset that the same programme already used, with a different endpoint, a different term set in reverse, and predictors dated after the event, is a stress test. **Lesson:** TRIPOD “external validation” requires an untouched cohort and the same prediction task.

**6. Internal calibration plus S0 is a deployable-looking object.** Readers will type the equation into a spreadsheet. If competing death was not modelled and the baseline is apparent, publishing S0 in Table 2 is a clinical-safety decision, not a formatting choice. **Lesson:** unpublished baselines cannot hurt patients; published ones can.

**7. Utility has one accepted display.** Without comparative decision curves (and preferably an outcome trial), you may not say candidate tool, first-line layer, or adds to the evidence the guideline asked for. **Lesson:** withdrawn DCA means withdrawn usefulness language, including synonyms.

**8. Disclosure does not licence contradiction.** Writing “Welsh Table 1 is uncorrected” and then printing Table 3 as 1,159/92 beside 1,169/102 tells a reviewer the pipeline is not locked. **Lesson:** a limitations list is not a second results section.

**9. Citation is a claim.** Out-of-window Tybjærg-Hansen 2005 cannot carry a 2026 scientific contrast. Unused refs 26–38 look like checklist stuffing. [10] and [11] do not support “apoB, imaging, PRS.” **Lesson:** every bracket must earn its sentence inside the 17 August 2016–17 August 2026 window.

**10. Class 1 tests are not optional extras.** A model that omits Lp(a) can still be scored in old registries. It cannot be positioned against a COR 1 once-in-adulthood Lp(a) recommendation. **Lesson:** parsimony is a data constraint, not a care pathway.

---

## Research-tool status table

| Tool | Status | What happened |
|---|---|---|
| `/academic` literature connector | **NOT EXPOSED/NOT CONFIGURED** | No callable `/academic` search tool. `academic-medical-writer` and `academic-executive` skills were **read** and used as review standards only. |
| Scite AI | **NOT EXPOSED/NOT CONFIGURED** | `GetMcpTools` returned only Google Drive. No Scite tool was callable. |
| SciSpace | **NOT EXPOSED/NOT CONFIGURED** | Not in the live MCP catalogue. |
| Elicit | **NOT EXPOSED/NOT CONFIGURED** | Not in the live MCP catalogue. |
| Consensus | **NOT EXPOSED/NOT CONFIGURED** | Not in the live MCP catalogue. |
| PubMed / NCBI E-utilities | **AVAILABLE BUT FAILED** | Intended via `pubmed_search.py` and Entrez URLs. Live WebFetch/WebSearch calls were **rejected in this session**, so no PubMed metadata returned. |
| Crossref / DOI.org | **AVAILABLE BUT FAILED** | Crossref API fetches were **rejected**. No DOI resolution table was produced live. |
| Native web search | **AVAILABLE BUT FAILED** | WebSearch rejected by the user/runtime. |
| Google Drive MCP `search_files` | **AVAILABLE BUT FAILED** | Call rejected. |
| Local publisher extracts | **USED — results returned** | Full-text extracts of ACC/AHA 2026, ESC/EAS 2025 (`ehaf190_full.txt`), SAFEHEART 2017, and FH-Risk-Score 2021 were read and used to verify guideline wording, SAFEHEART Table 3, and FH-Risk-Score design. |
| Aggregate CALON-C artefacts | **USED — results returned** | `RESULTS_FINAL_CORRECTED.md`, `calon_c_corrected.json`, `calon_c_equation.json`, `calon_apparent.json`, `calon_c_calibration.json`, `grey_zone_enhancers.json`, `htn_isolation.json`, `METHODS_CALON_C.md`, conflict ledger. No participant-level files opened. |
| Other models’ round-1 reviews | **Not used** | Blind round 1. A path grep for transport values briefly listed another model’s file; that content was not used in judgements. |

A 9 August 2026 programme literature log exists (`qc/LITERATURE_VERIFICATION_2026_08_09.md`). It was **not** treated as live Scite/PubMed verification for this review.

---

## Eligible evidence ledger

**Window:** 17 August 2016 through 17 August 2026 inclusive.

### Verified in this runtime (local publisher extract with DOI, volume, pages, date)

| Paper | Journal, year | Design / population | Finding used | DOI | Role |
|---|---|---|---|---|---|
| Blumenthal et al. 2026 ACC/AHA dyslipidaemia guideline | *Circulation* 2026;153:e1154–e1276 (28 Apr 2026) | North American CPG | HeFH: FH-specific scores **may** be useful short-term (COR 2b); general-population 10-/30-year tools **should not** be used (COR 3: Harm); Lp(a) once in all adults COR 1; do not use CAC=0 to de-risk FH | [10.1161/CIR.0000000000001423](https://doi.org/10.1161/CIR.0000000000001423) | Supports caution; **challenges** HeFH framing, no-Lp(a) care pathway, deployable equation |
| Mach et al. 2025 ESC/EAS focused update | *Eur Heart J* 2025;46:4359–4378 | European CPG | FH without other major risk factors = high risk; FH with ASCVD or another major risk factor = very-high risk | [10.1093/eurheartj/ehaf190](https://doi.org/10.1093/eurheartj/ehaf190) | Supports treating FH; does not support a new score as a treatment gate |
| Pérez de Isla et al. SAFEHEART-RE | *Circulation* 2017;135:2133–2144 (30 May 2017) | 2,404 molecular Spanish FH, primary+secondary | C=0.85 overall, 0.81 without prior ASCVD; prior ASCVD HR 4.15; measured LDL-C in multivariable model; pretreatment LDL cells blank; BMI by overweight/obesity; bootstrap ×100; 5- and 10-year examples | [10.1161/CIRCULATIONAHA.116.024541](https://doi.org/10.1161/CIRCULATIONAHA.116.024541) | Supports coding fidelity; **challenges** off-label superiority claim |
| Paquette et al. FH-Risk-Score | *ATVB* 2021;41:2632–2640 (Oct 2021) | 3,881 primary-prevention HeFH, age 18–65, 5 registries incl. UKB n=499 | 10-year C=0.75; vs SAFEHEART 0.69 in that sample; untreated 57%/imputed 43% LDL-C; median LDL-C 6.65 mmol/L | [10.1161/ATVBAHA.121.316106](https://doi.org/10.1161/ATVBAHA.121.316106) | Supports TIE as the like-for-like test; **challenges** population equivalence |

### UNVERIFIED — DO NOT CITE (listed in the manuscript or needed, but not resolved live and no local full extract read)

Refs 4–5 (Montreal primary papers), 7 (Gallo/REFERCHOL), 8 (McKay 2022), 9–11 (Tamehri 2026/2025; Zamora 2025), 12 (Gallo CAC 2021), 13 (Khera 2016 — also likely **pre-window**), 14, 16, 17, 19–23, 24 (TRIPOD+AI), 25 (PROBAST), 26–28, 31, 34–38.

These may be real papers. They are **not** evidence in this review until PubMed/Crossref/publisher resolution succeeds.

### Excluded historical context (pre-17 August 2016; must not support a manuscript claim)

| Item | Why it appeared | Rule |
|---|---|---|
| Tybjærg-Hansen et al. 2005 [15] | Clinic vs population LDLR phenotype | Do not use as evidence; replace with in-window genotype-first data after verification |
| Sudlow et al. 2015 [18] | UK Biobank resource paper | Historical description only |
| RECORD 2015 [39] | Reporting extension | Name as a reporting checklist if required by a journal, not as 2016–2026 evidence |
| Debray 2015 [29], Law 2003 [30], Jansen 2004 [32], Cohen 2006 [33] | Unused or background | Do not cite for claims |
| FAMCAT 2015 (skill reference, not in this manuscript) | Diagnostic, not event prediction | Out of window and wrong task |
| Harrell 1996 / classical Cox references | Internal validation history | Methods history only |

Karlson *EJPC* 2016 [31] may fall **before** 17 August 2016 depending on the exact publication date; treat as **UNVERIFIED / possible pre-window** until a date is resolved.

---

## Claims that must be deleted unless new evidence is produced

1. Any statement that the UK Biobank cohort is genetically confirmed, pathogenic/likely pathogenic, or clinically equivalent to heterozygous FH.
2. Independent external validation, geographic replication, or “the model transported” as a validation success.
3. Clinical utility, net benefit, candidate first-line ranking layer, treatment thresholds, risk bands for allocation, or that CALON-C adds the evidence ACC/AHA said was missing (decision-guiding LLT).
4. Superiority to SAFEHEART-RE **for SAFEHEART’s intended use** (molecular FH, including secondary prevention, native 5-year horizon).
5. Superiority to Montreal-FH-SCORE **for Montreal’s original prevalent-CVD task**, or retention of Montreal in a confirmatory superiority family.
6. Superiority, non-inferiority, or “similar ordering without Lp(a)” versus FH-Risk-Score. The result is a **TIE**, with unknown overlap.
7. Any 5-year confirmatory win; any Welsh head-to-head win.
8. Cumulative cholesterol exposure, cholesterol-years, or untreated-equivalent concentrations as validated individual reconstructions.
9. That lipid terms “still contribute useful exposure context” as a positive finding: the three HRs are TIEs and the nested +0.008 has no CI.
10. That specialised biomarkers (Lp(a), apoB) lack incremental value in HeFH or need not be measured — including grey-zone “translational” readings.
11. Tautological priority: “first head-to-head of CALON-C and the three instruments.”
12. “No comparator significantly outperformed CALON-C” as a result (stealth non-inferiority).
13. “Acceptable internal calibration” as a qualitative summary of slope 1.101 (0.884–1.318).
14. Deployable 5- and 10-year absolute risks from Table 2.
15. Out-of-window evidence claims resting on Tybjærg-Hansen 2005, and any claim relying on UNVERIFIED refs 7–11 until DOIs are resolved.
16. Pre-specification of the CALON-C specification (already withdrawn; do not let it return from older results files).

Until items 1–4 of the Top revisions exist as new source files or new analyses, the defensible public claim is only this:

*In 3,209 UK Biobank adults identified by an `ldlr_carrier` flag, a nine-term ridge Cox model had optimism-corrected C 0.7095. On complete-input subsets, full-follow-up C differences versus SAFEHEART-RE and Montreal-FH-SCORE excluded 0 after Holm correction, and the difference versus FH-Risk-Score was a TIE. Five-year confirmatory comparisons were TIEs. These are development and off-label ranking results, not clinic-HeFH validation and not clinical utility.*
