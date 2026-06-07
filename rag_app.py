import os
from dotenv import load_dotenv
from fastapi import FastAPI
# ADD THIS LINE RIGHT HERE:
import google.generativeai as genai

# Load the environment variables from your local .env file
load_dotenv()

# Read the GEMINI_API_KEY value
api_key = os.getenv("GEMINI_API_KEY")

# Fail clearly if the key is missing or empty
if not api_key:
    raise ValueError("CRITICAL ERROR: GEMINI_API_KEY is missing from your .env file!")

print("Configuration successful! Your Gemini API key loaded correctly.")

# ==========================================
# 2. ADD THESE FASTAPI LINES AT THE BOTTOM
# ==========================================

# This creates the main app instance that Uvicorn is looking for
app = FastAPI()

# This creates the /health path your instructions asked you to test
@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/test-gemini")
def test_gemini():
    try:
        # Initialize the model
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        # === STEP 1: Ask for a short outline ===
        first_prompt = "Create a brief 3-bullet point outline for an essay about why learning Python is useful."
        first_response = model.generate_content(first_prompt)
        outline_text = first_response.text
        
        # === STEP 2: Use the outline to generate the full response ===
        # We use an f-string to inject the text from step 1 straight into step 2
        second_prompt = f"Using this outline:\n{outline_text}\n\nWrite a coherent, single paragraph expanding on these points."
        second_response = model.generate_content(second_prompt)
        
        # Return the final resulting text
        return {
            "status": "success",
            "step_1_outline": outline_text,
            "step_2_final_response": second_response.text
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"An error occurred during multi-step execution: {str(e)}"
        }