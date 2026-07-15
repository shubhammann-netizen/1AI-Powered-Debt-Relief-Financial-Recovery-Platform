// src/pages/History.jsx
// Review past AI outputs: lists AI_History records (negotiation
// strategies, settlement letters, AI responses) with timestamps.

import React, { useEffect, useState } from "react";
import api from "../api/axios.js";
import Card from "../components/Card.jsx";

export default function History() {
  const [items, setItems] = useState([]);

  useEffect(() => {
    api.get("/history/").then((res) => setItems(res.data));
  }, []);

  return (
    <div className="dashboard">
      <h1>AI Interaction History</h1>
      {items.length === 0 && <p className="empty-state">No AI-generated history yet.</p>}
      {items.map((item) => (
        <Card
          key={item.history_id}
          title={new Date(item.generated_at).toLocaleString()}
        >
          <p><strong>Summary:</strong> {item.ai_response}</p>
          <details>
            <summary>View strategy & letter</summary>
            <p><strong>Strategy:</strong> {item.negotiation_strategy}</p>
            <pre className="letter-preview">{item.settlement_letter}</pre>
          </details>
        </Card>
      ))}
    </div>
  );
}
