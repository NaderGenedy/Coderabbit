# Neutrality audit log

Every closure declared by `bin/consensus.mjs` is audited by a model from a
different vendor than the one that dispositioned the objections. The auditor
files no objections and answers one question: does the record support the
closure? A `NOT SUPPORTED` verdict reverts the closure. The orchestrator does
not overrule an audit on the merits.

---

## Step 001 — closure REVERTED, 15 August 2026

- **Closure claimed:** `consensus.mjs --step 001` exit 0, CLOSEABLE, 3 of 3
  ACCEPTED-RISK
- **Dispositioned by:** claude alone, in step-000 round 3
- **Auditor:** grok-4.6/xhigh (different vendor)
- **Verdict:** `NOT SUPPORTED`
- **Full turn:** `debate/steps/step-001/audit/grok.md`

The auditor's three load-bearing findings, each checkable against the files:

1. `PROMPT_R3_SETTLEMENT.md` permits `ACCEPTED-RISK` only for a defect that is
   **agreed** and **Julius-blocked**. Neither half holds. No raiser was present
   to agree: kimi was never invoked in round 3 (403 usage limit), codex errored
   out, grok's turn was a 961-character fragment. OBJ-002 is actively contested
   by codex's OBJ-017, which calls the factorial non-diagnostic — and Claude's
   own `risk_text` records that disagreement and parks the parent anyway.
2. Claude's own `risk_text` on OBJ-001 states that `SAFEHEART_2017.pdf`
   (sha `2859d29d7b8e93ba`) is **on this machine**, so extracting the published
   coefficients is a local task. Codex's OBJ-017 unit test needs no participant
   data either. Calling both Julius-blocked is a skip, not a block.
3. Step 001 has no `rN/` directories, so `rounds` is 0 and the DEADLOCK valve
   cannot fire. CLOSEABLE was therefore reachable with no round of debate on the
   step at all — the letter of the schema, not consensus. `agents_engaged` was
   satisfied by the seeding agents, not by anyone who engaged in round 3.

`AGENT.md` permits leaving another agent's objection OPEN or answering it with an
artefact. It does not permit softening it. OBJ-001, OBJ-002 and OBJ-003 are
returned to OPEN.

**Action taken:** no entry written to `locked-decisions.md`. The three
objections are OPEN. The local half of OBJ-001 (the coefficient provenance
table from the two PDFs on disk) and OBJ-017's unit test are now scheduled as
local work rather than deferred to Julius.

**Panel defects this audit exposed**, all fixed in `bin/panel.mjs`:

| Defect | Effect | Fix |
|---|---|---|
| Grok ran with the default permission mode | Turn died `stopReason=Cancelled` on its first tool call; three rounds recorded ~600-1000 character narration fragments that looked like weak answers rather than blocked ones | `--permission-mode bypassPermissions` |
| Grok ran with `--output-format plain` | Only inter-tool narration reached stdout; the final message was dropped | `--output-format json`, extract `.text`, surface `stopReason` when it is not `EndTurn` |
| Auth heuristic scanned stderr, which for `codex exec` echoes the transcript | An agent writing "forbidden" or "unauthorised" flagged its own turn as an auth failure; a 7,421-character codex answer was overwritten with `[UNAVAILABLE]` | Heuristic consulted only when stdout is empty; raw streams now always kept as `<agent>.stderr.log` and `<agent>.raw-stdout.log` |
| `models_cache.json` corruption | `missing field base_instructions at line 95` killed codex for two rounds | Cache cleared and regenerated |

---

## Step 000 — closure NOT WRITTEN, 15 August 2026

- **Closure claimed:** `consensus.mjs --step 000` exit 0, CLOSEABLE at round 4/4
  (0 OPEN, 4 ANSWERED, 20 ACCEPTED-RISK, 3 WITHDRAWN)
- **Auditor:** grok-4.6/xhigh
- **Verdict:** `NOT SUPPORTED`
- **Full turn:** `debate/steps/step-000/audit/grok.md`

Auditor's split:

1. **(a) Legitimate.** OBJ-028 answered cross-vendor with
   `r4/code/obj028_residuals.tsv` (69/69 non-zero residuals). OBJ-029 parked
   honestly by both codex and grok because the on-disk QC JSON is still the
   superseded 10-term model.
2. **(b) Same skip as Step 001.** Nineteen ACCEPTED-RISK entries still carry
   `dissenter: claude` from the single-agent Round-3 turn. Raisers of the 13
   non-Claude ids never agreed. Claude's own `risk_text` admits local work on
   several of them (OBJ-012, 014–019, 022, 024). Round 4 was prompted only on
   028/029, so those parks were never re-examined by another vendor.

**Action taken:** no entry written to `locked-decisions.md`. Schema CLOSEABLE
stands in `consensus.mjs` output; the orchestrator treats the audit veto as
binding. Auditor recommendation (return the 13 other-agent r3 parks to OPEN, or
publish DEADLOCK with raisers named) is deferred — user paused code work after
supplying the missing comparator PDF paths under
`/Users/nader85/Downloads/CALON-DeepResearch/papers/`.
