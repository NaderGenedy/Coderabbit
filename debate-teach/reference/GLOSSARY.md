# Full-matrix debate glossary

Language for governing Claude / Codex / Kimi / Grok panels on CALON. Lens ≠ seat.

## Terms

**Agent**:
One subscription CLI on the panel: `claude`, `codex`, `kimi`, or `grok`.
_Avoid_: Seat, role, “the auditor”

**Lens**:
One of four question types every agent must answer in a single turn: Methodology, Implementation, Adversarial audit, Fifth (clinical/publication).
_Avoid_: Seat, job title for a model

**Full matrix**:
Every agent answers every lens each step (4×4 = 16 positions), then debates — no fixed seating.
_Avoid_: Round-robin seats, role rotation as the primary design

**Round-1 blindness**:
Agents see the brief, register, and transcript, but not other agents’ round-1 outputs.
_Avoid_: Parallel brainstorm with shared draft

**Objection**:
A checkable claim filed in an `objection` fence with `settled_by` naming a runnable test.
_Avoid_: “Concern”, “feels off”, “needs more discussion”

**ANSWERED**:
Objection status only when `evidence` names a file/path/number and `answered_by` ≠ `raised_by`.
_Avoid_: “We discussed and agree”

**ACCEPTED-RISK**:
Unresolved disagreement published with a named `dissenter` and written `risk_text`.
_Avoid_: Silent compromise, anonymous acceptance

**DEADLOCK**:
`MAX_ROUNDS` hit with objections still OPEN — a legitimate published outcome, not a failure to be papered over.
_Avoid_: Forced consensus

**consensus.mjs**:
The only closer. Exit 0 closable, 1 open, 2 deadlock, 3 malformed. Orchestrator runs it; does not judge merits.
_Avoid_: Model-declared “consensus reached”

**Gate 0**:
Subscription-auth preflight for all four CLIs before any panel dispatch (`subscription-preflight.mjs`).
_Avoid_: Hoping Cursor terminal “just works”
