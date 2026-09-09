import { useEffect, useState, type KeyboardEvent } from "react";
import "./App.css";

type SearchResult = {
  title: string;
  url: string;
  description: string;
  snippet: string;
  score: number;
  matched_terms: string[];
  trust_score: number;
  authority_score: number;
  freshness_score: number;
  trust_reasons: string[];
};

type SearchInfo = {
  total_results: number;
  total_pages: number;
  page: number;
  search_time_ms: number;
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
  const [searchInfo, setSearchInfo] = useState<SearchInfo | null>(null);
  const pageLimit = 10;


  useEffect(() => {
    const trimmedQuery = query.trim();

    if (trimmedQuery.length < 2) {
      setSuggestions([]);
      return;
    }

    const controller = new AbortController();

    const fetchSuggestions = async () => {
      try {
        const response = await fetch(
          `http://127.0.0.1:8000/suggest?query=${encodeURIComponent(trimmedQuery)}`,
          { signal: controller.signal }
        );

        if (!response.ok) {
          throw new Error("Suggestion request failed");
        }

        const data = await response.json();
        setSuggestions(data.suggestions || []);
      } catch (error) {
        if ((error as Error).name !== "AbortError") {
          console.error("Suggestion error:", error);
          setSuggestions([]);
        }
      }
    };

    fetchSuggestions();

    return () => controller.abort();
  }, [query]);


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
    setSearchInfo(null);

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
        setSearchInfo(data);
    } catch (err) {
      console.error(err);
      setError("Unable to connect to the search server.");
      setResults([]);
      setTotalPages(1);
      setTotalResults(0);
      setSearchInfo(null);
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

        {searchInfo && !loading && (
          <div className="search-info">
            About {searchInfo.total_results || 0} result
            {searchInfo.total_results !== 1 ? "s" : ""}
            {" · "}
            {searchInfo.search_time_ms || 0} ms
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
                className="result-card"
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

                <div className="result-meta">
                  <span>
                    Trust: {Math.round((result.trust_score || 0) * 100)}%
                  </span>
                  <span>
                    Authority: {Math.round((result.authority_score || 0) * 100)}%
                  </span>
                  <span>
                    Freshness: {Math.round((result.freshness_score || 0) * 100)}%
                  </span>
                </div>

                <div className="trust-reasons">
                  {result.trust_reasons?.map((reason) => (
                    <span key={reason}>✓ {reason}</span>
                  ))}
                </div>


                <div className="result-score">
                  Relevance: {result.score}
                </div>

              </article>

            ))}

            {totalPages > 1 && !loading && (
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