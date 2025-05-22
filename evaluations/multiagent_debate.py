import json
import argparse
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils.prompt_templates import DEBATE_PROMPT
from models.gemini_wrapper import query_gemini
from models.openai_wrapper import query_gpt_nli

# Choose your judge LLM here (add more if you wish)
JUDGE_MODELS = {
    "gemini": query_gemini,
    "gpt": query_gpt_nli,
}

def build_debate_prompt(original, recon_claims):
    recon_text = "\n".join(
        [f"{model}: {claim}" for model, claim in recon_claims.items() if claim and "Error" not in claim]
    )
    prompt = DEBATE_PROMPT.format(
        original=original,
        reconstructions=recon_text
    )
    return prompt

def run_debate_eval(input_file, output_file, judge_model="gemini"):
    with open(input_file, "r") as f:
        data = json.load(f)

    results = []
    for entry in data:
        orig = entry["original_claim"]
        recon_claims = entry["reconstructed_claims"]
        prompt = build_debate_prompt(orig, recon_claims)
        judge_response = JUDGE_MODELS[judge_model](prompt)
        results.append({
            "id": entry["id"],
            "original_claim": orig,
            "reconstructed_claims": recon_claims,
            "debate_judge": judge_model,
            "debate_result": judge_response
        })
        print(f"✅ Debate evaluated annotation ID {entry['id']} (Judge: {judge_model})")

    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n📦 Debate evaluation complete. Results saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True)
    parser.add_argument("--output", type=str, required=True)
    parser.add_argument("--judge", type=str, choices=JUDGE_MODELS.keys(), default="gemini")
    args = parser.parse_args()
    run_debate_eval(args.input, args.output, args.judge)
