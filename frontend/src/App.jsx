import { useState } from "react";
import ClaimForm from "./components/ClaimForm";
import ResultCard from "./components/ResultCard";
import { generateQuery } from "./api/queryApi";

const initialState = {
  loading: false,
  error: "",
  result: null,
};

function App() {
  const [state, setState] = useState(initialState);

  const handleSubmit = async (claim) => {
    setState({ loading: true, error: "", result: null });

    try {
      const response = await generateQuery(claim);
      setState({ loading: false, error: "", result: response.data });
    } catch (error) {
      setState({
        loading: false,
        error: error.message || "Failed to generate query. Please try again.",
        result: null,
      });
    }
  };

  return (
    <main className="page">
      <section className="card">
        <p className="eyebrow">Query Generation Module</p>
        <h1>Clinical Claim to PubMed Query</h1>
        <p className="subtitle">
          Enter an atomic medical claim to extract keywords and generate search-ready queries.
        </p>

        <ClaimForm onSubmit={handleSubmit} loading={state.loading} />

        {state.error ? <p className="error">{state.error}</p> : null}
        {state.result ? <ResultCard result={state.result} /> : null}
      </section>
    </main>
  );
}

export default App;
