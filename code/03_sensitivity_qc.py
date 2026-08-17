#!/usr/bin/env python3
"""Prespecified/structural sensitivities for the selected CALON-N model."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
from sklearn.metrics import roc_auc_score

ROOT = Path("/Users/nader85/Documents/CALON/calon_discordance_model_2026_08_09")

def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec); sys.modules[name] = module; spec.loader.exec_module(module)
    return module

b = load("calon_base_sens", ROOT / "code" / "01_calon_disc_analysis.py")
s = load("calon_scratch_sens", ROOT / "code" / "02_from_scratch_model.py")
b.CANDIDATES = s.SCRATCH


def auc_or_none(y, p):
    return float(roc_auc_score(y, p)) if np.unique(y).size == 2 else None


def main() -> None:
    cohorts = b.prepare_cohorts(); dragon, strict = cohorts["dragon"], cohorts["ukb_strict"]
    selected = json.loads((ROOT / "outputs" / "scratch_selection.json").read_text())["selected"]
    forward = b.transport(dragon, strict, selected, 20260829)
    reverse = b.transport(strict, dragon, selected, 20260830)
    pd, pu = forward["prediction"], reverse["prediction"]
    strict_d = dragon["strict_plp"].eq(1).to_numpy()
    required_raw = ["age", "male", "hdl", "hypertension", "smoke_ever", "ldl", "apob", "apoa1"]
    complete_d = dragon[required_raw].notna().all(axis=1).to_numpy()
    complete_u = strict[required_raw].notna().all(axis=1).to_numpy()
    result = {
        "selected": selected,
        "dragon_archived_exact_hgvs_ldlr_plp": {
            "n": int(strict_d.sum()), "events": int(dragon.loc[strict_d, "y"].sum()),
            "UKB_fitted_model_auc": auc_or_none(dragon.loc[strict_d, "y"].to_numpy(int), pu[strict_d]),
            "warning": "Small conservative sensitivity; local archived HGVS matching misses unparseable/absent clinically confirmed variants.",
        },
        "dragon_alternative_outcomes_using_UKB_fitted_model": {
            "registry_flag_n": int(len(dragon)), "registry_flag_events": int(dragon["y"].sum()),
            "registry_flag_auc": auc_or_none(dragon["y"].to_numpy(int), pu),
            "component_union_events": int(dragon["y_union"].sum()),
            "component_union_auc": auc_or_none(dragon["y_union"].to_numpy(int), pu),
            "hard_coronary_events": int(dragon["y_hard"].sum()),
            "hard_coronary_auc": auc_or_none(dragon["y_hard"].to_numpy(int), pu),
        },
        "complete_case_transport": {
            "DRAGON_to_UKB_strict": {"n": int(complete_u.sum()),
                "events": int(strict.loc[complete_u, "y"].sum()),
                "auc": auc_or_none(strict.loc[complete_u, "y"].to_numpy(int), pd[complete_u])},
            "UKB_strict_to_DRAGON": {"n": int(complete_d.sum()),
                "events": int(dragon.loc[complete_d, "y"].sum()),
                "auc": auc_or_none(dragon.loc[complete_d, "y"].to_numpy(int), pu[complete_d])},
        },
        "participant_level_outputs": False,
    }
    (ROOT / "outputs" / "scratch_sensitivity_qc.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
