import requests


USER_AGENT = (
    "MySearchEngineBot/0.1 "
    "(educational search engine project)"
)


def fetch_page(url: str, timeout: int = 10):
    """
    Download a web page and return the response.

    Returns:
        requests.Response | None
    """

    headers = {
        "User-Agent": USER_AGENT
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=timeout
        )

        response.raise_for_status()

        return response

    except requests.RequestException as error:
        print(f"[Crawler] Failed to fetch {url}: {error}")

        return None