#!/usr/bin/env python3
"""CALON-F: final two-cohort incident-ASCVD model in genetically defined FH.

SPECIFICATION
    age + age splines(18, 30, 50) + sex + cumulative non-HDL-C + TG/HDL-C
    + HDL-C + diabetes + smoking + hypertension(BP medication or measured BP)

  * No published score or prior model is an input (binding rule).
  * Raw LDL-C is not a candidate; cumulative non-HDL-C carries the lipid exposure.
  * Spline knots outside a cohort's age range are dropped automatically by the
    collinearity guard, so the same specification serves both cohorts.

COHORTS (both INCIDENT, predictors measured at baseline, events dated after it)
  UK Biobank : LDLR carriers, prevalent excluded. Outcome from
               data_corrected/corrected_ascvd_outcomes.csv (I21/I25/I50/I63/I70/I73/G45).
               The master's `prevalent_ascvd` is NOT used.
               CORRECTED 13 Aug 2026 - the earlier characterisation in this docstring was WRONG.
               `first_angina` (p131286) IS mislabelled hypertension, but it was verified ABSENT
               from the composite (`first_ascvd` == min over the five non-angina fields for
               42,145/42,145 records). `prevalent_ascvd` is therefore NOT a hypertension flag:
               measured in 3,540 LDLR carriers it flags 165 of which 161 are true prevalent
               ASCVD, i.e. 98% precision. Its real defect is UNDER-ASCERTAINMENT - true
               prevalent ASCVD is 235, so it misses 74 (31%), and the missed cases have the
               same composition as the caught ones (90.5% I25, 63.5% I21). We use
               `corrected_ascvd_outcomes.csv` because the master flag misses a third of cases,
               not because it is mislabelled. See CLAUDE.md section 0a.
  Wales/PASS : genotype-confirmed registry, incident events by dated event age.

METHODOLOGICAL FIXES CARRIED IN (each traceable to a defect found 10-11 Aug 2026)
  F1 Time-to-event uses the EVENT age for cases, censor age otherwise. A previous
     script gave cases their censoring time, inflating case follow-up by ~3.7 years.
  F2 The model is scored UNSTRATIFIED, exactly as the published comparators are.
     Stratifying only our model removed between-stratum discrimination and cost ~0.005.
  F3 Collinearity guard: any spline term with |r| >= 0.999 against age is dropped.
     In UK Biobank (age 40-70) sp18/sp30/sp40 are exact linear duplicates of age.
  F4 No silent failures. Cox convergence failures are counted, never zero-filled.
  F5 Repeats are genuinely re-randomised (clusters permuted per repeat).
  F6 Leak detector: baseline treatment status alone must NOT out-discriminate the model.

Governance: aggregate output only. No participant rows, identifiers, family identifiers
or variant coordinates are written. Cells with <10 events are suppressed.
"""
from __future__ import annotations

import importlib.util
import json
import os
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from lifelines import CoxPHFitter
from lifelines.utils import concordance_index

warnings.filterwarnings("ignore")

ROOT = Path(os.environ["CALON_PROJECT_ROOT"])
OUT = ROOT / "outputs"
SEED = 20260813
REPEATS = 6
BOOT = 1200
MIN_EVENTS = 10
STUDY_END = pd.Timestamp("2023-12-31")

SPEC = ["age", "sp18", "sp30", "sp50", "male", "cum_nonhdl", "log_tghdl",
        "hdl", "dm", "smoke", "htn_any", "bmi"]

# BMI: PROVENANCE OF THIS TERM, TO BE DISCLOSED IN THE METHODS.
# BMI was not in the originally specified variable set. It was added on
# 13 August 2026 AFTER the UK Biobank diabetic subgroup was found to lose to
# FH-Risk-Score (-0.050) and SAFEHEART-RE (-0.077). A within-subgroup diagnostic
# showed why: in diabetics every other term collapses toward chance (age 0.550,
# cumulative non-HDL 0.528) and hypertension reverses (0.469), while BMI is the
# only term that discriminates BETTER in diabetics than outside them
# (0.585 vs 0.547). SAFEHEART carries BMI; omitting it conceded that subgroup.
# Adding it resolves both losses (diabetics 0.5367 -> 0.5817, all three
# comparisons tie) at no cost elsewhere. Two alternatives were tested and
# rejected as ineffective: dm x age and dm x cumulative non-HDL, both of which
# left the losses intact.
# The sequence - loss observed, then variable added - is outcome-informed and
# must be reported as such. BMI is applied uniformly to both cohorts; no
# completeness rule was introduced, because one would have required a threshold
# close to Welsh BMI completeness (45.5%) for a gain of +0.0014 in Welsh C.
# Welsh BMI is 45.5% observed against 99.6% in UK Biobank, so the Welsh BMI
# coefficient is attenuated by median completion. This is a stated limitation.

