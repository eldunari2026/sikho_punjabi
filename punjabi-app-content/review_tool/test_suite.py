"""Pre-flight validation for the review tool. Run via: python3 -m review_tool.test_suite"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
VOCAB_DIR = ROOT_DIR / "processed_data" / "vocab"
PROVERBS_DIR = ROOT_DIR / "processed_data" / "proverbs"
STREAMS_DIR = ROOT_DIR / "session_work" / "2026-06-10_pipeline_plan"
TOP_PROVERBS_FILE = ROOT_DIR / "review_tool" / "top_100_proverbs.json"

PASS = "PASS"
WARN = "WARN"
FAIL = "FAIL"

results: list[tuple[str, str, str]] = []  # (level, name, detail)


def check(level: str, name: str, detail: str) -> None:
    results.append((level, name, detail))
    symbol = {"PASS": "✓", "WARN": "~", "FAIL": "✗"}[level]
    print(f"  {symbol} [{level}] {name}: {detail}")


# ── T1: Stream files exist and parse ─────────────────────────────────────────

def t1_stream_files() -> None:
    stream_patterns = [f"s{i}_*_enriched.json" for i in range(1, 10)]
    for i, pattern in enumerate(stream_patterns, start=1):
        matches = list(STREAMS_DIR.glob(pattern))
        if not matches:
            check(FAIL, f"T1-S{i}", f"No file matching {pattern} in {STREAMS_DIR.name}/")
            continue
        path = matches[0]
        try:
            with open(path) as f:
                data = json.load(f)
            if not isinstance(data, list) or len(data) == 0:
                check(FAIL, f"T1-S{i}", f"{path.name} is empty or not an array")
            else:
                check(PASS, f"T1-S{i}", f"{path.name}: {len(data)} items")
        except Exception as e:
            check(FAIL, f"T1-S{i}", f"Parse error in {path.name}: {e}")


# ── T2: Vocab counts match expected ─────────────────────────────────────────

EXPECTED_VOCAB = {
    "discoversikhism": (140, 160),
    "learnpunjabi": (460, 490),
    "elearnpunjabi": (410, 440),
    "omniglot": (35, 55),
    "wiktionary": (40, 60),
}

def t2_vocab_counts() -> None:
    from collections import defaultdict
    counts: dict[str, int] = defaultdict(int)
    for path in VOCAB_DIR.glob("[a-z]*_*.json"):
        source = path.stem.rsplit("_", 1)[0]
        counts[source] += 1
    for source, (lo, hi) in EXPECTED_VOCAB.items():
        n = counts.get(source, 0)
        if n == 0:
            check(FAIL, f"T2-{source}", "No files found")
        elif lo <= n <= hi:
            check(PASS, f"T2-{source}", f"{n} files (expected {lo}–{hi})")
        else:
            check(WARN, f"T2-{source}", f"{n} files (expected {lo}–{hi})")


# ── T3: Enriched vocab has roman.readable populated ─────────────────────────

def t3_vocab_enrichment() -> None:
    missing_roman = []
    enriched_count = 0
    for path in VOCAB_DIR.glob("[a-z]*_*.json"):
        if "wiktionary" in path.name:
            continue  # wiktionary not yet enriched — skip
        try:
            with open(path) as f:
                item = json.load(f)
        except Exception:
            continue
        if item.get("needs_enrichment"):
            continue  # expected: wiktionary items — handled above
        enriched_count += 1
        roman = item.get("roman", {})
        if not roman or not roman.get("readable", "").strip():
            missing_roman.append(item.get("id", path.name))
    if missing_roman:
        check(WARN, "T3-roman", f"{len(missing_roman)} enriched vocab items missing roman.readable: {missing_roman[:5]}")
    else:
        check(PASS, "T3-roman", f"All {enriched_count} enriched vocab items have roman.readable")


# ── T4: Proverbs have non-empty english field ────────────────────────────────

def t4_proverb_english() -> None:
    empty_english = []
    count = 0
    for path in PROVERBS_DIR.glob("akhaan_*.json"):
        try:
            with open(path) as f:
                item = json.load(f)
        except Exception:
            continue
        count += 1
        if not item.get("english", "").strip():
            empty_english.append(item.get("id", path.name))
    if empty_english:
        check(WARN, "T4-proverbs", f"{len(empty_english)}/{count} proverbs missing english field")
    else:
        check(PASS, "T4-proverbs", f"All {count} proverbs have english field")


# ── T5: No duplicate IDs across all content ──────────────────────────────────

def t5_id_uniqueness() -> None:
    seen: dict[str, str] = {}
    dupes: list[str] = []

    def scan(paths, loader):
        for path in paths:
            try:
                items = loader(path)
            except Exception:
                continue
            for item in items:
                item_id = item.get("id", "")
                if not item_id:
                    continue
                if item_id in seen:
                    dupes.append(f"{item_id} (in {path.name} and {seen[item_id]})")
                else:
                    seen[item_id] = path.name

    scan(VOCAB_DIR.glob("[a-z]*_*.json"), lambda p: [json.load(open(p))])
    scan(PROVERBS_DIR.glob("akhaan_*.json"), lambda p: [json.load(open(p))])
    scan(STREAMS_DIR.glob("s*_enriched.json"), lambda p: json.load(open(p)))

    if dupes:
        check(FAIL, "T5-ids", f"{len(dupes)} duplicate IDs: {dupes[:3]}")
    else:
        check(PASS, "T5-ids", f"{len(seen)} unique IDs across all content")


# ── T6: Stream items have required fields ────────────────────────────────────

STREAM_REQUIRED = {"id", "full_excerpt_gurmukhi", "romanization", "english_meaning"}

def t6_stream_fields() -> None:
    incomplete = []
    total = 0
    for path in STREAMS_DIR.glob("s*_enriched.json"):
        try:
            with open(path) as f:
                items = json.load(f)
        except Exception:
            continue
        for item in items:
            total += 1
            missing = STREAM_REQUIRED - set(item.keys())
            if missing:
                incomplete.append(f"{item.get('id', '?')} missing {missing}")
    if incomplete:
        check(WARN, "T6-streams", f"{len(incomplete)}/{total} stream items missing required fields: {incomplete[:3]}")
    else:
        check(PASS, "T6-streams", f"All {total} stream items have required fields")


# ── T7: top_100_proverbs.json exists (warning only — may still be generating) ─

def t7_top_proverbs() -> None:
    if TOP_PROVERBS_FILE.exists():
        try:
            with open(TOP_PROVERBS_FILE) as f:
                data = json.load(f)
            check(PASS, "T7-top100", f"top_100_proverbs.json: {len(data)} items")
        except Exception as e:
            check(FAIL, "T7-top100", f"Parse error: {e}")
    else:
        check(WARN, "T7-top100", "top_100_proverbs.json not yet generated — Proverbs tab will show 503 until ready")


def main() -> int:
    print("\n=== Sikho Punjabi Review Tool — Pre-flight Tests ===\n")
    t1_stream_files()
    t2_vocab_counts()
    t3_vocab_enrichment()
    t4_proverb_english()
    t5_id_uniqueness()
    t6_stream_fields()
    t7_top_proverbs()

    failures = [r for r in results if r[0] == FAIL]
    warnings = [r for r in results if r[0] == WARN]
    passes = [r for r in results if r[0] == PASS]

    print(f"\n=== Results: {len(passes)} passed, {len(warnings)} warnings, {len(failures)} failures ===\n")

    if failures:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
