from search.snippets import generate_snippet


def test_generate_snippet():
    text = (
        "Python is a programming language. "
        "It is widely used for web development."
    )

    snippet = generate_snippet(text, "python")

    assert "Python" in snippet


def test_no_match_returns_beginning():
    snippet = generate_snippet(
        "Java is a programming language.",
        "python"
    )

    assert snippet.startswith("Java")


def test_multiple_query_terms_find_match():
    snippet = generate_snippet(
        "Python is a programming language.",
        "python programming"
    )

    assert "Python" in snippet


def test_long_content_is_bounded():
    snippet = generate_snippet("word " * 500, "word", max_length=180)

    assert len(snippet) <= 186