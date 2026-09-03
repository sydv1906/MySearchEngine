from backend.database import (
    initialize_database,
    add_crawl_url,
    get_pending_url,
    mark_url_crawled,
    get_crawl_stats
)


def test_crawl_queue():
    initialize_database()

    url = "https://example.com/test-day7"

    add_crawl_url(url)

    pending = get_pending_url()

    assert pending is not None
    assert pending["url"] == url

    mark_url_crawled(url)

    stats = get_crawl_stats()

    assert stats["crawled"] >= 1