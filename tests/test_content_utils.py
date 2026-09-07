from crawler.content_utils import content_hash, normalize_content
from backend.database import add_document, initialize_database


def test_normalize_content():
    assert normalize_content("  Hello    WORLD  ") == "hello world"


def test_same_content_same_hash():
    assert content_hash("Hello World") == content_hash(
        "  hello   world "
    )


def test_different_content_different_hash():
    assert content_hash("Hello World") != content_hash("Goodbye World")


def test_database_deduplicates_content():
    initialize_database()

    first_id = add_document(
        title="First",
        url="https://example.com/content-first",
        content="Unique duplicate test content"
    )
    second_id = add_document(
        title="Second",
        url="https://example.com/content-second",
        content="  unique   duplicate test content  "
    )

    assert second_id == first_id


def test_database_deduplicates_url():
    initialize_database()

    first_id = add_document(
        title="First URL",
        url="https://example.com/url-duplicate",
        content="First URL content"
    )
    second_id = add_document(
        title="Updated URL",
        url="https://example.com/url-duplicate",
        content="Different URL content"
    )

    assert second_id == first_id