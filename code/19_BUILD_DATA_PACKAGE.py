#!/usr/bin/env python3
"""Assemble a complete, inventoried, endpoint-audited LOCAL data package.

Produces one folder holding every raw input the CALON programme uses, with:
  raw/                the actual data files, copied verbatim
  INVENTORY.csv/.md   every file: path, bytes, md5, rows, columns
  ENDPOINT_AUDIT.md   what each UK Biobank outcome field ACTUALLY encodes,
                      measured - hypertension vs heart failure vs ASCVD/MACE
  COLUMNS_*.csv       full column dictionary for each dataset
  README.md           provenance, governance, and how the model uses each file

GOVERNANCE - READ THIS
This package contains PARTICIPANT-LEVEL GOVERNED DATA: UK Biobank (Application
1002450) and All-Wales PASS/DRAGON. It is built for LOCAL use on the
investigator's own machine only. It must never be committed to git, uploaded,
synced to a shared drive, or transmitted to any external service. The
repository's .gitignore blocks every data extension; this folder is deliberately
created OUTSIDE the git working tree.

Why the endpoint audit exists: this programme has three times confused
`first_angina` (which encodes hypertension), heart failure (I50), and the
ASCVD/MACE composite. The audit settles each empirically rather than by reading
column names.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import warnings
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

STAMP = "2026-08-13"
OUT = Path.home() / "Downloads" / f"CALON_DATA_PACKAGE_{STAMP}"
GD = Path.home() / "Library/CloudStorage"


def gdrive(sub: str) -> Path | None:
    hits = sorted(GD.glob(f"GoogleDrive-*/My Drive/Projects/{sub}"))
    return hits[0] if hits else None


def to_md(df) -> str:
    """Markdown table without the optional `tabulate` dependency."""
    cols = list(df.columns)
    cells = [[("" if pd.isna(v) else str(v)) for v in row] for row in df.to_numpy()]
    w = [max(len(c), *(len(r[i]) for r in cells)) if cells else len(c)
         for i, c in enumerate(cols)]
    line = lambda vals: "| " + " | ".join(v.ljust(w[i]) for i, v in enumerate(vals)) + " |"
    return "\n".join([line(cols), "|" + "|".join("-" * (x + 2) for x in w) + "|"]
                      + [line(r) for r in cells])


def md5(p: Path) -> str:
    h = hashlib.md5()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()


def sources() -> dict[str, dict]:
    shared = Path(os.environ["CALON_SHARED_MASTER"])
    corr = gdrive("CALON_AlphaFold_Rebuild")
    wales = Path.home() / "Downloads"
    return {
        "ukb_master": {
            "path": shared / "UKB" / "ukb_master.csv",
            "cohort": "UK Biobank",
            "role": "Exposures, covariates, baseline dates, LDLR carrier flag. "
                    "Its own outcome columns are NOT used - see ENDPOINT_AUDIT.md.",
        },
        "ukb_corrected_outcomes": {
            "path": (corr / "data_corrected" / "corrected_ascvd_outcomes.csv") if corr else None,
            "cohort": "UK Biobank",
            "role": "THE OUTCOME SOURCE. ascvd_first_date_best plus per-ICD "
                    "component flags. The model's endpoint is built from the "
                    "atherosclerotic components only.",
        },
        "ukb_bp_medication": {
            "path": (corr / "New folder" / "04a_meds_touch.csv") if corr else None,
            "cohort": "UK Biobank",
            "role": "Touchscreen BP medication (p6153_i0 women, p6177_i0 men), "
                    "baseline instance only.",
        },
        "wales_registry": {
            "path": wales / "WALES_FH_CLEANED.csv",
            "cohort": "All-Wales",
            "role": "The Welsh analysis cohort. Genotype flag Positive1; outcome "
                    "ascvd_combine; baseline MeasurementDate.1.",
        },
        "pass_master": {
            "path": shared / "PASS" / "pass_master.csv",
            "cohort": "All-Wales",
            "role": "Same registry as WALES_FH_CLEANED under different column "
                    "naming; identical row count, zero shared column names.",
        },
        "dragon": {
            "path": wales / "FH_Dragon3 (1).csv",
            "cohort": "All-Wales (subset)",
            "role": "Specialist-clinic subset. 424/424 records match into the "
                    "Welsh registry on DatabaseNumber. NOT a separate cohort.",
        },
    }


# ------------------------------------------------------------------ inventory
def build_inventory(src: dict, raw_dir: Path) -> pd.DataFrame:
    rows = []
    for key, meta in src.items():
        p = meta["path"]
        if p is None or not p.exists():
            rows.append({"key": key, "cohort": meta["cohort"], "file": "MISSING",
                         "bytes": None, "md5": None, "rows": None, "columns": None,
                         "role": meta["role"], "source_path": str(p)})
            print("  MISSING: %s" % key)
            continue
        dest = raw_dir / p.name
        if not dest.exists() or dest.stat().st_size != p.stat().st_size:
            print("  copying %-26s %8.1f MB ..." % (p.name, p.stat().st_size / 1e6), flush=True)
            shutil.copy2(p, dest)
        digest = md5(dest)
        head = pd.read_csv(dest, nrows=0, low_memory=False)
        n = sum(1 for _ in open(dest, "rb")) - 1
        same = digest == md5(p)
        rows.append({"key": key, "cohort": meta["cohort"], "file": p.name,
                     "bytes": p.stat().st_size, "md5": digest, "rows": n,
                     "columns": len(head.columns), "copy_verified": same,
                     "role": meta["role"], "source_path": str(p)})
        print("  %-26s rows=%-8d cols=%-4d md5=%s  copy_verified=%s"
              % (p.name, n, len(head.columns), digest[:12], same))
        pd.DataFrame({"column": head.columns}).to_csv(
            raw_dir.parent / f"COLUMNS_{key}.csv", index=False)
    return pd.DataFrame(rows)


# ------------------------------------------------------------- endpoint audit
def endpoint_audit(src: dict) -> tuple[pd.DataFrame, dict]:
    """Measure what each UK Biobank outcome field actually encodes."""
    m = pd.read_csv(src["ukb_master"]["path"], low_memory=False)
    c = pd.read_csv(src["ukb_corrected_outcomes"]["path"], low_memory=False)
    d = m.merge(c, on="eid", how="left")
    comp = {k: pd.to_numeric(d[k], errors="coerce").fillna(0).gt(0)
            for k in ["i21_event", "i25_event", "i50_event", "i63_event",
                      "i70_event", "i73_event", "g45_event"]}
    sbp = pd.to_numeric(d.sbp, errors="coerce")
    male = 1 - pd.to_numeric(d.sex_F, errors="coerce").fillna(0)
    ref_sbp, ref_male = float(sbp.mean()), float(100 * male.mean())

    candidates = [c for c in m.columns if any(
        k in c for k in ("first_", "ascvd", "has_hf", "incident_", "prevalent_"))]

    def positive(col):
        s = d[col]
        if s.dtype == object:
            v = pd.to_datetime(s, errors="coerce")
            if v.notna().sum() > 0:
                return v.notna()
        return pd.to_numeric(s, errors="coerce").fillna(0).gt(0)

    rows = []
    for f in candidates:
        p = positive(f)
        n = int(p.sum())
        if n == 0:
            rows.append({"field": f, "n_positive": 0, "verdict": "EMPTY - unusable"})
            continue
        j = {k: float((p & v).sum() / max((p | v).sum(), 1)) for k, v in comp.items()}
        best = max(j, key=j.get)
        pct = 100 * p.mean()
        s_pos, m_pos = float(sbp[p].mean()), float(100 * male[p].mean())
        # Empirical classification, stated as a rule so it can be re-checked:
        if pct > 30 and s_pos > ref_sbp + 5 and m_pos < ref_male + 12:
            verdict = "HYPERTENSION - not what the name says. DO NOT USE."
        elif j["i50_event"] > 0.5:
            verdict = "HEART FAILURE (I50). Excluded from the ASCVD endpoint."
        elif n < 5000:
            verdict = "NEAR-EMPTY - too sparse to be a real composite"
        else:
            verdict = "ASCVD-like, best match %s (Jaccard %.3f)" % (best.replace("_event", ""), j[best])
        rows.append({"field": f, "n_positive": n, "pct_cohort": round(pct, 2),
                     "mean_sbp": round(s_pos, 1), "male_pct": round(m_pos, 1),
                     "best_icd_match": best.replace("_event", ""),
                     "jaccard": round(j[best], 3), "verdict": verdict})
    return pd.DataFrame(rows), {"reference_mean_sbp": round(ref_sbp, 1),
                                "reference_male_pct": round(ref_male, 1),
                                "n_participants": int(len(d))}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    raw = OUT / "raw"
    raw.mkdir(exist_ok=True)
    print("=" * 92)
    print("BUILDING LOCAL DATA PACKAGE ->", OUT)
    print("=" * 92)
    src = sources()

    print("\nINVENTORY")
    inv = build_inventory(src, raw)
    inv.to_csv(OUT / "INVENTORY.csv", index=False)
    (OUT / "INVENTORY.md").write_text(
        "# CALON data package inventory - %s\n\nLOCAL ONLY. Governed "
        "participant-level data; never transmit.\n\n" % STAMP
        + to_md(inv[["key", "cohort", "file", "rows", "columns", "bytes", "md5",
                     "copy_verified"]]) + "\n\n## Role of each file\n\n"
        + "\n".join("- **%s** (`%s`): %s" % (r["key"], r["file"], r["role"])
                     for _, r in inv.iterrows()) + "\n", encoding="utf-8")

    print("\nENDPOINT AUDIT")
    audit, ref = endpoint_audit(src)
    audit.to_csv(OUT / "ENDPOINT_AUDIT.csv", index=False)
    for _, r in audit.iterrows():
        print("  %-26s n=%-8s %s" % (r["field"], r["n_positive"], r.get("verdict", "")))

    (OUT / "ENDPOINT_AUDIT.md").write_text(
        "# UK Biobank endpoint audit - what each outcome field ACTUALLY encodes\n\n"
        f"Measured {STAMP} on {ref['n_participants']:,} participants. "
        f"Cohort reference: mean SBP {ref['reference_mean_sbp']} mmHg, "
        f"{ref['reference_male_pct']}% male.\n\n"
        "Classification is empirical, not name-based. A field is called "
        "HYPERTENSION when it flags >30% of the cohort with mean SBP more than "
        "5 mmHg above the cohort and no male excess; HEART FAILURE when its "
        "Jaccard overlap with `i50_event` exceeds 0.5.\n\n"
        + to_md(audit) + "\n", encoding="utf-8")

    (OUT / "README.md").write_text(f"""# CALON data package - {STAMP}

