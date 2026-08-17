#!/usr/bin/env python3
"""Cursor Kimi/Grok/Claude: each model runs a four-seat CALON-C panel, then cross-model debate and teaching synthesis."""
from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "review_panel/CALON_C_REVIEW_PROTOCOL.md"
MANUSCRIPT = ROOT / "outputs/manuscript_2026-08-16/CALON_C_MANUSCRIPT_HIGH_CALIBRE.md"
OUT = ROOT / "outputs/manuscript_2026-08-16/multi_agent_review_2026-08-17/cursor-three-model-four-seat"
MODELS = {
    "kimi": "kimi-k3-max",
    "grok": "cursor-grok-4.6-xhigh",
    "claude": "claude-opus-5-thinking-max",
}
FOUR_SEATS = """Inside your model, convene four named specialist subagents and keep their reasoning distinct:

1. **Biostatistician** — design, estimand, effective sample size, methods, uncertainty, calibration, competing risks, multiplicity, missing data, clustering, validation and reporting.
2. **Cardiologist** — clinical population, endpoint adjudication, event relevance, competing mortality, treatment decisions, clinical utility, patient safety and guideline translation.
3. **Lipid-medicine specialist** — LDLR/FH phenotype, cumulative exposure, lipid measurement, treatment correction, pharmacology, Lp(a), apoB, remnant biology, ascertainment and lipid-guideline alignment.
4. **Senior Editor-in-Chief** — novelty, priority claims, evidential hierarchy, citation fidelity, prose precision, reporting completeness, reproducibility, journal fit and rejection risk.

For every substantive manuscript paragraph, report each seat's independent judgement before the Editor-in-Chief adjudicates. Surface disagreements; do not manufacture consensus. End with an internal-panel debate and a teaching section for Dr Genedy explaining the methodological lesson behind each major criticism."""


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def cursor_call(name: str, model: str, prompt: str, timeout: int = 3600) -> tuple[str, dict]:
    cmd = [
        "cursor-agent", "-p", "--mode", "ask", "--trust",
        "--model", model, prompt,
    ]
    started = now()
    run = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, timeout=timeout)
    text = run.stdout.strip()
    meta = {
        "name": name, "model": model, "started": started, "finished": now(),
        "exit_code": run.returncode, "response_chars": len(text),
        "stderr": run.stderr[-4000:] if run.stderr else "",
    }
    if run.returncode != 0 or len(text) < 1000:
        raise RuntimeError(f"{name}/{model} failed: exit={run.returncode}; chars={len(text)}; {run.stderr[-500:]}")
    return text, meta


