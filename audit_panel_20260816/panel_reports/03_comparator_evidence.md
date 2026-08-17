# Panel 2 — Comparator evidence

Source: [Panel comparator review](a07bf98e-7afa-4d05-99d3-e24ea0cb4881)

**Verdict: PARTIALLY SUPPORTED (UKB published discrimination); NOT SUPPORTED for blanket PDF-faithful / Welsh superiority claims**

## Confirmed
- SAFEHEART coefficients and worked examples match the paper extract.
- Montreal point chart matches Table 3.
- UKB full published-strict deltas in RESULTS match `calon_c_headtohead.csv`.
- Paired bootstrap design (ΔC on comparator-evaluable set, B=2000) is correct.
- Cohort gates 3540/207/124/3209/289/97/194 verified.

## Not publication-safe without caveats
- SAFEHEART LDL entered as untreated/back-calculated; PDF multivariable uses measured LDL.
- Lp(a) nmol→mg/dL ÷2.15 is NOT-IN-PDF (exploratory conversion only).
- METHODS/RESULTS claim DRAGON Lp(a) recovery, but `build_wales()` sets `lpa = np.nan` (line 263); live strict Wales SAFEHEART/FH-RS `n_eval=0`.
- Welsh 5y “wins” vs SAFEHEART/FH-RS are **refit_varset only**, not published equations.
- Montreal smoking: paper allows prior/current; code closer to current.

## Locked publication-safe wording
In UK Biobank LDLR-variant carriers free of prevalent atherosclerotic disease (n=3,209; 289 events), a pre-specified Cox model was compared with published FH risk tools on each tool’s complete-case evaluable subset using paired cluster bootstraps (B=2,000). Over full follow-up, discrimination was higher than SAFEHEART-RE (ΔC +0.032, 95% CI 0.004–0.061; n=2,470) and Montreal-FH-SCORE (ΔC +0.033, 0.012–0.056; n=2,811), and did not differ from FH-Risk-Score (ΔC +0.021, −0.001 to 0.043; n=2,282). SAFEHEART coefficients matched published worked examples, but LDL-C was entered on an untreated/back-calculated scale; UK Biobank Lp(a) was converted nmol/L→mg/dL by ÷2.15 for threshold scoring only. In the Welsh cohort, Montreal was evaluable and did not differ significantly; full SAFEHEART-RE and FH-Risk-Score were not evaluable under the strict complete-input rule in the locked CALON-C run.
