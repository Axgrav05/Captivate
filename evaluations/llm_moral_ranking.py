from models.gemini_wrapper import query_gemini

def create_eval_prompt(annotation, outputs):
    return f"""
You are given a meme annotation and four interpretations from different LLMs that attempt to extract the meme's underlying moral.

Your task is to evaluate these outputs and:
1. Rank them from most to least accurate.
2. Briefly justify your ranking.
3. State which model produced the best moral.

Annotation:
{annotation}

LLM Outputs:
Gemini: {outputs.get("Gemini", "N/A")}
Mistral: {outputs.get("Mistral", "N/A")}
LLaMA: {outputs.get("LLaMA", "N/A")}
OpenRouter: {outputs.get("OpenRouter", "N/A")}

Respond in the following format:

Ranking:
1st: <model name>
2nd: <model name>
3rd: <model name>
4th: <model name>

Reasoning:
<your explanation>

Best Model: <model name>
""".strip()

def evaluate_outputs(annotation, outputs):
    prompt = create_eval_prompt(annotation, outputs)
    evaluation = query_gemini(prompt)
    return evaluation
