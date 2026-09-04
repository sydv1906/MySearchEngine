from types import SimpleNamespace

from crawler import crawler as crawler_module
from crawler.crawler import WebCrawler


def run_crawler(monkeypatch, pages, max_pages=10, max_urls=100):
    frontier = []
    statuses = {}
    page_map = iter(pages)

    monkeypatch.setattr(crawler_module, "initialize_database", lambda: None)
    monkeypatch.setattr(
        WebCrawler,
        "setup_robots",
        lambda self, start_url: setattr(self, "robots", None)
    )
    monkeypatch.setattr(
        crawler_module,
        "add_crawl_url",
        lambda url: frontier.append(url) if url not in frontier else None
    )
    monkeypatch.setattr(
        crawler_module,
        "get_pending_url",
        lambda: (
            {"url": frontier.pop(0)}
            if frontier else None
        )
    )
    monkeypatch.setattr(
        crawler_module,
        "mark_url_crawling",
        lambda url: statuses.__setitem__(url, "crawling")
    )
    monkeypatch.setattr(
        crawler_module,
        "mark_url_crawled",
        lambda url: statuses.__setitem__(url, "crawled")
    )
    monkeypatch.setattr(
        crawler_module,
        "mark_url_failed",
        lambda url: statuses.__setitem__(url, "failed")
    )
    monkeypatch.setattr(
        crawler_module,
        "is_url_crawled",
        lambda url: statuses.get(url) == "crawled"
    )
    monkeypatch.setattr(crawler_module, "fetch_page", lambda url: SimpleNamespace(
        headers={"content-type": "text/html"},
        text="<html></html>"
    ))
    monkeypatch.setattr(
        crawler_module,
        "parse_page",
        lambda html, url: next(page_map)
    )

    crawler = WebCrawler(
        max_pages=max_pages,
        max_urls=max_urls,
        same_domain=True
    )
    return crawler.crawl("https://example.com")


def test_max_pages_is_enforced(monkeypatch):
    pages = [
        {"title": "One", "text": "one", "links": [
            "https://example.com/two",
            "https://example.com/three"
        ]},
        {"title": "Two", "text": "two", "links": [
            "https://example.com/three"
        ]},
        {"title": "Three", "text": "three", "links": []}
    ]

    results = run_crawler(monkeypatch, pages, max_pages=2)

    assert len(results) == 2


def test_frontier_filters_domains_invalid_urls_and_duplicates(monkeypatch):
    pages = [{
        "title": "One",
        "text": "one",
        "links": [
            "https://example.com/page",
            "https://example.com/page#section",
            "https://google.com/",
            "mailto:test@example.com",
            "javascript:void(0)",
            "ftp://example.com/file"
        ]
    }]

    results = run_crawler(monkeypatch, pages, max_pages=1, max_urls=10)

    assert len(results) == 1