import { useState } from "react";

const defaultClaim = "Insulin is used to manage diabetes.";

function ClaimForm({ onSubmit, loading }) {
  const [claim, setClaim] = useState(defaultClaim);

  const handleSubmit = (event) => {
    event.preventDefault();
    onSubmit(claim);
  };

  return (
    <form className="form" onSubmit={handleSubmit}>
      <label htmlFor="claim" className="label">
        Enter clinical claim
      </label>
      <textarea
        id="claim"
        className="textarea"
        rows="5"
        value={claim}
        onChange={(event) => setClaim(event.target.value)}
        placeholder="Example: Hypertension increases the risk of stroke."
      />
      <button className="button" type="submit" disabled={loading}>
        {loading ? "Generating..." : "Generate Query"}
      </button>
    </form>
  );
}

export default ClaimForm;
