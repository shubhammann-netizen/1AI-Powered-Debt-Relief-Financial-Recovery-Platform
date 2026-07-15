// src/components/Navbar.jsx
import React from "react";
import { Link, useNavigate } from "react-router-dom";

export default function Navbar() {
  const navigate = useNavigate();

  function handleLogout() {
    localStorage.removeItem("finrelief_token");
    navigate("/login");
  }

  return (
    <nav className="navbar">
      <div className="navbar-brand">FinRelief AI</div>
      <div className="navbar-links">
        <Link to="/">Dashboard</Link>
        <Link to="/settlement">Settlement Predictor</Link>
        <Link to="/negotiation">Negotiation Email</Link>
        <Link to="/rights">Know Your Rights</Link>
        <Link to="/history">History</Link>
      </div>
      <button className="btn btn-secondary" onClick={handleLogout}>
        Logout
      </button>
    </nav>
  );
}
