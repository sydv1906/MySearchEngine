import sqlite3
from pathlib import Path


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Database directory
DATA_DIR = BASE_DIR / "data"

# Create data directory if it doesn't exist
DATA_DIR.mkdir(exist_ok=True)

# Database file
DATABASE_PATH = DATA_DIR / "search_engine.db"


def get_connection():
    """
    Create and return a connection to the SQLite database.
    """
    connection = sqlite3.connect(DATABASE_PATH)

    # Allows rows to behave like dictionaries
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    """
    Create the documents table if it does not already exist.
    """
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL DEFAULT '',
        url TEXT UNIQUE NOT NULL,
        description TEXT NOT NULL DEFAULT '',
        content TEXT NOT NULL DEFAULT '',
        status TEXT NOT NULL DEFAULT 'pending',
        retry_count INTEGER NOT NULL DEFAULT 0,
        discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    document_columns = {
        row[1]
        for row in cursor.execute("PRAGMA table_info(documents)")
    }

    missing_document_columns = {
        "title": "TEXT NOT NULL DEFAULT ''",
        "description": "TEXT NOT NULL DEFAULT ''",
        "content": "TEXT NOT NULL DEFAULT ''"
    }

    for column, definition in missing_document_columns.items():
        if column not in document_columns:
            cursor.execute(
                f"ALTER TABLE documents ADD COLUMN {column} {definition}"
            )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS crawl_queue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            retry_count INTEGER NOT NULL DEFAULT 0,
            discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            crawled_at TIMESTAMP
        )
        """
    )

    connection.commit()
    connection.close()

def add_crawl_url(url: str):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
            INSERT INTO crawl_queue
        (url, status)
        VALUES (?, 'pending')
            ON CONFLICT(url) DO UPDATE SET
                status = 'pending',
                retry_count = 0,
                crawled_at = NULL
        """,
        (url,)
    )

    connection.commit()
    connection.close()


def get_pending_url():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM crawl_queue
        WHERE status = 'pending'
        ORDER BY id ASC
        LIMIT 1
        """
    )

    row = cursor.fetchone()
    connection.close()

    return row

def mark_url_crawling(url: str):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE crawl_queue
        SET status = 'crawling'
        WHERE url = ?
        """,
        (url,)
    )

    connection.commit()
    connection.close()

def mark_url_crawled(url: str):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE crawl_queue
        SET status = 'crawled',
            crawled_at = CURRENT_TIMESTAMP
        WHERE url = ?
        """,
        (url,)
    )

    connection.commit()
    connection.close()

def mark_url_failed(url: str):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE crawl_queue
        SET status = 'failed',
            retry_count = retry_count + 1
        WHERE url = ?
        """,
        (url,)
    )

    connection.commit()
    connection.close()


def retry_failed_urls(max_retries: int = 3):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE crawl_queue
        SET status = 'pending'
        WHERE status = 'failed'
        AND retry_count < ?
        """,
        (max_retries,)
    )

    connection.commit()
    connection.close()

def get_crawl_stats():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT status, COUNT(*) AS count
        FROM crawl_queue
        GROUP BY status
        """
    )

    rows = cursor.fetchall()
    connection.close()

    stats = {
        "pending": 0,
        "crawling": 0,
        "crawled": 0,
        "failed": 0
    }

    for row in rows:
        stats[row["status"]] = row["count"]

    stats["total"] = sum(stats.values())

    return stats

def add_document(
    title: str,
    url: str,
    description: str = "",
    content: str = ""
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        "SELECT id FROM documents WHERE url = ?",
        (url,)
    )

    existing = cursor.fetchone()

    if existing:
        connection.close()

        return existing["id"]

    cursor.execute(
        """
        INSERT INTO documents
        (title, url, description, content)
        VALUES (?, ?, ?, ?)
        """,
        (
            title,
            url,
            description,
            content
        )
    )

    document_id = cursor.lastrowid

    connection.commit()

    connection.close()

    return document_id


def search_documents(query):
    """
    Search documents using SQLite text matching.
    """
    connection = get_connection()

    cursor = connection.cursor()

    search_pattern = f"%{query}%"

    cursor.execute(
        """
        SELECT id, title, url, description, content
        FROM documents
        WHERE title LIKE ?
           OR description LIKE ?
           OR content LIKE ?
        ORDER BY id DESC
        """,
        (search_pattern, search_pattern, search_pattern)
    )

    rows = cursor.fetchall()

    connection.close()

    return [dict(row) for row in rows]


def get_document_count():
    """
    Return the total number of documents in the database.
    """
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM documents")

    count = cursor.fetchone()[0]

    connection.close()

    return count


def get_all_documents():
    """
    Return all documents from the database.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, title, url, description, content
        FROM documents
        ORDER BY id
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return [dict(row) for row in rows]