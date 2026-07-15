// src/pages/Dashboard.jsx
// Financial Dashboard Interface: shows active loans, monthly surplus, debt
// stress analysis, and real-time financial health metrics.

import React, { useEffect, useState } from "react";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from "recharts";
import api from "../api/axios.js";
import Card from "../components/Card.jsx";

const STRESS_COLORS = { Low: "#22c55e", Medium: "#f59e0b", High: "#ef4444" };

export default function Dashboard() {
  const [metrics, setMetrics] = useState(null);
  const [loans, setLoans] = useState([]);
  const [profileForm, setProfileForm] = useState({
    monthly_income: "",
    monthly_expenses: "",
    existing_debts: "",
  });
  const [loanForm, setLoanForm] = useState({
    loan_type: "Credit Card",
    loan_amount: "",
    outstanding_amount: "",
    interest_rate: "",
    due_date: "",
  });
  const [message, setMessage] = useState("");

  async function loadData() {
    try {
      const [metricsRes, loansRes] = await Promise.all([
        api.get("/financial/metrics"),
        api.get("/loans/"),
      ]);
      setMetrics(metricsRes.data);
      setLoans(loansRes.data);
    } catch (err) {
      // If there is no profile yet, metrics endpoint still returns zeros
      console.error(err);
    }
  }

  useEffect(() => {
    loadData();
  }, []);

  async function submitProfile(e) {
    e.preventDefault();
    try {
      await api.post("/financial/profile", {
        monthly_income: parseFloat(profileForm.monthly_income),
        monthly_expenses: parseFloat(profileForm.monthly_expenses),
        existing_debts: parseFloat(profileForm.existing_debts),
      });
      setMessage("Financial profile saved.");
      loadData();
    } catch (err) {
      setMessage(err.response?.data?.detail || "Could not save profile.");
    }
  }

  async function submitLoan(e) {
    e.preventDefault();
    try {
      await api.post("/loans/", {
        ...loanForm,
        loan_amount: parseFloat(loanForm.loan_amount),
        outstanding_amount: parseFloat(loanForm.outstanding_amount),
        interest_rate: parseFloat(loanForm.interest_rate),
        due_date: new Date(loanForm.due_date).toISOString(),
      });
      setMessage("Loan added.");
      setLoanForm({
        loan_type: "Credit Card",
        loan_amount: "",
        outstanding_amount: "",
        interest_rate: "",
        due_date: "",
      });
      loadData();
    } catch (err) {
      setMessage(err.response?.data?.detail || "Could not add loan.");
    }
  }

  const healthScore = metrics?.financial_health_score ?? 0;
  const chartData = [
    { name: "Health Score", value: healthScore },
    { name: "Remaining", value: Math.max(100 - healthScore, 0) },
  ];

  return (
    <div className="dashboard">
      <h1>Financial Overview</h1>
      {message && <div className="alert alert-info">{message}</div>}

      <div className="grid grid-4">
        <Card title="Active Loans">
          <p className="metric-value">{loans.length}</p>
        </Card>
        <Card title="Monthly Surplus">
          <p className="metric-value">
            {metrics ? metrics.monthly_surplus.toFixed(2) : "--"}
          </p>
        </Card>
        <Card title="Total Outstanding Debt">
          <p className="metric-value">
            {metrics ? metrics.total_outstanding_debt.toFixed(2) : "--"}
          </p>
        </Card>
        <Card title="Debt Stress Level">
          <span
            className="badge"
            style={{ backgroundColor: STRESS_COLORS[metrics?.stress_level] || "#64748b" }}
          >
            {metrics?.stress_level || "N/A"}
          </span>
        </Card>
      </div>

      <div className="grid grid-2">
        <Card title="Financial Health Score">
          <ResponsiveContainer width="100%" height={220}>
            <PieChart>
              <Pie
                data={chartData}
                dataKey="value"
                innerRadius={60}
                outerRadius={90}
                startAngle={90}
                endAngle={-270}
              >
                <Cell fill="#6366f1" />
                <Cell fill="#1e293b" />
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
          <p className="metric-caption">{healthScore.toFixed(0)} / 100</p>
        </Card>

        <Card title="EMI-to-Income & Debt-to-Income Ratios">
          <p>EMI-to-Income Ratio: <strong>{metrics ? `${metrics.emi_to_income_ratio}%` : "--"}</strong></p>
          <p>Debt-to-Income Ratio: <strong>{metrics ? `${metrics.debt_to_income_ratio}%` : "--"}</strong></p>
        </Card>
      </div>

      <div className="grid grid-2">
        <Card title="Update Financial Profile">
          <form onSubmit={submitProfile} className="stacked-form">
            <label>Monthly Income</label>
            <input
              type="number"
              value={profileForm.monthly_income}
              onChange={(e) => setProfileForm({ ...profileForm, monthly_income: e.target.value })}
              required
            />
            <label>Monthly Expenses</label>
            <input
              type="number"
              value={profileForm.monthly_expenses}
              onChange={(e) => setProfileForm({ ...profileForm, monthly_expenses: e.target.value })}
              required
            />
            <label>Existing Debts</label>
            <input
              type="number"
              value={profileForm.existing_debts}
              onChange={(e) => setProfileForm({ ...profileForm, existing_debts: e.target.value })}
              required
            />
            <button className="btn btn-primary" type="submit">Save Profile</button>
          </form>
        </Card>

        <Card title="Add a Loan">
          <form onSubmit={submitLoan} className="stacked-form">
            <label>Loan Type</label>
            <select
              value={loanForm.loan_type}
              onChange={(e) => setLoanForm({ ...loanForm, loan_type: e.target.value })}
            >
              <option>Credit Card</option>
              <option>Personal Loan</option>
              <option>Auto Loan</option>
              <option>Medical Debt</option>
              <option>Student Loan</option>
              <option>Mortgage</option>
            </select>
            <label>Loan Amount</label>
            <input
              type="number"
              value={loanForm.loan_amount}
              onChange={(e) => setLoanForm({ ...loanForm, loan_amount: e.target.value })}
              required
            />
            <label>Outstanding Amount</label>
            <input
              type="number"
              value={loanForm.outstanding_amount}
              onChange={(e) => setLoanForm({ ...loanForm, outstanding_amount: e.target.value })}
              required
            />
            <label>Interest Rate (%)</label>
            <input
              type="number"
              value={loanForm.interest_rate}
              onChange={(e) => setLoanForm({ ...loanForm, interest_rate: e.target.value })}
              required
            />
            <label>Due Date</label>
            <input
              type="date"
              value={loanForm.due_date}
              onChange={(e) => setLoanForm({ ...loanForm, due_date: e.target.value })}
              required
            />
            <button className="btn btn-primary" type="submit">Add Loan</button>
          </form>
        </Card>
      </div>

      <Card title="Your Loans">
        <table className="data-table">
          <thead>
            <tr>
              <th>Type</th>
              <th>Original Amount</th>
              <th>Outstanding</th>
              <th>Interest Rate</th>
              <th>Due Date</th>
            </tr>
          </thead>
          <tbody>
            {loans.map((loan) => (
              <tr key={loan.loan_id}>
                <td>{loan.loan_type}</td>
                <td>{loan.loan_amount.toFixed(2)}</td>
                <td>{loan.outstanding_amount.toFixed(2)}</td>
                <td>{loan.interest_rate}%</td>
                <td>{new Date(loan.due_date).toLocaleDateString()}</td>
              </tr>
            ))}
            {loans.length === 0 && (
              <tr>
                <td colSpan={5} className="empty-state">No loans added yet.</td>
              </tr>
            )}
          </tbody>
        </table>
      </Card>
    </div>
  );
}
