# Query Generation Module Frontend

## Purpose

This frontend provides a simple React interface for entering a clinical claim and viewing generated keywords, a primary query, and alternate queries from the FastAPI backend.

## How to Run

### From Project Root

```powershell
npm run client
```

```bash
cd frontend
npm install
npm run dev
```

## Expected URL

Open:

```text
http://127.0.0.1:5173
```

## Sample Input

```json
{
  "claim": "Hypertension increases the risk of stroke."
}
```

## Common Fixes

- Make sure the backend is running at `http://127.0.0.1:8000`.
- If you see a CORS error, restart the backend and confirm it includes CORS middleware.
- If the page shows `Failed to fetch`, verify the backend is running before starting the frontend.
- If the page shows a backend request error, open `http://127.0.0.1:8000/docs` and test `POST /generate-query`.
- If port `5173` is in use, Vite may choose another port automatically. Check the terminal output.
- If `npm` is not recognized, reinstall Node.js and reopen the terminal.
- If you want frontend and backend together, run `npm run fullstack` from the project root.
