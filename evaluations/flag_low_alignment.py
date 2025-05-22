import json
import argparse
from pathlib import Path
import re

def extract_score(text):
    match = re.search(r"Score:\s*(\d)", text)
    return int(match.group(1)) if match else None

def flag_low_alignment(week, threshold=2):
    input_path = Path(f"output/week{week}_claim_eval_llm.json")
    output_path = Path(f"flagged/low_alignment_week{week}.json")

    if not input_path.exists():
        print(f"❌ File not found: {input_path}")
        return

    with open(input_path, "r") as f:
        data = json.load(f)

    flagged = []

    for entry in data:
        low_scores = {}
        for model, comparison in entry.get("comparisons", {}).items():
            score = extract_score(comparison)
            if score is not None and score <= threshold:
                low_scores[model] = {
                    "score": score,
                    "explanation": comparison
                }

        if low_scores:
            flagged.append({
                "id": entry["id"],
                "original_claim": entry["original_claim"],
                "reconstructed_claims": entry["reconstructed_claims"],
                "low_alignment": low_scores
            })

    output_path.parent.mkdir(exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(flagged, f, indent=2)

    print(f"🚩 Flagged {len(flagged)} annotations with low alignment (≤ {threshold}).")
    print(f"📦 Saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--week", type=int, required=True, help="Week number to scan")
    parser.add_argument("--threshold", type=int, default=2, help="Max score to flag")
    args = parser.parse_args()
    flag_low_alignment(args.week, args.threshold)
