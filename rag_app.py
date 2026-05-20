import os
from dotenv import load_dotenv
# 1. Add this new import line at the top
from fastapi import FastAPI

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
        # 1. Initialize the model precisely as requested
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # 2. Use the exact hardcoded prompt from Step 3
        prompt = "Explain what a large language model is in one paragraph."
        response = model.generate_content(prompt)
        
        # 3. Return the response text as a clean JSON object
        return {
            "status": "success",
            "gemini_response": response.text
        }
        
    except Exception as e:
        # Step 5: Raise a clear error without exposing secrets or printing the key
        return {
            "status": "error",
            "message": f"An error occurred while calling the Gemini API: {str(e)}"
        }