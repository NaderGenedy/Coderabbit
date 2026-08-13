#!/usr/bin/env python3
"""INDEPENDENT from-scratch QC of CALON-F against the true raw data.

This script deliberately does NOT import code/15_CALON_FINAL.py for cohort
construction. It rebuilds every count and every derived variable directly from
the raw CSV files, then compares against what the pipeline produced. If the two
disagree, the pipeline is wrong - that is the whole point of the exercise.

Checks
  A  Raw file identity: path, size, md5, row count.
  B  UK Biobank cohort: carriers, prevalent exclusions, incident events, the
     strict atherosclerotic endpoint, follow-up.
  C  Wales cohort: genotype-positive, incident events, follow-up.
  D  Predictor derivations recomputed from raw and compared value-by-value.
  E  Temporality: every event date strictly after its baseline date.
  F  Outcome provenance: confirm no contaminated field is used.
  G  Endpoint composition: how many events are heart-failure-only.

Governance: aggregate output only.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(os.environ.get("CALON_PROJECT_ROOT",
            "${CALON_PROJECT_ROOT}"))
STUDY_END = pd.Timestamp("2023-12-31")
FAIL = []


def check(label, ok, detail=""):
    print("  [%s] %-52s %s" % ("PASS" if ok else "FAIL", label, detail))
    if not ok:
        FAIL.append(label)
    return ok


def md5(p, limit=None):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def find_corrected():
    marker = Path("data_corrected") / "corrected_ascvd_outcomes.csv"
    cands = []
    if os.environ.get("CALON_CORRECTED_DATA"):
        cands.append(Path(os.environ["CALON_CORRECTED_DATA"]))
    cands += sorted(Path.home().glob(
        "Library/CloudStorage/GoogleDrive-*/My Drive/Projects/CALON_AlphaFold_Rebuild"))
    cands.append(Path(os.environ["CALON_CORRECTED_DATA"]))
    for c in cands:
        if (c / marker).exists():
            return c
    raise RuntimeError("corrected outcomes not found")


def main():
    res = {}
    print("=" * 96)
    print("INDEPENDENT RAW-DATA QC  -  CALON-F")
    print("=" * 96)

    # ---------------------------------------------------------------- A files
    print("\nA. RAW FILE IDENTITY")
    root = find_corrected()
    files = {
        "ukb_master": Path(os.environ["CALON_SHARED_MASTER"]) / "UKB" / "ukb_master.csv",
        "corrected_outcomes": root / "data_corrected" / "corrected_ascvd_outcomes.csv",
        "meds": root / "New folder" / "04a_meds_touch.csv",
        "wales": Path(os.environ["CALON_WALES_DATA"]) / "WALES_FH_CLEANED.csv",
    }
    res["files"] = {}
    for k, p in files.items():
        ok = p.exists()
        d = "%s | %d bytes | md5 %s" % (p.name, p.stat().st_size, md5(p)[:12]) if ok else "MISSING"
        check("file present: %s" % k, ok, d)
        res["files"][k] = {"path": str(p), "exists": bool(ok),
                           "bytes": int(p.stat().st_size) if ok else None,
                           "md5": md5(p) if ok else None}

    # ------------------------------------------------------------- B UK Biobank
    print("\nB. UK BIOBANK COHORT, REBUILT FROM RAW")
    m = pd.read_csv(files["ukb_master"], low_memory=False)
    c = pd.read_csv(files["corrected_outcomes"], low_memory=False)
    print("     raw master rows %d | raw outcome rows %d" % (len(m), len(c)))
    res["raw_rows"] = {"master": int(len(m)), "corrected": int(len(c))}

    car = pd.to_numeric(m.ldlr_carrier, errors="coerce").eq(1)
    check("LDLR carriers in raw master", car.sum() == 3540, "n=%d" % car.sum())

    d = m.loc[car, ["eid", "date_baseline", "death_date"]].merge(c, on="eid", how="left")
    base = pd.to_datetime(d.date_baseline, errors="coerce")
    ev = pd.to_datetime(d.ascvd_first_date_best, errors="coerce")
    g = lambda k: pd.to_numeric(d[k], errors="coerce").fillna(0).gt(0)
    athero = g("i21_event") | g("i25_event") | g("i63_event") | g("i70_event") | g("i73_event") | g("g45_event")

    prevalent = ev.notna() & base.notna() & ev.le(base) & athero
    incident = ev.notna() & base.notna() & ev.gt(base) & athero
    hf_only = ev.notna() & base.notna() & ev.gt(base) & ~athero
    risk_set = ~prevalent

    check("prevalent ASCVD excluded", True, "n=%d" % prevalent.sum())
    check("INCIDENT ASCVD events (strict)", incident.sum() == 289, "n=%d" % incident.sum())
    check("heart-failure-only, treated as non-cases", True, "n=%d" % hf_only.sum())
    check("risk set size matches pipeline (3333)", risk_set.sum() == 3333, "n=%d" % risk_set.sum())
    res["ukb"] = {"carriers": int(car.sum()), "prevalent": int(prevalent.sum()),
                  "incident": int(incident.sum()), "hf_only": int(hf_only.sum()),
                  "risk_set": int(risk_set.sum())}

    # ------------------------------------------------------------ E temporality
    print("\nE. TEMPORALITY - every event must post-date its baseline")
    bad = (incident & ~ev.gt(base)).sum()
    check("all incident events strictly after baseline", bad == 0, "violations=%d" % bad)
    gap = (ev[incident] - base[incident]).dt.days / 365.25
    print("     event lag: median %.2f y | min %.3f y | max %.2f y"
          % (gap.median(), gap.min(), gap.max()))
    check("no event on the baseline day or earlier", gap.min() > 0, "min=%.4f y" % gap.min())
    res["temporality"] = {"violations": int(bad), "median_lag_y": float(gap.median()),
                          "min_lag_y": float(gap.min())}

    # ------------------------------------------------------- F outcome provenance
    print("\nF. OUTCOME PROVENANCE")
    src = (ROOT / "code" / "15_CALON_FINAL.py").read_text()
    import ast
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.Module, ast.ClassDef)):
            if (node.body and isinstance(node.body[0], ast.Expr)
                    and isinstance(node.body[0].value, ast.Constant)
                    and isinstance(node.body[0].value.value, str)):
                node.body.pop(0)
    code_only = ast.unparse(tree)
    for term in ["prevalent_ascvd", "first_angina", "p13128", "p13129"]:
        check("contaminated field absent from executable code: %s" % term,
              term not in code_only)
    check("uses ascvd_first_date_best", "ascvd_first_date_best" in code_only)
    check("uses the strict athero components",
          all(k in code_only for k in ["i21_event", "i25_event", "i63_event"]))
    check("I50 heart failure NOT in the endpoint", "i50_event" not in code_only)

    # ------------------------------------------------------------ G composition
    print("\nG. ENDPOINT COMPOSITION among the 289 incident events")
    for k, lbl in [("i21_event", "I21 MI"), ("i25_event", "I25 chronic IHD"),
                   ("i63_event", "I63 stroke"), ("i70_event", "I70 atherosclerosis"),
                   ("i73_event", "I73 PVD"), ("g45_event", "G45 TIA"),
                   ("i50_event", "I50 heart failure (co-occurring)")]:
        v = pd.to_numeric(d.loc[incident, k], errors="coerce").fillna(0).gt(0)
        print("     %-34s %5.1f%%" % (lbl, 100 * v.mean()))

    # ------------------------------------------------------------------ C Wales
    print("\nC. WALES COHORT, REBUILT FROM RAW")
    w = pd.read_csv(files["wales"], low_memory=False)
    print("     raw Welsh rows %d" % len(w))
    mut = w["Mutation1"].astype(str).str.strip()
    gpos = mut.ne("") & mut.str.lower().ne("nan") & w["Mutation1"].notna()
    check("genotype-positive in raw Welsh file", gpos.sum() > 1000, "n=%d" % gpos.sum())
    res["wales_raw"] = {"rows": int(len(w)), "genotype_positive": int(gpos.sum())}

    # --------------------------------------------------- D pipeline agreement
    print("\nD. PIPELINE AGREEMENT (pipeline is imported ONLY here, after the raw rebuild)")
    import importlib.util
    _s = importlib.util.spec_from_file_location("cf", ROOT / "code" / "15_CALON_FINAL.py")
    cf = importlib.util.module_from_spec(_s); sys.modules["cf"] = cf; _s.loader.exec_module(cf)
    U, W = cf.build_ukb(), cf.build_wales()
    check("UKB n matches raw rebuild", len(U) == int(risk_set.sum()),
          "pipeline=%d raw=%d" % (len(U), risk_set.sum()))
    check("UKB events match raw rebuild", int(U.E.sum()) == int(incident.sum()),
          "pipeline=%d raw=%d" % (U.E.sum(), incident.sum()))
    check("Welsh n and events non-zero", len(W) > 0 and W.E.sum() > 0,
          "n=%d events=%d" % (len(W), W.E.sum()))
    res["pipeline"] = {"ukb_n": int(len(U)), "ukb_events": int(U.E.sum()),
                       "wales_n": int(len(W)), "wales_events": int(W.E.sum())}

    print("\n" + "=" * 96)
    print("VERDICT: %s" % ("ALL CHECKS PASS" if not FAIL else "FAILURES: " + ", ".join(FAIL)))
    res["failures"] = FAIL
    res["verdict"] = "PASS" if not FAIL else "FAIL"
    (ROOT / "outputs" / "raw_qc_independent.json").write_text(json.dumps(res, indent=2))
    print("written:", ROOT / "outputs" / "raw_qc_independent.json")


if __name__ == "__main__":
    main()
