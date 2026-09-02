from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from crawler.crawler import WebCrawler

from backend.database import (
    initialize_database,
    add_document,
    get_document_count,
    get_all_documents
)

from search.engine import SearchEngine


app = FastAPI(
    title="MySearchEngine API",
    description="Backend API for MySearchEngine",
    version="0.3.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


initialize_database()

search_engine = SearchEngine()


def load_search_index():
    """
    Load all database documents into the search index.
    """

    documents = get_all_documents()

    for document in documents:
        search_engine.add_document(
            document["id"],
            document["title"],
            document["url"],
            document["description"] or "",
            document["content"] or ""
        )


load_search_index()


@app.get("/")
def home():
    return {
        "message": "Welcome to MySearchEngine",
        "status": "running",
        "version": "0.2.0"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "database": "connected"
    }


@app.get("/stats")
def database_stats():
    return {
        "documents": get_document_count()
    }


@app.post("/documents")
def create_document(
    title: str,
    url: str,
    description: str = "",
    content: str = ""
):
    document_id = add_document(
        title=title,
        url=url,
        description=description,
        content=content
    )

    search_engine.add_document(
        document_id,
        title,
        url,
        description,
        content
    )

    return {
        "message": "Document added successfully",
        "document_id": document_id
    }


@app.get("/search")
def search(
    query: str = Query(
        ...,
        min_length=1,
        description="Search query"
    )
):
    results = search_engine.search(query)

    return {
        "query": query,
        "results_count": len(results),
        "results": results
    }

@app.post("/crawl")
def crawl_website(
    url: str,
    max_pages: int = 5
):

    crawler = WebCrawler(
        max_pages=max_pages,
        same_domain=True,
        delay=1.0
    )

    pages = crawler.crawl(url)

    indexed = 0

    for page in pages:

        document_id = add_document(
            title=page["title"] or page["url"],
            url=page["url"],
            description=page["content"][:300],
            content=page["content"]
        )

        search_engine.add_document(
            document_id,
            page["title"] or page["url"],
            page["url"],
            page["content"][:300],
            page["content"]
        )

        indexed += 1

    return {
        "message": "Crawl completed",
        "pages_crawled": len(pages),
        "pages_indexed": indexed
    }