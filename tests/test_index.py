from search.index import InvertedIndex


def test_document_indexing():
    index = InvertedIndex()

    index.add_document(
        1,
        "Python programming language"
    )

    assert 1 in index.get_documents("python")
    assert 1 in index.get_documents("programming")


def test_document_frequency():
    index = InvertedIndex()

    index.add_document(1, ["python", "programming"])
    index.add_document(2, ["python", "web"])

    assert index.document_frequency("python") == 2
    assert index.get_document_count() == 2


def test_term_frequency():
    index = InvertedIndex()

    index.add_document(1, ["python", "python", "web"])

    assert index.term_frequency("python", 1) == 2


def test_document_length():
    index = InvertedIndex()

    index.add_document(1, ["python", "web", "development"])

    assert index.get_document_length(1) == 3