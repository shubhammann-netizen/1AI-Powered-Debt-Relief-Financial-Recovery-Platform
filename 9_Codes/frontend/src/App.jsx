import React from "react";
import { NavLink, Outlet, useNavigate } from "react-router-dom";

export default function App() {
  const navigate = useNavigate();

  const logout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  const linkClass = ({ isActive }) =>
    isActive ? "nav-link active" : "nav-link";

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <h1 className="brand">FinRelief AI</h1>
        <nav>
          <NavLink to="/" end className={linkClass}>Dashboard</NavLink>
          <NavLink to="/settlement-predictor" className={linkClass}>Settlement Predictor</NavLink>
          <NavLink to="/negotiation-email" className={linkClass}>Negotiation Email</NavLink>
          <NavLink to="/know-your-rights" className={linkClass}>Know Your Rights</NavLink>
          <NavLink to="/history" className={linkClass}>History</NavLink>
        </nav>
        <button className="logout-btn" onClick={logout}>Logout</button>
      </aside>
      <main className="content">
        <Outlet />
      </main>
    </div>
  );
}
