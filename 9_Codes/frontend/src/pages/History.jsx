import React, { useEffect, useState } from "react";
import api from "../api/client";

export default function History() {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    api.get("/api/ai/history").then((res) => setHistory(res.data));
  }, []);

  return (
    <div>
      <h2>AI Interaction History</h2>
      {history.length === 0 && <p>No past AI-generated interactions yet.</p>}
      {history.map((h) => (
        <div key={h.history_id} className="card">
          <p style={{ color: "var(--text-secondary)" }}>
            {new Date(h.generated_at).toLocaleString()}
          </p>
          <h3>Strategy</h3>
          <pre style={{ whiteSpace: "pre-wrap" }}>{h.negotiation_strategy}</pre>
          <h3>Letter</h3>
          <pre style={{ whiteSpace: "pre-wrap" }}>{h.settlement_letter}</pre>
        </div>
      ))}
    </div>
  );
}
