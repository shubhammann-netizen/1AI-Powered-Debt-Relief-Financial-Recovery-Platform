import React, { useEffect, useState } from "react";
import api from "../api/client";

export default function NegotiationEmail() {
  const [loans, setLoans] = useState([]);
  const [form, setForm] = useState({ loan_id: "", lender_name: "", tone: "professional" });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    api.get("/api/loans/").then((res) => setLoans(res.data));
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await api.post("/api/ai/negotiate", {
        loan_id: parseInt(form.loan_id),
        lender_name: form.lender_name,
        tone: form.tone,
      });
      setResult(res.data);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>AI Negotiation Email Generator</h2>
      <div className="card">
        <form onSubmit={handleSubmit}>
          <select className="form-input" value={form.loan_id}
                  onChange={(e) => setForm({ ...form, loan_id: e.target.value })} required>
            <option value="">Select a loan</option>
            {loans.map((l) => (
              <option key={l.loan_id} value={l.loan_id}>
                {l.loan_type} — Rs. {l.outstanding_amount}
              </option>
            ))}
          </select>
          <input className="form-input" placeholder="Lender Name"
                 value={form.lender_name}
                 onChange={(e) => setForm({ ...form, lender_name: e.target.value })} required />
          <select className="form-input" value={form.tone}
                  onChange={(e) => setForm({ ...form, tone: e.target.value })}>
            <option value="professional">Professional</option>
            <option value="empathetic">Empathetic</option>
            <option value="firm">Firm</option>
          </select>
          <button className="btn-primary" type="submit" disabled={loading}>
            {loading ? "Generating..." : "Generate Strategy & Letter"}
          </button>
        </form>
      </div>

      {result && (
        <>
          <div className="card">
            <h3>Negotiation Strategy</h3>
            <pre style={{ whiteSpace: "pre-wrap" }}>{result.negotiation_strategy}</pre>
          </div>
          <div className="card">
            <h3>Negotiation Letter</h3>
            <pre style={{ whiteSpace: "pre-wrap" }}>{result.settlement_letter}</pre>
          </div>
        </>
      )}
    </div>
  );
}
