import sys
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import json
import argparse
from pathlib import Path
from models.gemini_wrapper import query_gemini
from models.mistral_wrapper import query_mistral
from models.llama_wrapper import query_llama
from models.openrouter_wrapper import query_openrouter

from utils.prompt_templates import CLAIM_RECONSTRUCT_LLM_PROMPT, CLAIM_COMPARE_PROMPT

def get_original_claim(annotation):
    sentences = annotation.strip().split(". ")
    return sentences[-1].strip().rstrip(".") + "."

def reconstruct_claims(annotation_body):
    prompt = CLAIM_RECONSTRUCT_LLM_PROMPT.format(body=annotation_body)
    return {
        "Gemini": query_gemini(prompt),
        "Mistral": query_mistral(prompt),
        "LLaMA": query_llama(prompt),
        "OpenRouter": query_openrouter(prompt)
    }

def compare_claims(original, reconstructed_claims):
    comparisons = {}
    for model, claim in reconstructed_claims.items():
        comparison_prompt = CLAIM_COMPARE_PROMPT.format(original=original, reconstructed=claim)
        result = query_openrouter(comparison_prompt)
        comparisons[model] = result.strip()
    return comparisons

def strip_final_sentence(annotation):
    sentences = annotation.strip().split(". ")
    return ". ".join(sentences[:-1]) if len(sentences) > 1 else annotation

def run_llm_claim_alignment(week):
    annotation_path = Path(f"annotations/week{week}_annotations.json")
    output_path = Path(f"output/week{week}_claim_eval_llm.json")

    with open(annotation_path, "r") as f:
        annotations = json.load(f)

    results = []

    for entry in annotations:
        annotation_id = entry["id"]
        full_annotation = entry["annotation"]

        original_claim = get_original_claim(full_annotation)
        annotation_body = strip_final_sentence(full_annotation)
        reconstructed_claims = reconstruct_claims(annotation_body)
        comparisons = compare_claims(original_claim, reconstructed_claims)

        results.append({
            "id": annotation_id,
            "original_claim": original_claim,
            "reconstructed_claims": reconstructed_claims,
            "comparisons": comparisons
        })

        print(f"✅ Processed annotation ID {annotation_id}")

    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n📦 Saved LLM claim alignment results to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--week", type=int, required=True, help="Week number to evaluate")
    args = parser.parse_args()
    run_llm_claim_alignment(args.week)
