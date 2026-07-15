// src/pages/SettlementPredictor.jsx
// AI-Powered Settlement Prediction Dashboard: generates and lists
// settlement recommendations per loan.

import React, { useEffect, useState } from "react";
import api from "../api/axios.js";
import Card from "../components/Card.jsx";

export default function SettlementPredictor() {
  const [loans, setLoans] = useState([]);
  const [selectedLoan, setSelectedLoan] = useState("");
  const [settlements, setSettlements] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function loadData() {
    const [loansRes, settlementsRes] = await Promise.all([
      api.get("/loans/"),
      api.get("/settlement/"),
    ]);
    setLoans(loansRes.data);
    setSettlements(settlementsRes.data);
    if (loansRes.data.length && !selectedLoan) {
      setSelectedLoan(String(loansRes.data[0].loan_id));
    }
  }

  useEffect(() => {
    loadData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function handlePredict() {
    if (!selectedLoan) return;
    setError("");
    setLoading(true);
    try {
      await api.post(`/settlement/predict/${selectedLoan}`);
      loadData();
    } catch (err) {
      setError(err.response?.data?.detail || "Could not generate a prediction.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="dashboard">
      <h1>Settlement Predictor</h1>
      {error && <div className="alert alert-error">{error}</div>}

      <Card title="Generate a Settlement Prediction">
        <div className="inline-form">
          <select value={selectedLoan} onChange={(e) => setSelectedLoan(e.target.value)}>
            {loans.map((loan) => (
              <option key={loan.loan_id} value={loan.loan_id}>
                {loan.loan_type} - outstanding {loan.outstanding_amount.toFixed(2)}
              </option>
            ))}
          </select>
          <button className="btn btn-primary" onClick={handlePredict} disabled={loading}>
            {loading ? "Analyzing..." : "Predict Settlement"}
          </button>
        </div>
      </Card>

      <Card title="Settlement History">
        <table className="data-table">
          <thead>
            <tr>
              <th>Loan</th>
              <th>Prediction</th>
              <th>Recommended Amount</th>
              <th>Priority</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            {settlements.map((s) => (
              <tr key={s.settlement_id}>
                <td>#{s.loan_id}</td>
                <td>{s.settlement_prediction}</td>
                <td>{s.recommended_amount.toFixed(2)}</td>
                <td>
                  <span className={`badge badge-${s.priority_level.toLowerCase()}`}>
                    {s.priority_level}
                  </span>
                </td>
                <td>{new Date(s.created_at).toLocaleDateString()}</td>
              </tr>
            ))}
            {settlements.length === 0 && (
              <tr>
                <td colSpan={5} className="empty-state">No settlement predictions yet.</td>
              </tr>
            )}
          </tbody>
        </table>
      </Card>
    </div>
  );
}
