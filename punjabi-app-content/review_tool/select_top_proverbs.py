from __future__ import annotations

import json
from math import ceil
from pathlib import Path
from typing import Any

from enrichment.client import chat


BATCH_SIZE = 300
PASS_1_PICK_COUNT = 20
FINAL_PICK_COUNT = 100

SYSTEM_PROMPT = (
    "You are a Punjabi cultural expert selecting proverbs for a conversational "
    "Punjabi learning app for diaspora and heritage speakers."
)

ROOT_DIR = Path(__file__).resolve().parents[1]
PROVERBS_DIR = ROOT_DIR / "processed_data" / "proverbs"
OUTPUT_PATH = ROOT_DIR / "review_tool" / "top_100_proverbs.json"


def load_proverbs() -> list[dict[str, Any]]:
    proverbs: list[dict[str, Any]] = []
    for path in sorted(PROVERBS_DIR.glob("akhaan_*.json")):
        with path.open("r", encoding="utf-8") as f:
            proverbs.append(json.load(f))
    return proverbs


def compact_proverb(proverb: dict[str, Any]) -> dict[str, str]:
    return {
        "id": str(proverb.get("id", "")),
        "english": str(proverb.get("english", "")),
        "cultural_note": str(proverb.get("cultural_note", "")),
    }


def compact_json(proverbs: list[dict[str, Any]]) -> str:
    compact = [compact_proverb(proverb) for proverb in proverbs]
    return json.dumps(compact, ensure_ascii=False, separators=(",", ":"))


def strip_markdown_fences(text: str) -> str:
    stripped = text.strip()
    if not stripped.startswith("```"):
        return stripped

    lines = stripped.splitlines()
    if lines and lines[0].lstrip().startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return "\n".join(lines).strip()


def parse_json_array(text: str) -> list[dict[str, Any]]:
    parsed = json.loads(strip_markdown_fences(text))
    if not isinstance(parsed, list):
        raise ValueError("GPT response was not a JSON array")
    if not all(isinstance(item, dict) for item in parsed):
        raise ValueError("GPT response array contained non-object items")
    return parsed


def json_chat(messages: list[dict[str, str]], temperature: float = 0.2) -> list[dict[str, Any]]:
    response = chat(messages, temperature=temperature)
    try:
        return parse_json_array(response)
    except (json.JSONDecodeError, ValueError):
        retry_messages = list(messages)
        retry_messages[-1] = {
            "role": "user",
            "content": (
                messages[-1]["content"]
                + "\n\nReminder: return raw JSON only. No markdown fences, no prose."
            ),
        }
        retry_response = chat(retry_messages, temperature=temperature)
        return parse_json_array(retry_response)


def build_pass_1_prompt(batch: list[dict[str, Any]]) -> str:
    json_str = compact_json(batch)
    n = len(batch)
    return (
        f"From these {n} Punjabi proverbs, select the TOP {PASS_1_PICK_COUNT} most "
        "culturally important for diaspora learners. Prioritize: widely recognized, "
        "clear wisdom, diverse themes (wisdom, family, nature, community, humor, "
        "courage, faith). Return ONLY a JSON array: "
        '[{"id": "akhaan_xxx", "reason": "one line"}]. No markdown, no other text.'
        f"\n\nProverbs:\n{json_str}"
    )


def build_pass_2_prompt(semifinalists: list[dict[str, Any]]) -> str:
    json_str = compact_json(semifinalists)
    n = len(semifinalists)
    return (
        f"From these {n} semifinalist Punjabi proverbs, select the BEST {FINAL_PICK_COUNT} "
        "for a heritage learner introduction. Ensure diversity across: wisdom/life, "
        "family/relationships, nature, community/society, humor, courage/resilience, "
        "faith/spirituality. Avoid redundancy — do not pick multiple proverbs expressing "
        "the same idea. Return ONLY a JSON array of exactly 100 objects: "
        '[{"id": "akhaan_xxx", "theme": "family", "reason": "one line"}]. '
        "No markdown, no other text."
        f"\n\nProverbs:\n{json_str}"
    )


def batch_items(items: list[dict[str, Any]], batch_size: int) -> list[list[dict[str, Any]]]:
    return [items[i : i + batch_size] for i in range(0, len(items), batch_size)]


def select_semifinalists(proverbs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {proverb["id"]: proverb for proverb in proverbs}
    selected_ids: set[str] = set()
    semifinalists: list[dict[str, Any]] = []
    batches = batch_items(proverbs, BATCH_SIZE)
    total_batches = len(batches)

    for index, batch in enumerate(batches, start=1):
        print(f"Pass 1: batch {index}/{total_batches}...", flush=True)
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_pass_1_prompt(batch)},
        ]
        try:
            picks = json_chat(messages)
        except Exception as exc:
            print(f"Warning: Pass 1 batch {index} failed: {exc}", flush=True)
            continue

        for pick in picks:
            proverb_id = pick.get("id")
            if proverb_id in by_id and proverb_id not in selected_ids:
                selected_ids.add(proverb_id)
                semifinalists.append(by_id[proverb_id])

    return semifinalists


def select_finalists(semifinalists: list[dict[str, Any]]) -> list[dict[str, Any]]:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": build_pass_2_prompt(semifinalists)},
    ]
    picks = json_chat(messages)
    by_id = {proverb["id"]: proverb for proverb in semifinalists}
    seen_ids: set[str] = set()
    finalists: list[dict[str, Any]] = []

    for pick in picks:
        proverb_id = pick.get("id")
        if proverb_id not in by_id or proverb_id in seen_ids:
            continue

        seen_ids.add(proverb_id)
        finalist = dict(by_id[proverb_id])
        finalist["selection_theme"] = str(pick.get("theme", "")).strip()
        finalist["selection_reason"] = str(pick.get("reason", "")).strip()
        finalists.append(finalist)

    if len(finalists) < 80:
        raise ValueError(
            f"Pass 2 returned only {len(finalists)} usable unique picks; expected ~{FINAL_PICK_COUNT}"
        )
    if len(finalists) != FINAL_PICK_COUNT:
        print(f"Warning: got {len(finalists)} finalists (expected {FINAL_PICK_COUNT}), proceeding", flush=True)

    return finalists


def save_finalists(finalists: list[dict[str, Any]]) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8") as f:
        json.dump(finalists, f, ensure_ascii=False, indent=2)
        f.write("\n")


def main() -> None:
    print("Loading proverbs...", flush=True)
    proverbs = load_proverbs()
    print(f"Loaded {len(proverbs)} proverbs", flush=True)

    total_batches = ceil(len(proverbs) / BATCH_SIZE)
    if total_batches == 0:
        raise ValueError(f"No proverb JSON files found in {PROVERBS_DIR}")

    semifinalists = select_semifinalists(proverbs)
    print(f"Pass 1 complete: {len(semifinalists)} semifinalists", flush=True)

    print("Pass 2: final selection...", flush=True)
    finalists = select_finalists(semifinalists)
    save_finalists(finalists)

    rel_output = OUTPUT_PATH.relative_to(ROOT_DIR)
    print(f"Done. Saved {len(finalists)} proverbs to {rel_output}", flush=True)


if __name__ == "__main__":
    main()
