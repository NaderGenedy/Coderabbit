# Debate panel — pinned highest reasoning models

Verified on this machine 2026-08-15. `bin/panel.mjs` hard-pins these so Julius-facing
debate turns do not silently fall back to weaker defaults.

| Seat | CLI | Model | Reasoning effort |
|---|---|---|---|
| Claude | `claude` | `opus` | `max` |
| Codex | `codex exec` | `gpt-5.6-sol` | `ultra` |
| Kimi | `kimi` | `kimi-code/k3` | `max` (model default + thinking) |
| Grok | `grok` | `grok-4.6` | `xhigh` |

Claude print mode uses `--dangerously-skip-permissions` (not sandbox data — prompt-only
debate). Empty `--tools ''` currently breaks with a bad MCP schema (HTTP 400); do not
re-enable until that is fixed.

Outputs are always written as human `.md` plus raw `.txt`.
