# Runbook — copy-paste text for every turn

Cursor is your editor. Agents are invoked from **its integrated terminal** using
your own subscriptions. Composer is not used and no Cursor credits are consumed.

**Thirty-second check before anything else.** Open Cursor's terminal and run:

```bash
export PATH="$HOME/.local/bin:$HOME/.hermes/node/bin:$HOME/.grok/bin:$HOME/.kimi-code/bin:$PATH"
for c in claude codex kimi grok gemini; do printf "%-8s " $c; $c --version 2>&1 | head -1; done
```

If none prompts for an API key, the subscription path works. If `gemini` is not
found, the PATH export above is why — it lives only in `~/.hermes/node/bin`.

---

## 1. Orchestrator bootstrap

Open a **separate** Claude Code session — not the one you debate in. Paste this
once:

```
You are the ORCHESTRATOR for a multi-model adversarial debate. You are NOT a
debating agent.

Read these three files now and follow them exactly:
  debate/mandates/ORCHESTRATOR.md   — your mandate and prohibitions
  debate/mandates/ROLES.md          — seating and rotation
  debate/state/open-questions.md    — the live objection register

Your loop is:
  1. Read the state files.
  2. Decide which agent goes next, for which step, per the rotation.
  3. Give me EXACTLY ONE command to paste into my terminal. Never a menu.
  4. When a round completes, RUN: node debate/bin/consensus.mjs --step NNN
  5. Report the exit code and the single next action.

Absolute constraints, from your mandate:
  - You never debate, never hold a substantive position, never break a tie on
    merits, never paraphrase an agent turn, never file an objection.
  - You never decide consensus. consensus.mjs decides. You run it and report.
  - If you want to close a step the script says is OPEN, stop — you are the
    failure mode this design exists to prevent.
  - No participant data in any state file, ever. Aggregate counts only.

Current state: step 001 is open with three unresolved objections (OBJ-001,
OBJ-002, OBJ-003) concerning whether two declared WINs are artefacts of
comparator misscoring.

Begin: read the files, then tell me the one command to paste.
```

---

## 2. Per-turn invocation strings — full matrix

Every model answers all four lenses. Round 1 is blind; round 2+ sees everything.

**Set once per shell session:**

```bash
cd /Users/nader85/Documents/CALON/calon_discordance_model_2026_08_09
export PATH="$HOME/.local/bin:$HOME/.hermes/node/bin:$HOME/.grok/bin:$HOME/.kimi-code/bin:$PATH"
export STEP=001 ROUND=1
mkdir -p debate/steps/step-$STEP
```

### Round 1 — independent and blind (all four, one command)

Each model gets the register and transcript but **not** the others' round-1
output. That blindness is the whole point; do not run round 1 twice.

```bash
node debate/bin/panel.mjs \
  --panel claude,codex,kimi,grok \
  --out debate/steps/step-$STEP/r$ROUND \
  --timeout 600000 \
  --prompt "$(cat debate/mandates/AGENT.md)

--- STEP $STEP, ROUND $ROUND (INDEPENDENT — you cannot see other models) ---
Answer ALL FOUR LENSES under their own headings.

--- OBJECTION REGISTER ---
$(cat debate/state/open-questions.md)

--- TRANSCRIPT ---
$(cat debate/state/transcript.md)"
```

Run one model alone if you prefer (substitute `--panel kimi`), or invoke a CLI
directly: `claude -p "..."`, `codex exec --skip-git-repo-check "..."`,
`kimi -p "..."`, `grok -p "..."`.

### Round 2+ — exchange and attack

```bash
export ROUND=2
node debate/bin/panel.mjs \
  --panel claude,codex,kimi,grok \
  --out debate/steps/step-$STEP/r$ROUND \
  --timeout 600000 \
  --prompt "$(cat debate/mandates/AGENT.md)

--- STEP $STEP, ROUND $ROUND (EXCHANGE) ---
Below are every other model's positions from the previous round. Engage
specifically: name the position you disagree with, the lens, and why. Do not
restate your own round-1 view.

--- ALL POSITIONS, PREVIOUS ROUND ---
$(cat debate/steps/step-$STEP/r$((ROUND-1))/*.txt)

--- OBJECTION REGISTER ---
$(cat debate/state/open-questions.md)"
```

### Consensus check

```bash
node debate/bin/consensus.mjs --step $STEP
```

## 3. What to paste back to the orchestrator

After any agent turn:

```
Turn complete: step $STEP round $ROUND, agent <name>.
State files updated. Read debate/state/open-questions.md and
debate/steps/step-$STEP/ and tell me the one next command.
```

After a consensus check:

```
consensus.mjs --step $STEP returned exit code <N>. Output:
<paste the output>
Tell me the one next command.
```

---

## 4. One complete step, cold start to locked decision

| # | Where | Action |
|---|---|---|
| 1 | Terminal | Run the thirty-second CLI check |
| 2 | Claude session B | Paste the orchestrator bootstrap |
| 3 | Orchestrator | Returns one command |
| 4 | Terminal | Paste it — Claude turn, round 1 |
| 5 | Orchestrator | Paste the "turn complete" text; get next command |
| 6 | Terminal | Codex turn, round 1 |
| 7–8 | | Repeat for Kimi and Grok |
| 9 | Terminal | `node debate/bin/consensus.mjs --step 001` |
| 10 | Orchestrator | Paste the exit code and output |
| 11 | | **Exit 1** → orchestrator starts round 2 at step 4. **Exit 2** → deadlock; orchestrator writes open risks with named dissenters. **Exit 0** → proceed |
| 12 | Orchestrator | Writes the `decision` block into `state/locked-decisions.md` |
| 13 | Terminal | Neutrality audit — a non-Claude model checks the closure: |

```bash
grok -p "Read debate/state/transcript.md and debate/state/locked-decisions.md.
The orchestrator closed step $STEP. Does the transcript support that closure, or
was an objection resolved by assertion rather than evidence? Answer only that
question. Do not re-argue the substance."
```

---

## 5. Stopping condition

`consensus.mjs` exits:

| Code | Meaning | Action |
|---|---|---|
| 0 | CLOSEABLE | Orchestrator may write the locked decision |
| 1 | OPEN | Another round. Closing anyway is forbidden |
| 2 | DEADLOCK | `MAX_ROUNDS` hit — publish the open risks with named dissenters |
| 3 | MALFORMED | Fix the register before anything else |

**Verified by adversarial test.** An objection answered by the agent that raised
it, with "we discussed it and agree" as evidence, plus a risk accepted with no
dissenter, was rejected with all four failures named. A step where only one
agent filed objections is refused as undebated. A model cannot end this by
typing a magic string.

**Deadlock is a legitimate outcome.** It gets published as an open risk with the
dissenter named. Manufacturing agreement to avoid it is the one unforgivable
move in this workflow.
