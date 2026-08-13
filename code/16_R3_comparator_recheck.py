#!/usr/bin/env python3
"""R3 RE-TEST: does "published FH scores work as well in matched non-carriers"
survive when the comparators are the PUBLISHED equations?

WHY THIS EXISTS
---------------
code/08_fh_vs_nonfh_robustness.py test R3 asked whether Montreal-FH-SCORE and the
FH-Risk-Score discriminate as well in age/sex-matched non-carriers as in FH
carriers. If they do, the FH-specific part of a model is its baseline level, not
its risk-factor slopes - a conclusion this programme has carried forward.

That test did not score the published equations. Its `montreal()` was
    age + 10*male - 10*HDL + 5*hypertension + 5*smoking
and its docstring claimed an Lp(a) term the function never had. Its `fhrs()` was
    age + 8*male - 8*HDL + 2*LDL + 6*hypertension + 6*smoking
Neither set of weights appears in either publication. The conclusion therefore
rested on invented coefficients.

This script scores BOTH forms side by side on the identical matched sets, so the
size of the error is measurable rather than assumed. The published equations are
the same ones used by code/15_CALON_FINAL.py:

  Montreal-FH-SCORE (Paquette 2017)
      0.75*z(age) - 0.27*z(HDL) + 0.25*male + 0.19*hypertension + 0.12*smoking
  FH-Risk-Score (Paquette 2021)
      age bands + LDL bands + HDL bands + 0.721*male + 0.644*hypertension
      + 0.625*smoking + 0.434*[Lp(a) >= 105]

Governance: aggregate output only.
"""
from __future__ import annotations

import os

import importlib.util
import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

warnings.filterwarnings("ignore")

ROOT = Path(os.environ["CALON_PROJECT_ROOT"])
OUT = ROOT / "outputs"
SEED = 20260810
BOOT = 2000


def _load(name, path):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    sys.modules[name] = m
    s.loader.exec_module(m)
    return m


f = _load("fhnf", ROOT / "code" / "07_fh_vs_nonfh.py")
rob = _load("rob", ROOT / "code" / "08_fh_vs_nonfh_robustness.py")


# ------------------------------------------------- the two comparator versions
def montreal_invented(d):
    a = pd.to_numeric(d["age"], errors="coerce")
    return np.asarray(a.fillna(a.median())
                      + 10 * pd.to_numeric(d["male"], errors="coerce").fillna(0)
                      - 10 * pd.to_numeric(d["hdl"], errors="coerce").fillna(1.4)
                      + 5 * pd.to_numeric(d["hypertension"], errors="coerce").fillna(0)
                      + 5 * pd.to_numeric(d["smoke_ever"], errors="coerce").fillna(0), float)


def fhrs_invented(d):
    a = pd.to_numeric(d["age"], errors="coerce")
    return np.asarray(a.fillna(a.median())
                      + 8 * pd.to_numeric(d["male"], errors="coerce").fillna(0)
                      - 8 * pd.to_numeric(d["hdl"], errors="coerce").fillna(1.4)
                      + 2 * pd.to_numeric(d["ldl"], errors="coerce").fillna(3.9)
                      + 6 * pd.to_numeric(d["hypertension"], errors="coerce").fillna(0)
                      + 6 * pd.to_numeric(d["smoke_ever"], errors="coerce").fillna(0), float)


def _cols(d):
    g = lambda c, fb: pd.to_numeric(d[c], errors="coerce") if c in d else pd.Series(fb, index=d.index)
    a = g("age", np.nan)
    hdl = g("hdl", np.nan).fillna(1.35)
    ldl = g("ldl", np.nan)
    return (a.fillna(a.median()), hdl, ldl.fillna(ldl.median()),
            g("male", 0).fillna(0), g("hypertension", 0).fillna(0),
            g("smoke_ever", 0).fillna(0), g("lpa", 0).fillna(0))


def montreal_published(d):
    a, hdl, _, ml, ht, sk, _ = _cols(d)
    return np.asarray(0.75 * (a - a.mean()) / a.std() - 0.27 * (hdl - hdl.mean()) / hdl.std()
                      + 0.25 * ml + 0.19 * ht + 0.12 * sk, float)


def fhrs_published(d):
    a, hdl, ldl, ml, ht, sk, lpa = _cols(d)
    ab = lambda v: (0 if v <= 30 else .938 if v <= 35 else 1.383 if v <= 40 else 1.621 if v <= 45
                    else 1.738 if v <= 50 else 1.804 if v <= 55 else 1.964 if v <= 60 else 2.256)
    lb = lambda v: (0 if v <= 5.5 else .315 if v <= 7.5 else .718 if v <= 8.5
                    else .918 if v <= 9.5 else 1.136)
    hb = lambda v: (0 if v > 1.30 else .298 if v >= 1.01 else .712 if v >= 0.85 else .752)
    return np.asarray(np.array([ab(v) for v in a]) + np.array([lb(v) for v in ldl])
                      + np.array([hb(v) for v in hdl]) + 0.721 * ml + 0.644 * ht
                      + 0.625 * sk + 0.434 * (lpa >= 105).astype(float), float)


def auc_ci(y, p, seed=SEED, b=BOOT):
    y, p = np.asarray(y, int), np.asarray(p, float)
    rng = np.random.default_rng(seed)
    v = []
    for _ in range(b):
        tk = rng.integers(0, len(y), len(y))
        if len(np.unique(y[tk])) < 2:
            continue
        v.append(roc_auc_score(y[tk], p[tk]))
    return float(roc_auc_score(y, p)), float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))


