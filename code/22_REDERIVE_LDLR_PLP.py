#!/usr/bin/env python3
"""Re-derive the UK Biobank LDLR carrier set against ClinVar pathogenicity.

WHY THIS EXISTS
An independent audit established that `ldlr_carrier` in ukb_master.csv does not
identify familial hypercholesterolaemia. Measured: untreated LDL-C excess of only
+0.55 mmol/L over non-carriers, 91.1% of "carriers" below 6.5 mmol/L, and
`variant_id` empty for all 501,936 rows so pathogenicity cannot be checked by
anyone. Genotype-confirmed HeFH should carry an untreated excess of roughly
+3 to +4 mmol/L. Every FH claim in the UK Biobank arm rests on this flag.

WHAT THIS DOES
Rebuilds the carrier definition from variant-level evidence held locally, so
nothing is transmitted:
    ukb_fh_all_carriers.tsv       CHROM/POS/REF/ALT/EID/GT/GENE  (the calls)
    ukb_ldlr_vep_annotations.csv  consequence, impact, protein position
    clinvar_ldlr_full.csv         clinical_significance, review_status

THE OFFSET TRAP
LDLR is numbered two ways: the full precursor including the 21-residue signal
peptide, and the mature protein without it. UKB VEP protein positions and
ClinVar entries can therefore differ by exactly 21. This programme has hit that
before. The script tests offsets -21, 0 and +21 and reports the match rate for
each rather than assuming one, because a silently wrong offset produces a
plausible-looking but meaningless classification.

THE TEST THAT MATTERS
A correct pathogenic set must show the FH phenotype. The script reports untreated
LDL-C in each classification tier. If P/LP carriers do not separate sharply from
non-carriers, the derivation is still wrong and must not be used.

Governance: aggregate output only. No participant rows, identifiers or variant
coordinates are printed. Local files only; nothing is sent anywhere.
"""
from __future__ import annotations

import os
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

BASE = Path.home() / "Downloads" / "CALON_MODEL_PACKAGE" / "raw_data"
PKG = Path.home() / "Downloads" / "CALON_DATA_PACKAGE_2026-08-13"
CALLS = BASE / "ukb_fh_all_carriers.tsv"
VEP = BASE / "ukb_ldlr_vep_annotations.csv"
CLINVAR = BASE / "clinvar_ldlr_full.csv"
MASTER = PKG / "raw" / "ukb_master.csv"

PATHOGENIC = ("pathogenic", "likely pathogenic")
BENIGN = ("benign", "likely benign")
LOF = ("frameshift", "stop_gained", "splice_acceptor", "splice_donor",
       "start_lost", "stop_lost", "transcript_ablation")


def clinvar_tier(sig: str) -> str:
    s = str(sig).lower()
    if "conflicting" in s:
        return "conflicting"
    if any(p in s for p in PATHOGENIC) and "benign" not in s:
        return "P/LP"
    if any(b in s for b in BENIGN) and "pathogenic" not in s:
        return "B/LB"
    if "uncertain" in s or "vus" in s:
        return "VUS"
    return "other"


