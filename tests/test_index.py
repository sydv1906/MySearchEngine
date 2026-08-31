from search.index import InvertedIndex


def test_document_indexing():
    index = InvertedIndex()

    index.add_document(
        1,
        "Python programming language"
    )

    assert 1 in index.get_documents("python")
    assert 1 in index.get_documents("programming")