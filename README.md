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