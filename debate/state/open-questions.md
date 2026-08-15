# Objection register

**This file is the consensus engine.** `bin/consensus.mjs` parses it and decides
whether a step may close. Nothing else decides that — not a model saying
"consensus reached", not the orchestrator's judgement.

## How to file an objection

Write a fenced ` ```objection ` block. Free prose between blocks is ignored, so
argue as much as you like around them; only the blocks are parsed.

**Required fields** — a block missing any of these makes the whole register
MALFORMED and blocks every step until fixed:

| Field | Meaning |
|---|---|
| `id` | `OBJ-NNN`, unique, never reused |
| `step` | the step number this belongs to |
| `raised_by` | `claude` \| `codex` \| `kimi` \| `grok` \| `gemini` |
| `claim` | the specific, checkable thing you say is wrong |
| `settled_by` | what evidence would settle it — name the test, not "further discussion" |
| `status` | `OPEN` \| `ANSWERED` \| `ACCEPTED-RISK` \| `WITHDRAWN` |

**Conditional fields:**
- `status: ANSWERED` → `evidence` naming a file, path or number, **and**
  `answered_by` which must differ from `raised_by`
- `status: ACCEPTED-RISK` → `dissenter` (a name) and `risk_text` (≥10 chars)
- `status: WITHDRAWN` → `withdrawn_because` (≥10 chars)

## Rules the script enforces, which you cannot talk your way past

1. **You may not close your own objection.** `answered_by` must differ from
   `raised_by`.
2. **"We agree" is not evidence.** `evidence` must contain a path, filename or
   number. Prose consensus does not resolve anything.
3. **Accepting a risk requires a name against it.** Anonymous acceptance is how
   disagreement gets quietly smoothed away.
4. **A step with objections from fewer than two agents cannot close.** A step
   nobody challenged has not been debated, it has been rubber-stamped.
5. **MAX_ROUNDS is enforced in code.** Hitting it writes DEADLOCK. Deadlock is a
   legitimate outcome and gets published as an open risk with the dissenter
   named. Manufacturing agreement to avoid it is the one unforgivable move.

---

## Live objections

The three below are real and unresolved, taken from an independent appraisal of
the Julius analysis run on 14 August 2026. They are seeded here deliberately: a
cold model reading this file must have something substantive to bite on, and
these are the sharpest open questions in the project.

```objection
id: OBJ-001
step: 001
raised_by: kimi
claim: Both declared WINs rest on comparator C-indices that disagree with the local pipeline in one direction only. Julius reports SAFEHEART C=0.628 and FH-Risk-Score C=0.651 in UK Biobank; the local pipeline gets 0.6944 and 0.6740. Substituting the local values turns SAFEHEART 10-year from +0.079 [0.033,0.123] WIN to +0.013 TIE, and FH-RS from +0.052 [0.001,0.104] WIN to +0.030 TIE. Montreal, the only comparator needing neither Lp(a) nor LDL-C bands, reproduces to 0.003. The asymmetry is not random.
settled_by: Score all three comparators from the coefficients printed in the source PDFs on disk, on one identical frozen cohort extract, and publish a provenance table with predictors, coefficients, endpoint, horizon and derivation cohort for each. Then recompute both deltas.
status: OPEN
```

```objection
id: OBJ-002
step: 001
raised_by: grok
claim: All four comparator calibration slopes cluster at 0.52-0.57. Three independently derived scores do not spontaneously agree on a uniform ~2x compression of the linear predictor. That signature indicates a shared implementation error - most likely baseline survival applied at the wrong horizon, or the linear predictor not centred on its derivation-cohort mean - not three coincidental miscalibrations.
settled_by: Recompute one comparator two ways, centred and uncentred, and at both 5-year and 10-year baseline survival. If the slope moves from ~0.55 toward 1.0 under one variant, the bug is identified. Report the slope under each variant.
status: OPEN
```

```objection
id: OBJ-003
step: 001
raised_by: codex
claim: Age carries HR 1.20 [0.91-1.60] - null - for 5-year incident ASCVD, which does not happen in real data. Age and cholesterol-years (defined as age x untreated total cholesterol) sit in the same model and both come out null (1.20 and 1.15). This is the collinearity the specification explicitly required a check for; the correlation with age was never reported and the drop rule at 0.999 was never applied. Every coefficient in the preferred model is suspect until resolved.
settled_by: Report the Pearson correlation between age and cholesterol-years in the analysis cohort, and refit with cholesterol-years replaced by untreated total cholesterol alone. If the age HR moves away from null, the collinearity is confirmed.
status: OPEN
```

## Worked example — what a resolved objection looks like

```objection
id: OBJ-000
step: 000
raised_by: kimi
claim: The UK Biobank arm is described as familial hypercholesterolaemia, but the carrier flag may not identify FH.
settled_by: Compare untreated LDL-C in flagged carriers against non-carriers and against the +3 to +4 mmol/L expected for heterozygous FH.
status: ANSWERED
answered_by: claude
evidence: verify/01_endpoints_htn_hf_mace.py output; median excess +0.226 mmol/L (95% CI 0.185-0.268), 2.1% of carriers above 6.5 mmol/L, variant_id empty in all 501936 rows
```
