#!/usr/bin/env python3
"""CALON-G Cycle 2, locked-protocol analysis engine.

Aggregates only; no eid prints; primary ASCVD endpoint (I50 out); MACE is NOT primary; missing data is train-fold impute NOT MCAR; B=2000; corrected horizon.

This module never reads participant-level files.  Supply already-loaded pandas
DataFrames to :func:`run_cycle2`, or paste the file into Julius after defining
``FROZEN``, ``COHORT_LEDGER`` and ``COHORT_HASH``.  Participant-level OOF
predictions stay in memory; only aggregate model, validation and provenance
tables are written.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import warnings
from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, version as package_version
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd
from lifelines import CoxPHFitter, KaplanMeierFitter
from lifelines.statistics import proportional_hazard_test
from lifelines.utils import concordance_index


# ---------------------------------------------------------------------------
# Frozen protocol
SEED = 20260815
B_BOOT = 2000
MIN_EVENTS = 10
OUTER_REPEATS = 6
OUTER_FOLDS = 5
INNER_FOLDS = 3
PENALTY_GRID = (0.001, 0.01, 0.05, 0.10, 0.50, 1.00)
DCA_THRESHOLDS = (0.05, 0.075, 0.10)
MMOL_TO_MGDL_CHOL = 38.67
LPA_EXPLORATORY_DIVISOR = 2.15

EXPECTED_COHORT_SHA256 = (
    "8c3a1e0598770c1beefe29db28d42fb7074f233f382c25c19eb0c843b59f49b2"
)
EXPECTED = {
    "n_carriers": 3540,
    "n_prevalent": 207,
    "n_undated": 124,
    "n_frozen": 3209,
    "events_full": 289,
    "events_5y": 97,
    "events_10y": 194,
}
PRIMARY_ENDPOINT = "I21|I25|I63|I70|I73|G45; I50 excluded"
SPEC_PRIMARY = (
    "age",
    "sp50",
    "male",
    "bpmed",
    "dm",
    "smoke_curr",
    "cum_nonhdl",
    "log_tghdl",
    "log_lpa",
)
SPEC_GREY = (
    "age",
    "sp50",
    "male",
    "bpmed",
    "dm",
    "smoke_curr",
    "log_apob_hdl",
    "log_tghdl",
    "log_lpa",
)
BINARY_TERMS = ("male", "bpmed", "dm", "smoke_curr")
CONTINUOUS_PRIMARY = tuple(x for x in SPEC_PRIMARY if x not in BINARY_TERMS)
LP_REFERENCE_RAW = {
    "age": 50.0,
    "sp50": 0.0,
    "male": 0.0,
    "bpmed": 0.0,
    "dm": 0.0,
    "smoke_curr": 0.0,
    "cum_nonhdl": 0.0,
    "log_apob_hdl": 0.0,
    "log_tghdl": 0.0,
    "log_lpa": 0.0,
}

# The settlement cell generated the locked SHA from these pre-Cycle-2 columns.
# Selecting this exact set prevents derived Cycle-2 columns from changing it.
LEGACY_HASH_COLUMNS = (
    "time_years",
    "event",
    "age",
    "male",
    "htn_any",
    "smoke_curr",
    "smoke_ever",
    "bmi",
    "hdl",
    "tc",
    "ldl",
    "lpa_nmol",
    "dm",
    "on_statin",
    "ldl_unt",
    "tc_unt",
    "nonhdl_unt",
)

SPEC_LOCK = {
    "model": "CALON-G Cycle 2",
    "endpoint": PRIMARY_ENDPOINT,
    "primary_horizon": "full follow-up",
    "sensitivity_horizon_years": 5,
    "primary_features": list(SPEC_PRIMARY),
    "grey_features": list(SPEC_GREY),
    "estimator": "ridge Cox; penalty selected by nested training-fold CV",
    "missing_data": "continuous median and binary mode within training folds",
    "outer_validation": f"{OUTER_REPEATS} repeats of {OUTER_FOLDS}-fold OOF CV",
    "penalty_grid": list(PENALTY_GRID),
    "oof_lp_reference_raw": LP_REFERENCE_RAW,
    "bootstrap_B": B_BOOT,
    "seed": SEED,
}


def _sha_json(obj: Any) -> str:
    payload = json.dumps(obj, sort_keys=True, default=str, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


SPEC_SHA256 = _sha_json(SPEC_LOCK)


def _installed_version(package: str) -> str:
    try:
        return package_version(package)
    except PackageNotFoundError:
        return "NOT_INSTALLED"


# ---------------------------------------------------------------------------
# Aggregate-only output guard
BANNED_OUTPUT_NAMES = {
    "eid",
    "participant_id",
    "familynumber",
    "databasenumber",
    "nhsnumber",
    "date_of_birth",
    "dob",
    "postcode",
    "variant_id",
}
CYCLE2_OUTPUT_FILES = {
    "findings_lock.json",
    "horizon_proof.csv",
    "predictor_diagnostics.csv",
    "calong_model_summary.json",
    "calong_outer_fold_summary.csv",
    "calong_grey_summary.json",
    "calong_wales_reduced_summary.json",
    "comparator_evaluability.csv",
    "calong_headtohead_full.csv",
    "headtohead_gate.json",
    "calibration_summary.csv",
    "calibration_bins.csv",
    "calibration_oof.png",
    "dca_10y.csv",
    "wales_filter_ledger.csv",
    "wales_transport.json",
    "wales_calibration_summary.csv",
    "wales_calibration_bins.csv",
    "tripod_ai_checklist.csv",
    "strobe_flow.csv",
    "run_meta.json",
}


def require_fresh_output_dir(path: Path) -> None:
    """Prevent evidence from a failed rerun mixing with an older run."""
    if not path.exists():
        return
    stale = sorted(name for name in CYCLE2_OUTPUT_FILES if (path / name).exists())
    if stale:
        raise RuntimeError(
            f"CYCLE2_OUT must be fresh; existing Cycle-2 artefacts found: {stale}. "
            "Choose a new output directory; this engine never deletes prior evidence."
        )


def _check_aggregate_object(obj: Any, label: str = "output") -> None:
    """Reject identifier-bearing or participant-length material before output."""
    if isinstance(obj, pd.DataFrame):
        bad = BANNED_OUTPUT_NAMES.intersection(str(c).lower() for c in obj.columns)
        if bad:
            raise RuntimeError(f"aggregate guard: banned columns in {label}: {sorted(bad)}")
        if len(obj) > 500:
            raise RuntimeError(f"aggregate guard: {label} has {len(obj)} rows")
        return
    if isinstance(obj, pd.Series):
        if len(obj) > 500:
            raise RuntimeError(f"aggregate guard: {label} has {len(obj)} values")
        return
    if isinstance(obj, np.ndarray):
        if obj.size > 500:
            raise RuntimeError(f"aggregate guard: participant-length array in {label}")
        return
    if isinstance(obj, Mapping):
        for key, value in obj.items():
            if str(key).lower() in BANNED_OUTPUT_NAMES:
                raise RuntimeError(f"aggregate guard: banned key in {label}")
            _check_aggregate_object(value, f"{label}.{key}")
        return
    if isinstance(obj, (list, tuple)):
        if len(obj) > 500:
            raise RuntimeError(f"aggregate guard: overlong sequence in {label}")
        for i, value in enumerate(obj):
            _check_aggregate_object(value, f"{label}[{i}]")


def emit_aggregate(obj: Any, title: str = "") -> None:
    _check_aggregate_object(obj, title or "output")
    if title:
        print(f"\n=== {title} ===")
    if isinstance(obj, pd.DataFrame):
        print(obj.to_string(index=False))
    else:
        print(json.dumps(_json_ready(obj), indent=2, default=str, allow_nan=False))


def write_aggregate_csv(frame: pd.DataFrame, path: Path) -> None:
    _check_aggregate_object(frame, path.name)
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False)


def write_aggregate_json(obj: Any, path: Path) -> None:
    _check_aggregate_object(obj, path.name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(_json_ready(obj), indent=2, default=str, allow_nan=False) + "\n",
        encoding="utf-8",
    )


def _json_ready(obj: Any) -> Any:
    """Convert numpy scalars and non-finite floats to strict-JSON values."""
    if isinstance(obj, Mapping):
        return {str(key): _json_ready(value) for key, value in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_json_ready(value) for value in obj]
    if isinstance(obj, np.generic):
        return _json_ready(obj.item())
    if isinstance(obj, float) and not math.isfinite(obj):
        return None
    return obj


# ---------------------------------------------------------------------------
# Frozen-cohort and horizon gates
def require_columns(frame: pd.DataFrame, columns: Sequence[str], label: str) -> None:
    missing = [c for c in columns if c not in frame.columns]
    if missing:
        raise KeyError(f"{label} missing required columns: {missing}")


def _binary_event_array(values: Sequence[Any], label: str = "event") -> np.ndarray:
    """Parse an event indicator without silently truncating non-binary floats."""
    try:
        raw = np.asarray(values, dtype=float)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be numeric binary 0/1") from exc
    if raw.ndim != 1:
        raise ValueError(f"{label} must be one-dimensional")
    if not np.isfinite(raw).all():
        raise ValueError(f"{label} must be finite binary 0/1")
    if not set(np.unique(raw)).issubset({0.0, 1.0}):
        raise ValueError(f"{label} must be binary 0/1 before integer conversion")
    return raw.astype(int)


def legacy_cohort_sha256(frozen: pd.DataFrame) -> str:
    """Reproduce the settlement cell's pre-Cycle-2 cohort signature."""
    require_columns(frozen, LEGACY_HASH_COLUMNS, "FROZEN SHA input")
    missingness = {
        c: float(frozen[c].isna().mean().round(4)) for c in LEGACY_HASH_COLUMNS
    }
    obj = {
        "n": len(frozen),
        "events": int(pd.to_numeric(frozen["event"], errors="raise").sum()),
        "cols": sorted(LEGACY_HASH_COLUMNS),
        "missingness": missingness,
    }
    # This intentionally matches the earlier helper, including default spacing.
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, default=str).encode("utf-8")
    ).hexdigest()


def _normalise_ledger(ledger: Mapping[str, Any]) -> dict[str, int]:
    aliases = {
        "n_carriers": ("n_carriers", "ukb_carriers", "carriers"),
        "n_prevalent": ("n_prevalent", "prevalent", "prevalent_excluded"),
        "n_undated": ("n_undated", "undated", "undated_excluded"),
        "n_frozen": ("n_frozen", "risk_set", "frozen"),
    }
    out: dict[str, int] = {}
    for target, names in aliases.items():
        found = [ledger[n] for n in names if n in ledger]
        if len(found) != 1:
            raise KeyError(
                f"COHORT_LEDGER must supply exactly one of {names} for {target}"
            )
        out[target] = int(found[0])
    return out


def resolve_cohort_sha256(
    frozen: pd.DataFrame, observed_sha: str | None = None
) -> str:
    supplied = observed_sha or frozen.attrs.get("cohort_sha256")
    recomputed: str | None = None
    if set(LEGACY_HASH_COLUMNS).issubset(frozen.columns):
        recomputed = legacy_cohort_sha256(frozen)
    if supplied is None and recomputed is None:
        raise RuntimeError(
            "No actual cohort SHA supplied and the legacy SHA columns are incomplete. "
            "Pass the upstream COHORT_HASH; never paste the expected hash as the observed one."
        )
    if supplied is not None and recomputed is not None and str(supplied) != recomputed:
        raise AssertionError(
            "supplied cohort SHA disagrees with the settlement-signature recomputation"
        )
    return str(supplied or recomputed)


def horizon_risk_set(
    time: Sequence[float], event: Sequence[int], horizon: float
) -> tuple[np.ndarray, np.ndarray]:
    """Administrative censoring at ``horizon`` without removing survivors."""
    t = np.asarray(time, dtype=float)
    e = _binary_event_array(event)
    if t.ndim != 1 or e.ndim != 1 or len(t) != len(e):
        raise ValueError("time and event must be equal-length one-dimensional arrays")
    if not np.isfinite(t).all() or np.any(t <= 0):
        raise ValueError("follow-up times must be finite and positive")
    h = float(horizon)
    if not np.isfinite(h) or h <= 0:
        raise ValueError("horizon must be finite and positive")
    t_h = np.minimum(t, h)
    e_h = ((e == 1) & (t <= h)).astype(int)
    return t_h, e_h


