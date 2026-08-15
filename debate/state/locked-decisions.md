# Locked decisions

One entry per closed step. Written by the orchestrator **only** after
`bin/consensus.mjs` exits 0. Never written on the strength of a model asserting
agreement.

Format follows the ADR convention already used in this project: the decision,
why, what was rejected, and — the field that matters most — what would make us
revisit it.

---

## Template

```decision
step: NNN
title: <short noun phrase>
decided: YYYY-MM-DD
consensus_exit_code: 0
rounds_used: N
decision: <what was decided, in one or two sentences>
because: <the evidence, naming artefacts>
rejected: <the alternative and why it lost>
accepted_risks: <OBJ-NNN with named dissenter, or "none">
revisit_if: <the observation that would reopen this>
```

## Worked example

```decision
step: 000
title: UK Biobank arm is variant carriers, not familial hypercholesterolaemia
decided: 2026-08-15
consensus_exit_code: 0
rounds_used: 2
decision: The UK Biobank cohort is described throughout as "LDLR variant carriers". The FH label is retained only for the All-Wales registry arm.
because: Untreated LDL-C excess over non-carriers is +0.226 mmol/L (95% CI 0.185-0.268); 2.1% of carriers exceed 6.5 mmol/L against 0.7% of non-carriers; variant_id is empty in all 501,936 rows so pathogenicity cannot be verified; and the 395 high-confidence loss-of-function carriers show no stronger phenotype, which rules out stringency as the explanation.
rejected: Restricting to ClinVar pathogenic/likely-pathogenic - not possible, variant_id is empty. Retaining the FH label with a caveat - rejected because the phenotype does not support it in the title or abstract.
accepted_risks: none
revisit_if: The provenance of the carrier flag is established and a genuinely pathogenic subset can be identified, or variant coordinates become available.
```
