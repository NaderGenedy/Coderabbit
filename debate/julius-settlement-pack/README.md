# Julius settlement pack (draft from Round‑1 debate)

**Status:** draft for your review. Round‑2 exchange is still running; Step‑003
panel is producing fuller Julius Python. Do **not** treat WIN/LOSS claims as
settled until these scripts print matching numbers on Julius.

## Paste order on Julius

1. `00_governance_header.py` — set file names only; no paths with identifiers in prints
2. `01_cohort_ledger_ukb.py` — settle n=3333 vs 3209
3. `02_obj001_dual_safeheart.py` — Spec Kit categorical vs local continuous
4. `03_obj002_calibration_factorial.py` — centred × horizon slopes
5. `04_obj003_age_cholyears.py` — Pearson r + refit design
6. `05_wales_filter_ledger.py` — n=1159 vs 1059

## Rules

- Print **aggregates only** (n, events, C, slopes, correlations).
- Never print `eid`, NHS numbers, DOB, or row-level dumps.
- Coefficients come from Spec Kit / PDFs — never from model memory.
- After each cell, save the printed JSON/table into your Julius export folder.

## Related debate outputs

- Round 1 review: `../agent-outputs-step000-r1b/*.md`
- Round 2 (when ready): `../agent-outputs-step000-r2/*.md`
- Step 003 agent designs (when ready): `../agent-outputs-step003-r1/*.md`
