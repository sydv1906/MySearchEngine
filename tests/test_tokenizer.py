from search.tokenizer import normalize_text, tokenize


def test_tokenize_lowercase():
    assert tokenize("Python") == ["python"]


def test_stop_words_removed():
    assert tokenize("Python is a language") == [
        "python",
        "language"
    ]


def test_normalize_text_removes_punctuation():
    assert normalize_text("Python Programming!!!") == (
        "python programming"
    )


def test_tokenize_can_keep_stop_words():
    assert tokenize("Python is a language", remove_stopwords=False) == [
        "python",
        "is",
        "a",
        "language"
    ]