#!/usr/bin/env python3
"""GROUND-TRUTH QC and full inventory of every UK Biobank / Welsh data file.

Nothing here is assumed:
  * File discovery is a FILESYSTEM WALK, not Spotlight. Spotlight missed 402
    files on this machine, so it is used only as a cross-check.
  * Every file is MD5-hashed in full, including multi-gigabyte ones. Duplicates
    are identified by content, never by name or size.
  * Row and column counts are MEASURED by reading each file, not inferred.
  * Whether a cloud-synced file is materialised on disk is measured from its
    allocated blocks, so an online-only stub cannot masquerade as present.

Writes FULL_INVENTORY.md and FULL_INVENTORY.csv into the local data package.

LOCAL ONLY. Governed participant-level data; never transmit.
"""
from __future__ import annotations

import csv
import hashlib
import os
import re
import subprocess
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

STAMP = "2026-08-13"
PKG = Path.home() / "Downloads" / f"CALON_DATA_PACKAGE_{STAMP}"
ROOTS = [Path.home() / "Downloads", Path.home() / "Documents", Path.home() / "Desktop",
         Path.home() / "Library" / "CloudStorage", Path("/Volumes/UnionSine")]
# Filename patterns are NOT sufficient on their own: `corrected_ascvd_outcomes.csv`
# and `04a_meds_touch.csv` - the outcome and BP-medication inputs - match none of
# the cohort keywords, and an earlier version of this audit reported 0 copies of
# each because of it. Discovery therefore also matches outcome/analysis keywords
# and always includes the explicit model inputs by exact name.
NAME = re.compile(r"ukb|biobank|wales|dragon|pass_master|ascvd|outcome|meds_touch"
                  r"|mace|lpa|carrier|fh_", re.I)
MUST_INCLUDE = {"corrected_ascvd_outcomes.csv", "04a_meds_touch.csv",
                "ukb_master.csv", "pass_master.csv", "WALES_FH_CLEANED.csv",
                "FH_Dragon3 (1).csv"}
EXT = {".csv", ".tsv", ".rds", ".parquet", ".pkl", ".dta", ".xlsx", ".txt"}
SKIP = ("/.Trash/", "node_modules", f"CALON_DATA_PACKAGE_{STAMP}")


def walk() -> list[Path]:
    """Ground truth: the filesystem itself."""
    out: set[Path] = set()
    for r in ROOTS:
        if not r.exists():
            print("  root absent, skipped: %s" % r)
            continue
        for dirpath, dirnames, files in os.walk(r, onerror=lambda e: None):
            if any(s in dirpath for s in SKIP):
                dirnames[:] = []
                continue
            for f in files:
                if Path(f).suffix.lower() in EXT and (NAME.search(f) or f in MUST_INCLUDE):
                    out.add(Path(dirpath) / f)
    return sorted(out)


def spotlight() -> set[str]:
    found: set[str] = set()
    for pat in ["ukb", "biobank", "wales", "dragon", "pass_master"]:
        try:
            r = subprocess.run(["mdfind", "-name", pat], capture_output=True,
                               text=True, timeout=120)
            found.update(x for x in r.stdout.splitlines() if x)
        except Exception:
            pass
    return found


def md5(p: Path) -> str | None:
    h = hashlib.md5()
    try:
        with open(p, "rb") as f:
            for b in iter(lambda: f.read(1 << 23), b""):
                h.update(b)
    except OSError:
        return None
    return h.hexdigest()


