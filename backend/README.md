# Query Generation Module Backend

## Purpose

This backend accepts a clinical claim, extracts useful medical keywords, generates a PubMed-friendly primary query, and returns alternate search queries as JSON.

## Tech Stack

- Python
- FastAPI
- Pydantic
- spaCy with safe fallback
- Uvicorn

## How to Run

### From Project Root

```powershell
npm run server
```

### PowerShell

```powershell
cd backend
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

### Command Prompt

```cmd
cd backend
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

### Without Activating Virtual Environment

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe run.py
```

### Alternative Safe Run Options

```powershell
cd backend
python run.py
```

Or:

```powershell
cd backend
python -m uvicorn app.main:app --reload
```

## Sample Request

```json
{
  "claim": "Insulin is used to manage diabetes."
}
```

## Sample Response

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

- If `uvicorn` is not recognized, use `python -m uvicorn app.main:app --reload`.
- If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`.
- If Command Prompt activation fails, use `.venv\Scripts\activate.bat`.
- If `Activate.ps1` is not found, create the virtual environment again with `python -m venv .venv`.
- If `python` is not recognized, try `py` instead of `python`.
- If `pip` is not recognized, use `python -m pip install -r requirements.txt`.
- If the spaCy model is missing, the API still works with built-in rule-based fallback logic.
- If port `8000` is in use, run `python -m uvicorn app.main:app --reload --port 8001`.
- If imports fail, make sure you are running commands from inside the `backend` folder.
- If you want the backend and frontend together, run `npm run fullstack` from the project root.
