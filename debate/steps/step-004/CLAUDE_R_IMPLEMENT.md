# Claude task — CALON-G Cycle-2 in R (parallel to Codex Python)

You are Claude (opus/max). Implement the **agreed CALON-G biostat protocol in R**.
Codex is implementing the Python twin in parallel — match the same SPEC and gates.

## Locked protocol (read first)
`/Users/nader85/Downloads/CALON_DATA_PACKAGE_2026-08-13/debate-teach/CALON_G_BIOSTAT_PROTOCOL.md`

## Primary SPEC (identical to Python)
`age, sp50, male, bpmed, dm, smoke_curr, cum_nonhdl, log_tghdl, log_lpa`
Sensitivity only: replace `cum_nonhdl` with `log_apob_hdl`.

## Hard rules
- Horizon: `t_h <- pmin(time, H)`; `e_h <- as.integer(event == 1 & time <= H)`. NEVER `(time<=H)|(event==1)`.
- Assert 5y events == 97 and full events == 289 when FROZEN is built.
- Cohort SHA expected: `8c3a1e0598770c1beefe29db28d42fb7074f233f382c25c19eb0c843b59f49b2`
- Missing data: train-fold median/mode only — NOT MCAR complete-case primary.
- Ridge/penalized Cox via `glmnet` or `survival`+penalty; OOF LP for discrimination.
- B=2000 paired bootstrap for ΔC.
- SAFEHEART centred (5.4078 if PDF/text confirms). Extract coefficients from:
  `/Users/nader85/Downloads/CALON_FH_PROGRAMME_2026-08-09/04_papers/extracted_text/`
  and PDFs under `/Users/nader85/Downloads/CALON-DeepResearch/papers/`
- Do not invent coefficients; mark NOT-IN-PDF / CANDIDATE.
- Aggregates only — never print eid/NHS/DOB.
- Primary endpoint = permitted ASCVD (I50 out). MACE is NOT primary.
- Do not git commit.

## Write these files (use Write/Edit tools)

Directory A (Julius / human paste):
`/Users/nader85/Downloads/CALON_DATA_PACKAGE_2026-08-13/debate-teach/julius-cycle2-pack-R/`
- `00_findings_lock.R`
- `01_horizon_prove.R`
- `02_calong_fit.R`
- `03_comparators_pdf_faithful.R`
- `04_headtohead_tripod.R`
- `05_wales_transport.R`
- `06_calibration_dca.R`
- `README.md`
- `PROVENANCE_TABLE.md`

Directory B (repo entry):
`/Users/nader85/Documents/CALON/calon_discordance_model_2026_08_09/code/r_cycle2/16_CALON_G_CYCLE2.R`

Also write a short Markdown turn to:
`/Users/nader85/Documents/CALON/calon_discordance_model_2026_08_09/debate/steps/step-004/r-implement/claude.md`
with headings Methodology / Implementation / Adversarial audit / Clinical reality summarizing what you built.

Packages: `survival`, `glmnet`, `rms` (optional for calibrate), `jsonlite`, `digest` (sha), `boot` or manual bootstrap.

Assume data frames `FROZEN` / `wales` already exist on Julius — do not load participant CSVs from disk in the paste cells.

When done, list files written and confirm `Rscript -e 'parse(...)'` succeeds on each `.R` file if R is available.
