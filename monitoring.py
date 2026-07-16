# monitoring.py
# -------------
# This file monitors the quality of our RAG app's responses.
#
# What is hallucination?
# Even when we give an LLM context documents, it sometimes generates
# information that isn't actually in those documents. It "fills in the gaps"
# with plausible-sounding but unverified facts. This is called hallucination.
#
# How do we detect it?
# We use a technique called "LLM-as-judge": we send the answer AND the
# source documents back to Gemini and ask it to evaluate whether the answer
# is actually supported by the context. This is a common pattern in
# production RAG systems.

from google import genai
from google.genai import types
from config import GEMINI_API_KEY, GEMINI_MODEL

_client = genai.Client(api_key=GEMINI_API_KEY)


def check_hallucination(answer, context_docs):
    """
    Ask Gemini to evaluate whether the generated answer is grounded in
    the source documents that were retrieved.

    Args:
        answer:       The answer our app generated.
        context_docs: The documents we retrieved and used as context.

    Returns:
        A dictionary with:
          - "verdict":     "GROUNDED", "PARTIAL", or "HALLUCINATED"
          - "is_grounded": True if verdict is GROUNDED, False otherwise
          - "warning":     A warning string to show the user (empty if grounded)
    """
    if not context_docs:
        return {
            "verdict": "HALLUCINATED",
            "is_grounded": False,
            "warning": "Warning: This answer may contain information not found in the source documents."
        }

    try:
        # 1. Format context_docs into a single string
        context = "\n\n".join([f"Document {i+1}: {doc}" for i, doc in enumerate(context_docs)])

        # 2. Build the evaluator prompt
        prompt = f"""You are an objective AI judge evaluating whether a generated answer is supported by the provided context documents.

Context Documents:
{context}

Generated Answer to Evaluate:
{answer}

Evaluate the alignment of the Generated Answer with the Context Documents. Classify the answer into exactly one of these three categories:
- GROUNDED: The generated answer is fully supported by, and contains no factual claims outside of, the provided context documents.
- PARTIAL: The generated answer is partially supported, but contains some additional assumptions, inferences, or outside facts not directly found in the documents.
- HALLUCINATED: The generated answer contains significant claims, facts, or instructions that are completely unsupported by the provided context documents.

Respond with exactly one word from this list: GROUNDED, PARTIAL, or HALLUCINATED. Do not include any other text, explanation, or punctuation."""

        # 3. Call Gemini with deterministic parameters (temperature=0.0)
        response = _client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.0),
        )
        
        verdict = response.text.strip().upper()

        # Clean up any trailing punctuation (like periods)
        for char in [".", "!", ",", "\n"]:
            verdict = verdict.replace(char, "")

        # 4. Fallback default if the model deviates
        valid_verdicts = {"GROUNDED", "PARTIAL", "HALLUCINATED"}
        if verdict not in valid_verdicts:
            verdict = "PARTIAL"

        # 5. Set appropriate warning thresholds
        if verdict == "GROUNDED":
            warning = ""
            is_grounded = True
        elif verdict == "PARTIAL":
            warning = "Note: This answer may include some information beyond the provided sources."
            is_grounded = False
        else: # HALLUCINATED
            warning = "Warning: This answer may contain information not found in the source documents."
            is_grounded = False

        return {
            "verdict": verdict,
            "is_grounded": is_grounded,
            "warning": warning
        }

    except Exception as e:
        # 6. Safety fallback in case of API failure
        return {
            "verdict": "UNKNOWN",
            "is_grounded": True,
            "warning": ""
        }


def calculate_confidence(distances):
    """
    Convert ChromaDB similarity distances into a 0–1 confidence score.

    Args:
        distances: A list of L2 distance values from ChromaDB.
                   0.0 = identical vectors, 2.0 = completely different.

    Returns:
        A float between 0.0 (not confident) and 1.0 (very confident).
    """
    # 1. Empty distances base case
    if not distances:
        return 0.0

    # 2. Compute the average vector distance
    avg_distance = sum(distances) / len(distances)

    # 3. Convert distance space to similarity confidence
    confidence = max(0.0, 1.0 - (avg_distance / 2.0))

    # 4. Round cleanly to 2 decimal places
    return round(confidence, 2)
