import React, { useEffect, useState } from "react";
import api from "../api/client";
import {
  ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip,
} from "recharts";

export default function Dashboard() {
  const [loans, setLoans] = useState([]);
  const [metrics, setMetrics] = useState(null);
  const [profileForm, setProfileForm] = useState({
    monthly_income: "", monthly_expenses: "", existing_debts: "",
  });

  const loadData = async () => {
    try {
      const loansRes = await api.get("/api/loans/");
      setLoans(loansRes.data);
    } catch (e) { /* no loans yet */ }
    try {
      const metricsRes = await api.get("/api/financial-profile/metrics");
      setMetrics(metricsRes.data);
    } catch (e) { /* no profile yet */ }
  };

  useEffect(() => { loadData(); }, []);

  const submitProfile = async (e) => {
    e.preventDefault();
    await api.post("/api/financial-profile/", {
      monthly_income: parseFloat(profileForm.monthly_income),
      monthly_expenses: parseFloat(profileForm.monthly_expenses),
      existing_debts: parseFloat(profileForm.existing_debts || 0),
    });
    loadData();
  };

  const chartData = metrics?.repayment_timeline_projection?.map((v, i) => ({
    month: `M${i + 1}`, balance: v,
  })) || [];

  const stressBadge = {
    Low: "badge-low", Medium: "badge-medium", High: "badge-high",
  }[metrics?.financial_stress_level] || "badge-medium";

  return (
    <div>
      <h2>Financial Dashboard</h2>

      <div className="grid">
        <div className="card">
          <h3>Active Loans</h3>
          <p style={{ fontSize: 28 }}>{loans.length}</p>
        </div>
        <div className="card">
          <h3>Monthly Surplus</h3>
          <p style={{ fontSize: 28 }}>Rs. {metrics?.monthly_surplus ?? "-"}</p>
        </div>
        <div className="card">
          <h3>EMI-to-Income Ratio</h3>
          <p style={{ fontSize: 28 }}>{metrics?.emi_to_income_ratio ?? "-"}%</p>
        </div>
        <div className="card">
          <h3>Financial Stress</h3>
          <p><span className={`badge ${stressBadge}`}>{metrics?.financial_stress_level ?? "N/A"}</span></p>
        </div>
        <div className="card">
          <h3>Financial Health Score</h3>
          <p style={{ fontSize: 28 }}>{metrics?.financial_health_score ?? "-"} / 100</p>
        </div>
      </div>

      {chartData.length > 0 && (
        <div className="card">
          <h3>Repayment Timeline Projection</h3>
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#30363d" />
              <XAxis dataKey="month" stroke="#8b949e" />
              <YAxis stroke="#8b949e" />
              <Tooltip contentStyle={{ background: "#161b22", border: "1px solid #30363d" }} />
              <Line type="monotone" dataKey="balance" stroke="#2f81f7" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      <div className="card">
        <h3>Update Financial Profile</h3>
        <form onSubmit={submitProfile}>
          <input className="form-input" type="number" placeholder="Monthly Income"
                 value={profileForm.monthly_income}
                 onChange={(e) => setProfileForm({ ...profileForm, monthly_income: e.target.value })} required />
          <input className="form-input" type="number" placeholder="Monthly Expenses"
                 value={profileForm.monthly_expenses}
                 onChange={(e) => setProfileForm({ ...profileForm, monthly_expenses: e.target.value })} required />
          <input className="form-input" type="number" placeholder="Existing Debts"
                 value={profileForm.existing_debts}
                 onChange={(e) => setProfileForm({ ...profileForm, existing_debts: e.target.value })} />
          <button className="btn-primary" type="submit">Save Profile</button>
        </form>
      </div>
    </div>
  );
}