def validate_frozen_lock(
    frozen: pd.DataFrame,
    ledger: Mapping[str, Any],
    observed_sha: str | None = None,
) -> dict[str, Any]:
    require_columns(frozen, ("time_years", "event"), "FROZEN")
    flow = _normalise_ledger(ledger)
    for key, value in flow.items():
        if value != EXPECTED[key]:
            raise AssertionError(f"{key}: got {value}, expected {EXPECTED[key]}")
    if len(frozen) != EXPECTED["n_frozen"]:
        raise AssertionError(
            f"frozen n: got {len(frozen)}, expected {EXPECTED['n_frozen']}"
        )
    t = pd.to_numeric(frozen["time_years"], errors="raise").to_numpy(float)
    e = _binary_event_array(
        pd.to_numeric(frozen["event"], errors="raise").to_numpy(), "FROZEN.event"
    )
    if int(e.sum()) != EXPECTED["events_full"]:
        raise AssertionError(
            f"full events: got {int(e.sum())}, expected {EXPECTED['events_full']}"
        )
    _, e5 = horizon_risk_set(t, e, 5.0)
    _, e10 = horizon_risk_set(t, e, 10.0)
    if int(e5.sum()) != EXPECTED["events_5y"]:
        raise AssertionError(
            f"5-year events: got {int(e5.sum())}, expected {EXPECTED['events_5y']}"
        )
    if int(e10.sum()) != EXPECTED["events_10y"]:
        raise AssertionError(
            f"10-year events: got {int(e10.sum())}, expected {EXPECTED['events_10y']}"
        )
    actual_sha = resolve_cohort_sha256(frozen, observed_sha)
    if actual_sha != EXPECTED_COHORT_SHA256:
        raise AssertionError(
            f"cohort SHA mismatch: got {actual_sha}, expected {EXPECTED_COHORT_SHA256}"
        )
    return {
        **flow,
        "events_full": int(e.sum()),
        "events_5y": int(e5.sum()),
        "events_10y": int(e10.sum()),
        "cohort_sha256": actual_sha,
        "endpoint": PRIMARY_ENDPOINT,
        "status": "PASS",
    }


# ---------------------------------------------------------------------------
# Fold-wise preprocessing and ridge Cox
@dataclass(frozen=True)
class Preprocessor:
    features: tuple[str, ...]
    continuous: tuple[str, ...]
    binary: tuple[str, ...]
    fill: dict[str, float]
    mean: dict[str, float]
    scale: dict[str, float]


@dataclass
class FrozenCoxBundle:
    label: str
    features: tuple[str, ...]
    preprocessor: Preprocessor
    penalty: float
    coefficients: dict[str, float]
    cox_center: dict[str, float]
    baseline_survival: dict[str, float]
    model: CoxPHFitter
    ph_summary: list[dict[str, Any]]

    def aggregate_dict(self) -> dict[str, Any]:
        return {
            "label": self.label,
            "features": list(self.features),
            "penalty": self.penalty,
            "coefficients_scaled": self.coefficients,
            "cox_center": self.cox_center,
            "imputation": self.preprocessor.fill,
            "continuous_mean": self.preprocessor.mean,
            "continuous_scale": self.preprocessor.scale,
            "baseline_survival": self.baseline_survival,
            "ph_test": self.ph_summary,
        }


@dataclass
class OOFFit:
    label: str
    features: tuple[str, ...]
    lp: np.ndarray
    risk5: np.ndarray
    risk10: np.ndarray
    coverage: np.ndarray
    splits: list[tuple[int, int, np.ndarray, np.ndarray]]
    fold_summary: pd.DataFrame
    final_bundle: FrozenCoxBundle
    c_index: float

    def aggregate_dict(self) -> dict[str, Any]:
        return {
            "label": self.label,
            "features": list(self.features),
            "n_oof": int(np.isfinite(self.lp).sum()),
            "coverage_min": int(self.coverage.min()),
            "coverage_max": int(self.coverage.max()),
            "C_oof_pooled_lp": self.c_index,
            "OOF_LP_anchor": (
                "each outer-fold LP is re-anchored to the locked common raw reference "
                "before pooling across folds/repeats"
            ),
            "OOF_LP_reference_raw": {
                term: LP_REFERENCE_RAW[term] for term in self.features
            },
            "outer_folds": int(len(self.fold_summary)),
            "selected_penalty_counts": {
                str(k): int(v)
                for k, v in self.fold_summary["penalty"].value_counts().sort_index().items()
            },
            "final_model": self.final_bundle.aggregate_dict(),
            "missingness": "training-fold median continuous / mode binary; NOT MCAR",
        }


def build_calong_frame(
    frozen: pd.DataFrame, features: Sequence[str] = SPEC_PRIMARY
) -> pd.DataFrame:
    """Construct the locked model frame without changing cohort membership."""
    features = tuple(features)
    if features not in (SPEC_PRIMARY, SPEC_GREY, tuple(x for x in SPEC_PRIMARY if x != "log_lpa")):
        raise ValueError("unregistered CALON-G feature set; do not retune the SPEC")
    require_columns(
        frozen,
        ("time_years", "event", "age", "male", "bpmed", "dm", "smoke_curr"),
        "FROZEN CALON-G",
    )
    out = pd.DataFrame(index=frozen.index)
    out["age"] = pd.to_numeric(frozen["age"], errors="coerce")
    derived_sp50 = (out["age"] - 50.0).clip(lower=0.0)
    if "sp50" in frozen:
        supplied = pd.to_numeric(frozen["sp50"], errors="coerce")
        both = supplied.notna() & derived_sp50.notna()
        if both.any() and not np.allclose(
            supplied[both], derived_sp50[both], rtol=0.0, atol=1e-10
        ):
            raise AssertionError("supplied sp50 is not max(age - 50, 0)")
    out["sp50"] = derived_sp50
    for column in ("male", "bpmed", "dm", "smoke_curr", "cum_nonhdl", "log_tghdl"):
        if column in features:
            require_columns(frozen, (column,), "FROZEN CALON-G")
            out[column] = pd.to_numeric(frozen[column], errors="coerce")
    if "log_lpa" in features:
        supplied_log = (
            pd.to_numeric(frozen["log_lpa"], errors="coerce")
            if "log_lpa" in frozen
            else pd.Series(np.nan, index=frozen.index, dtype=float)
        )
        native = (
            pd.to_numeric(frozen["lpa_nmol"], errors="coerce")
            if "lpa_nmol" in frozen
            else pd.Series(np.nan, index=frozen.index, dtype=float)
        )
        if (native.dropna() < 0).any():
            raise ValueError("negative native Lp(a); resolve assay coding upstream")
        both = supplied_log.notna() & native.notna()
        if (supplied_log.dropna() < 0).any():
            raise ValueError("log_lpa cannot be negative for log1p(nonnegative Lp(a))")
        if both.any() and not np.allclose(
            supplied_log[both], np.log1p(native[both]), rtol=1e-7, atol=1e-9
        ):
            raise AssertionError("log_lpa disagrees with log1p(lpa_nmol)")
        if supplied_log.notna().any():
            out["log_lpa"] = supplied_log.combine_first(np.log1p(native))
        elif native.notna().any():
            if (native.dropna() < 0).any():
                raise ValueError("negative native Lp(a); resolve assay coding upstream")
            out["log_lpa"] = np.log1p(native)
        else:
            raise KeyError("CALON-G requires usable log_lpa or native lpa_nmol")
    if "log_apob_hdl" in features:
        require_columns(frozen, ("log_apob_hdl",), "CALON-G-grey")
        out["log_apob_hdl"] = pd.to_numeric(
            frozen["log_apob_hdl"], errors="coerce"
        )
    out = out.loc[:, list(features)].replace([np.inf, -np.inf], np.nan)
    for column in set(features).intersection(BINARY_TERMS):
        values = set(out[column].dropna().unique())
        if not values.issubset({0, 1, 0.0, 1.0}):
            raise ValueError(f"{column} is not binary 0/1: {sorted(values)}")
    out["T"] = pd.to_numeric(frozen["time_years"], errors="raise").to_numpy(float)
    out["E"] = _binary_event_array(
        pd.to_numeric(frozen["event"], errors="raise").to_numpy(), "FROZEN.event"
    )
    return out


def predictor_diagnostics(frozen: pd.DataFrame) -> pd.DataFrame:
    """Aggregate prespecified collinearity diagnostics; never alter the SPEC."""
    require_columns(frozen, ("age", "cum_nonhdl"), "predictor diagnostics")
    age = pd.to_numeric(frozen["age"], errors="coerce")
    burden = pd.to_numeric(frozen["cum_nonhdl"], errors="coerce")
    finite = age.notna() & burden.notna() & np.isfinite(age) & np.isfinite(burden)
    correlation = float(age[finite].corr(burden[finite])) if int(finite.sum()) > 1 else float("nan")
    return pd.DataFrame(
        [
            {
                "pair": "age vs cum_nonhdl",
                "n_complete": int(finite.sum()),
                "pearson_r": correlation,
                "spec_kit_reference_r": 0.577,
                "action": "REPORT; DO NOT DROP OR RETUNE THE FROZEN SPEC",
            }
        ]
    )


def _groups_from_frame(frame: pd.DataFrame) -> np.ndarray:
    for name in ("FamilyNumber", "cluster"):
        if name in frame.columns:
            raw = frame[name].astype(object).to_numpy(copy=True)
            missing = pd.isna(raw)
            if missing.any():
                for i in np.flatnonzero(missing):
                    raw[i] = ("row", int(i))
            return raw
    return np.arange(len(frame), dtype=int)


def make_group_folds(
    groups: Sequence[Any], event: Sequence[int], n_splits: int, seed: int
) -> np.ndarray:
    """Deterministic event/size-balanced group folds; groups never cross folds."""
    grp = np.asarray(groups, dtype=object)
    evt = np.asarray(event, dtype=int)
    if len(grp) != len(evt):
        raise ValueError("group and event lengths differ")
    codes, uniques = pd.factorize(pd.Series(grp), sort=False)
    if len(uniques) < n_splits:
        raise ValueError("fewer independent groups than requested folds")
    g_n = np.bincount(codes, minlength=len(uniques)).astype(float)
    g_e = np.bincount(codes, weights=evt, minlength=len(uniques)).astype(float)
    rng = np.random.default_rng(seed)
    jitter = rng.random(len(uniques))
    order = np.lexsort((jitter, -g_n, -g_e))
    fold_n = np.zeros(n_splits, dtype=float)
    fold_e = np.zeros(n_splits, dtype=float)
    assignment = np.full(len(uniques), -1, dtype=int)
    target_n = max(len(evt) / n_splits, 1.0)
    target_e = max(evt.sum() / n_splits, 1.0)
    for position, group_code in enumerate(order):
        if position < n_splits:
            fold = position
        else:
            score = ((fold_n + g_n[group_code]) / target_n) ** 2
            score += ((fold_e + g_e[group_code]) / target_e) ** 2
            fold = int(np.argmin(score + rng.random(n_splits) * 1e-12))
        assignment[group_code] = fold
        fold_n[fold] += g_n[group_code]
        fold_e[fold] += g_e[group_code]
    folds = assignment[codes]
    if set(np.unique(folds)) != set(range(n_splits)):
        raise AssertionError("fold construction left an empty fold")
    return folds


def fit_preprocessor(
    x_train: pd.DataFrame,
    features: Sequence[str],
    continuous: Sequence[str],
    binary: Sequence[str],
) -> Preprocessor:
    features = tuple(features)
    continuous = tuple(continuous)
    binary = tuple(binary)
    require_columns(x_train, features, "training predictors")
    fill: dict[str, float] = {}
    mean: dict[str, float] = {}
    scale: dict[str, float] = {}
    for column in features:
        s = pd.to_numeric(x_train[column], errors="coerce").replace(
            [np.inf, -np.inf], np.nan
        )
        if s.notna().sum() == 0:
            raise ValueError(f"{column} is wholly unavailable in a training fold")
        if column in binary:
            modes = s.mode(dropna=True)
            if modes.empty:
                raise ValueError(f"no training-fold mode for {column}")
            fill[column] = float(modes.iloc[0])
            mean[column], scale[column] = 0.0, 1.0
        else:
            if column == "sp50" and "age" in features:
                if "age" not in fill:
                    raise AssertionError("age must precede sp50 in the frozen SPEC")
                fill[column] = max(fill["age"] - 50.0, 0.0)
            else:
                fill[column] = float(s.median())
            completed = s.fillna(fill[column])
            mean[column] = float(completed.mean())
            sd = float(completed.std(ddof=0))
            scale[column] = sd if np.isfinite(sd) and sd > 1e-12 else 1.0
    return Preprocessor(features, continuous, binary, fill, mean, scale)


def apply_preprocessor(frame: pd.DataFrame, prep: Preprocessor) -> pd.DataFrame:
    require_columns(frame, prep.features, "predictor frame")
    out = pd.DataFrame(index=frame.index)
    for column in prep.features:
        s = pd.to_numeric(frame[column], errors="coerce").replace(
            [np.inf, -np.inf], np.nan
        )
        s = s.fillna(prep.fill[column])
        if column in prep.continuous:
            s = (s - prep.mean[column]) / prep.scale[column]
        out[column] = s.astype(float)
    if not np.isfinite(out.to_numpy()).all():
        raise ValueError("non-finite value remains after preprocessing")
    return out


