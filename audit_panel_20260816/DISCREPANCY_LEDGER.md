# Discrepancy ledger — factual issues for debate round

Generated after raw reproduction (gates 11/11 PASS; performance 41/41 PASS) and all four panel reports. Provenance panel: [Panel provenance review](fc63330e-4f8a-4089-a0d7-fb72f239a88e) — AGREE WITH CONDITIONS (56 PASS / 9 FAIL / 3 UNVERIFIED).

| ID | Issue | Evidence | Severity | Proposed settlement |
|---|---|---|---|---|
| D1 | `STATUS.md`/`README.md` name CALON-F current; debate/outputs promote CALON-C | STATUS.md; step-008; outputs/RESULTS | High | Treat CALON-C as candidate under audit; do not call it repository-locked until STATUS amended |
| D2 | Wales `lpa` hard-coded NaN in `33`; RESULTS claim DRAGON nmol recovery with n=40/133 | code/33 line 263; calon_c_headtohead.csv n_eval=0; wales_lpa_strict_h2h.json | Critical | Primary CALON-C H2H: Wales SAFEHEART/FH-RS NOT_EVALUABLE. Side-file DRAGON results are exploratory only if re-run from one script of record |
| D3 | METHODS claims family-cluster Welsh optimism; `34` individual-resamples | METHODS §9; code/34; wales_cluster_optimism.json vs calon_apparent.csv | High | Prefer calon_apparent numbers or re-implement cluster bootstrap; disclose which |
| D4 | SAFEHEART scored on untreated LDL; PDF uses measured LDL | PROVENANCE_TABLE; comparator panel | High | Label adaptation; not “applied unchanged” |
| D5 | Lp(a) ÷2.15 NOT-IN-PDF | PROVENANCE_TABLE; METHODS | Medium | Exploratory conversion only |
| D6 | Welsh undated HTN/DM/smoke | measure_before_build.json 55/92 post-event BP | Critical | Dated-only co-reported; no clean external-validation claim |
| D7 | Welsh 5y wins vs SAFEHEART/FH-RS are refit_varset | headtohead.csv estimand column | High | Never bill as published-score wins |
| D8 | No PH / competing-risk modelling in code 32–35 | biostat panel; raw_reproduction PH added separately | Medium | Report PH (already PASS in audit); CIF sensitivity still missing |
| D9 | Multiplicity unmanaged | PRESPEC_HORIZON 6 confirmatory cells | Medium | Report full matrix; label exploratory |
| D10 | Manuscript drafts are retracted CALON-N/W | manuscript/ banners | High | No submission manuscript for CALON-C exists |
| D11 | Endpoint dating 147/289 unambiguous | measure_before_build; S1 C=0.660 | Medium | Limitation; not closed sensitivity |
| D12 | DCA overclaim | code/35; biostat/reviewer panels | High | Discrimination/calibration only until comparator DCA exists |
| D13 | Hard-coded Wales Downloads path | provenance F1; code/32–33 | Medium | Env/resolver like UKB |
| D14 | `usable()` full-sample term gating before CV | provenance F2 | Medium | Document intentional or move inside folds |
| D15 | audit_panel Lp(a) policy string not joined from Dragon | provenance F5; 01_raw_reproduction.py | Medium | Correct policy text to “not wired in 33” |
| D16 | No dependency lockfile | provenance F6 | Medium | Pin requirements |
| D17 | audit_panel circular for builder bugs | provenance F7 | Medium | Level-2 rebuild without importing 33 builders |
| D18 | `35` SHA not pinned in METHODS | provenance UNVERIFIED | Low | Hash-pin calibration/DCA script |

## Independent raw checks already closed
- UKB gates 7/7 PASS
- Wales gates 4/4 PASS
- SAFEHEART worked examples PASS
- Source SHA-256 pins match METHODS appendix (32/33/34/07)
- Isolated full rerun vs locked outputs: 41/41 PASS
- Schoenfeld (rank): no term p<0.05 UKB or Wales primary
- DRAGON unit folklore PASS; CALON-C DRAGON wiring FAIL (D2)
