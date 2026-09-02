from collections import deque
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

from crawler.fetcher import fetch_page
from crawler.parser import parse_page
import time


class WebCrawler:

    def __init__(
        self,
        max_pages: int = 10,
        same_domain: bool = True,
        delay: float = 0.0
    ):
        self.max_pages = max_pages
        self.same_domain = same_domain
        self.delay = delay
        self.visited = set()
        self.robots = None

    def setup_robots(self, start_url: str):
        parsed = urlparse(start_url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

        try:
            self.robots = RobotFileParser(robots_url)
            self.robots.read()
        except Exception as error:
            print(f"[Crawler] Could not read robots.txt: {error}")
            self.robots = None

    def allowed_by_robots(self, url: str) -> bool:
        if self.robots is None:
            return True

        return self.robots.can_fetch("MySearchEngineBot", url)

    def is_allowed_domain(
        self,
        url: str,
        base_domain: str
    ) -> bool:

        if not self.same_domain:
            return True

        parsed = urlparse(url)

        return parsed.netloc == base_domain

    def crawl(self, start_url: str):

        self.setup_robots(start_url)

        queue = deque([start_url])

        start_domain = urlparse(start_url).netloc
        results = []

        while queue and len(results) < self.max_pages:
            current_url = queue.popleft()

            if current_url in self.visited:
                continue

            self.visited.add(current_url)

            if not self.allowed_by_robots(current_url):
                print("[Crawler] Blocked by robots.txt:", current_url)
                continue

            print(f"[Crawler] Crawling: {current_url}")

            response = fetch_page(current_url)
            time.sleep(self.delay)  # Respect crawl delay if set

            if response is None:
                continue

            content_type = response.headers.get("content-type", "").lower()

            if "text/html" not in content_type:
                print("[Crawler] Skipping non-HTML page:", current_url)
                continue

            page = parse_page(response.text, current_url)

            result = {
                "url": current_url,
                "title": page["title"],
                "content": page["text"],
                "links": page["links"]
            }

            results.append(result)

            for link in page["links"]:
                if link in self.visited:
                    continue

                if not self.is_allowed_domain(link, start_domain):
                    continue

                if link not in queue:
                    queue.append(link)

        return results
