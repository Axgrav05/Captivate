import json
import argparse
from pathlib import Path
import sys

# Patch root to sys.path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from models.gemini_wrapper import query_gemini
from models.mistral_wrapper import query_mistral
from models.llama_wrapper import query_llama
from models.openrouter_wrapper import query_openrouter

ERROR_TAGS = ["Error", "Unauthorized", "not found", "Payment Required"]

LLM_FUNCTIONS = {
    "Gemini": query_gemini,
    "Mistral": query_mistral,
    "LLaMA": query_llama,
    "OpenRouter": query_openrouter,
}

def has_error(value):
    return any(tag in value for tag in ERROR_TAGS)

def retry_failed_outputs(week, mode):
    if mode == "results":
        path = Path(f"output/week{week}_results.json")
    elif mode == "claims":
        path = Path(f"output/week{week}_claim_eval_llm_subset.json")
    else:
        print("❌ Invalid mode. Use 'results' or 'claims'.")
        return

    if not path.exists():
        print(f"❌ File not found: {path}")
        return

    with open(path, "r") as f:
        data = json.load(f)

    updated = False

    for item in data:
        annotation = item.get("annotation") or item.get("original_claim")
        if not annotation:
            continue

        key = "outputs" if mode == "results" else "reconstructed_claims"
        model_responses = item.get(key, {})

        for model, func in LLM_FUNCTIONS.items():
            response = model_responses.get(model, "")
            if has_error(response):
                print(f"🔁 Retrying {model} for ID {item['id']}...")
                try:
                    new_output = func(annotation)
                    item[key][model] = new_output.strip()
                    updated = True
                except Exception as e:
                    print(f"❌ Retry failed for {model}: {e}")

    if updated:
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"✅ File updated: {path}")
    else:
        print("✅ No retries needed — all outputs are valid.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--week", type=int, required=True, help="Week number to patch")
    parser.add_argument("--mode", type=str, default="results", help="Which file to patch: 'results' or 'claims'")
    args = parser.parse_args()
    retry_failed_outputs(args.week, args.mode)