from search.engine import SearchEngine


def test_search_ignores_stopwords():
    engine = SearchEngine()

    engine.add_document(
        1,
        "Python Programming",
        "https://example.com/python",
        "Learn Python programming language",
        "Python is a programming language"
    )

    results = engine.search("the python programming language")

    assert results
    assert results[0]["title"] == "Python Programming"


def test_search_normalizes_query_punctuation():
    engine = SearchEngine()

    engine.add_document(
        1,
        "Python Guide",
        "https://example.com/python",
        "",
        "Learn Python"
    )

    plain_results = engine.search("python")
    punctuation_results = engine.search("Python!!!")

    assert punctuation_results[0]["url"] == plain_results[0]["url"]