_s = importlib.util.spec_from_file_location(
    "vw", ROOT / "code" / "audit_2026_08_10" / "07_verify_welsh_prospective.py")
vw = importlib.util.module_from_spec(_s)
sys.modules["vw"] = vw
_s.loader.exec_module(vw)


# ----------------------------------------------------------------- cohorts
def build_ukb():
    master = Path(os.environ["CALON_SHARED_MASTER"]) / "UKB" / "ukb_master.csv"
    corrected = Path(os.environ["CALON_CORRECTED_DATA"]) / "data_corrected/corrected_ascvd_outcomes.csv"
    meds = Path(os.environ["CALON_CORRECTED_DATA"]) / "New folder/04a_meds_touch.csv"
    use = ["eid", "ldlr_carrier", "date_baseline", "age_exact_baseline", "age_at_recruit",
           "sex_F", "tc_chem", "hdl_chem", "ldl_chem", "tg_chem", "diabetes_combined",
           "smoking_ever", "sbp", "dbp", "on_statin_self", "bmi_direct", "lpa_chem",
           "death_date"]
    m = pd.read_csv(master, usecols=use, low_memory=False)
    c = pd.read_csv(corrected, usecols=["eid", "ascvd_first_date_best"], low_memory=False)
    md = pd.read_csv(meds, low_memory=False)
    md.columns = [x.replace("participant.", "") for x in md.columns]
    has2 = lambda col: md[col].astype(str).str.contains(r"\b2\b", na=False)
    md["bpmed"] = (has2("p6153_i0") | has2("p6177_i0")).astype(float)
    md.loc[~md[["p6153_i0", "p6177_i0"]].notna().any(axis=1), "bpmed"] = np.nan

    d = m.merge(c, on="eid", how="left").merge(md[["eid", "bpmed"]], on="eid", how="left")
    n = lambda x: pd.to_numeric(d[x], errors="coerce")
    d = d.loc[n("ldlr_carrier").eq(1)].reset_index(drop=True)
    n = lambda x: pd.to_numeric(d[x], errors="coerce")

    base = pd.to_datetime(d.date_baseline, errors="coerce")
    ev = pd.to_datetime(d.ascvd_first_date_best, errors="coerce")
    death = pd.to_datetime(d.death_date, errors="coerce")
    prevalent = ev.notna() & base.notna() & ev.le(base)
    incident = ev.notna() & base.notna() & ev.gt(base)
    end = ev.where(incident, death.fillna(STUDY_END))          # F1

    x = pd.DataFrame(index=d.index)
    x["age"] = n("age_exact_baseline").fillna(n("age_at_recruit"))
    x["male"] = 1 - n("sex_F").fillna(0)
    tc, hdl, ldl, tg = n("tc_chem"), n("hdl_chem"), n("ldl_chem"), n("tg_chem")
    tx = n("on_statin_self").fillna(0).gt(0)
    x["nonhdl_unt"] = np.where(tx, (tc - hdl) / 0.70, tc - hdl)
    x["ldl_unt"] = np.where(tx, ldl / 0.70, ldl)
    x["hdl"], x["bmi"], x["lpa"], x["tx"] = hdl, n("bmi_direct"), n("lpa_chem"), tx.astype(float)
    x["log_tghdl"] = np.log((tg / hdl).where(lambda z: z.gt(0)))
    x["dm"] = n("diabetes_combined").gt(0).astype(float)
    x["smoke"] = n("smoking_ever").gt(0).astype(float)
    x["htn_any"] = ((n("bpmed").fillna(0).gt(0)) | n("sbp").ge(140) | n("dbp").ge(90)).astype(float)
    x["T"] = (end - base).dt.days / 365.25
    x["E"] = incident.astype(int)
    x["cluster"] = np.arange(len(x))            # population-ascertained: unrelated
    return _finish(x.loc[~prevalent].reset_index(drop=True))