def _fit_cox(
    x: pd.DataFrame, time: np.ndarray, event: np.ndarray, penalty: float
) -> CoxPHFitter:
    train = x.copy()
    train["T"] = time
    train["E"] = event
    model = CoxPHFitter(penalizer=float(penalty), l1_ratio=0.0)
    model.fit(train, duration_col="T", event_col="E", show_progress=False)
    return model


def _baseline_survival_at(model: CoxPHFitter, horizon: float) -> float:
    sf = model.baseline_survival_.iloc[:, 0]
    times = sf.index.to_numpy(float)
    pos = int(np.searchsorted(times, float(horizon), side="right") - 1)
    return 1.0 if pos < 0 else float(sf.iloc[min(pos, len(sf) - 1)])


def _predict_lp_and_risk(
    model: CoxPHFitter, x: pd.DataFrame, horizon: float
) -> tuple[np.ndarray, np.ndarray]:
    lp = model.predict_log_partial_hazard(x).to_numpy(float)
    s0 = _baseline_survival_at(model, horizon)
    risk = 1.0 - np.power(s0, np.exp(lp))
    return lp, np.clip(risk, 0.0, 1.0)


def _c_index(time: np.ndarray, event: np.ndarray, score: np.ndarray) -> float:
    return float(concordance_index(time, -score, event))


def select_penalty_nested(
    x: pd.DataFrame,
    time: np.ndarray,
    event: np.ndarray,
    groups: np.ndarray,
    features: Sequence[str],
    continuous: Sequence[str],
    binary: Sequence[str],
    seed: int,
) -> tuple[float, list[dict[str, Any]]]:
    folds = make_group_folds(groups, event, INNER_FOLDS, seed)
    diagnostics: list[dict[str, Any]] = []
    for penalty in PENALTY_GRID:
        values: list[float] = []
        failures = 0
        for fold in range(INNER_FOLDS):
            tr = np.flatnonzero(folds != fold)
            va = np.flatnonzero(folds == fold)
            if int(event[tr].sum()) < MIN_EVENTS or int(event[va].sum()) < 2:
                failures += 1
                continue
            try:
                prep = fit_preprocessor(
                    x.iloc[tr], features, continuous, binary
                )
                xtr = apply_preprocessor(x.iloc[tr], prep)
                xva = apply_preprocessor(x.iloc[va], prep)
                model = _fit_cox(xtr, time[tr], event[tr], penalty)
                lp = model.predict_log_partial_hazard(xva).to_numpy(float)
                values.append(_c_index(time[va], event[va], lp))
            except Exception:
                failures += 1
        diagnostics.append(
            {
                "penalty": float(penalty),
                "mean_inner_C": float(np.mean(values)) if values else float("nan"),
                "valid_inner_folds": len(values),
                "failed_inner_folds": failures,
            }
        )
    valid = [
        row
        for row in diagnostics
        if np.isfinite(row["mean_inner_C"])
        and row["valid_inner_folds"] == INNER_FOLDS
    ]
    if not valid:
        raise RuntimeError("no ridge penalty completed every inner fold")
    # Maximise inner C; exact ties favour stronger shrinkage.
    chosen = max(valid, key=lambda row: (row["mean_inner_C"], row["penalty"]))
    return float(chosen["penalty"]), diagnostics


def _ph_summary(model: CoxPHFitter, train: pd.DataFrame) -> list[dict[str, Any]]:
    try:
        result = proportional_hazard_test(model, train, time_transform="rank").summary
    except Exception as exc:
        return [{"term": "MODEL", "status": f"PH_TEST_FAILED: {type(exc).__name__}"}]
    rows = []
    for term, row in result.iterrows():
        rows.append(
            {
                "term": str(term),
                "test_statistic": float(row["test_statistic"]),
                "p": float(row["p"]),
                "status": "FLAG_P_LT_0.05" if float(row["p"]) < 0.05 else "PASS",
            }
        )
    return rows


def fit_calong_oof(
    frozen: pd.DataFrame,
    features: Sequence[str] = SPEC_PRIMARY,
    label: str = "CALON-G-primary",
) -> OOFFit:
    features = tuple(features)
    design = build_calong_frame(frozen, features)
    continuous = tuple(x for x in features if x not in BINARY_TERMS)
    binary = tuple(x for x in features if x in BINARY_TERMS)
    x = design.loc[:, list(features)]
    time = design["T"].to_numpy(float)
    event = design["E"].to_numpy(int)
    groups = _groups_from_frame(frozen)

    n = len(design)
    lp_sum = np.zeros(n, dtype=float)
    r5_sum = np.zeros(n, dtype=float)
    r10_sum = np.zeros(n, dtype=float)
    coverage = np.zeros(n, dtype=int)
    splits: list[tuple[int, int, np.ndarray, np.ndarray]] = []
    fold_rows: list[dict[str, Any]] = []

    for repeat in range(OUTER_REPEATS):
        outer = make_group_folds(groups, event, OUTER_FOLDS, SEED + repeat)
        repeat_seen = np.zeros(n, dtype=bool)
        for fold in range(OUTER_FOLDS):
            tr = np.flatnonzero(outer != fold)
            te = np.flatnonzero(outer == fold)
            if int(event[tr].sum()) < MIN_EVENTS or int(event[te].sum()) < 2:
                raise RuntimeError(
                    f"outer repeat {repeat} fold {fold} lacks enough events"
                )
            penalty, inner = select_penalty_nested(
                x.iloc[tr].reset_index(drop=True),
                time[tr],
                event[tr],
                groups[tr],
                features,
                continuous,
                binary,
                SEED + 1000 * repeat + fold,
            )
            prep = fit_preprocessor(x.iloc[tr], features, continuous, binary)
            xtr = apply_preprocessor(x.iloc[tr], prep)
            xte = apply_preprocessor(x.iloc[te], prep)
            model = _fit_cox(xtr, time[tr], event[tr], penalty)
            lp, r5 = _predict_lp_and_risk(model, xte, 5.0)
            _, r10 = _predict_lp_and_risk(model, xte, 10.0)
            reference_raw = pd.DataFrame(
                [{term: LP_REFERENCE_RAW[term] for term in features}]
            )
            reference_x = apply_preprocessor(reference_raw, prep)
            reference_lp = float(
                model.predict_log_partial_hazard(reference_x).to_numpy(float)[0]
            )
            lp = lp - reference_lp
            if not (np.isfinite(lp).all() and np.isfinite(r5).all() and np.isfinite(r10).all()):
                raise RuntimeError("non-finite OOF prediction")
            lp_sum[te] += lp
            r5_sum[te] += r5
            r10_sum[te] += r10
            coverage[te] += 1
            repeat_seen[te] = True
            splits.append((repeat, fold, tr, te))
            fold_rows.append(
                {
                    "repeat": repeat,
                    "fold": fold,
                    "n_train": len(tr),
                    "events_train": int(event[tr].sum()),
                    "n_test": len(te),
                    "events_test": int(event[te].sum()),
                    "penalty": penalty,
                    "LP_anchor_reference_prediction": reference_lp,
                    "inner_candidate_failures": int(
                        sum(row["failed_inner_folds"] for row in inner)
                    ),
                    "C_test": _c_index(time[te], event[te], lp),
                }
            )
        if not repeat_seen.all():
            raise RuntimeError(f"repeat {repeat} did not predict every participant")
    if not np.all(coverage == OUTER_REPEATS):
        raise RuntimeError(
            f"OOF coverage is not exactly {OUTER_REPEATS} for every participant"
        )
    lp = lp_sum / coverage
    risk5 = r5_sum / coverage
    risk10 = r10_sum / coverage

    final_penalty, _ = select_penalty_nested(
        x.reset_index(drop=True),
        time,
        event,
        groups,
        features,
        continuous,
        binary,
        SEED + 900000,
    )
    prep = fit_preprocessor(x, features, continuous, binary)
    x_full = apply_preprocessor(x, prep)
    final_model = _fit_cox(x_full, time, event, final_penalty)
    train_for_ph = x_full.copy()
    train_for_ph["T"] = time
    train_for_ph["E"] = event
    bundle = FrozenCoxBundle(
        label=label,
        features=features,
        preprocessor=prep,
        penalty=final_penalty,
        coefficients={k: float(v) for k, v in final_model.params_.items()},
        cox_center={k: float(v) for k, v in final_model._norm_mean.items()},
        baseline_survival={
            "5y": _baseline_survival_at(final_model, 5.0),
            "10y": _baseline_survival_at(final_model, 10.0),
        },
        model=final_model,
        ph_summary=_ph_summary(final_model, train_for_ph),
    )
    return OOFFit(
        label=label,
        features=features,
        lp=lp,
        risk5=risk5,
        risk10=risk10,
        coverage=coverage,
        splits=splits,
        fold_summary=pd.DataFrame(fold_rows),
        final_bundle=bundle,
        c_index=_c_index(time, event, lp),
    )


# ---------------------------------------------------------------------------
# PDF-faithful comparator equations
SAFEHEART_CENTER = 5.4078
SAFEHEART_S0_5Y = 0.9532
SAFEHEART_S0_10Y = 0.9025
FHRS_CENTER = 3.00
FHRS_S0_10Y = 0.889

COMPARATOR_PROVENANCE = {
    "SAFEHEART-RE": {
        "equation": "PDF_VERIFIED",
        "source": "Perez de Isla 2017, PDF pp5-7, Table 3/worked equation",
        "centring_constant": SAFEHEART_CENTER,
        "input_caveat": (
            "BMI numeric 25/30 cut-points are CANDIDATE: categories are in the PDF, "
            "but numeric boundaries are NOT-IN-PDF"
        ),
    },
    "FH-Risk-Score": {
        "equation": "PDF_VERIFIED",
        "source": "Paquette 2021 supplement PDF p9, Supplemental Table II",
        "centring_constant": FHRS_CENTER,
        "input_caveat": "native age range 18-65; untreated/imputed LDL-C required",
    },
    "Montreal-FH-SCORE": {
        "equation": "PDF_VERIFIED_POINT_CHART",
        "source": "Paquette 2017 derivation PDF p5, Table 3",
        "centring_constant": "NOT-IN-PDF",
        "input_caveat": (
            "ranking only; published model is prevalent-CVD and has no absolute-risk mapping"
        ),
    },
}


@dataclass
class ComparatorSet:
    scores: dict[str, np.ndarray]
    risks: dict[str, dict[int, np.ndarray]]
    audit: pd.DataFrame
    exploratory_lpa_conversion: bool


def safeheart_lp(
    age: np.ndarray,
    male: np.ndarray,
    prior_ascvd: np.ndarray,
    high_bp: np.ndarray,
    bmi: np.ndarray,
    active_smoke: np.ndarray,
    ldl_mgdl: np.ndarray,
    lpa_mgdl: np.ndarray,
) -> np.ndarray:
    """Published categorical LP; prior ASCVD is zero in the locked cohort."""
    lp = 0.70 * male
    lp += 1.07 * ((age >= 30.0) & (age < 60.0))
    lp += 1.45 * (age >= 60.0)
    lp += 0.69 * high_bp
    lp += 1.42 * prior_ascvd
    lp += 0.48 * active_smoke
    # The source names normal/overweight/obesity but does not print 25/30.
    lp += 0.88 * ((bmi >= 25.0) & (bmi < 30.0))
    lp += 0.98 * (bmi >= 30.0)
    lp += 0.92 * ((ldl_mgdl >= 100.0) & (ldl_mgdl < 160.0))
    lp += 1.57 * (ldl_mgdl >= 160.0)
    lp += 0.42 * (lpa_mgdl > 50.0)
    return np.asarray(lp, dtype=float) - SAFEHEART_CENTER


def safeheart_risk(lp_centred: np.ndarray, horizon: int) -> np.ndarray:
    base = {5: SAFEHEART_S0_5Y, 10: SAFEHEART_S0_10Y}.get(int(horizon))
    if base is None:
        raise ValueError("SAFEHEART publishes only 5- and 10-year risk bases")
    return np.clip(1.0 - np.power(base, np.exp(lp_centred)), 0.0, 1.0)


def fhrs_lp(
    age: np.ndarray,
    male: np.ndarray,
    hypertension: np.ndarray,
    active_smoke: np.ndarray,
    ldl_unt_mmol: np.ndarray,
    hdl_mmol: np.ndarray,
    lpa_mgdl: np.ndarray,
) -> np.ndarray:
    age_beta = np.select(
        [
            age <= 30.0,
            age <= 35.0,
            age <= 40.0,
            age <= 45.0,
            age <= 50.0,
            age <= 55.0,
            age <= 60.0,
            age <= 65.0,
        ],
        [0.0, 0.938, 1.383, 1.621, 1.738, 1.804, 1.964, 2.256],
        default=np.nan,
    )
    ldl_beta = np.select(
        [
            ldl_unt_mmol <= 5.50,
            ldl_unt_mmol <= 7.50,
            ldl_unt_mmol <= 8.50,
            ldl_unt_mmol <= 9.50,
        ],
        [0.0, 0.315, 0.718, 0.918],
        default=1.136,
    )
    hdl_beta = np.select(
        [hdl_mmol > 1.30, hdl_mmol > 1.00, hdl_mmol >= 0.85],
        [0.0, 0.298, 0.712],
        default=0.752,
    )
    lp = age_beta + ldl_beta + hdl_beta
    lp += 0.721 * male + 0.644 * hypertension + 0.625 * active_smoke
    lp += 0.434 * (lpa_mgdl >= 50.0)
    lp[(age < 18.0) | (age > 65.0)] = np.nan
    return np.asarray(lp, dtype=float)


