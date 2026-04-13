from app.schemas.query_schema import QueryData
from app.utils.text_utils import (
    build_alternate_queries,
    build_primary_query,
    deduplicate_terms,
    determine_focus_terms,
    extract_keywords,
)


class QueryService:
    @staticmethod
    def generate_queries(claim: str) -> QueryData:
        keywords, _method = extract_keywords(claim)
        focus_terms = determine_focus_terms(claim)

        combined_keywords = deduplicate_terms([*keywords, *focus_terms])
        primary_query = build_primary_query(keywords, focus_terms)
        alternate_queries = build_alternate_queries(keywords, focus_terms)

        if not primary_query:
            primary_query = claim.strip().lower()

        if not alternate_queries:
            alternate_queries = [primary_query]

        return QueryData(
            claim=claim.strip(),
            keywords=combined_keywords,
            primary_query=primary_query,
            alternate_queries=alternate_queries,
        )
