# CALON-C independent manuscript-review protocol

## Source manuscript

Read the complete file before reviewing:

`outputs/manuscript_2026-08-16/CALON_C_MANUSCRIPT_HIGH_CALIBRE.md`

Do not edit the manuscript or analysis. Produce a review only. Participant-level data must not be opened, printed, copied, or transmitted. The manuscript and aggregate artefacts may be read. Never report an identifier, participant row, family number, date of birth, or variant coordinate.

## Non-negotiable evidence window

Eligible literature must have been published from **17 August 2016 through 17 August 2026**, inclusive. Every paper used to support, challenge, compare with, or establish novelty must fall within this window.

If an important historical paper predates 17 August 2016, identify it only in an **Excluded historical context** note and do not use it as evidence for a manuscript claim. Do not silently breach the date window.

Prioritise, in order:

1. directly relevant FH/LDLR cohorts, prediction-model validations, guidelines, and methodological standards;
2. systematic reviews, major prospective cohorts, randomised evidence, and high-quality prediction-methods papers;
3. the highest-impact specialist journals available when top general journals contain no directly relevant evidence.

Journal prestige never compensates for population, outcome, or estimand mismatch.

## Research-tool requirements

Attempt to invoke or use any genuinely available `/academic` skill and the existing Scite AI, SciSpace, and Elicit integrations. Also use the agent's native scholarly/web-search tools where available.

For each named research tool, report exactly one status:

- **USED — results returned**: state what was retrieved and how it informed the review.
- **AVAILABLE BUT FAILED**: give the actual failure or authentication message.
- **NOT EXPOSED/NOT CONFIGURED**: the tool was not callable in this runtime.

Do not imply that Scite, SciSpace, Elicit, PubMed, Crossref, or any other service was consulted unless it actually returned results. Search snippets are discovery aids, not verification. Verify article metadata and DOI against a primary bibliographic record, publisher page, PubMed, or Crossref before treating the paper as verified. Mark unresolved citations **UNVERIFIED — DO NOT CITE**.

## Independence and assigned seats

In blind round 1, do not seek, read, or infer another model's or external subagent's output. Follow the specialist-seat structure in your invocation prompt. If assigned one specialist seat, remain within that lens. If assigned an internal four-seat panel, keep the Biostatistician, Cardiologist, Lipid-medicine specialist, and Senior Editor-in-Chief voices distinct; do not collapse them into an anonymous consensus. Cross-agent exchange is permitted only in the explicitly labelled debate round.

## Paragraph-by-paragraph review

Number paragraphs within each section in manuscript order, for example `Abstract ¶1`, `Methods—UK Biobank cohort ¶2`, and `Discussion—Competing risks ¶1`.

For **every substantive prose paragraph** from Key points through Conclusion, provide:

1. **Current claim** — one precise sentence.
2. **Weakness or unsupported element** — design mismatch, overreach, missing evidence, ambiguity, internal inconsistency, or reporting gap.
3. **Evidence check** — recent supporting and challenging literature within the eligible window, with journal, year, population/design, relevant finding, and verified DOI or stable identifier.
4. **Required improvement** — an actionable change.
5. **Suggested replacement wording** — when precision, causal language, or emphasis requires revision.
6. **Severity** — `FATAL`, `MAJOR`, `MODERATE`, or `MINOR`.

Do not pad a paragraph with tangential citations. State **insufficient validated evidence within the 10-year window** where appropriate.

## Whole-manuscript analyses

After the paragraph review, include:

### A. Novelty map

Separate:

- genuinely new;
- incremental but useful;
- already established;
- unsupported priority claims.

Name the closest overlapping work and explain the precise overlap and residual novelty.

### B. Agreement and disagreement with recent evidence

For each important supportive or contradictory paper, classify any conflict as:

- methodological;
- population/ascertainment-driven;
- endpoint/estimand-driven;
- implementation/calibration-driven; or
- substantive biological or clinical disagreement.

### C. Internal manuscript consistency audit

Check every repeated cohort count, event count, horizon, C-statistic, confidence interval, comparator definition, calibration statement, transport label, and limitation for contradictions within the manuscript. Do not recalculate from participant data.

### D. Reporting and publication audit

Assess TRIPOD+AI, PROBAST, STROBE, RECORD, calibration, clinical utility, competing risks, missing data, family clustering, fairness, reproducibility, citation fidelity, and whether the claimed contribution fits a high-impact cardiovascular or lipid journal.

### E. Top revisions

Rank the ten highest-impact revisions. Put rejection-level issues first and cosmetic changes last.

### F. Inter-panel tension memo

Predict the strongest point on which your lens will disagree with the other two lenses. Do not smooth the tension over.

## Output rules

- British English.
- Academic prose; no praise padding or marketing.
- Effect sizes and 95% confidence intervals before p values.
- A positive point estimate with an interval crossing zero is a **TIE**.
- No causal interpretation of predictive associations.
- Do not call Wales an independent external validation.
- Do not call the endpoint MACE.
- Do not infer variant pathogenicity beyond the available `ldlr_carrier` flag.
- Do not claim clinical utility without comparative decision-curve evidence.
- Distinguish internal calibration from transported/external calibration.
- Use `associated with` unless the design supports stronger language.

Begin with a one-page **Rejection-risk summary**, then the paragraph review, then the whole-manuscript analyses, the research-tool status table, and the eligible evidence ledger. End with a section titled **Claims that must be deleted unless new evidence is produced**.
