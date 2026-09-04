from search.ranking import bm25


def test_bm25_positive():
    score = bm25(
        term_frequency=3,
        document_frequency=2,
        document_length=100,
        average_document_length=100,
        document_count=10
    )

    assert score > 0


def test_bm25_zero_frequency():
    score = bm25(
        term_frequency=0,
        document_frequency=2,
        document_length=100,
        average_document_length=100,
        document_count=10
    )

    assert score == 0


def test_bm25_empty_collection():
    score = bm25(
        term_frequency=1,
        document_frequency=1,
        document_length=100,
        average_document_length=0,
        document_count=0
    )

    assert score == 0