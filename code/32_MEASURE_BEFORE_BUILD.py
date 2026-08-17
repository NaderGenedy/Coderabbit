#!/usr/bin/env python3
"""Measure the open questions against RAW DATA. No model is fitted here.

Every number this prints is a fact about the raw files, established before any
specification is chosen. Written after an independent adversarial audit of
CALON-H found four unresolved items:

  Q1 ENDPOINT DATING.  corrected_ascvd_outcomes.csv carries only two composite
     dates and no per-component dates. `ascvd_first_date_best` fires for
     heart-failure-only and no-flag participants, so for anyone with BOTH I50
     and an atherosclerotic component the recorded date may be the I50 date.
     How many incident cases are affected, and how far off can the date be?

  Q2 WELSH HYPERTENSION LEAK.  BloodPressureDate EXISTS. How many participants
     have a BP reading dated on or before the baseline visit (usable), versus
     dated after the event (contaminated)? Can a clean dated htn be built?

  Q3 WELSH EXCLUSIONS.  659 dropped for "no operational follow-up", reportedly
     including dated post-baseline events. Exact flow, and how many events.

  Q4 DATED SMOKING / DIABETES.  SmokerWhenStoppedYear and DiabetesYear exist.
     Can either be anchored to baseline?

  Q5 EPV and RELATEDNESS.  Events per parameter by cohort and horizon; whether
     UK Biobank carries any kinship/relatedness field at all.

Governance: aggregate counts only. No participant rows or identifiers printed.
"""
from __future__ import annotations

import importlib.util
import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

_s = importlib.util.spec_from_file_location(
    "vw", ROOT / "code" / "audit_2026_08_10" / "07_verify_welsh_prospective.py")
vw = importlib.util.module_from_spec(_s); sys.modules["vw"] = vw
_s.loader.exec_module(vw)

R = Path(os.environ["CALON_CORRECTED_DATA"])
M = Path(os.environ["CALON_SHARED_MASTER"]) / "UKB" / "ukb_master.csv"
W = Path("/Users/nader85/Downloads/WALES_FH_CLEANED.csv")
if not W.exists():
    W = Path("/Users/nader85/Downloads/CALON_DATA_PACKAGE_2026-08-13/raw/all_inputs/WALES_FH_CLEANED.csv")

facts = {}
p = lambda k, v: (print(f"  {k:58s} {v}"), facts.__setitem__(k, v))

# ------------------------------------------------------------------ Q1 UKB
print("=" * 84)
print("Q1  ENDPOINT DATING — can the recorded date belong to a non-ASCVD event?")
c = pd.read_csv(R / "data_corrected" / "corrected_ascvd_outcomes.csv", low_memory=False)
m = pd.read_csv(M, usecols=["eid", "ldlr_carrier", "date_baseline"], low_memory=False)
d = m.merge(c, on="eid", how="left")
d = d.loc[pd.to_numeric(d.ldlr_carrier, errors="coerce").eq(1)].reset_index(drop=True)
g = lambda k: pd.to_numeric(d[k], errors="coerce").fillna(0).gt(0)
ath = (g("i21_event") | g("i25_event") | g("i63_event")
       | g("i70_event") | g("i73_event") | g("g45_event"))
base = pd.to_datetime(d.date_baseline, errors="coerce")
best = pd.to_datetime(d.ascvd_first_date_best, errors="coerce")
dated = pd.to_datetime(d.ascvd_first_date_dated, errors="coerce")
inc = best.notna() & base.notna() & best.gt(base) & ath

p("incident atherosclerotic cases (the 289)", int(inc.sum()))
p("  ...of whom ALSO have i50 heart failure", int((inc & g("i50_event")).sum()))
p("  ...of whom have EXACTLY ONE athero component (date unambiguous)",
  int((inc & (g("i21_event").astype(int) + g("i25_event").astype(int)
              + g("i63_event").astype(int) + g("i70_event").astype(int)
              + g("i73_event").astype(int) + g("g45_event").astype(int) == 1)).sum()))
p("  ...i50-free AND single-component (fully clean date)",
  int((inc & ~g("i50_event")
       & (g("i21_event").astype(int) + g("i25_event").astype(int)
          + g("i63_event").astype(int) + g("i70_event").astype(int)
          + g("i73_event").astype(int) + g("g45_event").astype(int) == 1)).sum()))
agree = inc & best.notna() & dated.notna()
p("incident cases where best and dated both present", int(agree.sum()))
p("  ...and the two dates DISAGREE", int((agree & best.ne(dated)).sum()))
diff = (best - dated).dt.days[agree & best.ne(dated)]
p("  ...median |disagreement| in days", float(diff.abs().median()) if len(diff) else "n/a")
p("i50-positive carriers with NO athero component (must be non-cases)",
  int((g("i50_event") & ~ath).sum()))

