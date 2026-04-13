import { FormEvent, useState } from "react";
import { generateSearchQuery, QueryResponseData } from "./api";

export default function App() {
  const [claim, setClaim] = useState("");
  const [result, setResult] = useState<QueryResponseData | null>(null);
  const [status, setStatus] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setStatus(null);
    setResult(null);

    if (!claim.trim()) {
      setStatus("Please enter a medical claim.");
      return;
    }

    try {
      setLoading(true);
      const data = await generateSearchQuery(claim);
      setResult(data);
      setStatus("Query generated successfully.");
    } catch (error) {
      setStatus(error instanceof Error ? error.message : "Unexpected error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="mx-auto max-w-3xl rounded-3xl border border-slate-700 bg-slate-900/90 p-8 shadow-xl shadow-slate-950/20">
        <h1 className="mb-4 text-3xl font-semibold">Query Generation Module</h1>
        <p className="mb-6 text-slate-400">
          Enter a medical claim and generate an evidence-style PubMed search query.
        </p>

        <form onSubmit={handleSubmit} className="space-y-4">
          <label className="block text-sm font-medium text-slate-200">
            Clinical claim
          </label>
          <textarea
            value={claim}
            onChange={(event) => setClaim(event.target.value)}
            rows={4}
            className="w-full rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100 outline-none focus:border-sky-500"
            placeholder="Antibiotics cure diabetes"
          />

          <button
            type="submit"
            disabled={loading}
            className="inline-flex items-center justify-center rounded-2xl bg-sky-500 px-5 py-3 text-sm font-semibold text-slate-950 transition hover:bg-sky-400 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {loading ? "Generating…" : "Generate Query"}
          </button>
        </form>

        {status ? (
          <p className="mt-5 rounded-2xl bg-slate-800 px-4 py-3 text-sm text-slate-200">
            {status}
          </p>
        ) : null}

        {result ? (
          <section className="mt-6 space-y-4 rounded-3xl border border-slate-700 bg-slate-950/80 p-6">
            <div>
              <h2 className="text-xl font-semibold">Result</h2>
            </div>
            <div className="space-y-2 text-sm text-slate-300">
              <div>
                <strong>Original claim:</strong>
                <p className="mt-1 rounded-2xl bg-slate-900 p-3 text-slate-100">
                  {result.originalClaim}
                </p>
              </div>
              <div>
                <strong>Cleaned claim:</strong>
                <p className="mt-1 rounded-2xl bg-slate-900 p-3 text-slate-100">
                  {result.cleanedClaim}
                </p>
              </div>
              <div>
                <strong>Generated query:</strong>
                <p className="mt-1 rounded-2xl bg-slate-900 p-3 text-slate-100">
                  {result.generatedQuery}
                </p>
              </div>
              <div>
                <strong>Keywords:</strong>
                <p className="mt-1 rounded-2xl bg-slate-900 p-3 text-slate-100">
                  {result.keywords.length > 0
                    ? result.keywords.join(", ")
                    : "No keywords extracted"}
                </p>
              </div>
            </div>
          </section>
        ) : null}
      </div>
    </main>
  );
}
