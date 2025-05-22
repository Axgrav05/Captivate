from models.gemini_wrapper import query_gemini
from models.openai_wrapper import query_gpt_nli
from models.huggingface_wrapper import query_hf_bart_mnli

NLI_MODELS = {
    "gemini": query_gemini,
    "gpt": query_gpt_nli,
    "hf_bart_mnli": query_hf_bart_mnli,
}
