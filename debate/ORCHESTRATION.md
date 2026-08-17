# Orchestration — the strategic reconciliation

**Rewritten 16 August 2026** after a full read of `CALON_FH_PROGRAMME_2026-08-09/`
(README, both independent audits, the retraction, CALON-N), the Julius spec-kit
outputs, and all nine panel rounds in `debate-teach/`.

**This file replaces an earlier draft that duplicated existing work.** Everything
the first draft proposed as new — the comparator PDF paths, the SAFEHEART worked-case
test vectors, the horizon-mask fix, the one-frame collapse — was already on disk in
`CYCLE2_RESTART.md`, `julius-cycle2-pack/01_horizon_prove.py`, and
`agent-outputs-step004-r1/claude.md`. The tactical layer is covered. What is not
covered is below.

---

## 1. The contradiction nobody has reconciled

Two independent audits and a retraction, 8–9 August, reached a conclusion that
Cycle 2 is not engaging with.

**`CALON_FH_PROGRAMME_2026-08-09/README.md`, headline row:**

> **Does it beat the comparators?** **No.** FH-RS frozen scores 0.7642 in the same patients.
> The contribution is **not** a better score. It is that **score performance is set by
> study design and by ascertainment, not by the score.**
> Recommended next step: **write the design paper, not a model paper.**

**`AUDIT_V2_AGENT_2_CONCEPTS.md`, final verdict, reached independently:**

> A benchmarking-and-negative report. **Reporting standard: STROBE + RECORD, not TRIPOD.**
> TRIPOD+AI is met on **0 of 44 items**.

**`CALON_N_FINAL.md`, UK Biobank strand:**

> Nested cross-validation of the whole procedure: **0.6281**. Any FH model reporting
> AUC ≈ 0.8 in this setting is reading treatment, reading age, or reading the outcome.

Cycle 2 (15–16 August) is building **CALON-G, a nine-term prediction model, to
TRIPOD+AI**, with an explicit aim to be "competitive" with those comparators.

Nobody has written down why the 9 August ruling was set aside. It may be right to
set aside — the UKB frozen cohort is a different, larger frame (3,209/289) than the
Welsh one the audits judged (1,159/92). But that argument does not exist anywhere in
the record, and until it does, Cycle 2 is proceeding against its own audited verdict.

**This is the decision to make before another Julius cell is pasted.**

## 2. The evidence for the design paper is stronger than for the model paper

All of this is already computed, audited, and reproduced.

| Finding | Numbers | Source |
|---|---|---|
| Design determines performance | Same Welsh patients: prevalent **0.878**, incident **0.714**. Gap **0.164**. Montreal's own literature: 0.840 → 0.67 | README §1 |
| You win only under the design that flatters you | Same 2,061 patients — Montreal's rules: CALON-M 0.8785 vs 0.8632 **WIN**; SAFEHEART's rules: 0.7292 vs 0.7483 **LOSE**; FH-RS's rules: 0.7465 vs 0.7642 **LOSE** | README, three-design head-to-head |
| LDL-C inverts between designs | Same patients: OR **0.83** cross-sectionally, HR **1.02** prospectively. This is why Montreal contains no LDL-C | README §2 |
| Ascertainment moves absolute risk, not rank | E:O spread **10.6-fold** across four populations while C stays 0.64–0.74 | README §3 |
| UKB carriers are not FH in risk terms | Incident ASCVD **4.18%** carriers vs **4.19%** non-carriers | README §4, reproduced exactly |
| Clean lipids add nothing | Welsh, temporally clean: lipids over age+sex **+0.0157 (−0.009, +0.042), p=0.232**. In 40–70: **+0.0584 (−0.001, +0.117), p=0.052** | Retraction §3 |
| Age+sex is at chance where scores are deployed | 40–70 band: **0.5094** | Retraction §3 |
| The registry cannot validate any published score | All three require smoking + hypertension; both are undated status fields | Retraction §5 |
| Comparator instability is the field's problem | SAFEHEART-RE spans **C 0.55 → 0.85** across cohorts | README, comparator table |

