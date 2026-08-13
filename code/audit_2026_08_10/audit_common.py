#!/usr/bin/env python3
"""Independent, governance-safe helpers for the 2026-08-10 CALON-N audit.

This module reads participant-level sources only into memory.  It never prints or
writes participant rows, linkage keys, family labels, variant coordinates, HGVS
strings, or participant-level predictions.  Public functions return analytic
frames only to the calling process; only aggregate dictionaries are serialised.
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import warnings
from pathlib import Path
from typing import Any

import lifelines
import numpy as np
import pandas as pd
import scipy
import sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss, roc_auc_score
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs" / "audit_2026_08_10"
DRAGON_RAW = Path("${CALON_WALES_DATA}/FH_Dragon3 (1).csv")
CALLS_RAW = Path("${HOME}/Documents/calon_backup_data/ukb_fh_all_carriers.tsv")
PROHIBITED_RAW = Path("${CALON_WALES_DATA}/wales_clean_treatment_response.csv")

SEED = 20260810
PENALTIES = [0.01, 0.03, 0.10, 0.30, 1.00, 3.00]
CALON_N = ["age", "male", "hdl", "hypertension", "smoke_ever", "log_ratio", "log_apoa1"]
RAW_FEATURES = [
    "age", "male", "diabetes", "smoke_ever", "hypertension", "hdl", "ldl",
    "apob", "apoa1", "log_tghdl", "log_lpa", "lpa", "bmi", "treatment",
]
LOF_TERMS = {
    "stop_gained", "frameshift_variant", "splice_acceptor_variant",
    "splice_donor_variant", "start_lost",
}


def input_paths() -> dict[str, Path]:
    shared_value = os.environ.get("CALON_SHARED_MASTER")
    if not shared_value:
        raise RuntimeError("CALON_SHARED_MASTER is required")
    shared = Path(shared_value).expanduser().resolve()
    projects = shared.parent
    paths = {
        "dragon_clinic": DRAGON_RAW,
        "pass_linkage": shared / "PASS" / "pass_master.csv",
        "ukb_master": shared / "UKB" / "ukb_master.csv",
        "carrier_calls": CALLS_RAW,
        "clinvar_annotations": projects / "AlphaFold_SSS" / "data" / "analysis" / "ukb_clinvar_full.csv",
        "vep_annotations": projects / "AlphaFold_SSS" / "data" / "analysis" / "ukb_ldlr_vep_annotations.csv",
    }
    prohibited = PROHIBITED_RAW.resolve()
    for logical, path in paths.items():
        if path.resolve() == prohibited:
            raise RuntimeError(f"Prohibited source resolved for {logical}")
        if not path.is_file():
            raise FileNotFoundError(f"Missing required logical input: {logical}")
    return paths


def json_ready(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): json_ready(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(v) for v in value]
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        value = float(value)
    if isinstance(value, float):
        return value if np.isfinite(value) else None
    if isinstance(value, Path):
        return str(value)
    return value


def write_json(path: Path, payload: dict[str, Any]) -> None:
    """Create an output, or accept an identical existing deterministic output."""
    content = json.dumps(json_ready(payload), indent=2, sort_keys=True, allow_nan=False) + "\n"
    if path.exists():
        if path.read_text(encoding="utf-8") != content:
            raise FileExistsError(f"Refusing to overwrite a non-identical output: {path}")
        return
    path.write_text(content, encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    if not content.endswith("\n"):
        content += "\n"
    if path.exists():
        if path.read_text(encoding="utf-8") != content:
            raise FileExistsError(f"Refusing to overwrite a non-identical output: {path}")
        return
    path.write_text(content, encoding="utf-8")


def event_count(value: int) -> int | str:
    """Governance display rule for any cell defined by an event count."""
    n = int(value)
    return n if n >= 10 else "<10, non-estimable"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def environment_metadata() -> dict[str, Any]:
    return {
        "python": platform.python_version(),
        "pandas": pd.__version__,
        "numpy": np.__version__,
        "scikit_learn": sklearn.__version__,
        "scipy": scipy.__version__,
        "lifelines": lifelines.__version__,
        "seed_base": SEED,
    }


def num(frame: pd.DataFrame, name: str) -> pd.Series:
    if name not in frame:
        return pd.Series(np.nan, index=frame.index, dtype=float)
    return pd.to_numeric(frame[name], errors="coerce")


def bounded(series: pd.Series, low: float, high: float) -> pd.Series:
    return series.where(series.between(low, high))


def _normalise_key(values: pd.Series) -> pd.Series:
    return (
        values.astype("string").fillna("").str.strip().str.upper()
        .str.replace(r"\.0$", "", regex=True)
    )


def classify_clinvar(value: object) -> str:
    text = str(value).strip().lower()
    if text in {"", "nan", "none"}:
        return "NONE"
    tokens = {token.strip().replace(" ", "_") for token in text.split(",")}
    pathogenic = bool(tokens & {"pathogenic", "likely_pathogenic"})
    benign = bool(tokens & {"benign", "likely_benign"})
    uncertain = any("uncertain" in token for token in tokens)
    if pathogenic and benign:
        return "CONFLICT"
    if pathogenic:
        return "PLP"
    if uncertain:
        return "VUS"
    if benign:
        return "BLB"
    return "OTHER"


def has_lof(value: object) -> bool:
    terms = {part.strip() for part in str(value).lower().replace("&", ",").split(",")}
    return bool(terms & LOF_TERMS)


def _qualifying_components(
    annotated: pd.DataFrame,
    eligible: set[int],
    qualifying: pd.Series,
) -> dict[int, int]:
    """Connected carrier--variant components, retained only in memory."""
    coord = ["chrom", "pos", "ref", "alt"]
    edges = (
        annotated.loc[
            qualifying.fillna(False) & annotated["eid"].isin(eligible),
            ["eid"] + coord,
        ]
        .dropna(subset=["eid", "pos"])
        .drop_duplicates()
    )
    parent: dict[tuple[str, object], tuple[str, object]] = {}

    def find(node: tuple[str, object]) -> tuple[str, object]:
        parent.setdefault(node, node)
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    def union_nodes(a: tuple[str, object], b: tuple[str, object]) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for row in edges.itertuples(index=False):
        participant_node = ("p", int(row.eid))
        variant_node = ("v", (str(row.chrom), int(row.pos), str(row.ref), str(row.alt)))
        union_nodes(participant_node, variant_node)
    roots = {value: find(("p", int(value))) for value in sorted(eligible)}
    codes = {root: i for i, root in enumerate(sorted(set(roots.values()), key=repr))}
    return {value: codes[root] for value, root in roots.items()}


def build_dragon() -> pd.DataFrame:
    """Independently reconstruct the locked DRAGON analytic frame."""
    paths = input_paths()
    raw = pd.read_csv(paths["dragon_clinic"], low_memory=False)
    linkage = pd.read_csv(
        paths["pass_linkage"], usecols=["participant_id", "family_id"], dtype="string"
    )
    linkage["participant_key"] = _normalise_key(linkage["participant_id"])
    linkage["family_key"] = _normalise_key(linkage["family_id"])
    if linkage.loc[linkage["participant_key"].ne(""), "participant_key"].duplicated().any():
        raise RuntimeError("Non-unique linkage key in canonical family mapping")
    mapping = linkage.set_index("participant_key")["family_key"]
    direct_family = _normalise_key(raw["FamilyNumber"])
    canonical_family = _normalise_key(raw["DatabaseNumber"]).map(mapping)
    matched = canonical_family.notna() & canonical_family.ne("")
    family = canonical_family.where(matched, direct_family)
    missing = family.eq("")
    family.loc[missing] = "INTERNAL_ROW_" + pd.Series(np.arange(len(raw)), index=raw.index).astype(str)

    x = pd.DataFrame(index=raw.index)
    x["age"] = bounded(num(raw, "Currentage"), 5, 105)
    x["male"] = raw["Gender"].astype("string").str.strip().str.upper().eq("M").astype(float)
    diabetes = num(raw, "Diabetes_binary")
    smoking = num(raw, "Smoking_binary")
    x["diabetes"] = diabetes.gt(0).astype(float).where(diabetes.notna())
    x["smoke_ever"] = smoking.gt(0).astype(float).where(smoking.notna())
    sbp = bounded(num(raw, "BloodPressureSystolic"), 70, 260)
    dbp = bounded(num(raw, "BloodPressureDiastolic"), 35, 160)
    bp_medication_raw = num(raw, "BloodPressureMedication")
    observed_bp = sbp.notna() | dbp.notna() | bp_medication_raw.notna()
    x["hypertension"] = (
        sbp.ge(140) | dbp.ge(90) | bp_medication_raw.gt(0)
    ).astype(float).where(observed_bp)
    x["ldl"] = bounded(num(raw, "MtachedLDLC"), 0.3, 20)
    x["hdl"] = bounded(num(raw, "LastHDL").fillna(num(raw, "HDL_1")), 0.2, 5)
    triglyceride = bounded(num(raw, "LastTrigs").fillna(num(raw, "TRG_1")), 0.2, 25)
    x["apob"] = bounded(num(raw, "ApoB"), 0.2, 4)
    x["apoa1"] = bounded(num(raw, "ApoA1"), 0.3, 4)
    x["lpa"] = bounded(num(raw, "Lpa"), 0, 1000)
    x["log_tghdl"] = np.log((triglyceride / x["hdl"]).where(lambda z: z.gt(0)))
    x["log_lpa"] = np.log1p(x["lpa"])
    x["treatment"] = num(raw, "OnTreatment").fillna(0).gt(0).astype(float)
    x["bmi"] = np.nan
    x["y"] = num(raw, "ASCVD_combined").fillna(0).gt(0).astype(int)
    x["cluster"] = family.to_numpy()
    if len(x) != 424 or int(x["y"].sum()) != 62:
        raise RuntimeError("DRAGON invariant failed")
    return x.reset_index(drop=True)


def build_ukb() -> tuple[pd.DataFrame, dict[str, Any]]:
    """Independently reconstruct the strict and union carrier frames."""
    paths = input_paths()
    clinvar = pd.read_csv(paths["clinvar_annotations"], low_memory=False)
    vep = pd.read_csv(paths["vep_annotations"], low_memory=False)
    calls = pd.read_csv(paths["carrier_calls"], sep="\t", low_memory=False).rename(
        columns={"CHROM": "chrom", "POS": "pos", "REF": "ref", "ALT": "alt", "EID": "eid"}
    )
    coord = ["chrom", "pos", "ref", "alt"]
    for frame in (clinvar, vep, calls):
        frame["chrom"] = frame["chrom"].astype(str).str.replace("chr", "", regex=False)
        frame["pos"] = pd.to_numeric(frame["pos"], errors="coerce")
        frame["ref"] = frame["ref"].astype(str).str.upper()
        frame["alt"] = frame["alt"].astype(str).str.upper()
    calls["eid"] = pd.to_numeric(calls["eid"], errors="coerce").astype("Int64")
    clinvar["class"] = clinvar["clinvar"].map(classify_clinvar)
    clinvar["lof_cv"] = clinvar["consequence"].map(has_lof)
    vep["lof_vep"] = vep["consequence"].map(has_lof)
    clinvar_unique = clinvar.drop_duplicates(coord)
    vep_unique = vep.drop_duplicates(coord)
    annotated = calls.merge(
        clinvar_unique[coord + ["class", "lof_cv"]], on=coord, how="left"
    ).merge(vep_unique[coord + ["lof_vep"]], on=coord, how="left")

    plp = set(annotated.loc[annotated["class"].eq("PLP"), "eid"].dropna().astype(int))
    conflict = set(annotated.loc[annotated["class"].eq("CONFLICT"), "eid"].dropna().astype(int))
    strict = plp - conflict
    lof_cv = set(annotated.loc[annotated["lof_cv"].fillna(False), "eid"].dropna().astype(int))
    lof_vep = set(annotated.loc[annotated["lof_vep"].fillna(False), "eid"].dropna().astype(int))
    lof = lof_cv | lof_vep
    union = strict | lof

    strict_components = _qualifying_components(
        annotated,
        strict,
        annotated["eid"].isin(strict) & annotated["class"].eq("PLP"),
    )
    union_components = _qualifying_components(
        annotated,
        union,
        annotated["eid"].isin(union)
        & (
            (annotated["eid"].isin(strict) & annotated["class"].eq("PLP"))
            | annotated["lof_cv"].fillna(False)
            | annotated["lof_vep"].fillna(False)
        ),
    )

    use = [
        "eid", "ldlr_carrier", "prevalent_ascvd", "age_exact_baseline", "age_at_recruit",
        "sex_F", "diabetes_combined", "smoking_ever", "sbp", "dbp", "pre_tc", "tc_chem",
        "pre_ldl", "ldl_chem", "pre_hdl", "hdl_chem", "pre_tg", "tg_chem", "apob",
        "apob_chem", "apo_a1", "pre_lpa", "lpa_chem", "on_statin_self", "bmi_direct",
    ]
    raw = pd.read_csv(paths["ukb_master"], usecols=use, low_memory=False)
    raw["eid"] = pd.to_numeric(raw["eid"], errors="coerce").astype("Int64")
    raw = raw[num(raw, "ldlr_carrier").eq(1) & raw["eid"].isin(union)].copy().reset_index(drop=True)
    x = pd.DataFrame(index=raw.index)
    x["age"] = bounded(num(raw, "age_exact_baseline").fillna(num(raw, "age_at_recruit")), 5, 105)
    x["male"] = 1 - num(raw, "sex_F").fillna(0)
    diabetes = num(raw, "diabetes_combined")
    smoking = num(raw, "smoking_ever")
    x["diabetes"] = diabetes.gt(0).astype(float).where(diabetes.notna())
    x["smoke_ever"] = smoking.gt(0).astype(float).where(smoking.notna())
    sbp = bounded(num(raw, "sbp"), 70, 260)
    dbp = bounded(num(raw, "dbp"), 35, 160)
    x["hypertension"] = (sbp.ge(140) | dbp.ge(90)).astype(float).where(sbp.notna() | dbp.notna())
    total_cholesterol = bounded(num(raw, "pre_tc").fillna(num(raw, "tc_chem")), 1.5, 25)
    x["ldl"] = bounded(num(raw, "pre_ldl").fillna(num(raw, "ldl_chem")), 0.3, 20)
    x["hdl"] = bounded(num(raw, "pre_hdl").fillna(num(raw, "hdl_chem")), 0.2, 5)
    triglyceride = bounded(num(raw, "pre_tg").fillna(num(raw, "tg_chem")), 0.2, 25)
    x["apob"] = bounded(num(raw, "apob").fillna(num(raw, "apob_chem")), 0.2, 4)
    x["apoa1"] = bounded(num(raw, "apo_a1"), 0.3, 4)
    x["lpa"] = bounded(num(raw, "pre_lpa").fillna(num(raw, "lpa_chem")), 0, 1000)
    x["log_tghdl"] = np.log((triglyceride / x["hdl"]).where(lambda z: z.gt(0)))
    x["log_lpa"] = np.log1p(x["lpa"])
    x["treatment"] = num(raw, "on_statin_self").fillna(0).gt(0).astype(float)
    x["bmi"] = bounded(num(raw, "bmi_direct"), 12, 70)
    x["y"] = num(raw, "prevalent_ascvd").fillna(0).gt(0).astype(int)
    x["strict"] = raw["eid"].isin(strict).astype(int)
    x["plp_any"] = raw["eid"].isin(plp).astype(int)
    x["lof_cv"] = raw["eid"].isin(lof_cv).astype(int)
    x["lof_vep"] = raw["eid"].isin(lof_vep).astype(int)
    x["cluster_strict"] = raw["eid"].map(strict_components).to_numpy()
    x["cluster_union"] = raw["eid"].map(union_components).to_numpy()
    x["cluster"] = x["cluster_union"]

    strict_rows = x["strict"].eq(1)
    if (
        len(x) != 1264
        or int(x["y"].sum()) != 80
        or int(strict_rows.sum()) != 890
        or int(x.loc[strict_rows, "y"].sum()) != 57
    ):
        raise RuntimeError("UKB carrier invariants failed")
    set_audit = {
        "strict_definition_n": len(strict),
        "union_definition_n": len(union),
        "added_definition_n": len(union - strict),
        "added_without_any_plp_assertion_n": len((union - strict) - plp),
        "added_with_plp_but_conflict_excluded_n": len((union - strict) & plp),
        "added_flagged_by_clinvar_consequence_n": len((union - strict) & lof_cv),
        "added_flagged_by_vep_consequence_n": len((union - strict) & lof_vep),
    }
    return x.reset_index(drop=True), set_audit


def source_defaults(train: pd.DataFrame) -> dict[str, float]:
    defaults: dict[str, float] = {}
    for column in RAW_FEATURES:
        value = float(pd.to_numeric(train[column], errors="coerce").median())
        if not np.isfinite(value):
            value = 27.0 if column == "bmi" else 0.0
        defaults[column] = value
    return defaults


def fill_raw(frame: pd.DataFrame, defaults: dict[str, float]) -> pd.DataFrame:
    q = pd.DataFrame(index=frame.index)
    for column in RAW_FEATURES:
        q[column] = pd.to_numeric(frame[column], errors="coerce").fillna(defaults[column]).astype(float)
    for column in ["male", "diabetes", "smoke_ever", "hypertension", "treatment"]:
        q[column] = q[column].clip(0, 1)
    q["age"] = q["age"].clip(5, 105)
    q["ldl"] = q["ldl"].clip(0.3, 20)
    q["hdl"] = q["hdl"].clip(0.2, 5)
    q["apob"] = q["apob"].clip(0.2, 4)
    q["apoa1"] = q["apoa1"].clip(0.3, 4)
    q["lpa"] = q["lpa"].clip(0, 1000)
    q["bmi"] = q["bmi"].clip(12, 70)
    return q


def fit_preprocessor(train: pd.DataFrame) -> dict[str, Any]:
    defaults = source_defaults(train)
    q = fill_raw(train, defaults)
    observed = train["ldl"].notna() & train["apob"].notna()
    if int(observed.sum()) < 30:
        raise RuntimeError("Too few jointly observed lipid values")
    log_ldl = np.log(train.loc[observed, "ldl"].astype(float).clip(0.3, 20)).to_numpy()
    log_apob = np.log(train.loc[observed, "apob"].astype(float).clip(0.2, 4)).to_numpy()
    slope, intercept = np.polyfit(log_ldl, log_apob, 1)
    return {
        "defaults": defaults,
        "age_mean": float(q["age"].mean()),
        "age_sd": float(q["age"].std(ddof=0)),
        "hdl_mean": float(q["hdl"].mean()),
        "hdl_sd": float(q["hdl"].std(ddof=0)),
        "discordance_intercept": float(intercept),
        "discordance_slope": float(slope),
    }


def fhrs_lp(frame: pd.DataFrame) -> np.ndarray:
    age = frame["age"].to_numpy(float)
    ldl = frame["ldl"].to_numpy(float)
    hdl = frame["hdl"].to_numpy(float)
    age_term = np.select(
        [age <= 30, age <= 35, age <= 40, age <= 45, age <= 50, age <= 55, age <= 60],
        [0, 0.938, 1.383, 1.621, 1.738, 1.804, 1.964],
        default=2.256,
    )
    ldl_term = np.select(
        [ldl <= 5.5, ldl <= 7.5, ldl <= 8.5, ldl <= 9.5],
        [0, 0.315, 0.718, 0.918],
        default=1.136,
    )
    hdl_term = np.select([hdl > 1.30, hdl >= 1.01, hdl >= 0.85], [0, 0.298, 0.712], default=0.752)
    return (
        age_term + ldl_term + hdl_term + 0.721 * frame["male"].to_numpy()
        + 0.644 * frame["hypertension"].to_numpy()
        + 0.625 * frame["smoke_ever"].to_numpy()
        + 0.434 * (frame["lpa"].to_numpy() >= 105)
    )


def safeheart_risk(frame: pd.DataFrame) -> np.ndarray:
    age = frame["age"].to_numpy()
    bmi = frame["bmi"].to_numpy()
    ldl_mg = frame["ldl"].to_numpy() * 38.67
    lp = (
        0.70 * frame["male"].to_numpy()
        + 1.07 * ((age >= 30) & (age < 60))
        + 1.45 * (age >= 60)
        + 0.69 * frame["hypertension"].to_numpy()
        + 0.48 * frame["smoke_ever"].to_numpy()
        + 0.88 * ((bmi >= 25) & (bmi < 30))
        + 0.98 * (bmi >= 30)
        + 0.92 * ((ldl_mg >= 100) & (ldl_mg < 160))
        + 1.57 * (ldl_mg >= 160)
        + 0.42 * (frame["lpa"].to_numpy() > 125)
    )
    return 1 - np.power(0.9025, np.exp(lp - 5.4078))


def transform(frame: pd.DataFrame, prep: dict[str, Any]) -> pd.DataFrame:
    q = fill_raw(frame, prep["defaults"])
    z = pd.DataFrame(index=q.index)
    z["age"] = q["age"]
    z["male"] = q["male"]
    z["hdl"] = q["hdl"]
    z["hypertension"] = q["hypertension"]
    z["smoke_ever"] = q["smoke_ever"]
    z["log_ratio"] = np.log(q["apob"]) - np.log(q["ldl"])
    z["log_apoa1"] = np.log(q["apoa1"])
    z["montreal"] = (
        0.75 * (q["age"] - prep["age_mean"]) / max(prep["age_sd"], 1e-6)
        - 0.27 * (q["hdl"] - prep["hdl_mean"]) / max(prep["hdl_sd"], 1e-6)
        + 0.25 * q["male"] + 0.19 * q["hypertension"] + 0.12 * q["smoke_ever"]
    )
    z["fhrs"] = fhrs_lp(q)
    z["safeheart"] = safeheart_risk(q)
    return z


def fit_bundle(train: pd.DataFrame, columns: list[str], penalty: float) -> dict[str, Any]:
    prep = fit_preprocessor(train)
    z = transform(train, prep)
    scaler = StandardScaler().fit(z[columns])
    model = LogisticRegression(
        C=penalty, penalty="l2", solver="lbfgs", max_iter=5000, random_state=SEED
    )
    model.fit(scaler.transform(z[columns]), train["y"].to_numpy(int))
    return {"columns": columns, "preprocessor": prep, "scaler": scaler, "model": model}


def predict_bundle(bundle: dict[str, Any], target: pd.DataFrame) -> np.ndarray:
    z = transform(target, bundle["preprocessor"])
    return bundle["model"].predict_proba(bundle["scaler"].transform(z[bundle["columns"]]))[:, 1]


def choose_penalty(
    train: pd.DataFrame,
    columns: list[str],
    seed: int,
    n_splits: int = 5,
) -> tuple[float, list[dict[str, float]]]:
    y = train["y"].to_numpy(int)
    groups = train["cluster"].to_numpy()
    splitter = StratifiedGroupKFold(n_splits=n_splits, shuffle=True, random_state=seed)
    rows: list[dict[str, float]] = []
    for penalty in PENALTIES:
        prediction = np.full(len(train), np.nan)
        for train_index, validation_index in splitter.split(np.zeros(len(y)), y, groups):
            bundle = fit_bundle(train.iloc[train_index], columns, penalty)
            prediction[validation_index] = predict_bundle(bundle, train.iloc[validation_index])
        rows.append({
            "C": penalty,
            "brier": float(brier_score_loss(y, prediction)),
            "auc": float(roc_auc_score(y, prediction)),
        })
    rows.sort(key=lambda value: (value["brier"], value["C"]))
    return float(rows[0]["C"]), rows


def transport(
    source: pd.DataFrame,
    target: pd.DataFrame,
    columns: list[str],
    seed: int,
) -> dict[str, Any]:
    penalty, tuning = choose_penalty(source, columns, seed)
    bundle = fit_bundle(source, columns, penalty)
    prediction = predict_bundle(bundle, target)
    return {
        "penalty": penalty,
        "tuning": tuning,
        "bundle": bundle,
        "prediction": prediction,
        "auc": float(roc_auc_score(target["y"], prediction)),
        "brier": float(brier_score_loss(target["y"], prediction)),
    }


def source_comparators(source: pd.DataFrame, target: pd.DataFrame) -> dict[str, np.ndarray]:
    prep = fit_preprocessor(source)
    z = transform(target, prep)
    return {
        "Montreal_adapted": z["montreal"].to_numpy(),
        "FH_Risk_Score_adapted": z["fhrs"].to_numpy(),
        "SAFEHEART_adapted": z["safeheart"].to_numpy(),
    }


def expected_observed(y: np.ndarray, prediction: np.ndarray) -> float:
    return float(np.asarray(prediction, float).sum() / max(np.asarray(y, int).sum(), 1))


def metric_block(
    y: np.ndarray,
    primary: np.ndarray,
    groups: np.ndarray,
    comparators: dict[str, np.ndarray],
    seed: int,
    bootstrap: int = 4000,
) -> dict[str, Any]:
    rng = np.random.default_rng(seed)
    levels = pd.unique(groups)
    members = {group: np.flatnonzero(groups == group) for group in levels}
    auc_samples: list[float] = []
    delta_samples = {name: [] for name in comparators}
    for _ in range(bootstrap):
        draw = rng.choice(levels, size=len(levels), replace=True)
        index = np.concatenate([members[group] for group in draw])
        if np.unique(y[index]).size < 2:
            continue
        primary_auc = roc_auc_score(y[index], primary[index])
        auc_samples.append(primary_auc)
        for name, prediction in comparators.items():
            delta_samples[name].append(
                primary_auc - roc_auc_score(y[index], prediction[index])
            )
    primary_auc = float(roc_auc_score(y, primary))
    result = {
        "auc": primary_auc,
        "auc_ci": [float(v) for v in np.percentile(auc_samples, [2.5, 97.5])],
        "e_o": expected_observed(y, primary),
        "comparators": {},
        "bootstrap_replicates": bootstrap,
    }
    for name, prediction in comparators.items():
        comparator_auc = float(roc_auc_score(y, prediction))
        comparator_eo = (
            expected_observed(y, prediction)
            if name in {"age_sex", "SAFEHEART_adapted"}
            else None
        )
        result["comparators"][name] = {
            "auc": comparator_auc,
            "delta_calon_minus_comparator": primary_auc - comparator_auc,
            "delta_ci": [float(v) for v in np.percentile(delta_samples[name], [2.5, 97.5])],
            "e_o": comparator_eo,
            "e_o_status": (
                "estimable_probability"
                if comparator_eo is not None
                else "not_estimable_ranking_score_not_probability"
            ),
        }
    return result


def paired_auc_delta(
    y: np.ndarray,
    first: np.ndarray,
    second: np.ndarray,
    groups: np.ndarray,
    seed: int,
    bootstrap: int = 4000,
) -> dict[str, Any]:
    point = float(roc_auc_score(y, first) - roc_auc_score(y, second))
    rng = np.random.default_rng(seed)
    levels = pd.unique(groups)
    members = {group: np.flatnonzero(groups == group) for group in levels}
    values: list[float] = []
    for _ in range(bootstrap):
        draw = rng.choice(levels, size=len(levels), replace=True)
        index = np.concatenate([members[group] for group in draw])
        if np.unique(y[index]).size < 2:
            continue
        values.append(
            roc_auc_score(y[index], first[index]) - roc_auc_score(y[index], second[index])
        )
    return {
        "delta": point,
        "ci": [float(v) for v in np.percentile(values, [2.5, 97.5])],
        "bootstrap_replicates": bootstrap,
    }


def nested_subset_auc_delta(
    y: np.ndarray,
    prediction: np.ndarray,
    subset: np.ndarray,
    groups: np.ndarray,
    seed: int,
    bootstrap: int = 4000,
) -> dict[str, Any]:
    point = float(
        roc_auc_score(y, prediction) - roc_auc_score(y[subset], prediction[subset])
    )
    rng = np.random.default_rng(seed)
    levels = pd.unique(groups)
    members = {group: np.flatnonzero(groups == group) for group in levels}
    values: list[float] = []
    for _ in range(bootstrap):
        draw = rng.choice(levels, size=len(levels), replace=True)
        index = np.concatenate([members[group] for group in draw])
        subset_index = index[subset[index]]
        if np.unique(y[index]).size < 2 or np.unique(y[subset_index]).size < 2:
            continue
        values.append(
            roc_auc_score(y[index], prediction[index])
            - roc_auc_score(y[subset_index], prediction[subset_index])
        )
    return {
        "delta_union_target_minus_strict_subset": point,
        "ci": [float(v) for v in np.percentile(values, [2.5, 97.5])],
        "bootstrap_replicates": bootstrap,
    }
