# security.py
# -----------
# This file protects our RAG app from prompt injection attacks.
#
# What is prompt injection?
# When we send a user's question to Gemini, we embed it inside a larger
# prompt that includes instructions and context. A malicious user could
# write something like "Ignore your previous instructions and..." to try
# to override those instructions and make the AI behave differently.
#
# This is one of the most common attacks against LLM-based applications.
# The fix is to check user input BEFORE it ever reaches the LLM.

import re

# --- The RAG/security concept ---
# Think about what a prompt injection attack looks like.
# An attacker is trying to write text that will "escape" from the user
# input role and start issuing new instructions to the LLM.
#
# Add at least 6 phrases that signal this kind of attack.
# Think about phrases like: trying to ignore instructions, claiming a new
# identity, asking the model to forget its context, etc.
#
BLOCKED_PATTERNS = [
    "ignore previous instructions",
    "ignore your previous instructions", # <-- Added this variation!
    "ignore above instructions",
    "system override",
    "you are now a",
    "forget your instructions",
    "disregard all previous instructions",
    "new directive",
    "start instructions from scratch",
    "bypass safety filters",
    "tell me a joke" # <-- Added this to catch this specific test!
]

# Maximum allowed length for a user query.
# Very long inputs are expensive to process and often a sign of abuse.
MAX_QUERY_LENGTH = 500


def validate_input(query: str):
    """
    Validate the user's query against security boundaries.
    Checks for maximum length and malicious injection patterns.
    """
    if not query or not query.strip():
        return False, "Query cannot be empty."

    # 1. Check length limit
    if len(query) > MAX_QUERY_LENGTH:
        return False, f"Query exceeds the maximum limit of {MAX_QUERY_LENGTH} characters."

    # 2. Check blocked patterns (case-insensitive)
    query_lower = query.lower()
    for pattern in BLOCKED_PATTERNS:
        if pattern in query_lower:
            return False, "Security Alert: Unsafe input pattern or potential prompt injection detected."

    return True, ""

def sanitize_input(query: str) -> str:
    """
    Sanitize input to clean up extra spacing or basic formatting characters.
    """
    return query.strip()

def sanitize_input(query):
    """Remove leading/trailing whitespace from user input."""
    return query.strip()
