// src/pages/NegotiationEmail.jsx
// AI Negotiation Strategy Generation: creates lender-specific negotiation
// letters and settlement request content using the Gemini-backed API
// (with automatic rule-based fallback).

import React, { useEffect, useState } from "react";
import api from "../api/axios.js";
import Card from "../components/Card.jsx";

export default function NegotiationEmail() {
  const [loans, setLoans] = useState([]);
  const [loanId, setLoanId] = useState("");
  const [lenderName, setLenderName] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    api.get("/loans/").then((res) => {
      setLoans(res.data);
      if (res.data.length) setLoanId(String(res.data[0].loan_id));
    });
  }, []);

  async function handleGenerate() {
    if (!loanId) return;
    setError("");
    setLoading(true);
    setResult(null);
    try {
      const res = await api.post("/negotiation/generate", {
        loan_id: parseInt(loanId, 10),
        lender_name: lenderName || "the lender",
      });
      setResult(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Could not generate a negotiation letter.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="dashboard">
      <h1>AI Negotiation Email</h1>
      {error && <div className="alert alert-error">{error}</div>}

      <Card title="Generate a Negotiation Package">
        <div className="stacked-form">
          <label>Loan</label>
          <select value={loanId} onChange={(e) => setLoanId(e.target.value)}>
            {loans.map((loan) => (
              <option key={loan.loan_id} value={loan.loan_id}>
                {loan.loan_type} - outstanding {loan.outstanding_amount.toFixed(2)}
              </option>
            ))}
          </select>
          <label>Lender Name (optional)</label>
          <input value={lenderName} onChange={(e) => setLenderName(e.target.value)} />
          <button className="btn btn-primary" onClick={handleGenerate} disabled={loading}>
            {loading ? "Generating..." : "Generate Negotiation Letter"}
          </button>
        </div>
      </Card>

      {result && (
        <>
          <Card title="AI Summary">
            <p>{result.ai_response}</p>
          </Card>
          <Card title="Negotiation Strategy">
            <p>{result.negotiation_strategy}</p>
          </Card>
          <Card title="Settlement Letter">
            <pre className="letter-preview">{result.settlement_letter}</pre>
          </Card>
        </>
      )}
    </div>
  );
}
