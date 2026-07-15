// src/App.jsx
// Top-level router for the FinRelief AI dashboard: Login, Register,
// Dashboard, Settlement Predictor, Negotiation Email, Know Your Rights,
// and History pages, matching the "User Interface Development" story.

import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import Navbar from "./components/Navbar.jsx";
import Login from "./pages/Login.jsx";
import Register from "./pages/Register.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import SettlementPredictor from "./pages/SettlementPredictor.jsx";
import NegotiationEmail from "./pages/NegotiationEmail.jsx";
import KnowYourRights from "./pages/KnowYourRights.jsx";
import History from "./pages/History.jsx";

function isAuthenticated() {
  return Boolean(localStorage.getItem("finrelief_token"));
}

function ProtectedRoute({ children }) {
  return isAuthenticated() ? children : <Navigate to="/login" replace />;
}

export default function App() {
  return (
    <BrowserRouter>
      {isAuthenticated() && <Navbar />}
      <div className="page-container">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/settlement"
            element={
              <ProtectedRoute>
                <SettlementPredictor />
              </ProtectedRoute>
            }
          />
          <Route
            path="/negotiation"
            element={
              <ProtectedRoute>
                <NegotiationEmail />
              </ProtectedRoute>
            }
          />
          <Route path="/rights" element={<ProtectedRoute><KnowYourRights /></ProtectedRoute>} />
          <Route path="/history" element={<ProtectedRoute><History /></ProtectedRoute>} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}
