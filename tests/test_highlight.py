from search.highlight import highlight_terms


def test_highlight_terms():
    result = highlight_terms("Python is powerful", "python")

    assert "<strong>Python</strong>" in result


def test_highlight_case_insensitive():
    result = highlight_terms("PYTHON is powerful", "python")

    assert "<strong>PYTHON</strong>" in result


def test_highlight_escapes_untrusted_text():
    result = highlight_terms("<script>python</script>", "python")

    assert "<script>" not in result
    assert "&lt;script&gt;" in result