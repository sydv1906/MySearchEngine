# MySearchEngine

A privacy-focused search engine built from scratch. It crawls publicly accessible
HTML pages, stores documents in SQLite, builds an inverted index, ranks results
with BM25, and serves them through FastAPI and a React frontend.

## Technology Stack

- Python, FastAPI, SQLite
- BeautifulSoup and Requests
- React, TypeScript, and Vite
- Pytest

## Current Progress

The guided implementation is complete through **Day 12**.

### Day 1 - Project Setup

- Created the project structure and development configuration.

### Day 2 - FastAPI Backend

- Added the FastAPI application, health endpoint, and API documentation.

### Day 3 - SQLite Storage

- Added persistent document storage and database statistics.
- Added document creation and basic document search APIs.

### Day 4 - Search Engine Core

- Added tokenization, lowercase normalization, and stop-word removal.
- Added an inverted index with term and document statistics.
- Added ranked search and automatic index loading from SQLite.

### Day 5 - React Frontend

- Added the React/Vite search interface and backend integration.

### Day 6 - Crawler Foundation

- Added HTML fetching, parsing, title/text extraction, and link discovery.

### Day 7 - Crawl Queue

- Added SQLite-backed crawl queue statuses, retry handling, robots.txt support,
	crawl delay, and indexing of crawled pages.

### Day 8 - Indexing Pipeline

- Improved token-aware inverted-index statistics.
- Centralized TF-IDF calculations while preserving compatibility APIs.

### Day 9 - Smart URL Frontier

- Added URL normalization, HTTP/HTTPS validation, hostname-based same-domain
	checks, duplicate prevention, crawl status checks, `max_pages`, and `max_urls`.

### Day 10 - BM25 Ranking

- Replaced TF-IDF as the primary scorer with BM25.
- Added average document length, title weighting, and description weighting.

### Day 11 - Result Quality

- Added content-based snippets and matched query terms.
- Added safe case-insensitive highlighting while preserving capitalization.
- Updated React result cards without using `dangerouslySetInnerHTML`.

### Day 12 - Pagination and Search UX

- Added paginated engine and API search results.
- Added total result and total page metadata.
- Added FastAPI validation for `page` and `limit`.
- Added React Previous/Next controls and result totals.

### Day 13 - Smart Query Processing

- Added reusable text normalization for lowercase, punctuation, and whitespace.
- Added configurable stopword removal to the tokenizer.
- Added `QueryProcessor` for normalized query tokens and canonical query text.
- Integrated query processing into BM25 search without changing ranking,
  snippets, highlighting, or pagination behavior.

## Milestone 1 - Query, Suggestions, and Search API

Completed accelerated Session 1:

- Added `QueryAnalyzer` with keyword, question, informational, navigational,
	and transactional query metadata.
- Added `GET /suggest` with lightweight prefix suggestions.
- Added `query_type` and `intent` metadata to `GET /search`.
- Added React autocomplete suggestions with keyboard and click-to-search flows.
- Preserved BM25 ranking, snippets, highlighting, pagination, and existing API
	defaults.

## Search API

Start the backend from the project root:

```bash
uvicorn backend.main:app --reload
```

Search with optional pagination:

```text
GET /search?query=python&page=1&limit=10
```

`page` must be at least `1`. `limit` must be between `1` and `50`.
Existing requests such as `/search?query=python` continue to use page `1` and
limit `10`.

The response includes:

```json
{
	"query": "python",
	"results_count": 10,
	"total_results": 37,
	"page": 1,
	"limit": 10,
	"total_pages": 4,
	"results": []
}
```

Other endpoints include `GET /`, `GET /health`, `GET /stats`, `POST /documents`,
`POST /crawl`, and `GET /crawl/stats`. Interactive documentation is available
at `/docs` while the backend is running.

## Run the Frontend

From the `frontend` directory:

```bash
npm install
npm run dev
```

## Run Tests

From the project root:

```bash
venv\Scripts\python.exe -m pytest
```

Build the frontend:

```bash
cd frontend
npm run build
```

## Current Architecture

```text
Crawler -> SQLite document store -> Tokenizer -> Inverted index
				-> BM25 ranking -> Snippets/highlighting -> Paginated FastAPI API
				-> React search interface
```