import re

from search.tokenizer import tokenize


def generate_snippet(
    text: str,
    query: str,
    max_length: int = 180
) -> str:
    """Return a bounded excerpt centered on the first matching query term."""

    if not text:
        return ""

    if max_length <= 0:
        return ""

    query_terms = tokenize(query)
    match = None

    for term in query_terms:
        match = re.search(
            rf"\b{re.escape(term)}\b",
            text,
            flags=re.IGNORECASE
        )
        if match:
            break

    if match is None:
        return _bounded_start(text, max_length)

    half_window = max(1, (max_length - 6) // 2)
    start = max(0, match.start() - half_window)
    end = min(len(text), match.end() + half_window)

    if start > 0:
        boundary = text.find(" ", start)
        if boundary != -1 and boundary < match.start():
            start = boundary + 1

    if end < len(text):
        boundary = text.rfind(" ", match.end(), end)
        if boundary > match.end():
            end = boundary

    snippet = text[start:end].strip()

    if start > 0:
        snippet = "..." + snippet
    if end < len(text):
        snippet += "..."

    return snippet


def _bounded_start(text: str, max_length: int) -> str:
    if len(text) <= max_length:
        return text

    end = text.rfind(" ", 0, max_length - 3)
    if end <= 0:
        end = max_length - 3

    return text[:end].rstrip() + "..."