#!/usr/bin/env python3
"""Locked CALON-DISC multi-cohort cross-sectional analysis.

SUPERSEDED - RETAINED FOR PROVENANCE ONLY. DO NOT REUSE THIS DESIGN.

Two reasons this script must not be treated as current:

1. It violates the programme's binding modelling rule. `CANDIDATES` below feeds
   published risk scores into a fitted model as features - `montreal` in seven
   of nine candidates, and `score_stack_disc` stacking `montreal` and `fhrs`
   together. No published score, no prior model from this programme, and no
   linear predictor derived from either may be a feature. Published scores are
   comparators, never inputs.

2. The estimand is cross-sectional (established/prevalent ASCVD), so a
   predictor measured after the event can enter the fit. That is how the
   temporal leakage documented elsewhere in this repository arose.

The current model is code/15_CALON_FINAL.py: raw variables only, incident
design in both cohorts, so leakage is structurally impossible rather than
merely tested for.

Writes aggregate/model outputs only. Participant identifiers, family/variant
labels, participant rows, and participant-level predictions are never written.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.special import expit
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss, roc_auc_score
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.preprocessing import StandardScaler

ROOT = Path("${CALON_PROJECT_ROOT}")
SOURCE = Path("${CALON_HOME}/dragon_plp_full_rebuild_2026_08_08")
OUT = ROOT / "outputs"
MODEL = ROOT / "model"
FIG = ROOT / "figures"
SEED = 20260809
PENALTIES = [0.01, 0.03, 0.10, 0.30, 1.00, 3.00]
BOOT = 4000

for path in [OUT, MODEL, FIG]:
    path.mkdir(parents=True, exist_ok=True)

spec = importlib.util.spec_from_file_location("dragon_engine", SOURCE / "code" / "01_dragon_model_rebuild.py")
if spec is None or spec.loader is None:
    raise RuntimeError("Could not import canonical DRAGON/UKB construction engine")
e = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = e
spec.loader.exec_module(e)

RAW = [
    "age", "male", "diabetes", "smoke_ever", "hypertension", "hdl", "ldl",
    "apob", "apoa1", "log_tghdl", "log_lpa", "lpa", "bmi", "treatment",
]

CANDIDATES = {
    "age_sex": ["age", "male"],
    "montreal": ["montreal"],
    "montreal_ldl": ["montreal", "log_ldl"],
    "montreal_apob": ["montreal", "log_apob"],
    "montreal_ratio": ["montreal", "log_ratio"],
    "calon_disc_core": ["montreal", "log_ldl", "discordance"],
    "calon_disc_tghdl": ["montreal", "log_ldl", "discordance", "log_tghdl"],
    "calon_disc_lpa": ["montreal", "log_ldl", "discordance", "log_lpa"],
    "score_stack_disc": ["montreal", "fhrs", "log_ldl", "discordance"],
}

EXPECTED_POSITIVE = {
    "age", "male", "montreal", "log_ldl", "log_apob", "log_ratio",
    "discordance", "log_tghdl", "log_lpa", "fhrs",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def prepare_cohorts() -> dict[str, pd.DataFrame]:
    dragon, _ = e.build_dragon()
    ukb, _ = e.build_ukb()
    dragon = dragon.copy()
    dragon["y"] = dragon["y_flag"].astype(int)
    dragon["cluster"] = dragon["family"]
    dragon["bmi"] = np.nan
    strict = ukb.loc[ukb["strict"].eq(1)].copy().reset_index(drop=True)
    strict["cluster"] = strict["cluster_strict"]
    union = ukb.copy().reset_index(drop=True)
    union["cluster"] = union["cluster_union"]
    for d in [dragon, strict, union]:
        for c in RAW:
            if c not in d:
                d[c] = np.nan
    return {"dragon": dragon.reset_index(drop=True), "ukb_strict": strict, "ukb_union": union}


def source_defaults(train: pd.DataFrame) -> dict[str, float]:
    defaults = {}
    for c in RAW:
        value = float(pd.to_numeric(train[c], errors="coerce").median())
        if not np.isfinite(value):
            value = 27.0 if c == "bmi" else 0.0
        defaults[c] = value
    return defaults


def fill_raw(frame: pd.DataFrame, defaults: dict[str, float]) -> pd.DataFrame:
    q = pd.DataFrame(index=frame.index)
    for c in RAW:
        q[c] = pd.to_numeric(frame[c], errors="coerce").fillna(defaults[c]).astype(float)
    for c in ["male", "diabetes", "smoke_ever", "hypertension", "treatment"]:
        q[c] = q[c].clip(0, 1)
    q["age"] = q["age"].clip(5, 105)
    q["ldl"] = q["ldl"].clip(0.3, 20)
    q["hdl"] = q["hdl"].clip(0.2, 5)
    q["apob"] = q["apob"].clip(0.2, 4)
    q["apoa1"] = q["apoa1"].clip(0.3, 4)
    q["lpa"] = q["lpa"].clip(0, 1000)
    q["bmi"] = q["bmi"].clip(12, 70)
    return q


def fit_preprocessor(train: pd.DataFrame) -> dict:
    defaults = source_defaults(train)
    q = fill_raw(train, defaults)
    observed = train["ldl"].notna() & train["apob"].notna()
    if int(observed.sum()) < 30:
        raise RuntimeError("Too few jointly observed apoB/LDL measurements")
    x = np.log(train.loc[observed, "ldl"].astype(float).clip(0.3, 20)).to_numpy()
    y = np.log(train.loc[observed, "apob"].astype(float).clip(0.2, 4)).to_numpy()
    slope, intercept = np.polyfit(x, y, 1)
    return {
        "defaults": defaults,
        "age_mean": float(q["age"].mean()),
        "age_sd": float(q["age"].std(ddof=0)),
        "hdl_mean": float(q["hdl"].mean()),
        "hdl_sd": float(q["hdl"].std(ddof=0)),
        "discordance_intercept": float(intercept),
        "discordance_slope": float(slope),
    }


def transform(frame: pd.DataFrame, prep: dict) -> pd.DataFrame:
    q = fill_raw(frame, prep["defaults"])
    z = pd.DataFrame(index=q.index)
    z["age"] = q["age"]
    z["male"] = q["male"]
    z["hdl"] = q["hdl"]
    z["hypertension"] = q["hypertension"]
    z["smoke_ever"] = q["smoke_ever"]
    z["diabetes"] = q["diabetes"]
    z["log_ldl"] = np.log(q["ldl"])
    z["log_apob"] = np.log(q["apob"])
    z["log_ratio"] = z["log_apob"] - z["log_ldl"]
    z["discordance"] = z["log_apob"] - (
        prep["discordance_intercept"] + prep["discordance_slope"] * z["log_ldl"]
    )
    z["log_tghdl"] = q["log_tghdl"]
    z["log_lpa"] = q["log_lpa"]
    z["log_apoa1"] = np.log(q["apoa1"])
    z["montreal"] = (
        0.75 * (q["age"] - prep["age_mean"]) / max(prep["age_sd"], 1e-6)
        - 0.27 * (q["hdl"] - prep["hdl_mean"]) / max(prep["hdl_sd"], 1e-6)
        + 0.25 * q["male"] + 0.19 * q["hypertension"] + 0.12 * q["smoke_ever"]
    )
    f = pd.DataFrame({
        "age": q["age"], "male": q["male"], "ldl": q["ldl"], "hdl": q["hdl"],
        "lpa": q["lpa"], "hypertension": q["hypertension"], "smoke_ever": q["smoke_ever"],
    })
    z["fhrs"] = e.fhrs_lp(f)
    z["safeheart"] = e.safeheart_risk(pd.DataFrame({
        "age": q["age"], "male": q["male"], "hypertension": q["hypertension"],
        "smoke_ever": q["smoke_ever"], "bmi": q["bmi"], "ldl": q["ldl"], "lpa": q["lpa"],
    }))
    return z


def fit_candidate(train: pd.DataFrame, candidate: str, penalty: float) -> dict:
    prep = fit_preprocessor(train)
    z = transform(train, prep)
    cols = CANDIDATES[candidate]
    scaler = StandardScaler().fit(z[cols])
    model = LogisticRegression(C=penalty, penalty="l2", solver="lbfgs", max_iter=5000, random_state=SEED)
    model.fit(scaler.transform(z[cols]), train["y"].to_numpy(int))
    return {"candidate": candidate, "columns": cols, "penalty_C": penalty,
            "preprocessor": prep, "scaler": scaler, "model": model}


def predict_candidate(bundle: dict, frame: pd.DataFrame) -> np.ndarray:
    z = transform(frame, bundle["preprocessor"])
    return bundle["model"].predict_proba(bundle["scaler"].transform(z[bundle["columns"]]))[:, 1]


def choose_penalty(train: pd.DataFrame, candidate: str, seed: int, n_splits: int = 5) -> tuple[float, pd.DataFrame]:
    y = train["y"].to_numpy(int)
    groups = train["cluster"].to_numpy()
    splitter = StratifiedGroupKFold(n_splits=n_splits, shuffle=True, random_state=seed)
    rows = []
    for c in PENALTIES:
        pred = np.full(len(train), np.nan)
        for tr, va in splitter.split(np.zeros(len(y)), y, groups):
            bundle = fit_candidate(train.iloc[tr], candidate, c)
            pred[va] = predict_candidate(bundle, train.iloc[va])
        rows.append({"candidate": candidate, "C": c, "brier": brier_score_loss(y, pred),
                     "auc": roc_auc_score(y, pred)})
    table = pd.DataFrame(rows).sort_values(["brier", "C"], ascending=[True, True])
    return float(table.iloc[0]["C"]), table


def transport(source: pd.DataFrame, target: pd.DataFrame, candidate: str, seed: int) -> dict:
    penalty, tuning = choose_penalty(source, candidate, seed)
    bundle = fit_candidate(source, candidate, penalty)
    pred = predict_candidate(bundle, target)
    return {"penalty": penalty, "tuning": tuning, "bundle": bundle, "prediction": pred,
            "auc": float(roc_auc_score(target["y"], pred)),
            "brier": float(brier_score_loss(target["y"], pred))}


def nested_oof(frame: pd.DataFrame, candidate: str, repeats: int = 5) -> tuple[np.ndarray, list[float]]:
    y = frame["y"].to_numpy(int)
    groups = frame["cluster"].to_numpy()
    ranks = np.zeros(len(frame), float)
    repeat_aucs = []
    for r in range(repeats):
        outer = StratifiedGroupKFold(5, shuffle=True, random_state=SEED + 1000 + r)
        pred = np.full(len(frame), np.nan)
        for fold, (tr, va) in enumerate(outer.split(np.zeros(len(y)), y, groups)):
            penalty, _ = choose_penalty(frame.iloc[tr], candidate, SEED + 2000 + r * 100 + fold, n_splits=4)
            bundle = fit_candidate(frame.iloc[tr], candidate, penalty)
            pred[va] = predict_candidate(bundle, frame.iloc[va])
        repeat_aucs.append(float(roc_auc_score(y, pred)))
        ranks += pd.Series(pred).rank(method="average").to_numpy()
    return ranks / repeats, repeat_aucs


def cluster_boot_metrics(y: np.ndarray, pred: np.ndarray, groups: np.ndarray,
                         comparators: dict[str, np.ndarray], seed: int) -> dict:
    rng = np.random.default_rng(seed)
    levels = pd.unique(groups)
    members = {g: np.flatnonzero(groups == g) for g in levels}
    aucs = []
    deltas = {name: [] for name in comparators}
    for _ in range(BOOT):
        draw = rng.choice(levels, size=len(levels), replace=True)
        idx = np.concatenate([members[g] for g in draw])
        if np.unique(y[idx]).size < 2:
            continue
        a = roc_auc_score(y[idx], pred[idx])
        aucs.append(a)
        for name, cp in comparators.items():
            deltas[name].append(a - roc_auc_score(y[idx], cp[idx]))
    result = {"auc": float(roc_auc_score(y, pred)),
              "auc_ci": [float(v) for v in np.percentile(aucs, [2.5, 97.5])], "comparators": {}}
    for name, cp in comparators.items():
        vals = deltas[name]
        result["comparators"][name] = {
            "auc": float(roc_auc_score(y, cp)),
            "delta": float(roc_auc_score(y, pred) - roc_auc_score(y, cp)),
            "delta_ci": [float(v) for v in np.percentile(vals, [2.5, 97.5])],
        }
    return result


def calibration(y: np.ndarray, p: np.ndarray) -> dict[str, float]:
    p = np.clip(p, 1e-6, 1 - 1e-6)
    lp = np.log(p / (1 - p)).reshape(-1, 1)
    model = LogisticRegression(penalty=None, solver="lbfgs", max_iter=5000).fit(lp, y)
    return {"brier": float(brier_score_loss(y, p)),
            "intercept": float(model.intercept_[0]), "slope": float(model.coef_[0, 0]),
            "expected_observed_ratio": float(p.sum() / max(y.sum(), 1))}


def source_comparators(source: pd.DataFrame, target: pd.DataFrame) -> dict[str, np.ndarray]:
    prep = fit_preprocessor(source)
    z = transform(target, prep)
    return {"age_sex": z["age"].to_numpy() + 8.0 * z["male"].to_numpy(),
            "Montreal_adapted": z["montreal"].to_numpy(),
            "FH_Risk_Score_adapted": z["fhrs"].to_numpy(),
            "SAFEHEART_adapted": z["safeheart"].to_numpy()}


def decision_curve(y: np.ndarray, predictions: dict[str, np.ndarray], thresholds: list[float]) -> list[dict]:
    rows = []
    n = len(y)
    for t in thresholds:
        for name, p in predictions.items():
            positive = p >= t
            tp = int(((y == 1) & positive).sum())
            fp = int(((y == 0) & positive).sum())
            rows.append({"threshold": t, "model": name,
                         "net_benefit": tp / n - fp / n * t / (1 - t)})
        rows.append({"threshold": t, "model": "refer_none", "net_benefit": 0.0})
        rows.append({"threshold": t, "model": "refer_all",
                     "net_benefit": y.mean() - (1 - y.mean()) * t / (1 - t)})
    return rows


def subgroup_rows(cohort: str, frame: pd.DataFrame, primary: np.ndarray,
                  comparators: dict[str, np.ndarray]) -> list[dict]:
    age_median = float(frame["age"].median())
    masks = {
        "male": frame["male"].eq(1), "female": frame["male"].eq(0),
        "age_below_median": frame["age"].lt(age_median),
        "age_at_or_above_median": frame["age"].ge(age_median),
        "treated": frame["treatment"].eq(1), "untreated": frame["treatment"].eq(0),
        "diabetes": frame["diabetes"].eq(1), "no_diabetes": frame["diabetes"].eq(0),
        "lpa_high143": frame["lpa"].ge(143), "lpa_below143": frame["lpa"].lt(143),
    }
    y = frame["y"].to_numpy(int)
    rows = []
    for subgroup, mask in masks.items():
        idx = mask.fillna(False).to_numpy()
        events = int(y[idx].sum())
        status = "non_estimable" if events < 10 else ("descriptive" if events < 20 else "evaluable")
        if status == "non_estimable" or np.unique(y[idx]).size < 2:
            rows.append({"cohort": cohort, "subgroup": subgroup, "n": int(idx.sum()),
                         "events": events, "status": status, "model_auc": None,
                         "best_comparator": None, "best_comparator_auc": None, "delta": None})
            continue
        comp_auc = {k: float(roc_auc_score(y[idx], v[idx])) for k, v in comparators.items()}
        best = max(comp_auc, key=comp_auc.get)
        a = float(roc_auc_score(y[idx], primary[idx]))
        rows.append({"cohort": cohort, "subgroup": subgroup, "n": int(idx.sum()),
                     "events": events, "status": status, "model_auc": a,
                     "best_comparator": best, "best_comparator_auc": comp_auc[best],
                     "delta": a - comp_auc[best]})
    return rows


def raw_equation(bundle: dict) -> dict[str, float]:
    scaler = bundle["scaler"]
    fit = bundle["model"]
    raw = fit.coef_[0] / scaler.scale_
    intercept = float(fit.intercept_[0] - np.sum(fit.coef_[0] * scaler.mean_ / scaler.scale_))
    return {"intercept": intercept, **{k: float(v) for k, v in zip(bundle["columns"], raw)}}


def plot_results(candidate_table: pd.DataFrame, calibration_data: dict[str, dict]) -> None:
    order = list(CANDIDATES)
    fig, ax = plt.subplots(figsize=(8.5, 5.5))
    y = np.arange(len(order))
    for offset, direction, color in [(-0.12, "DRAGON_to_UKB_strict", "#1f77b4"),
                                     (0.12, "UKB_strict_to_DRAGON", "#d62728")]:
        sub = candidate_table[candidate_table["direction"].eq(direction)].set_index("candidate").loc[order]
        ax.scatter(sub["target_auc"], y + offset, label=direction.replace("_", " "), color=color)
    ax.set_yticks(y, [v.replace("_", " ") for v in order])
    ax.set_xlabel("Reciprocal-transport AUC")
    ax.set_xlim(0.60, 0.94)
    ax.grid(axis="x", alpha=0.25)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIG / "candidate_transport_auc.png", dpi=240)
    fig.savefig(FIG / "candidate_transport_auc.pdf")
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.3))
    for ax, (name, item) in zip(axes, calibration_data.items()):
        yv, p = item["y"], item["p"]
        bins = pd.qcut(pd.Series(p), q=min(5, len(np.unique(p))), duplicates="drop")
        tab = pd.DataFrame({"y": yv, "p": p, "bin": bins}).groupby("bin", observed=True).agg(
            observed=("y", "mean"), predicted=("p", "mean"), n=("y", "size"))
        ax.plot([0, max(0.35, tab[["observed", "predicted"]].to_numpy().max())],
                [0, max(0.35, tab[["observed", "predicted"]].to_numpy().max())], "--", color="grey")
        ax.plot(tab["predicted"], tab["observed"], "o-", color="#1f77b4")
        ax.set_title(name.replace("_", " "))
        ax.set_xlabel("Predicted probability")
        ax.set_ylabel("Observed prevalence")
    fig.tight_layout()
    fig.savefig(FIG / "external_calibration.png", dpi=240)
    fig.savefig(FIG / "external_calibration.pdf")
    plt.close(fig)


def main() -> None:
    cohorts = prepare_cohorts()
    dragon, strict, union = cohorts["dragon"], cohorts["ukb_strict"], cohorts["ukb_union"]
    audit = {}
    for name, frame in cohorts.items():
        audit[name] = {"n": int(len(frame)), "events": int(frame["y"].sum()),
                       "clusters": int(frame["cluster"].nunique()),
                       "coverage": {c: int(frame[c].notna().sum()) for c in RAW}}
    (OUT / "cohort_audit.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")

    directions = {
        "DRAGON_to_UKB_strict": (dragon, strict),
        "UKB_strict_to_DRAGON": (strict, dragon),
    }
    rows, tuning_rows, fitted = [], [], {}
    for d_i, (direction, (source, target)) in enumerate(directions.items()):
        for c_i, candidate in enumerate(CANDIDATES):
            result = transport(source, target, candidate, SEED + d_i * 100 + c_i)
            equation = raw_equation(result["bundle"])
            violations = [name for name, value in equation.items()
                          if name in EXPECTED_POSITIVE and value < -1e-9]
            rows.append({"direction": direction, "candidate": candidate,
                         "source_n": len(source), "source_events": int(source["y"].sum()),
                         "target_n": len(target), "target_events": int(target["y"].sum()),
                         "selected_C": result["penalty"], "target_auc": result["auc"],
                         "target_brier": result["brier"],
                         "sign_coherent": len(violations) == 0,
                         "sign_violations": ";".join(violations),
                         "source_equation": json.dumps(equation, sort_keys=True)})
            q = result["tuning"].copy()
            q.insert(0, "direction", direction)
            tuning_rows.append(q)
            fitted[(direction, candidate)] = result
            print(f"{direction}: {candidate}: AUC={result['auc']:.6f}, C={result['penalty']}", flush=True)
    candidate_table = pd.DataFrame(rows)
    candidate_table.to_csv(OUT / "candidate_reciprocal_transport.csv", index=False)
    pd.concat(tuning_rows, ignore_index=True).to_csv(OUT / "source_grouped_tuning.csv", index=False)

    pivot = candidate_table.pivot(index="candidate", columns="direction", values="target_auc")
    pivot["min_auc"] = pivot.min(axis=1)
    pivot["mean_auc"] = pivot[["DRAGON_to_UKB_strict", "UKB_strict_to_DRAGON"]].mean(axis=1)
    sign_gate = candidate_table.groupby("candidate")["sign_coherent"].all()
    pivot["sign_coherent_both_directions"] = sign_gate
    eligible = pivot.loc[pivot["sign_coherent_both_directions"]]
    if eligible.empty:
        raise RuntimeError("No candidate passed the locked sign-coherence gate")
    selected = str(eligible.sort_values(["min_auc", "mean_auc"], ascending=False).index[0])
    selection = {"selected_architecture": selected,
                 "criterion": "highest minimum reciprocal-transport AUC; target-informed exploratory selection",
                 "table": pivot.reset_index().to_dict(orient="records")}
    # Phase A tested score-augmentation architectures and is not the de novo
    # CALON-N selection used in the manuscript. Keep the phase in the filename
    # so this diagnostic cannot be mistaken for the locked Phase-B result.
    (OUT / "phase_a_score_augmentation_selection.json").write_text(
        json.dumps(selection, indent=2), encoding="utf-8"
    )

    internal_rows = []
    for name, frame in [("dragon", dragon), ("ukb_strict", strict)]:
        for candidate in ["age_sex", "montreal", "calon_disc_core", selected]:
            if any(r["candidate"] == candidate and r["cohort"] == name for r in internal_rows):
                continue
            pred, aucs = nested_oof(frame, candidate)
            internal_rows.append({"cohort": name, "candidate": candidate,
                                  "rank_aggregated_auc": float(roc_auc_score(frame["y"], pred)),
                                  "repeat_auc_mean": float(np.mean(aucs)),
                                  "repeat_auc_sd": float(np.std(aucs, ddof=1)),
                                  "repeat_aucs": json.dumps(aucs)})
    pd.DataFrame(internal_rows).to_csv(OUT / "candidate_nested_grouped_internal.csv", index=False)

    external = {}
    dca_rows, subgroup = [], []
    calibration_data = {}
    for d_i, (direction, (source, target)) in enumerate(directions.items()):
        result = fitted[(direction, selected)]
        p = result["prediction"]
        comps = source_comparators(source, target)
        comps["age_sex"] = fitted[(direction, "age_sex")]["prediction"]
        y = target["y"].to_numpy(int)
        g = target["cluster"].to_numpy()
        metrics = cluster_boot_metrics(y, p, g, comps, SEED + 400 + d_i)
        metrics["calibration"] = calibration(y, p)
        metrics["n"] = int(len(target)); metrics["events"] = int(y.sum())
        metrics["selected_C"] = result["penalty"]
        external[direction] = metrics
        predictions = {"CALON_DISC": p, **comps}
        dca = decision_curve(y, predictions, [0.05, 0.075, 0.10, 0.15, 0.20, 0.25])
        for row in dca:
            row["direction"] = direction
        dca_rows.extend(dca)
        cohort_name = "ukb_strict" if direction.startswith("DRAGON") else "dragon"
        subgroup.extend(subgroup_rows(cohort_name, target, p, comps))
        calibration_data[cohort_name] = {"y": y, "p": p}
    (OUT / "selected_external_performance.json").write_text(json.dumps(external, indent=2), encoding="utf-8")
    pd.DataFrame(dca_rows).to_csv(OUT / "decision_curve.csv", index=False)
    pd.DataFrame(subgroup).to_csv(OUT / "subgroup_performance.csv", index=False)

    # Prespecified union sensitivity, using the DRAGON-fitted selected model.
    union_result = fitted[("DRAGON_to_UKB_strict", selected)]
    p_union = predict_candidate(union_result["bundle"], union)
    union_comps = source_comparators(dragon, union)
    union_comps["age_sex"] = predict_candidate(
        fitted[("DRAGON_to_UKB_strict", "age_sex")]["bundle"], union
    )
    union_metrics = cluster_boot_metrics(union["y"].to_numpy(int), p_union,
                                         union["cluster"].to_numpy(), union_comps, SEED + 777)
    union_metrics["calibration"] = calibration(union["y"].to_numpy(int), p_union)
    union_metrics["n"] = int(len(union)); union_metrics["events"] = int(union["y"].sum())
    (OUT / "ukb_union_sensitivity.json").write_text(json.dumps(union_metrics, indent=2), encoding="utf-8")

    # Fit one pooled research bundle for future independent testing. No cohort indicator.
    pooled = pd.concat([dragon, strict], ignore_index=True)
    pooled["cluster"] = [f"D:{v}" for v in dragon["cluster"].astype(str)] + [f"U:{v}" for v in strict["cluster"].astype(str)]
    pooled_c, pooled_tuning = choose_penalty(pooled, selected, SEED + 900)
    pooled_bundle = fit_candidate(pooled, selected, pooled_c)
    pooled_bundle["name"] = "CALON-DISC cross-sectional established-ASCVD research classifier"
    pooled_bundle["version"] = "2026-08-09"
    pooled_bundle["estimand"] = "prevalent established-ASCVD case identification; not incidence prediction"
    pooled_bundle["equation_raw_transformed_units"] = raw_equation(pooled_bundle)
    joblib.dump(pooled_bundle, MODEL / "phase_a_score_augmentation.joblib", compress=3)
    (MODEL / "phase_a_score_augmentation_equation.json").write_text(json.dumps({
        "candidate": selected, "penalty_C": pooled_c,
        "features": pooled_bundle["columns"], "equation": raw_equation(pooled_bundle),
        "preprocessor": pooled_bundle["preprocessor"],
        "warning": "Pooled research equation has no untouched external validation and requires site recalibration."
    }, indent=2), encoding="utf-8")
    pooled_tuning.to_csv(OUT / "pooled_penalty_tuning.csv", index=False)

    # Algebraic identity check: reconstruct fitted linear predictor after replacing residual by log apoB/log LDL.
    eq = raw_equation(pooled_bundle)
    if "discordance" in eq:
        pre = pooled_bundle["preprocessor"]
        transformed = {
            "intercept": eq["intercept"] - eq["discordance"] * pre["discordance_intercept"],
            "montreal": eq.get("montreal", 0.0),
            "log_ldl": eq.get("log_ldl", 0.0) - eq["discordance"] * pre["discordance_slope"],
            "log_apob": eq["discordance"],
        }
        (OUT / "discordance_parameterisation_identity.json").write_text(json.dumps({
            "residual_parameterisation": eq, "equivalent_log_apob_log_ldl_parameterisation": transformed,
            "interpretation": "Residualisation changes interpretation, not the linear information space."
        }, indent=2), encoding="utf-8")

    plot_results(candidate_table, calibration_data)

    manifest = {
        "protocol_sha256": sha256(ROOT / "PROTOCOL_LOCK.md"),
        "canonical_engine_sha256": sha256(SOURCE / "code" / "01_dragon_model_rebuild.py"),
        "canonical_input_sha256": {str(p): sha256(p) for p in [e.DRAGON, e.PASS, e.UKB, e.CALLS, e.UKB_CLINVAR, e.UKB_VEP, e.DRAGON_CLINVAR]},
        "analysis_sha256": sha256(ROOT / "code" / "01_calon_disc_analysis.py"),
        "participant_level_outputs": False,
    }
    (OUT / "analysis_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps({"selected": selected, "external": external, "union": union_metrics,
                      "pooled_C": pooled_c, "equation": raw_equation(pooled_bundle)}, indent=2))


if __name__ == "__main__":
    main()
