import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from crawler.crawler import WebCrawler


crawler = WebCrawler(
    max_pages=5,
    same_domain=True
)


results = crawler.crawl(
    "https://example.com"
)


print()
print("========== CRAWL COMPLETE ==========")
print("Pages crawled:", len(results))
print()


for page in results:

    print("Title:", page["title"])
    print("URL:", page["url"])
    print("Links:", len(page["links"]))
    print("-" * 50)