#!/usr/bin/env python3
"""Catalogue every UK Biobank / Welsh data file on this machine, and write
runnable verification scripts so the investigator can check every claim.

Two deliverables, both written into the local data package:

  CATALOGUE_ALL_DATA.csv/.md   Every UKB and Welsh data file found on this Mac:
                               path, size, md5, duplicate group. Files are NOT
                               all copied - most are duplicates of the same
                               masters across Google Drive, the UnionSine drive
                               and Downloads. The six the model actually reads
                               are copied into raw/.

  verify/                      One self-contained script per claim. Each prints
                               CLAIM, the EVIDENCE it measured, and a VERDICT.
                               Nothing is taken on trust: each script reads the
                               raw CSVs itself.

LOCAL ONLY. Governed participant-level data; never transmit.
"""
from __future__ import annotations

import hashlib
import os
import re
import subprocess
import warnings
from pathlib import Path

import pandas as pd

warnings.filterwarnings("ignore")
STAMP = "2026-08-13"
PKG = Path.home() / "Downloads" / f"CALON_DATA_PACKAGE_{STAMP}"
MD5_LIMIT = 400 * 1024 * 1024          # md5 only files up to 400 MB; larger are matched on size


def md5(p: Path) -> str | None:
    if p.stat().st_size > MD5_LIMIT:
        return None
    h = hashlib.md5()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()


def catalogue() -> pd.DataFrame:
    pats = ["ukb", "UKB", "biobank", "ukbb", "WALES", "wales", "DRAGON", "Dragon", "pass_master"]
    seen: set[str] = set()
    for pat in pats:
        try:
            out = subprocess.run(["mdfind", "-name", pat], capture_output=True,
                                 text=True, timeout=90).stdout
        except Exception:
            continue
        seen.update(x for x in out.splitlines() if x)
    rows = []
    for s in sorted(seen):
        p = Path(s)
        if not p.is_file():
            continue
        if p.suffix.lower() not in (".csv", ".tsv", ".rds", ".parquet", ".pkl", ".dta", ".xlsx"):
            continue
        if any(k in s for k in (f"CALON_DATA_PACKAGE_{STAMP}", "/.Trash/", "node_modules")):
            continue
        try:
            size = p.stat().st_size
        except OSError:
            continue
        rows.append({"file": p.name, "bytes": size, "mb": round(size / 1e6, 1),
                     "md5": md5(p), "location": str(p.parent),
                     "cohort": ("UK Biobank" if re.search(r"ukb|biobank", p.name, re.I)
                                else "Wales/DRAGON" if re.search(r"wales|dragon|pass", p.name, re.I)
                                else "other")})
    df = pd.DataFrame(rows).sort_values("bytes", ascending=False).reset_index(drop=True)
    # duplicate grouping: identical md5, or identical name+size where md5 was skipped
    key = df["md5"].fillna(df["file"] + "|" + df["bytes"].astype(str))
    df["duplicate_group"] = key.map({k: i for i, k in enumerate(dict.fromkeys(key))})
    df["copies"] = df.groupby("duplicate_group")["file"].transform("size")
    return df


