import re
from functools import lru_cache
from typing import Iterable, List, Optional, Set, Tuple


BASIC_STOPWORDS: Set[str] = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "been",
    "by",
    "for",
    "from",
    "has",
    "have",
    "in",
    "into",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "their",
    "this",
    "to",
    "used",
    "use",
    "using",
    "was",
    "were",
    "with",
}

RELEVANT_TERMS: Set[str] = {
    "management",
    "treatment",
    "therapy",
    "risk",
    "diagnosis",
    "prevention",
    "stroke",
    "diabetes",
    "insulin",
    "hypertension",
    "infection",
    "asthma",
    "cancer",
    "symptom",
    "condition",
    "disease",
    "drug",
    "medication",
    "clinical",
    "treatment",
}

ACTION_WORDS_TO_SKIP: Set[str] = {
    "manage",
    "treat",
    "therapy",
    "control",
    "increase",
    "increases",
    "diagnose",
    "screen",
    "prevent",
    "improve",
    "reduce",
    "used",
    "use",
    "using",
}


def normalize_text(text: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9\s-]", " ", text.lower())
    return re.sub(r"\s+", " ", cleaned).strip()


def deduplicate_terms(terms: Iterable[str]) -> List[str]:
    seen: Set[str] = set()
    unique: List[str] = []
    for term in terms:
        if term and term not in seen:
            seen.add(term)
            unique.append(term)
    return unique


def tokenize_text(text: str) -> List[str]:
    return re.findall(r"[a-zA-Z]+(?:-[a-zA-Z]+)?|\d+[a-zA-Z]*|[a-zA-Z]+\d*", text)


def is_useful_token(token: str) -> bool:
    if token in ACTION_WORDS_TO_SKIP:
        return False
    return token in RELEVANT_TERMS or len(token) > 2 or bool(re.fullmatch(r"[a-z]\d+", token))


@lru_cache(maxsize=1)
def load_spacy_model():
    try:
        import spacy

        for model_name in ("en_core_sci_sm", "en_core_web_sm"):
            try:
                return spacy.load(model_name)
            except Exception:
                continue
    except Exception:
        return None
    return None


def extract_keywords_with_spacy(text: str) -> Tuple[List[str], Optional[str]]:
    try:
        nlp = load_spacy_model()
        if nlp is None:
            return [], None

        doc = nlp(text)
        keywords: List[str] = []

        for token in doc:
            if token.is_space or token.is_punct:
                continue

            lemma = token.lemma_.lower().strip()
            value = lemma if lemma and lemma != "-pron-" else token.text.lower().strip()

            if value in BASIC_STOPWORDS or not is_useful_token(value):
                continue

            if token.pos_ in {"NOUN", "PROPN", "ADJ"} or value in RELEVANT_TERMS:
                keywords.append(value)

        return deduplicate_terms(keywords), "spacy"
    except Exception:
        # If spaCy loads but fails during processing, never crash the API.
        return [], None


def extract_keywords_with_rules(text: str) -> Tuple[List[str], str]:
    tokens = tokenize_text(text)
    keywords: List[str] = []

    for token in tokens:
        value = token.lower()
        if value in BASIC_STOPWORDS:
            continue
        if not is_useful_token(value):
            continue
        keywords.append(value)

    unique_keywords = deduplicate_terms(keywords)

    if not unique_keywords:
        unique_keywords = deduplicate_terms([token.lower() for token in tokens if len(token) > 1])

    return unique_keywords, "rule_based"


def extract_keywords(text: str) -> Tuple[List[str], str]:
    normalized = normalize_text(text)

    try:
        keywords, method = extract_keywords_with_spacy(normalized)
        if keywords:
            return keywords, method or "spacy"
    except Exception:
        pass

    return extract_keywords_with_rules(normalized)


def determine_focus_terms(claim: str) -> List[str]:
    normalized = normalize_text(claim)
    focus_terms: List[str] = []

    if any(word in normalized for word in ("manage", "treat", "therapy", "control")):
        focus_terms.append("management")
    if any(word in normalized for word in ("risk", "increase", "association", "complication")):
        focus_terms.append("risk")
    if any(word in normalized for word in ("diagnose", "diagnosis", "screen", "symptom")):
        focus_terms.append("diagnosis")
    if any(word in normalized for word in ("prevent", "prevention")):
        focus_terms.append("prevention")

    return deduplicate_terms(focus_terms)


def build_primary_query(keywords: List[str], focus_terms: List[str]) -> str:
    return " ".join(deduplicate_terms([*keywords, *focus_terms])).strip()


def build_alternate_queries(keywords: List[str], focus_terms: List[str]) -> List[str]:
    if not keywords:
        return []

    lead = keywords[0]
    tail = keywords[1:]
    focus = focus_terms[0] if focus_terms else "treatment"
    queries: List[str] = []

    if tail:
        tail_text = " ".join(tail).strip()

        if focus == "management":
            queries.append(f"{lead} for {tail_text} management".strip())
            queries.append(f"{tail_text} {lead} therapy".strip())
            queries.append(f"{lead} and {tail_text} treatment".strip())
        elif focus == "risk":
            queries.append(f"{lead} and {tail_text} risk".strip())
            queries.append(f"{tail_text} in {lead}".strip())
            queries.append(f"{lead} {tail_text} association".strip())
        elif focus == "diagnosis":
            queries.append(f"{lead} {tail_text} diagnosis".strip())
            queries.append(f"{tail_text} diagnosis in {lead}".strip())
            queries.append(f"{lead} and {tail_text} clinical diagnosis".strip())
        else:
            queries.append(f"{lead} for {' '.join(tail + focus_terms)}".strip())
            queries.append(f"{tail_text} {lead} therapy".strip())
            queries.append(f"{lead} and {tail_text} treatment".strip())
    else:
        queries.append(f"{lead} {focus}")
        queries.append(f"{lead} clinical evidence")
        queries.append(f"{lead} medical study")

    cleaned_queries = [re.sub(r"\s+", " ", query).strip() for query in queries if query.strip()]
    return deduplicate_terms(cleaned_queries)[:3]
