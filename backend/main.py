from fastapi import FastAPI, Query
from backend.database import (
    initialize_database,
    add_document,
    search_documents,
    get_document_count
)


app = FastAPI(
    title="MySearchEngine API",
    description="Backend API for MySearchEngine",
    version="0.2.0"
)


# Initialize database when the application starts
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
    results = search_documents(query)

    cleaned_results = []

    for result in results:
        cleaned_results.append({
            "title": result["title"],
            "url": result["url"],
            "description": result["description"]
        })

    return {
        "query": query,
        "results_count": len(cleaned_results),
        "results": cleaned_results
    }