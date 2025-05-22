import json
import argparse
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from evaluations.nli_evaluator import run_nli_eval
from evaluations.multiagent_debate import run_debate_eval

def run_adversarial_tests(input_file, nli_output, debate_output, nli_models, judge_model):
    # Run NLI on adversarial set
    print("🔍 Running NLI evaluation on adversarial cases...")
    run_nli_eval(input_file, nli_output, nli_models)
    # Run Debate on adversarial set
    print("🔍 Running debate evaluation on adversarial cases...")
    run_debate_eval(input_file, debate_output, judge_model)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True)
    parser.add_argument("--nli_output", type=str, required=True)
    parser.add_argument("--debate_output", type=str, required=True)
    parser.add_argument("--nli_models", nargs="+", default=["gemini", "gpt"])
    parser.add_argument("--judge", type=str, default="gemini")
    args = parser.parse_args()
    run_adversarial_tests(
        args.input,
        args.nli_output,
        args.debate_output,
        args.nli_models,
        args.judge
    )
