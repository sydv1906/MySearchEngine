from contextlib import asynccontextmanager

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from crawler.crawler import WebCrawler

from backend.database import (
    initialize_database,
    add_document,
    get_document_count,
    get_all_documents,
    get_crawl_stats
)

from search.engine import SearchEngine


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


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_search_index()
    yield


app = FastAPI(
    title="MySearchEngine API",
    description="Backend API for MySearchEngine",
    version="0.3.0",
    lifespan=lifespan
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
    ),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50)
):
    search_results = search_engine.search_paginated(
        query,
        page=page,
        limit=limit
    )
    results = search_results["results"]
    query_analysis = search_engine.query_analyzer.analyze(query)

    return {
        "query": query,
        "query_type": query_analysis["query_type"],
        "intent": query_analysis["intent"],
        "results_count": len(results),
        "total_results": search_results["total_results"],
        "page": search_results["page"],
        "limit": search_results["limit"],
        "total_pages": search_results["total_pages"],
        "results": results
    }


@app.get("/suggest")
def suggest(query: str = ""):
    normalized_query = query.strip().lower()

    if not normalized_query:
        return {
            "query": "",
            "suggestions": []
        }

    candidates = [
        "python programming",
        "python tutorial",
        "python documentation",
        "python web development",
        "python machine learning",
        "python programming language",
    ]
    suggestions = [
        candidate
        for candidate in candidates
        if candidate.startswith(normalized_query)
    ]

    return {
        "query": normalized_query,
        "suggestions": suggestions[:5]
    }

@app.post("/crawl")
def crawl_website(
    url: str,
    max_pages: int = 5,
    max_urls: int = 100
):

    crawler = WebCrawler(
        max_pages=max_pages,
        max_urls=max_urls,
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


@app.get("/crawl/stats")
def crawl_stats():
    return get_crawl_stats()