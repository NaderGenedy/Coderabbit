#!/usr/bin/env python3
"""Four-seat Gemini 3.6 Flash (HIGH thinking) CALON-C review, debate and teaching synthesis.

Uses the existing GEMINI_API_KEY/GOOGLE_API_KEY in ~/.hermes/.env. The key is never
printed or written. Only the aggregate manuscript and review text are sent.
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "outputs/manuscript_2026-08-16/CALON_C_MANUSCRIPT_HIGH_CALIBRE.md"
PROTOCOL = ROOT / "review_panel/CALON_C_REVIEW_PROTOCOL.md"
OUT = ROOT / "outputs/manuscript_2026-08-16/multi_agent_review_2026-08-17/google-gemini-3.6-flash-high"
MODEL = "gemini-3.6-flash"
API_ROOT = "https://generativelanguage.googleapis.com/v1beta/models"

ROLES = {
    "biostatistician": """You are the BIOSTATISTICIAN. Audit design, estimands, effective sample size, event counts, Cox/ridge specification, internal validation and optimism, discrimination, calibration, competing risk, comparator fairness, paired uncertainty, multiplicity, missing data, family clustering, predictor timing, transport versus independent external validation, PROBAST and TRIPOD+AI. Statistical claims must be earned by the design and uncertainty.""",
    "cardiologist": """You are the CARDIOLOGIST. Audit clinical population, endpoint content and adjudication, first-event relevance, competing mortality, horizons, treatment-escalation implications, patient selection, calibration for decisions, decision curves, harms of de-risking FH, guideline translation, clinical workflow and the evidential threshold for adoption.""",
    "lipid_medicine": """You are the LIPID-MEDICINE SPECIALIST. Audit LDLR/FH phenotype definition, cumulative atherogenic exposure, non-HDL-C and remnant biology, lipid measurement, treatment correction, statin and non-statin pharmacology, Lp(a), apoB, guideline alignment, mechanistic plausibility, ascertainment route and whether lipid claims exceed the data.""",
    "senior_editor_in_chief": """You are the SENIOR EDITOR-IN-CHIEF of a leading cardiovascular journal. Audit novelty, priority claims, narrative structure, evidential hierarchy, citation fidelity, reporting completeness, reproducibility, generalisability, title/abstract accuracy, journal fit and rejection risk. Require precise replacement wording and distinguish fatal issues from repairable weaknesses.""",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_key() -> str:
    for name in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
        if os.getenv(name):
            return os.environ[name]
    env_path = Path.home() / ".hermes/.env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            if "=" not in line or line.lstrip().startswith("#"):
                continue
            key, value = line.split("=", 1)
            if key.strip() in ("GEMINI_API_KEY", "GOOGLE_API_KEY") and value.strip():
                return value.strip().strip('"').strip("'")
    raise RuntimeError("No GEMINI_API_KEY or GOOGLE_API_KEY is configured")


def extract_text(data: dict) -> str:
    parts: list[str] = []
    for candidate in data.get("candidates", []):
        for part in candidate.get("content", {}).get("parts", []):
            if "text" in part and not part.get("thought", False):
                parts.append(part["text"])
    return "\n".join(parts).strip()


def sanitised_metadata(data: dict) -> dict:
    candidates = []
    for c in data.get("candidates", []):
        candidates.append({
            "finishReason": c.get("finishReason"),
            "citationMetadata": c.get("citationMetadata"),
            "groundingMetadata": c.get("groundingMetadata"),
            "safetyRatings": c.get("safetyRatings"),
        })
    return {
        "modelVersion": data.get("modelVersion"),
        "responseId": data.get("responseId"),
        "usageMetadata": data.get("usageMetadata"),
        "candidates": candidates,
    }


def generate(label: str, prompt: str, key: str, max_output_tokens: int = 32768) -> tuple[str, dict]:
    url = f"{API_ROOT}/{MODEL}:generateContent?key={urllib.parse.quote(key)}"
    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {
            "thinkingConfig": {"thinkingLevel": "HIGH"},
            "temperature": 0.2,
            "maxOutputTokens": max_output_tokens,
        },
    }
    body = json.dumps(payload).encode("utf-8")
    last_error = None
    for attempt in range(1, 4):
        try:
            request = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(request, timeout=900) as response:
                data = json.load(response)
            text = extract_text(data)
            if len(text) < 500:
                raise RuntimeError(f"short response ({len(text)} characters)")
            return text, sanitised_metadata(data)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, RuntimeError) as exc:
            last_error = exc
            if attempt < 3:
                time.sleep(2 ** attempt)
    raise RuntimeError(f"{label} failed after 3 attempts: {last_error}")


def save_turn(stage: str, name: str, text: str, metadata: dict) -> None:
    folder = OUT / stage
    folder.mkdir(parents=True, exist_ok=True)
    (folder / f"{name}.md").write_text(text + "\n", encoding="utf-8")
    (folder / f"{name}.metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")


def run_parallel(stage: str, prompts: dict[str, str], key: str) -> dict[str, str]:
    folder = OUT / stage
    folder.mkdir(parents=True, exist_ok=True)
    outputs: dict[str, str] = {}
    records = []
    # Serial dispatch prevents Google AI Studio token/rate bursts while preserving
    # blind independence (prompts contain no other seat's output in round 1).
    with ThreadPoolExecutor(max_workers=1) as pool:
        futures = {pool.submit(generate, f"{stage}/{name}", prompt, key): name for name, prompt in prompts.items()}
        for future in as_completed(futures):
            name = futures[future]
            started = utc_now()
            try:
                text, metadata = future.result()
                save_turn(stage, name, text, metadata)
                outputs[name] = text
                records.append({"name": name, "ok": True, "response_chars": len(text), "recorded": started})
                print(f"OK {stage}/{name}: {len(text)} characters", flush=True)
            except Exception as exc:
                records.append({"name": name, "ok": False, "error": str(exc), "recorded": started})
                print(f"FAIL {stage}/{name}: {exc}", flush=True)
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "results.json").write_text(json.dumps(records, indent=2), encoding="utf-8")
    if len(outputs) != len(prompts):
        raise RuntimeError(f"{stage} incomplete: {len(outputs)}/{len(prompts)} agents returned")
    return outputs


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    key = load_key()
    protocol = PROTOCOL.read_text(encoding="utf-8")
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    manifest = {
        "created": utc_now(),
        "model": MODEL,
        "thinkingLevel": "HIGH",
        "provider": "Google AI Studio Gemini API",
        "key_source": "existing GEMINI_API_KEY/GOOGLE_API_KEY; value not logged",
        "google_search_grounding": False,
        "google_search_status": "AVAILABLE BUT FAILED — Google API returned HTTP 429 RESOURCE_EXHAUSTED for grounded search; review must disclose that no grounded search result was used",
        "evidence_window": ["2016-08-17", "2026-08-17"],
        "round_1": "four independent specialist subagents",
        "round_2": "each specialist receives all round-1 outputs and must debate them",
        "final": "editor-teacher synthesis",
        "participant_data": "prohibited; aggregate manuscript text only",
    }
    (OUT / "RUN_MANIFEST.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    shared = f"""{protocol}\n\n--- COMPLETE CALON-C MANUSCRIPT (AGGREGATE TEXT ONLY) ---\n\n{manuscript}"""
    round1_prompts = {
        name: f"""{role}\n\nBLIND ROUND 1. You cannot see the other three specialists. Apply your lens independently to the complete manuscript.\n\n{shared}"""
        for name, role in ROLES.items()
    }
    round1 = run_parallel("round-1-independent", round1_prompts, key)

    dossier = "\n\n".join(f"# ROUND-1 POSITION: {name}\n\n{text}" for name, text in round1.items())
    debate_instruction = """DEBATE ROUND. You now see all four independent reviews. Do not merely summarise them. Identify named claims from the other specialists that you accept, reject, or qualify. Resolve factual disagreements where the manuscript or verified recent literature permits; preserve named dissent where it does not. End with: (1) five consensus points, (2) five unresolved disputes, (3) what Dr Genedy should learn from those disputes, explained in plain clinical-research language."""
    round2_prompts = {
        name: f"""{role}\n\n{debate_instruction}\n\n{dossier}"""
        for name, role in ROLES.items()
    }
    round2 = run_parallel("round-2-debate", round2_prompts, key)

    debate_dossier = "\n\n".join(f"# DEBATE RESPONSE: {name}\n\n{text}" for name, text in round2.items())
    final_prompt = f"""You are the independent teaching chair and Senior Editor-in-Chief. Based only on the four round-1 reviews and four debate responses below, produce the final CALON-C teaching synthesis for Dr Nader Genedy.

Requirements:
1. Lead with the single issue most likely to cause rejection.
2. Give a ranked manuscript repair plan separating analyses that must be rerun, claims that must be weakened/deleted, and prose-only repairs.
3. Produce a consensus table with each specialist's position and any named dissent.
4. Teach the underlying principles in plain language: transport versus external validation; discrimination versus calibration and utility; causal LDL biology versus within-FH prognostic ranking; endpoint harmonisation; competing risk; and why a TIE is not equivalence.
5. Give paragraph-level examples of improved wording from the manuscript.
6. Preserve the 17 August 2016–17 August 2026 evidence window. Do not introduce a citation absent from the retrieved panel evidence unless explicitly labelled unverified.
7. End with a one-week critical-path plan and a submission-readiness verdict: NO-GO, CONDITIONAL GO, or GO.

--- ROUND 1 ---\n{dossier}\n\n--- ROUND 2 DEBATE ---\n{debate_dossier}"""
    final_text, final_meta = generate("final-teaching-synthesis", final_prompt, key, max_output_tokens=32768)
    save_turn("final", "TEACHING_SYNTHESIS", final_text, final_meta)
    print(f"COMPLETE: {OUT}", flush=True)


if __name__ == "__main__":
    main()
