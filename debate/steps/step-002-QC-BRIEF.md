# Step 002 — QC of results and methodology, by all agents

**Protocol:** full matrix. Every model QCs every number and every method under
all four lenses, independently in round 1, then exchanges.

**Governance:** every figure below is aggregate. No participant data appears here
and none may be requested. Strata under 10 events are `<10, non-estimable`.

---

## What you are QC-ing

Two independent analyses of the same data disagree. One is a local Python
pipeline; the other is a Julius AI run from a written specification. **Your job
is to determine which numbers are trustworthy and which method is right — not to
split the difference.**

## A. Numbers that AGREE across both analyses

Treat these as probably sound, but say so only if you have checked the logic.

| Quantity | Value |
|---|---|
| UK Biobank LDLR carriers | 3,540 |
| Prevalent ASCVD excluded | 207 |
| Undated atherosclerotic cases excluded | 124 |
| Incident events, 5-year | 97 |
| Incident events, 10-year | 194 |
| Risk set after both exclusions | 3,209 |
| Minimum event-to-baseline lag | 1 day |
| Model C-index, UK Biobank | 0.698 vs 0.6997 |
| Montreal C-index, UK Biobank | 0.670 vs 0.6671 |
| Welsh registry / PASS / DRAGON | 7,253 / 7,253 / 424 (424/424 matched) |

Event-date completeness: I21 100%, I25 100%, I63 40.9%, I70 64.3%, I73 52.8%,
G45 37.0%. The endpoint is therefore coronary-weighted.

## B. Numbers that DISAGREE — the core of this QC

| Quantity | Local pipeline | Julius | Gap |
|---|---|---|---|
| **SAFEHEART C, UK Biobank** | **0.6944** | **0.628 / 0.635** | **−0.06** |
| **FH-Risk-Score C, UK Biobank** | **0.6740** | **0.651** | **−0.023** |
| **Wales at risk** | **1,159** | **1,059** | **−100, unexplained** |
| **Wales incident events** | **92** | not reported | missing |
| **Model C, Wales** | **0.7486** | 0.698 / 0.700 / 0.713 | −0.04 to −0.05 |
| **Carrier untreated LDL-C excess** | +0.15 median | +0.226 [0.185–0.268] | third value; spec said +0.55 |
| **Carriers ≥6.5 mmol/L** | ~1% | 2.1% [1.6–2.6] | 2× |

## C. The two claimed WINs, and why they are in doubt

Julius declares two wins at the 10-year horizon:

- SAFEHEART: model 0.707 vs 0.628, Δ **+0.079 [0.033, 0.123]** → WIN
- FH-Risk-Score: model 0.704 vs 0.651, Δ **+0.052 [0.001, 0.104]** → WIN

Substituting the local comparator values: SAFEHEART Δ becomes **+0.013**, FH-RS
Δ becomes **+0.030**. At the reported interval half-widths both cross zero and
become **TIEs**.

**The asymmetry is the tell.** Montreal — the only comparator needing neither
Lp(a) nor LDL-C bands — reproduces to 0.003, and Montreal is where a TIE was
declared. Every comparator that Julius scores *lower* than the local pipeline is
one where a WIN was declared.

## D. Methodological issues to adjudicate

1. **Uniform calibration-slope compression.** All four comparator slopes cluster
   at **0.52–0.57**. Three independently derived scores do not spontaneously
   agree on a ~2× compression of the linear predictor. Shared implementation
   error, or genuine?

2. **Age is null.** Age HR **1.20 [0.91–1.60]** for 5-year incident ASCVD, and
   cholesterol-years (= age × untreated total cholesterol) HR 1.15 [0.90–1.48] in
   the same model. Both null. The specification required a correlation check
   against age with a drop rule at ≥0.999; it was never reported.

3. **Grey-zone AUC 0.489 — below chance.** In the 5–10% predicted-risk band
   (n=234, 22 events) the model has no discriminative ability. This is the band
   where a risk score is supposed to earn its keep.

4. **Welsh O/E = 6.31.** Back-calculated, the model predicts ~3.2% 10-year risk
   in a genotype-confirmed FH registry against 6.13% observed in the LDLR-carrier
   cohort where it was built. It predicts *lower* risk in the higher-risk
   population. Candidate cause: median imputation fitted in UK Biobank folds then
   applied to Welsh predictors. No Welsh missingness table exists to test it.

5. **Strict-horizon Welsh construction.** "Event before horizon OR documented
   follow-up to horizon" admits everyone with an event while making event-free
   admission progressively harder. Event rate 7.4% (n=529, 5y) → 20.4% (n=289,
   10y) as the sample shrinks 45%.

6. **300 bootstrap replicates.** The FH-RS win has CI lower bound **0.001**. A
   2.5th percentile from 300 draws is the 7.5th order statistic — essentially one
   resample. Convention is ≥2,000.

7. **Deviations declared but unexamined:** ridge-**logistic** rather than Cox;
   median imputation rather than survival-aware MICE; SAFEHEART scored with its
   prior-ASCVD term identically zero in an incident-only cohort; FH-RS assigning
   Lp(a)=0 to the 22.5% missing.

## E. What was specified but not delivered

No Table 1. No standardised mean differences. No Kaplan–Meier curves, log-rank,
or Schoenfeld PH checks. No Fine–Gray. No leak detector, EPV, or convergence
counts. No comparator provenance table or coefficients. No calibration plot or
calibration-in-the-large. No subgroups. No PROBAST. No item-level TRIPOD/STROBE —
and 21 of 49 items graded "partly met" against an explicit instruction to mark
anything not met as NOT MET. No model equation, so nobody can apply the model.
Five named reproducibility artefacts are absent from disk.

---

## Your task, under each lens

**Methodology.** Which analysis has the right design? Is ridge-logistic
defensible where Cox was specified? Is the strict-horizon Welsh construction
sound?

**Implementation.** Diagnose the 0.52–0.57 slope cluster. Name the single most
likely bug and the test that would confirm it.

**Adversarial audit.** Assume both WINs are artefacts. What is the strongest
evidence for that, and what single computation would settle it?

**Clinical and publication reality.** With grey-zone AUC 0.489 and a
coronary-weighted endpoint, what can honestly be claimed? Where does a reviewer
open?

File every disagreement as an objection block in `state/open-questions.md`. An
objection whose `settled_by` is not a runnable test will be rejected by
`consensus.mjs`.
