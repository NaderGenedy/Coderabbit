#!/usr/bin/env python3
"""CALON-C — final specification. Raw-data facts measured BEFORE the spec was set.

SPECIFICATION
  PRIMARY (one equation, both cohorts)
      age, sp50, male, htn, dm, smoke, cum_nonhdl, tg_filter, remnant_unt
  SENSITIVITY "dated-only"
      age, sp50, male, cum_nonhdl, tg_filter, remnant_unt

WHY htn / dm / smoke ARE RETAINED IN THE PRIMARY
  Type 2 diabetes and hypertension are chronic conditions that in almost all
  cases precede an atherosclerotic event; a status field recording them is not
  the same class of problem as a lipid drawn after the event. All three published
  comparators carry hypertension and smoking as plain baseline covariates, so
  removing them from this model while the comparators keep them would be an
  unforced asymmetry that biases the head-to-head against us.

  The Welsh fields are nonetheless undated, and index-event bias is real. It is
  handled as a LIMITATION STATED WITH NUMBERS, not by deleting variables. Measured
  in code/32_MEASURE_BEFORE_BUILD.py, against raw:
     of 92 Welsh incident events, 55 (59.8%) have BP dated AFTER the event
     only 94 of 1,159 have BP dated on or before the baseline visit
     BloodPressureMedication carries no date column at all
     DiabetesYear covers 29 of 1,159; SmokerWhenStoppedYear covers 140
  The dated-only sensitivity arm quantifies exactly what the primary owes to
  these fields. In UK Biobank all three are properly measured at the baseline
  visit and carry no such concern.

  Lipids on the untreated scale throughout (TUDOR, JCLINLIPID-D-25-01142_R2:
  back-calculation validated against measured pre-treatment LDL-C, MAE 1.20
  mmol/L [1.13-1.28], r 0.32, N=649; discrimination robust to correction method,
  AUC range < 0.02). tg_filter is TUDOR's Triglyceride Filter.

  Excluded by investigator decision: any statin/treatment flag as a predictor,
  Lp(a), apoB, and any published score or derived linear predictor as an input.

ENDPOINT MEASUREMENT ERROR, QUANTIFIED NOT HIDDEN
  corrected_ascvd_outcomes.csv carries no per-component dates. Of 289 incident
  atherosclerotic cases, 75 also carry I50 and 97 carry more than one
  atherosclerotic component, so only 147 have an unambiguously attributable
  event date. ascvd_first_date_best and ascvd_first_date_dated agree in 289/289.
  Sensitivity S1 restricts the UKB endpoint to those 147.

Governance: aggregate output only; strata under 10 events suppressed.
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

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "outputs"; OUT.mkdir(exist_ok=True)
SEED, REPEATS, FOLDS, BOOT, MIN_EVENTS = 20260816, 10, 10, 2000, 10
STUDY_END = pd.Timestamp("2023-12-31")
PENALTY, F_LDL, F_TG = 0.02, 0.70, 0.80

# PRIMARY. Type 2 diabetes and hypertension are chronic conditions that in almost
# all cases predate an atherosclerotic event, and all three published comparators
# carry them as plain baseline covariates. Excluding them here while the
# comparators keep them would be an unforced asymmetry. The Welsh fields are
# undated, which is an index-event-bias LIMITATION to state with numbers, not a
# reason to delete the variables — quantified in code/32 and reported below.
SPEC_FULL = ["age", "sp50", "male", "htn", "dm", "smoke",
             "cum_nonhdl", "tg_filter", "remnant_unt"]
# SENSITIVITY only: strictly dated fields (age at the dated visit, sex, lipids
# at that visit). Shows what the primary owes to the undated status fields.
SPEC_CLEAN = ["age", "sp50", "male", "cum_nonhdl", "tg_filter", "remnant_unt"]

VARSET = {"SAFEHEART-RE": ["age", "male", "htn", "smoke", "bmi", "ldl_unt", "lpa"],
          "FH-Risk-Score": ["age", "male", "hdl", "ldl_unt", "htn", "smoke", "lpa"],
          "Montreal-FH-SCORE": ["age", "hdl", "male", "htn", "smoke"]}
NEEDS = dict(VARSET)
NEEDS_NOLPA = {k: [c for c in v if c != "lpa"] for k, v in NEEDS.items()}

_s = importlib.util.spec_from_file_location(
    "vw", ROOT / "code" / "audit_2026_08_10" / "07_verify_welsh_prospective.py")
vw = importlib.util.module_from_spec(_s); sys.modules["vw"] = vw; _s.loader.exec_module(vw)

R = Path(os.environ["CALON_CORRECTED_DATA"])
MP = Path(os.environ["CALON_SHARED_MASTER"]) / "UKB" / "ukb_master.csv"
WP = Path("/Users/nader85/Downloads/WALES_FH_CLEANED.csv")
if not WP.exists():
    WP = Path("/Users/nader85/Downloads/CALON_DATA_PACKAGE_2026-08-13/raw/all_inputs/WALES_FH_CLEANED.csv")

# --------------------------------------------------------------- comparators
SB = dict(male=.70, age30_59=1.07, age60=1.45, highbp=.69, prior=1.42, smoke=.48,
          overweight=.88, obesity=.98, ldl100_159=.92, ldl160=1.57, lpa50=.42)
SB_C, SB_S0 = 5.4078, {5: .9532, 10: .9025}


def safeheart_lp(age, male, hbp, prior, smoke, bmi, ldl_mg, lpa_mg):
    a = np.floor(np.asarray(age, float)); bmi = np.asarray(bmi, float)
    ldl, lpa = np.asarray(ldl_mg, float), np.asarray(lpa_mg, float)
    return (SB["male"] * np.asarray(male, float) + SB["age30_59"] * ((a >= 30) & (a < 60))
            + SB["age60"] * (a >= 60) + SB["highbp"] * np.asarray(hbp, float)
            + SB["prior"] * np.asarray(prior, float) + SB["smoke"] * np.asarray(smoke, float)
            + SB["overweight"] * ((bmi >= 25) & (bmi < 30)) + SB["obesity"] * (bmi >= 30)
            + SB["ldl100_159"] * ((ldl >= 100) & (ldl < 160)) + SB["ldl160"] * (ldl >= 160)
            + SB["lpa50"] * (lpa > 50)).astype(float)


def _sh_risk(lp, h): return 1.0 - SB_S0[h] ** np.exp(lp - SB_C)


def _test_safeheart():
    l1 = safeheart_lp([20], [0], [0], [0], [0], [22.], [90], [33])
    l2 = safeheart_lp([63], [1], [1], [1], [1], [32.], [182], [64])
    assert abs(l1[0]) < 1e-12 and abs(l2[0] - 7.71) < 1e-12
    r = dict(c1_5=float(_sh_risk(l1, 5)[0]), c1_10=float(_sh_risk(l1, 10)[0]),
             c2_5=float(_sh_risk(l2, 5)[0]), c2_10=float(_sh_risk(l2, 10)[0]))
    assert abs(r["c1_5"] - .0002148) < 5e-6 and abs(r["c2_5"] - .3808) < 5e-4
    assert abs(r["c1_10"] - .0004598) < 5e-6 and abs(r["c2_10"] - .6415) < 5e-4
    return r


def _band(x, edges, pts):
    x = np.asarray(x, float); out = np.full(x.shape, np.nan); prev = -np.inf
    for e, p in zip(edges, pts[:-1]):
        out = np.where((x > prev) & (x <= e), p, out); prev = e
    return np.where(x > prev, pts[-1], out)


def fhrs(age, male, hdl, ldl, htn, smoke, lpahi):
    a = np.floor(np.asarray(age, float))
    return (7. * np.asarray(male, float)
            + _band(a, [30, 35, 40, 45, 50, 55, 60], [0, 9, 14, 16, 17, 18, 20, 23])
            + _band(hdl, [.84, 1.00, 1.30], [8, 7, 3, 0])
            + _band(ldl, [5.5, 7.5, 8.5, 9.5], [0, 3, 7, 9, 11])
            + 6. * np.asarray(htn, float) + 6. * np.asarray(smoke, float)
            + 4. * np.asarray(lpahi, float))


def montreal(age, hdl, male, htn, smoke):
    a = np.floor(np.asarray(age, float))
    return (_band(a, [21, 28, 35, 42, 49, 56, 63], [0, 4, 8, 12, 16, 20, 24, 28])
            + _band(hdl, [.60, .90, 1.20, 1.50], [12, 9, 6, 3, 0])
            + 3. * np.asarray(male, float) + 2. * np.asarray(htn, float)
            + 1. * np.asarray(smoke, float))


def score_published(d, name, omit_lpa=False):
    need = (NEEDS_NOLPA if omit_lpa else NEEDS)[name]
    ok = np.ones(len(d), bool)
    for c in need:
        ok &= pd.to_numeric(d[c], errors="coerce").notna().values
    lpa = pd.Series(0.0, index=d.index) if omit_lpa else pd.to_numeric(d["lpa"], errors="coerce") / 2.15
    if name == "SAFEHEART-RE":
        s = safeheart_lp(d.age, d.male, d.htn, d.prior, d.smoke, d.bmi,
                         pd.to_numeric(d.ldl_unt, errors="coerce") * 38.67, lpa)
    elif name == "FH-Risk-Score":
        s = fhrs(d.age, d.male, d.hdl, d.ldl_unt, d.htn, d.smoke, (lpa >= 50).astype(float))
    else:
        s = montreal(d.age, d.hdl, d.male, d.htn, d.smoke)
    s = np.asarray(s, float); s[~ok] = np.nan; return s


# ------------------------------------------------------------------- cohorts
def _lipids(x, tc, hdl, ldl, tg, tx, f_ldl=F_LDL, f_tg=F_TG):
    txb = np.asarray(tx, float) > 0
    nh = (tc - hdl).where(lambda z: z.between(0.3, 20))
    x["nonhdl_unt"] = np.where(txb, nh / f_ldl, nh)
    x["ldl_unt"] = np.where(txb, ldl / f_ldl, ldl)
    tgu = np.where(txb, tg / f_tg, tg)
    x["remnant_unt"] = (pd.Series(x["nonhdl_unt"], index=x.index)
                        - pd.Series(x["ldl_unt"], index=x.index)).where(lambda z: z.between(-1, 6))
    x["tg_filter"] = np.log((pd.Series(x["ldl_unt"], index=x.index)
                             / (pd.Series(tgu, index=x.index) + 0.1)).where(lambda z: z.gt(0)))
    return x


def _finish(x):
    x["sp50"] = (x.age - 50).clip(lower=0)
    x["cum_nonhdl"] = np.log((pd.Series(x.nonhdl_unt, index=x.index) * x.age).where(lambda z: z.gt(0)))
    return x.replace([np.inf, -np.inf], np.nan).loc[x["T"].gt(0)].reset_index(drop=True)


def build_ukb(f_ldl=F_LDL):
    use = ["eid", "ldlr_carrier", "date_baseline", "age_exact_baseline", "age_at_recruit",
           "sex_F", "tc_chem", "hdl_chem", "ldl_chem", "tg_chem", "diabetes_combined",
           "smoking_ever", "smoking_current", "sbp", "dbp", "on_statin_self",
           "bmi_direct", "lpa_chem", "death_date"]
    m = pd.read_csv(MP, usecols=use, low_memory=False)
    c = pd.read_csv(R / "data_corrected" / "corrected_ascvd_outcomes.csv", low_memory=False)
    g = lambda k: pd.to_numeric(c[k], errors="coerce").fillna(0).gt(0)
    comps = ["i21_event", "i25_event", "i63_event", "i70_event", "i73_event", "g45_event"]
    c["athero"] = np.logical_or.reduce([g(k).values for k in comps])
    c["ncomp"] = sum(g(k).astype(int) for k in comps)
    c["hf"] = g("i50_event")
    md = pd.read_csv(R / "New folder" / "04a_meds_touch.csv", low_memory=False)
    md.columns = [x.replace("participant.", "") for x in md.columns]
    h2 = lambda col: md[col].astype(str).str.contains(r"\b2\b", na=False)
    md["bpmed"] = (h2("p6153_i0") | h2("p6177_i0")).astype(float)
    md.loc[~md[["p6153_i0", "p6177_i0"]].notna().any(axis=1), "bpmed"] = np.nan
    d = m.merge(c[["eid", "ascvd_first_date_best", "athero", "ncomp", "hf"]], on="eid", how="left") \
         .merge(md[["eid", "bpmed"]], on="eid", how="left")
    n = lambda x: pd.to_numeric(d[x], errors="coerce")
    d = d.loc[n("ldlr_carrier").eq(1)].reset_index(drop=True)
    n = lambda x: pd.to_numeric(d[x], errors="coerce")
    led = {"carriers": int(len(d))}
    base = pd.to_datetime(d.date_baseline, errors="coerce")
    ev = pd.to_datetime(d.ascvd_first_date_best, errors="coerce")
    death = pd.to_datetime(d.death_date, errors="coerce")
    ath = d["athero"].fillna(False).astype(bool)
    prev = ev.notna() & base.notna() & ev.le(base) & ath
    inc = ev.notna() & base.notna() & ev.gt(base) & ath
    und = ath & ev.isna()
    hf_only = ev.notna() & base.notna() & ev.gt(base) & ~ath
    led |= {"prevalent_excluded": int(prev.sum()), "undated_excluded": int(und.sum())}
    end = ev.where(inc | hf_only, death.fillna(STUDY_END))
    x = pd.DataFrame(index=d.index)
    x["age"] = n("age_exact_baseline").fillna(n("age_at_recruit"))
    x["male"] = 1 - n("sex_F").fillna(0)
    x = _lipids(x, n("tc_chem"), n("hdl_chem"), n("ldl_chem"), n("tg_chem"),
                n("on_statin_self").fillna(0).gt(0), f_ldl)
    x["hdl"], x["bmi"], x["lpa"] = n("hdl_chem"), n("bmi_direct"), n("lpa_chem")
    x["dm"] = n("diabetes_combined").gt(0).astype(float)
    x["smoke"] = n("smoking_current").fillna(n("smoking_ever")).gt(0).astype(float)
    x["htn"] = ((n("bpmed").fillna(0).gt(0)) | n("sbp").ge(140) | n("dbp").ge(90)).astype(float)
    x["prior"] = 0.0
    x["T"] = (end - base).dt.days / 365.25
    x["E"] = inc.astype(int)
    # S1: unambiguously attributable event date (no I50, single athero component)
    x["clean_date"] = (inc & ~d["hf"].fillna(False) & d["ncomp"].eq(1)).astype(int)
    x["cluster"] = np.arange(len(x))
    x = _finish(x.loc[~(prev | und)].reset_index(drop=True))
    led |= {"risk_set": int(len(x)), "events_full": int(x.E.sum()),
            "events_5y": int(((x.E == 1) & (x["T"] <= 5)).sum()),
            "events_10y": int(((x.E == 1) & (x["T"] <= 10)).sum()),
            "events_unambiguous_date": int(x.clean_date.sum())}
    return x, led


def build_wales(f_ldl=F_LDL):
    raw = pd.read_csv(WP, low_memory=False)
    flow, active, incident, bage = vw.reconstruct_wales(raw)
    n = lambda c: (pd.to_numeric(raw[c].astype(str).str.strip().replace(
        {"": np.nan, "Unknown": np.nan, "NoValue": np.nan, "nan": np.nan}), errors="coerce")
        if c in raw else pd.Series(np.nan, index=raw.index))
    dob = vw.date(raw, "DOB").fillna(vw.date(raw, "DOB_1"))
    age_at = lambda c: (vw.date(raw, c) - dob).dt.total_seconds() / (365.25 * 86400.)
    ev_age = pd.concat([n(c) for c in ["MIACSAge", "PCIStentsAge", "CABGAge",
                                       "ANGINAAge", "TIAAge", "PVDAge"]], axis=1).min(axis=1)
    last = pd.concat([age_at("MeasurementDate.%d" % i) for i in (1, 2, 3, 4)]
                     + [age_at("BMIDate")], axis=1).max(axis=1)
    exit_age = ev_age.where(incident, n("AGE_AT_DECEASED").fillna(last))
    tx = (vw.date(raw, "Treatmentdate1").notna() & vw.date(raw, "MeasurementDate.1").notna()
          & vw.date(raw, "Treatmentdate1").le(vw.date(raw, "MeasurementDate.1"))).astype(float)
    x = pd.DataFrame(index=raw.index)
    x["age"] = bage
    x["male"] = raw["Gender"].astype(str).str[0].str.upper().eq("M").astype(float)
    x = _lipids(x, n("TC.1"), n("HDL.1"), n("LDL.1"), n("TRG.1"), tx, f_ldl)
    x["hdl"], x["bmi"], x["lpa"] = n("HDL.1"), n("BMI"), np.nan
    sm, dm = n("Smoking"), n("Diabetes")
    x["smoke"], x["dm"] = sm.where(sm.isin([0, 1])), dm.where(dm.isin([0, 1]))
    x["htn"] = ((n("BloodPressureMedication").eq(1)) | n("BloodPressureSystolic").ge(140)
                | n("BloodPressureDiastolic").ge(90)).astype(float)
    x["prior"], x["clean_date"] = 0.0, 1
    x["T"] = exit_age - bage
    x["E"] = incident.astype(int)
    x["cluster"] = raw["FamilyNumber"].astype(str)
    x = _finish(x.loc[active].reset_index(drop=True))
    return x, {"Positive1_total": 2405, "exclusion_flow": flow["flow"], "risk_set": int(len(x)),
               "events_full": int(x.E.sum()),
               "events_5y": int(((x.E == 1) & (x["T"] <= 5)).sum()),
               "events_10y": int(((x.E == 1) & (x["T"] <= 10)).sum())}


def horizon(df, H):
    d = df.copy(); d["E"] = ((df.E == 1) & (df["T"] <= H)).astype(int)
    d["T"] = df["T"].clip(upper=H)
    return d.loc[d["T"].gt(0)].reset_index(drop=True)


# ------------------------------------------------------------------ modelling
def usable(df, feats):
    keep = []
    for f in feats:
        if f not in df:
            continue
        v = pd.to_numeric(df[f], errors="coerce")
        if v.notna().sum() < 50 or v.nunique(dropna=True) < 2:
            continue
        if set(v.dropna().unique()) <= {0., 1.}:
            ev = df.loc[v.notna(), "E"]; vv = v[v.notna()]
            if min(ev[vv == 0].sum(), ev[vv == 1].sum()) < MIN_EVENTS:
                continue
        if f != "age" and "age" in df:
            r = np.corrcoef(v.fillna(v.median()), df["age"].fillna(df["age"].median()))[0, 1]
            if abs(r) >= .999:
                continue
        keep.append(f)
    return keep


def _fit(tr, feats):
    m = tr[feats + ["T", "E"]].copy()
    for f in feats:
        m[f] = pd.to_numeric(m[f], errors="coerce").fillna(m[f].median())
    return CoxPHFitter(penalizer=PENALTY).fit(m, "T", "E")


def cv(df, feats, seed=SEED):
    feats = usable(df, feats)
    if not feats:
        return np.nan, np.full(len(df), np.nan), feats
    cl = pd.Series(df["cluster"].astype(str)).values; uniq = np.unique(cl)
    acc, cnt = np.zeros(len(df)), 0
    for rep in range(REPEATS):
        rng = np.random.default_rng(seed + rep)
        assign = dict(zip(uniq, rng.permutation(len(uniq)) % FOLDS))
        fold = np.array([assign[c] for c in cl]); lp = np.full(len(df), np.nan)
        for k in range(FOLDS):
            tr, te = df.loc[fold != k], df.loc[fold == k]
            if tr.E.sum() < MIN_EVENTS or len(te) == 0:
                continue
            try:
                cph = _fit(tr, feats)
            except Exception:
                continue
            med = {f: pd.to_numeric(tr[f], errors="coerce").median() for f in feats}
            mm = te[feats].copy()
            for f in feats:
                mm[f] = pd.to_numeric(mm[f], errors="coerce").fillna(med[f])
            lp[fold == k] = np.log(np.asarray(cph.predict_partial_hazard(mm), float))
        if np.isfinite(lp).all():
            acc += lp; cnt += 1
    if cnt == 0:
        return np.nan, np.full(len(df), np.nan), feats
    lp = acc / cnt
    return float(concordance_index(df["T"], -lp, df["E"])), lp, feats


def delta_ci(d, a, b, seed=SEED):
    if d.E.sum() < MIN_EVENTS:
        return None
    ca, cb = concordance_index(d["T"], -a, d["E"]), concordance_index(d["T"], -b, d["E"])
    gi = d.groupby(d["cluster"].astype(str)).indices; keys = list(gi)
    rng = np.random.default_rng(seed); draws = []
    for _ in range(BOOT):
        idx = np.concatenate([gi[keys[i]] for i in rng.choice(len(keys), len(keys), True)])
        s = d.iloc[idx]
        if s.E.sum() < MIN_EVENTS:
            continue
        try:
            draws.append(concordance_index(s["T"], -a[idx], s["E"])
                         - concordance_index(s["T"], -b[idx], s["E"]))
        except Exception:
            pass
    if len(draws) < 100:
        return None
    lo, hi = np.percentile(draws, [2.5, 97.5])
    return dict(C_model=float(ca), C_comparator=float(cb), delta=float(ca - cb),
                lo=float(lo), hi=float(hi), B_eff=len(draws),
                rho=float(pd.Series(a).corr(pd.Series(b), method="spearman")),
                floor=float(1.96 * np.std(draws, ddof=1)),
                verdict="WIN" if lo > 0 else ("LOSS" if hi < 0 else "TIE"))


def calibration(df, lp, H):
    d = horizon(df, H)
    m = pd.DataFrame({"lp": lp, "T": d["T"], "E": d["E"]}).dropna()
    if m.E.sum() < MIN_EVENTS:
        return None
    try:
        c = CoxPHFitter(penalizer=0.).fit(m, "T", "E")
    except Exception:
        return None
    s, se = float(c.params_["lp"]), float(c.standard_errors_["lp"])
    return dict(horizon=H, slope=s, lo=s - 1.96 * se, hi=s + 1.96 * se,
                observed_rate=float(m.E.mean()), n=int(len(m)), events=int(m.E.sum()))


def main():
    res = {"primary_spec": SPEC_FULL, "sensitivity_spec": SPEC_CLEAN, "seed": SEED, "boot": BOOT,
           "index_event_bias_limitation": "Welsh htn/dm/smoke are undated status fields. Clinically T2DM and hypertension almost always predate an atherosclerotic event, and all three comparators use them as baseline covariates, so they are retained. Measured contamination, to be stated in Limitations: of 92 Welsh events, 55 (59.8%) have BP dated after the event; only 94/1159 have BP dated on or before baseline; DiabetesYear covers 29/1159; SmokerWhenStoppedYear covers 140/1159. The SENS dated-only arm quantifies what the primary owes to these fields.",
           "untreated": {"f_ldl": F_LDL, "f_tg": F_TG,
                         "source": "TUDOR JCLINLIPID-D-25-01142_R2; MAE 1.20 (1.13-1.28), "
                                   "r 0.32, N=649; robust to method, AUC range <0.02"}}
    print("=" * 84)
    res["safeheart_unit_test"] = _test_safeheart()
    print("SAFEHEART unit test:", {k: round(v, 6) for k, v in res["safeheart_unit_test"].items()})
    ukb, lu = build_ukb(); wal, lw = build_wales()
    res["ledger_ukb"], res["ledger_wales"] = lu, lw
    print("UKB  ", json.dumps(lu)); print("Wales", json.dumps({k: v for k, v in lw.items() if k != "exclusion_flow"}))
    res["gates"] = {"3540": lu["carriers"] == 3540, "207": lu["prevalent_excluded"] == 207,
                    "124": lu["undated_excluded"] == 124, "3209": lu["risk_set"] == 3209,
                    "289": lu["events_full"] == 289, "97": lu["events_5y"] == 97,
                    "194": lu["events_10y"] == 194}
    print("GATES", json.dumps(res["gates"]))

    rows, cal = [], []
    arms = [("UK Biobank", ukb, SPEC_FULL, "PRIMARY"),
            ("Wales", wal, SPEC_FULL, "PRIMARY"),
            ("UK Biobank", ukb, SPEC_CLEAN, "SENS dated-only"),
            ("Wales", wal, SPEC_CLEAN, "SENS dated-only")]
    for cname, df0, spec, arm in arms:
        for H, hl in ((None, "full"), (10, "10y"), (5, "5y")):
            d = df0 if H is None else horizon(df0, H)
            if d.E.sum() < MIN_EVENTS:
                continue
            c_all, lp, feats = cv(d, spec)
            epv = d.E.sum() / max(len(feats), 1)
            print(f"  {arm:20s} {cname:11s} {hl:5s} n={len(d):5d} ev={int(d.E.sum()):4d} "
                  f"C={c_all:.4f} terms={len(feats)} EPV={epv:.1f}")
            if H is not None:
                cb = calibration(df0, lp, H)
                if cb:
                    cal.append({"arm": arm, "cohort": cname, **cb})
            if arm != "PRIMARY":
                continue
            for comp in NEEDS:
                for pol, _ in (("strict", 0), ("lpa_omitted", 1)):
                    s = score_published(d, comp, omit_lpa=(pol == "lpa_omitted"))
                    ok = np.isfinite(s) & np.isfinite(lp)
                    if ok.sum() < 50:
                        rows.append(dict(arm=arm, cohort=cname, horizon=hl, comparator=comp,
                                         estimand="published", lpa_policy=pol,
                                         n_eval=int(ok.sum()), note="NOT_EVALUABLE")); continue
                    r = delta_ci(d.loc[ok].reset_index(drop=True), lp[ok], s[ok])
                    if r:
                        rows.append(dict(arm=arm, cohort=cname, horizon=hl, comparator=comp,
                                         estimand="published", lpa_policy=pol,
                                         n_eval=int(ok.sum()),
                                         events_eval=int(d.loc[ok, "E"].sum()), **r))
                vs = [v for v in VARSET[comp] if v in d.columns
                      and pd.to_numeric(d[v], errors="coerce").notna().sum() >= 50]
                _, lpv, _ = cv(d, vs)
                if np.isfinite(lpv).all():
                    r = delta_ci(d, lp, lpv)
                    if r:
                        rows.append(dict(arm=arm, cohort=cname, horizon=hl, comparator=comp,
                                         estimand="refit_varset", lpa_policy="n/a",
                                         n_eval=int(len(d)), events_eval=int(d.E.sum()), **r))
            _, lpas, _ = cv(d, ["age", "male"])
            r = delta_ci(d, lp, lpas)
            if r:
                rows.append(dict(arm=arm, cohort=cname, horizon=hl, comparator="age+sex",
                                 estimand="refit_varset", lpa_policy="n/a",
                                 n_eval=int(len(d)), events_eval=int(d.E.sum()), **r))

    # ---- transport, one equation, both directions
    def transport(dev, val, dn, vn):
        f = [x for x in usable(dev, SPEC_FULL) if x in val.columns]
        cph = _fit(dev, f); med = {k: pd.to_numeric(dev[k], errors="coerce").median() for k in f}
        m = val[f].copy()
        for k in f:
            m[k] = pd.to_numeric(m[k], errors="coerce").fillna(med[k])
        lp = np.log(np.asarray(cph.predict_partial_hazard(m), float))
        return dict(dev=dn, val=vn, terms=f, C=float(concordance_index(val["T"], -lp, val["E"])),
                    n=int(len(val)), events=int(val.E.sum()))
    res["transport"] = [transport(ukb, wal, "UK Biobank", "Wales"),
                        transport(wal, ukb, "Wales", "UK Biobank")]
    for t in res["transport"]:
        print(f"  transport {t['dev']:11s} -> {t['val']:11s} C={t['C']:.4f} ({len(t['terms'])} terms)")

    # ---- S1 unambiguous-date endpoint
    u1 = ukb.copy(); u1["E"] = u1["clean_date"]
    c1, _, f1 = cv(u1, SPEC_FULL)
    res["S1_unambiguous_date"] = {"events": int(u1.E.sum()), "C": c1, "terms": f1}
    print(f"  S1 unambiguous-date endpoint: {int(u1.E.sum())} events, C={c1:.4f}")

    # ---- S2 correction-factor sensitivity
    s2 = []
    for f in (0.65, 0.70, 0.75):
        uu, _ = build_ukb(f_ldl=f); cc, _, _ = cv(uu, SPEC_FULL)
        ww, _ = build_wales(f_ldl=f); cw, _, _ = cv(ww, SPEC_FULL)
        s2.append({"f_ldl": f, "C_ukb": cc, "C_wales": cw})
        print(f"  S2 f_ldl={f}: UKB {cc:.4f}  Wales {cw:.4f}")
    res["S2_correction_factor"] = s2
    res["head_to_head"], res["calibration"] = rows, cal
    (OUT / "calon_c.json").write_text(json.dumps(res, indent=2, default=str))
    pd.DataFrame(rows).to_csv(OUT / "calon_c_headtohead.csv", index=False)
    print("=" * 84); print("written:", OUT / "calon_c.json")


if __name__ == "__main__":
    main()