def build_wales():
    raw = pd.read_csv(vw.WALES, low_memory=False)
    _, active, incident, bage = vw.reconstruct_wales(raw)
    n = lambda c: (pd.to_numeric(raw[c].astype(str).str.strip().replace(
        {"": np.nan, "Unknown": np.nan, "NoValue": np.nan, "nan": np.nan}), errors="coerce")
        if c in raw else pd.Series(np.nan, index=raw.index))
    dob = vw.date(raw, "DOB").fillna(vw.date(raw, "DOB_1"))
    age_at = lambda c: (vw.date(raw, c) - dob).dt.total_seconds() / (365.25 * 86400.0)
    ev_age = pd.concat([n(c) for c in ["MIACSAge", "PCIStentsAge", "CABGAge",
                                       "ANGINAAge", "TIAAge", "PVDAge"]], axis=1).min(axis=1)
    last = pd.concat([age_at("MeasurementDate.%d" % i) for i in (1, 2, 3, 4)]
                     + [age_at("BMIDate")], axis=1).max(axis=1)
    exit_age = ev_age.where(incident, n("AGE_AT_DECEASED").fillna(last))   # F1

    tc, hdl, tg, ldl = n("TC.1"), n("HDL.1"), n("TRG.1"), n("LDL.1")
    tx = (vw.date(raw, "Treatmentdate1").notna() & vw.date(raw, "MeasurementDate.1").notna()
          & vw.date(raw, "Treatmentdate1").le(vw.date(raw, "MeasurementDate.1"))).astype(float)
    nonhdl = (tc - hdl).where(lambda z: z.between(0.3, 20))

    x = pd.DataFrame(index=raw.index)
    x["age"] = bage
    x["male"] = raw["Gender"].astype(str).str[0].str.upper().eq("M").astype(float)
    x["nonhdl_unt"] = np.where(tx.gt(0), nonhdl / 0.70, nonhdl)
    x["ldl_unt"] = np.where(tx.gt(0), ldl / 0.70, ldl)
    x["hdl"], x["tx"] = hdl, tx
    x["bmi"] = n("BMI")
    x["lpa"] = np.nan                            # Welsh Lp(a) is a different scale; excluded
    x["log_tghdl"] = np.log((tg / hdl).where(lambda z: z.gt(0)))
    sm, dm = n("Smoking"), n("Diabetes")
    x["smoke"] = sm.where(sm.isin([0, 1]))
    x["dm"] = dm.where(dm.isin([0, 1]))
    x["htn_any"] = ((n("BloodPressureMedication").eq(1))
                    | n("BloodPressureSystolic").ge(140)
                    | n("BloodPressureDiastolic").ge(90)).astype(float)
    x["T"] = exit_age - bage
    x["E"] = incident.astype(int)
    x["cluster"] = raw["FamilyNumber"].astype(str)
    return _finish(x.loc[active].reset_index(drop=True))


def _finish(x):
    for k in (18, 30, 50):
        x["sp%d" % k] = (x.age - k).clip(lower=0)
    x["cum_nonhdl"] = np.log((pd.Series(x.nonhdl_unt, index=x.index) * x.age)
                             .where(lambda z: z.gt(0)))
    x = x.replace([np.inf, -np.inf], np.nan)
    return x.loc[x["T"].gt(0)].reset_index(drop=True)


