import { useState, type KeyboardEvent } from "react";
import "./App.css";

type SearchResult = {
  title: string;
  url: string;
  description: string;
  score: number;
};

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);
  const [error, setError] = useState("");


  const search = async () => {
    const trimmedQuery = query.trim();

    if (!trimmedQuery) {
      return;
    }

    setLoading(true);
    setSearched(true);
    setError("");

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/search?query=${encodeURIComponent(trimmedQuery)}`
      );

      if (!response.ok) {
        throw new Error("Search request failed");
      }

      const data = await response.json();

      setResults(data.results || []);
    } catch (err) {
      console.error(err);
      setError("Unable to connect to the search server.");
      setResults([]);
    } finally {
      setLoading(false);
    }
  };


  const handleKeyDown = (event: KeyboardEvent<HTMLInputElement>) => {
    if (event.key === "Enter") {
      search();
    }
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
            onChange={(event) => setQuery(event.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Search anything..."
            className="search-input"
          />

          <button
            onClick={search}
            className="search-button"
            disabled={loading}
          >
            {loading ? "Searching..." : "Search"}
          </button>

        </div>


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
              Found {results.length} result
              {results.length !== 1 ? "s" : ""}
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
                  {result.title}
                </a>


                <div className="result-url">
                  {result.url}
                </div>


                <p className="result-description">
                  {result.description}
                </p>


                <div className="result-score">
                  Relevance: {result.score}
                </div>

              </article>

            ))}

          </div>
        )}

      </main>

    </div>
  );
}


export default App;