from typing import List

from pydantic import BaseModel, Field, field_validator


class QueryRequest(BaseModel):
    claim: str = Field(..., description="Atomic clinical claim to convert into search queries")

    @field_validator("claim")
    @classmethod
    def validate_claim(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Claim cannot be empty")
        return cleaned


class QueryData(BaseModel):
    claim: str
    keywords: List[str]
    primary_query: str
    alternate_queries: List[str]


class QueryResponse(BaseModel):
    success: bool
    message: str
    data: QueryData


class HealthResponse(BaseModel):
    status: str
    service: str


class RootResponse(BaseModel):
    module: str
    status: str
    purpose: str
    version: str
