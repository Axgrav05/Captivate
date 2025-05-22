CLAIM_RECONSTRUCT_LLM_PROMPT = """
Based only on the body of the annotation below (excluding any conclusion), infer the best possible main claim or moral.
Write a single concise sentence.

Annotation body:
{body}

Reconstructed Claim:
"""

CLAIM_COMPARE_PROMPT = """
Compare the following two claims. Are they semantically similar? Give a 1–5 rating and a short explanation.

Score Guide:
1 - Completely unrelated or contradictory messages.
2 - Vaguely related topic, but different main ideas.
3 - Moderately similar, some overlap in themes but not exact.
4 - Strong similarity with small differences in phrasing or focus.
5 - Perfect match: same message and intent.

Example 1:
Original: "Mayor Frey is an inept and hypocritical leader."
Reconstructed: "Jacob Frey failed to protect the city and should not be compensated for riot damage."
Score: 5
Explanation: Both claims express blame and hypocrisy, with clear alignment on responsibility.

Example 2:
Original: "Obama ruined America."
Reconstructed: "The U.S. faced challenges during Obama’s presidency."
Score: 2
Explanation: Different tone and framing; one is harshly critical, the other neutral.

Now evaluate the following:
Original Claim: {original}
Reconstructed Claim: {reconstructed}

Your response should look like:
Score: <1-5>
Explanation: <why>
"""

CLAIM_EXTRACTION_PROMPT = """
Given this annotation, extract the main claim in a single sentence...
"""

# New NLI prompt
NLI_PROMPT = """
Given two statements, classify their logical relationship as Entailment, Neutral, or Contradiction.

Statement A (Original claim): {original}
Statement B (Reconstructed claim): {reconstructed}

Your response format:
Label: <Entailment/Neutral/Contradiction>
Explanation: <short justification>
"""

DEBATE_PROMPT = """
You are an impartial AI judge.
Given the original claim and several reconstructed claims from different AI models, rank the reconstructed claims by how closely they align with the original.
Justify your ranking briefly.

Original claim:
{original}

Reconstructed claims:
{reconstructions}

Your format:
1st: <model>
2nd: <model>
3rd: <model>
...
Reasoning:
<your explanation>
"""
