"""Export enriched review content to static JSON files for CDN hosting."""

from __future__ import annotations

import json
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]   # Sikho_Punjabi/
CONTENT_DIR = Path(__file__).resolve().parents[1]  # punjabi-app-content/
VOCAB_DIR = CONTENT_DIR / "processed_data" / "vocab"
PROVERBS_FILE = Path(__file__).resolve().parent / "top_100_proverbs.json"
STREAMS_DIR = CONTENT_DIR / "session_work" / "2026-06-10_pipeline_plan"
OUTPUT_DIR = ROOT_DIR / "public" / "data"


def load_json_file(path: Path):
    try:
        with path.open(encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Warning: failed to parse {path}: {e}")
    except OSError as e:
        print(f"Warning: failed to read {path}: {e}")
    return None


def write_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def display_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT_DIR).as_posix()
    except ValueError:
        return path.as_posix()


def stream_sort_key(stream_key: str) -> tuple[int, str]:
    if len(stream_key) > 1 and stream_key[0] == "s" and stream_key[1:].isdigit():
        return (int(stream_key[1:]), stream_key)
    return (10_000, stream_key)


def generate_vocab() -> list[dict]:
    vocab_items = []

    for path in sorted(VOCAB_DIR.glob("[a-z]*_*.json")):
        item = load_json_file(path)
        if item is None:
            continue
        if not isinstance(item, dict):
            print(f"Warning: {path} did not contain a JSON object, skipping")
            continue
        if "id" not in item:
            print(f"Warning: {path} missing id, skipping")
            continue

        needs_enrichment = item.get("needs_enrichment")
        if isinstance(needs_enrichment, list) and needs_enrichment:
            continue

        tags = item.get("tags", [])
        if not isinstance(tags, list):
            tags = []

        source = ""
        for tag in tags:
            if tag != "conversational":
                source = tag
                break

        roman = item.get("roman")
        roman_readable = roman.get("readable", "") if isinstance(roman, dict) else ""

        vocab_items.append(
            {
                "id": item["id"],
                "gurmukhi": item.get("gurmukhi", ""),
                "roman_readable": roman_readable,
                "english": item.get("english", ""),
                "part_of_speech": item.get("part_of_speech", ""),
                "tags": tags,
                "source": source,
            }
        )

    return sorted(vocab_items, key=lambda item: (item["source"], item["id"]))


def generate_proverbs() -> list:
    if not PROVERBS_FILE.exists():
        print("Warning: top_100_proverbs.json not found, skipping proverbs")
        return []

    proverbs = load_json_file(PROVERBS_FILE)
    if proverbs is None:
        return []
    if not isinstance(proverbs, list):
        print(f"Warning: {PROVERBS_FILE} did not contain a JSON array, skipping proverbs")
        return []
    return proverbs


def generate_streams() -> dict[str, list]:
    streams = {}

    for path in sorted(STREAMS_DIR.glob("s*_enriched.json")):
        stream_key = path.name.split("_", 1)[0]
        items = load_json_file(path)
        if items is None:
            continue
        if not isinstance(items, list):
            print(f"Warning: {path} did not contain a JSON array, skipping")
            continue
        streams[stream_key] = items

    return {key: streams[key] for key in sorted(streams, key=stream_sort_key)}


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    vocab = generate_vocab()
    vocab_file = OUTPUT_DIR / "vocab.json"
    write_json(vocab_file, vocab)
    print(f"Writing {display_path(vocab_file)} ... {len(vocab)} items")

    proverbs = generate_proverbs()
    proverbs_file = OUTPUT_DIR / "proverbs.json"
    write_json(proverbs_file, proverbs)
    print(f"Writing {display_path(proverbs_file)} ... {len(proverbs)} items")

    streams = generate_streams()
    streams_file = OUTPUT_DIR / "streams.json"
    stream_item_count = sum(len(items) for items in streams.values())
    write_json(streams_file, streams)
    print(
        f"Writing {display_path(streams_file)} ... "
        f"{stream_item_count} items across {len(streams)} streams"
    )

    print(f"Done. Output in {display_path(OUTPUT_DIR)}/")


if __name__ == "__main__":
    main()