# ------------------------------------------------------------- Q2/Q3/Q4 Wales
print("=" * 84)
print("Q2  WELSH HYPERTENSION — is a temporally clean htn constructible?")
raw = pd.read_csv(W, low_memory=False)
flow, active, incident, bage = vw.reconstruct_wales(raw)
dob = vw.date(raw, "DOB").fillna(vw.date(raw, "DOB_1"))
bdate = vw.date(raw, "MeasurementDate.1")
bpdate = vw.date(raw, "BloodPressureDate")
num = lambda c: (pd.to_numeric(raw[c].astype(str).str.strip().replace(
    {"": np.nan, "Unknown": np.nan, "NoValue": np.nan, "nan": np.nan}), errors="coerce")
    if c in raw else pd.Series(np.nan, index=raw.index))
ev_age = pd.concat([num(c) for c in ["MIACSAge", "PCIStentsAge", "CABGAge",
                                     "ANGINAAge", "TIAAge", "PVDAge"]], axis=1).min(axis=1)
ev_date = dob + pd.to_timedelta(ev_age * 365.25, unit="D")
A = active.fillna(False)

p("Welsh analysis cohort", int(A.sum()))
p("  BloodPressureDate present", int((A & bpdate.notna()).sum()))
p("  BP dated ON OR BEFORE baseline visit  (USABLE)", int((A & bpdate.notna() & bdate.notna() & bpdate.le(bdate)).sum()))
p("  BP dated AFTER baseline visit         (post-baseline)", int((A & bpdate.notna() & bdate.notna() & bpdate.gt(bdate)).sum()))
p("  BP date missing entirely", int((A & bpdate.isna()).sum()))
INC = incident.fillna(False)
p("incident events", int(INC.sum()))
p("  events whose BP is dated AFTER the event (CONTAMINATED)",
  int((INC & bpdate.notna() & ev_date.notna() & bpdate.gt(ev_date)).sum()))
p("  events with BP dated on/before baseline (clean)",
  int((INC & bpdate.notna() & bdate.notna() & bpdate.le(bdate)).sum()))
p("BloodPressureMedication has any date column", "NO — undated status field")
p("clean-BP subset: n / events",
  f"{int((A & bpdate.notna() & bdate.notna() & bpdate.le(bdate)).sum())} / "
  f"{int((INC & bpdate.notna() & bdate.notna() & bpdate.le(bdate)).sum())}")

print("=" * 84)
print("Q3  WELSH EXCLUSION FLOW (verbatim from the reconstruction)")
for k, v in flow.items():
    p("  " + k, v)

print("=" * 84)
print("Q4  DATED SMOKING / DIABETES — anchorable to baseline?")
dyear = num("DiabetesYear")
byear = bdate.dt.year
p("DiabetesYear present in cohort", int((A & dyear.notna()).sum()))
p("  ...of those, diagnosed ON OR BEFORE baseline year", int((A & dyear.notna() & byear.notna() & dyear.le(byear)).sum()))
p("  ...diagnosed AFTER baseline year (must be coded 0 at baseline)",
  int((A & dyear.notna() & byear.notna() & dyear.gt(byear)).sum()))
p("Diabetes flag present but undated", int((A & num("Diabetes").notna() & dyear.isna()).sum()))
syear = num("SmokerWhenStoppedYear")
p("SmokerWhenStoppedYear present", int((A & syear.notna()).sum()))
p("Smoking flag present but no stop-year", int((A & num("Smoking").notna() & syear.isna()).sum()))

print("=" * 84)
print("Q5  EPV AND RELATEDNESS")
hdr = pd.read_csv(M, nrows=1)
kin = [c for c in hdr.columns if any(k in c.lower() for k in
       ("kinship", "related", "genetic_rel", "pc1", "principal"))]
p("UKB kinship/relatedness columns found", kin if kin else "NONE")
p("UKB clusters used", "singleton per participant — no relatedness control")
p("Welsh clusters (FamilyNumber)", int(raw.loc[A, "FamilyNumber"].astype(str).nunique()))
T = (ev_age.where(INC, num("AGE_AT_DECEASED").fillna(
    pd.concat([(vw.date(raw, "MeasurementDate.%d" % i) - dob).dt.days / 365.25
               for i in (1, 2, 3, 4)], axis=1).max(axis=1))) - bage)
for H, lab in ((None, "full"), (10, "10y"), (5, "5y")):
    ev = int(INC.sum()) if H is None else int((INC & T.le(H)).sum())
    p(f"  Wales events {lab} / EPV at 7 terms", f"{ev} / {ev/7:.1f}")
for H, lab, ev in ((None, "full", 289), (10, "10y", 194), (5, "5y", 97)):
    p(f"  UKB events {lab} / EPV at 9 terms", f"{ev} / {ev/9:.1f}")

(OUT / "measure_before_build.json").write_text(json.dumps(facts, indent=2, default=str))
print("=" * 84)
print("written:", OUT / "measure_before_build.json")
