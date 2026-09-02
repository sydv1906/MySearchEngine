from crawler.parser import parse_page


def test_parse_page():

    html = """
    <html>
        <head>
            <title>Test Page</title>
        </head>

        <body>
            <h1>Hello World</h1>
            <p>This is a test page.</p>

            <a href="/about">
                About
            </a>
        </body>
    </html>
    """

    result = parse_page(
        html,
        "https://example.com"
    )

    assert result["title"] == "Test Page"

    assert "Hello World" in result["text"]

    assert (
        "https://example.com/about"
        in result["links"]
    )