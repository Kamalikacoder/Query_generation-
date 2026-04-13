# Query Generation Module

A lightweight TypeScript + Express backend with a minimal React UI for converting clinical claims into medical search queries.

## What is included
- `backend/` - full backend structure with Express, validation, and query generation logic
- `src/` - React UI to submit clinical claims and view generated results
- `vite.config.ts` - frontend proxy to backend API during development
- `backend/.env.example` - sample backend environment file

## Backend API

### Health check
- **GET** `/api/health`
- Response:
  ```json
  { "success": true, "message": "backend running" }
  ```

### Generate query
- **POST** `/api/query/generate`
- Request body:
  ```json
  { "claim": "Antibiotics cure diabetes" }
  ```
- Response:
  ```json
  {
    "success": true,
    "message": "Query generated successfully",
    "data": {
      "originalClaim": "Antibiotics cure diabetes",
      "cleanedClaim": "antibiotics cure diabetes",
      "keywords": ["antibiotics", "diabetes"],
      "generatedQuery": "antibiotics diabetes treatment evidence",
      "message": "Query generated successfully"
    }
  }
  ```

## Run locally

1. Install dependencies in the root:
   ```bash
   npm install
   ```

2. Start backend only:
   ```bash
   npm run dev:backend
   ```
   Backend API will run at `http://localhost:4000`.

3. Start frontend only:
   ```bash
   npm run dev:frontend
   ```
   Open the execution page at `http://localhost:5173`.

4. Start both together:
   ```bash
   npm run dev
   ```
   Then use:
   - Frontend UI: `http://localhost:5173`
   - Backend health check: `http://localhost:4000/api/health`

## Expected local behavior

- `http://localhost:5173` shows the Query Generation Module page.
- `http://localhost:4000/api/health` returns the backend status JSON.
- `http://localhost:4000/` is backend root only and returns:
  ```json
  { "success": false, "message": "Route not found" }
  ```

## Notes
- Backend listens on port `4000` by default.
- Frontend dev server is fixed to port `5173`.
- Frontend proxy forwards `/api` requests to the backend.
- The frontend UI is a simple claim form at the Vite app.
- Environment config is stored in `backend/.env` and `backend/.env.example`.
