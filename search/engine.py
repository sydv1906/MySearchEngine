from search.index import InvertedIndex
from search.ranking import bm25
from search.tokenizer import tokenize


TITLE_BOOST = 2.0
DESCRIPTION_BOOST = 1.25


class SearchEngine:
    """
    Simple search engine using an inverted index and BM25 scoring.
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
        average_document_length = (
            self.index.get_average_document_length()
        )

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

                score = bm25(
                    term_frequency=term_frequency,
                    document_frequency=document_frequency,
                    document_length=document_length,
                    average_document_length=average_document_length,
                    document_count=total_documents
                )

                document = self.documents[document_id]
                if term in tokenize(document["title"]):
                    score *= TITLE_BOOST
                elif term in tokenize(document["description"]):
                    score *= DESCRIPTION_BOOST

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