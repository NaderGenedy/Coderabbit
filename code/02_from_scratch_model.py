#!/usr/bin/env python3
"""Phase-B CALON-N: from-scratch, raw-variable model development.

The script imports cohort construction and validation utilities from phase A,
but no published score is permitted as a model input. Aggregate outputs only.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

ROOT = Path("/Users/nader85/Documents/CALON/calon_discordance_model_2026_08_09")
BASE = ROOT / "code" / "01_calon_disc_analysis.py"
OUT = ROOT / "outputs"
MODEL = ROOT / "model"
FIG = ROOT / "figures"
SEED = 20260819

spec = importlib.util.spec_from_file_location("calon_base", BASE)
if spec is None or spec.loader is None:
    raise RuntimeError("Could not import phase-A engine")
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)

SCRATCH = {
    "age_sex": ["age", "male"],
    "age_sex_ratio": ["age", "male", "log_ratio"],
    "clinical5": ["age", "male", "hdl", "hypertension", "smoke_ever"],
    "calon_n_core": ["age", "male", "hdl", "hypertension", "smoke_ever", "log_ratio"],
    "calon_n_diabetes": ["age", "male", "hdl", "hypertension", "smoke_ever", "log_ratio", "diabetes"],
    "calon_n_tghdl": ["age", "male", "hdl", "hypertension", "smoke_ever", "log_ratio", "log_tghdl"],
    "calon_n_lpa": ["age", "male", "hdl", "hypertension", "smoke_ever", "log_ratio", "log_lpa"],
    "calon_n_apoa1": ["age", "male", "hdl", "hypertension", "smoke_ever", "log_ratio", "log_apoa1"],
    "calon_n_discordance": ["age", "male", "hdl", "hypertension", "smoke_ever", "log_ldl", "discordance"],
    "calon_n_parsimonious": ["age", "male", "hypertension", "log_ratio"],
}

EXPECTED = {
    "age": 1, "male": 1, "hdl": -1, "hypertension": 1, "smoke_ever": 1,
    "log_ratio": 1, "diabetes": 1, "log_tghdl": 1, "log_lpa": 1,
    "log_apoa1": -1, "log_ldl": 1, "discordance": 1,
}

m.CANDIDATES = SCRATCH


def violations(equation: dict[str, float]) -> list[str]:
    return [name for name, sign in EXPECTED.items()
            if name in equation and sign * equation[name] < -1e-9]


def main() -> None:
    cohorts = m.prepare_cohorts()
    dragon, strict, union = cohorts["dragon"], cohorts["ukb_strict"], cohorts["ukb_union"]
    directions = {
        "DRAGON_to_UKB_strict": (dragon, strict),
        "UKB_strict_to_DRAGON": (strict, dragon),
    }
    rows, tuning, fitted = [], [], {}
    for di, (direction, (source, target)) in enumerate(directions.items()):
        for ci, candidate in enumerate(SCRATCH):
            result = m.transport(source, target, candidate, SEED + di * 100 + ci)
            eq = m.raw_equation(result["bundle"])
            bad = violations(eq)
            rows.append({
                "direction": direction, "candidate": candidate,
                "source_n": len(source), "source_events": int(source["y"].sum()),
                "target_n": len(target), "target_events": int(target["y"].sum()),
                "selected_C": result["penalty"], "target_auc": result["auc"],
                "target_brier": result["brier"], "sign_coherent": not bad,
                "sign_violations": ";".join(bad), "source_equation": json.dumps(eq, sort_keys=True),
            })
            q = result["tuning"].copy(); q.insert(0, "direction", direction)
            tuning.append(q)
            fitted[(direction, candidate)] = result
            print(f"{direction}: {candidate}: AUC={result['auc']:.6f}; signs={'PASS' if not bad else bad}", flush=True)
    table = pd.DataFrame(rows)
    table.to_csv(OUT / "scratch_candidate_transport.csv", index=False)
    pd.concat(tuning, ignore_index=True).to_csv(OUT / "scratch_source_tuning.csv", index=False)

    pivot = table.pivot(index="candidate", columns="direction", values="target_auc")
    pivot["min_auc"] = pivot.min(axis=1)
    pivot["mean_auc"] = pivot[["DRAGON_to_UKB_strict", "UKB_strict_to_DRAGON"]].mean(axis=1)
    pivot["sign_coherent_both_directions"] = table.groupby("candidate")["sign_coherent"].all()
    eligible = pivot[pivot["sign_coherent_both_directions"]]
    if eligible.empty:
        raise RuntimeError("No from-scratch candidate passed sign coherence")
    selected = str(eligible.sort_values(["min_auc", "mean_auc"], ascending=False).index[0])
    (OUT / "scratch_selection.json").write_text(json.dumps({
        "selected": selected,
        "criterion": "highest minimum reciprocal-transport AUC after locked sign gate",
        "target_informed": True,
        "published_score_used_as_input": False,
        "table": pivot.reset_index().to_dict(orient="records"),
    }, indent=2), encoding="utf-8")

    internal = []
    for name, frame in [("dragon", dragon), ("ukb_strict", strict)]:
        for candidate in dict.fromkeys(["age_sex", "clinical5", "age_sex_ratio", selected]):
            pred, aucs = m.nested_oof(frame, candidate)
            internal.append({"cohort": name, "candidate": candidate,
                             "rank_aggregated_auc": float(roc_auc_score(frame["y"], pred)),
                             "repeat_auc_mean": float(np.mean(aucs)),
                             "repeat_auc_sd": float(np.std(aucs, ddof=1)),
                             "repeat_aucs": json.dumps(aucs)})
    pd.DataFrame(internal).to_csv(OUT / "scratch_nested_grouped_internal.csv", index=False)

    external, dca_rows, subgroup_rows, calibration_data = {}, [], [], {}
    for di, (direction, (source, target)) in enumerate(directions.items()):
        result = fitted[(direction, selected)]
        p = result["prediction"]
        comps = m.source_comparators(source, target)
        comps["age_sex"] = fitted[(direction, "age_sex")]["prediction"]
        y, g = target["y"].to_numpy(int), target["cluster"].to_numpy()
        perf = m.cluster_boot_metrics(y, p, g, comps, SEED + 400 + di)
        perf["calibration"] = m.calibration(y, p)
        perf["n"] = int(len(target)); perf["events"] = int(y.sum())
        perf["selected_C"] = result["penalty"]
        external[direction] = perf
        for row in m.decision_curve(y, {"CALON_N": p, **comps}, [0.05, 0.075, 0.10, 0.15, 0.20, 0.25]):
            row["direction"] = direction
            row["valid_for_comparator_inference"] = False
            row["qc_status"] = (
                "WITHDRAWN: Montreal and FH-Risk-Score outputs are ranking "
                "scores/linear predictors, not calibrated probabilities on a common scale"
            )
            dca_rows.append(row)
        cohort_name = "ukb_strict" if direction.startswith("DRAGON") else "dragon"
        subgroup_rows.extend(m.subgroup_rows(cohort_name, target, p, comps))
        calibration_data[cohort_name] = {"y": y, "p": p}
    (OUT / "scratch_external_performance.json").write_text(json.dumps(external, indent=2), encoding="utf-8")
    pd.DataFrame(dca_rows).to_csv(OUT / "scratch_decision_curve.csv", index=False)
    pd.DataFrame(subgroup_rows).to_csv(OUT / "scratch_subgroups.csv", index=False)

    # DRAGON-fitted union sensitivity.
    p_union = m.predict_candidate(fitted[("DRAGON_to_UKB_strict", selected)]["bundle"], union)
    comps_union = m.source_comparators(dragon, union)
    comps_union["age_sex"] = m.predict_candidate(fitted[("DRAGON_to_UKB_strict", "age_sex")]["bundle"], union)
    union_perf = m.cluster_boot_metrics(union["y"].to_numpy(int), p_union,
                                        union["cluster"].to_numpy(), comps_union, SEED + 700)
    union_perf["calibration"] = m.calibration(union["y"].to_numpy(int), p_union)
    union_perf["n"] = int(len(union)); union_perf["events"] = int(union["y"].sum())
    (OUT / "scratch_union_sensitivity.json").write_text(json.dumps(union_perf, indent=2), encoding="utf-8")

    # Pooled research equation for future testing only.
    pooled = pd.concat([dragon, strict], ignore_index=True)
    pooled["cluster"] = [f"D:{v}" for v in dragon["cluster"].astype(str)] + [f"U:{v}" for v in strict["cluster"].astype(str)]
    c, tune = m.choose_penalty(pooled, selected, SEED + 900)
    bundle = m.fit_candidate(pooled, selected, c)
    bundle.update({"name": "CALON-N from-scratch established-ASCVD research classifier",
                   "version": "2026-08-09", "published_score_used_as_input": False,
                   "estimand": "cross-sectional established-ASCVD case identification; not incidence prediction",
                   "equation_raw_transformed_units": m.raw_equation(bundle)})
    joblib.dump(bundle, MODEL / "calon_n_from_scratch.joblib", compress=3)
    (MODEL / "calon_n_equation.json").write_text(json.dumps({
        "candidate": selected, "penalty_C": c, "features": bundle["columns"],
        "equation": m.raw_equation(bundle), "preprocessor": bundle["preprocessor"],
        "warning": "Target-informed pooled research equation; no untouched external validation; not an incidence model."
    }, indent=2), encoding="utf-8")
    tune.to_csv(OUT / "scratch_pooled_tuning.csv", index=False)

    # Compact performance plot.
    order = list(SCRATCH)
    fig, ax = plt.subplots(figsize=(8.5, 5.7))
    yy = np.arange(len(order))
    for off, direction, color in [(-0.12, "DRAGON_to_UKB_strict", "#20639b"),
                                  (0.12, "UKB_strict_to_DRAGON", "#d1495b")]:
        q = table[table["direction"].eq(direction)].set_index("candidate").loc[order]
        ax.scatter(q["target_auc"], yy + off, color=color, label=direction.replace("_", " "))
    ax.set_yticks(yy, [x.replace("_", " ") for x in order]); ax.set_xlim(0.60, 0.94)
    ax.set_xlabel("Reciprocal-transport AUC"); ax.grid(axis="x", alpha=.25); ax.legend(frameon=False)
    fig.tight_layout(); fig.savefig(FIG / "scratch_transport_auc.png", dpi=240); fig.savefig(FIG / "scratch_transport_auc.pdf"); plt.close(fig)

    (OUT / "scratch_run_summary.json").write_text(json.dumps({
        "selected": selected, "external": external, "union": union_perf,
        "pooled_C": c, "pooled_equation": m.raw_equation(bundle),
        "participant_level_outputs": False,
    }, indent=2), encoding="utf-8")
    print(json.dumps({"selected": selected, "external": external,
                      "pooled_equation": m.raw_equation(bundle)}, indent=2))


if __name__ == "__main__":
    main()
