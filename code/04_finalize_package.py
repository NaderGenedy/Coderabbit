#!/usr/bin/env python3
"""Finalize hashes and run non-destructive package integrity checks."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

ROOT = Path("/Users/nader85/Documents/CALON/calon_discordance_model_2026_08_09")
SOURCE = Path("/Users/nader85/Documents/CALON/dragon_plp_full_rebuild_2026_08_08")
def is_render_qa_part(part: str) -> bool:
    """Exclude disposable DOCX-render inspection directories from the lock."""
    return part.startswith("render_") or part.startswith("render2_") or part.startswith("rendered_")


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    mod = importlib.util.module_from_spec(spec); sys.modules[name] = mod; spec.loader.exec_module(mod)
    return mod


def main() -> None:
    base = load("calon_final_base", ROOT / "code" / "01_calon_disc_analysis.py")
    scorer = load("calon_final_scorer", ROOT / "code" / "apply_calon_n.py")
    bundle = joblib.load(ROOT / "model" / "calon_n_from_scratch.joblib")
    synthetic = pd.read_csv(ROOT / "model" / "synthetic_predictors.csv")
    p1 = scorer.score(synthetic, bundle); p2 = scorer.score(synthetic.iloc[::-1], bundle)[::-1]
    if not np.allclose(p1, p2, atol=1e-15, rtol=0):
        raise RuntimeError("Scorer changes under row reversal")
    equation_file = json.loads((ROOT / "model" / "calon_n_equation.json").read_text())
    if equation_file["features"] != bundle["columns"]:
        raise RuntimeError("Equation/model feature mismatch")
    selected = json.loads((ROOT / "outputs" / "scratch_selection.json").read_text())["selected"]
    if selected != equation_file["candidate"]:
        raise RuntimeError("Selection/equation candidate mismatch")

    empirical_row_markers = ["participant_id", "family_id", "eid", "chrom", "variant_coordinate"]
    suspicious = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.name == "MANIFEST.json":
            continue
        lower = path.name.lower()
        if any(marker in lower for marker in empirical_row_markers):
            suspicious.append(str(path.relative_to(ROOT)))
    if suspicious:
        raise RuntimeError("Potential participant-level output filenames: " + ", ".join(suspicious))

    inputs = [base.e.DRAGON, base.e.PASS, base.e.UKB, base.e.CALLS,
              base.e.UKB_CLINVAR, base.e.UKB_VEP, base.e.DRAGON_CLINVAR]
    files = {}
    for path in sorted(ROOT.rglob("*")):
        if (
            path.is_file()
            and path.name != "MANIFEST.json"
            and "__pycache__" not in path.parts
            and not any(is_render_qa_part(part) for part in path.parts)
        ):
            files[str(path.relative_to(ROOT))] = sha(path)
    manifest = {
        "package": "CALON-N",
        "version": "2026-08-09",
        "estimand": "cross-sectional established-ASCVD case identification",
        "selected_candidate": selected,
        "canonical_inputs": {str(path): sha(path) for path in inputs},
        "package_files": files,
        "checks": {
            "synthetic_row_order_invariant_max_abs_difference": float(np.max(np.abs(p1 - p2))),
            "equation_model_features_match": True,
            "selection_equation_match": True,
            "participant_level_outputs": False,
        },
    }
    (ROOT / "MANIFEST.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps({"files_hashed": len(files), "checks": manifest["checks"]}, indent=2))


if __name__ == "__main__":
    main()
