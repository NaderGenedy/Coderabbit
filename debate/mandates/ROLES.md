# Full-matrix protocol — every model plays every lens

## The design

There are no fixed seats. On every step, **each model independently produces a
position under all four lenses**, blind to the others. Only then do they
exchange and attack.

| | Methodology | Implementation | Adversarial audit | Fifth lens |
|---|---|---|---|---|
| **Claude** | ✓ | ✓ | ✓ | ✓ |
| **Codex** | ✓ | ✓ | ✓ | ✓ |
| **Kimi** | ✓ | ✓ | ✓ | ✓ |
| **Grok** | ✓ | ✓ | ✓ | ✓ |
| *Gemini* | optional | optional | optional | optional |

Sixteen independent positions per step from four models, then debate.

## Why this beats fixed seats

With one seat each, a disagreement is confounded: when the audit seat contradicts
the methodology seat you cannot tell whether that is a real conflict or just two
different jobs producing different emphases. Worse, a wrong seat assignment hides
a model's best insight — if Grok would have caught the collinearity but Grok was
assigned implementation, the catch never happens.

With the full matrix, every disagreement is **four models answering the same
question**. That is a signal you can act on. It also removes the need for
rotation entirely: nobody settles into a stance, because everybody argues every
position on every step.

The cost is roughly four times the invocations. For the stages that matter —
specification, gaps, analysis choice — that is worth paying. For mechanical
checklist work it is not; see the triage table below.

## The four lenses

Each model answers all four, in one turn, clearly separated by heading.

**1. Methodology.** Is the estimand right? Does the design answer the question
asked? Are the reporting standards met? Would a reviewer accept the inference the
design licenses?

**2. Implementation.** Would the code actually do what it claims? Is anything
silently degrading — a check that cannot fail, a filter excluding its own target,
a default swallowing an error? Is it reproducible from the stated inputs?

**3. Adversarial audit.** Assume the conclusion is wrong. What is the most likely
way it is wrong? What would have failed if it were? Attack the strongest version
of the claim, not a weak paraphrase.

**4. Fifth lens — clinical and publication reality.** Would a lipidologist
believe this? Does it change practice? Where does a hostile reviewer open? Is
anything over-claimed relative to what the numbers support?

## Round structure

**Round 1 — independent, blind.** Each model receives the step question, the
objection register and the transcript, but **not** the other models' round-1
output. Four turns, four models, all four lenses each. No cross-talk.

**Round 2+ — exchange and attack.** Each model now receives every other model's
positions and must engage specifically: name which position it disagrees with,
under which lens, and why. Filing no objection requires stating what was checked
and why it held.

**Close.** `bin/consensus.mjs` decides. Never a model, never the orchestrator.

## Where the full matrix earns its cost

| Stage | Protocol | Why |
|---|---|---|
| Project specification | **Full matrix** | Framing errors are the expensive ones |
| Requirements | Full matrix | Cheap relative to the cost of an omission |
| **Gaps / missing pieces** | **Full matrix — highest value** | Where every real defect in this project was found |
| Best-suited analyses | Full matrix | Genuine methodological disagreement |
| Explicit reasoning per choice | Full matrix | This is the record that survives peer review |
| TRIPOD / STROBE mapping | **One model, one pass** | Mechanical checklist; sixteen positions on a tick-box is theatre |
| Hallucination detection | Full matrix, bounded | Catches internal fabrication; cannot verify a published number |
| QC vs prior studies | One model + human | Bounded by literature access |

## The honest limit on hallucination detection

Cross-model disagreement reliably catches **internal** fabrication: invented
coefficients, numbers contradicting a state file, claims with no named artefact.
Four models each running an audit lens catches this far better than one.

It cannot establish that a published C-index is real. Four models can agree on a
wrong remembered number, and they will do so confidently. That check is human,
against the PDFs on disk. Extract comparator coefficients from those PDFs and
never from any model's memory — this project has already shipped comparator
functions carrying invented weights while their docstrings claimed published
provenance, and no amount of cross-model agreement would have caught it.