That is a complete, audited, multi-cohort paper. The model paper, after a week of
Cycle-2 work, has one honest primary result available: **TIE**.

## 3. Step 000 is not closed, and the retired objections are the load-bearing ones

`agent-outputs-step000-audit/grok.md` — the cross-vendor neutrality audit — returns
**NOT SUPPORTED**:

> Round 4 settled two ids. The other nineteen were parked by the same single Claude
> turn the Step 001 audit already reversed. Exit 0 is schema, not consensus.
> **Do not write `locked-decisions.md`.**

`r3/panel.json`: claude 67,785 chars; **codex ERROR; kimi absent; grok 961-char wrap**.
Nineteen objections carrying `dissenter: claude` were disposed of by one agent in a
round where no raiser was present. Had they stayed OPEN, round 4 was **DEADLOCK**.

What was retired that way: **Wales-is-not-external (OBJ-006), zero external wins
(OBJ-022), comparator provenance (OBJ-014/019/024), UKB-is-not-FH (OBJ-011/026).**

Those are precisely the objections that decide §1. The strategic question was closed
by the failure mode the whole architecture exists to prevent.

**Action:** return the thirteen other-agent parks to OPEN, or DEADLOCK them with
their raisers named, exactly as grok's audit instructs. `CONSENSUS_STATE.md` already
records "audit NOT SUPPORTED — no lock", so the state file and the register disagree.

## 4. What is genuinely settled

| Objection | Status | Evidence |
|---|---|---|
| OBJ-003 age / collinearity | **REFUTED.** r = 0.606, condition number 2.02, age HR 1.033–1.055 across four fits | `obj003_collinearity.json` |
| OBJ-002 slope cluster | **PARTIAL.** Centring fixes absolute risk (mean 77.0% → 1.22%; slope 0.166 → 0.871) but the Cox slope is invariant at 0.7661, so 0.52–0.57 remains unexplained and must be re-scoped | `obj002_factorial.json` |
| OBJ-001 comparator scoring | **Provenance is a Methods defect, not a performance lever.** PDF-faithful SAFEHEART C = 0.6949; the fabricated local one C = 0.6971 | `obj001_rescore.csv` |
| Horizon mask | **CONFIRMED BROKEN.** Every 5-year cell carries the full-follow-up event count — n=163, events=146, an 89.6% event rate. Case-only sets, not leaky ones | `headtohead_full.csv` |
| The 9 LOSSes | **ARTEFACT.** Model predictions loaded from a 5-year fit and scored over full follow-up | execution report, point 6 |

## 5. Recommended sequence

**Step 1 — settle §1 by panel, not by drift.** One brief, four agents, blind round 1:
*given the 9 August audited verdict (STROBE+RECORD benchmarking report, TRIPOD 0/44)
and the Cycle-2 UKB frozen cohort (3,209/289, five times the Welsh events), is the
model paper still the right paper?* That is a genuine open question with evidence on
both sides, and it is the highest-value thing this panel could argue about.

**Step 2 — reopen the thirteen parks** per grok's audit before any lock.

**Step 3 — finish Cycle 2 regardless of the §1 answer.** The frozen frame, corrected
horizon, PDF-locked comparators and B=2,000 are needed for the design paper too — the
design paper's central claim *is* a head-to-head across designs, and it needs the same
machinery. Nothing in Cycle 2 is wasted under either outcome.

**Step 4 — write the paper the evidence carries.** On present evidence that is:

> *Performance of familial hypercholesterolaemia risk scores is determined by study
> design and ascertainment, not by score content: evidence from a UK genotype-confirmed
> registry, UK Biobank LDLR carriers, and five external cohorts.*

with the three-design head-to-head as Figure 1, the 10.6-fold E:O spread as Figure 2,
the LDL sign inversion as Figure 3, and the negative ledger as the centrepiece table.

## 6. The single biggest risk

That the programme keeps producing tactically excellent Cycle-N work — and it *is*
excellent; the panel's cross-vendor refusal to chase WINs, and grok's neutrality
audit, are better governance than most published prediction-model papers receive —
while the strategic question decided on 9 August stays quietly reopened by momentum
rather than by argument.
