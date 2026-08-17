# Panel 4 — Raw provenance / reproducibility

Source: [Panel provenance review](fc63330e-4f8a-4089-a0d7-fb72f239a88e)

**Verdict: AGREE WITH CONDITIONS**

**Tally:** 56 PASS · 9 FAIL · 3 UNVERIFIED

## What holds
- Script hashes 32/33/34/07 match METHODS appendix.
- Raw file hashes match `raw_reproduction.json`.
- UKB gates 3540→3209 / 289·97·194 and Wales 1159 / 92·44·66 reproduce.
- Endpoint construction (athero-only, I50 non-event, S1=147) PASS.
- Train-fold median imputation PASS; CV/ΔC cluster-awareness PASS for folds/bootstrap.
- UKB Lp(a) ÷2.15 for comparator thresholds PASS.
- DRAGON unit evidence (ratio ≈4.65; 32.6% ≥105 nmol) PASS as folklore, **not** as CALON-C wiring.
- Aggregate governance PASS; SAFEHEART worked examples PASS.

## FAIL conditions that must close
1. METHODS/audit stop claiming Welsh DRAGON Lp(a) is used by CALON-C (or wire and test the join).
2. METHODS stop claiming family-clustered Welsh optimism (or fix `34`).
3. Replace hard-coded Wales Downloads paths with env/resolver pattern.
4. Pre-specify `usable()` inside training folds (or document full-sample term gating).
5. Pin dependencies; hash-pin `35`; implement comparator DCA or fix docstring.
6. Treat `audit_panel` as ledger echo of `33`, not independent Level-2 rebuild.

## UNVERIFIED
- `35` SHA not in METHODS appendix.
- `dayfirst=True` Wales sensitivity not re-run here.
- Full OOF C bit-reproduction 33↔34 not re-executed in this pass (separate isolated rerun already 41/41).