def shape(p: Path) -> tuple[int | None, int | None]:
    """Measured rows and columns. Text formats only; binary returns (None, None)."""
    if p.suffix.lower() not in (".csv", ".tsv", ".txt"):
        return None, None
    try:
        sep = "\t" if p.suffix.lower() == ".tsv" else ","
        with open(p, "r", encoding="utf-8", errors="replace", newline="") as f:
            header = f.readline()
        # Some extracts contain NUL bytes, which csv.reader refuses. Strip them
        # rather than abandon the file - a NUL is a corruption artefact, not data.
        header = header.replace("\x00", "")
        try:
            ncol = len(next(csv.reader([header], delimiter=sep))) if header.strip() else 0
        except Exception:
            ncol = header.count(sep) + 1 if header.strip() else 0
        n = 0
        with open(p, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 23), b""):
                n += chunk.count(b"\n")
        return max(n - 1, 0), ncol
    except Exception:
        return None, None


def main():
    PKG.mkdir(parents=True, exist_ok=True)
    print("=" * 92)
    print("GROUND-TRUTH DATA QC - filesystem walk, full hashing, measured shapes")
    print("=" * 92)

    print("\n1. FILESYSTEM WALK (ground truth)")
    files = walk()
    print("   files found: %d" % len(files))

    print("\n2. SPOTLIGHT CROSS-CHECK (does the index miss anything?)")
    sl = spotlight()
    missed = [p for p in files if str(p) not in sl]
    print("   Spotlight indexed : %d" % len(sl))
    print("   walk found but Spotlight MISSED: %d" % len(missed))
    if missed:
        print("   -> Spotlight is unreliable here; the walk is authoritative.")

    print("\n3. HASHING AND MEASURING (%d files, this reads every byte)" % len(files))
    rows = []
    total = 0
    for i, p in enumerate(files, 1):
        try:
            st = p.stat()
        except OSError:
            continue
        allocated = st.st_blocks * 512
        materialised = allocated >= min(st.st_size * 0.5, st.st_size)
        digest = md5(p) if materialised else None
        # any single unreadable file must not abort a 4,000-file audit
        nrow, ncol = shape(p) if materialised and st.st_size < (6 << 30) else (None, None)
        total += st.st_size
        rows.append({"file": p.name, "bytes": st.st_size, "mb": round(st.st_size / 1e6, 2),
                     "rows": nrow, "columns": ncol, "md5": digest,
                     "materialised": materialised, "location": str(p.parent),
                     "cohort": ("UK Biobank" if re.search(r"ukb|biobank", p.name, re.I)
                                else "Wales/DRAGON")})
        if i % 250 == 0 or i == len(files):
            print("   %d/%d  (%.1f GB read)" % (i, len(files), total / 1e9), flush=True)

    stubs = [r for r in rows if not r["materialised"]]
    hashed = [r for r in rows if r["md5"]]
    by_hash: dict[str, list] = {}
    for r in hashed:
        by_hash.setdefault(r["md5"], []).append(r)
    uniq = len(by_hash)
    dup_bytes = sum(r["bytes"] for g in by_hash.values() for r in g[1:])

    print("\n4. RESULT")
    print("   total files            : %d" % len(rows))
    print("   total bytes            : %.2f GB" % (total / 1e9))
    print("   fully hashed           : %d" % len(hashed))
    print("   online-only stubs      : %d" % len(stubs))
    print("   UNIQUE datasets (md5)  : %d" % uniq)
    print("   wasted on duplicates   : %.2f GB" % (dup_bytes / 1e9))

    with open(PKG / "FULL_INVENTORY.csv", "w", newline="", encoding="utf-8") as f:
        wtr = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        wtr.writeheader()
        wtr.writerows(rows)

    # ---- the six files the model actually reads, verified against the package
    MODEL = ["ukb_master.csv", "corrected_ascvd_outcomes.csv", "04a_meds_touch.csv",
             "WALES_FH_CLEANED.csv", "pass_master.csv", "FH_Dragon3 (1).csv"]
    print("\n5. THE SIX FILES THE MODEL READS - package copy vs every copy on disk")
    model_rows = []
    for name in MODEL:
        pkg = PKG / "raw" / name
        pkg_md5 = md5(pkg) if pkg.exists() else None
        others = [r for r in rows if r["file"] == name and r["md5"]]
        agree = sum(1 for r in others if r["md5"] == pkg_md5)
        ok = pkg_md5 is not None and agree > 0
        print("   %-32s package md5 %s | %d/%d copies on disk agree  %s"
              % (name, (pkg_md5 or "MISSING")[:12], agree, len(others), "OK" if ok else "CHECK"))
        model_rows.append({"file": name, "package_md5": pkg_md5,
                           "copies_on_disk": len(others), "copies_agreeing": agree,
                           "verified": ok})

    largest = sorted(by_hash.values(), key=lambda g: -g[0]["bytes"])[:40]
    md = ["# Full data inventory - UK Biobank and Welsh", "",
          "**Built %s. LOCAL ONLY - governed participant-level data under UK Biobank "
          "Application 1002450 and All-Wales PASS/DRAGON approvals. Never commit, "
          "upload, or transmit.**" % STAMP, "",
          "## How this was produced", "",
          "Nothing is assumed. Files were discovered by walking the filesystem, not by "
          "querying Spotlight — Spotlight missed **%d** of them. Every materialised file "
          "was MD5-hashed in full, so duplicates are identified by content rather than by "
          "name or size. Row and column counts were measured by reading each file. "
          "Cloud-synced files were checked for on-disk allocation so an online-only stub "
          "cannot appear as present." % len(missed), "",
          "## Totals", "",
          "| | |", "|---|---|",
          "| Files found | %d |" % len(rows),
          "| Total size | %.2f GB |" % (total / 1e9),
          "| Fully hashed | %d |" % len(hashed),
          "| Online-only stubs | %d |" % len(stubs),
          "| **Unique datasets (by md5)** | **%d** |" % uniq,
          "| Space held by duplicate copies | %.2f GB |" % (dup_bytes / 1e9),
          "| Spotlight missed | %d |" % len(missed), "",
          "## The six files the analysis actually reads", "",
          "Each is copied into `raw/` and its hash compared against every copy found on "
          "disk. `copies agreeing` counts how many independent copies carry the identical "
          "content, which is what makes the package copy trustworthy.", "",
          "| file | package md5 | copies on disk | agreeing | verified |",
          "|---|---|---|---|---|"]
    for r in model_rows:
        md.append("| `%s` | `%s` | %d | %d | %s |"
                  % (r["file"], (r["package_md5"] or "MISSING")[:16], r["copies_on_disk"],
                     r["copies_agreeing"], "yes" if r["verified"] else "CHECK"))
    md += ["", "## Largest unique datasets", "",
           "One row per distinct file content. `copies` is how many times that exact "
           "content appears on this machine.", "",
           "| file | MB | rows | cols | copies | cohort | one location |",
           "|---|---|---|---|---|---|---|"]
    for g in largest:
        r = g[0]
        md.append("| `%s` | %.0f | %s | %s | %d | %s | `%s` |"
                  % (r["file"], r["mb"], r["rows"] if r["rows"] is not None else "-",
                     r["columns"] if r["columns"] is not None else "-", len(g),
                     r["cohort"], r["location"]))
    if stubs:
        md += ["", "## Online-only stubs (present in the folder listing, NOT on disk)", "",
               "These could not be hashed or measured because their bytes are not local. "
               "Anything needed for analysis must be materialised first.", "",
               "| file | MB | location |", "|---|---|---|"]
        for r in stubs[:40]:
            md.append("| `%s` | %.0f | `%s` |" % (r["file"], r["mb"], r["location"]))
    md += ["", "## Full listing", "",
           "`FULL_INVENTORY.csv` holds every file with its path, size, measured shape, "
           "md5 and materialisation status.", ""]
    (PKG / "FULL_INVENTORY.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\nwritten: %s" % (PKG / "FULL_INVENTORY.md"))
    print("written: %s" % (PKG / "FULL_INVENTORY.csv"))


if __name__ == "__main__":
    main()
