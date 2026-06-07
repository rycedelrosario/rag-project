# RAG Project

This repository contains my Retrieval-Augmented Generation (RAG) project for the GenAI Secure Coding course.

This project will be built incrementally each week.


## Git Commands Used So Far

- git clone  
- git status  
- git add  
- git commit  
- git push

## Project Architecture & Code Breakdown

- **Environment Setup:** Uses `python-dotenv` to securely pull the `GEMINI_API_KEY` from a local `.env` file into system memory without hardcoding secrets.
- **Error Handling:** Features a safety check that crashes early with a `ValueError` if the API key is missing, protecting the application from failing silently.
- **Backend API:** Initialized via `FastAPI()`.
- **Endpoints:** Includes a `/health` route that serves a JSON status message to verify server connectivity and uptime.

## Week 4 Summary

### What Was Set Up This Week
- **Virtual Environment:** Created and activated an isolated Python workspace (`venv`) to keep project packages independent from the system.
- **Dependencies:** Successfully configured a `requirements.txt` file and installed the core libraries needed for development (`fastapi`, `uvicorn`, `python-dotenv`, and `google-generativeai`).
- **Environment Variables:** Set up a secure `.env` file to hold sensitive credentials like the `GEMINI_API_KEY` and updated the project's `.gitignore` to ensure private tokens are never tracked by version control.

### Purpose of `rag_app.py`
The `rag_app.py` file serves as the core entry point and backend server hub for the application. Currently, it responsibly handles:
1. Loading and verifying essential environment configurations.
2. Initializing the main `FastAPI` application instance.
3. Hosting operational endpoints, such as the `/health` check route, to monitor server status and connectivity.

### Questions or Uncertainties
- Everything is clear so far! The environment is running cleanly local, and packages are fully authenticated. Looking forward to implementing the core Retrieval-Augmented Generation (RAG) and Gemini prompting logic in the upcoming weeks.

## Week 5 Summary — Gemini API Integration

### What Was Set Up This Week
- **API Connectivity:** Integrated the official Google GenAI Python SDK (`google-generativeai`) to handle secure network handshakes between our local FastAPI server and Google's model gateways.
- **Environment Synchronization:** Validated our backend configuration to guarantee that the `GEMINI_API_KEY` is loaded dynamically from the local `.env` file into system memory without exposing plain-text secrets to version control.
- **Endpoint Implementation:** Created a brand-new live development route (`/test-gemini`) to verify end-to-end communication from the local client, through our server, to the external AI cloud.

### Purpose of `rag_app.py`
The `rag_app.py` file has transitioned from a static web server blueprint to an operational, data-routing backend engine. Its primary functions now include:
1. Orchestrating secure environment startup configurations and package definitions.
2. Managing system-level routing for structural endpoints (such as `/health`).
3. Controlling upstream API calling parameters safely inside backend-isolated functions, ensuring prompt details and credentials remain completely protected from client-side interception.

### What Was Learned From the Gemini Documentation
- **Model Selection:** Learned to target `gemini-1.5-flash`, balancing high processing speed and conversational accuracy for text generation.
- **SDK Methods:** Mastered how to initialize runtime engine objects via `genai.GenerativeModel` and handle responses cleanly using the `.text` data parsing attribute.
- **Fail-Safe Implementation:** Explored structural `try/except` error blocks, ensuring that when an upstream request fails (e.g., due to an expired or rotated key), the backend catches the crash elegantly and returns a clean error string without printing raw variables or exposing private tokens.

### Troubleshooting & Roadblocks Conquered This Week
- **Git Security & Exposure:** Accidentally committed the raw `.env` file to version control early in the week. Resolved this by running `git rm --cached .env` to clear it from Git's tracking history, updating the `.gitignore` with a strict `.env` exclusion rule, and successfully rotating the compromised API key inside Google AI Studio to prevent unauthorized access.
- **Python Indentation Handling:** Encountered an `IndentationError: unexpected indent` when setting up the FastAPI route block. Learned that Python relies strictly on uniform whitespace (4-space tabs) for defining code hierarchy, which was resolved by re-aligning the block structures inside the text editor.
- **API Key Expiration & 404 Handshakes:** Faced cryptic `404` and `400` errors during initial endpoint connection attempts. Discovered that Google automatically flags and deactivates API keys found in public repository histories, which caused the initial system handshake to fail until a freshly generated token was deployed locally.

### Any Questions / Uncertainties
- While the final API connection is completely functional and secure, the debugging process highlighted how fragile the pipeline can be when string formats or environment states change. Moving forward, I want to explore how to create better local logs so tracking down backend connection issues doesn't rely entirely on standard browser error strings. Ready to transition into building the custom data ingestion and chunking mechanics next week!

## Week 6 Summary — Sequential Prompt Chaining Pipeline

### Description of the Multi-Step Flow
This week, the `/test-gemini` endpoint was redesigned to shift away from a basic single-request layout into a chained, multi-step pipeline architecture. The application now handles data generation across two distinct, linear phases on the backend before delivering a unified response payload to the client.

### Break Down of What Each Step Does
1. **Step 1 (Outline Generation):** The backend queries `gemini-1.5-flash` using a rigid, hardcoded prompt to generate a 3-bullet core structure outlining Python's utility. This text is held strictly inside local server memory as an intermediate variable.
2. **Step 2 (Contextual Expansion):** The application reads that exact intermediate string variable, embeds it directly inside a new prompt template via an f-string, and calls the API a second time to force the model to expand those specific structural notes into a fluid summary paragraph.

### Why the Steps Are Separated
Dividing complex text tasks into modular, sequential phases mirrors how enterprise GenAI pipelines work in production. Splitting the process yields:
- **Better Automated Reasoning:** Forcing the LLM to structure its rules first prevents it from losing context or drifting away from instructions mid-generation.
- **Safer Validation Gates:** It establishes a clear foundation for our upcoming RAG pipeline, allowing data verification layers to inspect or filter information *between* independent execution stages.

### Challenges & Open Questions
- **Dependency Debugging:** A notable hurdle during development was managing local configuration and formatting rules. Getting comfortable adjusting syntax spacing in Python and recognizing editor status colors (like modified file tracking states) emphasized how meticulous backend architecture needs to be.
- **Key Expiration Impacts:** Encountering API key invalidation blocks early on highlighted that upstream pipeline errors require robust, non-leaking safety catches (`try/except`) so that authentication tokens never escape into client-side browser errors during systemic failures.