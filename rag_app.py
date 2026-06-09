import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException  # Added HTTPException here
from pydantic import BaseModel              # Added Pydantic data structures
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
# Step 2: Define the incoming data shape from the user
class QueryRequest(BaseModel):
    question: str

# Step 3: Reject empty or bad inputs before touching the API
def validate_user_input(text: str):
    if text is None or text.strip() == "":
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    if len(text) < 5:
        raise HTTPException(status_code=400, detail="Question is too short")
        
    if len(text) > 500:
        raise HTTPException(status_code=400, detail="Question is too long")
        # Step 4: Ensure the AI didn't return an empty or broken answer
def validate_model_output(text: str):
    if text is None or text.strip() == "":
        raise HTTPException(status_code=500, detail="AI returned an empty response")
        
    if len(text) < 10:
        raise HTTPException(status_code=500, detail="AI response is too short")

# ==========================================
# WEEK 7 — STABLE INPUT/OUTPUT PIPELINE (gemini-2.5-flash)
# ==========================================

def review_model_output(original_answer: str):
    review_prompt = f"""
    You are reviewing an AI-generated response.
    
    Your job:
    - If the response is unclear, incomplete, or poorly written, improve it.
    - If the response is already good, return it unchanged. Do not add conversational meta-text.
    
    AI response to review:
    {original_answer}
    """
    try:
        # Give the Google API gateway 2 seconds to reset its rate limit counter
        time.sleep(2)
        
        review_model = genai.GenerativeModel("gemini-2.5-flash")
        review_response = review_model.generate_content(review_prompt)
        
        if review_response and review_response.text:
            return review_response.text.strip()
        return original_answer
    except Exception:
        # If we hit a 429 rate limit, silently fall back to the original answer so the user gets a response!
        return original_answer

@app.post("/query")
def query_ai(request: QueryRequest):
    try:
        validate_user_input(request.question)
        
        primary_model = genai.GenerativeModel("gemini-2.5-flash")
        primary_response = primary_model.generate_content(request.question)
        raw_answer = primary_response.text
        
        validate_model_output(raw_answer)
        
        # This function now safely catches 429 quota exceptions
        reviewed_answer = review_model_output(raw_answer)
        
        return {
            "question": request.question,
            "answer": reviewed_answer
        }
        
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"An error occurred during pipeline execution: {str(e)}"
        )
    
    return review_response.text
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