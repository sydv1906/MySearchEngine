from backend.main import health_check, search, suggest


def test_suggestions():
    result = suggest("PY")

    assert result["query"] == "py"
    assert len(result["suggestions"]) > 0


def test_empty_suggestions():
    assert suggest("") == {
        "query": "",
        "suggestions": []
    }


def test_unknown_suggestions():
    assert suggest("xyz")["suggestions"] == []


def test_search_includes_query_metadata():
    response = search("python", page=1, limit=10)

    assert response["query"] == "python"
    assert response["query_type"] == "keyword"
    assert response["intent"] == "general"
    assert "total_results" in response
    assert "search_time_ms" in response
    assert response["search_time_ms"] >= 0


def test_health_endpoint_identifies_service():
    response = health_check()

    assert response["status"] == "ok"
    assert response["service"] == "MySearchEngine"