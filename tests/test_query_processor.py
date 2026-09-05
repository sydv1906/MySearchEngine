from search.query_processor import QueryProcessor


def test_query_processing():
    processor = QueryProcessor()

    result = processor.process(
        "Python is a powerful programming language"
    )

    assert "python" in result
    assert "programming" in result
    assert "language" in result
    assert "is" not in result
    assert "a" not in result


def test_query_normalization():
    processor = QueryProcessor()

    assert processor.normalize("Python Programming!!!") == (
        "python programming"
    )


def test_empty_query():
    processor = QueryProcessor()

    assert processor.process("") == []
    assert processor.normalize("") == ""