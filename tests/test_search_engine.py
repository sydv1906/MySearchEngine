from search.engine import SearchEngine


engine = SearchEngine()


engine.add_document(
    1,
    "Python Programming",
    "https://www.python.org/",
    "Python programming language",
    "Python is widely used for programming and software development."
)


engine.add_document(
    2,
    "FastAPI Documentation",
    "https://fastapi.tiangolo.com/",
    "Fast web framework",
    "FastAPI is a Python framework for building APIs."
)


engine.add_document(
    3,
    "GitHub",
    "https://github.com/",
    "Software development platform",
    "GitHub provides repositories for software development."
)


results = engine.search("python programming")


for result in results:
    print(
        result["title"],
        "->",
        result["score"]
    )