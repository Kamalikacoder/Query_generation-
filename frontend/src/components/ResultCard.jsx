function ResultCard({ result }) {
  return (
    <section className="result">
      <h2>Generated Output</h2>

      <div className="result-block">
        <span className="result-label">Original claim</span>
        <p>{result.claim}</p>
      </div>

      <div className="result-block">
        <span className="result-label">Keywords</span>
        <div className="chips">
          {result.keywords.map((keyword) => (
            <span key={keyword} className="chip">
              {keyword}
            </span>
          ))}
        </div>
      </div>

      <div className="result-block">
        <span className="result-label">Primary query</span>
        <p>{result.primary_query}</p>
      </div>

      <div className="result-block">
        <span className="result-label">Alternate queries</span>
        <ul className="list">
          {result.alternate_queries.map((query) => (
            <li key={query}>{query}</li>
          ))}
        </ul>
      </div>
    </section>
  );
}

export default ResultCard;
