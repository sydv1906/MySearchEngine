import re


STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "has",
    "he",
    "in",
    "is",
    "it",
    "its",
    "of",
    "on",
    "that",
    "the",
    "this",
    "to",
    "was",
    "were",
    "will",
    "with",
}


def tokenize(text: str) -> list[str]:
    """
    Convert text into normalized search tokens.
    """

    if not text:
        return []

    text = text.lower()

    tokens = re.findall(r"\b[a-z0-9]+\b", text)

    tokens = [
        token
        for token in tokens
        if token not in STOP_WORDS
    ]

    return tokens