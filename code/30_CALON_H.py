#!/usr/bin/env python3
"""CALON-H — treatment-free incident-ASCVD model, UK Biobank + All-Wales.

SPECIFICATION (frozen before fitting, investigator-directed 16 Aug 2026)

    age, sp50, male, htn, dm, smoke, cum_nonhdl, log_tghdl, remnant_chol

  * NO statin / treatment flag as a predictor  (investigator decision, 16 Aug 2026)
  * NO Lp(a), NO apoB                          (investigator decision — enables
                                                Welsh external validation, which
                                                Lp(a)/apoB make impossible)
  * NO published score or prior CALON model as an input  (binding programme rule)

  Treatment enters ONLY as the divide-by-0.70 back-correction producing untreated
  non-HDL-C, using DATED treatment fields in both cohorts. FH-Risk-Score does the
  same thing (its LDL is "untreated or imputed"), so this is symmetric with the
  comparators rather than an advantage.

COMPARATORS — transcribed from the source PDFs, not from memory.
  SAFEHEART-RE  Perez de Isla, Circulation 2017;135:2139-40
  FH-Risk-Score Paquette, ATVB 2021;41:2637-8 (Table 3 chart)
  Montreal      Paquette, J Clin Lipidol 2017;11:84 (Table 3)
  SAFEHEART is unit-tested against its own published worked examples. If that
  test fails, the script aborts before scoring anything.

HORIZON — corrected mask.  E_h = (E==1) & (T<=H) ; T_h = min(T,H).
  The withdrawn form (T<=H)|(E==1) returned 146 five-year events against 97.

Governance: aggregate output only. No participant rows, identifiers, family
identifiers or variant coordinates are written. Cells with <10 events suppressed.
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
REPEATS = 10
FOLDS = 10
BOOT = 2000
MIN_EVENTS = 10
STUDY_END = pd.Timestamp("2023-12-31")
PENALTY = 0.02

SPEC = ["age", "sp50", "male", "htn", "dm", "smoke",
        "cum_nonhdl", "log_tghdl", "remnant_chol"]

_s = importlib.util.spec_from_file_location(
    "vw", ROOT / "code" / "audit_2026_08_10" / "07_verify_welsh_prospective.py")
vw = importlib.util.module_from_spec(_s)
sys.modules["vw"] = vw
_s.loader.exec_module(vw)


# ---------------------------------------------------------------- data paths
def corrected_root() -> Path:
    marker = Path("data_corrected") / "corrected_ascvd_outcomes.csv"
    cands = []
    env = os.environ.get("CALON_CORRECTED_DATA")
    if env:
        cands.append(Path(env))
    cands += sorted(Path.home().glob(
        "Library/CloudStorage/GoogleDrive-*/My Drive/Projects/CALON_AlphaFold_Rebuild"))
    cands.append(Path("/Volumes/UnionSine/Projects/CALON_AlphaFold_Rebuild"))
    for c in cands:
        if (c / marker).exists():
            return c
    raise RuntimeError("corrected_ascvd_outcomes.csv not found; set CALON_CORRECTED_DATA")


def master_path() -> Path:
    env = os.environ.get("CALON_SHARED_MASTER")
    if env and (Path(env) / "UKB" / "ukb_master.csv").exists():
        return Path(env) / "UKB" / "ukb_master.csv"
    for c in sorted(Path.home().glob(
            "Library/CloudStorage/GoogleDrive-*/My Drive/Projects/SHARED_MASTER_DATA")):
        if (c / "UKB" / "ukb_master.csv").exists():
            return c / "UKB" / "ukb_master.csv"
    p = Path("/Users/nader85/Downloads/CALON_DATA_PACKAGE_2026-08-13/raw/all_inputs/ukb_master.csv")
    if p.exists():
        return p
    raise RuntimeError("ukb_master.csv not found; set CALON_SHARED_MASTER")


def wales_path() -> Path:
    for p in (vw.WALES,
              Path("/Users/nader85/Downloads/CALON_DATA_PACKAGE_2026-08-13/raw/all_inputs/WALES_FH_CLEANED.csv")):
        if Path(p).exists():
            return Path(p)
    raise RuntimeError("WALES_FH_CLEANED.csv not found")


# ------------------------------------------------------- comparator equations
# Transcribed from the source PDFs. Page/table pinpoints in the docstring above.

SAFEHEART_BETA = dict(male=0.70, age30_59=1.07, age60=1.45, highbp=0.69,
                      prior=1.42, smoke=0.48, overweight=0.88, obesity=0.98,
                      ldl100_159=0.92, ldl160=1.57, lpa50=0.42)
SAFEHEART_CENTRE = 5.4078
SAFEHEART_S0 = {5: 0.9532, 10: 0.9025}


def safeheart_lp(age, male, highbp, prior, smoke, bmi, ldl_mgdl, lpa_mgdl):
    """Linear predictor, published categorical form. Arrays in, array out."""
    age, bmi = np.asarray(age, float), np.asarray(bmi, float)
    ldl, lpa = np.asarray(ldl_mgdl, float), np.asarray(lpa_mgdl, float)
    b = SAFEHEART_BETA
    lp = (b["male"] * np.asarray(male, float)
          + b["age30_59"] * ((age >= 30) & (age < 60)).astype(float)
          + b["age60"] * (age >= 60).astype(float)
          + b["highbp"] * np.asarray(highbp, float)
          + b["prior"] * np.asarray(prior, float)
          + b["smoke"] * np.asarray(smoke, float)
          + b["overweight"] * ((bmi >= 25) & (bmi < 30)).astype(float)
          + b["obesity"] * (bmi >= 30).astype(float)
          + b["ldl100_159"] * ((ldl >= 100) & (ldl < 160)).astype(float)
          + b["ldl160"] * (ldl >= 160).astype(float)
          + b["lpa50"] * (lpa > 50).astype(float))
    return lp


def safeheart_risk(lp, horizon):
    return 1.0 - SAFEHEART_S0[horizon] ** np.exp(lp - SAFEHEART_CENTRE)


def _test_safeheart():
    """Published worked examples, Circulation 2017;135:2140. MUST pass."""
    # Case 1: 20 y woman, normal BP, no prior ASCVD, non-smoker, normal BMI,
    #         LDL-C 90 mg/dL, Lp(a) 33 mg/dL  ->  0.02% / 0.05%
    lp1 = safeheart_lp([20], [0], [0], [0], [0], [22.0], [90], [33])
    r5, r10 = safeheart_risk(lp1, 5)[0], safeheart_risk(lp1, 10)[0]
    assert abs(lp1[0] - 0.0) < 1e-12, f"case1 lp {lp1[0]}"
    assert abs(r5 - 0.0002148) < 5e-6, f"case1 5y {r5}"
    assert abs(r10 - 0.0004598) < 5e-6, f"case1 10y {r10}"
    # Case 2: 63 y man, hypertensive, previous MI, current smoker, obese,
    #         LDL-C 182 mg/dL, Lp(a) 64 mg/dL  ->  38.08% / 64.15%
    lp2 = safeheart_lp([63], [1], [1], [1], [1], [32.0], [182], [64])
    r5, r10 = safeheart_risk(lp2, 5)[0], safeheart_risk(lp2, 10)[0]
    assert abs(lp2[0] - 7.71) < 1e-12, f"case2 lp {lp2[0]}"
    assert abs(r5 - 0.3808) < 5e-4, f"case2 5y {r5}"
    assert abs(r10 - 0.6415) < 5e-4, f"case2 10y {r10}"
    return dict(case1_5y=float(safeheart_risk(lp1, 5)[0]),
                case1_10y=float(safeheart_risk(lp1, 10)[0]),
                case2_5y=float(safeheart_risk(lp2, 5)[0]),
                case2_10y=float(safeheart_risk(lp2, 10)[0]))


def _band(x, edges, points):
    """edges ascending upper bounds; points same length (last = above top edge)."""
    x = np.asarray(x, float)
    out = np.full(x.shape, np.nan)
    prev = -np.inf
    for e, p in zip(edges, points[:-1]):
        out = np.where((x > prev) & (x <= e), p, out)
        prev = e
    out = np.where(x > prev, points[-1], out)
    return out


def fhrs_points(age, male, hdl, ldl_unt, htn, smoke, lpa_hi):
    """ATVB 2021 Table 3 chart. Points; higher = higher risk."""
    p = (7.0 * np.asarray(male, float)
         + _band(age, [30, 35, 40, 45, 50, 55, 60], [0, 9, 14, 16, 17, 18, 20, 23])
         + _band(hdl, [0.84, 1.00, 1.30], [8, 7, 3, 0])
         + _band(ldl_unt, [5.50, 7.50, 8.50, 9.50], [0, 3, 7, 9, 11])
         + 6.0 * np.asarray(htn, float)
         + 6.0 * np.asarray(smoke, float)
         + 4.0 * np.asarray(lpa_hi, float))
    return p


def montreal_points(age, hdl, male, htn, smoke):
    """J Clin Lipidol 2017;11:84 Table 3. Integer points; ranking only."""
    return (_band(age, [21, 28, 35, 42, 49, 56, 63], [0, 4, 8, 12, 16, 20, 24, 28])
            + _band(hdl, [0.60, 0.90, 1.20, 1.50], [12, 9, 6, 3, 0])
            + 3.0 * np.asarray(male, float)
            + 2.0 * np.asarray(htn, float)
            + 1.0 * np.asarray(smoke, float))


# ------------------------------------------------------------------- cohorts
def build_ukb():
    use = ["eid", "ldlr_carrier", "date_baseline", "age_exact_baseline", "age_at_recruit",
           "sex_F", "tc_chem", "hdl_chem", "ldl_chem", "tg_chem", "diabetes_combined",
           "smoking_ever", "smoking_current", "sbp", "dbp", "on_statin_self",
           "bmi_direct", "lpa_chem", "death_date"]
    m = pd.read_csv(master_path(), usecols=use, low_memory=False)
    _root = corrected_root()
    c = pd.read_csv(_root / "data_corrected" / "corrected_ascvd_outcomes.csv",
                    usecols=["eid", "ascvd_first_date_best", "i21_event", "i25_event",
                             "i63_event", "i70_event", "i73_event", "g45_event"],
                    low_memory=False)
    _g = lambda k: pd.to_numeric(c[k], errors="coerce").fillna(0).gt(0)
    c["athero"] = (_g("i21_event") | _g("i25_event") | _g("i63_event")
                   | _g("i70_event") | _g("i73_event") | _g("g45_event"))
    md = pd.read_csv(_root / "New folder" / "04a_meds_touch.csv", low_memory=False)
    md.columns = [x.replace("participant.", "") for x in md.columns]
    has2 = lambda col: md[col].astype(str).str.contains(r"\b2\b", na=False)
    md["bpmed"] = (has2("p6153_i0") | has2("p6177_i0")).astype(float)
    md.loc[~md[["p6153_i0", "p6177_i0"]].notna().any(axis=1), "bpmed"] = np.nan

    d = m.merge(c, on="eid", how="left").merge(md[["eid", "bpmed"]], on="eid", how="left")
    n = lambda x: pd.to_numeric(d[x], errors="coerce")
    d = d.loc[n("ldlr_carrier").eq(1)].reset_index(drop=True)
    n = lambda x: pd.to_numeric(d[x], errors="coerce")
    ledger = {"carriers": int(len(d))}

    base = pd.to_datetime(d.date_baseline, errors="coerce")
    ev = pd.to_datetime(d.ascvd_first_date_best, errors="coerce")
    death = pd.to_datetime(d.death_date, errors="coerce")
    athero = d["athero"].fillna(False).astype(bool)
    prevalent = ev.notna() & base.notna() & ev.le(base) & athero
    incident = ev.notna() & base.notna() & ev.gt(base) & athero
    undated = athero & ev.isna()
    hf_only = ev.notna() & base.notna() & ev.gt(base) & ~athero
    ledger["prevalent_excluded"] = int(prevalent.sum())
    ledger["undated_excluded"] = int(undated.sum())
    end = ev.where(incident | hf_only, death.fillna(STUDY_END))

    x = pd.DataFrame(index=d.index)
    x["age"] = n("age_exact_baseline").fillna(n("age_at_recruit"))
    x["male"] = 1 - n("sex_F").fillna(0)
    tc, hdl, ldl, tg = n("tc_chem"), n("hdl_chem"), n("ldl_chem"), n("tg_chem")
    tx = n("on_statin_self").fillna(0).gt(0)          # DATED baseline field
    nonhdl = (tc - hdl).where(lambda z: z.between(0.3, 20))
    x["nonhdl_unt"] = np.where(tx, nonhdl / 0.70, nonhdl)
    x["ldl_unt"] = np.where(tx, ldl / 0.70, ldl)
    x["hdl"], x["bmi"], x["lpa"] = hdl, n("bmi_direct"), n("lpa_chem")
    x["remnant_chol"] = (tc - hdl - ldl).where(lambda z: z.between(-1, 6))
    x["log_tghdl"] = np.log((tg / hdl).where(lambda z: z.gt(0)))
    x["dm"] = n("diabetes_combined").gt(0).astype(float)
    x["smoke"] = n("smoking_current").fillna(n("smoking_ever")).gt(0).astype(float)
    x["htn"] = ((n("bpmed").fillna(0).gt(0)) | n("sbp").ge(140) | n("dbp").ge(90)).astype(float)
    x["prior"] = 0.0                                   # incident cohort by construction
    x["T"] = (end - base).dt.days / 365.25
    x["E"] = incident.astype(int)
    x["cluster"] = np.arange(len(x))
    x = _finish(x.loc[~(prevalent | undated)].reset_index(drop=True))
    ledger["risk_set"] = int(len(x))
    ledger["events_full"] = int(x.E.sum())
    ledger["events_5y"] = int(((x.E == 1) & (x["T"] <= 5)).sum())
    ledger["events_10y"] = int(((x.E == 1) & (x["T"] <= 10)).sum())
    return x, ledger


def build_wales():
    raw = pd.read_csv(wales_path(), low_memory=False)
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
    exit_age = ev_age.where(incident, n("AGE_AT_DECEASED").fillna(last))

    tc, hdl, tg, ldl = n("TC.1"), n("HDL.1"), n("TRG.1"), n("LDL.1")
    # DATED treatment only: treatment start on or before the visit-1 measurement.
    tx = (vw.date(raw, "Treatmentdate1").notna() & vw.date(raw, "MeasurementDate.1").notna()
          & vw.date(raw, "Treatmentdate1").le(vw.date(raw, "MeasurementDate.1"))).astype(float)
    nonhdl = (tc - hdl).where(lambda z: z.between(0.3, 20))

    x = pd.DataFrame(index=raw.index)
    x["age"] = bage
    x["male"] = raw["Gender"].astype(str).str[0].str.upper().eq("M").astype(float)
    x["nonhdl_unt"] = np.where(tx.gt(0), nonhdl / 0.70, nonhdl)
    x["ldl_unt"] = np.where(tx.gt(0), ldl / 0.70, ldl)
    x["hdl"] = hdl
    x["bmi"] = n("BMI")
    x["lpa"] = np.nan                                  # different assay/scale; excluded
    x["remnant_chol"] = (tc - hdl - ldl).where(lambda z: z.between(-1, 6))
    x["log_tghdl"] = np.log((tg / hdl).where(lambda z: z.gt(0)))
    sm, dm = n("Smoking"), n("Diabetes")
    x["smoke"] = sm.where(sm.isin([0, 1]))
    x["dm"] = dm.where(dm.isin([0, 1]))
    x["htn"] = ((n("BloodPressureMedication").eq(1))
                | n("BloodPressureSystolic").ge(140)
                | n("BloodPressureDiastolic").ge(90)).astype(float)
    x["prior"] = 0.0
    x["T"] = exit_age - bage
    x["E"] = incident.astype(int)
    x["cluster"] = raw["FamilyNumber"].astype(str)
    x["proband"] = (raw["Proband"].astype(str).str.upper().str[0].eq("Y").astype(float)
                    if "Proband" in raw else 0.0)
    x = _finish(x.loc[active].reset_index(drop=True))
    ledger = {"genotype_positive": int(active.sum()), "risk_set": int(len(x)),
              "events_full": int(x.E.sum()),
              "events_5y": int(((x.E == 1) & (x["T"] <= 5)).sum()),
              "events_10y": int(((x.E == 1) & (x["T"] <= 10)).sum())}
    return x, ledger


def _finish(x):
    x["sp50"] = (x.age - 50).clip(lower=0)
    x["cum_nonhdl"] = np.log((pd.Series(x.nonhdl_unt, index=x.index) * x.age)
                             .where(lambda z: z.gt(0)))
    x = x.replace([np.inf, -np.inf], np.nan)
    return x.loc[x["T"].gt(0)].reset_index(drop=True)


# --------------------------------------------------------- horizon + scoring
def horizon(df, H):
    """CORRECT fixed-horizon construction. Withdrawn form was (T<=H)|(E==1)."""
    d = df.copy()
    d["E"] = ((df.E == 1) & (df["T"] <= H)).astype(int)
    d["T"] = df["T"].clip(upper=H)
    return d.loc[d["T"].gt(0)].reset_index(drop=True)


def comparators(d, lpa_units="nmol"):
    """Published equations, scored not fitted. Never model inputs."""
    ldl_mgdl = d.ldl_unt * 38.67
    if lpa_units == "nmol":
        lpa_mgdl = d.lpa / 2.15
    else:
        lpa_mgdl = d.lpa
    lpa_mgdl = pd.Series(lpa_mgdl, index=d.index)
    bmi = d.bmi
    out = {}
    out["SAFEHEART-RE"] = safeheart_lp(d.age, d.male, d.htn, d.prior, d.smoke,
                                       bmi, ldl_mgdl, lpa_mgdl.fillna(0))
    out["FH-Risk-Score"] = fhrs_points(d.age, d.male, d.hdl, d.ldl_unt, d.htn,
                                       d.smoke, (lpa_mgdl.fillna(0) >= 50).astype(float))
    out["Montreal-FH-SCORE"] = montreal_points(d.age, d.hdl, d.male, d.htn, d.smoke)
    return {k: np.asarray(v, float) for k, v in out.items()}


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
            ev = df.loc[v.notna(), "E"]
            if min(ev[v[v.notna()] == 0].sum(), ev[v[v.notna()] == 1].sum()) < MIN_EVENTS:
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
    cph = CoxPHFitter(penalizer=PENALTY)
    cph.fit(m, "T", "E")
    return cph


def _predict(cph, te, feats, med):
    m = te[feats].copy()
    for f in feats:
        m[f] = pd.to_numeric(m[f], errors="coerce").fillna(med[f])
    return np.asarray(cph.predict_partial_hazard(m), float)


def cv(df, feats, repeats=REPEATS, seed=SEED):
    """Out-of-fold LP, family-clustered, genuinely re-randomised per repeat."""
    feats = usable(df, feats)
    if not feats:
        return np.nan, np.zeros(len(df)), feats, 0
    clusters = pd.Series(df["cluster"].astype(str)).values
    uniq = np.unique(clusters)
    acc, cnt, fails = np.zeros(len(df)), 0, 0
    for rep in range(repeats):
        rng = np.random.default_rng(seed + rep)
        perm = rng.permutation(len(uniq))
        assign = dict(zip(uniq, perm % FOLDS))
        fold = np.array([assign[c] for c in clusters])
        lp = np.full(len(df), np.nan)
        for k in range(FOLDS):
            tr, te = df.loc[fold != k], df.loc[fold == k]
            if tr.E.sum() < MIN_EVENTS or len(te) == 0:
                continue
            try:
                cph = _fit(tr, feats)
            except Exception:
                fails += 1
                continue
            med = {f: pd.to_numeric(tr[f], errors="coerce").median() for f in feats}
            lp[fold == k] = np.log(_predict(cph, te, feats, med))
        if np.isfinite(lp).all():
            acc += lp
            cnt += 1
    if cnt == 0:
        return np.nan, np.zeros(len(df)), feats, fails
    lp = acc / cnt
    c = concordance_index(df["T"], -lp, df["E"])
    return float(c), lp, feats, fails


def delta_ci(df, lp_a, lp_b, B=BOOT, seed=SEED):
    """Paired cluster bootstrap of C(a) - C(b). Also returns measured rho."""
    ok = np.isfinite(lp_a) & np.isfinite(lp_b)
    d = df.loc[ok].reset_index(drop=True)
    a, b = lp_a[ok], lp_b[ok]
    if d.E.sum() < MIN_EVENTS:
        return None
    obs = concordance_index(d["T"], -a, d["E"]) - concordance_index(d["T"], -b, d["E"])
    rho = float(pd.Series(a).corr(pd.Series(b), method="spearman"))
    groups = d.groupby(d["cluster"].astype(str)).indices
    keys = list(groups.keys())
    rng = np.random.default_rng(seed)
    draws, eff = [], 0
    for _ in range(B):
        pick = rng.choice(len(keys), len(keys), replace=True)
        idx = np.concatenate([groups[keys[i]] for i in pick])
        sub = d.iloc[idx]
        if sub.E.sum() < MIN_EVENTS:
            continue
        try:
            draws.append(concordance_index(sub["T"], -a[idx], sub["E"])
                         - concordance_index(sub["T"], -b[idx], sub["E"]))
            eff += 1
        except Exception:
            continue
    if eff < 100:
        return None
    lo, hi = np.percentile(draws, [2.5, 97.5])
    # Measured-rho detection floor (audit D10): MDD at the observed correlation.
    se = float(np.std(draws, ddof=1))
    floor = 1.96 * se
    return dict(delta=float(obs), lo=float(lo), hi=float(hi), B_eff=eff,
                rho=rho, floor=float(floor),
                verdict="WIN" if lo > 0 else ("LOSS" if hi < 0 else "TIE"))


def calib(df, lp, horizon_years):
    """E:O and calibration slope at a fixed horizon, Breslow baseline."""
    d = horizon(df, horizon_years)
    m = pd.DataFrame({"lp": lp[:len(d)] if len(lp) >= len(d) else np.pad(
        lp, (0, len(d) - len(lp)), constant_values=np.nan),
        "T": d["T"], "E": d["E"]}).dropna()
    if m.E.sum() < MIN_EVENTS:
        return None
    cph = CoxPHFitter(penalizer=0.0)
    try:
        cph.fit(m[["lp", "T", "E"]], "T", "E")
        slope = float(cph.params_["lp"])
        se = float(cph.standard_errors_["lp"])
    except Exception:
        return None
    obs = float(m.E.mean())
    return dict(slope=slope, slope_lo=slope - 1.96 * se, slope_hi=slope + 1.96 * se,
                observed=obs, n=int(len(m)), events=int(m.E.sum()))


# ---------------------------------------------------------------------- main
def main():
    res = {"spec": SPEC, "seed": SEED, "boot": BOOT, "repeats": REPEATS,
           "penalty": PENALTY,
           "excluded_by_decision": ["statin/treatment flag as predictor",
                                    "Lp(a) as model input", "apoB as model input",
                                    "any published score or prior CALON LP"]}

    print("=" * 74)
    print("UNIT TEST — SAFEHEART published worked examples")
    res["safeheart_unit_test"] = _test_safeheart()
    for k, v in res["safeheart_unit_test"].items():
        print(f"  {k:12s} {v:.6f}")
    print("  PASS — equation reproduces Circulation 2017;135:2140 to 4 dp")

    print("=" * 74)
    print("COHORTS")
    ukb, ledg_u = build_ukb()
    wal, ledg_w = build_wales()
    res["ledger_ukb"], res["ledger_wales"] = ledg_u, ledg_w
    print("  UKB   ", json.dumps(ledg_u))
    print("  Wales ", json.dumps(ledg_w))

    # ---- gates
    gates = {
        "ukb_carriers_3540": ledg_u["carriers"] == 3540,
        "ukb_prevalent_207": ledg_u["prevalent_excluded"] == 207,
        "ukb_undated_124": ledg_u["undated_excluded"] == 124,
        "ukb_riskset_3209": ledg_u["risk_set"] == 3209,
        "ukb_events_289": ledg_u["events_full"] == 289,
        "ukb_events5y_97": ledg_u["events_5y"] == 97,
        "ukb_events10y_194": ledg_u["events_10y"] == 194,
    }
    res["gates"] = gates
    print("  GATES ", json.dumps(gates))

    # ---- G1 census (Welsh complete lipids at the dated visit)
    need = ["remnant_chol", "log_tghdl", "cum_nonhdl"]
    cc = wal[need].notna().all(axis=1)
    res["G1_wales_census"] = {"complete_case_n": int(cc.sum()),
                              "complete_case_events": int(wal.loc[cc, "E"].sum()),
                              "of_n": int(len(wal)), "of_events": int(wal.E.sum())}
    print("  G1 census", json.dumps(res["G1_wales_census"]))

    out_rows = []
    for name, df in (("UK Biobank", ukb), ("Wales", wal)):
        for H, label in ((None, "full"), (10, "10y"), (5, "5y")):
            d = df if H is None else horizon(df, H)
            if d.E.sum() < MIN_EVENTS:
                continue
            c_m, lp_m, feats, fails = cv(d, SPEC)
            comps = comparators(d)
            row_base = dict(cohort=name, horizon=label, n=int(len(d)),
                            events=int(d.E.sum()), C_model=c_m,
                            terms=feats, cox_failures=fails)
            for cname, cscore in comps.items():
                ok = np.isfinite(cscore)
                if ok.sum() < 50:
                    continue
                sub = d.loc[ok].reset_index(drop=True)
                r = delta_ci(sub, lp_m[ok], cscore[ok])
                if r is None:
                    continue
                out_rows.append({**row_base, "comparator": cname,
                                 "n_eval": int(ok.sum()),
                                 "events_eval": int(sub.E.sum()),
                                 "C_comparator": float(concordance_index(
                                     sub["T"], -cscore[ok], sub["E"])),
                                 **r})
            # age+sex reference
            c_as, lp_as, _, _ = cv(d, ["age", "male"])
            r = delta_ci(d, lp_m, lp_as)
            if r is not None:
                out_rows.append({**row_base, "comparator": "age+sex",
                                 "n_eval": int(len(d)), "events_eval": int(d.E.sum()),
                                 "C_comparator": c_as, **r})
            print(f"  {name:11s} {label:5s} n={len(d):5d} ev={int(d.E.sum()):4d} "
                  f"C_model={c_m:.4f} terms={len(feats)}")

    res["head_to_head"] = out_rows

    # ---- external transport: fit UKB, score Wales, and the reverse
    def transport(dev, val, dev_name, val_name):
        feats = usable(dev, SPEC)
        feats = [f for f in feats if f in val.columns]
        cph = _fit(dev, feats)
        med = {f: pd.to_numeric(dev[f], errors="coerce").median() for f in feats}
        lp = np.log(_predict(cph, val, feats, med))
        c = concordance_index(val["T"], -lp, val["E"])
        return dict(dev=dev_name, val=val_name, terms=feats,
                    C_external=float(c), n=int(len(val)), events=int(val.E.sum()))

    res["transport"] = [transport(ukb, wal, "UK Biobank", "Wales"),
                        transport(wal, ukb, "Wales", "UK Biobank")]
    for t in res["transport"]:
        print(f"  transport {t['dev']:11s} -> {t['val']:11s} C={t['C_external']:.4f} "
              f"(n={t['n']}, ev={t['events']})")

    (OUT / "calon_h.json").write_text(json.dumps(res, indent=2, default=str))
    pd.DataFrame(out_rows).to_csv(OUT / "calon_h_headtohead.csv", index=False)
    print("=" * 74)
    print(f"written: {OUT/'calon_h.json'}")
    print(f"written: {OUT/'calon_h_headtohead.csv'}")


if __name__ == "__main__":
    main()
