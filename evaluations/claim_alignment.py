import sys
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import sys
import json
import argparse
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))


from models.openrouter_wrapper import query_openrouter


CLAIM_PROMPT = """
Extract the main claim from the following annotation. The claim should be a single, clear sentence that captures the main moral or message implied by the author:

Annotation:
{annotation}

Claim:
"""

RECONSTRUCT_PROMPT = """
Based only on the body of the annotation below (excluding the author's concluding sentence), infer the best possible main claim or moral that this annotation is leading to. Write a single sentence:

Body:
{annotation_body}

Inferred Claim:
"""

COMPARE_PROMPT = """
Compare the two claims below. Are they semantically similar? Provide a 1-5 rating (1 = completely different, 5 = perfect match) and explain your reasoning.

Original Claim: {original}
Reconstructed Claim: {reconstructed}

Rating and Explanation:
"""

def strip_final_sentence(text):
    sentences = text.strip().split(". ")
    return ". ".join(sentences[:-1]) if len(sentences) > 1 else text

def run_claim_alignment(week):
    annotation_path = Path(f"annotations/week{week}_annotations.json")
    output_path = Path(f"output/week{week}_claim_eval.json")

    with open(annotation_path, "r") as f:
        annotations = json.load(f)

    results = []

    for entry in annotations:
        full_text = entry["annotation"]
        annotation_id = entry["id"]

        # Step 1: Extract original claim
        claim_prompt = CLAIM_PROMPT.format(annotation=full_text)
        original_claim = query_openrouter(claim_prompt)

        # Step 2: Reconstruct from body
        annotation_body = strip_final_sentence(full_text)
        reconstruct_prompt = RECONSTRUCT_PROMPT.format(annotation_body=annotation_body)
        reconstructed_claim = query_openrouter(reconstruct_prompt)

        # Step 3: Compare both
        compare_prompt = COMPARE_PROMPT.format(original=original_claim, reconstructed=reconstructed_claim)
        comparison = query_openrouter(compare_prompt)

        result = {
            "id": annotation_id,
            "original_claim": original_claim.strip(),
            "reconstructed_claim": reconstructed_claim.strip(),
            "comparison": comparison.strip()
        }

        results.append(result)
        print(f"✅ Processed annotation ID {annotation_id}")

    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n🎯 Claim evaluation complete for week {week}. Results saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--week", type=int, required=True, help="Week number to evaluate")
    args = parser.parse_args()
    run_claim_alignment(args.week)
