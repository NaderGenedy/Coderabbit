# Step 006 — Build the final model. One round. Deadline conditions.

You are one voice on a four-model panel (Claude, Codex, Kimi, Grok). Round 1 is
blind. There will be **one exchange round, not four** — the investigator is against
a deadline. Say everything that matters in your first turn.

**You have no data access and never will.** Your output is an **analysis
specification and the runnable code to execute it**, which the investigator pastes
into Julius AI. Never request an extract, a row, or an identifier. Argue about what
the code should do and why — never about numbers you cannot see.

---

## THE GOAL, STATED AS ONE NUMBER

Build a model that beats the published comparators **with external validation** and
**without Lp(a) or apoB**.

Three designs have already been run on the same 2,061 Welsh patients
(`01_results/M13_THREEDESIGN.json`):

| Design | Best CALON | Comparator | Result |
|---|---|---|---|
| Montreal's rules (prevalent) | 0.8785 | Montreal 0.8632 | WIN +0.015 |
| SAFEHEART's rules (prior ASCVD in) | 0.7292 | SAFEHEART 0.7483 | LOSE −0.019 |
| **FH-RS's rules (incident, prior out)** | **0.7465** | **FH-RS 0.7642** | **LOSE −0.018** |

**Everything reduces to that last cell.** Win it and the programme has its paper.
Lose it and no framing rescues one.

## WHAT CHANGED, AND WHY THIS IS NOW WINNABLE

**1. The detection floor is four times smaller than the project record says.**
`AUDIT_V2_AGENT_1_NUMBERS.md` D10: the 0.085 floor assumed ρ = 0.5 between model and
comparator predictions. Measured ρ is **0.907 (Montreal) / 0.884 (FH-RS) / 0.869
(SAFEHEART)**. At observed correlation the floors are **0.037 / 0.041 / 0.044**. The
target is **+0.04, not +0.15**. Every "underpowered" statement in the older records
was computed at an assumed ρ and is wrong.

**2. +0.033 of headroom is already banked.** CALON-A alone scores 0.7135. CALON-A
given the FH-RS variable set scores **0.7465**. Hypertension and smoking bought
+0.033. The remaining gap to 0.7642 is **0.018**.

**3. Excluding Lp(a) and apoB is the enabling constraint.** Cycle-3, agreed by all
four vendors: *"Promotion to confirmatory is effectively blocked. Wales lacks
comparable apoB and Lp(a) scale differs."* Yet `CALON_G_BIOSTAT_PROTOCOL.md` puts
`log_lpa` in the **primary** spec — the single term that makes Welsh external
validation impossible. The investigator's constraint removes that blocker. Treat
`log_lpa` as **removed from the primary**; it may appear only as a labelled
UKB-internal sensitivity.

## THE PROBLEM NOBODY HAS ADDRESSED

In UK Biobank carriers with frozen published comparators
(`01_results/M12_FAITHFUL.json`, n=2,952, 127 events):

| Score | C (full) | **5-y AUC** |
|---|---|---|
| CALON | **0.6428** | 0.6149 |
| FH-RS | 0.6287 | **0.6528** |
| Montreal | 0.6179 | 0.6309 |
| age + sex | 0.6083 | 0.6244 |

**The model wins on full-follow-up C and loses at five years to both comparators.**
Five years is the horizon a clinic uses. No document in the programme addresses this.
Any specification you propose must either fix it or state plainly that the claim is
restricted to long-horizon discrimination.

## CANDIDATE SPECIFICATION — attack it or improve it

Nine terms. No published score as input. No Lp(a), no apoB, no treatment flag.
Every term computable in both cohorts from one dated lipid visit.

```text
age, sp50, male, htn, dm, smoke, cum_nonhdl, log_tghdl, remnant_chol
```

| Term | Construction | Rationale |
|---|---|---|
| `age`, `sp50` | `age`, `max(age−50,0)` | Shared by all comparators |
| `male` | `1 − sex_F` | SAFEHEART β 0.70; FH-RS 7 pts; Montreal 3 pts |
| `htn` | BP medication (dated) or SBP≥140/DBP≥90 | In all three |
| `dm` | diabetes | Univariable-significant in **both** derivations (SAFEHEART HR 3.45; FH-RS 1.64, p=0.054) but **dropped from both multivariable models**. UKB has far more diabetes than a lipid clinic. |
| `smoke` | current | In all three |
| `cum_nonhdl` | `log((TC−HDL)_untreated × age)` | **Duration** — no comparator has it |
| `log_tghdl` | `log(TG/HDL)` | Insulin-resistance axis — absent from all three |
| `remnant_chol` | `TC − HDL − LDL` | Absent from all three |

