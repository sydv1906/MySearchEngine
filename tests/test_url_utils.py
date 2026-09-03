from crawler.url_utils import normalize_url


def test_remove_fragment():
    url = "https://example.com/page#section"

    assert normalize_url(url) == "https://example.com/page"


def test_remove_trailing_slash():
    url = "https://example.com/about/"

    assert normalize_url(url) == "https://example.com/about"


def test_root_slash():
    url = "https://example.com"

    assert normalize_url(url) == "https://example.com/"