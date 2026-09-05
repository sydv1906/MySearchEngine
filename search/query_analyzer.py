from search.tokenizer import tokenize


class QueryAnalyzer:
    """Analyze user queries before they reach the search engine."""

    QUESTION_WORDS = {
        "who",
        "what",
        "when",
        "where",
        "why",
        "how",
    }

    INFORMATIONAL_WORDS = {
        "who",
        "what",
        "when",
        "where",
        "why",
        "how",
        "explain",
        "meaning",
        "definition",
    }

    NAVIGATIONAL_WORDS = {
        "login",
        "website",
        "official",
        "homepage",
    }

    TRANSACTIONAL_WORDS = {
        "buy",
        "price",
        "cost",
        "purchase",
        "download",
    }

    def analyze(self, query: str) -> dict:
        if not query or not query.strip():
            return {
                "original_query": query or "",
                "tokens": [],
                "token_count": 0,
                "query_type": "empty",
                "intent": "unknown",
            }

        tokens = tokenize(query)

        return {
            "original_query": query,
            "tokens": tokens,
            "token_count": len(tokens),
            "query_type": self.detect_query_type(query, tokens),
            "intent": self.detect_intent(tokens),
        }

    def detect_query_type(self, query: str, tokens: list[str]) -> str:
        if not tokens:
            return "empty"

        words = query.strip().lower().split()
        first_word = words[0] if words else ""

        if first_word in self.QUESTION_WORDS:
            return "question"

        if len(tokens) <= 2:
            return "keyword"

        return "general"

    def detect_intent(self, tokens: list[str]) -> str:
        token_set = set(tokens)

        if token_set & self.INFORMATIONAL_WORDS:
            return "informational"

        if token_set & self.NAVIGATIONAL_WORDS:
            return "navigational"

        if token_set & self.TRANSACTIONAL_WORDS:
            return "transactional"

        return "general"