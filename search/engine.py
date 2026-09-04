from search.index import InvertedIndex
from search.ranking import tf_idf
from search.tokenizer import tokenize


class SearchEngine:
    """
    Simple search engine using an inverted index
    and TF-IDF-style scoring.
    """

    def __init__(self):
        self.index = InvertedIndex()
        self.documents = {}

    def add_document(
        self,
        document_id: int,
        title: str,
        url: str,
        description: str,
        content: str
    ):
        """
        Add a document to the search engine.
        """

        combined_text = " ".join([
            title,
            description,
            content
        ])

        self.documents[document_id] = {
            "title": title,
            "url": url,
            "description": description,
            "content": content
        }

        self.index.add_document(
            document_id,
            combined_text
        )

    def search(self, query: str, limit: int = 10):
        """
        Search indexed documents and rank them.
        """

        query_tokens = tokenize(query)

        if not query_tokens:
            return []

        scores = {}

        total_documents = self.index.get_document_count()

        for term in query_tokens:

            matching_documents = self.index.search_term(term)
            document_frequency = self.index.document_frequency(term)

            if document_frequency == 0:
                continue

            for document_id, term_frequency in (
                matching_documents.items()
            ):
                document_length = self.index.get_document_length(
                    document_id
                )

                score = tf_idf(
                    term_frequency,
                    document_length,
                    total_documents,
                    document_frequency
                )

                scores[document_id] = (
                    scores.get(document_id, 0.0)
                    + score
                )

        ranked_results = sorted(
            scores.items(),
            key=lambda item: item[1],
            reverse=True
        )

        results = []

        for document_id, score in ranked_results[:limit]:

            document = self.documents[document_id]

            results.append({
                "title": document["title"],
                "url": document["url"],
                "description": document["description"],
                "score": round(score, 6)
            })

        return results