from backend.database import get_crawl_stats
from backend.main import crawl_website


def test_crawl_rejects_invalid_url():
    try:
        crawl_website("ftp://example.com")
    except Exception as error:
        assert getattr(error, "status_code", None) == 400
    else:
        raise AssertionError("Invalid crawl URL was accepted")


def test_crawl_stats_include_document_count():
    stats = get_crawl_stats()

    assert "documents" in stats