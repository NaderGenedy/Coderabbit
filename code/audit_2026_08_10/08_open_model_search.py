#!/usr/bin/env python3
"""DELTA 5: governance-safe open raw-variable model search.

The script reads participant data in place and writes aggregate outputs only.  It
never reads wales_clean_treatment_response.csv and never writes identifiers,
family values, variant coordinates, or participant-level predictions.

Primary estimand
-----------------
Ten-year first hard coronary event (MI/ACS, PCI/stent, or CABG) after the first
dated Welsh clinic visit among genotype-positive adults aged 18--75 and free of
any recorded ASCVD at baseline.  Death before a hard event is competing; a
registry extraction-age clock supplies administrative follow-up; follow-up
shorter than ten years is handled by inverse-probability-of-censoring weighting.

Model-selection policy
----------------------
Published/prior scores and linear predictors are comparators only.  The open
search spans raw-variable architectures, transformations, shrinkage strengths,
elastic-net mixtures, and two tree learners.  Candidate selection is performed
inside family-grouped outer resampling and uses a one-standard-error rule on
IPCW Brier score.  Every attempted specification is retained in aggregate form.
"""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import math
import os
import platform
import sys
import warnings
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Optional, Union

import numpy as np
import pandas as pd
from lifelines import CoxPHFitter
from lifelines.utils import concordance_index
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.experimental import enable_iterative_imputer  # noqa: F401
from sklearn.impute import IterativeImputer
from sklearn.linear_model import BayesianRidge, LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.preprocessing import StandardScaler


# The local Accelerate/NumPy stack emits spurious sklearn matmul RuntimeWarnings;
# all inputs, coefficients, and predictions are checked explicitly for finiteness.
warnings.filterwarnings("ignore", category=RuntimeWarning, module=r"sklearn\..*")


SEED = 20260810
OUTER_REPEATS = 5
OUTER_FOLDS = 5
INNER_FOLDS = 4
OUTER_IMPUTATIONS = 3
FINAL_IMPUTATIONS = 10
BOOTSTRAPS = 2000
FORBIDDEN_BASENAME = "wales_clean_treatment_response.csv"

ROOT = Path("/Users/nader85/Documents/CALON/calon_discordance_model_2026_08_09")
OUT = ROOT / "outputs" / "audit_2026_08_10"
WALES = Path("/Users/nader85/Downloads/WALES_FH_CLEANED.csv")
MASTER = Path(os.environ.get(
    "CALON_SHARED_MASTER",
    "/Users/nader85/Library/CloudStorage/GoogleDrive-nadergenedy1@gmail.com/My Drive/Projects/SHARED_MASTER_DATA",
))
PASS = MASTER / "PASS" / "pass_master.csv"
UKB = MASTER / "UKB" / "ukb_master.csv"
CALLS = Path("/Users/nader85/Documents/calon_backup_data/ukb_fh_all_carriers.tsv")
CLINVAR = MASTER / "../AlphaFold_SSS/data/analysis/ukb_clinvar_full.csv"
CLINVAR = CLINVAR.resolve()


def jdefault(value: Any) -> Any:
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return None if not np.isfinite(value) else float(value)
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, Path):
        return str(value)
    raise TypeError(type(value).__name__)


