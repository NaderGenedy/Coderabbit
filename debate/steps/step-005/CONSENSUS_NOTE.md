# Where the consensus is — 16 August 2026

Consensus is decided only by `debate/bin/consensus.mjs`, never by an agent
saying so. A cross-vendor neutrality audit must also pass before any locked
decision is written. The table below is an **orchestrator status**, not a lock.

## Verdicts right now

| Step | Verdict | Exit | Round | Notes |
|---|---|---|---|---|
| 000 — resource audit | CLOSEABLE by schema; audit NOT SUPPORTED — no lock | 0 | 4 of 4 | Grok neutrality NOT SUPPORTED |
| 001 — comparator WINs | OPEN | 1 | 1 of 4 | OBJ-001/003/030/031 open |
| 004 — Cycle-2 CALON-G lock | Panel ran; R implement + R pilot done | — | r1 | Confirmatory SPEC frozen |
| **005 — Cycle-3 grey-zone** | **Panel 4/4 complete; synthesis written** | — | r1 | Exploratory adjunct only |

## Cycle-3 panel result (live)

| Agent | Status | Recommendation (clinical §4) |
|---|---|---|
| Claude | OK · 21.5 KB | Deploy two-stage as **exploratory/labelled**; promotion foreclosed (Wales no apoB) |
| Codex | OK · 17.1 KB | Promote adjunct **only if named gates pass**; else keep CALON-G |
| Kimi | OK · 15.2 KB | Deploy exploratory/labelled; gate 6 (Wales transport) currently unmeetable |
| Grok | OK · 26.7 KB | Promote only if gates pass; else **keep locked primary alone** |

**Cross-vendor agreement:** keep the 9-term CALON-G primary confirmatory; grey-zone
`log_lpa` + `log(apoB/LDL)` is exploratory only; do not chase comparator WINs
with the adjunct.

## Cycle-2 R pilot (still exploratory: B=300)

- Gates PASS: n=3209; events 289 / 97 / 194
- C_oof ≈ 0.705; tally WIN=10 / TIE=44
- ALL: TIE vs SAFEHEART & FH-RS; WIN vs Montreal

## Artefacts to open now

- Panel Markdown: `debate-teach/agent-outputs-step005-r1/{claude,codex,kimi,grok}.md`
- Synthesis: `debate-teach/step-005/CYCLE3_SYNTHESIS.md`
- Spec: `debate-teach/step-005/GREYZONE_IMPLEMENTATION.md`
- Protocol addendum: `debate-teach/CALON_G_BIOSTAT_PROTOCOL.md` (Cycle-3 section)