EPV: UKB 289/9 = 32.1 · Wales 92/9 = 10.2 (thin — ridge required).

## TREATMENT STATUS IS EXCLUDED BY INVESTIGATOR DECISION — do not reopen it

No statin or treatment flag enters the model as a predictor. This is settled and is
**not** one of the decisions below. Do not propose it, do not test it, do not raise
it as a missed opportunity.

Two consequences you must carry:

- **The Welsh C = 0.8443 recorded for CALON-6D is off the table**, because that
  specification contained `on_statin_flag`. Do not quote it, plan against it, or use
  it as a baseline. The defensible Welsh expectation for a treatment-free
  specification is **≈0.74** (`M10_EXTERNAL.json` Welsh genotype-positive C 0.7404;
  `M13_THREEDESIGN.json` CALON-A + FH-RS variable set 0.7465).
- **Treatment still enters as a covariate transformation only** — the ÷0.70
  back-correction producing untreated non-HDL-C. Use the **dated** treatment field
  (`Treatmentdate1` ≤ `MeasurementDate.1` in Wales; `on_statin_self` at baseline in
  UKB), never the undated `OnTreatment`. FH-RS does the same thing (its LDL is
  "untreated or imputed"), so this is symmetric with the comparators, not an advantage.

## TWO PRE-FLIGHT GATES — code these first; each can cancel the plan

| Gate | Test | Cancels if |
|---|---|---|
| **G1 census** | Of 1,159 Welsh at-risk, how many have TC **and** HDL **and** TG **and** LDL at `MeasurementDate.1`? | Complete-case n < ~800 or events < ~70 → `remnant_chol` not estimable; spec must shrink |
| **G2 floor** | Recompute the paired cluster-bootstrap floor at **measured** ρ per comparator | Floors return near 0.085 → target reverts to +0.09, out of reach |

## FOUR DECISIONS YOU MUST RESOLVE — the panel exists for these

1. **Development direction.** Project memory (2 Aug): *developing in UKB is strictly
   worse — 0 wins/1 loss vs 2 wins/0.* Against it: EPV 32 vs 10, the frozen SHA cohort
   is UKB, and `M10_EXTERNAL.json` shows a UKB-developed equation reaching **C 0.7404,
   E:O 0.815** in Welsh genotype-positives. Which is primary, and why? Both directions
   must be pre-specified either way.

2. **`cum_nonhdl` and `remnant_chol` together.** Both derive from TC, HDL, LDL. Report
   the expected correlation and decide: both, one, or a composite. The 0.999 drop rule
   catches only exact duplicates — do not hide behind it.

3. **Undated Welsh smoking and hypertension.** All three comparators need them; both
   are status-at-last-contact, so contamination is **symmetric**. Options: registry-fields
   frame only, dated-fields-only frame, or both reported. Choose and justify.

4. **The five-year loss.** Fix it in the specification, or restrict the claim. Name
   which.

## RULES — non-negotiable

- **No published score, and no linear predictor derived from one, may be a model
  input.** Comparators are scored, never fitted.
- **No Lp(a), no apoB in the primary.** Not as an enhancer, not in a two-stage design.
- **No treatment/statin flag as a predictor.** Treatment enters only via the ÷0.70
  untreated back-correction of lipid terms.
- **No term added after seeing a WIN/TIE/LOSS matrix.** Cycle 1 added BMI after the
  diabetic subgroup lost; that is on the record as a Methods vulnerability.
- Score comparators **from the coefficients in the source PDFs on disk**, never from
  memory. SAFEHEART must pass its own published worked cases: Case 1 → 0.02% / 0.05%,
  Case 2 → **38.08% / 64.15%**. The test must FAIL on the current local function.
- Horizon mask: `E_h = (E==1) & (T<=H)`, `T_h = min(T,H)`. The old
  `(T<=H) | (E==1)` produced 146 "five-year" events against the frozen 97.
- Frozen cohort gates print on every run: **3,540 / 207 / 124 / 3,209 / 289 / 97 / 194**,
  cohort SHA `8c3a1e0598770c1beefe29db28d42fb7074f233f382c25c19eb0c843b59f49b2`.