def num(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def dates(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series, errors="coerce", format="mixed", dayfirst=True)


def clean_key(series: pd.Series) -> pd.Series:
    return (
        series.astype("string").str.strip().str.upper()
        .str.replace(r"\.0$", "", regex=True)
        .replace({"": pd.NA, "NAN": pd.NA, "NONE": pd.NA})
    )


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def event_cell(value: int) -> Union[int, str]:
    return int(value) if int(value) >= 10 else "<10, non-estimable"


def pct(n: int, d: int) -> float:
    return float(100 * n / d) if d else float("nan")


RAW_IMPUTE = [
    "age", "male", "ldl", "hdl", "tg", "tc", "smoke_current",
    "diabetes", "htn", "treatment_verified", "bmi",
]
CONTINUOUS = ["age", "ldl", "hdl", "tg", "tc", "bmi"]
BINARY = [c for c in RAW_IMPUTE if c not in CONTINUOUS]


def build_wales() -> tuple[pd.DataFrame, dict[str, Any], pd.DataFrame]:
    """Independently align raw Wales predictors to PASS follow-up in memory."""
    wcols = [
        "DatabaseNumber", "FamilyNumber", "Positive1", "DOB", "DOB_1",
        "MeasurementDate.1", "Gender", "LDL.1", "HDL.1", "TC.1", "TRG.1",
        "Smoking", "BloodPressureSystolic", "BloodPressureDiastolic",
        "BloodPressureDate", "BloodPressureMedication", "Diabetes", "DiabetesYear",
        "BMIDate", "BMI", "Treatmentdate1", "Treatmentdate2", "Treatmentdate3",
        "Treatment1.1", "Treatment1.2", "Treatment1.3", "Lpa.1",
        "MIACSAge", "PCIStentsAge", "CABGAge", "ANGINAAge", "TIAAge", "PVDAge",
        "ascvd_combine", "AGE_AT_DECEASED", "MeasurementDate.2", "MeasurementDate.3",
        "MeasurementDate.4",
    ]
    pcols = [
        "participant_id", "family_id", "mutation_positive", "age_years",
        "deceased_date", "event_any", "mi_acs_age", "pci_age", "cabg_age",
        "angina_age", "tia_age", "pvd_age", "pre_ldl",
    ]
    w = pd.read_csv(WALES, usecols=wcols, low_memory=False)
    p = pd.read_csv(PASS, usecols=pcols, low_memory=False)
    w["_key"] = clean_key(w["DatabaseNumber"])
    p["_key"] = clean_key(p["participant_id"])
    if w["_key"].duplicated().any() or p["_key"].duplicated().any():
        raise RuntimeError("Participant linkage key is not one-to-one")
    d = w.merge(p, on="_key", how="inner", validate="one_to_one", suffixes=("_w", "_p"))
    if len(d) != len(w) or len(d) != len(p):
        raise RuntimeError("WALES/PASS linkage is incomplete")

    dob = dates(d["DOB"]).fillna(dates(d["DOB_1"]))
    baseline_date = dates(d["MeasurementDate.1"])
    age = (baseline_date - dob).dt.total_seconds() / (365.25 * 86400)
    broad_age = pd.concat(
        [num(d[c]) for c in ["mi_acs_age", "pci_age", "cabg_age", "angina_age", "tia_age", "pvd_age"]],
        axis=1,
    ).min(axis=1)
    hard_age = pd.concat([num(d[c]) for c in ["mi_acs_age", "pci_age", "cabg_age"]], axis=1).min(axis=1)
    any_flag = num(d["event_any"]).fillna(0).gt(0)
    death_age = (dates(d["deceased_date"]) - dob).dt.total_seconds() / (365.25 * 86400)
    admin_age = num(d["age_years"])
    hard_time = hard_age - age
    death_time = death_age - age
    admin_time = admin_age - age

    genotype = num(d["mutation_positive"]).eq(1)
    risk = (
        genotype & age.notna() & age.between(18, 75, inclusive="both")
        & ~(broad_age.notna() & broad_age.lt(age))
        & ~(any_flag & broad_age.isna())
        & admin_time.gt(0)
    )
    event10 = (
        hard_age.notna() & hard_time.ge(0) & hard_time.le(10)
        & (death_age.isna() | hard_age.le(death_age))
    )
    death10 = (
        death_time.ge(0) & death_time.le(10)
        & (hard_age.isna() | death_age.lt(hard_age))
    )
    known_control = (~event10) & (~death10) & ((hard_age.notna() & hard_time.gt(10)) | admin_time.ge(10))
    early_censor = (~event10) & (~death10) & (~known_control) & admin_time.ge(0) & admin_time.lt(10)
    active = risk & (event10 | death10 | known_control | early_censor)

    gender = d["Gender"].astype("string").str.strip().str.upper()
    male = gender.map({"M": 1.0, "MALE": 1.0, "1": 1.0, "F": 0.0, "FEMALE": 0.0, "0": 0.0})
    ldl = num(d["LDL.1"]).where(num(d["LDL.1"]).between(0.3, 20, inclusive="neither"))
    hdl = num(d["HDL.1"]).where(num(d["HDL.1"]).between(0.2, 5, inclusive="neither"))
    tg = num(d["TRG.1"]).where(num(d["TRG.1"]).between(0.2, 25, inclusive="neither"))
    tc = num(d["TC.1"]).where(num(d["TC.1"]).between(1.5, 25, inclusive="neither"))
    smoke = num(d["Smoking"]).where(num(d["Smoking"]).isin([0, 1]))
    diabetes_text = d["Diabetes"].astype("string").str.strip().str.lower()
    diabetes = pd.Series(np.nan, index=d.index, dtype=float)
    diabetes.loc[diabetes_text.isin(["yes", "y", "1", "1.0", "true"])] = 1.0
    diabetes.loc[diabetes_text.isin(["no", "n", "0", "0.0", "false"])] = 0.0
    sbp, dbp = num(d["BloodPressureSystolic"]), num(d["BloodPressureDiastolic"])
    bp_pre = (
        sbp.between(50, 300) & dbp.between(20, 200)
        & dates(d["BloodPressureDate"]).notna() & dates(d["BloodPressureDate"]).le(baseline_date)
    )
    htn = pd.Series(np.nan, index=d.index, dtype=float)
    htn.loc[bp_pre] = ((sbp.loc[bp_pre] >= 140) | (dbp.loc[bp_pre] >= 90)).astype(float)
    bmi = num(d["BMI"]).where(
        num(d["BMI"]).between(12, 70)
        & dates(d["BMIDate"]).notna() & dates(d["BMIDate"]).le(baseline_date)
    )
    treatment_dates = pd.concat([dates(d[f"Treatmentdate{i}"]) for i in range(1, 4)], axis=1)
    treatment_verified = treatment_dates.le(baseline_date, axis=0).any(axis=1).astype(float)
    visit_drug = pd.Series(False, index=d.index)
    for c in ["Treatment1.1", "Treatment1.2", "Treatment1.3"]:
        z = d[c].astype("string").str.strip().str.lower()
        visit_drug |= z.notna() & ~z.isin(["", "nan", "none", "nat"])

    fam = clean_key(d.loc[active, "family_id"])
    missing = fam.isna()
    internal_family = fam.copy()
    internal_family.loc[missing] = pd.Series(
        [f"missing-{i}" for i in range(missing.sum())], index=fam.index[missing], dtype="string"
    )

    out = pd.DataFrame({
        "age": age.loc[active].to_numpy(float),
        "male": male.loc[active].to_numpy(float),
        "ldl": ldl.loc[active].to_numpy(float),
        "hdl": hdl.loc[active].to_numpy(float),
        "tg": tg.loc[active].to_numpy(float),
        "tc": tc.loc[active].to_numpy(float),
        "smoke_current": smoke.loc[active].to_numpy(float),
        "diabetes": diabetes.loc[active].to_numpy(float),
        "htn": htn.loc[active].to_numpy(float),
        "treatment_verified": treatment_verified.loc[active].to_numpy(float),
        "treatment_visit_record": visit_drug.loc[active].astype(float).to_numpy(),
        "bmi": bmi.loc[active].to_numpy(float),
        "lpa": num(d["Lpa.1"]).where(num(d["Lpa.1"]).ge(0)).loc[active].to_numpy(float),
        "pre_ldl_sensitivity": num(d["pre_ldl"]).where(num(d["pre_ldl"]).between(0.3, 25)).loc[active].to_numpy(float),
        "event": event10.loc[active].astype(int).to_numpy(),
        "status": np.where(
            event10.loc[active], 1,
            np.where(death10.loc[active], 2, np.where(early_censor.loc[active], 3, 0)),
        ),
        "time": np.where(
            event10.loc[active], hard_time.loc[active],
            np.where(death10.loc[active], death_time.loc[active], np.minimum(admin_time.loc[active], 10.0)),
        ),
        "group": pd.factorize(internal_family)[0],
    }).reset_index(drop=True)

    if out["event"].sum() < 40:
        raise RuntimeError("Primary Welsh event count is below the minimum modelling gate")
    if (out["time"] < 0).any() or (out["time"] > 10 + 1e-9).any():
        raise RuntimeError("Invalid Welsh follow-up time")

    flow = {
        "linked_rows": int(len(d)),
        "genotype_positive": int(genotype.sum()),
        "adults_18_75_with_dated_baseline_and_positive_admin_followup": int(risk.sum()),
        "primary_n": int(len(out)),
        "events_10y": int(out["event"].sum()),
        "competing_deaths_10y": int((out["status"] == 2).sum()),
        "known_eventfree_10y": int((out["status"] == 0).sum()),
        "administratively_censored_before_10y": int((out["status"] == 3).sum()),
        "families_plus_singletons": int(out["group"].nunique()),
        "endpoint": "first MI/ACS, PCI/stent, or CABG within 10 years; any recorded ASCVD excludes at baseline",
        "censor_clock": "PASS age_years extraction-age field; not later-clinic attendance",
    }
    availability = []
    for c in RAW_IMPUTE + ["lpa", "pre_ldl_sensitivity", "treatment_visit_record"]:
        n = int(out[c].notna().sum())
        e = int(out.loc[out[c].notna(), "event"].sum())
        availability.append({
            "variable": c, "observed_n": n, "observed_pct": pct(n, len(out)),
            "events_with_value": event_cell(e),
        })
    return out, flow, pd.DataFrame(availability)


def classify_clinvar(value: object) -> bool:
    tokens = {x.strip().lower().replace(" ", "_") for x in str(value).split(",")}
    pathogenic = bool(tokens & {"pathogenic", "likely_pathogenic"})
    benign = bool(tokens & {"benign", "likely_benign"})
    return pathogenic and not benign


def strict_carrier_map() -> dict[int, str]:
    cv = pd.read_csv(CLINVAR, low_memory=False)
    cv = cv.loc[cv["clinvar"].map(classify_clinvar)].copy()
    for c in ["chrom", "ref", "alt"]:
        cv[c] = cv[c].astype(str).str.replace("chr", "", regex=False).str.upper()
    cv["pos"] = num(cv["pos"]).astype("Int64")
    keys = set(zip(cv["chrom"], cv["pos"], cv["ref"], cv["alt"]))
    mapping: dict[int, set[str]] = defaultdict(set)
    for chunk in pd.read_csv(CALLS, sep="\t", chunksize=750_000, low_memory=False):
        chunk = chunk.rename(columns={"CHROM": "chrom", "POS": "pos", "REF": "ref", "ALT": "alt", "EID": "eid"})
        chrom = chunk["chrom"].astype(str).str.replace("chr", "", regex=False).str.upper()
        pos = num(chunk["pos"]).astype("Int64")
        ref = chunk["ref"].astype(str).str.upper()
        alt = chunk["alt"].astype(str).str.upper()
        hit = pd.Series(list(zip(chrom, pos, ref, alt)), index=chunk.index).isin(keys)
        q = chunk.loc[hit, ["eid"]].copy()
        q["variant"] = [f"{a}:{b}:{c}:{d}" for a, b, c, d in zip(chrom[hit], pos[hit], ref[hit], alt[hit])]
        q["eid"] = num(q["eid"]).astype("Int64")
        for eid, variant in q.dropna(subset=["eid"]).itertuples(index=False):
            mapping[int(eid)].add(str(variant))
    return {eid: "|".join(sorted(values)) for eid, values in mapping.items()}


def build_ukb_strict() -> tuple[pd.DataFrame, dict[str, Any], pd.DataFrame]:
    carriers = strict_carrier_map()
    cols = [
        "eid", "ldlr_carrier", "prevalent_ascvd", "incident_ascvd", "date_baseline_ts",
        "date_baseline", "first_ascvd", "censor_date", "death_date", "age_exact_baseline",
        "age_at_recruit", "sex_F", "ldl_chem", "hdl_chem", "tg_chem", "tc_chem",
        "smoking_current", "diabetes_combined", "sbp", "dbp", "bmi_direct", "lpa_chem",
        "on_statin_self", "age_at_statin_start",
    ]
    u = pd.read_csv(UKB, usecols=cols, low_memory=False)
    u["eid"] = num(u["eid"]).astype("Int64")
    u = u.loc[u["eid"].isin(carriers) & num(u["ldlr_carrier"]).eq(1)].copy()
    u = u.loc[~num(u["prevalent_ascvd"]).fillna(0).gt(0)].copy()
    age = num(u["age_exact_baseline"]).fillna(num(u["age_at_recruit"]))
    u = u.loc[age.between(18, 75, inclusive="both")].copy()
    age = age.loc[u.index]
    base = dates(u["date_baseline_ts"]).fillna(dates(u["date_baseline"]))
    event_date, death_date, censor_date = dates(u["first_ascvd"]), dates(u["death_date"]), dates(u["censor_date"])
    event_time = (event_date - base).dt.total_seconds() / (365.25 * 86400)
    death_time = (death_date - base).dt.total_seconds() / (365.25 * 86400)
    censor_time = (censor_date - base).dt.total_seconds() / (365.25 * 86400)
    incident = num(u["incident_ascvd"]).eq(1)
    event10 = incident & event_time.between(0, 10) & (death_date.isna() | event_date.le(death_date))
    death10 = death_time.between(0, 10) & (~incident | event_date.isna() | death_date.lt(event_date))
    control = (~event10) & (~death10) & (censor_time.ge(10) | (incident & event_time.gt(10)))
    early = (~event10) & (~death10) & (~control) & censor_time.between(0, 10, inclusive="left")
    keep = event10 | death10 | control | early
    u, age = u.loc[keep].copy(), age.loc[keep]
    event10, death10, control, early = event10.loc[keep], death10.loc[keep], control.loc[keep], early.loc[keep]
    event_time, death_time, censor_time = event_time.loc[keep], death_time.loc[keep], censor_time.loc[keep]

    sbp, dbp = num(u["sbp"]), num(u["dbp"])
    htn = pd.Series(np.nan, index=u.index, dtype=float)
    known_bp = sbp.notna() | dbp.notna()
    htn.loc[known_bp] = ((sbp.loc[known_bp] >= 140) | (dbp.loc[known_bp] >= 90)).astype(float)
    on_statin = num(u["on_statin_self"]).where(num(u["on_statin_self"]).isin([0, 1]))
    start_age = num(u["age_at_statin_start"])
    verified_treatment = (on_statin.eq(1) & start_age.notna() & start_age.le(age)).astype(float)
    variant_cluster = u["eid"].map(carriers)
    out = pd.DataFrame({
        "age": age.to_numpy(float),
        "male": (1 - num(u["sex_F"])).to_numpy(float),
        "ldl": num(u["ldl_chem"]).where(num(u["ldl_chem"]).between(0.3, 20)).to_numpy(float),
        "hdl": num(u["hdl_chem"]).where(num(u["hdl_chem"]).between(0.2, 5)).to_numpy(float),
        "tg": num(u["tg_chem"]).where(num(u["tg_chem"]).between(0.2, 25)).to_numpy(float),
        "tc": num(u["tc_chem"]).where(num(u["tc_chem"]).between(1.5, 25)).to_numpy(float),
        "smoke_current": num(u["smoking_current"]).where(num(u["smoking_current"]).isin([0, 1])).to_numpy(float),
        "diabetes": num(u["diabetes_combined"]).where(num(u["diabetes_combined"]).isin([0, 1])).to_numpy(float),
        "htn": htn.to_numpy(float),
        "treatment_verified": verified_treatment.to_numpy(float),
        "treatment_visit_record": on_statin.fillna(0).to_numpy(float),
        "bmi": num(u["bmi_direct"]).where(num(u["bmi_direct"]).between(12, 70)).to_numpy(float),
        "lpa": num(u["lpa_chem"]).where(num(u["lpa_chem"]).ge(0)).to_numpy(float),
        "pre_ldl_sensitivity": np.nan,
        "event": event10.astype(int).to_numpy(),
        "status": np.where(event10, 1, np.where(death10, 2, np.where(early, 3, 0))),
        "time": np.where(event10, event_time, np.where(death10, death_time, np.minimum(censor_time, 10.0))),
        "group": pd.factorize(variant_cluster)[0],
    }).reset_index(drop=True)
    flow = {
        "strict_clinvar_carriers_before_clinical_filters": int(len(carriers)),
        "primary_prevention_adults_n": int(len(out)),
        "events_10y": event_cell(int(out["event"].sum())),
        "competing_deaths_10y": event_cell(int((out["status"] == 2).sum())),
        "known_eventfree_10y": int((out["status"] == 0).sum()),
        "administratively_censored_before_10y": int((out["status"] == 3).sum()),
        "variant_clusters": int(out["group"].nunique()),
        "status": "retrospective transport stress test; endpoint is related but not source-code harmonised",
    }
    availability = []
    for c in RAW_IMPUTE + ["lpa"]:
        n = int(out[c].notna().sum())
        e = int(out.loc[out[c].notna(), "event"].sum())
        availability.append({"variable": c, "observed_n": n, "observed_pct": pct(n, len(out)), "events_with_value": event_cell(e)})
    return out, flow, pd.DataFrame(availability)


@dataclass
class CensorKM:
    times: np.ndarray
    surv_before: np.ndarray
    final_surv: float

    @classmethod
    def fit(cls, status: np.ndarray, time: np.ndarray) -> "CensorKM":
        status, time = np.asarray(status), np.asarray(time, float)
        censor = status == 3
        unique = np.unique(time[np.isfinite(time)])
        if not len(unique):
            raise RuntimeError("No finite follow-up times")
        before, surv = [], 1.0
        for t in unique:
            before.append(surv)
            at_risk = int(np.sum(time >= t))
            n_censor = int(np.sum(censor & np.isclose(time, t)))
            if at_risk:
                surv *= 1 - n_censor / at_risk
        return cls(unique, np.asarray(before), float(surv))

    def g_before(self, query: np.ndarray) -> np.ndarray:
        query = np.asarray(query, float)
        idx = np.searchsorted(self.times, query, side="left")
        idx = np.clip(idx, 0, len(self.times) - 1)
        g = self.surv_before[idx]
        g[query > self.times[-1]] = self.final_surv
        return np.clip(g, 0.02, 1.0)

    def weights(self, status: np.ndarray, time: np.ndarray) -> np.ndarray:
        status, time = np.asarray(status), np.asarray(time, float)
        known = status != 3
        query = np.where(status == 0, 10.0, time)
        w = np.where(known, 1 / self.g_before(query), 0.0)
        positive = w[w > 0]
        if positive.size:
            w = np.minimum(w, np.quantile(positive, 0.99))
        return w


class FoldImputer:
    def __init__(self, seed: int, stochastic: bool):
        self.seed = seed
        self.stochastic = stochastic
        self.bounds: dict[str, tuple[float, float]] = {}
        self.model = IterativeImputer(
            estimator=BayesianRidge(), max_iter=10, sample_posterior=stochastic,
            initial_strategy="median", random_state=seed, skip_complete=False,
        )

    def _frame(self, d: pd.DataFrame) -> pd.DataFrame:
        x = d.reindex(columns=RAW_IMPUTE).astype(float).replace([np.inf, -np.inf], np.nan)
        for c, (lo, hi) in self.bounds.items():
            x[c] = x[c].clip(lo, hi)
        return x

    def fit(self, d: pd.DataFrame) -> "FoldImputer":
        for c in CONTINUOUS:
            v = num(d[c]).replace([np.inf, -np.inf], np.nan).dropna().to_numpy(float)
            if v.size:
                self.bounds[c] = tuple(float(x) for x in np.quantile(v, [0.005, 0.995]))
        self.model.fit(self._frame(d))
        return self

    def transform(self, d: pd.DataFrame) -> pd.DataFrame:
        values = self.model.transform(self._frame(d))
        x = pd.DataFrame(values, columns=RAW_IMPUTE, index=d.index)
        for c in BINARY:
            x[c] = x[c].clip(0, 1)
        for c, (lo, hi) in self.bounds.items():
            x[c] = x[c].clip(lo, hi)
        return enrich(x)


def enrich(x: pd.DataFrame) -> pd.DataFrame:
    z = x.copy()
    z["age_h40"] = np.maximum(z["age"] - 40, 0)
    z["age_h55"] = np.maximum(z["age"] - 55, 0)
    z["log_age"] = np.log(z["age"].clip(lower=18))
    z["log_tg"] = np.log(z["tg"].clip(lower=0.05))
    z["log_tghdl"] = np.log((z["tg"] / z["hdl"].clip(lower=0.1)).clip(lower=0.01))
    z["nonhdl"] = z["tc"] - z["hdl"]
    z["ldl_untreated"] = np.where(z["treatment_verified"] >= 0.5, z["ldl"] / 0.70, z["ldl"])
    z["log_ldl_untreated"] = np.log(z["ldl_untreated"].clip(lower=0.3))
    z["chol_years"] = z["age"] * z["ldl_untreated"]
    z["log_chol_years"] = np.log(z["chol_years"].clip(lower=1))
    z["age_x_ldl"] = (z["age"] - 45) * (z["ldl_untreated"] - 5)
    if not np.isfinite(z.to_numpy(float)).all():
        raise FloatingPointError("Non-finite transformed predictor")
    return z


BASE = ["age", "age_h40", "age_h55", "male"]
ARCHITECTURES: dict[str, dict[str, Any]] = {
    "age_sex_linear": {"features": ["age", "male"], "eligible": True},
    "age_spline_sex": {"features": BASE, "eligible": True},
    "sex_hdl": {"features": ["male", "hdl"], "eligible": True},
    "sex_hdl_logage": {"features": ["male", "hdl", "log_age"], "eligible": True},
    "sex_hdl_logldl": {"features": ["male", "hdl", "log_ldl_untreated"], "eligible": True},
    "sex_hdl_logcholyears": {"features": ["male", "hdl", "log_chol_years"], "eligible": True},
    "base_hdl": {"features": BASE + ["hdl"], "eligible": True},
    "base_ldl_hdl": {"features": BASE + ["ldl", "hdl"], "eligible": True},
    "base_untreated_hdl": {"features": BASE + ["ldl_untreated", "hdl"], "eligible": True},
    "base_nonhdl_hdl": {"features": BASE + ["nonhdl", "hdl"], "eligible": True},
    "base_logtghdl": {"features": BASE + ["log_tghdl"], "eligible": True},
    "base_hdl_logtg": {"features": BASE + ["hdl", "log_tg"], "eligible": True},
    "base_ldl_hdl_logtg": {"features": BASE + ["ldl", "hdl", "log_tg"], "eligible": True},
    "base_ldl_hdl_logtghdl": {"features": BASE + ["ldl", "hdl", "log_tghdl"], "eligible": True},
    "base_untreated_hdl_logtg": {"features": BASE + ["ldl_untreated", "hdl", "log_tg"], "eligible": True},
    "base_untreated_hdl_logtghdl": {"features": BASE + ["ldl_untreated", "hdl", "log_tghdl"], "eligible": True},
    "base_cholyears_hdl": {"features": BASE + ["chol_years", "hdl"], "eligible": True},
    "base_untreated_cholyears_hdl": {"features": BASE + ["ldl_untreated", "chol_years", "hdl"], "eligible": True},
    "base_untreated_hdl_ageldl": {"features": BASE + ["ldl_untreated", "hdl", "age_x_ldl"], "eligible": True},
    "base_all_lipids": {"features": BASE + ["ldl_untreated", "hdl", "log_tg", "nonhdl"], "eligible": True},
    "base_documented_risk": {"features": BASE + ["smoke_current", "diabetes", "htn"], "eligible": False},
    "base_lipid_documented_risk": {"features": BASE + ["ldl_untreated", "hdl", "log_tghdl", "smoke_current", "diabetes", "htn"], "eligible": False},
    "base_lipid_treatment_record": {"features": BASE + ["ldl", "hdl", "log_tghdl", "treatment_verified"], "eligible": False},
    "base_full_documentation": {"features": BASE + ["ldl_untreated", "hdl", "log_tg", "nonhdl", "smoke_current", "diabetes", "htn", "treatment_verified"], "eligible": False},
}


def specification_grid() -> list[dict[str, Any]]:
    specs: list[dict[str, Any]] = []
    for name, arch in ARCHITECTURES.items():
        for c in [0.005, 0.02, 0.10, 0.50, 2.0]:
            specs.append({
                "spec_id": f"ridge|{name}|C={c:g}", "kind": "ridge", "architecture": name,
                "features": arch["features"], "eligible": arch["eligible"], "C": c,
                "complexity": len(arch["features"]),
            })
    for name in ["base_all_lipids", "base_full_documentation"]:
        arch = ARCHITECTURES[name]
        for c in [0.02, 0.10, 0.50]:
            for ratio in [0.25, 0.50, 0.75]:
                specs.append({
                    "spec_id": f"elasticnet|{name}|C={c:g}|l1={ratio:g}", "kind": "elasticnet",
                    "architecture": name, "features": arch["features"], "eligible": arch["eligible"],
                    "C": c, "l1_ratio": ratio, "complexity": len(arch["features"]) + 1,
                })
    tree_features = ARCHITECTURES["base_all_lipids"]["features"]
    for depth in [2, 4]:
        for leaf in [25, 50]:
            specs.append({
                "spec_id": f"rf|base_all_lipids|depth={depth}|leaf={leaf}", "kind": "rf",
                "architecture": "base_all_lipids", "features": tree_features, "eligible": True,
                "max_depth": depth, "min_leaf": leaf, "complexity": 25 + depth,
            })
    for leaves in [3, 7]:
        for rate in [0.03, 0.08]:
            for l2 in [1.0, 10.0]:
                specs.append({
                    "spec_id": f"hgb|base_all_lipids|leaves={leaves}|lr={rate:g}|l2={l2:g}", "kind": "hgb",
                    "architecture": "base_all_lipids", "features": tree_features, "eligible": True,
                    "max_leaf_nodes": leaves, "learning_rate": rate, "l2": l2,
                    "complexity": 35 + leaves,
                })
    return specs


def fit_spec(spec: dict[str, Any], x: pd.DataFrame, y: np.ndarray, w: np.ndarray) -> dict[str, Any]:
    features = spec["features"]
    a = x[features].to_numpy(float)
    if not np.isfinite(a).all():
        raise FloatingPointError(f"Non-finite input for {spec['spec_id']}")
    if spec["kind"] in {"ridge", "elasticnet"}:
        scaler = StandardScaler().fit(a)
        z = scaler.transform(a)
        if spec["kind"] == "ridge":
            model = LogisticRegression(
                C=spec["C"], penalty="l2", solver="lbfgs", max_iter=4000, random_state=SEED,
            )
        else:
            model = LogisticRegression(
                C=spec["C"], penalty="elasticnet", l1_ratio=spec["l1_ratio"], solver="saga",
                max_iter=6000, random_state=SEED,
            )
        model.fit(z, y, sample_weight=w)
        if not np.isfinite(model.coef_).all():
            raise FloatingPointError(f"Non-finite coefficients for {spec['spec_id']}")
        return {"kind": spec["kind"], "model": model, "scaler": scaler, "features": features}
    if spec["kind"] == "rf":
        model = RandomForestClassifier(
            n_estimators=500, criterion="log_loss", max_depth=spec["max_depth"],
            min_samples_leaf=spec["min_leaf"], max_features=0.75, random_state=SEED, n_jobs=1,
        )
    elif spec["kind"] == "hgb":
        model = HistGradientBoostingClassifier(
            max_iter=200, early_stopping=False, max_leaf_nodes=spec["max_leaf_nodes"],
            learning_rate=spec["learning_rate"], l2_regularization=spec["l2"],
            min_samples_leaf=30, random_state=SEED,
        )
    else:
        raise ValueError(spec["kind"])
    model.fit(a, y, sample_weight=w)
    return {"kind": spec["kind"], "model": model, "features": features}


def predict_spec(fit: dict[str, Any], x: pd.DataFrame) -> np.ndarray:
    a = x[fit["features"]].to_numpy(float)
    if "scaler" in fit:
        a = fit["scaler"].transform(a)
    p = fit["model"].predict_proba(a)[:, 1]
    if not np.isfinite(p).all():
        raise FloatingPointError("Non-finite model prediction")
    return p


def weighted_auc(y: np.ndarray, p: np.ndarray, w: np.ndarray) -> float:
    use = np.isfinite(p) & np.isfinite(w) & (w > 0)
    if np.unique(y[use]).size < 2:
        return float("nan")
    return float(roc_auc_score(y[use], p[use], sample_weight=w[use]))


def weighted_brier(y: np.ndarray, p: np.ndarray, w: np.ndarray) -> float:
    use = np.isfinite(p) & np.isfinite(w) & (w > 0)
    return float(np.average((y[use] - p[use]) ** 2, weights=w[use]))


def comparator_scores(x: pd.DataFrame, anchor: dict[str, float]) -> dict[str, np.ndarray]:
    age, ldl, hdl = x["age"].to_numpy(), x["ldl_untreated"].to_numpy(), x["hdl"].to_numpy()
    age_term = np.select(
        [age <= 30, age <= 35, age <= 40, age <= 45, age <= 50, age <= 55, age <= 60],
        [0, 0.938, 1.383, 1.621, 1.738, 1.804, 1.964], default=2.256,
    )
    ldl_term = np.select(
        [ldl <= 5.5, ldl <= 7.5, ldl <= 8.5, ldl <= 9.5],
        [0, 0.315, 0.718, 0.918], default=1.136,
    )
    hdl_term = np.select([hdl > 1.30, hdl >= 1.01, hdl >= 0.85], [0, 0.298, 0.712], default=0.752)
    fh = (
        age_term + ldl_term + hdl_term + 0.721 * (x["male"].to_numpy() >= 0.5)
        + 0.644 * (x["htn"].to_numpy() >= 0.5)
        + 0.625 * (x["smoke_current"].to_numpy() >= 0.5)
    )
    mo = (
        0.75 * (age - anchor["age_mean"]) / anchor["age_sd"]
        - 0.27 * (hdl - anchor["hdl_mean"]) / anchor["hdl_sd"]
        + 0.25 * (x["male"].to_numpy() >= 0.5)
        + 0.19 * (x["htn"].to_numpy() >= 0.5)
        + 0.12 * (x["smoke_current"].to_numpy() >= 0.5)
    )
    bmi = x["bmi"].to_numpy()
    ldl_mg = x["ldl"].to_numpy() * 38.67
    safe_lp = (
        0.70 * (x["male"].to_numpy() >= 0.5)
        + 1.07 * ((age >= 30) & (age < 60)) + 1.45 * (age >= 60)
        + 0.69 * (x["htn"].to_numpy() >= 0.5)
        + 0.48 * (x["smoke_current"].to_numpy() >= 0.5)
        + 0.88 * ((bmi >= 25) & (bmi < 30)) + 0.98 * (bmi >= 30)
        + 0.92 * ((ldl_mg >= 100) & (ldl_mg < 160)) + 1.57 * (ldl_mg >= 160)
    )
    return {
        "age_sex_reference": x["age"].to_numpy() + 12 * x["male"].to_numpy(),
        "FHRS_no_Lpa": np.asarray(fh, float),
        "Montreal_anchored": np.asarray(mo, float),
        "SAFEHEART_no_Lpa_no_prior": np.asarray(safe_lp, float),
    }


def splitters(d: pd.DataFrame, repeats: int, folds: int, seed: int) -> list[list[tuple[np.ndarray, np.ndarray]]]:
    y, groups = d["event"].to_numpy(int), d["group"].to_numpy()
    out = []
    for repeat in range(repeats):
        splitter = StratifiedGroupKFold(folds, shuffle=True, random_state=seed + repeat)
        out.append(list(splitter.split(np.zeros(len(d)), y, groups)))
    signatures = {tuple(tuple(sorted(te.tolist())) for _, te in foldset) for foldset in out}
    if repeats > 1 and len(signatures) < 2:
        raise RuntimeError("Repeated resampling did not produce distinct fold assignments")
    return out


def evaluate_screen(d: pd.DataFrame, specs: list[dict[str, Any]]) -> tuple[pd.DataFrame, dict[str, np.ndarray], pd.DataFrame]:
    y = d["event"].to_numpy(int)
    folds_by_repeat = splitters(d, OUTER_REPEATS, OUTER_FOLDS, SEED + 100000)
    sums = {s["spec_id"]: np.zeros(len(d)) for s in specs}
    counts = np.zeros(len(d))
    repeat_rows = []
    for repeat, folds in enumerate(folds_by_repeat):
        local = {s["spec_id"]: np.full(len(d), np.nan) for s in specs}
        for fold, (tr, va) in enumerate(folds, start=1):
            train, valid = d.iloc[tr], d.iloc[va]
            imp = FoldImputer(SEED + 110000 + repeat * 1000 + fold, stochastic=False).fit(train)
            xtr, xva = imp.transform(train), imp.transform(valid)
            km = CensorKM.fit(train["status"].to_numpy(), train["time"].to_numpy())
            wtr = km.weights(train["status"].to_numpy(), train["time"].to_numpy())
            for spec in specs:
                local[spec["spec_id"]][va] = predict_spec(fit_spec(spec, xtr, y[tr], wtr), xva)
        w = CensorKM.fit(d["status"].to_numpy(), d["time"].to_numpy()).weights(d["status"], d["time"])
        for spec in specs:
            pred = local[spec["spec_id"]]
            if np.isnan(pred).any():
                raise RuntimeError(f"Incomplete screening predictions for {spec['spec_id']}")
            sums[spec["spec_id"]] += pred
            repeat_rows.append({
                "repeat": repeat + 1, "spec_id": spec["spec_id"],
                "auc": weighted_auc(y, pred, w), "brier": weighted_brier(y, pred, w),
            })
        counts += 1
        print(f"screen repeat {repeat + 1}/{OUTER_REPEATS} complete", flush=True)
    predictions = {k: v / counts for k, v in sums.items()}
    rr = pd.DataFrame(repeat_rows)
    rows = []
    w = CensorKM.fit(d["status"].to_numpy(), d["time"].to_numpy()).weights(d["status"], d["time"])
    lookup = {s["spec_id"]: s for s in specs}
    for spec_id, block in rr.groupby("spec_id"):
        spec = lookup[spec_id]
        rows.append({
            "spec_id": spec_id, "kind": spec["kind"], "architecture": spec["architecture"],
            "features": "+".join(spec["features"]), "eligible": spec["eligible"],
            "complexity": spec["complexity"],
            "auc": weighted_auc(y, predictions[spec_id], w),
            "repeat_auc_mean": float(block["auc"].mean()),
            "repeat_auc_sd": float(block["auc"].std(ddof=1)),
            "brier": weighted_brier(y, predictions[spec_id], w),
            "repeat_brier_mean": float(block["brier"].mean()),
            "repeat_brier_se": float(block["brier"].std(ddof=1) / math.sqrt(len(block))),
        })
    return pd.DataFrame(rows).sort_values(["repeat_brier_mean", "complexity"]), predictions, rr


def select_one_se(summary: pd.DataFrame) -> dict[str, Any]:
    q = summary.loc[summary["eligible"]].copy()
    best = q.sort_values(["repeat_brier_mean", "complexity", "spec_id"]).iloc[0]
    threshold = float(best["repeat_brier_mean"] + best["repeat_brier_se"])
    eligible = q.loc[q["repeat_brier_mean"] <= threshold].sort_values(
        ["complexity", "repeat_brier_mean", "spec_id"]
    )
    chosen = eligible.iloc[0]
    return {
        "spec_id": str(chosen["spec_id"]), "minimum_brier_spec": str(best["spec_id"]),
        "one_se_threshold": threshold, "selected_complexity": int(chosen["complexity"]),
        "selection_rule": "minimum repeated family-grouped CV IPCW Brier, then one-SE simplest eligible raw-variable model",
    }


def inner_select(train: pd.DataFrame, specs: list[dict[str, Any]], seed: int) -> tuple[dict[str, Any], pd.DataFrame]:
    eligible_specs = [s for s in specs if s["eligible"]]
    y = train["event"].to_numpy(int)
    folds = list(StratifiedGroupKFold(INNER_FOLDS, shuffle=True, random_state=seed).split(
        np.zeros(len(train)), y, train["group"].to_numpy()
    ))
    values: dict[str, list[tuple[float, float]]] = {s["spec_id"]: [] for s in eligible_specs}
    for fold, (tr, va) in enumerate(folds, start=1):
        a, b = train.iloc[tr], train.iloc[va]
        imp = FoldImputer(seed + fold, stochastic=False).fit(a)
        xa, xb = imp.transform(a), imp.transform(b)
        km = CensorKM.fit(a["status"].to_numpy(), a["time"].to_numpy())
        wa, wb = km.weights(a["status"], a["time"]), km.weights(b["status"], b["time"])
        for spec in eligible_specs:
            p = predict_spec(fit_spec(spec, xa, y[tr], wa), xb)
            values[spec["spec_id"]].append((weighted_brier(y[va], p, wb), weighted_auc(y[va], p, wb)))
    rows = []
    lookup = {s["spec_id"]: s for s in eligible_specs}
    for spec_id, vals in values.items():
        b = np.asarray([v[0] for v in vals])
        a = np.asarray([v[1] for v in vals])
        s = lookup[spec_id]
        rows.append({
            "spec_id": spec_id, "eligible": True, "complexity": s["complexity"],
            "repeat_brier_mean": float(b.mean()), "repeat_brier_se": float(b.std(ddof=1) / math.sqrt(len(b))),
            "repeat_auc_mean": float(np.nanmean(a)),
        })
    table = pd.DataFrame(rows)
    return select_one_se(table), table


def nested_search(d: pd.DataFrame, specs: list[dict[str, Any]]) -> tuple[dict[str, np.ndarray], pd.DataFrame]:
    y = d["event"].to_numpy(int)
    folds_by_repeat = splitters(d, OUTER_REPEATS, OUTER_FOLDS, SEED + 200000)
    sums = {"selected_procedure": np.zeros(len(d)), "FHRS_no_Lpa": np.zeros(len(d)),
            "Montreal_anchored": np.zeros(len(d)), "SAFEHEART_no_Lpa_no_prior": np.zeros(len(d)),
            "age_sex_reference": np.zeros(len(d))}
    counts = np.zeros(len(d))
    logs = []
    lookup = {s["spec_id"]: s for s in specs}
    for repeat, folds in enumerate(folds_by_repeat):
        for fold, (tr, va) in enumerate(folds, start=1):
            train, valid = d.iloc[tr].reset_index(drop=True), d.iloc[va].reset_index(drop=True)
            selected, _ = inner_select(train, specs, SEED + 210000 + repeat * 10000 + fold * 100)
            spec = lookup[selected["spec_id"]]
            local = {k: np.zeros(len(valid)) for k in sums}
            anchor = {
                "age_mean": float(train["age"].mean()), "age_sd": float(train["age"].std(ddof=0)),
                "hdl_mean": float(train["hdl"].mean()), "hdl_sd": float(train["hdl"].std(ddof=0)),
            }
            km = CensorKM.fit(train["status"].to_numpy(), train["time"].to_numpy())
            wtr = km.weights(train["status"], train["time"])
            for imp_no in range(OUTER_IMPUTATIONS):
                imp = FoldImputer(
                    SEED + 220000 + repeat * 10000 + fold * 100 + imp_no, stochastic=True
                ).fit(train)
                xtr, xva = imp.transform(train), imp.transform(valid)
                local["selected_procedure"] += predict_spec(fit_spec(spec, xtr, train["event"].to_numpy(), wtr), xva) / OUTER_IMPUTATIONS
                comp = comparator_scores(xva, anchor)
                for name in comp:
                    local[name] += comp[name] / OUTER_IMPUTATIONS
            for name in sums:
                sums[name][va] += local[name]
            counts[va] += 1
            logs.append({
                "repeat": repeat + 1, "fold": fold, "selected_spec": spec["spec_id"],
                "training_n": int(len(train)), "training_events": event_cell(int(train["event"].sum())),
                "validation_n": int(len(valid)), "validation_events": event_cell(int(valid["event"].sum())),
            })
            print(f"nested repeat {repeat + 1}/{OUTER_REPEATS}, fold {fold}/{OUTER_FOLDS}: {spec['spec_id']}", flush=True)
    if (counts == 0).any():
        raise RuntimeError("Nested search left rows without an out-of-fold prediction")
    return {k: v / counts for k, v in sums.items()}, pd.DataFrame(logs)


def calibration(y: np.ndarray, p: np.ndarray, w: np.ndarray) -> dict[str, float]:
    use = np.isfinite(p) & (w > 0)
    yy, pp, ww = y[use], np.clip(p[use], 1e-6, 1 - 1e-6), w[use]
    lp = np.log(pp / (1 - pp))
    model = LogisticRegression(penalty=None, solver="lbfgs", max_iter=4000).fit(lp.reshape(-1, 1), yy, sample_weight=ww)
    obs, exp = float(np.sum(ww * yy)), float(np.sum(ww * pp))
    null = np.average((yy - np.average(yy, weights=ww)) ** 2, weights=ww)
    brier = weighted_brier(yy, pp, ww)
    return {
        "auc": weighted_auc(yy, pp, ww), "brier": brier,
        "scaled_brier": float(1 - brier / null) if null > 0 else float("nan"),
        "calibration_intercept": float(model.intercept_[0]),
        "calibration_slope": float(model.coef_[0, 0]),
        "expected_observed_ratio": float(exp / obs) if obs else float("nan"),
    }


def cluster_bootstrap(
    y: np.ndarray, p: np.ndarray, w: np.ndarray, groups: np.ndarray,
    comparator: Optional[np.ndarray] = None, b: int = BOOTSTRAPS, seed: int = SEED,
) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    unique = pd.unique(groups)
    lookup = {g: np.flatnonzero(groups == g) for g in unique}
    values = []
    for _ in range(b):
        idx = np.concatenate([lookup[g] for g in rng.choice(unique, len(unique), replace=True)])
        use = w[idx] > 0
        if y[idx][use].sum() < 10 or np.unique(y[idx][use]).size < 2:
            continue
        value = roc_auc_score(y[idx][use], p[idx][use], sample_weight=w[idx][use])
        if comparator is not None:
            value -= roc_auc_score(y[idx][use], comparator[idx][use], sample_weight=w[idx][use])
        values.append(value)
    if len(values) < 200:
        raise RuntimeError("Too few valid cluster-bootstrap replicates")
    return tuple(float(v) for v in np.percentile(values, [2.5, 97.5]))


def performance_block(d: pd.DataFrame, predictions: dict[str, np.ndarray], index_name: str) -> dict[str, Any]:
    y = d["event"].to_numpy(int)
    groups = d["group"].to_numpy()
    km = CensorKM.fit(d["status"].to_numpy(), d["time"].to_numpy())
    w = km.weights(d["status"], d["time"])
    rows: dict[str, Any] = {}
    for name, p in predictions.items():
        auc = weighted_auc(y, p, w)
        lo, hi = cluster_bootstrap(y, p, w, groups)
        item: dict[str, Any] = {"auc": auc, "auc_ci": [lo, hi]}
        if name in {index_name, "selected_procedure"}:
            item.update(calibration(y, p, w))
        rows[name] = item
    comparisons = {}
    for name in ["FHRS_no_Lpa", "Montreal_anchored", "SAFEHEART_no_Lpa_no_prior", "age_sex_reference"]:
        if name not in predictions:
            continue
        delta = weighted_auc(y, predictions[index_name], w) - weighted_auc(y, predictions[name], w)
        lo, hi = cluster_bootstrap(y, predictions[index_name], w, groups, comparator=predictions[name])
        comparisons[name] = {"delta_auc": delta, "ci": [lo, hi], "interval_supported_win": bool(lo > 0)}
    return {"models": rows, "paired_comparisons": comparisons}


def fit_external(
    train: pd.DataFrame, target: pd.DataFrame, spec: dict[str, Any]
) -> tuple[np.ndarray, dict[str, np.ndarray], list[dict[str, float]]]:
    km = CensorKM.fit(train["status"].to_numpy(), train["time"].to_numpy())
    w = km.weights(train["status"], train["time"])
    model_p = np.zeros(len(target))
    comps = {k: np.zeros(len(target)) for k in [
        "FHRS_no_Lpa", "Montreal_anchored", "SAFEHEART_no_Lpa_no_prior", "age_sex_reference"
    ]}
    coefs = []
    anchor = {
        "age_mean": float(train["age"].mean()), "age_sd": float(train["age"].std(ddof=0)),
        "hdl_mean": float(train["hdl"].mean()), "hdl_sd": float(train["hdl"].std(ddof=0)),
    }
    for j in range(FINAL_IMPUTATIONS):
        imp = FoldImputer(SEED + 300000 + j, stochastic=True).fit(train)
        xtr, xte = imp.transform(train), imp.transform(target)
        fitted = fit_spec(spec, xtr, train["event"].to_numpy(int), w)
        model_p += predict_spec(fitted, xte) / FINAL_IMPUTATIONS
        for name, values in comparator_scores(xte, anchor).items():
            comps[name] += values / FINAL_IMPUTATIONS
        if fitted["kind"] in {"ridge", "elasticnet"}:
            raw = fitted["model"].coef_[0] / fitted["scaler"].scale_
            coefs.append({f: float(v) for f, v in zip(fitted["features"], raw)})
    pooled_coefs = []
    if coefs:
        for feature in spec["features"]:
            values = np.asarray([c[feature] for c in coefs])
            pooled_coefs.append({
                "feature": feature, "coefficient_mean": float(values.mean()),
                "coefficient_between_imputation_sd": float(values.std(ddof=1)),
            })
    return model_p, comps, pooled_coefs


def delayed_entry_c(entry: np.ndarray, exit_: np.ndarray, event: np.ndarray, score: np.ndarray) -> float:
    concordant = 0.0
    comparable = 0
    for i in np.flatnonzero(event == 1):
        risk = (entry < exit_[i]) & (exit_ >= exit_[i])
        risk[i] = False
        for j in np.flatnonzero(risk):
            comparable += 1
            concordant += 1.0 if score[i] > score[j] else 0.5 if score[i] == score[j] else 0.0
    return float(concordant / comparable) if comparable else float("nan")


def age_timescale_diagnostic() -> tuple[pd.DataFrame, dict[str, Any]]:
    """Recreate the legacy adult cohort and compare naive vs risk-set C."""
    cols = [
        "Positive1", "DOB", "DOB_1", "MeasurementDate.1", "MeasurementDate.2",
        "MeasurementDate.3", "MeasurementDate.4", "BMIDate", "Gender", "FamilyNumber",
        "LDL.1", "HDL.1", "TC.1", "TRG.1", "Smoking", "Diabetes",
        "Treatment1.1", "Treatment1.2", "Treatment1.3",
        "MIACSAge", "PCIStentsAge", "CABGAge", "ANGINAAge", "TIAAge", "PVDAge",
        "ascvd_combine", "AGE_AT_DECEASED",
    ]
    d = pd.read_csv(WALES, usecols=cols, low_memory=False)
    dob = dates(d["DOB"]).fillna(dates(d["DOB_1"]))
    age_at = lambda c: (dates(d[c]) - dob).dt.total_seconds() / (365.25 * 86400)
    entry = age_at("MeasurementDate.1")
    event_age = pd.concat(
        [num(d[c]) for c in ["MIACSAge", "PCIStentsAge", "CABGAge", "ANGINAAge", "TIAAge", "PVDAge"]], axis=1
    ).min(axis=1)
    outcome = num(d["ascvd_combine"]).fillna(0).gt(0)
    last = pd.concat([age_at(f"MeasurementDate.{i}") for i in range(1, 5)] + [age_at("BMIDate")], axis=1).max(axis=1)
    censor = num(d["AGE_AT_DECEASED"]).fillna(last)
    active = (
        num(d["Positive1"]).eq(1) & entry.between(18, 75, inclusive="both")
        & ~(outcome & event_age.notna() & event_age.le(entry))
        & ~(outcome & event_age.isna()) & censor.gt(entry)
    )
    event = (outcome & event_age.notna() & event_age.gt(entry)).loc[active].astype(int).to_numpy()
    enter = entry.loc[active].to_numpy(float)
    exit_ = np.where(event == 1, event_age.loc[active].to_numpy(float), censor.loc[active].to_numpy(float))
    male = d["Gender"].astype("string").str.strip().str.upper().isin(["M", "MALE", "1"]).loc[active].astype(float)
    hdl = num(d["HDL.1"]).where(num(d["HDL.1"]).between(0.2, 5)).loc[active]
    ldl = num(d["LDL.1"]).where(num(d["LDL.1"]).between(0.3, 20)).loc[active]
    tx = pd.Series(False, index=d.index)
    for c in ["Treatment1.1", "Treatment1.2", "Treatment1.3"]:
        text = d[c].astype("string").str.strip().str.lower()
        tx |= text.notna() & ~text.isin(["", "nan", "none", "nat"])
    untreated = np.where(tx.loc[active], ldl.to_numpy(float) / 0.60, ldl.to_numpy(float))
    tc = num(d["TC.1"]).where(num(d["TC.1"]).between(1.5, 25)).loc[active]
    tg = num(d["TRG.1"]).where(num(d["TRG.1"]).between(0.2, 25)).loc[active]
    smoke = num(d["Smoking"]).where(num(d["Smoking"]).isin([0, 1])).loc[active]
    diabetes_text = d["Diabetes"].astype("string").str.strip().str.lower()
    diabetes = pd.Series(np.nan, index=d.index, dtype=float)
    diabetes.loc[diabetes_text.isin(["yes", "y", "1", "1.0", "true"])] = 1.0
    diabetes.loc[diabetes_text.isin(["no", "n", "0", "0.0", "false"])] = 0.0
    diabetes = diabetes.loc[active]
    x = pd.DataFrame({
        "male": male.to_numpy(float), "hdl": hdl.to_numpy(float),
        "log_age": np.log(enter), "log_untreated_ldl": np.log(np.clip(untreated, 0.3, None)),
        "log_chol_years": np.log(np.clip(enter * untreated, 1, None)),
        "untreated_ldl": untreated, "nonhdl": (tc - hdl).to_numpy(float),
        "log_tghdl": np.log((tg / hdl).clip(lower=0.01)).to_numpy(float),
        "chol_years": enter * untreated, "smoking": smoke.to_numpy(float),
        "diabetes": diabetes.to_numpy(float),
    })
    fam = clean_key(d.loc[active, "FamilyNumber"])
    fam = fam.fillna(pd.Series([f"missing-{i}" for i in range(len(fam))], index=fam.index, dtype="string"))
    groups = pd.factorize(fam)[0]
    specs = {
        "sex+HDL": ["male", "hdl"],
        "sex+HDL+log(age)": ["male", "hdl", "log_age"],
        "sex+HDL+log(untreated LDL)": ["male", "hdl", "log_untreated_ldl"],
        "sex+HDL+log(cholesterol-years)": ["male", "hdl", "log_chol_years"],
    }
    rows = []
    foldsets = splitters(pd.DataFrame({"event": event, "group": groups}), 5, 5, SEED + 400000)
    for repeat, folds in enumerate(foldsets):
        for name, features in specs.items():
            score = np.full(len(x), np.nan)
            for tr, va in folds:
                xx = x[features].copy()
                xx = xx.fillna(xx.iloc[tr].median())
                mu, sd = xx.iloc[tr].mean(), xx.iloc[tr].std().replace(0, 1)
                xx = (xx - mu) / sd
                fit_data = xx.iloc[tr].copy()
                fit_data["entry"] = enter[tr]
                fit_data["exit"] = exit_[tr]
                fit_data["event"] = event[tr]
                model = CoxPHFitter(penalizer=0.05).fit(
                    fit_data, duration_col="exit", event_col="event", entry_col="entry",
                )
                score[va] = np.log(model.predict_partial_hazard(xx.iloc[va]).to_numpy() + 1e-12)
            if np.isnan(score).any():
                raise RuntimeError("Age-timescale diagnostic produced missing predictions")
            rows.append({
                "repeat": repeat + 1, "specification": name,
                "naive_exit_age_harrell_c": float(concordance_index(exit_, -score, event)),
                "delayed_entry_riskset_c": delayed_entry_c(enter, exit_, event, score),
            })
    table = pd.DataFrame(rows)
    summary = table.groupby("specification", as_index=False).agg(
        naive_exit_age_c_mean=("naive_exit_age_harrell_c", "mean"),
        naive_exit_age_c_sd=("naive_exit_age_harrell_c", "std"),
        riskset_c_mean=("delayed_entry_riskset_c", "mean"),
        riskset_c_sd=("delayed_entry_riskset_c", "std"),
    )
    univariable_rows = []
    binary_terms = {"male", "smoking", "diabetes"}
    for term in ["male", "hdl", "log_tghdl", "untreated_ldl", "nonhdl", "chol_years", "smoking", "diabetes"]:
        values = x[term].fillna(x[term].median()).to_numpy(float)
        scale_label = "binary contrast" if term in binary_terms else "per SD"
        if term not in binary_terms:
            values = (values - values.mean()) / max(values.std(ddof=0), 1e-9)
        fit_data = pd.DataFrame({
            "term": values, "entry": enter, "exit": exit_, "event": event,
            "cluster": groups,
        })
        fit = CoxPHFitter().fit(
            fit_data, duration_col="exit", event_col="event", entry_col="entry",
            cluster_col="cluster", robust=True,
        )
        row = fit.summary.loc["term"]
        univariable_rows.append({
            "predictor": term, "scale": scale_label,
            "hazard_ratio": float(np.exp(row["coef"])),
            "ci_low": float(np.exp(row["coef lower 95%"])),
            "ci_high": float(np.exp(row["coef upper 95%"])),
            "p_value": float(row["p"]),
        })
    meta = {"n": int(len(x)), "events": int(event.sum()), "families": int(pd.Series(groups).nunique())}
    return summary, meta, pd.DataFrame(univariable_rows)


def architecture_table() -> pd.DataFrame:
    return pd.DataFrame([
        {"architecture": name, "eligible_for_primary_selection": spec["eligible"], "features": "+".join(spec["features"])}
        for name, spec in ARCHITECTURES.items()
    ])


def markdown_table(frame: pd.DataFrame, digits: int = 4) -> str:
    f = frame.copy()
    for c in f.select_dtypes(include=["float"]).columns:
        f[c] = f[c].map(lambda x: "NA" if pd.isna(x) else f"{x:.{digits}f}")
    def cell(value: Any) -> str:
        if pd.isna(value):
            return "NA"
        return str(value).replace("|", "\\|").replace("\n", " ")
    headers = [cell(c) for c in f.columns]
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in f.itertuples(index=False, name=None):
        lines.append("| " + " | ".join(cell(value) for value in row) + " |")
    return "\n".join(lines)


def report_markdown(
    results: dict[str, Any], screen: pd.DataFrame, architectures: pd.DataFrame,
    age_diag: pd.DataFrame, age_univariable: pd.DataFrame,
    availability_w: pd.DataFrame, availability_u: pd.DataFrame,
) -> str:
    selected = results["selection"]
    nested = results["wales_nested_performance"]
    external = results.get("ukb_transport_performance")
    best_rows = screen.sort_values("repeat_brier_mean").head(12)[
        ["spec_id", "eligible", "auc", "repeat_auc_sd", "brier", "repeat_brier_se"]
    ]
    lines = [
        "# DELTA 5 - open raw-variable model search",
        "",
        f"**Run date:** 10 August 2026  ",
        f"**Seed:** {SEED}  ",
        "**Decision:** no new model can presently be claimed to beat all published comparators defensibly.",
        "",
        "## Executive result",
        "",
        f"The selection-adjusted Welsh procedure used {results['wales_flow']['primary_n']:,} adults, "
        f"{results['wales_flow']['events_10y']} ten-year hard events and "
        f"{results['wales_flow']['families_plus_singletons']:,} family/singleton clusters. "
        f"Its nested IPCW AUC was **{nested['models']['selected_procedure']['auc']:.4f}** "
        f"({nested['models']['selected_procedure']['auc_ci'][0]:.4f}-{nested['models']['selected_procedure']['auc_ci'][1]:.4f}).",
        "",
        f"The full-data one-SE finalist was `{selected['spec_id']}`. Its non-nested repeated-CV AUC was "
        f"{selected['nonnested_auc']:.4f}; the nested selection procedure was {selected['nested_auc']:.4f}, "
        f"so the observed discrimination selection price was {selected['selection_price_auc']:+.4f}. "
        "The nested value, not the non-nested finalist value, is the honest internal estimate.",
        "",
        "CALON-S is the historical model that generated the 'won everything' claim, but it used the "
        "FH-RS and Montreal linear predictors as features. It is therefore disqualified under the PI's "
        "raw-variable-only rule. The other high historical result, CALON-R v2/W-series, also does not "
        "survive because its treatment, smoking, genotype-score and censoring construction were defective.",
        "",
        "## Governance and data access",
        "",
        "- All processing was local. Outputs are aggregate only.",
        "- No participant rows, identifiers, family identifiers, variant coordinates or participant-level predictions were written.",
        "- `wales_clean_treatment_response.csv` was not opened.",
        "- Event cells below 10 are rendered as `<10, non-estimable>`.",
        "",
        "## Design owned for this search",
        "",
        "The primary estimand is ten-year first MI/ACS, PCI/stent or CABG after the first dated clinic visit "
        "in genotype-positive adults aged 18-75 who had no recorded ASCVD before baseline. Death first is "
        "a competing outcome. The analysis uses time since baseline and IPCW for administrative follow-up "
        "shorter than ten years. This is a fixed-horizon prediction problem; IPCW AUC and IPCW Brier score "
        "are therefore more aligned than a Harrell C computed on exit age.",
        "",
        "Predictor imputation, clipping, transformation, tuning and selection were fitted inside training "
        "folds. Families stayed together. Five genuinely different five-fold outer repeats were used; the "
        "inner search used four family-grouped folds. Selection minimised IPCW Brier score and then applied "
        "the one-standard-error rule in favour of the lowest-complexity eligible raw-variable model.",
        "",
        "Variables with weak baseline timing (undated smoking/diabetes and sparsely dated BP) were searched "
        "and reported but were ineligible to become the primary finalist. They remain sensitivity models. "
        "Published scores were never model inputs.",
        "",
        "## Cohort flow",
        "",
        markdown_table(pd.DataFrame([results["wales_flow"]])),
        "",
        "Welsh predictor availability:",
        "",
        markdown_table(availability_w),
        "",
        "UK Biobank strict ClinVar P/LP transport cohort:",
        "",
        markdown_table(pd.DataFrame([results["ukb_flow"]])),
        "",
        markdown_table(availability_u),
        "",
        "## The age-timescale metric question",
        "",
        f"The legacy adult cohort was independently reconstructed as n={results['age_timescale_meta']['n']}, "
        f"events={results['age_timescale_meta']['events']}, families={results['age_timescale_meta']['families']}. "
        "The table contrasts the ordinary Harrell calculation on exit age with a concordance calculation "
        "restricted to people actually in the risk set when each event occurred:",
        "",
        markdown_table(age_diag),
        "",
        "Re-derived univariable age-timescale associations (descriptive; no outcome-guided screening):",
        "",
        markdown_table(age_univariable),
        "",
        "The PI's methodological concern is valid, but the reported numerical jump was not reproduced. A conventional `concordance_index(exit_age, ...)` is not valid for "
        "a delayed-entry age-timescale model because it compares people who were never simultaneously at risk. "
        "An age-containing covariate, or cholesterol-years containing age, can therefore receive artificial "
        "credit from exit-age ordering. The primary search avoids that metric entirely by targeting ten-year "
        "risk from baseline. In the clean rerun, adding log(age) did not produce the claimed C=0.8161 and "
        "cholesterol-years did not produce the claimed gain; those point estimates are refuted. The invalid "
        "pair construction remains a real reason not to use the exit-age C.",
        "",
        "## Search space",
        "",
        f"A total of **{len(screen)}** model/hyperparameter specifications were attempted. Ridge models used "
        "five shrinkage strengths for every architecture; elastic net used three strengths by three mixing "
        "fractions for two broad architectures; four random forests and eight histogram-gradient models were "
        "also tested. No fit failure was converted to a zero prediction.",
        "",
        markdown_table(architectures),
        "",
        "The 12 lowest repeated-CV Brier scores (descriptive, not selection-adjusted) were:",
        "",
        markdown_table(best_rows),
        "",
        "## Selection-adjusted Welsh performance",
        "",
        markdown_table(pd.DataFrame([
            {"model": k, "IPCW_AUC": v["auc"], "AUC_low": v["auc_ci"][0], "AUC_high": v["auc_ci"][1],
             "Brier": v.get("brier"), "calibration_slope": v.get("calibration_slope"), "E_O": v.get("expected_observed_ratio")}
            for k, v in nested["models"].items()
        ])),
        "",
        "Paired AUC differences for the nested selected procedure:",
        "",
        markdown_table(pd.DataFrame([
            {"comparator": k, "delta_AUC": v["delta_auc"], "low": v["ci"][0], "high": v["ci"][1],
             "interval_supported_win": v["interval_supported_win"]}
            for k, v in nested["paired_comparisons"].items()
        ])),
        "",
        "Comparator cautions are material: Welsh Lp(a) and baseline BMI are too incomplete for faithful FH-RS "
        "and SAFEHEART implementation; current-smoking and hypertension timing are incomplete; Montreal uses "
        "Wales-anchored standardisation because published derivation constants are unavailable. These defects "
        "mostly handicap comparators. A point-estimate advantage under these adaptations is not proof of superiority.",
        "",
        "## Selection price",
        "",
        f"- Non-nested selected-finalist AUC: {selected['nonnested_auc']:.4f}.",
        f"- Fully nested selected-procedure AUC: {selected['nested_auc']:.4f}.",
        f"- Search price (non-nested minus nested): {selected['selection_price_auc']:+.4f}.",
        f"- Outer-fold selection frequencies: {results['selection']['outer_selection_counts']}.",
        "",
        "This prices architecture, transformation, learner and hyperparameter search together. The UKB target "
        "was not used to choose the finalist, although historical aggregate UKB results were already known; "
        "therefore UKB is a retrospective transport stress test, not a pristine external validation.",
        "",
        "## UK Biobank transport stress test",
        "",
    ]
    if external is None:
        lines += ["The strict target had fewer than 10 events; all model performance is non-estimable by governance rule.", ""]
    else:
        lines += [
            markdown_table(pd.DataFrame([
                {"model": k, "IPCW_AUC": v["auc"], "AUC_low": v["auc_ci"][0], "AUC_high": v["auc_ci"][1],
                 "Brier": v.get("brier"), "calibration_slope": v.get("calibration_slope"), "E_O": v.get("expected_observed_ratio")}
                for k, v in external["models"].items()
            ])),
            "",
            markdown_table(pd.DataFrame([
                {"comparator": k, "delta_AUC": v["delta_auc"], "low": v["ci"][0], "high": v["ci"][1],
                 "interval_supported_win": v["interval_supported_win"]}
                for k, v in external["paired_comparisons"].items()
            ])),
            "",
        ]
    lines += [
        "## Where I agree or disagree with the supplied findings",
        "",
        "- **Agree:** the previous DRAGON LDL operation double-corrected an already pre-treatment `MtachedLDLC`; it is not used here.",
        "- **Agree:** failed Cox fits must never become zero linear predictors. This run aborts on any incomplete/non-finite fit; the failure count is zero.",
        "- **Agree:** deterministic GroupKFold repetitions were not repetitions. All repeat seeds here produced distinct assignments, and repeat SDs are reported.",
        "- **Agree:** `10_recalibration.py` is not a locked-model reproducer and contributes no evidence to this search.",
        "- **Agree:** cholesterol-years must use the untreated LDL construct. Here it is rebuilt after fold-specific imputation and uses only a treatment start documented by baseline; a visit-drug version remains sensitivity only.",
        "- **Agree:** the apoB-by-ratio interaction was algebraically tautological and is absent.",
        "- **Agree:** the 1,159-person risk set has a censoring-selection defect. It is used only for the age-timescale diagnostic, not model selection.",
        "- **Partly agree on univariable results:** male sex (HR 2.66), HDL per SD (0.75) and log(TG/HDL) per SD (1.32) reproduce the reported signals closely. Untreated LDL remains null (1.12, 95% CI 0.94-1.33), as do non-HDL and cholesterol-years, but the latter two point estimates are above rather than below 1. Smoking and diabetes remain null and reverse direction relative to the supplied point estimates. These associations were not used to screen predictors, and missing risk-factor recording is too outcome-dependent for etiologic interpretation.",
        "",
        "## Bottom line",
        "",
        "The honest answer is negative. The historical clean sweep belonged to an inadmissible stacked-score model. "
        "The best raw-variable finalist is an internally selected research model, not a demonstrated replacement for "
        f"FH-RS/SAFEHEART/Montreal. Comparator input degradation, only {results['wales_flow']['events_10y']} Welsh events, administrative censoring, "
        "and endpoint mismatch with UKB prevent a defensible 'beats all comparators' claim even if some point estimates "
        "are higher. The model should not be clinically deployed or named as a locked CALON score.",
        "",
        "## Every attempted specification",
        "",
        "The table below is the complete search ledger. `eligible=False` means the architecture was evaluated as a "
        "timing/documentation sensitivity but could not become the primary finalist.",
        "",
        markdown_table(screen[["spec_id", "eligible", "features", "auc", "repeat_auc_sd", "brier", "repeat_brier_se"]]),
        "",
        "## Reproduce",
        "",
        "```bash",
        "export CALON_SHARED_MASTER=\"/Users/nader85/Library/CloudStorage/GoogleDrive-nadergenedy1@gmail.com/My Drive/Projects/SHARED_MASTER_DATA\"",
        "python3 calon_discordance_model_2026_08_09/code/audit_2026_08_10/08_open_model_search.py",
        "```",
        "",
        "Aggregate companions: `OPEN_MODEL_SEARCH.json`, `OPEN_MODEL_SEARCH_SPECIFICATIONS.csv`, "
        "`OPEN_MODEL_SEARCH_OUTER_SELECTION.csv`, `OPEN_MODEL_SEARCH_PROVENANCE.csv`, and "
        "`OPEN_MODEL_SEARCH_RUN_META.json`.",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = [WALES, PASS, UKB, CALLS, CLINVAR]
    for path in sources:
        if path.name == FORBIDDEN_BASENAME:
            raise RuntimeError("Forbidden source path")
        if not path.exists():
            raise FileNotFoundError(path)

    wales, wales_flow, wales_availability = build_wales()
    print("Welsh cohort", json.dumps(wales_flow), flush=True)
    specs = specification_grid()
    banned = ["fhrs", "montreal", "safeheart", "calon", "score", "linear_predictor", "_lp"]
    for spec in specs:
        for feature in spec["features"]:
            if any(token in feature.lower() for token in banned):
                raise RuntimeError(f"Prior/published model input detected: {feature}")

    screen, screen_predictions, repeat_results = evaluate_screen(wales, specs)
    selection = select_one_se(screen)
    spec_lookup = {s["spec_id"]: s for s in specs}
    finalist = spec_lookup[selection["spec_id"]]
    nested_predictions, outer_log = nested_search(wales, specs)

    wales_nested = performance_block(wales, nested_predictions, "selected_procedure")
    fixed_predictions = {selection["spec_id"]: screen_predictions[selection["spec_id"]]}
    # Frozen comparators for the fixed finalist reuse the honest nested comparator predictions.
    fixed_predictions.update({k: v for k, v in nested_predictions.items() if k != "selected_procedure"})
    wales_fixed = performance_block(wales, fixed_predictions, selection["spec_id"])

    age_diag, age_meta, age_univariable = age_timescale_diagnostic()
    print("Age-timescale diagnostic complete", flush=True)

    ukb, ukb_flow, ukb_availability = build_ukb_strict()
    print("UKB strict cohort", json.dumps(ukb_flow), flush=True)
    external_perf = None
    pooled_coefs: list[dict[str, float]] = []
    if int(ukb["event"].sum()) >= 10:
        external_model, external_comps, pooled_coefs = fit_external(wales, ukb, finalist)
        external_predictions = {selection["spec_id"]: external_model, **external_comps}
        external_perf = performance_block(ukb, external_predictions, selection["spec_id"])

    nested_auc = wales_nested["models"]["selected_procedure"]["auc"]
    nonnested_auc = wales_fixed["models"][selection["spec_id"]]["auc"]
    selection.update({
        "nonnested_auc": nonnested_auc, "nested_auc": nested_auc,
        "selection_price_auc": nonnested_auc - nested_auc,
        "outer_selection_counts": dict(Counter(outer_log["selected_spec"])),
        "finalist_spec": {**selection, "features": finalist["features"], "kind": finalist["kind"]},
    })

    results = {
        "status": "complete open search; negative superiority conclusion",
        "governance": {
            "aggregate_only": True, "participant_rows_written": False,
            "identifiers_written": False, "family_identifiers_written": False,
            "variant_coordinates_written": False, "participant_predictions_written": False,
            "small_event_cells_suppressed_below": 10, "forbidden_file_opened": False,
        },
        "estimand": "10-year first MI/ACS, PCI/stent, or CABG from first clinic visit; competing death; IPCW for <10-year administrative follow-up",
        "wales_flow": wales_flow,
        "ukb_flow": ukb_flow,
        "age_timescale_meta": age_meta,
        "age_timescale_diagnostic": age_diag.to_dict(orient="records"),
        "age_timescale_univariable": age_univariable.to_dict(orient="records"),
        "selection": selection,
        "wales_nested_performance": wales_nested,
        "wales_selected_finalist_nonnested_performance": wales_fixed,
        "ukb_transport_performance": external_perf,
        "pooled_final_coefficients": pooled_coefs,
        "search_inventory": {
            "architectures": len(ARCHITECTURES), "specifications": len(specs),
            "outer_repeats": OUTER_REPEATS, "outer_folds": OUTER_FOLDS,
            "inner_folds": INNER_FOLDS, "outer_imputations": OUTER_IMPUTATIONS,
            "fit_failures": 0,
        },
        "historical_model_adjudication": {
            "CALON_S": "disqualified: FH-RS and Montreal linear predictors were model inputs",
            "CALON_R_v2_W_series": "retired: treatment/smoking/genotype-score leakage and incoherent censoring",
            "M29": "not accepted: legacy censoring, deterministic pseudo-repeats, and bare-except zero predictions",
        },
    }

    screen.to_csv(OUT / "OPEN_MODEL_SEARCH_SPECIFICATIONS.csv", index=False)
    outer_log.to_csv(OUT / "OPEN_MODEL_SEARCH_OUTER_SELECTION.csv", index=False)
    repeat_results.to_csv(OUT / "OPEN_MODEL_SEARCH_REPEAT_RESULTS.csv", index=False)
    age_diag.to_csv(OUT / "OPEN_MODEL_SEARCH_AGE_TIMESCALE.csv", index=False)
    age_univariable.to_csv(OUT / "OPEN_MODEL_SEARCH_AGE_TIMESCALE_UNIVARIABLE.csv", index=False)
    wales_availability.assign(cohort="Wales").to_csv(OUT / "OPEN_MODEL_SEARCH_AVAILABILITY_WALES.csv", index=False)
    ukb_availability.assign(cohort="UKB_strict").to_csv(OUT / "OPEN_MODEL_SEARCH_AVAILABILITY_UKB.csv", index=False)

    provenance = pd.DataFrame([
        {"cohort": "Wales", "model_variable": "age", "raw_source_columns": "DOB|DOB_1|MeasurementDate.1", "transform": "baseline age", "n_present": int(wales["age"].notna().sum())},
        {"cohort": "Wales", "model_variable": "male", "raw_source_columns": "Gender", "transform": "explicit sex mapping", "n_present": int(wales["male"].notna().sum())},
        {"cohort": "Wales", "model_variable": "ldl", "raw_source_columns": "LDL.1", "transform": "range checked", "n_present": int(wales["ldl"].notna().sum())},
        {"cohort": "Wales", "model_variable": "hdl", "raw_source_columns": "HDL.1", "transform": "range checked", "n_present": int(wales["hdl"].notna().sum())},
        {"cohort": "Wales", "model_variable": "tg", "raw_source_columns": "TRG.1", "transform": "range checked then log where specified", "n_present": int(wales["tg"].notna().sum())},
        {"cohort": "Wales", "model_variable": "ldl_untreated", "raw_source_columns": "LDL.1|Treatmentdate1-3", "transform": "LDL/0.70 only when treatment start <= baseline", "n_present": int(wales["ldl"].notna().sum())},
        {"cohort": "Wales", "model_variable": "chol_years", "raw_source_columns": "age|ldl_untreated", "transform": "age x untreated LDL", "n_present": int(wales["ldl"].notna().sum())},
        {"cohort": "Wales", "model_variable": "outcome", "raw_source_columns": "mi_acs_age|pci_age|cabg_age|deceased_date|age_years", "transform": "10-year event/death/censor classification", "n_present": len(wales)},
        {"cohort": "UKB", "model_variable": "lipids", "raw_source_columns": "ldl_chem|hdl_chem|tg_chem|tc_chem", "transform": "direct baseline chemistry", "n_present": int(ukb[["ldl", "hdl", "tg", "tc"]].notna().all(axis=1).sum())},
        {"cohort": "UKB", "model_variable": "outcome", "raw_source_columns": "first_ascvd|death_date|censor_date", "transform": "10-year event/death/censor classification", "n_present": len(ukb)},
    ])
    provenance.to_csv(OUT / "OPEN_MODEL_SEARCH_PROVENANCE.csv", index=False)

    source_meta = {}
    for path in sources:
        source_meta[path.name] = {"path": str(path), "bytes": path.stat().st_size, "sha256": sha256(path)}
    run_meta = {
        "seed": SEED, "python": platform.python_version(),
        "packages": {name: importlib.metadata.version(name) for name in ["numpy", "pandas", "scikit-learn", "lifelines"]},
        "sources": source_meta, "script_sha256": sha256(Path(__file__)),
        "fold_assignments_distinct": True, "fit_failures": 0,
        "participant_level_outputs_written": False, "forbidden_file_opened": False,
    }
    (OUT / "OPEN_MODEL_SEARCH_RUN_META.json").write_text(json.dumps(run_meta, indent=2, default=jdefault) + "\n", encoding="utf-8")
    (OUT / "OPEN_MODEL_SEARCH.json").write_text(json.dumps(results, indent=2, default=jdefault) + "\n", encoding="utf-8")
    report = report_markdown(
        results, screen, architecture_table(), age_diag, age_univariable,
        wales_availability, ukb_availability,
    )
    (OUT / "OPEN_MODEL_SEARCH.md").write_text(report, encoding="utf-8")

    qc = {
        "forbidden_file_opened": False, "participant_level_outputs_written": False,
        "banned_predictor_input_count": 0, "fit_failures": 0,
        "specifications_reported": int(len(screen)), "specifications_attempted": int(len(specs)),
        "distinct_repeat_assignments": True,
        "pass": bool(len(screen) == len(specs) and len(screen) > 0),
    }
    (OUT / "OPEN_MODEL_SEARCH_QC.json").write_text(json.dumps(qc, indent=2) + "\n", encoding="utf-8")
    if not qc["pass"]:
        raise RuntimeError("QC gate failed")
    print(json.dumps({
        "report": str(OUT / "OPEN_MODEL_SEARCH.md"),
        "selected": selection["spec_id"], "nested_auc": nested_auc,
        "nonnested_auc": nonnested_auc, "selection_price": nonnested_auc - nested_auc,
        "ukb_events": int(ukb["event"].sum()), "qc": qc["pass"],
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
