import json
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from python_backend.evidence_retrieval import retrieve_evidence
from python_backend.query_generation import generate_queries


HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", "8000"))


HTML = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Factual Hallucination Detection and Correction in Medical Summaries</title>
    <style>
      :root {
        --bg: #f3efe6;
        --paper: #fffdf8;
        --ink: #1f2937;
        --muted: #5b6472;
        --accent: #0f766e;
        --accent-soft: #d7f3ee;
        --border: #d8d0c0;
        --shadow: 0 16px 40px rgba(31, 41, 55, 0.08);
      }
      * { box-sizing: border-box; }
      body {
        margin: 0;
        font-family: Georgia, "Times New Roman", serif;
        background:
          radial-gradient(circle at top left, #f8d9a0 0, transparent 22rem),
          linear-gradient(180deg, #efe7d6 0%, var(--bg) 100%);
        color: var(--ink);
      }
      .wrap { width: min(960px, calc(100% - 32px)); margin: 40px auto; }
      .hero, .card {
        background: rgba(255, 253, 248, 0.94);
        border: 1px solid rgba(216, 208, 192, 0.9);
        border-radius: 24px;
        box-shadow: var(--shadow);
      }
      .hero { padding: 32px; margin-bottom: 24px; }
      h1 { margin: 0; font-size: clamp(2rem, 5vw, 3.4rem); line-height: 1; }
      .sub { margin: 14px 0 0; max-width: 44rem; color: var(--muted); font: 400 1rem/1.7 Arial, sans-serif; }
      form.card { padding: 24px; }
      .grid { display: grid; gap: 16px; }
      @media (min-width: 760px) { .grid.two { grid-template-columns: 2fr 1fr; } }
      label { display: block; margin-bottom: 8px; font: 700 0.95rem/1.4 Arial, sans-serif; }
      input, textarea {
        width: 100%;
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 14px 16px;
        font: 400 1rem/1.5 Arial, sans-serif;
        background: #fff;
        color: var(--ink);
      }
      textarea { min-height: 120px; resize: vertical; }
      button {
        border: 0;
        border-radius: 999px;
        padding: 14px 22px;
        font: 700 0.95rem/1 Arial, sans-serif;
        color: white;
        background: linear-gradient(135deg, #0f766e, #155e75);
        cursor: pointer;
      }
      button:disabled { opacity: 0.7; cursor: wait; }
      .ghost-btn { border: 1px solid var(--border); color: var(--ink); background: #fff; }
      .toolbar, .claim-actions { display: flex; gap: 12px; align-items: center; margin-top: 16px; flex-wrap: wrap; }
      .hint, .status, .meta, .empty { font: 400 0.95rem/1.6 Arial, sans-serif; color: var(--muted); }
      .status { margin: 18px 2px; }
      .query-preview {
        margin-top: 10px;
        padding: 12px 14px;
        border-radius: 14px;
        background: #f6f1e7;
        border: 1px solid var(--border);
        font: 400 0.95rem/1.6 Arial, sans-serif;
        color: var(--muted);
      }
      .results { display: grid; gap: 18px; margin-top: 18px; }
      .card.result { padding: 22px; }
      .result h2 { margin: 0 0 10px; font-size: 1.35rem; line-height: 1.35; }
      .meta { margin: 0 0 12px; }
      .chips { display: flex; gap: 10px; flex-wrap: wrap; margin: 14px 0 18px; }
      .chip {
        background: var(--accent-soft);
        color: var(--accent);
        border-radius: 999px;
        padding: 6px 10px;
        font: 700 0.8rem/1 Arial, sans-serif;
      }
      .result p { margin: 0; font: 400 1rem/1.7 Arial, sans-serif; }
      a { color: #0b5ea8; }
    </style>
  </head>
  <body>
    <main class="wrap">
      <section class="hero">
        <h1>Factual Hallucination Detection and Correction in Medical Summaries</h1>
      </section>

      <form id="evidence-form" class="card">
        <label for="claim">Claim</label>
        <textarea id="claim" name="claim" placeholder="Aspirin is used for heart attack prevention" required></textarea>
        <div class="claim-actions">
          <button id="generate-query-btn" class="ghost-btn" type="button">Generate Query</button>
          <span class="hint">This generates a query and then fetches PubMed evidence.</span>
        </div>

        <div class="grid two" style="margin-top: 16px;">
          <div>
            <label for="query">Search query</label>
            <input id="query" name="query" placeholder="Generated query will appear here" readonly />
            <div id="query-preview" class="query-preview" hidden></div>
          </div>
          <div>
            <label for="maxResults">Max results</label>
            <input id="maxResults" name="maxResults" type="number" min="1" max="10" value="5" />
          </div>
        </div>

        <div class="toolbar">
          <button id="submit-btn" type="submit" disabled hidden>Fetch Evidence from PubMed</button>
        </div>

        <div id="status" class="status"></div>
        <section id="results" class="results"></section>
      </form>
    </main>

    <script>
      const form = document.getElementById("evidence-form");
      const resultsEl = document.getElementById("results");
      const statusEl = document.getElementById("status");
      const submitBtn = document.getElementById("submit-btn");
      const generateQueryBtn = document.getElementById("generate-query-btn");
      const queryPreviewEl = document.getElementById("query-preview");
      const claimEl = document.getElementById("claim");
      const queryEl = document.getElementById("query");

      function escapeHtml(value) {
        return String(value)
          .replaceAll("&", "&amp;")
          .replaceAll("<", "&lt;")
          .replaceAll(">", "&gt;")
          .replaceAll('"', "&quot;")
          .replaceAll("'", "&#39;");
      }

      function setGeneratedQuery(query) {
        const cleanQuery = String(query || "").trim();
        queryEl.value = cleanQuery;
        submitBtn.disabled = !cleanQuery;
        queryPreviewEl.hidden = !cleanQuery;
        queryPreviewEl.textContent = cleanQuery ? "Generated query: " + cleanQuery : "";
      }

      function renderResults(data) {
        if (!data.results || data.results.length === 0) {
          resultsEl.innerHTML = '<div class="card result empty">No evidence found for this claim.</div>';
          return;
        }

        resultsEl.innerHTML = data.results.map((item) => {
          const authors = Array.isArray(item.authors) && item.authors.length
            ? escapeHtml(item.authors.join(", "))
            : "Authors not available";

          return `
            <article class="card result">
              <h2>${escapeHtml(item.title || "Untitled")}</h2>
              <p class="meta">
                PMID: ${escapeHtml(item.pmid || "")} |
                Source: ${escapeHtml(item.source || "Unknown")} |
                Date: ${escapeHtml(item.pubdate || "Unknown")}
              </p>
              <div class="chips">
                <span class="chip">Title overlap: ${escapeHtml(item.title_overlap ?? 0)}</span>
                <span class="chip">Abstract overlap: ${escapeHtml(item.abstract_overlap ?? 0)}</span>
                <span class="chip">Score: ${escapeHtml(item.relevance_score ?? 0)}</span>
              </div>
              <p><strong>Authors:</strong> ${authors}</p>
              <p style="margin-top: 12px;">${escapeHtml(item.abstract || "Abstract not available.")}</p>
              <p style="margin-top: 14px;">
                <a href="${escapeHtml(item.url || "#")}" target="_blank" rel="noreferrer">Open PubMed article</a>
              </p>
            </article>
          `;
        }).join("");
      }

      async function fetchEvidence(claim, query, maxResults) {
        submitBtn.disabled = true;
        statusEl.textContent = "Fetching evidence...";
        resultsEl.innerHTML = "";

        const params = new URLSearchParams({ claim, query, maxResults });
        const response = await fetch("/api/evidence?" + params.toString());
        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.error || "Failed to fetch evidence.");
        }

        statusEl.textContent = `Found ${data.results.length} result(s) for: "${claim}"`;
        renderResults(data);
      }

      async function generateQuery() {
        const claim = claimEl.value.trim();
        if (!claim) {
          statusEl.textContent = "Enter a claim before generating a query.";
          return;
        }

        generateQueryBtn.disabled = true;
        statusEl.textContent = "Generating query...";
        resultsEl.innerHTML = "";

        try {
          const queryResponse = await fetch("/api/query?claim=" + encodeURIComponent(claim));
          const queryData = await queryResponse.json();
          if (!queryResponse.ok) {
            throw new Error(queryData.error || "Failed to generate query.");
          }

          setGeneratedQuery(queryData.query);
          await fetchEvidence(claim, queryData.query, String(document.getElementById("maxResults").value || "5"));
        } catch (error) {
          statusEl.textContent = error instanceof Error ? error.message : "Unexpected error";
        } finally {
          generateQueryBtn.disabled = false;
          submitBtn.disabled = !queryEl.value;
        }
      }

      generateQueryBtn.addEventListener("click", generateQuery);
      claimEl.addEventListener("input", () => {
        setGeneratedQuery("");
        resultsEl.innerHTML = "";
      });
      form.addEventListener("submit", async (event) => {
        event.preventDefault();
        await fetchEvidence(claimEl.value.trim(), queryEl.value.trim(), String(document.getElementById("maxResults").value || "5"));
      });
    </script>
  </body>
</html>"""


class AppHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/":
            self._send_html(HTML)
            return

        if parsed.path == "/api/health":
            self._send_json({"ok": True, "port": PORT})
            return

        if parsed.path == "/api/query":
            self._handle_query(parsed.query)
            return

        if parsed.path == "/api/evidence":
            self._handle_evidence(parsed.query)
            return

        self._send_json({"error": "Not found"}, status=HTTPStatus.NOT_FOUND)

    def log_message(self, format, *args):
        print("%s - %s" % (self.address_string(), format % args))

    def _handle_query(self, raw_query):
        params = parse_qs(raw_query)
        claim = self._first(params, "claim")

        if not claim:
            self._send_json({"error": "Claim is required."}, status=HTTPStatus.BAD_REQUEST)
            return

        self._send_json({"claim": claim, "query": generate_queries(claim)})

    def _handle_evidence(self, raw_query):
        params = parse_qs(raw_query)
        claim = self._first(params, "claim")
        query = self._first(params, "query") or claim
        max_results = self._safe_max_results(self._first(params, "maxResults"))

        if not claim:
            self._send_json({"error": "Claim is required."}, status=HTTPStatus.BAD_REQUEST)
            return

        results = retrieve_evidence(claim, query, max_results=max_results)
        self._send_json({
            "claim": claim,
            "query": query,
            "maxResults": max_results,
            "results": results,
        })

    def _send_html(self, html):
        content = html.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def _send_json(self, payload, status=HTTPStatus.OK):
        content = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    @staticmethod
    def _first(params, key):
        values = params.get(key, [])
        return values[0].strip() if values else ""

    @staticmethod
    def _safe_max_results(value):
        try:
            return max(1, min(10, int(value or 5)))
        except ValueError:
            return 5


def main():
    server = ThreadingHTTPServer((HOST, PORT), AppHandler)
    print(f"Python server running on http://localhost:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
