#!/usr/bin/env python3
"""Classify Markdown evidence by declared status without modifying source files."""
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent / "document_inventory.csv"


def classify(text: str, path: Path) -> tuple[str, str]:
    lower = text.lower()
    if "contains retracted results" in lower or "retracted" in lower and path.parts[-2:-1] == ("manuscript",):
        return "RETRACTED_OR_HISTORICAL", "Explicit retraction marker or manuscript archive"
    if path.name == "STATUS.md":
        return "STATUS_AUTHORITY", "Repository declares this current-state register"
    if path.name in {"METHODS_CALON_C.md", "RESULTS_SUMMARY_2026-08-16.md", "PRESPEC_HORIZON.md"}:
        return "CALON_C_CURRENT_CANDIDATE", "Live CALON-C methods/result artefact"
    if "supersedes step-007" in lower or "verify calon-c" in lower:
        return "CALON_C_REVIEW_BRIEF", "Latest adversarial verification brief"
    if "calon-h" in lower or "calon-g" in lower or "cycle-2" in lower:
        return "HISTORICAL_OR_PROTOCOL", "Earlier/research-cycle material"
    return "CONTEXT_OR_UNCLASSIFIED", "Requires claim-level review"


def main() -> None:
    rows = []
    for path in sorted(ROOT.rglob("*.md")):
        if "audit_panel_20260816" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        status, rationale = classify(text, path)
        rows.append(
            {
                "path": str(path.relative_to(ROOT)),
                "status": status,
                "rationale": rationale,
                "mentions_calon_c": "CALON-C" in text,
                "mentions_calon_f": "CALON-F" in text,
                "mentions_retraction": "retract" in text.lower(),
                "numeric_claim_tokens": sum(character.isdigit() for character in text),
            }
        )
    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"Inventoried {len(rows)} Markdown files: {OUT}")


if __name__ == "__main__":
    main()