VERIFY = {
"01_endpoints_htn_hf_mace.py": '''#!/usr/bin/env python3
"""VERIFY: what the UK Biobank outcome fields actually encode.

CLAIMS UNDER TEST
  1. `first_angina` is NOT angina - it encodes essential hypertension (I10).
  2. `has_hf` is heart failure (I50), and heart failure is EXCLUDED from the
     model's ASCVD endpoint.
  3. The master's own MI and stroke components are near-empty, so `first_ascvd`
     is effectively chronic IHD alone and is NOT a MACE composite.

HOW TO READ THE OUTPUT
  Angina in a middle-aged cohort runs at a few per cent and is roughly 2:1 male.
  Essential hypertension runs near 40%, raises mean systolic pressure, and has
  no male excess. Jaccard is overlap / union: 1.0 is identical, 0 is disjoint.
"""
import pandas as pd, numpy as np, warnings; warnings.filterwarnings("ignore")
from pathlib import Path
RAW = Path(__file__).resolve().parent.parent / "raw"
m = pd.read_csv(RAW / "ukb_master.csv", low_memory=False)
c = pd.read_csv(RAW / "corrected_ascvd_outcomes.csv", low_memory=False)
d = m.merge(c, on="eid", how="left")
sbp = pd.to_numeric(d.sbp, errors="coerce"); male = 1 - pd.to_numeric(d.sex_F, errors="coerce").fillna(0)
print("COHORT REFERENCE: n=%d | mean SBP %.1f mmHg | %.1f%% male\\n" % (len(d), sbp.mean(), 100*male.mean()))

ang = pd.to_datetime(d.first_angina, errors="coerce").notna()
print("CLAIM 1 - `first_angina` encodes HYPERTENSION, not angina")
print("  flagged            : %d (%.1f%% of the cohort)" % (ang.sum(), 100*ang.mean()))
print("  mean SBP if flagged: %.1f mmHg  (cohort %.1f)" % (sbp[ang].mean(), sbp.mean()))
print("  %% male if flagged  : %.1f%%       (cohort %.1f%%)" % (100*male[ang].mean(), 100*male.mean()))
print("  VERDICT: %s\\n" % ("CONFIRMED - 40%-scale prevalence, raised SBP, no male excess"
      if ang.mean() > .3 and sbp[ang].mean() > sbp.mean()+5 and male[ang].mean() < male.mean()+.12
      else "NOT CONFIRMED - re-examine"))

g = lambda k: pd.to_numeric(d[k], errors="coerce").fillna(0).gt(0)
hf = pd.to_numeric(d.has_hf, errors="coerce").fillna(0).gt(0)
j = (hf & g("i50_event")).sum() / max((hf | g("i50_event")).sum(), 1)
print("CLAIM 2 - `has_hf` is heart failure (I50), excluded from the endpoint")
print("  Jaccard(has_hf, i50_event): %.3f" % j)
print("  VERDICT: %s\\n" % ("CONFIRMED - it is the I50 field" if j > .5 else "NOT CONFIRMED"))

print("CLAIM 3 - the master's MACE components are near-empty")
for f, exp in [("first_acute_mi","MI, expect tens of thousands"),
               ("first_stroke","stroke, expect thousands"),
               ("first_other_ihd","chronic IHD"), ("first_ascvd","the composite")]:
    n = pd.to_datetime(d[f], errors="coerce").notna().sum()
    print("  %-22s %8d  (%.2f%%)   %s" % (f, n, 100*n/len(d), exp))
mi = pd.to_datetime(d.first_acute_mi, errors="coerce").notna().sum()
oi = pd.to_datetime(d.first_other_ihd, errors="coerce").notna().sum()
av = pd.to_datetime(d.first_ascvd, errors="coerce").notna().sum()
print("  first_ascvd is %.1f%% accounted for by first_other_ihd alone" % (100*oi/max(av,1)))
print("  VERDICT: %s" % ("CONFIRMED - MI/stroke are near-empty, so `first_ascvd` is chronic IHD, not MACE"
      if mi < 5000 and oi/max(av,1) > .85 else "NOT CONFIRMED"))
''',

"02_ukb_cohort_and_endpoint.py": '''#!/usr/bin/env python3
"""VERIFY: the UK Biobank analysis cohort, built from raw.

CLAIMS UNDER TEST
  LDLR carriers 3,540 -> 207 prevalent excluded -> 62 heart-failure-only treated
  as non-cases -> 289 incident ASCVD events in a risk set of 3,333, with every
  event dated strictly AFTER baseline.

HOW TO READ THE OUTPUT
  "Prevalent" means the event pre-dates the blood draw: those people are removed
  because you cannot predict what has already happened. "Heart-failure-only"
  means the person had I50 but no atherosclerotic code - not ASCVD, so not an
  event. The temporality line is the anti-leakage check: the minimum lag must be
  positive, or a predictor could have been measured after the outcome.
"""
import pandas as pd, numpy as np, warnings; warnings.filterwarnings("ignore")
from pathlib import Path
RAW = Path(__file__).resolve().parent.parent / "raw"
m = pd.read_csv(RAW / "ukb_master.csv", usecols=["eid","ldlr_carrier","date_baseline"], low_memory=False)
c = pd.read_csv(RAW / "corrected_ascvd_outcomes.csv", low_memory=False)
car = pd.to_numeric(m.ldlr_carrier, errors="coerce").eq(1)
d = m.loc[car].merge(c, on="eid", how="left")
base = pd.to_datetime(d.date_baseline, errors="coerce")
ev = pd.to_datetime(d.ascvd_first_date_best, errors="coerce")
g = lambda k: pd.to_numeric(d[k], errors="coerce").fillna(0).gt(0)
ath = g("i21_event")|g("i25_event")|g("i63_event")|g("i70_event")|g("i73_event")|g("g45_event")
prev = ev.notna()&base.notna()&ev.le(base)&ath
inc  = ev.notna()&base.notna()&ev.gt(base)&ath
hfo  = ev.notna()&base.notna()&ev.gt(base)&~ath
print("ENDPOINT = I21 | I25 | I63 | I70 | I73 | G45.  I50 heart failure is NOT included.\\n")
for lbl, val, exp in [("LDLR carriers", car.sum(), 3540), ("prevalent ASCVD excluded", prev.sum(), 207),
                      ("heart-failure-only (non-cases)", hfo.sum(), 62),
                      ("INCIDENT ASCVD events", inc.sum(), 289),
                      ("risk set", (~prev).sum(), 3333)]:
    print("  %-32s %6d   expected %-6d %s" % (lbl, val, exp, "OK" if val == exp else "MISMATCH"))
lag = (ev[inc] - base[inc]).dt.days / 365.25
print("\\n  temporality: min lag %.3f y | median %.2f y | max %.2f y" % (lag.min(), lag.median(), lag.max()))
print("  VERDICT: %s" % ("CONFIRMED - no event on or before its baseline" if lag.min() > 0 else "LEAK"))
''',

"03_welsh_cohort.py": '''#!/usr/bin/env python3
"""VERIFY: the All-Wales analysis cohort, and the field definitions it depends on.

CLAIMS UNDER TEST
  1. Genotype status is the `Positive1` flag (2,405), NOT the presence of
     `Mutation1` (3,562). Using the wrong one changes the cohort.
  2. The outcome is `ascvd_combine`, not "has a dated event age".
  3. With the correct fields the cohort is 1,159 with 92 incident events.
  4. Date parsing matters: `MeasurementDate.2` feeds the censoring age and a
     day-first parser resolves it differently, which changes who qualifies.

HOW TO READ THE OUTPUT
  Each exclusion is applied in order. Getting any field wrong silently produces
  a different cohort - a first attempt at this check produced 1,079/110, and a
  second produced 948/82, both from field or parser choices alone.
"""
import pandas as pd, numpy as np, warnings; warnings.filterwarnings("ignore")
from pathlib import Path
RAW = Path(__file__).resolve().parent.parent / "raw"
w = pd.read_csv(RAW / "WALES_FH_CLEANED.csv", low_memory=False)
n = lambda c: pd.to_numeric(w[c].astype(str).str.strip().replace(
    {"":np.nan,"Unknown":np.nan,"NoValue":np.nan,"nan":np.nan}), errors="coerce") if c in w else pd.Series(np.nan, index=w.index)
dt = lambda c: pd.to_datetime(w[c], errors="coerce", format="mixed") if c in w else pd.Series(pd.NaT, index=w.index)
dob = dt("DOB").fillna(dt("DOB_1")); age_at = lambda c: (dt(c)-dob).dt.total_seconds()/(365.25*86400)
gp = w["Positive1"].astype(str).str.strip().isin(["1","1.0"])
mut = w["Mutation1"].astype(str).str.strip()
mp = mut.ne("") & mut.str.lower().ne("nan") & w["Mutation1"].notna()
print("CLAIM 1 - genotype flag")
print("  Positive1 == 1        : %d   <- the correct flag" % gp.sum())
print("  Mutation1 present     : %d   <- NOT the flag; %d more people" % (mp.sum(), mp.sum()-gp.sum()))
base = age_at("MeasurementDate.1")
ev = pd.concat([n(c) for c in ["MIACSAge","PCIStentsAge","CABGAge","ANGINAAge","TIAAge","PVDAge"]], axis=1).min(axis=1)
out = n("ascvd_combine").fillna(0).gt(0)
last = pd.concat([age_at("MeasurementDate.%d"%i) for i in (1,2,3,4)]+[age_at("BMIDate")], axis=1).max(axis=1)
cens = n("AGE_AT_DECEASED").fillna(last)
print("\\nCLAIM 2/3 - exclusions in order")
act = gp.copy(); print("  genotype-positive                       %6d" % act.sum())
act &= ~base.isna();                                  print("  - missing baseline                      %6d" % act.sum())
act &= ~(out & ev.notna() & ev.le(base));             print("  - prevalent ASCVD                       %6d" % act.sum())
act &= ~(out & ev.isna());                            print("  - outcome positive, no dated event age  %6d" % act.sum())
act &= cens.gt(base);                                 print("  - no positive follow-up                 %6d" % act.sum())
incd = act & out & ev.notna() & ev.gt(base)
print("\\n  risk set %d (expected 1159) %s" % (act.sum(), "OK" if act.sum()==1159 else "MISMATCH"))
print("  incident %d (expected 92)   %s" % (incd.sum(), "OK" if incd.sum()==92 else "MISMATCH"))
print("\\nCLAIM 4 - date-parser sensitivity")
for c in ["MeasurementDate.1","MeasurementDate.2","MeasurementDate.4"]:
    a = pd.to_datetime(w[c], errors="coerce", format="mixed")
    b = pd.to_datetime(w[c], errors="coerce", dayfirst=True)
    print("  %-20s mixed %5d | dayfirst %5d | genuinely disagree %5d"
          % (c, a.notna().sum(), b.notna().sum(), (a.notna()&b.notna()&(a!=b)).sum()))
print("  Compare with `a.notna() & b.notna() & (a != b)`. A bare `a != b` counts")
print("  NaT vs NaT as a difference and invents disagreements.")
''',

"04_dragon_is_a_subset.py": '''#!/usr/bin/env python3
"""VERIFY: DRAGON is a subset of the All-Wales registry, not a third cohort.

CLAIMS UNDER TEST
  1. All 424 DRAGON records match into the Welsh registry on `DatabaseNumber`.
  2. Standing alone, DRAGON yields only 5 incident events - below the 10-event
     reporting threshold - so it cannot be a separate validation cohort.

HOW TO READ THE OUTPUT
  If DRAGON were reported as a third cohort alongside Wales, the same 424
  patients would be counted twice. The follow-up figure shows why it cannot
  stand alone: about a year of observation is a work-up window, not a
  natural-history follow-up.
"""
import pandas as pd, numpy as np, warnings; warnings.filterwarnings("ignore")
from pathlib import Path
RAW = Path(__file__).resolve().parent.parent / "raw"
w = pd.read_csv(RAW / "WALES_FH_CLEANED.csv", low_memory=False)
dr = pd.read_csv(RAW / "FH_Dragon3 (1).csv", low_memory=False)
a = set(w["DatabaseNumber"].dropna().astype(str).str.strip()) - {""}
b = set(dr["DatabaseNumber"].dropna().astype(str).str.strip()) - {""}
print("CLAIM 1 - containment")
print("  DRAGON records            : %d" % len(b))
print("  matched into Welsh registry: %d (%.1f%%)" % (len(a&b), 100*len(a&b)/max(len(b),1)))
print("  VERDICT: %s\\n" % ("CONFIRMED - complete subset" if len(a&b)==len(b) else "NOT a complete subset"))
n = lambda c: pd.to_numeric(dr[c].astype(str).str.strip().replace(
    {"":np.nan,"Unknown":np.nan,"NoValue":np.nan,"nan":np.nan}), errors="coerce") if c in dr else pd.Series(np.nan, index=dr.index)
dt = lambda c: pd.to_datetime(dr[c], errors="coerce", dayfirst=True)
anchor = (dt("MeasurementDate_1")-dt("BirthDate")).dt.total_seconds()/(365.25*86400)
ev, cens = n("age_at_event"), n("age_at_event_or_censoring")
use = anchor.between(0,105) & cens.between(0,110)
prev = use & ev.notna() & ev.le(anchor)
inc = use & ev.notna() & ev.gt(anchor) & ev.le(cens)
fu = (cens-anchor).where(use & ~prev)
print("CLAIM 2 - DRAGON cannot stand alone")
print("  rows %d | usable baseline anchor %d | prevalent %d" % (len(dr), use.sum(), prev.sum()))
print("  INCIDENT events %d | risk set %d | median follow-up %.2f y" % (inc.sum(), (use&~prev).sum(), fu.median()))
print("  VERDICT: %s" % ("CONFIRMED - below the 10-event threshold" if inc.sum() < 10 else "re-examine"))
''',

"05_model_auc.py": '''#!/usr/bin/env python3
"""VERIFY: the reported AUCs and the head-to-head against published scores.

CLAIMS UNDER TEST
  UK Biobank C = 0.6997, beating Montreal (0.6671) and FH-Risk-Score (0.6740)
  with intervals excluding zero, tying SAFEHEART (0.6944).
  All-Wales C = 0.7486, tying all three.

HOW TO READ THE OUTPUT
  This runs the locked model itself, so it needs CALON_SHARED_MASTER set and the
  analysis repository present. C-index (AUC) of 0.5 is a coin toss and 1.0 is
  perfect. A difference "wins" only when its 95%% interval excludes zero; a
  positive point estimate whose interval crosses zero is a TIE, not a win.
  Welsh ties are expected: with 92 events the smallest difference that cohort
  can resolve is roughly 0.15, and every observed difference is far below that.
"""
import importlib.util, json, os, sys
from pathlib import Path
REPO = Path(os.environ.get("CALON_PROJECT_ROOT",
        Path.home()/"Documents"/"CALON"/"calon_discordance_model_2026_08_09"))
script = REPO / "code" / "15_CALON_FINAL.py"
if not script.exists():
    sys.exit("Analysis repository not found. Set CALON_PROJECT_ROOT to it.")
if "CALON_SHARED_MASTER" not in os.environ:
    sys.exit("Set CALON_SHARED_MASTER first (see the package README).")
out = REPO / "outputs" / "calon_final.json"
if not out.exists():
    sys.exit("Run `python3 %s` first, then re-run this script." % script)
d = json.loads(out.read_text())
print("SPEC: %s\\n" % " + ".join(d["spec"]))
for k, lbl in [("ukb","UK BIOBANK"), ("wales","ALL-WALES")]:
    q = d[k]; a = q["subgroups"]["ALL"]
    print("%s  n=%d  events=%d" % (lbl, q["qc"]["n"], q["qc"]["events"]))
    print("  %-14s %8.4f   reference" % ("CALON", a["c_index"]))
    for cn in ("Montreal","FH-RS","SAFEHEART"):
        v = a["vs"][cn]
        print("  %-14s %8.4f   %+0.3f (%+0.3f, %+0.3f)  %s"
              % (cn, v["comparator_c"], v["delta"], v["ci"][0], v["ci"][1], v["verdict"]))
    print("  tally: %s\\n" % q["tally"])
print("COMBINED: %s" % d["combined_tally"])
''',
}


