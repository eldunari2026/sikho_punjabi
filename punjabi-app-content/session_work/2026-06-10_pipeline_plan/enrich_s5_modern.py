"""
S5 Modern Literary Poetry enrichment: adds cultural reference fields.
SOURCE-ONLY stream — no full poem text. Adds cultural_summary, key_phrases,
copyright_status, and first_lines_gurmukhi (2–4 lines reference only).

Run from punjabi-app-content:
    python3 session_work/2026-06-10_pipeline_plan/enrich_s5_modern.py
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from enrichment.client import chat

SYSTEM_PROMPT = """You are a scholar of 20th-century Punjabi literary poetry. Your task is to produce cultural reference enrichment for poems that are under active copyright and cannot be fully reproduced.

For each item, return a JSON object with exactly these fields:
{
  "first_lines_gurmukhi": "opening 2–4 lines in Gurmukhi script, joined by \\n — reference only, not a full excerpt",
  "romanization": "phonetic romanization of those lines, joined by \\n. Use readable Majhi-dialect conventions: aa/ee/oo for long vowels, no IPA symbols, no diacritics.",
  "cultural_summary": "2–3 sentences in English on the poem's cultural significance, why it matters in the Punjabi literary canon, and what event or discourse it is typically invoked in.",
  "key_phrases_in_usage": "in English: specific phrases from this poem (if any) that have entered everyday Punjabi speech, political discourse, or cultural reference — Gurmukhi phrase followed by a brief English note on how it is used. Empty string if none.",
  "copyright_note": "one sentence in English: copyright status and approximate public domain year."
}

Rules:
- This is a REFERENCE record, not a text reproduction. Do NOT provide full poem text.
- First lines are for reference/identification only — strictly 2–4 lines maximum.
- cultural_summary, key_phrases_in_usage, and copyright_note MUST be written in English.
- Return only the JSON object. No prose before or after."""


def enrich_candidate(candidate: dict) -> dict:
    user_msg = f"""Enrich this cultural reference entry:

Title: {candidate["title"]}
Opening line (Gurmukhi): {candidate["first_line_gurmukhi"]}
Poet: {candidate["poet"]}
Collection: {candidate.get("collection", "N/A")}
Year: {candidate.get("year_published", "N/A")}
Form: {candidate.get("form", "N/A")}
Why important (from curation): {candidate.get("why_important", "")}
Phrases already noted: {candidate.get("phrases_in_general_usage", "")}
Copyright expiry: {candidate.get("copyright_expiry", "N/A")}

Return the JSON object with first_lines_gurmukhi, romanization, cultural_summary, key_phrases_in_usage, copyright_note."""

    raw = chat(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        temperature=0.1,
    )

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass
        return {
            "first_lines_gurmukhi": candidate["first_line_gurmukhi"],
            "romanization": "",
            "cultural_summary": f"PARSE_ERROR — raw: {raw[:300]}",
            "key_phrases_in_usage": "",
            "copyright_note": "",
        }


def main():
    candidates_path = Path(__file__).parent / "s5_modern_candidates.json"
    with open(candidates_path, encoding="utf-8") as f:
        candidates = json.load(f)

    enriched = []
    errors = []

    for i, c in enumerate(candidates):
        print(f"[{i+1:02d}/{len(candidates)}] {c['id']}  {c['title'][:45]}  [{c['poet']}]")
        result = enrich_candidate(c)
        item = {**c, **result}
        enriched.append(item)

        if "PARSE_ERROR" in item.get("cultural_summary", ""):
            print("  ⚠ PARSE_ERROR")
            errors.append(c["id"])
        else:
            print(f"  ✓")

    out_path = Path(__file__).parent / "s5_modern_enriched.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(enriched, f, ensure_ascii=False, indent=2)

    print(f"\n✓ Wrote {len(enriched)} enriched items → {out_path.name}")
    if errors:
        print(f"⚠ Parse errors on: {errors}")

    print("\n─── PREVIEW: first 5 items ───\n")
    for item in enriched[:5]:
        print(f"{'='*60}")
        print(f"{item['id']}  {item['title']}  [{item['poet']} / {item['register']}]")
        print(f"── First lines (reference) ──")
        print(item.get("first_lines_gurmukhi", ""))
        print(f"── Cultural summary ──")
        print(item.get("cultural_summary", ""))
        print(f"── Phrases in usage ──")
        print(item.get("key_phrases_in_usage", "—"))
        print(f"── Copyright ──")
        print(item.get("copyright_note", ""))
        print()


if __name__ == "__main__":
    main()