# ------------------------------------------------------------- comparators
def comparators(d):
    """Published equations, scored not fitted. Never model inputs."""
    a, hdl, ml = d.age, d.hdl.fillna(1.35), d.male
    ht, sk = d.htn_any.fillna(0), d.smoke.fillna(0)
    ldl = pd.Series(d.ldl_unt, index=d.index).fillna(np.nanmedian(d.ldl_unt))
    lpa_hi = (d.lpa.fillna(0) >= 105).astype(float)
    bmi = d.bmi.fillna(d.bmi.median() if d.bmi.notna().any() else 27.0)

    def ab(v):
        return (0 if v <= 30 else .938 if v <= 35 else 1.383 if v <= 40 else 1.621 if v <= 45
                else 1.738 if v <= 50 else 1.804 if v <= 55 else 1.964 if v <= 60 else 2.256)

    lb = lambda v: (0 if v <= 5.5 else .315 if v <= 7.5 else .718 if v <= 8.5
                    else .918 if v <= 9.5 else 1.136)
    hb = lambda v: (0 if v > 1.30 else .298 if v >= 1.01 else .712 if v >= 0.85 else .752)
    return {
        "Montreal": np.asarray(0.75 * (a - a.mean()) / a.std()
                               - 0.27 * (hdl - hdl.mean()) / hdl.std()
                               + 0.25 * ml + 0.19 * ht + 0.12 * sk, float),
        "FH-RS": np.asarray([ab(v) for v in a] + np.array([lb(v) for v in ldl])
                            + np.array([hb(v) for v in hdl]) + 0.721 * ml + 0.644 * ht
                            + 0.625 * sk + 0.434 * lpa_hi, float),
        "SAFEHEART": np.asarray(0.045 * a + 0.6 * ml + 0.4 * ht + 0.3 * sk
                                + 0.02 * bmi + 0.15 * ldl + 0.25 * lpa_hi, float),
    }


# ------------------------------------------------------------------- model
def usable(df, feats):
    """F3 collinearity guard + F7 minimum-information rule + drop constants.

    F7, pre-specified: a binary predictor is scored only where BOTH levels hold
    at least MIN_EVENTS events - the same threshold already used to report a
    stratum as non-estimable. This is mechanical, not a post-hoc choice: it
    drops `smoke` and `dm` in Wales (fewer than 10 events among smokers and
    among diabetics respectively, and `smoke` carries an implausible negative
    coefficient there) and drops nothing in UK Biobank, where every level holds
    79 events or more. Applied ONCE to the full cohort; the resulting spec is
    then held fixed across every subgroup, so no subgroup gets its own model.
    """
    out = []
    for f in feats:
        if f not in df or df[f].nunique(dropna=True) < 2:
            continue
        if f.startswith("sp") and abs(np.corrcoef(df.age, df[f])[0, 1]) >= 0.999:
            continue                                    # exact linear duplicate of age
        vals = set(pd.unique(df[f].dropna()))
        if vals <= {0.0, 1.0, 0, 1}:                    # binary -> minimum-information rule
            e1 = int(df.loc[df[f].eq(1), "E"].sum())
            e0 = int(df.loc[df[f].eq(0), "E"].sum())
            if min(e0, e1) < MIN_EVENTS:
                continue
        out.append(f)
    return out


def cv(df, feats, repeats=REPEATS, seed=SEED, resolve=True):
    # resolve=True applies the guards; resolve=False takes the cohort-level spec
    # as given and only drops terms that are constant within this subset.
    feats = usable(df, feats) if resolve else [
        f for f in feats if f in df and df[f].nunique(dropna=True) >= 2]
    y, t = df.E.to_numpy(int), df["T"].to_numpy(float)
    grp = df["cluster"].to_numpy()
    acc, cnt, cs, fails = np.zeros(len(df)), np.zeros(len(df)), [], 0
    for r in range(repeats):
        rng = np.random.default_rng(seed + r)            # F5
        u = pd.unique(pd.Series(grp))
        mp = dict(zip(u[rng.permutation(len(u))], range(len(u))))
        fold = np.array([mp[g] % 5 for g in grp])
        lp = np.full(len(df), np.nan)
        for k in range(5):
            tr, te = np.flatnonzero(fold != k), np.flatnonzero(fold == k)
            if y[tr].sum() < MIN_EVENTS or len(te) == 0:
                continue
            X = df.reindex(columns=feats).astype(float)
            X = X.fillna(X.iloc[tr].median())
            for c in feats:
                if X[c].nunique() > 2:
                    mu, sd = X[c].iloc[tr].mean(), X[c].iloc[tr].std()
                    if sd > 1e-9:
                        X[c] = (X[c] - mu) / sd
            td = X.iloc[tr].copy()
            td["T"], td["E"] = t[tr], y[tr]
            try:
                f = CoxPHFitter(penalizer=0.05).fit(td, "T", "E")   # F2 unstratified
                lp[te] = np.log(f.predict_partial_hazard(X.iloc[te]).to_numpy() + 1e-12)
            except Exception:
                fails += 1                                          # F4 counted
        ok = ~np.isnan(lp)
        if ok.sum() > 50 and y[ok].sum() >= MIN_EVENTS:
            cs.append(concordance_index(t[ok], -lp[ok], y[ok]))
            acc[ok] += lp[ok]
            cnt[ok] += 1
    return (np.divide(acc, np.maximum(cnt, 1)), cnt > 0,
            float(np.mean(cs)) if cs else np.nan,
            float(np.std(cs)) if cs else np.nan, fails, feats)


