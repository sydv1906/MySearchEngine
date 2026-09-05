import re


STOPWORDS = {
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
    "these",
    "those",
    "or",
    "but",
}


STOP_WORDS = STOPWORDS


def normalize_text(text: str) -> str:
    """Normalize case, punctuation, and whitespace before tokenization."""

    if not text:
        return ""

    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def tokenize(
    text: str,
    remove_stopwords: bool = True
) -> list[str]:
    """
    Convert text into normalized search tokens.
    """

    text = normalize_text(text)

    if not text:
        return []

    tokens = text.split()

    if remove_stopwords:
        tokens = [
            token
            for token in tokens
            if token not in STOPWORDS
        ]

    return tokens