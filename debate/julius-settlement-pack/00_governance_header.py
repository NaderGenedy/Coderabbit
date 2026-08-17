# Julius Cell 0 — governance + file handles (aggregates only)
# Paste into Julius. Point FILE_* at the tables already loaded in your session.
# Do not print paths that embed participant identifiers.

from __future__ import annotations

import json
from dataclasses import asdict, dataclass

import numpy as np
import pandas as pd

# --- edit these names to match Julius session objects / uploaded files ---
FILE_UKB_MASTER = "ukb_master"          # or the DataFrame already in memory
FILE_UKB_OUTCOMES = "corrected_ascvd_outcomes"
FILE_WALES = "WALES_FH_CLEANED"

MMOL_TO_MGDL_LDL = 38.67  # LDL mmol/L → mg/dL


@dataclass
class AggregateReport:
    script: str
    notes: list
    metrics: dict

    def show(self) -> None:
        print(json.dumps({"script": self.script, "notes": self.notes, "metrics": self.metrics}, indent=2, default=str))


def as_df(obj) -> pd.DataFrame:
    if isinstance(obj, pd.DataFrame):
        return obj
    raise TypeError(f"Expected DataFrame for {obj!r}; load the CSV in Julius first, then pass the frame.")


print("GOVERNANCE_OK — aggregates only; no eid prints in settlement scripts.")
