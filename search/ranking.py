import math

from search.tokenizer import tokenize


def bm25(
    term_frequency: int,
    document_frequency: int,
    document_length: int,
    average_document_length: float,
    document_count: int,
    k1: float = 1.5,
    b: float = 0.75
) -> float:
    """Calculate a BM25 relevance score for one term and document."""

    if (
        document_count == 0
        or document_frequency == 0
        or average_document_length == 0
        or term_frequency == 0
    ):
        return 0.0

    inverse_document_frequency = math.log(
        1 + (
            (document_count - document_frequency + 0.5)
            / (document_frequency + 0.5)
        )
    )

    numerator = term_frequency * (k1 + 1)
    denominator = term_frequency + k1 * (
        1 - b
        + b * (document_length / average_document_length)
    )

    return inverse_document_frequency * (numerator / denominator)


def tf(term_frequency: int, document_length: int) -> float:
    """Calculate normalized term frequency."""

    if document_length == 0:
        return 0.0

    return term_frequency / document_length


def idf(document_count: int, document_frequency: int) -> float:
    """Calculate smoothed inverse document frequency."""

    if document_frequency == 0:
        return 0.0

    return math.log(
        (document_count + 1)
        / (document_frequency + 1)
    ) + 1


def tf_idf(
    term_frequency: int,
    document_length: int,
    document_count: int,
    document_frequency: int
) -> float:
    """Calculate a normalized TF-IDF score."""

    return tf(term_frequency, document_length) * idf(
        document_count,
        document_frequency
    )


def calculate_tf(term: str, document_text: str) -> float:
    """
    Calculate term frequency.
    """

    tokens = tokenize(document_text)

    if not tokens:
        return 0.0

    term_count = tokens.count(term)

    return term_count / len(tokens)


def calculate_idf(
    document_frequency: int,
    total_documents: int
) -> float:
    """
    Calculate inverse document frequency.
    """

    return idf(total_documents, document_frequency)


def calculate_tfidf(
    term: str,
    document_text: str,
    document_frequency: int,
    total_documents: int
) -> float:
    """
    Calculate TF-IDF score for a term.
    """

    tf = calculate_tf(
        term,
        document_text
    )

    idf = calculate_idf(
        document_frequency,
        total_documents
    )

    return tf * idf