#!/usr/bin/env python3
"""A3: independent raw-source re-derivation of locked CALON-N numbers.

The stored aggregate JSON is loaded only after all independent predictions and
statistics have been computed. Only aggregate comparisons are serialised.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

from audit_common import (
    CALON_N,
    OUT,
    ROOT,
    bounded,
    build_dragon,
    build_ukb,
    event_count,
    expected_observed,
    input_paths,
    metric_block,
    num,
    source_comparators,
    transport,
    write_json,
)


BOOTSTRAP = 4000
LOCKED_SEEDS = {
    "calon_forward": 20260826,
    "calon_reverse": 20260926,
    "age_sex_forward": 20260819,
    "age_sex_reverse": 20260919,
    "metric_forward": 20261219,
    "metric_reverse": 20261220,
    "matching": 20260810,
}
FH_FEATURES = ["age", "male", "hdl", "hypertension", "smoke_ever", "log_ratio", "log_apoa1"]


def match_controls(
    case_age: np.ndarray,
    case_sex: np.ndarray,
    controls: pd.DataFrame,
    ratio: int,
    calliper: float,
    seed: int,
) -> tuple[list[int], pd.DataFrame]:
    rng = np.random.default_rng(seed)
    taken = np.zeros(len(controls), dtype=bool)
    control_age = controls["age"].to_numpy()
    control_sex = controls["male"].to_numpy()
    picked: list[int] = []
    kept_cases: list[int] = []
    for case_position in rng.permutation(len(case_age)):
        eligible = (
            (~taken)
            & (control_sex == case_sex[case_position])
            & (np.abs(control_age - case_age[case_position]) <= calliper)
        )
        candidates = np.flatnonzero(eligible)
        if candidates.size < ratio:
            continue
        ordering = np.argsort(
            np.abs(control_age[candidates] - case_age[case_position]), kind="stable"
        )
        chosen = candidates[ordering][:ratio]
        taken[chosen] = True
        picked.extend(chosen.tolist())
        kept_cases.append(int(case_position))
    return sorted(kept_cases), controls.iloc[sorted(picked)].reset_index(drop=True)


def build_nonfh_pool() -> pd.DataFrame:
    master = input_paths()["ukb_master"]
    use = [
        "ldlr_carrier", "prevalent_ascvd", "age_exact_baseline", "age_at_recruit",
        "sex_F", "diabetes_combined", "smoking_ever", "sbp", "dbp", "pre_tc", "tc_chem",
        "pre_ldl", "ldl_chem", "pre_hdl", "hdl_chem", "pre_tg", "tg_chem", "apob",
        "apob_chem", "apo_a1", "pre_lpa", "lpa_chem", "on_statin_self", "bmi_direct",
    ]
    raw = pd.read_csv(master, usecols=use, low_memory=False)
    raw = raw.loc[num(raw, "ldlr_carrier").fillna(0).ne(1)].reset_index(drop=True)
    x = pd.DataFrame(index=raw.index)
    x["age"] = bounded(num(raw, "age_exact_baseline").fillna(num(raw, "age_at_recruit")), 5, 105)
    x["male"] = 1 - num(raw, "sex_F").fillna(0)
    diabetes = num(raw, "diabetes_combined")
    smoking = num(raw, "smoking_ever")
    x["diabetes"] = diabetes.gt(0).astype(float).where(diabetes.notna())
    x["smoke_ever"] = smoking.gt(0).astype(float).where(smoking.notna())
    sbp, dbp = bounded(num(raw, "sbp"), 70, 260), bounded(num(raw, "dbp"), 35, 160)
    x["hypertension"] = (sbp.ge(140) | dbp.ge(90)).astype(float).where(sbp.notna() | dbp.notna())
    x["ldl"] = bounded(num(raw, "pre_ldl").fillna(num(raw, "ldl_chem")), 0.3, 20)
    x["hdl"] = bounded(num(raw, "pre_hdl").fillna(num(raw, "hdl_chem")), 0.2, 5)
    x["apob"] = bounded(num(raw, "apob").fillna(num(raw, "apob_chem")), 0.2, 4)
    x["apoa1"] = bounded(num(raw, "apo_a1"), 0.3, 4)
    x["log_ratio"] = np.log((x["apob"] / x["ldl"]).where(lambda value: value.gt(0)))
    x["log_apoa1"] = np.log(x["apoa1"])
    x["y"] = num(raw, "prevalent_ascvd").fillna(0).gt(0).astype(int)
    return x.loc[x["age"].notna()].reset_index(drop=True)


def complete_for_auxiliary_model(frame: pd.DataFrame, features: list[str]) -> pd.DataFrame:
    q = frame.copy()
    for feature in features:
        q[feature] = pd.to_numeric(q[feature], errors="coerce")
        q[feature] = q[feature].fillna(q[feature].median())
    return q


def fit_auxiliary_model(frame: pd.DataFrame, features: list[str], penalty: float = 0.3) -> dict:
    q = complete_for_auxiliary_model(frame, features)
    matrix = q[features].to_numpy(float)
    mean = matrix.mean(axis=0)
    sd = matrix.std(axis=0)
    sd[sd < 1e-9] = 1.0
    model = LogisticRegression(C=penalty, max_iter=5000)
    model.fit((matrix - mean) / sd, q["y"].to_numpy(int))
    return {"features": features, "mean": mean, "sd": sd, "model": model}


def predict_auxiliary_model(bundle: dict, frame: pd.DataFrame) -> np.ndarray:
    # This deliberately reproduces code/07: missing values are filled using
    # target-frame medians at prediction time, which is flagged as transductive.
    q = complete_for_auxiliary_model(frame, bundle["features"])
    matrix = q[bundle["features"]].to_numpy(float)
    return bundle["model"].predict_proba((matrix - bundle["mean"]) / bundle["sd"])[:, 1]


def fh_nonfh_reproduction(strict: pd.DataFrame) -> dict:
    fh = strict.copy()
    fh["log_ratio"] = np.log((fh["apob"] / fh["ldl"]).where(lambda value: value.gt(0)))
    fh["log_apoa1"] = np.log(fh["apoa1"])
    pool = build_nonfh_pool()
    kept_cases, controls = match_controls(
        fh["age"].to_numpy(float),
        fh["male"].to_numpy(float),
        pool,
        ratio=5,
        calliper=1.0,
        seed=LOCKED_SEEDS["matching"],
    )
    fh_matched = fh.iloc[kept_cases].reset_index(drop=True)
    if len(fh_matched) != 890 or len(controls) != 4450:
        raise RuntimeError("FH/non-FH matching invariant failed")
    a = int(fh_matched["y"].sum())
    b = len(fh_matched) - a
    c = int(controls["y"].sum())
    d = len(controls) - c
    odds_ratio = float((a * d) / (b * c))
    standard_error = float(np.sqrt(1 / a + 1 / b + 1 / c + 1 / d))
    odds_ratio_ci = [
        float(np.exp(np.log(odds_ratio) - 1.96 * standard_error)),
        float(np.exp(np.log(odds_ratio) + 1.96 * standard_error)),
    ]
    fh_model = fit_auxiliary_model(fh_matched, FH_FEATURES)
    nonfh_model = fit_auxiliary_model(controls, FH_FEATURES)
    fh_to_nonfh = predict_auxiliary_model(fh_model, controls)
    nonfh_to_fh = predict_auxiliary_model(nonfh_model, fh_matched)
    return {
        "n_fh": len(fh_matched),
        "events_fh": event_count(a),
        "n_nonfh": len(controls),
        "events_nonfh": event_count(c),
        "odds_ratio": odds_ratio,
        "odds_ratio_ci": odds_ratio_ci,
        "e_o_fh_model_to_nonfh": expected_observed(controls["y"].to_numpy(int), fh_to_nonfh),
        "e_o_nonfh_model_to_fh": expected_observed(fh_matched["y"].to_numpy(int), nonfh_to_fh),
        "unmatched_fh_n": len(fh) - len(fh_matched),
    }


def compare_number(computed: float, stored: float) -> dict:
    difference = float(abs(float(computed) - float(stored)))
    return {
        "computed": float(computed),
        "stored": float(stored),
        "computed_4dp": round(float(computed), 4),
        "stored_4dp": round(float(stored), 4),
        "absolute_difference": difference,
        "defect_over_0_001": bool(difference > 0.001),
    }


def main() -> None:
    # Phase 1: raw-source computation. No stored performance result is read in
    # this phase.
    dragon = build_dragon()
    ukb, _ = build_ukb()
    strict = ukb.loc[ukb["strict"].eq(1)].copy().reset_index(drop=True)
    strict["cluster"] = strict["cluster_strict"]

    forward = transport(dragon, strict, CALON_N, LOCKED_SEEDS["calon_forward"])
    reverse = transport(strict, dragon, CALON_N, LOCKED_SEEDS["calon_reverse"])
    forward_age_sex = transport(
        dragon, strict, ["age", "male"], LOCKED_SEEDS["age_sex_forward"]
    )
    reverse_age_sex = transport(
        strict, dragon, ["age", "male"], LOCKED_SEEDS["age_sex_reverse"]
    )
    forward_comparators = source_comparators(dragon, strict)
    forward_comparators["age_sex"] = forward_age_sex["prediction"]
    reverse_comparators = source_comparators(strict, dragon)
    reverse_comparators["age_sex"] = reverse_age_sex["prediction"]
    order = ["age_sex", "Montreal_adapted", "FH_Risk_Score_adapted", "SAFEHEART_adapted"]
    forward_comparators = {name: forward_comparators[name] for name in order}
    reverse_comparators = {name: reverse_comparators[name] for name in order}
    computed = {
        "DRAGON_to_UKB_strict": metric_block(
            strict["y"].to_numpy(int),
            forward["prediction"],
            strict["cluster"].to_numpy(),
            forward_comparators,
            LOCKED_SEEDS["metric_forward"],
            BOOTSTRAP,
        ),
        "UKB_strict_to_DRAGON": metric_block(
            dragon["y"].to_numpy(int),
            reverse["prediction"],
            dragon["cluster"].to_numpy(),
            reverse_comparators,
            LOCKED_SEEDS["metric_reverse"],
            BOOTSTRAP,
        ),
    }
    computed["DRAGON_to_UKB_strict"].update({
        "n": len(strict), "events": event_count(int(strict["y"].sum())),
        "selected_C": forward["penalty"],
    })
    computed["UKB_strict_to_DRAGON"].update({
        "n": len(dragon), "events": event_count(int(dragon["y"].sum())),
        "selected_C": reverse["penalty"],
    })
    fh_nonfh = fh_nonfh_reproduction(strict)

    # Phase 2: aggregate-only comparison with locked outputs.
    stored_external = json.loads((ROOT / "outputs" / "scratch_external_performance.json").read_text())
    stored_fh = json.loads((ROOT / "outputs" / "fh_vs_nonfh.json").read_text())["arms"][0]
    comparisons: dict[str, dict] = {}
    for direction in ["DRAGON_to_UKB_strict", "UKB_strict_to_DRAGON"]:
        comparisons[direction] = {
            "auc": compare_number(computed[direction]["auc"], stored_external[direction]["auc"]),
            "e_o": compare_number(
                computed[direction]["e_o"],
                stored_external[direction]["calibration"]["expected_observed_ratio"],
            ),
            "comparators": {},
        }
        for name in order:
            independent = computed[direction]["comparators"][name]
            locked = stored_external[direction]["comparators"][name]
            comparisons[direction]["comparators"][name] = {
                "auc": compare_number(independent["auc"], locked["auc"]),
                "delta": compare_number(
                    independent["delta_calon_minus_comparator"], locked["delta"]
                ),
                "delta_ci_low": compare_number(independent["delta_ci"][0], locked["delta_ci"][0]),
                "delta_ci_high": compare_number(independent["delta_ci"][1], locked["delta_ci"][1]),
            }
    comparisons["FH_vs_matched_nonFH"] = {
        "odds_ratio": compare_number(fh_nonfh["odds_ratio"], stored_fh["odds_ratio_fh_vs_nonfh"]),
        "or_ci_low": compare_number(fh_nonfh["odds_ratio_ci"][0], stored_fh["or_ci"][0]),
        "or_ci_high": compare_number(fh_nonfh["odds_ratio_ci"][1], stored_fh["or_ci"][1]),
        "e_o_fh_model_to_nonfh": compare_number(
            fh_nonfh["e_o_fh_model_to_nonfh"], stored_fh["fh_to_nonfh"]["E_O"]
        ),
        "e_o_nonfh_model_to_fh": compare_number(
            fh_nonfh["e_o_nonfh_model_to_fh"], stored_fh["nonfh_to_fh"]["E_O"]
        ),
    }

    defects: list[dict] = []
    def collect(path: str, value: object) -> None:
        if isinstance(value, dict):
            if value.get("defect_over_0_001"):
                defects.append({"metric": path, "cause": "Independent raw-source value differs from locked aggregate."})
            for key, child in value.items():
                collect(f"{path}.{key}" if path else key, child)
    collect("", comparisons)

    result = {
        "task": "A3_locked_reproduction",
        "independent_computed": computed,
        "fh_vs_matched_nonfh_independent": fh_nonfh,
        "agreement_checks": comparisons,
        "discrepancy_gate": {
            "threshold_absolute": 0.001,
            "defect_count": len(defects),
            "defects": defects,
            "all_locked_numbers_reproduce": len(defects) == 0,
            "verdict": "yes" if not defects else "no",
        },
        "methodological_defects_not_numeric_drift": [
            {
                "severity": "blocking_for_prospective_risk_claim",
                "defect": "Prevalent-outcome temporality violation",
                "evidence": "Welsh current/last clinical predictors and UKB recruitment biomarkers can occur after established ASCVD.",
            },
            {
                "severity": "blocking_for_unbiased_external_performance_claim",
                "defect": "Target-informed architecture selection",
                "evidence": "Both reciprocal transport targets were used to choose the reported architecture before its AUCs were headlined.",
            },
            {
                "severity": "major_for_FH_vs_nonFH_auxiliary_claim",
                "defect": "Matched-design dependence ignored",
                "evidence": "The reported four-cell Wald OR CI does not account for matched sets or carrier clustering.",
            },
            {
                "severity": "major_for_FH_vs_nonFH_transport",
                "defect": "Target-frame median imputation",
                "evidence": "Prediction-time missing values are filled from the full target frame, making the auxiliary transport transductive.",
            },
            {
                "severity": "major_for_comparator_interpretation",
                "defect": "Comparator estimands are not harmonised",
                "evidence": "Adapted ranking scores and a 5-year SAFEHEART probability are compared with cross-sectional prevalence; E:O is undefined or horizon-incompatible.",
            },
        ],
        "participant_level_outputs": False,
    }
    write_json(OUT / "a3_locked_reproduction.json", result)
    print(json.dumps({
        "A3": {
            "forward_auc": computed["DRAGON_to_UKB_strict"]["auc"],
            "reverse_auc": computed["UKB_strict_to_DRAGON"]["auc"],
            "fh_nonfh_or": fh_nonfh["odds_ratio"],
            "numeric_defects_over_0_001": len(defects),
            "verdict": result["discrepancy_gate"]["verdict"],
        },
        "written": "outputs/audit_2026_08_10/a3_locked_reproduction.json",
    }, indent=2))


if __name__ == "__main__":
    main()
