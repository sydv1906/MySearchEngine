from search.tokenizer import tokenize


def test_tokenize_lowercase():
    assert tokenize("Python") == ["python"]


def test_stop_words_removed():
    assert tokenize("Python is a language") == [
        "python",
        "language"
    ]