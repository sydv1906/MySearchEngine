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
    assert "snippet" in results[0]
    assert "matched_terms" in results[0]


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


def test_bm25_search_ranking():
    engine = SearchEngine()

    engine.add_document(
        1,
        "Python Programming",
        "https://example.com/python",
        "Python programming",
        "Python Python Python programming"
    )
    engine.add_document(
        2,
        "Java Programming",
        "https://example.com/java",
        "Programming language",
        "Java programming language"
    )

    results = engine.search("python")

    assert results
    assert results[0]["url"] == "https://example.com/python"

    multi_term_results = engine.search("python programming")
    assert set(multi_term_results[0]["matched_terms"]) == {
        "python",
        "programming"
    }


def test_title_match_receives_a_ranking_boost():
    engine = SearchEngine()

    engine.add_document(
        1,
        "Python Guide",
        "https://example.com/title-match",
        "A guide",
        "Learn programming"
    )
    engine.add_document(
        2,
        "Programming Guide",
        "https://example.com/content-match",
        "A guide",
        "Learn Python"
    )

    results = engine.search("python")

    assert results[0]["url"] == "https://example.com/title-match"