- Effect size + 95% CI + absolute risk. A positive point estimate whose interval
  crosses zero is a **TIE** — label it one.
- Any stratum with <10 events is `<10, non-estimable`.
- B = 2,000 for anything reported.
- Aggregate output only. No eid, NHS number, name, date of birth or variant coordinate.
- If you cannot do something, say so. Never substitute a weaker analysis silently.

## COMPARATOR SOURCES — on disk, verified

`/Users/nader85/Downloads/CALON-DeepResearch/papers/` — text extracts at
`/Users/nader85/Downloads/CALON_FH_PROGRAMME_2026-08-09/04_papers/extracted_text/`

- **SAFEHEART** `Circulation 2017;135:2139–40` — `risk = 1 − S0^exp(Σβx − 5.4078)`,
  S0(5y)=0.9532, S0(10y)=0.9025. β = 0.70 male · 1.07 age30–59 · 1.45 age≥60 · 0.69
  highBP · 1.42 priorASCVD · 0.48 smoking · 0.88 overweight · 0.98 obesity · 0.92 LDL
  100–159 mg/dL · 1.57 LDL ≥160 · 0.42 Lp(a)>50 mg/dL.
- **FH-RS** `ATVB 2021;41:2637–8` — chart points = 10 × β. Male 7 · age
  0/9/14/16/17/18/20/23 · HDL-C 0/3/7/8 · LDL-C (mmol/L) 0/3/7/9/11 · HTN 6 · smoking 6
  · Lp(a)≥50 mg/dL 4.
- **Montreal** `J Clin Lipidol 2017;11:84` Table 3 — integer points. Age ≤21:0, 22–28:4,
  29–35:8, 36–42:12, 43–49:16, 50–56:20, 57–63:24, >63:28 · HDL-C (mmol/L) ≤0.60:12,
  0.61–0.90:9, 0.91–1.20:6, 1.21–1.50:3, >1.50:0 · Men 3 · HTN 2 · Smoking 1.

## DATA TRAPS — each has produced a wrong published-quality result

1. `first_angina` is **hypertension** (41.7% of UKB, SBP 148.9 vs 139.7). Never use.
2. `first_ascvd` is 93.4% chronic IHD. Use `corrected_ascvd_outcomes.csv`.
3. `i50_event` is heart failure. Excluded from the endpoint.
4. Welsh cohort flag is **`Positive1`** (2,405), not `Mutation1` (3,562).
5. Welsh outcome flag is **`ascvd_combine`**, not "has a dated event age".
6. Welsh dates need `format="mixed"`; `dayfirst=True` silently changes the cohort from
   1,159/92 to 948/82.
7. `MtachedLDLC` is **already pre-treatment** — do not apply ÷0.70 to it.
8. `on_statin_self` is populated for carriers, missing for **all** non-carriers.
9. DRAGON `eGFR`/`BMI` hold `""` and `">90"` — parse as text first.
10. Compare dates with `a.notna() & b.notna() & (a != b)`.

## DELIVERABLE — all four lenses, under their own headings

**1. METHODOLOGY.** Resolve the five decisions. Defend the specification against the
comparators' published forms. State the estimand in one sentence.

**2. IMPLEMENTATION.** Write the actual runnable code: the three gates, cohort
construction, corrected horizon, PDF-faithful comparator scoring with the SAFEHEART
worked-case test, out-of-fold family-clustered fit, IECV both directions, head-to-head
at measured-ρ floors, ascertainment-stratified recalibration, Welsh transport. Name
every column you read. Your gates must reproduce 3,209 / 289 / 97 / 194.

**3. ADVERSARIAL AUDIT.** Assume the resulting model is wrong. The most likely way it
is wrong is a leak that inflates Wales — that has happened three times. Name the single
test that would catch it, and one failure mode nobody in this brief has anticipated.

**4. CLINICAL AND PUBLICATION REALITY.** With the five-year loss and a coronary-weighted
endpoint (date completeness I21 100%, I25 100%, I63 40.9%, I70 64.3%, I73 52.8%, G45
37.0%), what can honestly be claimed? Where does a reviewer open?

**End with:** the specification you recommend in one line, your answer to each of the
five decisions in one sentence each, and the single biggest risk in your own proposal.

File every disagreement as an `objection` block. An objection whose `settled_by` is not
a runnable test will be rejected by `consensus.mjs`.
