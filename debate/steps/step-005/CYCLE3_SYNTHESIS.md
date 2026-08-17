# Cycle-3 synthesis — grey-zone adjunct (16 August 2026)

**Panel:** Step-005 Round 1 — Claude, Codex, Kimi, Grok (**4/4 OK**)  
**Outputs:** `debate/steps/step-005/r1/` · teach mirror `debate-teach/agent-outputs-step005-r1/`

## Cross-vendor consensus (supported by all four)

1. **Keep the locked CALON-G primary as confirmatory.**  
   SPEC unchanged: `age, sp50, male, bpmed, dm, smoke_curr, cum_nonhdl, log_tghdl, log_lpa`.  
   Cycle-2 R pilot (B=300, exploratory ÷2.15) stays labelled exploratory: C_oof≈0.705; WIN=10 / TIE=44; ALL TIE vs SAFEHEART & FH-RS, WIN vs Montreal.

2. **Grey-zone Lp(a)+apoB/LDL is exploratory only.**  
   It does **not** replace the primary. Comparator LOSSes are results, not tuning signals. Chasing WIN in every direction is forbidden.

3. **Deployment architecture (if tested):**
   - **Stage A (accessible core):** 8 terms — primary without `log_lpa` / apoB.  
   - **Band (locked now):** middle tertile of Stage-A **OOF** risk (sensitivity named now only: middle quintile).  
   - **Stage B (in-band, assays present):** `log1p(Lp(a)_nmol)` + `log(apoB/untreated_LDL)` once each, ideally as an **offset** on frozen Stage-A LP.  
   - Missing assays → Stage A (or confirmatory primary when full panel is the care path).

4. **Primary adjunct endpoint is not another comparator matrix.**  
   One primary exploratory contrast: **in-band hybrid vs Stage-A** (ΔC and/or net benefit). Claude: name NB of P2 vs full-assay Stage-A+lpa policy at 10% 10y. Others: in-band OOF ΔC + DCA. Comparator re-scoring of the adjunct is secondary/labelled if done at all.

5. **Promotion to confirmatory is effectively blocked this programme.**  
   Wales lacks comparable apoB (and Lp(a) scale differs). Without external transport of Stage-B, no “universal winner” / clinical-promotion claim.

6. **If gates fail or events in-band &lt;10 → keep primary alone.**

## Objections filed (must clear before adjunct fit)

| Agent | Issue |
|---|---|
| Claude | In-band ΔC vs Stage-A alone is range-restricted by construction → include locked primary / full-assay policy as comparator; name primary NB cell now |
| Claude | Treatment-contaminated `apoB/LDL_unt` → co-report on-treatment form + statin stratification |
| Claude / Kimi / Grok | Print assay+event census in band **before** Stage-B fit; stop if &lt;10 events |
| Codex / Kimi / Grok | Nested CV: band cutoffs from training folds only; no full-cohort enhancer leakage |

## Recommendation (programme decision)

| Path | Decision |
|---|---|
| Confirmatory paper | **CALON-G 9-term primary** only (B=2000, PDF-faithful, Wales transport) |
| Assay-economy question | Optional **labelled exploratory** two-stage adjunct under the gates below |
| If adjunct null / underpowered / untransportable | **Keep winner (primary)** — do not engineer a WIN |

### Adjunct acceptance gates (exploratory label only)

1. Cohort SHA + 289/97/194  
2. Band census printed; in-band events ≥10 (else stop)  
3. Nested OOF; Stage-B offset; no Stage-A re-entry  
4. B=2000 for any reported adjunct ΔC / NB  
5. Calibration + DCA in-band at pre-specified thresholds  
6. Full cell dump; multiplicity warning  
7. No Wales universal-winner language for Stage-B  

## Next implementation (when ready)

- R: `julius-cycle2-pack-R/07_greyzone_adjunct.R` (census → nested fit → in-band metrics)  
- Python twin: `julius-cycle2-pack/07_greyzone_adjunct.py`  
- Do **not** start until assay/event census gate is printed.

## Artefacts

- Prompt: `debate/steps/step-005/PROMPT_R1_CYCLE3.md`  
- Panel: `claude.md`, `codex.md`, `kimi.md`, `grok.md`  
- Cycle-2 pilot: `debate/evidence/julius-spec-kit/cycle2_r_pilot/`
