import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../api/client";

export default function Register() {
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await api.post("/api/auth/register", form);
      navigate("/login");
    } catch (err) {
      setError(err.response?.data?.detail || "Registration failed");
    }
  };

  return (
    <div className="auth-page">
      <form className="auth-card" onSubmit={handleSubmit}>
        <h2>Create Account</h2>
        {error && <p style={{ color: "#f85149" }}>{error}</p>}
        <input className="form-input" name="name" placeholder="Full Name"
               value={form.name} onChange={handleChange} required />
        <input className="form-input" name="email" type="email" placeholder="Email"
               value={form.email} onChange={handleChange} required />
        <input className="form-input" name="password" type="password" placeholder="Password"
               value={form.password} onChange={handleChange} required />
        <button className="btn-primary" type="submit" style={{ width: "100%" }}>Register</button>
        <p style={{ marginTop: 16 }}>
          Already have an account? <Link to="/login">Login</Link>
        </p>
      </form>
    </div>
  );
}
