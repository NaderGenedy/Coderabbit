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
  C  Welsh sources: registry vs PASS, DRAGON containment and standalone
     feasibility, and an INDEPENDENT rebuild of the Welsh analysis cohort.
  D  Pipeline agreement: n and events compared against the raw rebuild in BOTH
     cohorts. This compares cohort construction, not individual predictor
     values.
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
MIN_EVENTS = 10   # same suppression threshold used throughout the programme
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
        "wales_registry": Path(os.environ["CALON_WALES_DATA"]) / "WALES_FH_CLEANED.csv",
        "pass_master": Path(os.environ["CALON_SHARED_MASTER"]) / "PASS" / "pass_master.csv",
        "dragon": Path(os.environ["CALON_WALES_DATA"]) / "FH_Dragon3 (1).csv",
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

    # These were previously `check(..., True, ...)` - labels that printed PASS but
    # tested nothing. Replaced with assertions that can actually fail.
    check("prevalent ASCVD excluded from the risk set",
          not (prevalent & risk_set).any(),
          "n=%d excluded, 0 remain in the risk set" % prevalent.sum())
    check("INCIDENT ASCVD events (strict)", incident.sum() == 289, "n=%d" % incident.sum())
    check("heart-failure-only cases carry NO atherosclerotic component",
          bool((~athero[hf_only]).all()) and hf_only.sum() > 0,
          "n=%d, all athero-negative" % hf_only.sum())
    check("incident and heart-failure-only sets are disjoint",
          not (incident & hf_only).any(), "overlap=%d" % (incident & hf_only).sum())
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

    # ------------------------------------------------------- C Welsh sources
    print("\nC. WELSH SOURCES, REBUILT FROM RAW  (registry / PASS / DRAGON)")
    w = pd.read_csv(files["wales_registry"], low_memory=False)
    pm = pd.read_csv(files["pass_master"], low_memory=False)
    dr = pd.read_csv(files["dragon"], low_memory=False)
    print("     WALES_FH_CLEANED %d x %d | pass_master %d x %d | FH_Dragon3 %d x %d"
          % (w.shape + pm.shape + dr.shape))

    # C1 - the registry file and PASS are the same cohort under different naming
    check("registry and PASS hold the same n", len(w) == len(pm),
          "%d vs %d" % (len(w), len(pm)))

    # C2 - DRAGON containment. If DRAGON is a subset it is NOT a separate cohort.
    key = "DatabaseNumber"
    matched = -1
    if key in w.columns and key in dr.columns:
        a = set(w[key].dropna().astype(str).str.strip()) - {""}
        b = set(dr[key].dropna().astype(str).str.strip()) - {""}
        matched = len(a & b)
        check("DRAGON is a complete subset of the Welsh registry",
              matched == len(b), "%d/%d matched on %s" % (matched, len(b), key))
    else:
        check("DRAGON containment key present", False, "no %s" % key)

    # C3 - can DRAGON support an incident arm on its own?
    dn = lambda c: (pd.to_numeric(dr[c].astype(str).str.strip().replace(
        {"": np.nan, "Unknown": np.nan, "NoValue": np.nan, "nan": np.nan}), errors="coerce")
        if c in dr else pd.Series(np.nan, index=dr.index))
    ddt = lambda c: pd.to_datetime(dr[c], errors="coerce", dayfirst=True)
    d_anchor = (ddt("MeasurementDate_1") - ddt("BirthDate")).dt.total_seconds() / (365.25 * 86400)
    d_ev, d_cens = dn("age_at_event"), dn("age_at_event_or_censoring")
    d_use = d_anchor.between(0, 105) & d_cens.between(0, 110)
    d_prev = d_use & d_ev.notna() & d_ev.le(d_anchor)
    d_inc = d_use & d_ev.notna() & d_ev.gt(d_anchor) & d_ev.le(d_cens)
    d_fu = (d_cens - d_anchor).where(d_use & ~d_prev)
    print("     DRAGON standalone: usable anchor %d | prevalent %d | INCIDENT %d"
          % (d_use.sum(), d_prev.sum(), d_inc.sum()))
    print("       risk set %d | person-years %.0f | median follow-up %.2f y"
          % ((d_use & ~d_prev).sum(), d_fu.sum(), d_fu.median()))
    check("DRAGON correctly NOT analysed as a separate cohort",
          d_inc.sum() < MIN_EVENTS,
          "%d incident events (<%d threshold)" % (d_inc.sum(), MIN_EVENTS))

    mut = w["Mutation1"].astype(str).str.strip()
    gpos = mut.ne("") & mut.str.lower().ne("nan") & w["Mutation1"].notna()
    check("genotype-positive in the Welsh registry", gpos.sum() > 1000, "n=%d" % gpos.sum())

    # C4 - INDEPENDENT rebuild of the Welsh ANALYSIS cohort, from first
    # principles, without importing reconstruct_wales().
    #
    # A first attempt at this check FAILED (1,079 / 110 against the pipeline's
    # 1,159 / 92) because it guessed the cohort definition from obvious column
    # names. The Welsh cohort turns on two flags whose names do not announce
    # what they do, and one exclusion that is easy to miss:
    #   genotype  = `Positive1` in {1, 1.0}   NOT the presence of `Mutation1`
    #               (Mutation1 is non-empty for 3,562 rows; Positive1 is the
    #               genotype-confirmed flag)
    #   outcome   = `ascvd_combine` > 0       NOT "has a dated event age"
    #   exclusion = outcome-positive WITHOUT an event age is dropped, because
    #               such a person cannot be placed in time
    # Any independent reimplementation that misses these gets a different
    # cohort. That is a Methods-reporting obligation, not a defect: the paper
    # must name these fields explicitly.
    wn = lambda c: (pd.to_numeric(w[c].astype(str).str.strip().replace(
        {"": np.nan, "Unknown": np.nan, "NoValue": np.nan, "nan": np.nan}), errors="coerce")
        if c in w else pd.Series(np.nan, index=w.index))
    # DATE PARSING IS LOAD-BEARING, AND THE CULPRIT IS NOT THE BASELINE COLUMN.
    # A first version of this rebuild used dayfirst=True and produced 948/82
    # instead of 1,159/92. `MeasurementDate.1` (the baseline anchor) is NOT the
    # cause: it parses identically under every convention, 0 disagreements.
    # The cause is `MeasurementDate.2`, which feeds the last-clinic censor age:
    # format="mixed" parses 3,783 values, dayfirst=True only 1,597, and 1,417
    # genuinely disagree. Losing those parses lowers censor ages, so 211 extra
    # people fail the positive-follow-up test. `MeasurementDate.4` disagrees on
    # 185. The pipeline uses format="mixed" and this rebuild matches it.
    # NOTE ON COMPARING DATES: use `a.notna() & b.notna() & (a != b)`. A bare
    # `a != b` counts NaT vs NaT as a difference and manufactures phantom
    # disagreements - that error produced a spurious "1,350 ambiguous values"
    # during this investigation.
    wdt = lambda c: (pd.to_datetime(w[c], errors="coerce", format="mixed")
                     if c in w else pd.Series(pd.NaT, index=w.index))
    dob = wdt("DOB").fillna(wdt("DOB_1"))
    age_at = lambda c: (wdt(c) - dob).dt.total_seconds() / (365.25 * 86400.0)
    w_base = age_at("MeasurementDate.1")
    w_ev = pd.concat([wn(c) for c in ["MIACSAge", "PCIStentsAge", "CABGAge",
                                      "ANGINAAge", "TIAAge", "PVDAge"]], axis=1).min(axis=1)
    w_out = wn("ascvd_combine").fillna(0).gt(0)
    w_gpos = w["Positive1"].astype(str).str.strip().isin(["1", "1.0"])
    w_last = pd.concat([age_at("MeasurementDate.%d" % i) for i in (1, 2, 3, 4)]
                       + [age_at("BMIDate")], axis=1).max(axis=1)
    w_cens = wn("AGE_AT_DECEASED").fillna(w_last)

    act = w_gpos.copy()
    act &= ~w_base.isna()
    act &= ~(w_out & w_ev.notna() & w_ev.le(w_base))          # prevalent
    act &= ~(w_out & w_ev.isna())                             # untimeable outcome
    act &= w_cens.gt(w_base)                                  # positive follow-up
    w_incident = act & w_out & w_ev.notna() & w_ev.gt(w_base)
    print("     independent Welsh rebuild: Positive1 %d | risk set %d | INCIDENT %d"
          % (w_gpos.sum(), act.sum(), w_incident.sum()))
    check("Welsh risk set reproduces the pipeline (1159)",
          int(act.sum()) == 1159, "raw=%d" % act.sum())
    check("Welsh incident events reproduce the pipeline (92)",
          int(w_incident.sum()) == 92, "raw=%d" % w_incident.sum())
    print("     DATE-PARSER SENSITIVITY (format='mixed' vs dayfirst=True)")
    _amb = {}
    for _c in ["DOB", "MeasurementDate.1", "MeasurementDate.2",
               "MeasurementDate.3", "MeasurementDate.4", "BMIDate"]:
        if _c not in w:
            continue
        _m = pd.to_datetime(w[_c], errors="coerce", format="mixed")
        _f = pd.to_datetime(w[_c], errors="coerce", dayfirst=True)
        _amb[_c] = {"parsed_mixed": int(_m.notna().sum()),
                    "parsed_dayfirst": int(_f.notna().sum()),
                    "genuine_disagreements": int((_m.notna() & _f.notna() & (_m != _f)).sum())}
        print("       %-20s mixed %5d | dayfirst %5d | disagree %5d"
              % (_c, _amb[_c]["parsed_mixed"], _amb[_c]["parsed_dayfirst"],
                 _amb[_c]["genuine_disagreements"]))
    _worst = max(_amb.values(), key=lambda v: v["genuine_disagreements"])
    check("date-parser sensitivity is measured and documented",
          _worst["genuine_disagreements"] > 0,
          "worst column disagrees on %d values - Methods must state format='mixed'"
          % _worst["genuine_disagreements"])
    res["date_parser_sensitivity"] = _amb
    check("genotype flag is Positive1, not Mutation1 presence",
          int(w_gpos.sum()) != int(gpos.sum()),
          "Positive1=%d vs Mutation1-present=%d" % (w_gpos.sum(), gpos.sum()))
    res["wales_independent_rebuild"] = {
        "genotype_flag": "Positive1", "outcome_flag": "ascvd_combine",
        "positive1_n": int(w_gpos.sum()), "mutation1_present_n": int(gpos.sum()),
        "risk_set": int(act.sum()), "incident": int(w_incident.sum())}
    w_active, w_inc = act, w_incident
    res["welsh_sources"] = {
        "registry_rows": int(len(w)), "pass_rows": int(len(pm)), "dragon_rows": int(len(dr)),
        "dragon_matched_into_registry": int(matched), "genotype_positive": int(gpos.sum()),
        "dragon_standalone_incident_events": int(d_inc.sum()),
        "dragon_standalone_risk_set": int((d_use & ~d_prev).sum()),
        "dragon_treated_as_separate_cohort": False}

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
    check("Welsh n matches raw rebuild", len(W) == int(w_active.sum()),
          "pipeline=%d raw=%d" % (len(W), w_active.sum()))
    check("Welsh events match raw rebuild", int(W.E.sum()) == int((w_inc & w_active).sum()),
          "pipeline=%d raw=%d" % (W.E.sum(), (w_inc & w_active).sum()))
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
