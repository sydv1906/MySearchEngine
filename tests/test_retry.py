from backend.database import (
    initialize_database,
    add_crawl_url,
    mark_url_failed,
    get_pending_url,
    retry_failed_urls
)


def test_retry_failed_url():
    initialize_database()

    url = "https://example.com/retry-test"

    add_crawl_url(url)

    # Move it from pending → failed
    mark_url_failed(url)

    # Move failed → pending
    retry_failed_urls(max_retries=3)

    pending = get_pending_url()

    assert pending is not None