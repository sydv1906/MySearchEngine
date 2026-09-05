from search.query_analyzer import QueryAnalyzer


def test_keyword_query():
    result = QueryAnalyzer().analyze("python")

    assert result["query_type"] == "keyword"
    assert result["intent"] == "general"
    assert "python" in result["tokens"]


def test_question_query():
    result = QueryAnalyzer().analyze("how does python work")

    assert result["query_type"] == "question"
    assert result["intent"] == "informational"


def test_navigational_query():
    result = QueryAnalyzer().analyze("python official website")

    assert result["intent"] == "navigational"


def test_transactional_query():
    result = QueryAnalyzer().analyze("buy laptop")

    assert result["intent"] == "transactional"


def test_empty_query():
    result = QueryAnalyzer().analyze("")

    assert result["query_type"] == "empty"
    assert result["intent"] == "unknown"
    assert result["tokens"] == []