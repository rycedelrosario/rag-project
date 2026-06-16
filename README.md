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

## Week 7 Summary — Production Guardrails, Input/Output Validation & Rate Limiting

### Technical Objectives Achieved
This week, our application transitioned from a static testing environment into a robust, user-interactive backend API by implementing a live `POST /query` route using FastAPI and Pydantic data schemas. 

### Why Structural Guardrails Matter in Production

1. **Why Input Validation Is Crucial:**
   Processing raw user strings directly exposes an application to system overflows, empty payload anomalies, and excessive token usage. By applying strict constraint rules (`validate_user_input`) at the gateway layer, we block invalid requests before they ever fire a cloud API call. This safeguards server runtime stability and entirely eliminates wasted operational expenses.

2. **Why Output Validation Is Crucial:**
   Generative AI models are fundamentally stochastic and can occasionally return void outputs, truncated text signatures, or fail to complete packets due to minor backend delivery drops. Enforcing server-side structural checks ensures we immediately intercept empty string payloads, throwing clean, professional errors to the frontend client instead of rendering a broken, silently failing user interface.

3. **Why a Dual-Model Critic Pattern Is Used:**
   Passing an original answer draft into a secondary, independent prompt layout (`review_model_output`) establishes an automated proofreading mechanism. This structural design helps audit logic flow, smooth out formatting quirks, and minimize algorithmic hallucinations without requiring manual human oversight.

### Obstacles Overmounted & Debugging Log
- **Resolving Void Payloads (`null` Error Signals):** Encountered an early structural hurdle where the payload successfully cleared the API handshake but returned an empty `"answer": null` layout string. Fixed this by tracking down extraction bottlenecks inside the secondary text parsing attributes and implementing clean variable fallbacks.
- **Handling Free-Tier Quota Caps (`429` Rate Limits):** Moving to the new `gemini-2.5-flash` engine introduced tight token rate caps (5 requests per minute). Because our endpoint fires two distinct queries back-to-back, rapid client testing immediately triggered a `429 Too Many Requests` crash.
- **The Architectural Fix:** Resolved this by updating the backend logic with Python's native `time` utility to introduce an intentional processing delay between generation stages, allowing the Google API gateway counter to reset. Additionally, deployed an exception handling block within the critic loop: if a 429 quota ceiling is encountered, the system gracefully bypasses the review tier and serves the validated primary answer, maintaining application uptime instead of throwing a generic internal server crash.

## Week 8 Summary — Wireframing, Product Design & Secure MVP Architecture

### Technical Objectives Achieved
This week, the project scope shifted from backend server loops to frontend interface design, wireframing, and product management prompt engineering. Using Lovable.dev, a complete 5-screen low-fidelity wireframe prototype was engineered for a Cybersecurity Bootcamp Student Portal.

### Application Screen Architecture
The prototype incorporates five essential views tailored to user workflows and diagnostic training tracking:
1. **Login Screen:** Access gate utilizing authentication boundaries and secure input perimeters.
2. **Dashboard Screen:** High-fidelity overview displaying dynamic student metrics and progress tracking.
3. **Q&A / Quiz Screen:** Hands-on secure-coding training interface for diagnostic exercises.
4. **Report Screen:** Performance summary module detailing grade structures and module completion.
5. **Edit Settings Screen:** Profiles and security configuration panel for credentials.

### Architectural Core Metrics Explained

1. **Representing Progress Actionably (Scenario A):**
   To solve the broad instruction "Students should see progress," the Dashboard was designed with three distinct visualization layers: a top high-level metrics percentage circle (`72% Complete`), a horizontal milestones timeline, and a granular lab checklist. The module checklist combined with stats was chosen as the optimal MVP structure. Technical students require specific, actionable visibility into which exact engineering labs (e.g., packet analysis, network scanning) they have mastered rather than relying on a vague percentage wheel alone.

2. **Secure-by-Design Prototyping (Scenario C):**
   The training interface maps out three critical security constraints directly onto the wireframe layout before any backend code is written:
   - **Password Protection:** Cryptographically masked text blocks on the login gateway.
   - **Input Sanitization:** Constrained text fields built to block malicious string arrays and prevent Injection exploits.
   - **Session Handling:** Integrated layout markers for automated inactivity logout alerts on shared terminal environments.

### Challenges & Engineering Takeaways
- **Managing Vague Product Specifications:** Transitioning from rigid backend specifications to highly ambiguous frontend product scripts required testing different UI layouts side-by-side to find out which elements serve the user best.
- **AI-Assisted Wireframing:** Leveraged sequential chat iterations in Lovable.dev to automatically generate interactive front-end states, proving how rapidly a developer can test user flows and security requirements at the visual stage.