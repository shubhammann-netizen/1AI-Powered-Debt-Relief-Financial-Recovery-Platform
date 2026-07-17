import React, { useEffect, useState } from "react";
import api from "../api/client";

export default function SettlementPredictor() {
  const [loans, setLoans] = useState([]);
  const [loanForm, setLoanForm] = useState({
    loan_type: "credit_card", loan_amount: "", outstanding_amount: "",
    interest_rate: "", due_date: "",
  });
  const [results, setResults] = useState([]);

  const loadLoans = async () => {
    const res = await api.get("/api/loans/");
    setLoans(res.data);
  };

  useEffect(() => { loadLoans(); }, []);

  const addLoan = async (e) => {
    e.preventDefault();
    await api.post("/api/loans/", {
      ...loanForm,
      loan_amount: parseFloat(loanForm.loan_amount),
      outstanding_amount: parseFloat(loanForm.outstanding_amount),
      interest_rate: parseFloat(loanForm.interest_rate),
      due_date: new Date(loanForm.due_date).toISOString(),
    });
    setLoanForm({ loan_type: "credit_card", loan_amount: "", outstanding_amount: "", interest_rate: "", due_date: "" });
    loadLoans();
  };

  const predict = async (loanId) => {
    const res = await api.post(`/api/settlements/predict/${loanId}`);
    setResults((prev) => [res.data, ...prev]);
  };

  const badgeClass = { High: "badge-high", Medium: "badge-medium", Low: "badge-low" };

  return (
    <div>
      <h2>Settlement Predictor</h2>

      <div className="card">
        <h3>Add a Loan</h3>
        <form onSubmit={addLoan}>
          <select className="form-input" value={loanForm.loan_type}
                  onChange={(e) => setLoanForm({ ...loanForm, loan_type: e.target.value })}>
            <option value="credit_card">Credit Card</option>
            <option value="personal_loan">Personal Loan</option>
            <option value="medical_loan">Medical Loan</option>
            <option value="auto_loan">Auto Loan</option>
            <option value="education_loan">Education Loan</option>
          </select>
          <input className="form-input" type="number" placeholder="Loan Amount"
                 value={loanForm.loan_amount}
                 onChange={(e) => setLoanForm({ ...loanForm, loan_amount: e.target.value })} required />
          <input className="form-input" type="number" placeholder="Outstanding Amount"
                 value={loanForm.outstanding_amount}
                 onChange={(e) => setLoanForm({ ...loanForm, outstanding_amount: e.target.value })} required />
          <input className="form-input" type="number" placeholder="Interest Rate (%)"
                 value={loanForm.interest_rate}
                 onChange={(e) => setLoanForm({ ...loanForm, interest_rate: e.target.value })} required />
          <input className="form-input" type="date"
                 value={loanForm.due_date}
                 onChange={(e) => setLoanForm({ ...loanForm, due_date: e.target.value })} required />
          <button className="btn-primary" type="submit">Add Loan</button>
        </form>
      </div>

      <div className="card">
        <h3>Your Loans</h3>
        {loans.length === 0 && <p>No loans added yet.</p>}
        {loans.map((loan) => (
          <div key={loan.loan_id} className="card" style={{ background: "#0d1117" }}>
            <p><strong>{loan.loan_type}</strong> — Outstanding: Rs. {loan.outstanding_amount}</p>
            <button className="btn-primary" onClick={() => predict(loan.loan_id)}>
              Predict Settlement
            </button>
          </div>
        ))}
      </div>

      {results.length > 0 && (
        <div className="card">
          <h3>Prediction Results</h3>
          {results.map((r) => (
            <div key={r.settlement_id} className="card" style={{ background: "#0d1117" }}>
              <p>Prediction: <strong>{r.settlement_prediction}</strong></p>
              <p>Recommended Amount: Rs. {r.recommended_amount}</p>
              <p>Priority: <span className={`badge ${badgeClass[r.priority_level]}`}>{r.priority_level}</span></p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