def fhrs_risk10(lp: np.ndarray) -> np.ndarray:
    return np.clip(1.0 - np.power(FHRS_S0_10Y, np.exp(lp - FHRS_CENTER)), 0.0, 1.0)


def montreal_points(
    age: np.ndarray,
    male: np.ndarray,
    hypertension: np.ndarray,
    ever_smoke: np.ndarray,
    hdl_mmol: np.ndarray,
) -> np.ndarray:
    age_points = np.select(
        [
            age <= 21.0,
            age <= 28.0,
            age <= 35.0,
            age <= 42.0,
            age <= 49.0,
            age <= 56.0,
            age <= 63.0,
        ],
        [0.0, 4.0, 8.0, 12.0, 16.0, 20.0, 24.0],
        default=28.0,
    )
    hdl_points = np.select(
        [hdl_mmol <= 0.60, hdl_mmol <= 0.90, hdl_mmol <= 1.20, hdl_mmol <= 1.50],
        [12.0, 9.0, 6.0, 3.0],
        default=0.0,
    )
    return np.asarray(
        age_points + hdl_points + 3.0 * male + 2.0 * hypertension + ever_smoke,
        dtype=float,
    )


def _numeric_or_missing(frame: pd.DataFrame, name: str) -> pd.Series:
    if name not in frame:
        return pd.Series(np.nan, index=frame.index, dtype=float)
    return pd.to_numeric(frame[name], errors="coerce").replace([np.inf, -np.inf], np.nan)


