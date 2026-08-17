# FOR ALL AGENTS — Julius Spec-kit dump

Read this directory before arguing about OBJ-001 / 002 / 003, cohort n, or any
WIN/TIE/LOSS tally.

Key facts already locked in `spec_kit_execution_report.md` and
`calon_settlement_out/spec_frozen.json`:

- Frozen UKB: n=3209, events=289, 5y=97, 10y=194
- SHA-256: 8c3a1e0598770c1beefe29db28d42fb7074f233f382c25c19eb0c843b59f49b2
- Confirmatory tally is NOT publishable (invalid horizon mask; unverified comparators)
- Uncentred SAFEHEART is broken; centred form is required
- Age × chol-years r ≈ 0.606 (does not trip 0.999)

Full zip: `calon_spec_kit_outputs.zip` in this folder.

## Cycle-2 CALON-G biostat lock (15 Aug night)

Read `CALON_G_BIOSTAT_PROTOCOL.md` in this folder. Key rules:

- Reverse-engineer from **comparator domains + biology**, not from subgroup WIN/LOSS.
- Primary endpoint remains permitted ASCVD (I50 out). MACE is a separate sensitivity with its own SHA.
- Do **not** assume MCAR; primary = fold-wise train-only imputation; MICE under MAR as sensitivity.
- External validation = Wales with **frozen UKB coefficients** (TRIPOD+AI).
- Primary SPEC: age, sp50, male, bpmed, dm, smoke_curr, cum_nonhdl, log_tghdl, log_lpa
