import json
import os
import argparse
from pathlib import Path
from dotenv import load_dotenv
from models.gemini_wrapper import query_gemini
from models.mistral_wrapper import query_mistral
from models.llama_wrapper import query_llama
from models.openrouter_wrapper import query_openrouter
from evaluations.llm_moral_ranking import evaluate_outputs




# Load environment variables
load_dotenv()

# Load prompt template
def load_prompt_template():
    path = Path("prompts/prompt_template.txt")
    return path.read_text()

# Load annotations
def load_annotations():
    path = Path("annotations/samples.json")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

# Replace placeholder in prompt
def format_prompt(template, annotation_text):
    return template.replace("{INSERT_ANNOTATION_HERE}", annotation_text)

def run_pipeline(week):
    annotation_file = Path(f"annotations/week{week}_annotations.json")
    output_file = Path(f"output/week{week}_results.json")

    with open("prompts/prompt_template.txt", "r") as f:
        prompt_template = f.read()

    with open(annotation_file, "r") as f:
        annotations = json.load(f)

    results = []

    for item in annotations:
        print(f"\n🔍 Processing annotation ID: {item['id']}")
        prompt = format_prompt(prompt_template, item["annotation"])

        gemini_response = query_gemini(prompt)
        mistral_response = query_mistral(prompt)
        llama_response = query_llama(prompt)
        openrouter_response = query_openrouter(prompt)

        outputs = {
            "Gemini": gemini_response,
            "Mistral": mistral_response,
            "LLaMA": llama_response,
            "OpenRouter": openrouter_response
        }

        evaluation = evaluate_outputs(item["annotation"], outputs)

        result = {
            "id": item["id"],
            "annotation": item["annotation"],
            "outputs": outputs,
            "evaluation": evaluation
        }

        results.append(result)

    output_file.write_text(json.dumps(results, indent=2))
    print(f"\n✅ Week {week} complete! Results saved to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--week", type=int, required=True, help="Week number to process")
    args = parser.parse_args()

    run_pipeline(args.week)

