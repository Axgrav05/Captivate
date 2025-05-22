import json
import sys
import argparse
from pathlib import Path

ANNOTATION_DIR = Path("annotations")

def load_annotations(week):
    path = ANNOTATION_DIR / f"week{week}_annotations.json"
    if not path.exists():
        print(f"⚠️ File {path} does not exist. Creating a new one...")
        path.write_text("[]")
    with open(path, "r") as f:
        return json.load(f), path

def save_annotations(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def add_new_annotation(week):
    annotations, path = load_annotations(week)
    next_id = max([int(entry["id"]) for entry in annotations], default=0) + 1

    print("\n📋 Paste your annotation below. When done, press Ctrl+D (Mac/Linux) or Ctrl+Z then Enter (Windows):\n")
    try:
        new_annotation = sys.stdin.read()
    except EOFError:
        new_annotation = ""

    if not new_annotation.strip():
        print("⚠️ No annotation entered. Aborting.")
        return

    new_entry = {
        "id": str(next_id).zfill(3),
        "annotation": new_annotation.strip()
    }

    annotations.append(new_entry)
    save_annotations(path, annotations)

    print(f"\n✅ Annotation added to week {week} with ID {new_entry['id']}. Total annotations: {len(annotations)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add an annotation for a specific week.")
    parser.add_argument("--week", type=int, required=True, help="Week number (e.g., 2 for week2_annotations.json)")
    args = parser.parse_args()

    add_new_annotation(args.week)