def gap_ci(y_fh, p_fh, y_nf, p_nf, seed=SEED, b=BOOT):
    """AUC in FH minus AUC in matched non-FH, with a bootstrap interval."""
    rng = np.random.default_rng(seed)
    y_fh, p_fh, y_nf, p_nf = map(np.asarray, (y_fh, p_fh, y_nf, p_nf))
    pt = roc_auc_score(y_fh, p_fh) - roc_auc_score(y_nf, p_nf)
    v = []
    for _ in range(b):
        i = rng.integers(0, len(y_fh), len(y_fh))
        j = rng.integers(0, len(y_nf), len(y_nf))
        if len(np.unique(y_fh[i])) < 2 or len(np.unique(y_nf[j])) < 2:
            continue
        v.append(roc_auc_score(y_fh[i], p_fh[i]) - roc_auc_score(y_nf[j], p_nf[j]))
    return pt, float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))


def main():
    fh_all, pool = rob.build()
    keep, ctrl = f.match(fh_all["age"].to_numpy(float), fh_all["male"].to_numpy(float),
                         pool, 5, 1.0, SEED)
    fh = fh_all.iloc[keep].reset_index(drop=True)
    ctrl = ctrl.reset_index(drop=True)
    y_fh, y_nf = fh["y"].to_numpy(int), ctrl["y"].to_numpy(int)

    print("=" * 100)
    print("R3 RE-TEST  |  do published FH scores discriminate as well in matched non-carriers?")
    print("=" * 100)
    print("  FH carriers      n=%-5d events=%-4d" % (len(fh), y_fh.sum()))
    print("  matched non-FH   n=%-5d events=%-4d" % (len(ctrl), y_nf.sum()))
    print("  Lp(a) available in the matched frames: FH %s | non-FH %s"
          % ("yes" if "lpa" in fh else "NO (term scored as 0)",
             "yes" if "lpa" in ctrl else "NO (term scored as 0)"))

    versions = {
        "Montreal  INVENTED (as run in code/08)": montreal_invented,
        "Montreal  PUBLISHED (Paquette 2017)": montreal_published,
        "FH-RS     INVENTED (as run in code/08)": fhrs_invented,
        "FH-RS     PUBLISHED (Paquette 2021)": fhrs_published,
    }
    res = {"seed": SEED, "bootstrap": BOOT, "participant_level_outputs": False,
           "n_fh": int(len(fh)), "events_fh": int(y_fh.sum()),
           "n_nonfh": int(len(ctrl)), "events_nonfh": int(y_nf.sum()),
           "lpa_present": bool("lpa" in fh and "lpa" in ctrl), "scores": {}}

    print("\n  %-40s %-22s %-22s %s"
          % ("score version", "AUC in FH", "AUC in matched non-FH", "gap (FH - nonFH)"))
    for lbl, fn in versions.items():
        a_fh = auc_ci(y_fh, fn(fh))
        a_nf = auc_ci(y_nf, fn(ctrl))
        g, glo, ghi = gap_ci(y_fh, fn(fh), y_nf, fn(ctrl))
        verdict = "DIFFERS" if (glo > 0 or ghi < 0) else "no difference"
        res["scores"][lbl] = {"auc_fh": a_fh[0], "auc_fh_ci": [a_fh[1], a_fh[2]],
                              "auc_nonfh": a_nf[0], "auc_nonfh_ci": [a_nf[1], a_nf[2]],
                              "gap": g, "gap_ci": [glo, ghi], "verdict": verdict}
        print("  %-40s %.3f (%.3f-%.3f)   %.3f (%.3f-%.3f)   %+.3f (%+.3f,%+.3f) %s"
              % (lbl, a_fh[0], a_fh[1], a_fh[2], a_nf[0], a_nf[1], a_nf[2], g, glo, ghi, verdict))

    print("\n  HOW MUCH DID THE INVENTED FORMULA MATTER?")
    for base in ("Montreal", "FH-RS"):
        inv = next(v for k, v in res["scores"].items() if k.startswith(base) and "INVENTED" in k)
        pub = next(v for k, v in res["scores"].items() if k.startswith(base) and "PUBLISHED" in k)
        print("    %-10s AUC in FH      invented %.3f -> published %.3f  (%+.3f)"
              % (base, inv["auc_fh"], pub["auc_fh"], pub["auc_fh"] - inv["auc_fh"]))
        print("    %-10s AUC in non-FH  invented %.3f -> published %.3f  (%+.3f)"
              % ("", inv["auc_nonfh"], pub["auc_nonfh"], pub["auc_nonfh"] - inv["auc_nonfh"]))
        print("    %-10s conclusion     invented '%s' -> published '%s'  => %s"
              % ("", inv["verdict"], pub["verdict"],
                 "UNCHANGED" if inv["verdict"] == pub["verdict"] else "CHANGED"))

    survives = all(res["scores"][k]["verdict"] == "no difference"
                   for k in res["scores"] if "PUBLISHED" in k)
    res["original_conclusion"] = ("Published FH scores discriminate about as well in matched "
                                 "non-carriers as in FH carriers, so the FH-specific element is "
                                 "the baseline level rather than the risk-factor slopes.")
    res["conclusion_survives_with_published_equations"] = bool(survives)
    print("\n  ORIGINAL CONCLUSION: %s" % res["original_conclusion"])
    print("  WITH PUBLISHED EQUATIONS: %s"
          % ("SURVIVES" if survives else "DOES NOT SURVIVE - at least one score differs by genotype"))
    (OUT / "R3_comparator_recheck.json").write_text(json.dumps(res, indent=2))
    print("\nwritten:", OUT / "R3_comparator_recheck.json")


if __name__ == "__main__":
    main()
