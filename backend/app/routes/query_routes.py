from fastapi import APIRouter

from app.schemas.query_schema import QueryRequest, QueryResponse
from app.services.query_service import QueryService


router = APIRouter(tags=["query"])


@router.post("/generate-query", response_model=QueryResponse)
@router.post("/api/generate-query", response_model=QueryResponse, include_in_schema=False)
def generate_query(payload: QueryRequest) -> QueryResponse:
    result = QueryService.generate_queries(payload.claim)
    return QueryResponse(
        success=True,
        message="Query generated successfully",
        data=result,
    )