def run_parallel(stage: str, prompts: dict[str, str]) -> dict[str, str]:
    folder = OUT / stage
    folder.mkdir(parents=True, exist_ok=True)
    outputs: dict[str, str] = {}
    records = []
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {pool.submit(cursor_call, name, MODELS[name], prompt): name for name, prompt in prompts.items()}
        for future in as_completed(futures):
            name = futures[future]
            try:
                text, meta = future.result()
                outputs[name] = text
                records.append({**meta, "ok": True})
                (folder / f"{name}.md").write_text(text + "\n", encoding="utf-8")
                (folder / f"{name}.result.json").write_text(json.dumps({**meta, "ok": True}, indent=2), encoding="utf-8")
                print(f"OK {stage}/{name}: {len(text)} characters", flush=True)
            except Exception as exc:
                record = {"name": name, "model": MODELS[name], "ok": False, "error": str(exc), "finished": now()}
                records.append(record)
                (folder / f"{name}.result.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
                print(f"FAIL {stage}/{name}: {exc}", flush=True)
    (folder / "results.json").write_text(json.dumps(records, indent=2), encoding="utf-8")
    if len(outputs) != len(prompts):
        raise RuntimeError(f"{stage} incomplete: {len(outputs)}/{len(prompts)} models returned")
    return outputs


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    protocol = PROTOCOL.read_text(encoding="utf-8")
    manifest = {
        "created": now(),
        "provider": "Cursor subscription; cursor-agent authenticated account",
        "models": MODELS,
        "panel_inside_each_model": ["Biostatistician", "Cardiologist", "Lipid-medicine specialist", "Senior Editor-in-Chief"],
        "round_1": "three models blind; each contains four specialist seats",
        "round_2": "three models see all round-1 reports and debate named positions",
        "final": "Claude Cursor model produces teaching synthesis from the debate record",
        "evidence_window": ["2016-08-17", "2026-08-17"],
        "manuscript": str(MANUSCRIPT.relative_to(ROOT)),
        "participant_data": "prohibited; manuscript and aggregate artefacts only",
        "research_integrations": "agents must report USED/FAILED/NOT CONFIGURED for /academic, Scite, SciSpace and Elicit",
    }
    (OUT / "RUN_MANIFEST.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    base = f"""{FOUR_SEATS}\n\nBLIND ROUND 1: do not inspect another model's outputs. Read the complete manuscript at `{MANUSCRIPT.relative_to(ROOT)}` and follow this protocol exactly:\n\n{protocol}"""
    round1 = run_parallel("round-1-independent", {name: f"You are the {name.upper()} model.\n\n{base}" for name in MODELS})

    dossier_path = OUT / "ROUND_1_DOSSIER.md"
    dossier_path.write_text("\n\n".join(f"# {name.upper()} ROUND-1 REPORT\n\n{text}" for name, text in round1.items()), encoding="utf-8")
    debate = f"""{FOUR_SEATS}\n\nCROSS-MODEL DEBATE ROUND. Read `{dossier_path.relative_to(ROOT)}` containing the complete blind reports from Kimi, Grok and Claude. Your four internal specialists must challenge named claims from all three model reports. Identify agreements, contradictions, citation conflicts, and whether each conflict is methodological, population-driven, endpoint/estimand-driven, implementation/calibration-driven, or substantive. Resolve only what the manuscript or verified 10-year literature permits. Preserve named dissent otherwise. End with: consensus; unresolved disputes; required manuscript actions; and a plain-language lesson for Dr Genedy."""
    round2 = run_parallel("round-2-cross-model-debate", {name: f"You are the {name.upper()} model.\n\n{debate}" for name in MODELS})

    debate_path = OUT / "ROUND_2_DOSSIER.md"
    debate_path.write_text("\n\n".join(f"# {name.upper()} DEBATE RESPONSE\n\n{text}" for name, text in round2.items()), encoding="utf-8")
    final_prompt = f"""You are the final teaching chair, operating through Claude but bound to report all named Kimi, Grok and Claude dissent fairly. Read `{dossier_path.relative_to(ROOT)}` and `{debate_path.relative_to(ROOT)}`. Produce a definitive teaching synthesis for Dr Nader Genedy:

1. Single most likely rejection reason.
2. Consensus matrix across all three models and four specialist seats.
3. Named unresolved dissent and why it remains unresolved.
4. Ranked repair plan: analyses to rerun; claims to delete/weaken; prose-only repairs.
5. Paragraph-level replacement wording for the most serious passages.
6. Teach in plain language: transport versus external validation; discrimination versus calibration/utility; causal LDL biology versus within-FH prediction; endpoint harmonisation; competing risks; and why a TIE is not equivalence.
7. One-week critical path and submission verdict: NO-GO, CONDITIONAL GO or GO.

Do not introduce literature outside 17 August 2016–17 August 2026 or citations not verified in the reports. Mark unresolved citations unverified."""
    final_text, final_meta = cursor_call("teaching_chair", MODELS["claude"], final_prompt)
    final_folder = OUT / "final"
    final_folder.mkdir(exist_ok=True)
    (final_folder / "TEACHING_SYNTHESIS.md").write_text(final_text + "\n", encoding="utf-8")
    (final_folder / "TEACHING_SYNTHESIS.result.json").write_text(json.dumps(final_meta, indent=2), encoding="utf-8")
    print(f"COMPLETE: {OUT}", flush=True)


if __name__ == "__main__":
    main()
