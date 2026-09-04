from collections import Counter, defaultdict

from search.tokenizer import tokenize


class InvertedIndex:
    """
    Maps words to the documents that contain them.
    """

    def __init__(self):
        self.index = defaultdict(Counter)
        self.document_lengths = {}
        self.documents = {}

    def add_document(self, document_id: int, text_or_tokens):
        """
        Add a raw-text or tokenized document to the inverted index.
        """

        tokens = (
            tokenize(text_or_tokens)
            if isinstance(text_or_tokens, str)
            else list(text_or_tokens)
        )

        term_counts = Counter(tokens)

        self.document_lengths[document_id] = len(tokens)
        self.documents[document_id] = {
            "length": len(tokens)
        }

        for term, frequency in term_counts.items():
            self.index[term][document_id] = frequency

    def get_documents(self, term: str):
        """
        Return documents containing a term.
        """

        return self.index.get(term, {})

    def search_term(self, term: str):
        """Return documents containing a term and their frequencies."""

        return dict(self.index.get(term, {}))

    def get_document_frequency(self, term: str) -> int:
        """
        Return the number of documents containing the term.
        """

        return len(self.index.get(term, {}))

    def document_frequency(self, term: str) -> int:
        """Return the number of documents containing a term."""

        return len(self.index.get(term, {}))

    def term_frequency(self, term: str, document_id: int) -> int:
        """Return the frequency of a term in a document."""

        return self.index.get(term, {}).get(document_id, 0)

    def get_document_length(self, document_id: int) -> int:
        """Return the number of indexed tokens in a document."""

        return self.document_lengths.get(document_id, 0)

    def get_document_count(self) -> int:
        """Return the number of indexed documents."""

        return len(self.document_lengths)

    def get_average_document_length(self) -> float:
        """Return the average number of indexed tokens per document."""

        if not self.document_lengths:
            return 0.0

        return sum(self.document_lengths.values()) / len(
            self.document_lengths
        )

    def __len__(self):
        """
        Return the number of indexed terms.
        """

        return len(self.index)