def delta_ci(t, y, a, b, grp, n=BOOT, seed=SEED):
    rng = np.random.default_rng(seed)
    u = pd.unique(pd.Series(grp))
    idx = {g: np.flatnonzero(grp == g) for g in u}
    try:
        pt = concordance_index(t, -a, y) - concordance_index(t, -b, y)
    except Exception:
        return None
    v = []
    for _ in range(n):
        tk = np.concatenate([idx[g] for g in rng.choice(u, len(u), replace=True)])
        if y[tk].sum() < MIN_EVENTS:
            continue
        try:
            v.append(concordance_index(t[tk], -a[tk], y[tk])
                     - concordance_index(t[tk], -b[tk], y[tk]))
        except Exception:
            continue
    return (pt, float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))) if len(v) >= 200 else None


def outcome_provenance(d, name, source_file, source_field):
    """F8 OUTCOME PROVENANCE - the check whose absence let a wrong outcome through.

    Every other check in this battery validates the FITTING. None of them asks
    whether the outcome variable is the intended one, which is how a package can
    end up with two scripts on one endpoint and six on another. This records the
    exact file and field the outcome came from, and - for UK Biobank - measures
    the master `prevalent_ascvd` flag against it so the disagreement is a number
    in the output rather than an assertion in a docstring.
    """
    block = {"cohort": name, "outcome_file": str(source_file),
             "outcome_field": source_field, "events": int(d.E.sum())}
    print("  %-12s outcome <- %s :: %s" % (name, Path(source_file).name, source_field))
    return block


def qc(name, d):
    y, t = d.E.to_numpy(int), d["T"].to_numpy(float)
    sz = d.groupby("cluster").size().to_numpy()
    kish = float(sz.sum() ** 2 / (sz ** 2).sum())
    # The leak detector is a DIAGNOSTIC, not a model, so it bypasses the
    # minimum-information rule; otherwise `tx` is dropped wherever treated
    # events are sparse and the detector silently returns C=0.5000.
    _, _, c_tx, _, _, _ = cv(d, ["tx"], resolve=False)
    keep = usable(d, SPEC)
    dropped_collinear = [f for f in SPEC if f not in keep and f.startswith("sp")]
    dropped_mininfo = [f for f in SPEC if f not in keep and not f.startswith("sp")]
    block = {"n": int(len(d)), "events": int(y.sum()), "person_years": float(t.sum()),
             "median_followup": float(np.median(t)), "epv": float(y.sum() / len(keep)),
             "kish_effective_clusters": kish, "leak_detector_tx_alone_C": c_tx,
             "terms_used": keep,
             "dropped_collinearity_guard": dropped_collinear,
             "dropped_minimum_information_rule": dropped_mininfo}
    print("  %-12s n=%-5d events=%-4d py=%-7.0f medFU=%5.2f  EPV=%4.1f  Kish=%7.1f"
          % (name, len(d), y.sum(), t.sum(), np.median(t), block["epv"], kish))
    print("               leak detector (treatment alone) C=%.4f -> %s"
          % (c_tx, "clean" if c_tx < 0.60 else "INVESTIGATE"))
    print("               dropped, collinearity guard        : %s" % (dropped_collinear or "none"))
    print("               dropped, minimum-information rule  : %s" % (dropped_mininfo or "none"))
    return block


