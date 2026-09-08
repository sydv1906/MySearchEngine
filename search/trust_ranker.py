from datetime import datetime, timezone
from urllib.parse import urlparse


class TrustRanker:
    """Calculate measurable source-quality signals for search results."""

    HIGH_AUTHORITY_DOMAINS = {
        "wikipedia.org",
        "github.com",
        "python.org",
        "mozilla.org",
        "microsoft.com",
        "mit.edu",
        "stanford.edu",
        "harvard.edu",
        "nist.gov",
        "cisa.gov",
        "nasa.gov",
        "who.int",
        "un.org",
    }

    EDUCATIONAL_TLDS = {".edu", ".ac.uk", ".ac.in"}
    GOVERNMENT_TLDS = {".gov", ".gov.in"}

    def domain(self, url: str) -> str:
        try:
            hostname = urlparse(url).hostname or ""
            hostname = hostname.lower()
            if hostname.startswith("www."):
                hostname = hostname[4:]
            return hostname
        except (TypeError, ValueError):
            return ""

    def authority_score(self, url: str) -> float:
        domain = self.domain(url)

        if not domain:
            return 0.0

        if any(
            domain == authority_domain
            or domain.endswith("." + authority_domain)
            for authority_domain in self.HIGH_AUTHORITY_DOMAINS
        ):
            return 1.0

        if any(domain.endswith(tld) for tld in self.EDUCATIONAL_TLDS):
            return 0.9

        if any(domain.endswith(tld) for tld in self.GOVERNMENT_TLDS):
            return 0.95

        return 0.5

    def freshness_score(self, crawled_at=None) -> float:
        if not crawled_at:
            return 0.5

        try:
            if isinstance(crawled_at, str):
                crawled_at = datetime.fromisoformat(
                    crawled_at.replace("Z", "+00:00")
                )

            if crawled_at.tzinfo is None:
                crawled_at = crawled_at.replace(tzinfo=timezone.utc)

            age_days = max(
                (datetime.now(timezone.utc) - crawled_at).days,
                0
            )

            if age_days <= 7:
                return 1.0
            if age_days <= 30:
                return 0.9
            if age_days <= 90:
                return 0.75
            if age_days <= 365:
                return 0.6
            return 0.4
        except (ValueError, TypeError, AttributeError):
            return 0.5

    def calculate(self, url: str, crawled_at=None) -> dict:
        authority = self.authority_score(url)
        freshness = self.freshness_score(crawled_at)
        trust_score = authority * 0.7 + freshness * 0.3

        return {
            "authority": round(authority, 4),
            "freshness": round(freshness, 4),
            "trust_score": round(trust_score, 4),
        }


def trust_reasons(
    authority_score: float,
    freshness_score: float
) -> list[str]:
    """Return concise explanations for the source-quality signals."""

    reasons = []

    if authority_score >= 0.9:
        reasons.append("High-authority domain")

    if freshness_score >= 0.9:
        reasons.append("Recently crawled")

    if not reasons:
        reasons.append("Standard source-quality signals")

    return reasons