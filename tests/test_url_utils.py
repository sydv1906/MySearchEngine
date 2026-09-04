from crawler.url_utils import (
    is_same_domain,
    is_valid_url,
    normalize_url
)


def test_remove_fragment():
    url = "https://example.com/page#section"

    assert normalize_url(url) == "https://example.com/page"


def test_remove_trailing_slash():
    url = "https://example.com/about/"

    assert normalize_url(url) == "https://example.com/about"


def test_root_slash():
    url = "https://example.com"

    assert normalize_url(url) == "https://example.com/"


def test_normalize_host_and_default_port():
    assert normalize_url(
        "HTTPS://Example.COM:443/page/?q=python#section"
    ) == "https://example.com/page?q=python"

    assert normalize_url("http://Example.COM:80") == "http://example.com/"


def test_valid_http_urls():
    assert is_valid_url("https://example.com")
    assert is_valid_url("http://example.com")


def test_invalid_url_schemes():
    assert not is_valid_url("ftp://example.com")
    assert not is_valid_url("mailto:test@example.com")
    assert not is_valid_url("javascript:void(0)")
    assert not is_valid_url("https:///missing-host")


def test_same_domain_compares_hostnames():
    assert is_same_domain(
        "https://example.com/about",
        "https://example.com"
    )
    assert not is_same_domain(
        "https://google.com",
        "https://example.com"
    )