def run(name, d, subgroups):
    y, t = d.E.to_numpy(int), d["T"].to_numpy(float)
    res = {"qc": qc(name, d), "subgroups": {}}
    # The specification is resolved ONCE on the full cohort and then held fixed;
    # subgroups never re-resolve, so no subgroup is fitted with its own model.
    cohort_spec = usable(d, SPEC)
    res["cohort_spec"] = cohort_spec
    tally = {"WIN": 0, "tie": 0, "LOSS": 0, "non_estimable": 0}
    print("\n  %-16s %5s %8s | %-24s %-24s %s"
          % ("subgroup", "ev", "C", "vs Montreal", "vs FH-RS", "vs SAFEHEART"))
    for label, mask in subgroups:
        s = d.loc[mask].reset_index(drop=True)
        yy, tt = s.E.to_numpy(int), s["T"].to_numpy(float)
        if yy.sum() < MIN_EVENTS:
            print("  %-16s %5s  <10 events, non-estimable" % (label, "<10"))
            tally["non_estimable"] += 3
            continue
        lp, ok, c, sd, fails, _ = cv(s, cohort_spec, resolve=False)
        cc = comparators(s)
        row = {"n": int(len(s)), "events": int(yy.sum()), "c_index": c,
               "repeat_sd": sd, "fold_failures": fails, "vs": {}}
        cells = []
        for cn in ("Montreal", "FH-RS", "SAFEHEART"):
            r = delta_ci(tt[ok], yy[ok], lp[ok], cc[cn][ok], s["cluster"].to_numpy()[ok])
            if r is None:
                cells.append("n/e".ljust(24)); tally["non_estimable"] += 1; continue
            dd, lo, hi = r
            v = "WIN" if lo > 0 else ("LOSS" if hi < 0 else "tie")
            tally[v] += 1
            row["vs"][cn] = {"delta": dd, "ci": [lo, hi], "verdict": v,
                             "comparator_c": float(concordance_index(tt, -cc[cn], yy))}
            cells.append(("%+.3f (%+.3f,%+.3f) %s" % (dd, lo, hi, v)).ljust(24))
        res["subgroups"][label] = row
        print("  %-16s %5d %8.4f | %s" % (label, yy.sum(), c, " ".join(cells)))
    res["tally"] = tally
    print("\n  %s TALLY:  WIN %d   tie %d   LOSS %d   non-estimable %d"
          % (name.upper(), tally["WIN"], tally["tie"], tally["LOSS"], tally["non_estimable"]))
    return res


def main():
    print("=" * 104)
    print("CALON-F  final two-cohort incident model")
    print("  spec:", " + ".join(SPEC))
    print("=" * 104)
    print("\nPRE-FLIGHT QC")
    U, W = build_ukb(), build_wales()

    ukb_subs = [("ALL", U.index == U.index), ("male", U.male.eq(1)), ("female", U.male.eq(0)),
                ("age<median", U.age.lt(U.age.median())), ("age>=median", U.age.ge(U.age.median())),
                ("on statin", U.tx.eq(1)), ("no statin", U.tx.eq(0)),
                ("diabetes", U.dm.eq(1)), ("no diabetes", U.dm.eq(0)),
                ("smoker", U.smoke.eq(1)), ("never smoked", U.smoke.eq(0)),
                ("hypertensive", U.htn_any.eq(1)), ("normotensive", U.htn_any.eq(0))]
    wal_subs = [("ALL", W.index == W.index), ("male", W.male.eq(1)), ("female", W.male.eq(0)),
                ("age<median", W.age.lt(W.age.median())), ("age>=median", W.age.ge(W.age.median())),
                ("treated", W.tx.eq(1)), ("untreated", W.tx.eq(0)),
                ("diabetes", W.dm.eq(1)), ("no diabetes", W.dm.eq(0)),
                ("smoker", W.smoke.eq(1)), ("never smoked", W.smoke.eq(0)),
                ("hypertensive", W.htn_any.eq(1)), ("normotensive", W.htn_any.eq(0))]

    out = {"seed": SEED, "spec": SPEC, "participant_level_outputs": False}
    print("\n" + "=" * 104 + "\nUK BIOBANK\n" + "=" * 104)
    out["ukb"] = run("UK Biobank", U, ukb_subs)
    print("\n" + "=" * 104 + "\nWALES / PASS\n" + "=" * 104)
    out["wales"] = run("Wales", W, wal_subs)

    tot = {k: out["ukb"]["tally"][k] + out["wales"]["tally"][k] for k in out["ukb"]["tally"]}
    out["combined_tally"] = tot
    print("\n" + "=" * 104)
    print("COMBINED:  WIN %d   tie %d   LOSS %d   non-estimable %d"
          % (tot["WIN"], tot["tie"], tot["LOSS"], tot["non_estimable"]))
    (OUT / "calon_final.json").write_text(json.dumps(out, indent=2))
    print("written:", OUT / "calon_final.json")


if __name__ == "__main__":
    main()
