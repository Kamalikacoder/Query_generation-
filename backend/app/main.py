import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.query_routes import router as query_router
from app.schemas.query_schema import HealthResponse, RootResponse


app = FastAPI(
    title="Query Generation Module",
    version="1.0.0",
    description="Convert clinical claims into PubMed-friendly queries",
)


def _get_allowed_origins() -> list[str]:
    configured = os.getenv("ALLOWED_ORIGINS", "").strip()
    if configured:
        return [origin.strip() for origin in configured.split(",") if origin.strip()]

    frontend_url = os.getenv("FRONTEND_URL", "").strip()
    default_origins = ["http://127.0.0.1:5173", "http://localhost:5173"]

    if frontend_url and frontend_url not in default_origins:
        default_origins.append(frontend_url)

    return default_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=_get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=RootResponse)
def root() -> RootResponse:
    return RootResponse(
        module="Query Generation Module Backend",
        status="active",
        purpose="Convert clinical claims into PubMed-friendly queries",
        version="1.0.0",
    )


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="healthy", service="Query Generation Module Backend")


@app.get("/api/health", response_model=HealthResponse)
def api_health() -> HealthResponse:
    return HealthResponse(status="healthy", service="Query Generation Module Backend")


app.include_router(query_router)
