import React from "react";

const RIGHTS = [
  {
    title: "Right to Fair Communication",
    text: "Lenders and recovery agents must communicate respectfully and cannot use threats, abusive language, or harassment during debt collection.",
  },
  {
    title: "Right to Written Communication",
    text: "You are entitled to request all settlement offers and negotiation terms in writing before agreeing to any repayment plan.",
  },
  {
    title: "Right to Reasonable Contact Hours",
    text: "Debt collectors should only contact you during reasonable hours and cannot contact you excessively or at your workplace without consent.",
  },
  {
    title: "Right to Dispute Incorrect Debt",
    text: "If you believe a debt amount is incorrect, you have the right to formally dispute it and request supporting documentation.",
  },
  {
    title: "Right to Privacy",
    text: "Your financial information cannot be disclosed to third parties, employers, or family members without your consent.",
  },
  {
    title: "Right to Negotiate Settlement",
    text: "You are entitled to propose a reasonable settlement amount based on your financial capacity and negotiate repayment terms.",
  },
];

export default function KnowYourRights() {
  return (
    <div>
      <h2>Know Your Rights</h2>
      <div className="grid">
        {RIGHTS.map((r) => (
          <div key={r.title} className="card">
            <h3>{r.title}</h3>
            <p style={{ color: "var(--text-secondary)" }}>{r.text}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
