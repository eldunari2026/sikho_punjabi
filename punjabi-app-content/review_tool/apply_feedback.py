import argparse
import json
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
FEEDBACK_FILE = ROOT_DIR / "review_tool" / "feedback.json"
VOCAB_DIR = ROOT_DIR / "processed_data" / "vocab"
PROVERBS_DIR = ROOT_DIR / "processed_data" / "proverbs"
STREAMS_DIR = ROOT_DIR / "session_work" / "2026-06-10_pipeline_plan"


def load_json(path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def write_json(path, data):
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def index_single_item_files(index, paths):
    for path in paths:
        try:
            item = load_json(path)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"Warning: could not load {path}: {exc}", file=sys.stderr)
            continue

        item_id = item.get("id")
        if not item_id:
            print(f"Warning: skipping {path}: missing id", file=sys.stderr)
            continue

        index[item_id] = {"kind": "single", "path": path}


def index_stream_files(index, paths):
    for path in paths:
        try:
            items = load_json(path)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"Warning: could not load {path}: {exc}", file=sys.stderr)
            continue

        if not isinstance(items, list):
            print(f"Warning: skipping {path}: expected JSON array", file=sys.stderr)
            continue

        for position, item in enumerate(items):
            if not isinstance(item, dict):
                print(f"Warning: skipping non-object item {position} in {path}", file=sys.stderr)
                continue

            item_id = item.get("id")
            if not item_id:
                print(f"Warning: skipping item {position} in {path}: missing id", file=sys.stderr)
                continue

            index[item_id] = {"kind": "stream", "path": path, "position": position}


def build_source_index():
    index = {}
    index_single_item_files(index, VOCAB_DIR.glob("[a-z]*_*.json"))
    index_single_item_files(index, PROVERBS_DIR.glob("akhaan_*.json"))
    index_stream_files(index, STREAMS_DIR.glob("s*_enriched.json"))
    return index


def update_single_item(path, action, comment):
    item = load_json(path)
    item["review_action"] = action
    item["review_comment"] = comment
    write_json(path, item)


def update_stream_item(path, item_id, action, comment):
    items = load_json(path)
    for item in items:
        if isinstance(item, dict) and item.get("id") == item_id:
            item["review_action"] = action
            item["review_comment"] = comment
            write_json(path, items)
            return True
    return False


def apply_feedback(dry_run):
    if not FEEDBACK_FILE.exists():
        print(f"Error: feedback file not found: {FEEDBACK_FILE}", file=sys.stderr)
        return 1

    try:
        feedback = load_json(FEEDBACK_FILE)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Error: could not load feedback file: {exc}", file=sys.stderr)
        return 1

    if not isinstance(feedback, dict):
        print("Error: feedback file must contain a JSON object", file=sys.stderr)
        return 1

    index = build_source_index()
    updated = 0

    for item_id, decision in feedback.items():
        if not isinstance(decision, dict):
            print(f"Warning: skipping {item_id}: decision is not an object", file=sys.stderr)
            continue

        action = decision.get("action", "")
        if not action:
            continue

        source = index.get(item_id)
        if not source:
            print(f"Warning: item id not found in source files: {item_id}", file=sys.stderr)
            continue

        comment = decision.get("comment", "")
        if dry_run:
            print(f"Would update {item_id}: action={action}, comment={comment[:40]}")
        elif source["kind"] == "single":
            update_single_item(source["path"], action, comment)
        else:
            found = update_stream_item(source["path"], item_id, action, comment)
            if not found:
                print(f"Warning: item id not found in stream file during update: {item_id}", file=sys.stderr)
                continue

        updated += 1

    suffix = " (dry-run)" if dry_run else ""
    print(f"Updated {updated} items{suffix}")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Apply review feedback to source JSON files.")
    parser.add_argument("--dry-run", action="store_true", help="Preview updates without writing files.")
    args = parser.parse_args()

    return apply_feedback(args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
