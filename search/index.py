from collections import defaultdict, Counter

from search.tokenizer import tokenize


class InvertedIndex:
    """
    Maps words to the documents that contain them.
    """

    def __init__(self):
        self.index = defaultdict(dict)
        self.documents = {}

    def add_document(self, document_id: int, text: str):
        """
        Add a document to the inverted index.
        """

        tokens = tokenize(text)

        term_counts = Counter(tokens)

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

    def get_document_frequency(self, term: str) -> int:
        """
        Return the number of documents containing the term.
        """

        return len(self.index.get(term, {}))

    def __len__(self):
        """
        Return the number of indexed terms.
        """

        return len(self.index)