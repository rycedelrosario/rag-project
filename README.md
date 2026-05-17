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