from search.engine import SearchEngine


def test_search_engine_ranks_matching_document_first():
    engine = SearchEngine()

    engine.add_document(
        1,
        "Python Tutorial",
        "https://example.com/python",
        "Python programming tutorial",
        "Learn Python programming"
    )
    engine.add_document(
        2,
        "Java Tutorial",
        "https://example.com/java",
        "Java programming tutorial",
        "Learn Java programming"
    )

    results = engine.search("Python")

    assert results
    assert results[0]["url"] == "https://example.com/python"


def test_search_engine_respects_limit():
    engine = SearchEngine()

    for document_id in range(3):
        engine.add_document(
            document_id,
            "Python document",
            f"https://example.com/{document_id}",
            "",
            "Python content"
        )

    assert len(engine.search("python", limit=2)) == 2