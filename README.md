# Factual Hallucination Detection and Correction in LLM-Generated Medical Summaries Using Claim Decomposition and Evidence Retrieval

## Query Generation Module

This project is now organized as a clean full-stack structure with a separate FastAPI backend and React frontend. The backend preserves the useful existing claim-to-query generation logic, and the frontend provides a simple student-friendly UI for testing it.

## What Was Kept and Reorganized

- Kept the working FastAPI request flow and Pydantic schemas from the existing `app/` code.
- Preserved the useful rule-based query generation logic and moved it into a proper backend service and utility layer.
- Added safe spaCy fallback so the backend does not crash if a model is unavailable.
- Added a new React + Vite frontend for interacting with the backend.
- Removed the old misplaced root backend files in favor of a clear `backend/` and `frontend/` separation.
- Added root-level scripts so the whole project can be started from VS Code or a single terminal.
- Preserved backward-compatible API routes such as `/api/health` and `/api/generate-query` to avoid breaking older callers.

## Final Folder Structure

```text
query-generation-module/
|
|-- backend/
|   |-- app/
|   |   |-- main.py
|   |   |-- routes/
|   |   |   `-- query_routes.py
|   |   |-- services/
|   |   |   `-- query_service.py
|   |   |-- schemas/
|   |   |   `-- query_schema.py
|   |   |-- utils/
|   |   |   `-- text_utils.py
|   |   `-- __init__.py
|   |-- requirements.txt
|   |-- run.py
|   `-- README.md
|
|-- frontend/
|   |-- src/
|   |   |-- App.jsx
|   |   |-- main.jsx
|   |   |-- components/
|   |   |   |-- ClaimForm.jsx
|   |   |   `-- ResultCard.jsx
|   |   `-- api/
|   |       `-- queryApi.js
|   |-- index.html
|   |-- package.json
|   |-- vite.config.js
|   `-- README.md
|
`-- README.md
```

## Quick Start

### One Command

```powershell
npm install
python -m pip install -r backend/requirements.txt
npm run fullstack
```

This starts:

- Backend on `http://127.0.0.1:8000`
- Backend docs on `http://127.0.0.1:8000/docs`
- Frontend on `http://127.0.0.1:5173`

### Individual Commands

```powershell
npm run server
npm run client
npm run dev
```

### VS Code

Use the task `Run fullstack app` from `Terminal -> Run Task`, or run `npm run fullstack` in the integrated terminal.

## Expected Localhost Links

- Backend: `http://127.0.0.1:8000`
- Backend docs: `http://127.0.0.1:8000/docs`
- Frontend: `http://127.0.0.1:5173`

## Sample Backend Input

```json
{
  "claim": "Insulin is used to manage diabetes."
}
```

## Sample Backend Output

```json
{
  "success": true,
  "message": "Query generated successfully",
  "data": {
    "claim": "Insulin is used to manage diabetes.",
    "keywords": ["insulin", "diabetes", "management"],
    "primary_query": "insulin diabetes management",
    "alternate_queries": [
      "insulin for diabetes management",
      "diabetes insulin therapy",
      "insulin and diabetes treatment"
    ]
  }
}
```

## Common Fixes

- If `python` is not recognized, install Python from python.org and enable the `Add Python to PATH` option, or use `py`.
- If root `npm install` finishes but the frontend still lacks dependencies, run `npm --prefix frontend install`.
- If `pip` is not recognized, use `python -m pip` instead of plain `pip`.
- If `uvicorn` is not recognized, use `python -m uvicorn app.main:app --reload`.
- If PowerShell activation is blocked, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`.
- If `Activate.ps1` is not found, recreate the environment with `python -m venv .venv`.
- If port `8000` is in use, run `python -m uvicorn app.main:app --reload --port 8001`.
- If port `5173` is in use, check the Vite terminal output for the new frontend URL.
- If spaCy models are missing, the backend falls back automatically to simple keyword extraction.
- If the frontend cannot connect, verify the backend is running and CORS is enabled for `http://127.0.0.1:5173`.
- If the frontend still shows backend errors, restart both terminals after code changes so Vite proxy and FastAPI reload pick up the latest updates.
