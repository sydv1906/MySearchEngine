import math

from search.tokenizer import tokenize


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

    if document_frequency == 0:
        return 0.0

    return math.log(
        (total_documents + 1)
        / (document_frequency + 1)
    ) + 1


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