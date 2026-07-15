// src/components/Card.jsx
import React from "react";

export default function Card({ title, children, accent }) {
  return (
    <div className={`card ${accent ? `card-accent-${accent}` : ""}`}>
      {title && <h3 className="card-title">{title}</h3>}
      <div className="card-body">{children}</div>
    </div>
  );
}