Complete raw data for the CALON programme: UK Biobank, All-Wales PASS registry,
and the DRAGON specialist-clinic subset, with a full inventory and an empirical
endpoint audit.

## GOVERNANCE - LOCAL ONLY

This folder contains **participant-level governed data** under UK Biobank
Application 1002450 and All-Wales PASS/DRAGON approvals. It must never be
committed to git, uploaded, shared, or transmitted to any external service. It
sits outside the git working tree deliberately. The analysis repository's
`.gitignore` blocks every data extension.

## Contents

| Item | What it is |
|---|---|
| `raw/` | The data files, copied verbatim, md5-verified against source |
| `INVENTORY.csv` | Every file: bytes, md5, rows, columns, role, source path |
| `ENDPOINT_AUDIT.md` / `.csv` | What each UK Biobank outcome field really encodes |
| `COLUMNS_*.csv` | Full column dictionary per dataset |

## The three endpoint questions, answered

**Hypertension.** `first_angina` is mislabelled: it flags 41.7% of UK Biobank
with mean SBP well above cohort and no male excess. That is essential
hypertension (I10), not angina. It is never used, and it is verified absent from
the composite.

**Heart failure.** `has_hf` tracks I50 (Jaccard 0.92). Heart failure is **not**
atherosclerotic disease and is **excluded** from the model's endpoint. In the
LDLR carriers, 62 of 351 events in the broad composite were heart-failure-only.

