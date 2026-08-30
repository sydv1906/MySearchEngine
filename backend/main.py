from fastapi import FastAPI

app = FastAPI(
    title="MySearchEngine API",
    description="Backend API for MySearchEngine",
    version="0.1.0"
)


# Temporary sample data
sample_documents = [
    {
        "title": "Python Official Website",
        "url": "https://www.python.org/",
        "description": "Official website of the Python programming language."
    },
    {
        "title": "FastAPI",
        "url": "https://fastapi.tiangolo.com/",
        "description": "Modern and fast web framework for building APIs with Python."
    },
    {
        "title": "GitHub",
        "url": "https://github.com/",
        "description": "A platform for hosting and collaborating on software projects."
    }
]


@app.get("/")
def home():
    return {
        "message": "Welcome to MySearchEngine",
        "status": "running",
        "version": "0.1.0"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.get("/search")
def search(query: str):
    results = []

    query_lower = query.lower()

    for document in sample_documents:
        searchable_text = (
            document["title"] + " " +
            document["description"]
        ).lower()

        if query_lower in searchable_text:
            results.append(document)

    return {
        "query": query,
        "results_count": len(results),
        "results": results
    }