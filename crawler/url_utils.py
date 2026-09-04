from urllib.parse import urlparse, urlunparse


def is_valid_url(url: str) -> bool:
    """Return whether a URL is an HTTP or HTTPS URL with a hostname."""

    if not isinstance(url, str) or not url.strip():
        return False

    try:
        parsed = urlparse(url.strip())
        if parsed.scheme.lower() not in {"http", "https"}:
            return False

        if not parsed.hostname:
            return False

        parsed.port
        return True
    except ValueError:
        return False


def is_same_domain(url: str, base_url: str) -> bool:
    """Compare URL hostnames without relying on string matching."""

    if not is_valid_url(url) or not is_valid_url(base_url):
        return False

    return urlparse(url).hostname.lower() == urlparse(
        base_url
    ).hostname.lower()


def normalize_url(url: str) -> str:
    """
    Normalize a URL to reduce duplicate URLs.
    """

    url = url.strip()

    parsed = urlparse(url)

    scheme = parsed.scheme.lower()
    hostname = parsed.hostname.lower() if parsed.hostname else ""

    try:
        port = parsed.port
    except ValueError:
        port = None

    if port is not None and not (
        (scheme == "http" and port == 80)
        or (scheme == "https" and port == 443)
    ):
        hostname = f"{hostname}:{port}"

    netloc = hostname

    path = parsed.path

    if not path:
        path = "/"

    # Remove trailing slash except for root
    if path != "/" and path.endswith("/"):
        path = path.rstrip("/")

    return urlunparse(
        (
            scheme,
            netloc,
            path,
            "",
            parsed.query,
            ""
        )
    )