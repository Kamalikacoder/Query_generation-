# Evidence Retrieval Module

Complete full-stack project for:

**Factual Hallucination Detection and Correction in LLM-Generated Medical Summaries Using Claim Decomposition and Evidence Retrieval**

This project contains:

- `backend/` FastAPI service running at `http://127.0.0.1:8000`
- `frontend/` React + Vite client running at `http://localhost:5173`

Start the backend first, then start the frontend.

## Folder Structure

```text
backend/
  app/
    __init__.py
    config.py
    main.py
    routes/
      __init__.py
      evidence.py
    schemas/
      __init__.py
      evidence_schema.py
    services/
      __init__.py
      pubmed_service.py
      retrieval_service.py
    utils/
      __init__.py
      query_utils.py
      text_utils.py
  .env.example
  requirements.txt
  README.md

frontend/
  src/
    App.jsx
    main.jsx
    api.js
    components/
      SearchBox.jsx
      ResultCard.jsx
      ErrorMessage.jsx
    styles.css
  index.html
  package.json
  vite.config.js
  .env.example
  README.md
```

## Backend Setup

1. `cd backend`
2. `python -m venv venv`
3. Activate the virtual environment.
   PowerShell: `.\\venv\\Scripts\\Activate.ps1`
   Command Prompt: `venv\\Scripts\\activate`
4. `pip install -r requirements.txt`
5. Create `.env` from `.env.example`
6. `uvicorn app.main:app --reload --port 8000`

Backend URLs:

- App root: `http://127.0.0.1:8000/`
- Health: `http://127.0.0.1:8000/health`
- Docs: `http://127.0.0.1:8000/docs`

## Frontend Setup

1. Open a second terminal
2. `cd frontend`
3. `npm install`
4. Create `.env` from `.env.example`
5. `npm run dev`

Frontend URL:

- `http://localhost:5173`

## API Contract

### POST `http://127.0.0.1:8000/api/v1/retrieve-evidence`

Request body:

```json
{
  "claim": "Antibiotics cure diabetes",
  "top_k": 3
}
```

Success response:

```json
{
  "input_claim": "Antibiotics cure diabetes",
  "search_query": "(Antibiotics cure diabetes) AND (antibiotics AND cure AND diabetes)",
  "retrieved_evidence": [
    {
      "pmid": "12345678",
      "title": "Example article title",
      "abstract": "Abstract text or Abstract not available",
      "authors": ["Jane Doe"],
      "journal": "Example Journal",
      "publication_year": "2024",
      "pubmed_url": "https://pubmed.ncbi.nlm.nih.gov/12345678/"
    }
  ]
}
```

Error response:

```json
{
  "detail": "Claim must not be empty."
}
```

## Notes

- Backend must be started first.
- Frontend uses `VITE_API_BASE_URL=http://127.0.0.1:8000`.
- CORS allows `http://localhost:5173`.
- Empty abstracts fall back to `Abstract not available`.
- Missing authors fall back to an empty list from the backend and a readable message in the UI.
- If PubMed returns no matches, the frontend shows a dedicated no-results state.
