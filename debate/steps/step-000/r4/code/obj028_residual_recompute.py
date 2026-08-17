#!/usr/bin/env python3
"""OBJ-028 local settlement: residual = delta - (c_index - comparator_c).

Reads only outputs/calon_final.json. Writes no participant data.
"""
from __future__ import annotations

import json
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
SRC = ROOT / "outputs" / "calon_final.json"
OUT = Path(__file__).with_name("obj028_residuals.tsv")


def main() -> None:
    d = json.loads(SRC.read_text())
    rows = []
    for cohort in ("ukb", "wales"):
        for sg, block in d[cohort]["subgroups"].items():
            c = float(block["c_index"])
            for comp, cell in block["vs"].items():
                delta = float(cell["delta"])
                cc = float(cell["comparator_c"])
                residual = delta - (c - cc)
                rows.append(
                    {
                        "cohort": cohort,
                        "subgroup": sg,
                        "comparator": comp,
                        "n": block["n"],
                        "events": block["events"],
                        "c_index": c,
                        "delta": delta,
                        "comparator_c": cc,
                        "c_minus_cc": c - cc,
                        "residual": residual,
                        "verdict": cell["verdict"],
                        "lo": float(cell["ci"][0]),
                        "hi": float(cell["ci"][1]),
                    }
                )

    n = len(rows)
    residuals = [r["residual"] for r in rows]
    abs_r = [abs(x) for x in residuals]
    nonzero = sum(x != 0.0 for x in residuals)

    by_sg: dict[tuple[str, str], list[float]] = {}
    for r in rows:
        by_sg.setdefault((r["cohort"], r["subgroup"]), []).append(r["residual"])
    n_sg = len(by_sg)
    n_differ = 0
    sg_res = []
    for vals in by_sg.values():
        if any(abs(v - vals[0]) > 1e-12 for v in vals):
            n_differ += 1
        sg_res.append(vals[0])
    n_pos = sum(x > 0 for x in sg_res)
    n_neg = sum(x < 0 for x in sg_res)

    # Hypothetical: shift stored delta/CI by -residual (mean-C identity).
    n_flip = 0
    flips = []
    for r in rows:
        new_lo = r["lo"] - r["residual"]
        new_hi = r["hi"] - r["residual"]
        new_v = "WIN" if new_lo > 0 else ("LOSS" if new_hi < 0 else "tie")
        if new_v != r["verdict"]:
            n_flip += 1
            flips.append((r, new_v))

    lines = [
        "cohort\tsubgroup\tcomparator\tn\tevents\tc_index\tdelta\tcomparator_c\tc_minus_cc\tresidual\tverdict"
    ]
    for r in rows:
        lines.append(
            "\t".join(
                [
                    r["cohort"],
                    r["subgroup"],
                    r["comparator"],
                    str(r["n"]),
                    str(r["events"]),
                    f"{r['c_index']:.16f}",
                    f"{r['delta']:.16f}",
                    f"{r['comparator_c']:.16f}",
                    f"{r['c_minus_cc']:.16f}",
                    f"{r['residual']:.16e}",
                    r["verdict"],
                ]
            )
        )
    OUT.write_text("\n".join(lines) + "\n")

    print(f"source={SRC}")
    print(f"n_cells={n}")
    print(f"n_nonzero={nonzero}")
    print(f"signed_min={min(residuals):.16e}")
    print(f"signed_median_69={statistics.median(residuals):.16e}")
    print(f"signed_max={max(residuals):.16e}")
    print(f"signed_mean_69={statistics.mean(residuals):.16e}")
    print(f"abs_min={min(abs_r):.16e}")
    print(f"abs_median_23={statistics.median([abs(x) for x in sg_res]):.16e}")
    print(f"abs_max={max(abs_r):.16e}")
    print(f"n_subgroups={n_sg}")
    print(f"n_subgroups_residual_differ_gt_1e-12={n_differ}")
    print(f"n_subgroups_residual_positive={n_pos}")
    print(f"n_subgroups_residual_negative={n_neg}")
    print(f"mean_of_23_subgroup_residuals={statistics.mean(sg_res):.16e}")
    print(f"hypothetical_additive_ci_flips={n_flip}")
    print("ukb_ALL_implied_c_index_minus_delta:")
    for r in rows:
        if r["cohort"] == "ukb" and r["subgroup"] == "ALL":
            print(
                f"  {r['comparator']} stored_cc={r['comparator_c']:.16f} "
                f"implied={r['c_index']-r['delta']:.16f} residual={r['residual']:.16e}"
            )
    print(f"written={OUT}")


if __name__ == "__main__":
    main()
