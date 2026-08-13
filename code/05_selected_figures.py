#!/usr/bin/env python3
"""Generate CALON-N-specific calibration figures without saving row predictions."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path("${CALON_PROJECT_ROOT}")

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec); sys.modules[name] = module; spec.loader.exec_module(module)
    return module

b = load("calon_fig_base", ROOT / "code" / "01_calon_disc_analysis.py")
s = load("calon_fig_scratch", ROOT / "code" / "02_from_scratch_model.py")
b.CANDIDATES = s.SCRATCH

def main():
    cohorts = b.prepare_cohorts(); dragon, strict = cohorts["dragon"], cohorts["ukb_strict"]
    selected = json.loads((ROOT / "outputs" / "scratch_selection.json").read_text())["selected"]
    analyses = [
        ("DRAGON to UKB strict", strict, b.transport(dragon, strict, selected, 20260839)["prediction"]),
        ("UKB strict to DRAGON", dragon, b.transport(strict, dragon, selected, 20260840)["prediction"]),
    ]
    fig, axes = plt.subplots(1, 2, figsize=(9.5, 4.3))
    for ax, (title, frame, pred) in zip(axes, analyses):
        y = frame["y"].to_numpy(int)
        bins = pd.qcut(pd.Series(pred), q=5, duplicates="drop")
        tab = pd.DataFrame({"y": y, "p": pred, "bin": bins}).groupby("bin", observed=True).agg(
            observed=("y", "mean"), predicted=("p", "mean"), n=("y", "size"))
        top = max(.35, float(tab[["observed", "predicted"]].max().max()) * 1.08)
        ax.plot([0, top], [0, top], "--", color="#777777", linewidth=1)
        ax.plot(tab["predicted"], tab["observed"], "o-", color="#20639b", linewidth=1.7)
        for x, yv, n in zip(tab["predicted"], tab["observed"], tab["n"]):
            ax.annotate(f"n={n}", (x, yv), xytext=(4, 5), textcoords="offset points", fontsize=7)
        ax.set(xlim=(0, top), ylim=(0, top), xlabel="Predicted probability",
               ylabel="Observed prevalence", title=title)
    fig.tight_layout()
    fig.savefig(ROOT / "figures" / "scratch_external_calibration.png", dpi=260)
    fig.savefig(ROOT / "figures" / "scratch_external_calibration.pdf")
    plt.close(fig)

if __name__ == "__main__":
    main()
