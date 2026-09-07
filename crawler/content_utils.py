import hashlib


def normalize_content(text: str) -> str:
    """Normalize content for stable duplicate detection."""

    if not text:
        return ""

    return " ".join(text.lower().split())


def content_hash(text: str) -> str:
    """Return a stable SHA-256 hash of normalized content."""

    normalized = normalize_content(text)

    return hashlib.sha256(
        normalized.encode("utf-8")
    ).hexdigest()