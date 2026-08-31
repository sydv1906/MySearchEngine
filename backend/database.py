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
            title TEXT NOT NULL,
            url TEXT NOT NULL UNIQUE,
            description TEXT,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    connection.commit()
    connection.close()


def add_document(title, url, description="", content=""):
    """
    Add a document to the database.
    """
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO documents
        (title, url, description, content)
        VALUES (?, ?, ?, ?)
        """,
        (title, url, description, content)
    )

    connection.commit()

    document_id = cursor.lastrowid

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