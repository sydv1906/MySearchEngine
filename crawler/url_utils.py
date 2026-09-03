from urllib.parse import urlparse, urlunparse


def normalize_url(url: str) -> str:
    """
    Normalize a URL to reduce duplicate URLs.
    """

    url = url.strip()

    parsed = urlparse(url)

    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()

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