import html
import re

from search.tokenizer import tokenize


def highlight_terms(text: str, query: str) -> str:
    """Return escaped text with case-preserving matched terms wrapped safely."""

    if not text:
        return ""

    terms = tokenize(query)
    if not terms:
        return html.escape(text)

    pattern = re.compile(
        r"\b(?:" + "|".join(re.escape(term) for term in terms) + r")\b",
        flags=re.IGNORECASE
    )

    parts = []
    cursor = 0
    for match in pattern.finditer(text):
        parts.append(html.escape(text[cursor:match.start()]))
        parts.append(
            "<strong>"
            + html.escape(match.group(0))
            + "</strong>"
        )
        cursor = match.end()

    parts.append(html.escape(text[cursor:]))
    return "".join(parts)