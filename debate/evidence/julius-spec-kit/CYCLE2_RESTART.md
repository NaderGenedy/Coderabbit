# Cycle 2 restart — 15 August 2026 (night)

Built from your Julius Spec-kit run. Cycle 1 did **not** lock a publishable
confirmatory head-to-head. Cycle 2 starts from the frozen cohort you reproduced
and from the defects you found.

## What Julius locked (do not reopen without a hash change)

| Quantity | Value |
|---|---|
| LDLR carriers | 3,540 |
| Prevalent ASCVD exclusions (atherosclerotic components only) | 207 |
| Undated exclusions | 124 |
| Frozen incident cohort | **3,209** |
| Full-follow-up events | **289** |
| 5-year events | **97** |
| 10-year events | **194** |
| Frozen-cohort SHA-256 | `8c3a1e0598770c1beefe29db28d42fb7074f233f382c25c19eb0c843b59f49b2` |

Any cell that does not reproduce these counts is **fail-loud**, not negotiable.

## Cycle 1 defects that carry into Cycle 2 (must be fixed first)

1. **Horizon mask invalid** — `(time <= H) | (event == 1)` keeps post-horizon events.
   Your 5-year set had **146** events instead of **97**. All `cell_09` / `cell_13`
   horizon results are **withdrawn**. Correct form:

   ```python
   t_h = np.minimum(time, H)
   e_h = (event == 1) & (time <= H)
   ```

2. **Compact `01_cohort_ledger_ukb.py`** — prevalence not restricted to permitted
   atherosclerotic components → 235 / 3,181 (wrong). Use the settlement definition
   that yielded 207 / 3,209.

3. **Compact `02_obj001_dual_safeheart.py`** — dropped survivors without death date
   → 429 / 269 (wrong). Must score the full frozen 3,209.

4. **SAFEHEART centring** — omitting `5.4078` is confirmed broken (5y mean risk
   77% vs 1.22% centred; slopes 0.166 vs 0.871). Cycle 2 comparators are
   **centred Spec-kit forms only**, PDF-checked.

5. **Age × cholesterol-years** — r = **0.606** (age × cum non-HDL r = **0.577**).
   Does **not** trip a 0.999 drop rule. Age HR stays ~1.03–1.05 across refits.
   Collinearity is real but not the “extreme structural” story from Cycle 1.

6. **Confirmatory tally 68 TIE / 9 LOSS / 1 WIN** — mechanical only; **not
   publishable**. Comparators not PDF-verified; Lp(a) used exploratory ÷2.15;
   B=300 not 2000; horizon mask invalid.

## Cycle 2 objective (locked framing)

**Not:** search until the model wins or ties every comparator in every stratum.

**Yes:** pre-specify **CALON-G**, freeze the covariate set and fitting protocol
*before* looking at head-to-head deltas, then report WIN / TIE / LOSS honestly
on the frozen SHA cohort with PDF-faithful centred comparators and the corrected
horizon definition.

If the result is mostly TIEs and a few LOSSes, that is the result. Searching for
universal WINs after seeing the matrix is the same outcome-informed path that
added BMI in Cycle 1 and is already on the record as a Methods vulnerability.

## CALON-G candidate specification (your list)

| Term | Role | Notes |
|---|---|---|
| `age` + age spikes (`sp18`, `sp30`, `sp50`) | Time scale | Spikes are the functional form of age, not extra clinical variables. Collinearity guard: drop only exact duplicates (r≥0.999) **or** report VIF; do not pretend 0.999 controls age–spike sharing |
| `male` | Sex | |
| `smoke` | Smoking | Align to SAFEHEART/FH-RS definition (current vs ever) in the Methods; do not silently switch |
| `bpmed` / HTN medication | Hypertension | Prefer **medication** as you specified, not the broader `htn_any`, unless completeness forces a documented fallback |
| `dm` | T2DM | |
| `log_tghdl` | log(TG/HDL) | |
| `cum_nonhdl` **or** grey-zone `log_apob_hdl` | Lipid burden | Pre-specify **one primary**. Keep the other as a single sensitivity, not both in the primary LP |
| `log_lpa` or `lpa_hi` | Lp(a) | UKB scale; document unit. Wales may lack a comparable assay — state transport limit |

**Primary recommendation for the locked SPEC (one row):**

```text
age, sp50, male, bpmed, dm, smoke, cum_nonhdl, log_tghdl, log_lpa
```

- Keep `sp18`/`sp30` in the candidate pool only if the collinearity guard can
  actually drop them when out of range (as in Cycle 1).
- Do **not** put both `cum_nonhdl` and `log_apob_hdl` in the primary model.
  Put `log_apob_hdl` in sensitivity `CALON-G-grey`.

This expands Cycle 1’s published 8-term set by adding **Lp(a)** and switching
HTN to **medication**. That is a **new model**, disclosed as Cycle 2
re-specification after settlement — not a silent continuation of CALON-F.

## Comparator lock (PDF paths you supplied)

| Score | PDF | Text extract |
|---|---|---|
| SAFEHEART-RE | `CALON-DeepResearch/papers/SAFEHEART-RE_PerezDeIsla_2017.pdf` (+ suppl) | `…/extracted_text/SAFEHEART_RE_Circulation_2017_.txt` |
| FH-Risk-Score | `…/FH-Risk-Score_Paquette_2021.pdf` (+ suppl) | `…/FH_RS_ATVB_2021_.txt` |
| Montreal-FH-SCORE | `…/Montreal-FH-SCORE_Paquette_2017_derivation.pdf` (+ validation) | `…/MONTREAL_orig_JCL_2017_.txt` |

Cycle 1 claim “no Montreal PDF” is **false for the Mac** — sources live outside
the discordance tree. Cycle 2 must fill the provenance table from these files
before any WIN is quoted.

## Paste order on Julius (Cycle 2 pack)

Folder: `debate-teach/julius-cycle2-pack/`

1. `00_findings_lock.py` — assert SHA + reference counts
2. `01_horizon_correct.py` — define `horizon_risk_set()`; prove 5y events = 97
3. `02_comparators_pdf_faithful.py` — centred SAFEHEART + PDF coefficients only
4. `03_calong_fit.py` — fit CALON-G OOF on frozen 3,209
5. `04_headtohead.py` — full × 5y × subgroups; B=2000; no invalid mask
6. `05_wales_transport.py` — only after UKB lock; genotype Positive1 = 2,405 start

## Success criteria for Cycle 2 (when to stop)

- Frozen SHA reproduced every run.
- 5-year events in any horizon analysis = **97** (not 146).
- Every comparator row cites PDF page/table or is labelled `CANDIDATE`.
- Head-to-head table published in full (no selective WIN narrative).
- Multiplicity + optimism warnings printed beside any tally.
- No further covariate added after seeing the WIN/TIE/LOSS matrix.

## Single next action

On Julius: paste `julius-cycle2-pack/00` → `01` and confirm **97** five-year events
and SHA `8c3a1e05…`. Only then fit CALON-G.