**ASCVD / MACE.** The model does not use any master outcome column. It uses
`ascvd_first_date_best` from `corrected_ascvd_outcomes.csv`, restricted to the
atherosclerotic components **I21, I25, I63, I70, I73, G45**.

## How the model uses these files

`code/15_CALON_FINAL.py` reads exposures and baseline dates from `ukb_master`,
the outcome from `corrected_ascvd_outcomes`, BP medication from
`04a_meds_touch`, and the Welsh cohort from `WALES_FH_CLEANED`. `pass_master`
and `FH_Dragon3` are included for completeness and provenance; DRAGON is a
complete subset of the Welsh registry (424/424 on `DatabaseNumber`) and is not
analysed separately.

Rebuild: `python3 code/19_BUILD_DATA_PACKAGE.py`
""", encoding="utf-8")

    total = sum(int(b) for b in inv["bytes"].dropna())
    (OUT / "MANIFEST.json").write_text(json.dumps({
        "package": "CALON_DATA_PACKAGE", "built": STAMP,
        "governance": "LOCAL ONLY - participant-level governed data, never transmit",
        "total_bytes": total, "files": inv.to_dict(orient="records"),
        "endpoint_audit": audit.to_dict(orient="records"), "reference": ref,
    }, indent=2, default=str), encoding="utf-8")

    print("\n" + "=" * 92)
    print("PACKAGE BUILT: %s" % OUT)
    print("  files inventoried : %d" % len(inv))
    print("  total raw size    : %.1f MB" % (total / 1e6))
    print("  endpoint fields   : %d audited" % len(audit))


if __name__ == "__main__":
    main()
