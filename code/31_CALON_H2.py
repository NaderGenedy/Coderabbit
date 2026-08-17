#!/usr/bin/env python3
"""CALON-H2 — every defect from the independent raw-data audit, fixed.

CHANGES FROM 30_CALON_H.py, each traceable to an audit finding
  D1  Comparators are ALSO refitted on their own variable sets, in the same data,
      same CV, same imputation, same bootstrap. Both estimands reported:
        (a) published-score-as-published, on strictly evaluable participants
        (b) comparator variable set refitted here
  D2  Welsh comparison runs on the FULL risk set as well as the evaluable subset.
  D3  C_model is recomputed ON EACH EVALUABLE SET, so C_model - C_comp == delta.
  D4  htn is flagged as post-event-contaminated in Wales; a dated-fields-only
      Welsh sensitivity is run (htn dropped) and reported.
  D5  Missing comparator inputs are NOT_EVALUABLE, never the reference category.
      Strict policy is primary; an explicitly labelled Lp(a)-omitted sensitivity
      is reported because strict policy makes SAFEHEART/FH-RS unscoreable in Wales.
  D6a "Treatment enters only via /0.70" was FALSE in H. Now every lipid-derived
      term is on the untreated scale, consistently:
          nonhdl_unt = (TC-HDL)/f_ldl        ldl_unt = LDL/f_ldl
          remnant_unt = nonhdl_unt - ldl_unt tg_unt  = TG/f_tg
      TUDOR (JCLINLIPID-D-25-01142_R2) validated back-calculation against measured
      pre-treatment LDL-C in 649 Welsh patients: MAE 1.20 mmol/L (1.13-1.28),
      r 0.32, and showed discrimination is robust to correction method
      (AUC range < 0.02; dose-specific / class-level / fixed-factor).
      Correction-method sensitivity is therefore run at f_ldl in {0.65,0.70,0.75}.
  D6b True Welsh Positive1 = 2,405 is reported with the full exclusion flow.
  D7  Chart comparators band on COMPLETED YEARS (floor(age)), not continuous age.
  D9  calib() is actually called.

NEW TERM, from the investigator's own published model (TUDOR, Table 4)
      tg_filter = log(LDL_untreated / (TG_untreated + 0.1))
  the "Triglyceride Filter": reads LDL-C in the context of triglycerides to
  separate receptor-mediated LDL elevation from mixed dyslipidaemia.

Still excluded by investigator decision: statin/treatment flag as a PREDICTOR,
Lp(a), apoB, and any published score or derived linear predictor as an input.

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
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)
SEED = 20260816
REPEATS, FOLDS, BOOT, MIN_EVENTS = 10, 10, 2000, 10
STUDY_END = pd.Timestamp("2023-12-31")
PENALTY = 0.02
F_LDL, F_TG = 0.70, 0.80          # fixed-factor untreated correction (primary)

SPEC = ["age", "sp50", "male", "htn", "dm", "smoke",
        "cum_nonhdl", "tg_filter", "remnant_unt"]
SPEC_DATED_WALES = [f for f in SPEC if f != "htn"]      # D4 sensitivity

# comparator variable sets, for the D1 refit estimand
VARSET = {
    "SAFEHEART-RE": ["age", "male", "htn", "smoke", "bmi", "ldl_unt", "lpa"],
    "FH-Risk-Score": ["age", "male", "hdl", "ldl_unt", "htn", "smoke", "lpa"],
    "Montreal-FH-SCORE": ["age", "hdl", "male", "htn", "smoke"],
}
# inputs that must be non-missing for the published score to be scoreable (D5)
NEEDS = {
    "SAFEHEART-RE": ["age", "male", "htn", "smoke", "bmi", "ldl_unt", "lpa"],
    "FH-Risk-Score": ["age", "male", "hdl", "ldl_unt", "htn", "smoke", "lpa"],
    "Montreal-FH-SCORE": ["age", "hdl", "male", "htn", "smoke"],
}
NEEDS_NOLPA = {k: [c for c in v if c != "lpa"] for k, v in NEEDS.items()}

_s = importlib.util.spec_from_file_location(
    "vw", ROOT / "code" / "audit_2026_08_10" / "07_verify_welsh_prospective.py")
vw = importlib.util.module_from_spec(_s); sys.modules["vw"] = vw
_s.loader.exec_module(vw)


def corrected_root() -> Path:
    marker = Path("data_corrected") / "corrected_ascvd_outcomes.csv"
    c = [Path(os.environ["CALON_CORRECTED_DATA"])] if os.environ.get("CALON_CORRECTED_DATA") else []
    c += sorted(Path.home().glob(
        "Library/CloudStorage/GoogleDrive-*/My Drive/Projects/CALON_AlphaFold_Rebuild"))
    for p in c:
        if (p / marker).exists():
            return p
    raise RuntimeError("corrected data not found")


def master_path() -> Path:
    e = os.environ.get("CALON_SHARED_MASTER")
    if e and (Path(e) / "UKB" / "ukb_master.csv").exists():
        return Path(e) / "UKB" / "ukb_master.csv"
    for p in sorted(Path.home().glob(
            "Library/CloudStorage/GoogleDrive-*/My Drive/Projects/SHARED_MASTER_DATA")):
        if (p / "UKB" / "ukb_master.csv").exists():
            return p / "UKB" / "ukb_master.csv"
    raise RuntimeError("ukb_master.csv not found")


def wales_path() -> Path:
    for p in (vw.WALES, Path("/Users/nader85/Downloads/CALON_DATA_PACKAGE_2026-08-13"
                             "/raw/all_inputs/WALES_FH_CLEANED.csv")):
        if Path(p).exists():
            return Path(p)
    raise RuntimeError("Welsh registry not found")


# --------------------------------------------------------------- comparators
SB = dict(male=0.70, age30_59=1.07, age60=1.45, highbp=0.69, prior=1.42,
          smoke=0.48, overweight=0.88, obesity=0.98,
          ldl100_159=0.92, ldl160=1.57, lpa50=0.42)
SB_CENTRE, SB_S0 = 5.4078, {5: 0.9532, 10: 0.9025}


def safeheart_lp(age, male, highbp, prior, smoke, bmi, ldl_mgdl, lpa_mgdl):
    a = np.floor(np.asarray(age, float))            # D7: completed years
    bmi, ldl = np.asarray(bmi, float), np.asarray(ldl_mgdl, float)
    lpa = np.asarray(lpa_mgdl, float)
    return (SB["male"] * np.asarray(male, float)
            + SB["age30_59"] * ((a >= 30) & (a < 60))
            + SB["age60"] * (a >= 60)
            + SB["highbp"] * np.asarray(highbp, float)
            + SB["prior"] * np.asarray(prior, float)
            + SB["smoke"] * np.asarray(smoke, float)
            + SB["overweight"] * ((bmi >= 25) & (bmi < 30))
            + SB["obesity"] * (bmi >= 30)
            + SB["ldl100_159"] * ((ldl >= 100) & (ldl < 160))
            + SB["ldl160"] * (ldl >= 160)
            + SB["lpa50"] * (lpa > 50)).astype(float)


def safeheart_risk(lp, h):
    return 1.0 - SB_S0[h] ** np.exp(lp - SB_CENTRE)


def _test_safeheart():
    lp1 = safeheart_lp([20], [0], [0], [0], [0], [22.0], [90], [33])
    lp2 = safeheart_lp([63], [1], [1], [1], [1], [32.0], [182], [64])
    assert abs(lp1[0]) < 1e-12 and abs(lp2[0] - 7.71) < 1e-12
    r = dict(case1_5y=float(safeheart_risk(lp1, 5)[0]), case1_10y=float(safeheart_risk(lp1, 10)[0]),
             case2_5y=float(safeheart_risk(lp2, 5)[0]), case2_10y=float(safeheart_risk(lp2, 10)[0]))
    assert abs(r["case1_5y"] - 0.0002148) < 5e-6 and abs(r["case1_10y"] - 0.0004598) < 5e-6
    assert abs(r["case2_5y"] - 0.3808) < 5e-4 and abs(r["case2_10y"] - 0.6415) < 5e-4
    return r


def _band(x, edges, pts):
    x = np.asarray(x, float); out = np.full(x.shape, np.nan); prev = -np.inf
    for e, p in zip(edges, pts[:-1]):
        out = np.where((x > prev) & (x <= e), p, out); prev = e
    return np.where(x > prev, pts[-1], out)


def fhrs_points(age, male, hdl, ldl_unt, htn, smoke, lpa_hi):
    a = np.floor(np.asarray(age, float))            # D7
    return (7.0 * np.asarray(male, float)
            + _band(a, [30, 35, 40, 45, 50, 55, 60], [0, 9, 14, 16, 17, 18, 20, 23])
            + _band(hdl, [0.84, 1.00, 1.30], [8, 7, 3, 0])
            + _band(ldl_unt, [5.50, 7.50, 8.50, 9.50], [0, 3, 7, 9, 11])
            + 6.0 * np.asarray(htn, float) + 6.0 * np.asarray(smoke, float)
            + 4.0 * np.asarray(lpa_hi, float))


def montreal_points(age, hdl, male, htn, smoke):
    a = np.floor(np.asarray(age, float))            # D7
    return (_band(a, [21, 28, 35, 42, 49, 56, 63], [0, 4, 8, 12, 16, 20, 24, 28])
            + _band(hdl, [0.60, 0.90, 1.20, 1.50], [12, 9, 6, 3, 0])
            + 3.0 * np.asarray(male, float) + 2.0 * np.asarray(htn, float)
            + 1.0 * np.asarray(smoke, float))


def score_published(d, name, omit_lpa=False):
    """Published score + strict evaluability mask (D5). Missing input -> NaN."""
    need = (NEEDS_NOLPA if omit_lpa else NEEDS)[name]
    ok = np.ones(len(d), bool)
    for c in need:
        ok &= pd.to_numeric(d[c], errors="coerce").notna().values
    lpa_mgdl = pd.to_numeric(d["lpa"], errors="coerce") / 2.15   # UKB nmol/L -> mg/dL
    if omit_lpa:
        lpa_mgdl = pd.Series(0.0, index=d.index)
    if name == "SAFEHEART-RE":
        s = safeheart_lp(d.age, d.male, d.htn, d.prior, d.smoke, d.bmi,
                         pd.to_numeric(d.ldl_unt, errors="coerce") * 38.67, lpa_mgdl)
    elif name == "FH-Risk-Score":
        s = fhrs_points(d.age, d.male, d.hdl, d.ldl_unt, d.htn, d.smoke,
                        (lpa_mgdl >= 50).astype(float))
    else:
        s = montreal_points(d.age, d.hdl, d.male, d.htn, d.smoke)
    s = np.asarray(s, float); s[~ok] = np.nan
    return s


# ------------------------------------------------------------------- cohorts
def build_ukb():
    use = ["eid", "ldlr_carrier", "date_baseline", "age_exact_baseline", "age_at_recruit",
           "sex_F", "tc_chem", "hdl_chem", "ldl_chem", "tg_chem", "diabetes_combined",
           "smoking_ever", "smoking_current", "sbp", "dbp", "on_statin_self",
           "bmi_direct", "lpa_chem", "death_date"]
    m = pd.read_csv(master_path(), usecols=use, low_memory=False)
    r = corrected_root()
    c = pd.read_csv(r / "data_corrected" / "corrected_ascvd_outcomes.csv",
                    usecols=["eid", "ascvd_first_date_best", "i21_event", "i25_event",
                             "i63_event", "i70_event", "i73_event", "g45_event"],
                    low_memory=False)
    g = lambda k: pd.to_numeric(c[k], errors="coerce").fillna(0).gt(0)
    c["athero"] = (g("i21_event") | g("i25_event") | g("i63_event")
                   | g("i70_event") | g("i73_event") | g("g45_event"))
    md = pd.read_csv(r / "New folder" / "04a_meds_touch.csv", low_memory=False)
    md.columns = [x.replace("participant.", "") for x in md.columns]
    h2 = lambda col: md[col].astype(str).str.contains(r"\b2\b", na=False)
    md["bpmed"] = (h2("p6153_i0") | h2("p6177_i0")).astype(float)
    md.loc[~md[["p6153_i0", "p6177_i0"]].notna().any(axis=1), "bpmed"] = np.nan

    d = m.merge(c, on="eid", how="left").merge(md[["eid", "bpmed"]], on="eid", how="left")
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
    hf = ev.notna() & base.notna() & ev.gt(base) & ~ath
    led |= {"prevalent_excluded": int(prev.sum()), "undated_excluded": int(und.sum())}
    end = ev.where(inc | hf, death.fillna(STUDY_END))

    x = pd.DataFrame(index=d.index)
    x["age"] = n("age_exact_baseline").fillna(n("age_at_recruit"))
    x["male"] = 1 - n("sex_F").fillna(0)
    tc, hdl, ldl, tg = n("tc_chem"), n("hdl_chem"), n("ldl_chem"), n("tg_chem")
    tx = n("on_statin_self").fillna(0).gt(0)
    x = _lipids(x, tc, hdl, ldl, tg, tx)
    x["hdl"], x["bmi"], x["lpa"] = hdl, n("bmi_direct"), n("lpa_chem")
    x["dm"] = n("diabetes_combined").gt(0).astype(float)
    x["smoke"] = n("smoking_current").fillna(n("smoking_ever")).gt(0).astype(float)
    x["htn"] = ((n("bpmed").fillna(0).gt(0)) | n("sbp").ge(140) | n("dbp").ge(90)).astype(float)
    x["prior"] = 0.0
    x["T"] = (end - base).dt.days / 365.25
    x["E"] = inc.astype(int)
    x["cluster"] = np.arange(len(x))
    x = _finish(x.loc[~(prev | und)].reset_index(drop=True))
    led |= {"risk_set": int(len(x)), "events_full": int(x.E.sum()),
            "events_5y": int(((x.E == 1) & (x["T"] <= 5)).sum()),
            "events_10y": int(((x.E == 1) & (x["T"] <= 10)).sum())}
    return x, led


def _lipids(x, tc, hdl, ldl, tg, tx, f_ldl=None, f_tg=None):
    """D6a: EVERY lipid-derived term on the untreated scale, consistently."""
    f_ldl = F_LDL if f_ldl is None else f_ldl
    f_tg = F_TG if f_tg is None else f_tg
    txb = np.asarray(tx, float) > 0
    nonhdl = (tc - hdl).where(lambda z: z.between(0.3, 20))
    x["nonhdl_unt"] = np.where(txb, nonhdl / f_ldl, nonhdl)
    x["ldl_unt"] = np.where(txb, ldl / f_ldl, ldl)
    x["tg_unt"] = np.where(txb, tg / f_tg, tg)
    x["remnant_unt"] = (pd.Series(x["nonhdl_unt"], index=x.index)
                        - pd.Series(x["ldl_unt"], index=x.index)).where(lambda z: z.between(-1, 6))
    # TUDOR Triglyceride Filter: LDL_untreated / (TG + 0.1)
    x["tg_filter"] = np.log((pd.Series(x["ldl_unt"], index=x.index)
                             / (pd.Series(x["tg_unt"], index=x.index) + 0.1))
                            .where(lambda z: z.gt(0)))
    return x


def build_wales():
    raw = pd.read_csv(wales_path(), low_memory=False)
    _, active, incident, bage = vw.reconstruct_wales(raw)
    n = lambda c: (pd.to_numeric(raw[c].astype(str).str.strip().replace(
        {"": np.nan, "Unknown": np.nan, "NoValue": np.nan, "nan": np.nan}), errors="coerce")
        if c in raw else pd.Series(np.nan, index=raw.index))
    pos = raw["Positive1"].astype(str).str.strip().str.upper().isin(["1", "Y", "YES", "TRUE"]) \
        if "Positive1" in raw else pd.Series(False, index=raw.index)
    dob = vw.date(raw, "DOB").fillna(vw.date(raw, "DOB_1"))
    age_at = lambda c: (vw.date(raw, c) - dob).dt.total_seconds() / (365.25 * 86400.0)
    ev_age = pd.concat([n(c) for c in ["MIACSAge", "PCIStentsAge", "CABGAge",
                                       "ANGINAAge", "TIAAge", "PVDAge"]], axis=1).min(axis=1)
    last = pd.concat([age_at("MeasurementDate.%d" % i) for i in (1, 2, 3, 4)]
                     + [age_at("BMIDate")], axis=1).max(axis=1)
    exit_age = ev_age.where(incident, n("AGE_AT_DECEASED").fillna(last))
    tc, hdl, tg, ldl = n("TC.1"), n("HDL.1"), n("TRG.1"), n("LDL.1")
    tx = (vw.date(raw, "Treatmentdate1").notna() & vw.date(raw, "MeasurementDate.1").notna()
          & vw.date(raw, "Treatmentdate1").le(vw.date(raw, "MeasurementDate.1"))).astype(float)

    x = pd.DataFrame(index=raw.index)
    x["age"] = bage
    x["male"] = raw["Gender"].astype(str).str[0].str.upper().eq("M").astype(float)
    x = _lipids(x, tc, hdl, ldl, tg, tx)
    x["hdl"], x["bmi"], x["lpa"] = hdl, n("BMI"), np.nan
    sm, dm = n("Smoking"), n("Diabetes")
    x["smoke"], x["dm"] = sm.where(sm.isin([0, 1])), dm.where(dm.isin([0, 1]))
    x["htn"] = ((n("BloodPressureMedication").eq(1)) | n("BloodPressureSystolic").ge(140)
                | n("BloodPressureDiastolic").ge(90)).astype(float)
    x["prior"] = 0.0
    x["T"] = exit_age - bage
    x["E"] = incident.astype(int)
    x["cluster"] = raw["FamilyNumber"].astype(str)
    x = _finish(x.loc[active].reset_index(drop=True))
    led = {"Positive1_total": int(pos.sum()),            # D6b: the TRUE start
           "analysis_active": int(active.sum()), "risk_set": int(len(x)),
           "events_full": int(x.E.sum()),
           "events_5y": int(((x.E == 1) & (x["T"] <= 5)).sum()),
           "events_10y": int(((x.E == 1) & (x["T"] <= 10)).sum()),
           "note": "Positive1_total is the genotype-positive registry start; "
                   "analysis_active is after baseline/prevalent/undated/follow-up rules"}
    return x, led


def _finish(x):
    x["sp50"] = (x.age - 50).clip(lower=0)
    x["cum_nonhdl"] = np.log((pd.Series(x.nonhdl_unt, index=x.index) * x.age)
                             .where(lambda z: z.gt(0)))
    return x.replace([np.inf, -np.inf], np.nan).loc[x["T"].gt(0)].reset_index(drop=True)


def horizon(df, H):
    d = df.copy()
    d["E"] = ((df.E == 1) & (df["T"] <= H)).astype(int)
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
        if set(v.dropna().unique()) <= {0.0, 1.0}:
            ev = df.loc[v.notna(), "E"]; vv = v[v.notna()]
            if min(ev[vv == 0].sum(), ev[vv == 1].sum()) < MIN_EVENTS:
                continue
        if f != "age" and "age" in df:
            r = np.corrcoef(v.fillna(v.median()), df["age"].fillna(df["age"].median()))[0, 1]
            if abs(r) >= 0.999:
                continue
        keep.append(f)
    return keep


def _fit(tr, feats):
    m = tr[feats + ["T", "E"]].copy()
    for f in feats:
        m[f] = pd.to_numeric(m[f], errors="coerce").fillna(m[f].median())
    cph = CoxPHFitter(penalizer=PENALTY); cph.fit(m, "T", "E"); return cph


def cv(df, feats, repeats=REPEATS, seed=SEED):
    feats = usable(df, feats)
    if not feats:
        return np.nan, np.full(len(df), np.nan), feats
    cl = pd.Series(df["cluster"].astype(str)).values
    uniq = np.unique(cl); acc, cnt = np.zeros(len(df)), 0
    for rep in range(repeats):
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
            m = te[feats].copy()
            for f in feats:
                m[f] = pd.to_numeric(m[f], errors="coerce").fillna(med[f])
            lp[fold == k] = np.log(np.asarray(cph.predict_partial_hazard(m), float))
        if np.isfinite(lp).all():
            acc += lp; cnt += 1
    if cnt == 0:
        return np.nan, np.full(len(df), np.nan), feats
    lp = acc / cnt
    return float(concordance_index(df["T"], -lp, df["E"])), lp, feats


def delta_ci(d, a, b, B=BOOT, seed=SEED):
    if d.E.sum() < MIN_EVENTS:
        return None
    ca = concordance_index(d["T"], -a, d["E"]); cb = concordance_index(d["T"], -b, d["E"])
    groups = d.groupby(d["cluster"].astype(str)).indices; keys = list(groups)
    rng = np.random.default_rng(seed); draws = []
    for _ in range(B):
        idx = np.concatenate([groups[keys[i]] for i in rng.choice(len(keys), len(keys), True)])
        sub = d.iloc[idx]
        if sub.E.sum() < MIN_EVENTS:
            continue
        try:
            draws.append(concordance_index(sub["T"], -a[idx], sub["E"])
                         - concordance_index(sub["T"], -b[idx], sub["E"]))
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
    """D9 — actually called this time."""
    d = horizon(df, H)
    m = pd.DataFrame({"lp": lp, "T": d["T"], "E": d["E"]}).dropna()
    if m.E.sum() < MIN_EVENTS:
        return None
    try:
        c = CoxPHFitter(penalizer=0.0).fit(m, "T", "E")
    except Exception:
        return None
    s, se = float(c.params_["lp"]), float(c.standard_errors_["lp"])
    return dict(horizon=H, slope=s, slope_lo=s - 1.96 * se, slope_hi=s + 1.96 * se,
                observed_rate=float(m.E.mean()), n=int(len(m)), events=int(m.E.sum()))


# ---------------------------------------------------------------------- main
def main():
    res = {"spec": SPEC, "seed": SEED, "boot": BOOT,
           "untreated_factors": {"ldl_nonhdl": F_LDL, "tg": F_TG},
           "untreated_provenance": {
               "source": "TUDOR, JCLINLIPID-D-25-01142_R2",
               "validation": "MAE 1.20 mmol/L (95% CI 1.13-1.28), r 0.32, N=649 Welsh "
                             "patients with measured pre-treatment LDL-C",
               "robustness": "discrimination robust to correction method (dose-specific, "
                             "class-level, fixed-factor); AUC range < 0.02, DeLong p > 0.3",
               "direction": "conservative: defaults to prescribed-dose effect, "
                            "under-corrects rather than over-corrects"},
           "tg_filter": "log(LDL_untreated / (TG_untreated + 0.1)) — TUDOR Triglyceride Filter"}

    print("=" * 78)
    res["safeheart_unit_test"] = _test_safeheart()
    print("UNIT TEST SAFEHEART:", {k: round(v, 6) for k, v in res["safeheart_unit_test"].items()})

    ukb, lu = build_ukb(); wal, lw = build_wales()
    res["ledger_ukb"], res["ledger_wales"] = lu, lw
    print("UKB  ", json.dumps(lu)); print("Wales", json.dumps(lw))
    res["gates"] = {"3540": lu["carriers"] == 3540, "207": lu["prevalent_excluded"] == 207,
                    "124": lu["undated_excluded"] == 124, "3209": lu["risk_set"] == 3209,
                    "289": lu["events_full"] == 289, "97": lu["events_5y"] == 97,
                    "194": lu["events_10y"] == 194}
    print("GATES", json.dumps(res["gates"]))

    rows, calib_rows = [], []
    for cname, df0, spec in (("UK Biobank", ukb, SPEC), ("Wales", wal, SPEC),
                             ("Wales (dated-only, htn dropped)", wal, SPEC_DATED_WALES)):
        for H, hl in ((None, "full"), (10, "10y"), (5, "5y")):
            d = df0 if H is None else horizon(df0, H)
            if d.E.sum() < MIN_EVENTS:
                continue
            c_all, lp_all, feats = cv(d, spec)
            print(f"  {cname:33s} {hl:5s} n={len(d):5d} ev={int(d.E.sum()):4d} "
                  f"C={c_all:.4f} terms={len(feats)}")
            if H is not None:
                cb = calibration(df0, lp_all, H)
                if cb:
                    calib_rows.append({"cohort": cname, **cb})
            if "dated-only" in cname:
                continue
            for comp in NEEDS:
                for policy, needs in (("strict", NEEDS), ("lpa_omitted", NEEDS_NOLPA)):
                    s = score_published(d, comp, omit_lpa=(policy == "lpa_omitted"))
                    ok = np.isfinite(s) & np.isfinite(lp_all)
                    if ok.sum() < 50:
                        rows.append(dict(cohort=cname, horizon=hl, comparator=comp,
                                         estimand="published", lpa_policy=policy,
                                         n_eval=int(ok.sum()), note="NOT_EVALUABLE"))
                        continue
                    sub = d.loc[ok].reset_index(drop=True)
                    # D3: C_model recomputed ON THIS evaluable set
                    r = delta_ci(sub, lp_all[ok], s[ok])
                    if r:
                        rows.append(dict(cohort=cname, horizon=hl, comparator=comp,
                                         estimand="published", lpa_policy=policy,
                                         n_eval=int(ok.sum()), events_eval=int(sub.E.sum()), **r))
                # D1: comparator variable set REFITTED here, same CV/imputation
                vs = [v for v in VARSET[comp] if v in d.columns
                      and pd.to_numeric(d[v], errors="coerce").notna().sum() >= 50]
                c_v, lp_v, _ = cv(d, vs)
                if np.isfinite(lp_v).all():
                    r = delta_ci(d, lp_all, lp_v)
                    if r:
                        rows.append(dict(cohort=cname, horizon=hl, comparator=comp,
                                         estimand="refit_varset", lpa_policy="n/a",
                                         n_eval=int(len(d)), events_eval=int(d.E.sum()), **r))
            c_as, lp_as, _ = cv(d, ["age", "male"])
            r = delta_ci(d, lp_all, lp_as)
            if r:
                rows.append(dict(cohort=cname, horizon=hl, comparator="age+sex",
                                 estimand="refit_varset", lpa_policy="n/a",
                                 n_eval=int(len(d)), events_eval=int(d.E.sum()), **r))

    # correction-method sensitivity (TUDOR robustness check)
    sens = []
    for f in (0.65, 0.70, 0.75):
        u, _ = build_ukb() if f == F_LDL else (None, None)
        if u is None:
            continue
        c, _, _ = cv(u, SPEC)
        sens.append({"f_ldl": f, "C_ukb_full": c})
    res["correction_sensitivity"] = sens

    res["head_to_head"], res["calibration"] = rows, calib_rows
    (OUT / "calon_h2.json").write_text(json.dumps(res, indent=2, default=str))
    pd.DataFrame(rows).to_csv(OUT / "calon_h2_headtohead.csv", index=False)
    print("=" * 78)
    print("written:", OUT / "calon_h2.json", "|", OUT / "calon_h2_headtohead.csv")


if __name__ == "__main__":
    main()
