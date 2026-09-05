from search.tokenizer import tokenize


class QueryProcessor:
    """Process a user's search query before ranking."""

    def process(self, query: str) -> list[str]:
        if not query:
            return []

        return tokenize(query, remove_stopwords=True)

    def normalize(self, query: str) -> str:
        if not query:
            return ""

        return " ".join(self.process(query))