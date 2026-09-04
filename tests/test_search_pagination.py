import pytest

from search.engine import SearchEngine


def make_engine(document_count=5):
    engine = SearchEngine()
    for document_id in range(document_count):
        engine.add_document(
            document_id,
            "Python document",
            f"https://example.com/{document_id}",
            "",
            "Python content"
        )
    return engine


def test_page_one_returns_first_page():
    results = make_engine().search("python", page=1, limit=2)

    assert len(results) == 2
    assert results[0]["url"] == "https://example.com/0"


def test_page_two_returns_next_results():
    engine = make_engine()

    page_one = engine.search("python", page=1, limit=2)
    page_two = engine.search("python", page=2, limit=2)

    assert len(page_two) == 2
    assert page_one[0]["url"] != page_two[0]["url"]


def test_page_boundary():
    engine = make_engine()

    assert len(engine.search("python", page=1, limit=2)) == 2
    assert len(engine.search("python", page=2, limit=2)) == 2
    assert len(engine.search("python", page=3, limit=2)) == 1


def test_page_beyond_available_results_is_empty():
    assert make_engine().search("python", page=10, limit=2) == []


def test_pagination_metadata():
    metadata = make_engine(10).search_paginated(
        "python",
        page=2,
        limit=3
    )

    assert metadata["total_results"] == 10
    assert metadata["total_pages"] == 4
    assert metadata["page"] == 2
    assert metadata["limit"] == 3
    assert len(metadata["results"]) == 3


def test_invalid_engine_pagination_parameters():
    engine = make_engine()

    with pytest.raises(ValueError):
        engine.search("python", page=0)

    with pytest.raises(ValueError):
        engine.search("python", page=-1)

    with pytest.raises(ValueError):
        engine.search("python", limit=0)