def build_comparator_inputs(
    frozen: pd.DataFrame, exploratory_lpa_conversion: bool = False
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Map already-derived cohort columns to published comparator inputs."""
    out = pd.DataFrame(index=frozen.index)
    out["age"] = _numeric_or_missing(frozen, "age")
    out["male"] = _numeric_or_missing(frozen, "male")
    out["active_smoke"] = _numeric_or_missing(frozen, "smoke_curr")
    out["ever_smoke"] = _numeric_or_missing(frozen, "smoke_ever")
    if "safeheart_hbp" in frozen:
        out["hypertension"] = _numeric_or_missing(frozen, "safeheart_hbp")
        htn_source = "safeheart_hbp"
    else:
        out["hypertension"] = _numeric_or_missing(frozen, "htn_any")
        htn_source = "htn_any mapping (measurement-frequency limitation)"
    out["bmi"] = _numeric_or_missing(frozen, "bmi")
    if "ldl_mgdl" in frozen:
        out["ldl_measured_mgdl"] = _numeric_or_missing(frozen, "ldl_mgdl")
        measured_source = "ldl_mgdl"
    else:
        out["ldl_measured_mgdl"] = _numeric_or_missing(frozen, "ldl") * MMOL_TO_MGDL_CHOL
        measured_source = "ldl mmol/L multiplied by 38.67"
    if "ldl_unt_mmol" in frozen:
        out["ldl_unt_mmol"] = _numeric_or_missing(frozen, "ldl_unt_mmol")
    else:
        out["ldl_unt_mmol"] = _numeric_or_missing(frozen, "ldl_unt")
    out["hdl_mmol"] = _numeric_or_missing(frozen, "hdl")
    native_lpa = _numeric_or_missing(frozen, "lpa_mgdl")
    nmol_lpa = _numeric_or_missing(frozen, "lpa_nmol")
    if (native_lpa.dropna() < 0).any() or (nmol_lpa.dropna() < 0).any():
        raise ValueError("negative comparator Lp(a); resolve assay coding upstream")
    conversion_used = False
    if native_lpa.notna().any():
        out["lpa_mgdl"] = native_lpa
        lpa_source = "native lpa_mgdl"
    elif exploratory_lpa_conversion and nmol_lpa.notna().any():
        out["lpa_mgdl"] = nmol_lpa / LPA_EXPLORATORY_DIVISOR
        lpa_source = "EXPLORATORY nmol/L divided by 2.15"
        conversion_used = True
    else:
        out["lpa_mgdl"] = np.nan
        lpa_source = "NOT_EVALUABLE: native mg/dL unavailable"
    for column in ("male", "active_smoke", "ever_smoke", "hypertension"):
        values = set(out[column].dropna().unique())
        if not values.issubset({0, 1, 0.0, 1.0}):
            raise ValueError(f"comparator input {column} is not binary")
    return out, {
        "hypertension": htn_source,
        "measured_ldl": measured_source,
        "lpa": lpa_source,
        "lpa_conversion_used": conversion_used,
    }


COMPARATOR_FIELDS = {
    "SAFEHEART-RE": {
        "continuous": ("age", "bmi", "ldl_measured_mgdl", "lpa_mgdl"),
        "binary": ("male", "hypertension", "active_smoke"),
    },
    "FH-Risk-Score": {
        "continuous": ("age", "ldl_unt_mmol", "hdl_mmol", "lpa_mgdl"),
        "binary": ("male", "hypertension", "active_smoke"),
    },
    "Montreal-FH-SCORE": {
        "continuous": ("age", "hdl_mmol"),
        "binary": ("male", "hypertension", "ever_smoke"),
    },
}


def _score_comparator(name: str, x: pd.DataFrame) -> tuple[np.ndarray, dict[int, np.ndarray]]:
    a = {c: x[c].to_numpy(float) for c in x.columns}
    if name == "SAFEHEART-RE":
        lp = safeheart_lp(
            a["age"],
            a["male"],
            np.zeros(len(x), dtype=float),
            a["hypertension"],
            a["bmi"],
            a["active_smoke"],
            a["ldl_measured_mgdl"],
            a["lpa_mgdl"],
        )
        return lp, {5: safeheart_risk(lp, 5), 10: safeheart_risk(lp, 10)}
    if name == "FH-Risk-Score":
        lp = fhrs_lp(
            a["age"],
            a["male"],
            a["hypertension"],
            a["active_smoke"],
            a["ldl_unt_mmol"],
            a["hdl_mmol"],
            a["lpa_mgdl"],
        )
        return lp, {10: fhrs_risk10(lp)}
    if name == "Montreal-FH-SCORE":
        return (
            montreal_points(
                a["age"],
                a["male"],
                a["hypertension"],
                a["ever_smoke"],
                a["hdl_mmol"],
            ),
            {},
        )
    raise KeyError(name)


def score_comparators_oof(
    frozen: pd.DataFrame,
    splits: Sequence[tuple[int, int, np.ndarray, np.ndarray]],
    exploratory_lpa_conversion: bool = False,
) -> ComparatorSet:
    raw, mapping = build_comparator_inputs(frozen, exploratory_lpa_conversion)
    conversion_used = bool(mapping["lpa_conversion_used"])
    n = len(raw)
    score_sum = {name: np.zeros(n, dtype=float) for name in COMPARATOR_FIELDS}
    score_count = {name: np.zeros(n, dtype=int) for name in COMPARATOR_FIELDS}
    risk_sum = {
        "SAFEHEART-RE": {5: np.zeros(n), 10: np.zeros(n)},
        "FH-Risk-Score": {10: np.zeros(n)},
        "Montreal-FH-SCORE": {},
    }
    risk_count = {
        name: {h: np.zeros(n, dtype=int) for h in horizons}
        for name, horizons in risk_sum.items()
    }
    fold_unavailable = {name: 0 for name in COMPARATOR_FIELDS}

    for _repeat, _fold, tr, te in splits:
        for name, fields in COMPARATOR_FIELDS.items():
            features = tuple(fields["continuous"]) + tuple(fields["binary"])
            if any(raw.iloc[tr][column].notna().sum() == 0 for column in features):
                fold_unavailable[name] += 1
                continue
            prep = fit_preprocessor(
                raw.iloc[tr], features, fields["continuous"], fields["binary"]
            )
            test = apply_preprocessor(raw.iloc[te], prep)
            # Comparator coefficients operate in native units; undo scaling.
            for column in fields["continuous"]:
                test[column] = test[column] * prep.scale[column] + prep.mean[column]
            score, risks = _score_comparator(name, test)
            finite = np.isfinite(score)
            idx = te[finite]
            score_sum[name][idx] += score[finite]
            score_count[name][idx] += 1
            for horizon, risk in risks.items():
                good = finite & np.isfinite(risk)
                ridx = te[good]
                risk_sum[name][horizon][ridx] += risk[good]
                risk_count[name][horizon][ridx] += 1

    scores: dict[str, np.ndarray] = {}
    risks_out: dict[str, dict[int, np.ndarray]] = {}
    audit_rows: list[dict[str, Any]] = []
    for name in COMPARATOR_FIELDS:
        score = np.full(n, np.nan)
        complete = score_count[name] == OUTER_REPEATS
        score[complete] = score_sum[name][complete] / score_count[name][complete]
        scores[name] = score
        risks_out[name] = {}
        for horizon in risk_sum[name]:
            risk = np.full(n, np.nan)
            r_complete = risk_count[name][horizon] == OUTER_REPEATS
            risk[r_complete] = (
                risk_sum[name][horizon][r_complete]
                / risk_count[name][horizon][r_complete]
            )
            risks_out[name][horizon] = risk
        finite = np.isfinite(score)
        audit_rows.append(
            {
                "comparator": name,
                "n_evaluable": int(finite.sum()),
                "events": int(pd.to_numeric(frozen.loc[finite, "event"]).sum()),
                "unavailable_outer_folds": fold_unavailable[name],
                "equation_status": COMPARATOR_PROVENANCE[name]["equation"],
                "analysis_label": (
                    "EXPLORATORY_LPA_CONVERSION"
                    if conversion_used and name != "Montreal-FH-SCORE"
                    else "PRIMARY_NATIVE_UNITS"
                ),
                "lpa_input": mapping["lpa"] if name != "Montreal-FH-SCORE" else "not used",
            }
        )
    return ComparatorSet(
        scores=scores,
        risks=risks_out,
        audit=pd.DataFrame(audit_rows),
        exploratory_lpa_conversion=conversion_used,
    )


# ---------------------------------------------------------------------------
# Paired clustered head-to-head
def _cluster_bootstrap_delta(
    time: np.ndarray,
    event: np.ndarray,
    model_score: np.ndarray,
    comparator_score: np.ndarray,
    groups: np.ndarray,
    b: int = B_BOOT,
    seed: int = SEED,
) -> dict[str, Any]:
    if int(b) != B_BOOT:
        raise ValueError(f"confirmatory bootstrap must use B={B_BOOT}")
    codes, uniques = pd.factorize(pd.Series(groups), sort=False)
    members = [np.flatnonzero(codes == i) for i in range(len(uniques))]
    rng = np.random.default_rng(seed)
    observed = _c_index(time, event, model_score) - _c_index(
        time, event, comparator_score
    )
    draws: list[float] = []
    attempts = 0
    max_attempts = max(10 * b, b + 1000)
    while len(draws) < b and attempts < max_attempts:
        attempts += 1
        chosen = rng.integers(0, len(members), len(members))
        idx = np.concatenate([members[j] for j in chosen])
        if int(event[idx].sum()) < MIN_EVENTS:
            continue
        try:
            draws.append(
                _c_index(time[idx], event[idx], model_score[idx])
                - _c_index(time[idx], event[idx], comparator_score[idx])
            )
        except ZeroDivisionError:
            continue
    if len(draws) != b:
        return {
            "delta": observed,
            "lo": float("nan"),
            "hi": float("nan"),
            "B_effective": len(draws),
            "verdict": "NONCONFIRMATORY_BOOTSTRAP_SHORTFALL",
        }
    lo, hi = np.percentile(draws, [2.5, 97.5])
    verdict = "WIN" if lo > 0 else ("LOSS" if hi < 0 else "TIE")
    return {
        "delta": observed,
        "lo": float(lo),
        "hi": float(hi),
        "B_effective": len(draws),
        "verdict": verdict,
    }


def _subgroup_masks(frozen: pd.DataFrame) -> dict[str, np.ndarray | None]:
    n = len(frozen)

    def binary_pair(column: str, yes: str, no: str) -> dict[str, np.ndarray | None]:
        if column not in frozen:
            return {yes: None, no: None}
        values = pd.to_numeric(frozen[column], errors="coerce")
        observed = set(values.dropna().unique())
        if not observed.issubset({0, 1, 0.0, 1.0}):
            raise ValueError(f"subgroup field {column} is not binary 0/1")
        return {yes: values.eq(1).to_numpy(), no: values.eq(0).to_numpy()}

    age = pd.to_numeric(frozen["age"], errors="coerce")
    median_age = float(age.median())
    masks: dict[str, np.ndarray | None] = {
        "ALL": np.ones(n, dtype=bool),
        "male": pd.to_numeric(frozen["male"], errors="coerce").eq(1).to_numpy(),
        "female": pd.to_numeric(frozen["male"], errors="coerce").eq(0).to_numpy(),
        "age<median": age.lt(median_age).to_numpy(),
        "age>=median": age.ge(median_age).to_numpy(),
    }
    masks.update(binary_pair("on_statin", "on statin", "no statin"))
    masks.update(binary_pair("dm", "diabetes", "no diabetes"))
    masks.update(binary_pair("smoke_curr", "current smoker", "not current smoker"))
    masks.update(binary_pair("htn_any", "hypertension", "no hypertension"))
    return masks


def run_headtohead(
    frozen: pd.DataFrame,
    fit: OOFFit,
    comparators: ComparatorSet,
    out_dir: Path,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    expected_names = {"SAFEHEART-RE", "FH-Risk-Score", "Montreal-FH-SCORE"}
    if set(comparators.scores) != expected_names:
        raise AssertionError("head-to-head requires exactly the three locked comparators")
    common = np.isfinite(fit.lp)
    for score in comparators.scores.values():
        common &= np.isfinite(score)
    common_n = int(common.sum())
    common_events = int(pd.to_numeric(frozen.loc[common, "event"]).sum())
    audit = {
        "n_common_evaluable": common_n,
        "events_common_evaluable": common_events,
        "native_lpa_only": not comparators.exploratory_lpa_conversion,
        "cohort_sha256": EXPECTED_COHORT_SHA256,
        "bootstrap_B_required": B_BOOT,
    }
    row_analysis_status = (
        "EXPLORATORY_LPA_CONVERSION"
        if comparators.exploratory_lpa_conversion
        else "PRIMARY_NATIVE_UNITS"
    )
    if common_n == 0 or common_events < MIN_EVENTS:
        write_aggregate_json(
            {**audit, "status": "FAIL_NOT_EVALUABLE"}, out_dir / "headtohead_gate.json"
        )
        raise RuntimeError(
            "common comparator set is not evaluable; native Lp(a) mg/dL may be absent. "
            "Do not silently enable the exploratory conversion."
        )

    time_full = pd.to_numeric(frozen["time_years"], errors="raise").to_numpy(float)
    event_full = _binary_event_array(
        pd.to_numeric(frozen["event"], errors="raise").to_numpy(), "FROZEN.event"
    )
    groups = _groups_from_frame(frozen)
    masks = _subgroup_masks(frozen)
    rows: list[dict[str, Any]] = []
    for comparator_index, (name, comparator_score) in enumerate(comparators.scores.items()):
        for subgroup_index, (subgroup, subgroup_mask) in enumerate(masks.items()):
            for horizon_index, horizon in enumerate(("full", "5y")):
                if subgroup_mask is None:
                    rows.append(
                        {
                            "comparator": name,
                            "subgroup": subgroup,
                            "horizon": horizon,
                            "analysis_status": row_analysis_status,
                            "n_evaluable": 0,
                            "events": 0,
                            "verdict": "NOT_EVALUABLE_MISSING_SUBGROUP_FIELD",
                        }
                    )
                    continue
                selected = common & subgroup_mask
                if horizon == "full":
                    time, event = time_full, event_full
                else:
                    time, event = horizon_risk_set(time_full, event_full, 5.0)
                n_selected = int(selected.sum())
                events_selected = int(event[selected].sum())
                base = {
                    "comparator": name,
                    "subgroup": subgroup,
                    "horizon": horizon,
                    "analysis_status": row_analysis_status,
                    "n_evaluable": n_selected,
                    "events": events_selected,
                }
                if events_selected < MIN_EVENTS or n_selected < 2:
                    rows.append({**base, "verdict": "<10, non-estimable"})
                    continue
                idx = np.flatnonzero(selected)
                model_score = fit.lp[idx]
                comp_score = comparator_score[idx]
                result = _cluster_bootstrap_delta(
                    time[idx],
                    event[idx],
                    model_score,
                    comp_score,
                    groups[idx],
                    b=B_BOOT,
                    seed=(
                        SEED
                        + 100000 * comparator_index
                        + 1000 * subgroup_index
                        + horizon_index
                    ),
                )
                rows.append(
                    {
                        **base,
                        "C_model": _c_index(time[idx], event[idx], model_score),
                        "C_comparator": _c_index(time[idx], event[idx], comp_score),
                        **result,
                    }
                )
    table = pd.DataFrame(rows)
    write_aggregate_csv(table, out_dir / "calong_headtohead_full.csv")
    valid_verdicts = table["verdict"].isin(["WIN", "TIE", "LOSS"])
    tally = table.loc[valid_verdicts, "verdict"].value_counts().to_dict()
    shortfall = bool(
        table["verdict"].eq("NONCONFIRMATORY_BOOTSTRAP_SHORTFALL").any()
    )
    gate = {
        **audit,
        "rows_published": len(table),
        "tally": {str(k): int(v) for k, v in tally.items()},
        "bootstrap_gate": "FAIL" if shortfall else "PASS",
        "analysis_status": (
            "NONCONFIRMATORY_BOOTSTRAP_SHORTFALL"
            if shortfall
            else row_analysis_status
        ),
        "multiplicity_warning": (
            "Dependent subgroup cells; no selective WIN narrative and no universal-win claim."
        ),
        "optimism_warning": (
            "CALON-G is OOF; comparator coefficients are frozen, but input transport and "
            "SAFEHEART BMI cut-points remain explicit limitations."
        ),
        "endpoint": PRIMARY_ENDPOINT,
    }
    write_aggregate_json(gate, out_dir / "headtohead_gate.json")
    return table, gate


# ---------------------------------------------------------------------------
# Censoring-aware calibration and simple survival DCA
def _ipcw_at_horizon(
    time: np.ndarray, event: np.ndarray, horizon: float
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return horizon outcome, IPC weights and known-status mask."""
    _, outcome = horizon_risk_set(time, event, horizon)
    cases = (event == 1) & (time <= horizon)
    known = np.logical_or(cases, time >= horizon)
    km = KaplanMeierFitter()
    km.fit(time, event_observed=(event == 0).astype(int))
    g_h = float(km.predict(float(horizon)))
    if not np.isfinite(g_h) or g_h <= 1e-8:
        raise RuntimeError(f"censoring survival is too small at {horizon} years")
    weight = np.zeros(len(time), dtype=float)
    if cases.any():
        just_before = np.nextafter(time[cases], -np.inf)
        g_case = np.asarray(km.predict(just_before), dtype=float)
        if np.any(g_case <= 1e-8):
            raise RuntimeError("censoring survival is too small before an event")
        weight[cases] = 1.0 / g_case
    controls = known & ~cases
    weight[controls] = 1.0 / g_h
    return outcome.astype(float), weight, known


def _weighted_logistic_irls(
    x: np.ndarray,
    y: np.ndarray,
    weight: np.ndarray,
    offset: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    weight = np.asarray(weight, dtype=float)
    if x.ndim == 1:
        x = x[:, None]
    off = np.zeros(len(y), dtype=float) if offset is None else np.asarray(offset, float)
    beta = np.zeros(x.shape[1], dtype=float)
    for _ in range(100):
        eta = np.clip(off + x @ beta, -35.0, 35.0)
        prob = 1.0 / (1.0 + np.exp(-eta))
        score = x.T @ (weight * (y - prob))
        curvature = weight * prob * (1.0 - prob)
        info = x.T @ (curvature[:, None] * x)
        info = info + np.eye(info.shape[0]) * 1e-10
        step = np.linalg.solve(info, score)
        beta_new = beta + step
        if np.max(np.abs(step)) < 1e-9:
            beta = beta_new
            break
        beta = beta_new
    else:
        raise RuntimeError("weighted calibration model did not converge")
    eta = np.clip(off + x @ beta, -35.0, 35.0)
    prob = 1.0 / (1.0 + np.exp(-eta))
    info = x.T @ ((weight * prob * (1.0 - prob))[:, None] * x)
    cov = np.linalg.pinv(info)
    return beta, cov


def _cluster_sandwich_cov(
    x: np.ndarray,
    y: np.ndarray,
    weight: np.ndarray,
    beta: np.ndarray,
    groups: np.ndarray,
    offset: np.ndarray | None = None,
) -> np.ndarray:
    """Cluster-robust sandwich covariance, conditional on the IPC weights."""
    x = np.asarray(x, dtype=float)
    if x.ndim == 1:
        x = x[:, None]
    y = np.asarray(y, dtype=float)
    weight = np.asarray(weight, dtype=float)
    groups = np.asarray(groups, dtype=object)
    off = np.zeros(len(y), dtype=float) if offset is None else np.asarray(offset, float)
    eta = np.clip(off + x @ np.asarray(beta, dtype=float), -35.0, 35.0)
    prob = 1.0 / (1.0 + np.exp(-eta))
    info = x.T @ ((weight * prob * (1.0 - prob))[:, None] * x)
    bread = np.linalg.pinv(info)
    individual = x * (weight * (y - prob))[:, None]
    codes, uniques = pd.factorize(pd.Series(groups), sort=False)
    if np.any(codes < 0):
        raise ValueError("missing cluster IDs must be normalised before calibration")
    if len(uniques) < 2:
        raise ValueError("cluster-robust calibration requires at least two clusters")
    group_scores = np.zeros((len(uniques), x.shape[1]), dtype=float)
    np.add.at(group_scores, codes, individual)
    meat = group_scores.T @ group_scores
    correction = (len(uniques) / (len(uniques) - 1.0)) * (
        (len(y) - 1.0) / max(len(y) - x.shape[1], 1.0)
    )
    return bread @ (meat * correction) @ bread


def calibration_at_horizon(
    time: np.ndarray,
    event: np.ndarray,
    predicted_risk: np.ndarray,
    horizon: float,
    model_name: str,
    groups: np.ndarray | None = None,
) -> tuple[dict[str, Any], pd.DataFrame]:
    risk = np.asarray(predicted_risk, dtype=float)
    finite = np.isfinite(time) & np.isfinite(event) & np.isfinite(risk)
    time, event, risk = time[finite], event[finite], risk[finite]
    calibration_groups = None if groups is None else np.asarray(groups, dtype=object)[finite]
    if int(((event == 1) & (time <= horizon)).sum()) < MIN_EVENTS:
        raise RuntimeError(f"{model_name} has fewer than {MIN_EVENTS} events at {horizon}y")
    y, weight, known = _ipcw_at_horizon(time, event, horizon)
    risk = np.clip(risk, 1e-6, 1.0 - 1e-6)
    z = np.log(risk / (1.0 - risk))
    use = known & (weight > 0)

    citl_beta, citl_cov = _weighted_logistic_irls(
        np.ones((int(use.sum()), 1)), y[use], weight[use], offset=z[use]
    )
    joint_x = np.column_stack([np.ones(int(use.sum())), z[use]])
    joint_beta, joint_cov = _weighted_logistic_irls(
        joint_x, y[use], weight[use]
    )
    uncertainty = "model-based IRLS; censoring-weight uncertainty not propagated"
    if calibration_groups is not None:
        citl_cov = _cluster_sandwich_cov(
            np.ones((int(use.sum()), 1)),
            y[use],
            weight[use],
            citl_beta,
            calibration_groups[use],
            offset=z[use],
        )
        joint_cov = _cluster_sandwich_cov(
            joint_x,
            y[use],
            weight[use],
            joint_beta,
            calibration_groups[use],
        )
        uncertainty = (
            "family/cluster-robust sandwich conditional on estimated IPC weights; "
            "censoring-weight uncertainty not propagated"
        )
    citl_se = float(np.sqrt(max(citl_cov[0, 0], 0.0)))
    int_se = float(np.sqrt(max(joint_cov[0, 0], 0.0)))
    slope_se = float(np.sqrt(max(joint_cov[1, 1], 0.0)))
    summary = {
        "model": model_name,
        "horizon_years": float(horizon),
        "n": len(time),
        "events_by_horizon": int(y.sum()),
        "known_status_n": int(use.sum()),
        "early_censored_n": int((~known).sum()),
        "mean_predicted_risk": float(risk.mean()),
        "observed_ipcw_risk": float(np.sum(weight * y) / len(time)),
        "calibration_in_the_large": float(citl_beta[0]),
        "citl_lo": float(citl_beta[0] - 1.96 * citl_se),
        "citl_hi": float(citl_beta[0] + 1.96 * citl_se),
        "joint_intercept": float(joint_beta[0]),
        "joint_intercept_lo": float(joint_beta[0] - 1.96 * int_se),
        "joint_intercept_hi": float(joint_beta[0] + 1.96 * int_se),
        "calibration_slope": float(joint_beta[1]),
        "slope_lo": float(joint_beta[1] - 1.96 * slope_se),
        "slope_hi": float(joint_beta[1] + 1.96 * slope_se),
        "method": "IPCW weighted logistic calibration; early censoring not treated as event-free",
        "uncertainty": uncertainty,
    }

    bins = pd.qcut(pd.Series(risk), q=min(10, len(risk)), duplicates="drop")
    bin_rows: list[dict[str, Any]] = []
    for number, category in enumerate(bins.cat.categories, 1):
        mask = bins.eq(category).to_numpy()
        n_bin = int(mask.sum())
        bin_rows.append(
            {
                "model": model_name,
                "horizon_years": float(horizon),
                "bin": number,
                "n": n_bin,
                "events_by_horizon": int(y[mask].sum()),
                "mean_predicted_risk": float(risk[mask].mean()),
                "observed_ipcw_risk": float(np.sum(weight[mask] * y[mask]) / n_bin),
            }
        )
    return summary, pd.DataFrame(bin_rows)


def dca_at_horizon(
    time: np.ndarray,
    event: np.ndarray,
    predicted_risk: np.ndarray,
    horizon: float,
    model_name: str,
    thresholds: Sequence[float] = DCA_THRESHOLDS,
) -> pd.DataFrame:
    risk = np.asarray(predicted_risk, dtype=float)
    finite = np.isfinite(time) & np.isfinite(event) & np.isfinite(risk)
    time, event, risk = time[finite], event[finite], risk[finite]
    y, weight, known = _ipcw_at_horizon(time, event, horizon)
    n = len(time)
    rows: list[dict[str, Any]] = []
    for threshold in thresholds:
        threshold = float(threshold)
        if not 0 < threshold < 1:
            raise ValueError("DCA threshold must lie strictly between zero and one")
        treated = risk >= threshold
        tp = float(np.sum(weight * y * treated))
        fp = float(np.sum(weight * (1.0 - y) * treated * known))
        odds = threshold / (1.0 - threshold)
        event_rate = float(np.sum(weight * y) / n)
        none_nb = 0.0
        all_nb = event_rate - (1.0 - event_rate) * odds
        rows.append(
            {
                "model": model_name,
                "horizon_years": float(horizon),
                "threshold": threshold,
                "n": n,
                "events_by_horizon": int(y.sum()),
                "net_benefit_model": tp / n - fp / n * odds,
                "net_benefit_treat_all": all_nb,
                "net_benefit_treat_none": none_nb,
                "method": "simple IPCW survival DCA",
            }
        )
    return pd.DataFrame(rows)


def _write_calibration_plot(bins: pd.DataFrame, path: Path) -> None:
    if bins.empty:
        return
    os.environ.setdefault("MPLCONFIGDIR", str(path.parent / ".mplcache"))
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(6.2, 5.2), constrained_layout=True)
    for (name, horizon), group in bins.groupby(["model", "horizon_years"], sort=False):
        ax.plot(
            group["mean_predicted_risk"],
            group["observed_ipcw_risk"],
            marker="o",
            linewidth=1.5,
            label=f"{name}, {horizon:g}y",
        )
    upper = float(
        min(
            1.0,
            max(
                0.10,
                bins[["mean_predicted_risk", "observed_ipcw_risk"]]
                .to_numpy(float)
                .max()
                * 1.08,
            ),
        )
    )
    ax.plot([0, upper], [0, upper], color="black", linestyle="--", linewidth=1)
    ax.set(xlim=(0, upper), ylim=(0, upper), xlabel="Mean predicted risk", ylabel="IPCW observed risk")
    ax.legend(frameon=False, fontsize=8)
    ax.grid(alpha=0.2)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def run_calibration_dca(
    frozen: pd.DataFrame,
    fit: OOFFit,
    comparators: ComparatorSet,
    out_dir: Path,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    time = pd.to_numeric(frozen["time_years"], errors="raise").to_numpy(float)
    event = _binary_event_array(
        pd.to_numeric(frozen["event"], errors="raise").to_numpy(), "FROZEN.event"
    )
    groups = _groups_from_frame(frozen)
    _, e5 = horizon_risk_set(time, event, 5.0)
    _, e10 = horizon_risk_set(time, event, 10.0)
    if int(e5.sum()) != EXPECTED["events_5y"] or int(e10.sum()) != EXPECTED["events_10y"]:
        raise AssertionError("calibration horizon event gate failed")

    entries_by_horizon: dict[int, list[tuple[str, np.ndarray]]] = {
        5: [(fit.label, fit.risk5)],
        10: [(fit.label, fit.risk10)],
    }
    for name, horizons in comparators.risks.items():
        for horizon, risk in horizons.items():
            if np.isfinite(risk).sum() > 0:
                entries_by_horizon[int(horizon)].append((name, risk))

    summaries: list[dict[str, Any]] = []
    bin_frames: list[pd.DataFrame] = []
    dca_frames: list[pd.DataFrame] = []
    for horizon, entries in entries_by_horizon.items():
        common = np.ones(len(time), dtype=bool)
        for _name, risk in entries:
            common &= np.isfinite(risk)
        if int(common.sum()) == 0:
            raise RuntimeError(f"no common finite absolute-risk set at {horizon}y")
        common_models = "; ".join(name for name, _risk in entries)
        for name, risk in entries:
            summary, bins = calibration_at_horizon(
                time[common],
                event[common],
                risk[common],
                horizon,
                name,
                groups=groups[common],
            )
            summary["evaluation_set"] = "common finite absolute-risk set"
            summary["models_in_common_set"] = common_models
            summaries.append(summary)
            bins["evaluation_set"] = "common finite absolute-risk set"
            bin_frames.append(bins)
            if horizon == 10:
                dca = dca_at_horizon(
                    time[common], event[common], risk[common], 10.0, name
                )
                dca["evaluation_set"] = "common finite absolute-risk set"
                dca["models_in_common_set"] = common_models
                dca_frames.append(dca)
    summaries.append(
        {
            "model": "Montreal-FH-SCORE",
            "horizon_years": "NOT-IN-PDF",
            "method": "ranking only; absolute-risk calibration and DCA not permitted",
        }
    )
    summary_frame = pd.DataFrame(summaries)
    bins_frame = pd.concat(bin_frames, ignore_index=True) if bin_frames else pd.DataFrame()
    dca_frame = pd.concat(dca_frames, ignore_index=True) if dca_frames else pd.DataFrame()
    write_aggregate_csv(summary_frame, out_dir / "calibration_summary.csv")
    write_aggregate_csv(bins_frame, out_dir / "calibration_bins.csv")
    write_aggregate_csv(dca_frame, out_dir / "dca_10y.csv")
    _write_calibration_plot(bins_frame, out_dir / "calibration_oof.png")
    return summary_frame, bins_frame, dca_frame


# ---------------------------------------------------------------------------
# Wales external geographical transport
class WalesLpAUnavailable(RuntimeError):
    """The confirmatory Welsh Lp(a) transport is unavailable or incomparable."""


def _strict_nonnegative_int(value: Any, label: str) -> int:
    if isinstance(value, (bool, np.bool_)):
        raise ValueError(f"{label} must be a non-negative integer count")
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be a non-negative integer count") from exc
    if not np.isfinite(number) or number < 0 or not number.is_integer():
        raise ValueError(f"{label} must be a non-negative integer count")
    return int(number)


def validate_wales_ledger(
    wales_start: pd.DataFrame,
    wales_final: pd.DataFrame,
    ledger: Sequence[Mapping[str, Any]] | pd.DataFrame,
) -> pd.DataFrame:
    """Require a complete, monotone Wales filter ledger before any scoring."""
    require_columns(wales_start, ("Positive1",), "WALES_START")
    positive = pd.to_numeric(wales_start["Positive1"], errors="coerce").eq(1)
    if int(positive.sum()) != 2405:
        raise AssertionError(
            f"Wales Positive1 start: got {int(positive.sum())}, expected 2405"
        )
    records = ledger.to_dict("records") if isinstance(ledger, pd.DataFrame) else list(ledger)
    if not records:
        raise RuntimeError("WALES_LEDGER is empty")
    if len(records) < 2:
        raise RuntimeError(
            "WALES_LEDGER needs a Positive1 start row plus at least one completed "
            "eligibility/analysis-set row; a one-row attestation is insufficient"
        )
    required = {"step", "status", "n", "criterion", "source_fields", "excluded_n"}
    placeholder_tokens = ("TODO", "TBD", "PLACEHOLDER", "UNKNOWN", "NOT DONE")
    for index, row in enumerate(records):
        missing = required.difference(row)
        if missing:
            raise KeyError(f"WALES_LEDGER row {index} missing {sorted(missing)}")
        if str(row["status"]).upper() != "COMPLETE":
            raise RuntimeError(
                f"Wales ledger incomplete at step {row['step']!r}: {row['status']!r}"
            )
        for field in ("step", "criterion", "source_fields"):
            text = str(row[field]).strip()
            if not text or any(token in text.upper() for token in placeholder_tokens):
                raise RuntimeError(
                    f"WALES_LEDGER row {index} has incomplete {field}: {row[field]!r}"
                )
    counts = [
        _strict_nonnegative_int(row["n"], f"WALES_LEDGER row {index} n")
        for index, row in enumerate(records)
    ]
    if counts[0] != 2405:
        raise AssertionError("first WALES_LEDGER count must be Positive1 n=2405")
    if any(next_n > n for n, next_n in zip(counts, counts[1:])):
        raise AssertionError("WALES_LEDGER counts must be non-increasing")
    excluded = [
        _strict_nonnegative_int(
            row["excluded_n"], f"WALES_LEDGER row {index} excluded_n"
        )
        for index, row in enumerate(records)
    ]
    if excluded[0] != 0:
        raise AssertionError("first WALES_LEDGER excluded_n must be 0")
    for index in range(1, len(records)):
        expected_excluded = counts[index - 1] - counts[index]
        if excluded[index] != expected_excluded:
            raise AssertionError(
                f"WALES_LEDGER row {index} excluded_n={excluded[index]} but "
                f"the count change is {expected_excluded}"
            )
    first_criterion = str(records[0]["criterion"]).replace(" ", "").lower()
    if "positive1" not in first_criterion or "1" not in first_criterion:
        raise AssertionError(
            "first WALES_LEDGER criterion must explicitly record Positive1 == 1"
        )
    if counts[-1] != len(wales_final):
        raise AssertionError(
            f"final Wales ledger n={counts[-1]} but WALES_FINAL n={len(wales_final)}"
        )
    require_columns(wales_final, ("time_years", "event"), "WALES_FINAL")
    final_time = pd.to_numeric(wales_final["time_years"], errors="raise").to_numpy(float)
    final_event = _binary_event_array(
        pd.to_numeric(wales_final["event"], errors="raise").to_numpy(),
        "WALES_FINAL.event",
    )
    if not np.isfinite(final_time).all() or np.any(final_time <= 0):
        raise ValueError("WALES_FINAL.time_years must be finite and positive")
    final_events = int(final_event.sum())
    final_required = {
        "events",
        "filters_complete",
        "analysis_set",
        "investigator_approved",
        "endpoint",
        "i50_excluded",
    }
    missing_final = final_required.difference(records[-1])
    if missing_final:
        raise RuntimeError(
            f"final WALES_LEDGER row missing completion fields: {sorted(missing_final)}"
        )
    if records[-1]["events"] in (None, "", "TODO"):
        raise RuntimeError("final WALES_LEDGER row must contain a completed events count")
    ledger_events = _strict_nonnegative_int(
        records[-1]["events"], "final WALES_LEDGER events"
    )
    if ledger_events != final_events:
        raise AssertionError(
            f"final Wales ledger events={records[-1]['events']} but frame events={final_events}"
        )
    for flag in ("filters_complete", "analysis_set", "investigator_approved", "i50_excluded"):
        if records[-1][flag] not in (True, 1):
            raise RuntimeError(f"final WALES_LEDGER must explicitly set {flag}=True")
    if str(records[-1]["endpoint"]).strip() != PRIMARY_ENDPOINT:
        raise AssertionError(
            "final WALES_LEDGER endpoint must exactly match the locked primary ASCVD "
            "definition with I50 excluded"
        )
    return pd.DataFrame(records)


def _validate_frozen_bundle(bundle: FrozenCoxBundle, expected_features: Sequence[str]) -> None:
    expected_features = tuple(expected_features)
    if tuple(bundle.features) != expected_features:
        raise AssertionError("Wales transport bundle does not match the frozen UKB SPEC")
    if tuple(bundle.preprocessor.features) != expected_features:
        raise AssertionError("Wales transport preprocessor does not match the frozen UKB SPEC")
    if set(bundle.coefficients) != set(expected_features):
        raise AssertionError("Wales transport coefficient ledger is incomplete")
    if not all(np.isfinite(float(value)) for value in bundle.coefficients.values()):
        raise ValueError("Wales transport coefficient ledger contains non-finite values")
    if set(bundle.baseline_survival) != {"5y", "10y"}:
        raise AssertionError("Wales transport requires frozen UKB 5y and 10y baselines")


def _require_wales_lpa_transport(
    frame: pd.DataFrame,
    bundle: FrozenCoxBundle,
    lpa_comparable: bool | None,
) -> None:
    if "log_lpa" not in bundle.features:
        return
    if lpa_comparable is None:
        raise RuntimeError(
            "Set WALES_LPA_COMPARABLE explicitly True or False before transport; "
            "column presence is not assay comparability"
        )
    if not isinstance(lpa_comparable, (bool, np.bool_)):
        raise TypeError("WALES_LPA_COMPARABLE must be a boolean")
    if not bool(lpa_comparable):
        raise WalesLpAUnavailable(
            "investigator marked Welsh Lp(a) assay/units incomparable with UKB"
        )
    usable_log = "log_lpa" in frame and pd.to_numeric(
        frame["log_lpa"], errors="coerce"
    ).notna().any()
    usable_native = "lpa_nmol" in frame and pd.to_numeric(
        frame["lpa_nmol"], errors="coerce"
    ).notna().any()
    if not usable_log and not usable_native:
        raise WalesLpAUnavailable(
            "Welsh Lp(a) was declared comparable but no usable log_lpa/lpa_nmol values exist"
        )


def _bundle_predict(
    frame: pd.DataFrame, bundle: FrozenCoxBundle
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    design = build_calong_frame(frame, bundle.features)
    predictors = design.loc[:, list(bundle.features)]
    wholly_missing = [c for c in bundle.features if predictors[c].notna().sum() == 0]
    if wholly_missing:
        raise ValueError(f"transport predictors wholly unavailable: {wholly_missing}")
    x = apply_preprocessor(predictors, bundle.preprocessor)
    lp, risk5 = _predict_lp_and_risk(bundle.model, x, 5.0)
    _, risk10 = _predict_lp_and_risk(bundle.model, x, 10.0)
    return lp, risk5, risk10


def _cluster_bootstrap_c_index(
    time: np.ndarray,
    event: np.ndarray,
    score: np.ndarray,
    groups: np.ndarray,
    b: int = B_BOOT,
    seed: int = SEED,
) -> dict[str, Any]:
    if b != B_BOOT:
        raise ValueError(f"external validation bootstrap must use B={B_BOOT}")
    codes, uniques = pd.factorize(pd.Series(groups), sort=False)
    if np.any(codes < 0):
        raise ValueError("missing cluster IDs must be normalised before bootstrap")
    members = [np.flatnonzero(codes == i) for i in range(len(uniques))]
    rng = np.random.default_rng(seed)
    values: list[float] = []
    attempts = 0
    while len(values) < b and attempts < 10 * b:
        attempts += 1
        chosen = rng.integers(0, len(members), len(members))
        idx = np.concatenate([members[j] for j in chosen])
        if int(event[idx].sum()) < MIN_EVENTS:
            continue
        try:
            values.append(_c_index(time[idx], event[idx], score[idx]))
        except ZeroDivisionError:
            continue
    if len(values) != b:
        return {
            "C": _c_index(time, event, score),
            "lo": float("nan"),
            "hi": float("nan"),
            "B_effective": len(values),
            "status": "NONCONFIRMATORY_BOOTSTRAP_SHORTFALL",
        }
    lo, hi = np.percentile(values, [2.5, 97.5])
    return {
        "C": _c_index(time, event, score),
        "lo": float(lo),
        "hi": float(hi),
        "B_effective": len(values),
        "status": "PASS",
    }


def _recalibrate_lp_in_wales(
    wales_final: pd.DataFrame, lp: np.ndarray
) -> dict[str, Any]:
    require_columns(wales_final, ("FamilyNumber",), "WALES_FINAL recalibration")
    groups = _groups_from_frame(wales_final)
    cluster_labels = np.asarray(
        [f"{type(value).__name__}:{value!r}" for value in groups], dtype=object
    )
    data = pd.DataFrame(
        {
            "LP": lp,
            "T": pd.to_numeric(wales_final["time_years"], errors="raise").to_numpy(float),
            "E": _binary_event_array(
                pd.to_numeric(wales_final["event"], errors="raise").to_numpy(),
                "WALES_FINAL.event",
            ),
            "family_cluster": cluster_labels,
        }
    )
    model = CoxPHFitter(penalizer=0.0)
    model.fit(
        data,
        duration_col="T",
        event_col="E",
        cluster_col="family_cluster",
        robust=True,
        show_progress=False,
    )
    coefficient = float(model.params_["LP"])
    se = float(model.standard_errors_["LP"])
    lp_center = float(model._norm_mean["LP"])
    return {
        "recalibration_slope": coefficient,
        "slope_lo": coefficient - 1.96 * se,
        "slope_hi": coefficient + 1.96 * se,
        "baseline_survival_5y": _baseline_survival_at(model, 5.0),
        "baseline_survival_10y": _baseline_survival_at(model, 10.0),
        "lp_center": lp_center,
        "recalibrated_risk_formula": (
            "risk(t)=1-S0_Wales(t)^exp(recalibration_slope*(LP-lp_center))"
        ),
        "label": "EXPLORATORY Wales recalibration of UKB-reduced no-Lp(a) model",
    }


def run_wales_transport(
    wales_start: pd.DataFrame,
    wales_final: pd.DataFrame,
    ledger: Sequence[Mapping[str, Any]] | pd.DataFrame,
    primary_bundle: FrozenCoxBundle,
    out_dir: Path,
    reduced_bundle: FrozenCoxBundle | None = None,
    lpa_comparable: bool | None = None,
) -> dict[str, Any]:
    ledger_frame = validate_wales_ledger(wales_start, wales_final, ledger)
    write_aggregate_csv(ledger_frame, out_dir / "wales_filter_ledger.csv")
    require_columns(wales_final, ("FamilyNumber",), "WALES_FINAL")
    time = pd.to_numeric(wales_final["time_years"], errors="raise").to_numpy(float)
    event = _binary_event_array(
        pd.to_numeric(wales_final["event"], errors="raise").to_numpy(),
        "WALES_FINAL.event",
    )
    groups = _groups_from_frame(wales_final)
    _validate_frozen_bundle(primary_bundle, SPEC_PRIMARY)
    result: dict[str, Any] = {
        "validation_type": "external geographical validation",
        "n": len(wales_final),
        "events": int(event.sum()),
        "ukb_cohort_sha256": EXPECTED_COHORT_SHA256,
        "ukb_coefficients_frozen": True,
        "wales_refit_for_confirmatory_claim": False,
        "missing_family_ids_unique_row_clusters": int(
            wales_final["FamilyNumber"].isna().sum()
        ),
        "wales_lpa_comparable": lpa_comparable,
    }
    try:
        _require_wales_lpa_transport(wales_final, primary_bundle, lpa_comparable)
        lp, risk5, risk10 = _bundle_predict(wales_final, primary_bundle)
    except WalesLpAUnavailable as exc:
        result["primary"] = {
            "status": "NOT_EVALUABLE",
            "reason": str(exc),
            "interpretation": "not the same CALON-G model if Lp(a) is omitted",
        }
        if reduced_bundle is None:
            write_aggregate_json(result, out_dir / "wales_transport.json")
            return result
        _validate_frozen_bundle(
            reduced_bundle, tuple(x for x in SPEC_PRIMARY if x != "log_lpa")
        )
        reduced_lp, _, _ = _bundle_predict(wales_final, reduced_bundle)
        result["reduced_no_lpa_sensitivity"] = {
            **_cluster_bootstrap_c_index(time, event, reduced_lp, groups),
            **_recalibrate_lp_in_wales(wales_final, reduced_lp),
            "ukb_reduced_coefficients_frozen_before_wales": True,
            "confirmatory_primary": False,
        }
        write_aggregate_json(result, out_dir / "wales_transport.json")
        return result

    calibration_rows: list[dict[str, Any]] = []
    calibration_bins: list[pd.DataFrame] = []
    for horizon, risk in ((5, risk5), (10, risk10)):
        try:
            summary, bins = calibration_at_horizon(
                time,
                event,
                risk,
                float(horizon),
                "CALON-G-primary frozen UKB -> Wales",
                groups=groups,
            )
            summary["validation_type"] = "external geographical validation"
            summary["wales_recalibration"] = False
            calibration_rows.append(summary)
            bins["validation_type"] = "external geographical validation"
            calibration_bins.append(bins)
        except RuntimeError as exc:
            calibration_rows.append(
                {
                    "model": "CALON-G-primary frozen UKB -> Wales",
                    "horizon_years": horizon,
                    "status": "NON_ESTIMABLE",
                    "reason": str(exc),
                    "validation_type": "external geographical validation",
                    "wales_recalibration": False,
                }
            )
    wales_calibration = pd.DataFrame(calibration_rows)
    wales_bins = (
        pd.concat(calibration_bins, ignore_index=True)
        if calibration_bins
        else pd.DataFrame()
    )
    write_aggregate_csv(wales_calibration, out_dir / "wales_calibration_summary.csv")
    write_aggregate_csv(wales_bins, out_dir / "wales_calibration_bins.csv")
    result["primary"] = {
        **_cluster_bootstrap_c_index(time, event, lp, groups),
        "mean_predicted_risk_5y": float(np.mean(risk5)),
        "mean_predicted_risk_10y": float(np.mean(risk10)),
        "status_detail": "frozen UKB coefficients and preprocessing; no Wales refit",
        "calibration": calibration_rows,
    }
    write_aggregate_json(result, out_dir / "wales_transport.json")
    return result


# ---------------------------------------------------------------------------
# Reporting-standard artefacts
def reporting_standard_tables(
    lock: Mapping[str, Any],
    head_gate: Mapping[str, Any] | None,
    calibration: pd.DataFrame,
    wales: Mapping[str, Any],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Emit explicit TRIPOD+AI and STROBE audit tables without inventing results."""
    head_status = (
        "PASS"
        if head_gate is not None and head_gate.get("bootstrap_gate") == "PASS"
        else "FAIL_OR_NOT_EVALUABLE"
    )
    primary_calibration = calibration.loc[
        calibration.get("model", pd.Series(dtype=object)).eq("CALON-G-primary")
    ]
    calibrated_horizons = set(
        pd.to_numeric(primary_calibration.get("horizon_years"), errors="coerce")
        .dropna()
        .astype(int)
        .tolist()
    )
    calibration_status = "PASS" if {5, 10}.issubset(calibrated_horizons) else "FAIL"
    wales_primary = wales.get("primary", {}) if isinstance(wales, Mapping) else {}
    if wales_primary.get("status") == "PASS":
        wales_status = "PASS"
        wales_evidence = "frozen UKB model; external C and 5y/10y calibration emitted"
    elif wales.get("status") == "NOT_RUN":
        wales_status = "PENDING_DATA"
        wales_evidence = str(wales.get("reason", "Wales inputs not supplied"))
    else:
        wales_status = "NOT_EVALUABLE_OR_EXPLORATORY"
        wales_evidence = str(
            wales_primary.get("reason", "see wales_transport.json for gated sensitivity")
        )

    tripod = pd.DataFrame(
        [
            ("Objective / estimand", "PASS", "locked prediction/risk-stratification estimand"),
            ("Data source / participants", "PASS", f"UKB frozen SHA {lock['cohort_sha256']}"),
            ("Outcome", "PASS", PRIMARY_ENDPOINT),
            ("Predictors", "PASS", f"frozen SPEC SHA {SPEC_SHA256}"),
            ("Study size", "PASS", f"n={lock['n_frozen']}; events={lock['events_full']}"),
            ("Missing data", "PASS", "training-fold median/mode; NOT MCAR"),
            ("Analytical methods", "PASS", "nested-CV ridge Cox; paired cluster B=2000"),
            ("Internal validation / discrimination", head_status, "common-reference OOF LP"),
            ("Calibration", calibration_status, "OOF IPCW intercept/slope at 5y and 10y"),
            ("External geographical validation", wales_status, wales_evidence),
            ("Subgroups / multiplicity", head_status, "full matrix emitted with warning"),
            ("Code / provenance availability", "PASS", "Cycle-2 code plus PDF provenance table"),
            (
                "Title / abstract wording",
                "INVESTIGATOR_ACTION",
                "identify prediction model and ridge Cox; do not call it AI",
            ),
        ],
        columns=["tripod_ai_item", "status", "evidence_or_action"],
    )
    strobe = pd.DataFrame(
        [
            ("Genotype-confirmed UKB carriers", lock["n_carriers"], 0, "source population"),
            (
                "After prevalent permitted ASCVD exclusion",
                lock["n_carriers"] - lock["n_prevalent"],
                lock["n_prevalent"],
                PRIMARY_ENDPOINT,
            ),
            (
                "Frozen incident risk set after undated exclusion",
                lock["n_frozen"],
                lock["n_undated"],
                "cohort SHA gate passed",
            ),
            ("Full-follow-up outcomes", lock["n_frozen"], 0, f"events={lock['events_full']}"),
            ("5-year administratively truncated outcomes", lock["n_frozen"], 0, f"events={lock['events_5y']}"),
            ("10-year administratively truncated outcomes", lock["n_frozen"], 0, f"events={lock['events_10y']}"),
        ],
        columns=["strobe_stage", "n_remaining", "excluded_at_step", "detail"],
    )
    return tripod, strobe


# ---------------------------------------------------------------------------
# Orchestration
def run_cycle2(
    frozen: pd.DataFrame,
    cohort_ledger: Mapping[str, Any],
    cohort_sha: str | None = None,
    *,
    out_dir: str | Path = "calon_cycle2_out",
    exploratory_lpa_conversion: bool = False,
    wales_start: pd.DataFrame | None = None,
    wales_final: pd.DataFrame | None = None,
    wales_ledger: Sequence[Mapping[str, Any]] | pd.DataFrame | None = None,
    wales_lpa_comparable: bool | None = None,
    allow_wales_reduced_lpa_sensitivity: bool = False,
) -> dict[str, Any]:
    """Run Cycle 2 from already-loaded frames and write aggregate artefacts only."""
    output = Path(out_dir)
    require_fresh_output_dir(output)
    output.mkdir(parents=True, exist_ok=True)
    lock = validate_frozen_lock(frozen, cohort_ledger, cohort_sha)
    write_aggregate_json(lock, output / "findings_lock.json")
    horizon_proof = pd.DataFrame(
        [
            {
                "horizon": "full",
                "n": lock["n_frozen"],
                "events": lock["events_full"],
                "expected_events": EXPECTED["events_full"],
                "status": "PASS",
            },
            {
                "horizon": "5y",
                "n": lock["n_frozen"],
                "events": lock["events_5y"],
                "expected_events": EXPECTED["events_5y"],
                "status": "PASS",
            },
            {
                "horizon": "10y",
                "n": lock["n_frozen"],
                "events": lock["events_10y"],
                "expected_events": EXPECTED["events_10y"],
                "status": "PASS",
            },
        ]
    )
    write_aggregate_csv(horizon_proof, output / "horizon_proof.csv")
    emit_aggregate(lock, "CYCLE-2 FINDINGS LOCK")

    predictor_qc = predictor_diagnostics(frozen)
    write_aggregate_csv(predictor_qc, output / "predictor_diagnostics.csv")
    emit_aggregate(predictor_qc, "PRESPECIFIED PREDICTOR DIAGNOSTICS")

    primary = fit_calong_oof(frozen, SPEC_PRIMARY, "CALON-G-primary")
    write_aggregate_json(primary.aggregate_dict(), output / "calong_model_summary.json")
    write_aggregate_csv(primary.fold_summary, output / "calong_outer_fold_summary.csv")
    emit_aggregate(primary.aggregate_dict(), "CALON-G PRIMARY OOF")

    grey: OOFFit | None = None
    if "log_apob_hdl" in frozen and frozen["log_apob_hdl"].notna().any():
        grey = fit_calong_oof(frozen, SPEC_GREY, "CALON-G-grey sensitivity")
        write_aggregate_json(grey.aggregate_dict(), output / "calong_grey_summary.json")
    else:
        write_aggregate_json(
            {
                "label": "CALON-G-grey sensitivity",
                "status": "NOT_EVALUABLE",
                "reason": "log_apob_hdl unavailable",
                "spec": list(SPEC_GREY),
            },
            output / "calong_grey_summary.json",
        )

    comparators = score_comparators_oof(
        frozen,
        primary.splits,
        exploratory_lpa_conversion=exploratory_lpa_conversion,
    )
    write_aggregate_csv(comparators.audit, output / "comparator_evaluability.csv")
    emit_aggregate(comparators.audit, "COMPARATOR EVALUABILITY")

    head_table: pd.DataFrame | None = None
    head_gate: dict[str, Any] | None = None
    head_error: Exception | None = None
    try:
        head_table, head_gate = run_headtohead(frozen, primary, comparators, output)
        emit_aggregate(head_table, "FULL HEAD-TO-HEAD TABLE")
        emit_aggregate(head_gate, "HEAD-TO-HEAD GATES")
        if head_gate["bootstrap_gate"] != "PASS":
            head_error = RuntimeError(
                "confirmatory paired cluster bootstrap did not complete exactly B=2000"
            )
    except RuntimeError as exc:
        head_error = exc
        emit_aggregate(
            {"status": "FAIL_LOUD", "reason": str(exc)}, "HEAD-TO-HEAD GATE"
        )

    calibration, calibration_bins, dca = run_calibration_dca(
        frozen, primary, comparators, output
    )
    emit_aggregate(calibration, "OOF CALIBRATION")
    emit_aggregate(dca, "10-YEAR DCA")

    wales: dict[str, Any]
    supplied_wales = [wales_start is not None, wales_final is not None, wales_ledger is not None]
    reduced_fit: OOFFit | None = None
    if any(supplied_wales) and not all(supplied_wales):
        raise RuntimeError(
            "Wales transport requires WALES_START, WALES_FINAL and WALES_LEDGER together"
        )
    if all(supplied_wales):
        reduced_bundle: FrozenCoxBundle | None = None
        if allow_wales_reduced_lpa_sensitivity:
            reduced_spec = tuple(x for x in SPEC_PRIMARY if x != "log_lpa")
            reduced_fit = fit_calong_oof(
                frozen, reduced_spec, "CALON-G Wales reduced no-Lp(a) sensitivity"
            )
            reduced_bundle = reduced_fit.final_bundle
            write_aggregate_json(
                reduced_fit.aggregate_dict(), output / "calong_wales_reduced_summary.json"
            )
        wales = run_wales_transport(
            wales_start,
            wales_final,
            wales_ledger,
            primary.final_bundle,
            output,
            reduced_bundle=reduced_bundle,
            lpa_comparable=wales_lpa_comparable,
        )
    else:
        wales = {
            "status": "NOT_RUN",
            "reason": "Wales frames/ledger not supplied; incomplete ledger must fail loud",
        }
        write_aggregate_json(wales, output / "wales_transport.json")

    tripod_ai, strobe_flow = reporting_standard_tables(
        lock, head_gate, calibration, wales
    )
    write_aggregate_csv(tripod_ai, output / "tripod_ai_checklist.csv")
    write_aggregate_csv(strobe_flow, output / "strobe_flow.csv")
    emit_aggregate(tripod_ai, "TRIPOD+AI CHECKLIST")
    emit_aggregate(strobe_flow, "STROBE FLOW")

    run_meta = {
        "cohort_sha256": lock["cohort_sha256"],
        "spec_sha256": SPEC_SHA256,
        "spec": SPEC_LOCK,
        "endpoint": PRIMARY_ENDPOINT,
        "participant_level_outputs": False,
        "run_complete": head_error is None,
        "exploratory_lpa_conversion_requested": exploratory_lpa_conversion,
        "exploratory_lpa_conversion_used": comparators.exploratory_lpa_conversion,
        "headtohead_status": (
            "FAIL" if head_error is not None else head_gate["analysis_status"]
        ),
        "wales_status": wales.get("status", wales.get("primary", {}).get("status", "PASS")),
        "wales_lpa_comparable": wales_lpa_comparable,
        "mice_mar_sensitivity": (
            "PRESPECIFIED, not auto-run: m>=20; outcome not imputed; pooling method must be "
            "declared in Julius before execution"
        ),
        "versions": {
            "python": os.sys.version.split()[0],
            "numpy": np.__version__,
            "pandas": pd.__version__,
            "lifelines": _installed_version("lifelines"),
            "matplotlib": _installed_version("matplotlib"),
        },
    }
    write_aggregate_json(run_meta, output / "run_meta.json")
    if head_error is not None:
        raise RuntimeError(str(head_error)) from head_error
    return {
        "lock": lock,
        "horizon_proof": horizon_proof,
        "predictor_diagnostics": predictor_qc,
        "primary": primary,
        "grey": grey,
        "comparators": comparators,
        "headtohead": head_table,
        "headtohead_gate": head_gate,
        "calibration": calibration,
        "calibration_bins": calibration_bins,
        "dca": dca,
        "wales": wales,
        "wales_reduced": reduced_fit,
        "tripod_ai_checklist": tripod_ai,
        "strobe_flow": strobe_flow,
        "run_meta": run_meta,
    }


def self_test() -> dict[str, Any]:
    """Formula/horizon smoke tests using constants only, never synthetic cohorts."""
    toy_t = np.array([1.0, 7.0, 4.0])
    toy_e = np.array([1, 1, 0])
    t5, e5 = horizon_risk_set(toy_t, toy_e, 5.0)
    if not np.array_equal(t5, np.array([1.0, 5.0, 4.0])):
        raise AssertionError("horizon time truncation self-test failed")
    if not np.array_equal(e5, np.array([1, 0, 0])):
        raise AssertionError("horizon event truncation self-test failed")
    try:
        horizon_risk_set(np.array([1.0, 2.0]), np.array([0.5, 1.0]), 5.0)
    except ValueError:
        pass
    else:
        raise AssertionError("fractional event indicators were silently accepted")

    case1_lp = safeheart_lp(
        np.array([20.0]),
        np.array([0.0]),
        np.array([0.0]),
        np.array([0.0]),
        np.array([22.0]),
        np.array([0.0]),
        np.array([90.0]),
        np.array([33.0]),
    )
    case2_lp = safeheart_lp(
        np.array([63.0]),
        np.array([1.0]),
        np.array([1.0]),
        np.array([1.0]),
        np.array([31.0]),
        np.array([1.0]),
        np.array([182.0]),
        np.array([64.0]),
    )
    case1_5 = float(safeheart_risk(case1_lp, 5)[0])
    case2_5 = float(safeheart_risk(case2_lp, 5)[0])
    if not math.isclose(case1_5, 0.0002148, rel_tol=0.02, abs_tol=2e-7):
        raise AssertionError("SAFEHEART worked case 1 did not reproduce")
    if not math.isclose(case2_5, 0.3808, rel_tol=0.01, abs_tol=2e-3):
        raise AssertionError("SAFEHEART worked case 2 did not reproduce")
    fhrs_reference = float(fhrs_risk10(np.array([0.0]))[0])
    if not math.isclose(fhrs_reference, 0.0058407, rel_tol=1e-4):
        raise AssertionError("FH-Risk-Score reference risk did not reproduce")
    montreal = float(
        montreal_points(
            np.array([50.0]),
            np.array([1.0]),
            np.array([1.0]),
            np.array([1.0]),
            np.array([1.0]),
        )[0]
    )
    if montreal != 32.0:
        raise AssertionError("Montreal point-chart self-test failed")
    return {
        "status": "PASS",
        "horizon": "correct administrative truncation",
        "binary_event_validation": "PASS",
        "safeheart_case1_5y": case1_5,
        "safeheart_case2_5y": case2_5,
        "fhrs_reference_10y": fhrs_reference,
        "montreal_test_points": montreal,
        "spec_sha256": SPEC_SHA256,
    }


def _cli(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="CALON-G Cycle 2 engine; DataFrames must already be loaded"
    )
    parser.add_argument(
        "--self-test", action="store_true", help="run source-equation smoke tests only"
    )
    args = parser.parse_args(argv)
    if args.self_test:
        emit_aggregate(self_test(), "SELF-TEST")
        return 0
    parser.error(
        "this script never reads participant files; import/run_path it and call "
        "run_cycle2(FROZEN, COHORT_LEDGER, COHORT_HASH)"
    )
    return 2


if __name__ == "__main__" and "__file__" in globals():
    if "FROZEN" in globals():
        CYCLE2_RESULTS = run_cycle2(
            globals()["FROZEN"],
            globals().get("COHORT_LEDGER", {}),
            globals().get("COHORT_HASH"),
            out_dir=globals().get("CYCLE2_OUT", "calon_cycle2_out"),
            exploratory_lpa_conversion=bool(
                globals().get("RUN_EXPLORATORY_LPA_CONVERSION", False)
            ),
            wales_start=globals().get("WALES_START"),
            wales_final=globals().get("WALES_FINAL"),
            wales_ledger=globals().get("WALES_LEDGER"),
            wales_lpa_comparable=globals().get("WALES_LPA_COMPARABLE"),
            allow_wales_reduced_lpa_sensitivity=bool(
                globals().get("ALLOW_WALES_REDUCED_LPA_SENSITIVITY", False)
            ),
        )
    else:
        raise SystemExit(_cli())
