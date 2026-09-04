from uuid import uuid4

from backend.database import (
    initialize_database,
    add_crawl_url,
    get_pending_url,
    mark_url_crawled,
    get_crawl_stats,
    get_connection,
    is_url_crawled
)


def test_crawl_queue():
    initialize_database()

    connection = get_connection()
    connection.execute("DELETE FROM crawl_queue")
    connection.commit()
    connection.close()

    url = f"https://example.com/test-day9-{uuid4()}"

    add_crawl_url(url)

    pending = get_pending_url()

    assert pending is not None
    assert pending["url"] == url

    mark_url_crawled(url)

    assert is_url_crawled(url)

    stats = get_crawl_stats()

    assert stats["crawled"] >= 1