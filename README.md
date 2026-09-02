# MySearchEngine# MySearchEngine

A privacy-focused search engine built from scratch.

## Project Goal

MySearchEngine is an independent search engine designed to:

- Crawl publicly accessible web pages
- Extract and process webpage content
- Build a searchable index
- Rank search results
- Provide a clean search interface
- Avoid dependence on commercial search APIs

## Technology Stack

- Python
- FastAPI
- React / Next.js
- SQLite / PostgreSQL
- BeautifulSoup
- Git & GitHub

## Current Status

Day 1 - Project setup completed.

## Development Roadmap

- [ ] Backend API
- [ ] Database
- [ ] Search functionality
- [ ] Frontend
- [ ] Web crawler
- [ ] Indexing system
- [ ] Ranking algorithm
- [ ] Search suggestions
- [ ] Search filters
- [ ] Security
- [ ] Deployment



## Current Status

Day 2 - FastAPI backend created and tested successfully.

## Backend API

The backend currently provides:

- `GET /` - API welcome endpoint
- `GET /health` - Health check endpoint
- `GET /search?query=<query>` - Temporary sample search endpoint

Interactive API documentation is available at:

`/docs`


## Current Status

Day 3 - SQLite database and persistent document search implemented.

## Backend API

The backend currently provides:

- `GET /` - API welcome endpoint
- `GET /health` - Health check endpoint
- `GET /stats` - Database statistics
- `POST /documents` - Add a searchable document
- `GET /search?query=<query>` - Search indexed documents

## Database

MySearchEngine currently uses SQLite for local document storage.

The database is generated automatically in the local `data/` directory.

## Current Status

Day 4 - Search engine core implemented.

## Search Engine

MySearchEngine now includes:

- Text tokenization
- Lowercase normalization
- Stop-word removal
- Inverted index
- Term frequency calculation
- Inverse document frequency calculation
- TF-IDF-style relevance scoring
- Ranked search results
- Automatic index rebuilding from SQLite


## Search Architecture

The current search pipeline is:

User Query
→ Tokenization
→ Inverted Index
→ TF-IDF Scoring
→ Ranking
→ Search Results

## Current Status

Day 5- MySearchEngine Frontend

React + Vite frontend for MySearchEngine.

## Run locally

From the frontend directory:

```bash
npm install
npm run dev


Run the backend:

```bash
uvicorn backend.main:app --reload

## Web Crawler

MySearchEngine now includes a basic web crawler.

The crawler can:

- Accept a starting URL
- Download HTML pages
- Parse HTML
- Extract page titles
- Extract page text
- Extract links
- Convert relative links to absolute URLs
- Avoid duplicate URLs
- Restrict crawling to the same domain
- Respect robots.txt
- Apply a crawl delay
- Limit the number of pages crawled
- Store crawled pages in SQLite
- Add crawled pages to the search index

## Crawl API

Start the FastAPI server:

```bash
uvicorn backend.main:app --reload