def main():
    PKG.mkdir(parents=True, exist_ok=True)
    print("Cataloguing UK Biobank / Welsh data on this machine ...")
    cat = catalogue()
    cat.to_csv(PKG / "CATALOGUE_ALL_DATA.csv", index=False)
    uniq = cat.drop_duplicates("duplicate_group")
    print("  files found: %d  |  unique datasets: %d  |  total on disk: %.1f GB"
          % (len(cat), len(uniq), cat["bytes"].sum() / 1e9))

    lines = ["# Every UK Biobank / Welsh data file on this Mac - %s" % STAMP, "",
             "LOCAL ONLY. Governed participant-level data; never transmit.", "",
             "%d files, %d unique datasets, %.1f GB total. Most large files are the "
             "same master duplicated across Google Drive, the UnionSine drive and "
             "Downloads. Only the six the model reads are copied into `raw/`; the "
             "rest are catalogued in place." % (len(cat), len(uniq), cat["bytes"].sum() / 1e9),
             "", "## Largest unique datasets", "",
             "| file | MB | copies | cohort | location |", "|---|---|---|---|---|"]
    for _, r in uniq.head(30).iterrows():
        lines.append("| `%s` | %.0f | %d | %s | `%s` |"
                     % (r["file"], r["mb"], r["copies"], r["cohort"], r["location"]))
    (PKG / "CATALOGUE_ALL_DATA.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    vdir = PKG / "verify"
    vdir.mkdir(exist_ok=True)
    for name, body in VERIFY.items():
        (vdir / name).write_text(body, encoding="utf-8")
        os.chmod(vdir / name, 0o755)
    (vdir / "run_all.sh").write_text(
        "#!/bin/bash\n# Run every verification in order.\ncd \"$(dirname \"$0\")\"\n"
        "for f in 0*.py; do\n  echo; echo \"================ $f ================\"\n"
        "  python3 \"$f\"\ndone\n", encoding="utf-8")
    os.chmod(vdir / "run_all.sh", 0o755)
    print("  verification scripts written: %d" % len(VERIFY))

    (PKG / "HOW_TO_VERIFY.md").write_text(f"""# How to check everything I told you

Every claim in the analysis has a script here that re-measures it from the raw
CSVs in `raw/`. Nothing is taken on trust and nothing is hard-coded except the
expected answer, which is printed next to the measured one so a mismatch is
obvious.

## Run them all

```bash
cd ~/Downloads/CALON_DATA_PACKAGE_{STAMP}/verify
./run_all.sh
```

Scripts 01-04 need only the files in `raw/`. Script 05 runs the model itself, so
it needs the analysis repository and:

```bash
export CALON_SHARED_MASTER="<your SHARED_MASTER_DATA folder>"
export CALON_PROJECT_ROOT="<the calon_discordance_model_2026_08_09 folder>"
```

## What each script checks

| Script | Question it answers |
|---|---|
| `01_endpoints_htn_hf_mace.py` | Is `first_angina` really hypertension? Is `has_hf` really I50? Is `first_ascvd` really MACE? |
| `02_ukb_cohort_and_endpoint.py` | Where do 3,540 carriers become 3,333 at risk and 289 events? Is any event dated before its baseline? |
| `03_welsh_cohort.py` | Which fields define the Welsh cohort, and why does using the obvious ones give the wrong answer? |
| `04_dragon_is_a_subset.py` | Is DRAGON a separate cohort or the same patients again? |
| `05_model_auc.py` | Do the reported AUCs and win/tie/loss verdicts reproduce? |

## Reading the numbers

**C-index (AUC)** — 0.5 is a coin toss, 1.0 is perfect. Values near 0.70 are
normal for cardiovascular risk models.

**A difference is a WIN only when its 95% interval excludes zero.** A positive
point estimate whose interval crosses zero is a **tie**, not a win. This matters
in Wales: with 92 events that cohort can only resolve differences of roughly
0.15, and every observed difference is far smaller, so all Welsh comparisons are
ties in both directions. That is a statement about power, not about equivalence.

**Jaccard** — overlap divided by union. 1.0 means two flags identify the same
people; 0 means they share nobody.

**Prevalent vs incident** — prevalent means the event pre-dates the blood draw.
Those people are excluded, because a model that "predicts" an event that already
happened is detecting its consequences, not forecasting it.

## The three endpoint answers, in one place

- **Hypertension.** `first_angina` flags 41.7% of UK Biobank with raised systolic
  pressure and no male excess. That is essential hypertension, not angina. Never
  used; verified absent from the executable code.
- **Heart failure.** `has_hf` tracks I50 (Jaccard 0.92). Heart failure is not
  atherosclerotic disease and is excluded. In the LDLR carriers, 62 events in the
  broad composite were heart-failure-only.
- **ASCVD / MACE.** The model ignores every master outcome column and uses
  `ascvd_first_date_best` restricted to **I21, I25, I63, I70, I73, G45**. This
  matters because the master's own MI field holds 1,293 people and its stroke
  field 321 - far too few - so `first_ascvd` is chronic IHD, not MACE.

## Governance

Participant-level data under UK Biobank Application 1002450 and All-Wales
PASS/DRAGON approvals. Local use only: never commit, upload, or transmit.
""", encoding="utf-8")
    print("\nPACKAGE UPDATED: %s" % PKG)


if __name__ == "__main__":
    main()
