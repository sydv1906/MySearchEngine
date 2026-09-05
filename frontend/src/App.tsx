import { useState, type KeyboardEvent } from "react";
import "./App.css";

type SearchResult = {
  title: string;
  url: string;
  description: string;
  snippet: string;
  score: number;
  matched_terms: string[];
};

function HighlightedText({
  text,
  terms
}: {
  text: string;
  terms: string[];
}) {
  if (!terms.length) {
    return <>{text}</>;
  }

  const pattern = new RegExp(
    `(${terms.map((term) => term.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")).join("|")})`,
    "gi"
  );

  return <>{text.split(pattern).map((part, index) => {
    const isMatch = terms.some(
      (term) => part.toLowerCase() === term.toLowerCase()
    );

    return isMatch ? <strong key={index}>{part}</strong> : part;
  })}</>;
}

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);
  const [error, setError] = useState("");
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalResults, setTotalResults] = useState(0);
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const pageLimit = 10;


  const fetchSuggestions = async (value: string) => {
    const trimmedValue = value.trim();

    if (!trimmedValue) {
      setSuggestions([]);
      return;
    }

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/suggest?query=${encodeURIComponent(trimmedValue)}`
      );

      if (!response.ok) {
        throw new Error("Suggestion request failed");
      }

      const data = await response.json();
      setSuggestions(data.suggestions || []);
    } catch (error) {
      console.error("Suggestion error:", error);
      setSuggestions([]);
    }
  };


  const search = async (
    searchQuery = query,
    requestedPage = 1
  ) => {
    const trimmedQuery = searchQuery.trim();

    if (!trimmedQuery) {
      return;
    }

    setLoading(true);
    setSearched(true);
    setError("");
    setPage(requestedPage);
    setSuggestions([]);

    try {
      const params = new URLSearchParams({
        query: trimmedQuery,
        page: String(requestedPage),
        limit: String(pageLimit)
      });
      const response = await fetch(
        `http://127.0.0.1:8000/search?${params.toString()}`
      );

      if (!response.ok) {
        throw new Error("Search request failed");
      }

      const data = await response.json();

      setResults(data.results || []);
  setTotalPages(data.total_pages || 1);
  setTotalResults(data.total_results || 0);
    } catch (err) {
      console.error(err);
      setError("Unable to connect to the search server.");
      setResults([]);
      setTotalPages(1);
      setTotalResults(0);
    } finally {
      setLoading(false);
    }
  };


  const handleKeyDown = (event: KeyboardEvent<HTMLInputElement>) => {
    if (event.key === "Enter") {
      search(query, 1);
    }
  };


  const goToPage = (nextPage: number) => {
    search(query, nextPage);
  };


  return (
    <div className="app">

      <header className="header">
        <h1>MySearchEngine</h1>
        <p>Search the web, your way.</p>
      </header>


      <main className="main">

        <div className="search-container">

          <input
            type="text"
            value={query}
            onChange={(event) => {
              const value = event.target.value;
              setQuery(value);
              fetchSuggestions(value);
            }}
            onKeyDown={handleKeyDown}
            placeholder="Search anything..."
            className="search-input"
          />

          <button
            onClick={() => search(query, 1)}
            className="search-button"
            disabled={loading}
          >
            {loading ? "Searching..." : "Search"}
          </button>

        </div>

        {suggestions.length > 0 && (
          <div className="suggestions" role="listbox">
            {suggestions.map((suggestion) => (
              <button
                type="button"
                className="suggestion"
                key={suggestion}
                onClick={() => {
                  setQuery(suggestion);
                  setSuggestions([]);
                  search(suggestion, 1);
                }}
              >
                {suggestion}
              </button>
            ))}
          </div>
        )}


        {error && (
          <div className="error">
            {error}
          </div>
        )}


        {loading && (
          <div className="loading">
            Searching MySearchEngine...
          </div>
        )}


        {!loading && searched && results.length === 0 && !error && (
          <div className="no-results">
            <h2>No results found</h2>
            <p>
              Try using different keywords.
            </p>
          </div>
        )}


        {!loading && results.length > 0 && (
          <div className="results">

            <p className="results-count">
              {totalResults} result{totalResults !== 1 ? "s" : ""} found
            </p>


            {results.map((result, index) => (

              <article
                className="result"
                key={`${result.url}-${index}`}
              >

                <a
                  href={result.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="result-title"
                >
                  <HighlightedText
                    text={result.title}
                    terms={result.matched_terms}
                  />
                </a>


                <div className="result-url">
                  {result.url}
                </div>


                <p className="result-description">
                  {result.description}
                </p>

                <p className="result-snippet">
                  <HighlightedText
                    text={result.snippet}
                    terms={result.matched_terms}
                  />
                </p>


                <div className="result-score">
                  Relevance: {result.score}
                </div>

              </article>

            ))}

            {totalPages > 1 && (
              <div className="pagination" aria-label="Search results pages">
                <button
                  type="button"
                  onClick={() => goToPage(page - 1)}
                  disabled={page === 1 || loading}
                >
                  Previous
                </button>
                <span>Page {page} of {totalPages}</span>
                <button
                  type="button"
                  onClick={() => goToPage(page + 1)}
                  disabled={page === totalPages || loading}
                >
                  Next
                </button>
              </div>
            )}

          </div>
        )}

      </main>

    </div>
  );
}


export default App;