def main():
    print("=" * 96)
    print("RE-DERIVING THE LDLR CARRIER SET AGAINST CLINVAR")
    print("=" * 96)

    vep = pd.read_csv(VEP)
    cv = pd.read_csv(CLINVAR)
    print("\nINPUTS")
    print("  UKB LDLR variants (VEP)      : %d" % len(vep))
    print("  ClinVar LDLR entries         : %d" % len(cv))

    cv["tier"] = cv["clinical_significance"].map(clinvar_tier)
    print("\n  ClinVar tiers: %s" % dict(cv["tier"].value_counts()))

    # ---- protein-position join, testing the signal-peptide offset -----------
    vep["prot_pos"] = pd.to_numeric(vep["protein_position"], errors="coerce")
    aa = vep["amino_acids"].astype(str).str.split("/", expand=True)
    vep["wt"] = aa[0].str.strip()
    vep["mut"] = aa[1].str.strip() if aa.shape[1] > 1 else np.nan
    cv["pos_n"] = pd.to_numeric(cv["position"], errors="coerce")

    print("\nSIGNAL-PEPTIDE OFFSET TEST (LDLR precursor vs mature numbering)")
    best, best_n = 0, -1
    for off in (-21, 0, 21):
        k_v = vep["prot_pos"] + off
        merged = pd.merge(
            pd.DataFrame({"p": k_v, "wt": vep["wt"], "mut": vep["mut"]}).dropna(subset=["p"]),
            cv[["pos_n", "wt_aa", "mut_aa"]].dropna(subset=["pos_n"]),
            left_on=["p", "wt", "mut"], right_on=["pos_n", "wt_aa", "mut_aa"], how="inner")
        n = len(merged.drop_duplicates())
        print("  offset %+3d : %4d variants match ClinVar on position AND both amino acids" % (off, n))
        if n > best_n:
            best, best_n = off, n
    print("  -> using offset %+d (%d matches). A wrong offset would classify by "
          "coincidence." % (best, best_n))

    vep["cv_pos"] = vep["prot_pos"] + best
    m = vep.merge(cv[["pos_n", "wt_aa", "mut_aa", "tier", "review_status"]],
                  left_on=["cv_pos", "wt", "mut"],
                  right_on=["pos_n", "wt_aa", "mut_aa"], how="left")
    m["consequence"] = m["consequence"].astype(str)
    m["is_lof"] = m["consequence"].str.contains("|".join(LOF), case=False, na=False)
    m["tier"] = m["tier"].fillna("unclassified")
    # A high-confidence LoF with no ClinVar entry is still mechanistically P/LP
    m["final"] = np.where(m["tier"].eq("P/LP"), "P/LP",
                  np.where(m["is_lof"] & m["tier"].isin(["unclassified", "VUS"]), "LoF (no ClinVar P/LP)",
                  m["tier"]))

    print("\nVARIANT CLASSIFICATION (%d UKB LDLR variants)" % len(m))
    for k, v in m["final"].value_counts().items():
        car = m.loc[m["final"].eq(k), "n_carriers"].sum()
        print("  %-26s %4d variants   %6d carrier calls" % (k, v, car))

    # ---- carrier sets --------------------------------------------------------
    calls = pd.read_csv(CALLS, sep="\t", usecols=["CHROM", "POS", "REF", "ALT", "EID", "GENE"],
                        low_memory=False)
    calls = calls.loc[calls["GENE"].astype(str).str.upper().eq("LDLR")]
    key = ["chrom", "pos", "ref", "alt"]
    m2 = m.rename(columns={"chrom": "chrom", "pos": "pos", "ref": "ref", "alt": "alt"})
    calls = calls.rename(columns={"CHROM": "chrom", "POS": "pos", "REF": "ref", "ALT": "alt"})
    for c in ("chrom",):
        calls[c] = calls[c].astype(str).str.replace("chr", "", regex=False)
        m2[c] = m2[c].astype(str).str.replace("chr", "", regex=False)
    calls["pos"] = pd.to_numeric(calls["pos"], errors="coerce")
    m2["pos"] = pd.to_numeric(m2["pos"], errors="coerce")
    j = calls.merge(m2[key + ["final"]], on=key, how="left")
    j["final"] = j["final"].fillna("unmatched")

    sets = {
        "P/LP only": j.loc[j["final"].eq("P/LP"), "EID"].unique(),
        "P/LP or high-confidence LoF": j.loc[j["final"].isin(
            ["P/LP", "LoF (no ClinVar P/LP)"]), "EID"].unique(),
        "any LDLR variant call (current flag)": j["EID"].unique(),
    }

    # ---- the phenotype test --------------------------------------------------
    md = pd.read_csv(MASTER, usecols=["eid", "ldlr_carrier", "ldl_chem", "on_statin_self"],
                     low_memory=False)
    ldl = pd.to_numeric(md["ldl_chem"], errors="coerce")
    tx = pd.to_numeric(md["on_statin_self"], errors="coerce").fillna(0).gt(0)
    md["untreated_ldl"] = np.where(tx, ldl / 0.70, ldl)
    flag = pd.to_numeric(md["ldlr_carrier"], errors="coerce").eq(1)
    base = md.loc[~flag, "untreated_ldl"]

    print("\nPHENOTYPE TEST - does each definition look like FH?")
    print("  reference: non-carriers by the CURRENT flag, untreated LDL-C %.2f mmol/L" % base.mean())
    print("\n  %-38s %7s %9s %9s %9s" % ("definition", "n", "LDL-C", "excess", ">=6.5"))
    rows = []
    for name, eids in sets.items():
        s = md.loc[md["eid"].isin(set(eids)), "untreated_ldl"]
        if len(s) == 0:
            print("  %-38s %7s" % (name, "0"))
            continue
        print("  %-38s %7d %9.2f %+9.2f %8.1f%%"
              % (name, len(s), s.mean(), s.mean() - base.mean(), 100 * s.ge(6.5).mean()))
        rows.append({"definition": name, "n": len(s), "untreated_ldl": s.mean(),
                     "excess": s.mean() - base.mean(), "pct_ge_6_5": 100 * s.ge(6.5).mean()})
    print("  %-38s %7d %9.2f %+9.2f %8.1f%%"
          % ("current ldlr_carrier flag", flag.sum(),
             md.loc[flag, "untreated_ldl"].mean(),
             md.loc[flag, "untreated_ldl"].mean() - base.mean(),
             100 * md.loc[flag, "untreated_ldl"].ge(6.5).mean()))

    print("\nINTERPRETATION")
    print("  Genotype-confirmed HeFH should show an untreated LDL-C excess of roughly")
    print("  +3 to +4 mmol/L. A definition that does not separate from non-carriers is")
    print("  not identifying FH, however it is labelled.")
    pd.DataFrame(rows).to_csv(PKG / "LDLR_REDERIVATION.csv", index=False)
    print("\nwritten: %s" % (PKG / "LDLR_REDERIVATION.csv"))


if __name__ == "__main__":
    main()
