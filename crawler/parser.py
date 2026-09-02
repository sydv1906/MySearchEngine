from urllib.parse import urljoin, urldefrag

from bs4 import BeautifulSoup


def parse_page(html: str, base_url: str):
    """
    Parse HTML and extract useful search information.
    """

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    # Extract title
    title = ""

    if soup.title:
        title = soup.title.get_text(
            strip=True
        )

    # Remove elements that aren't useful
    # for searchable page content.
    for element in soup([
        "script",
        "style",
        "noscript"
    ]):
        element.decompose()

    # Extract visible-ish text
    text = soup.get_text(
        separator=" ",
        strip=True
    )

    # Extract links
    links = set()

    for anchor in soup.find_all("a", href=True):

        href = anchor["href"]

        absolute_url = urljoin(
            base_url,
            href
        )

        # Remove URL fragments
        absolute_url, _ = urldefrag(
            absolute_url
        )

        if absolute_url.startswith(
            ("http://", "https://")
        ):
            links.add(absolute_url)

    return {
        "title": title,
        "text": text,
        "links": list(links)
    }