import json
import argparse
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils.prompt_templates import NLI_PROMPT
from utils.config import NLI_MODELS

def nli_compare(original, reconstructed, model_name):
    prompt = NLI_PROMPT.format(original=original, reconstructed=reconstructed)
    return NLI_MODELS[model_name](prompt)

def run_nli_eval(input_file, output_file, models):
    with open(input_file, "r") as f:
        data = json.load(f)

    results = []
    for entry in data:
        orig = entry["original_claim"]
        nli_results = {}
        for model, claim in entry["reconstructed_claims"].items():
            for nli_model in models:
                if claim and "Error" not in claim:
                    result = nli_compare(orig, claim, nli_model)
                    nli_results[f"{model}_by_{nli_model}"] = result
        results.append({
            "id": entry["id"],
            "original_claim": orig,
            "reconstructed_claims": entry["reconstructed_claims"],
            "nli_results": nli_results
        })
        print(f"✅ NLI-evaluated annotation ID {entry['id']}")

    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n📦 NLI evaluation complete. Results saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True)
    parser.add_argument("--output", type=str, required=True)
    parser.add_argument("--nli_models", nargs="+", default=["gemini", "gpt"])
    args = parser.parse_args()
    run_nli_eval(args.input, args.output, args.nli_models)
