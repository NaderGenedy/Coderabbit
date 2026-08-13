#!/usr/bin/env python3
"""Apply the frozen CALON-N research classifier to a predictor CSV.

Required columns (raw clinical units): age, male, hdl, hypertension,
smoke_ever, ldl, apob, apoa1. Extra columns are ignored. Missing values use
the frozen pooled-development medians. This program must not be used to infer
future ASCVD risk or guide treatment.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

DEFAULT_MODEL = Path(
    "${CALON_PROJECT_ROOT}/model/calon_n_from_scratch.joblib"
)
REQUIRED = ["age", "male", "hdl", "hypertension", "smoke_ever", "ldl", "apob", "apoa1"]


def score(frame: pd.DataFrame, bundle: dict) -> np.ndarray:
    missing = [c for c in REQUIRED if c not in frame]
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(missing))
    defaults = bundle["preprocessor"]["defaults"]
    q = pd.DataFrame(index=frame.index)
    for c in REQUIRED:
        q[c] = pd.to_numeric(frame[c], errors="coerce").fillna(defaults[c]).astype(float)
    q["age"] = q["age"].clip(5, 105)
    q["male"] = q["male"].clip(0, 1)
    q["hdl"] = q["hdl"].clip(0.2, 5)
    q["hypertension"] = q["hypertension"].clip(0, 1)
    q["smoke_ever"] = q["smoke_ever"].clip(0, 1)
    q["ldl"] = q["ldl"].clip(0.3, 20)
    q["apob"] = q["apob"].clip(0.2, 4)
    q["apoa1"] = q["apoa1"].clip(0.3, 4)
    z = pd.DataFrame({
        "age": q["age"], "male": q["male"], "hdl": q["hdl"],
        "hypertension": q["hypertension"], "smoke_ever": q["smoke_ever"],
        "log_ratio": np.log(q["apob"] / q["ldl"]),
        "log_apoa1": np.log(q["apoa1"]),
    })
    columns = bundle["columns"]
    return bundle["model"].predict_proba(bundle["scaler"].transform(z[columns]))[:, 1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("output_csv", type=Path)
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL)
    args = parser.parse_args()
    bundle = joblib.load(args.model)
    frame = pd.read_csv(args.input_csv)
    output = pd.DataFrame({"calon_n_probability": score(frame, bundle)})
    output.to_csv(args.output_csv, index=False)


if __name__ == "__main__":
    main()
