// src/pages/KnowYourRights.jsx
// Borrower Rights & Financial Guidance Module: static financial-awareness
// and borrower-rights reference content.

import React from "react";
import Card from "../components/Card.jsx";

const RIGHTS = [
  {
    title: "Right to Accurate Information",
    text: "Borrowers are entitled to clear, accurate information about their loan balance, interest rate, and repayment terms at all times.",
  },
  {
    title: "Right to Fair Communication",
    text: "Collectors must communicate respectfully and are generally restricted from contacting borrowers at unreasonable hours or in a harassing manner.",
  },
  {
    title: "Right to Dispute Errors",
    text: "Borrowers can formally dispute inaccurate debt amounts or reporting errors with the lender or relevant credit bureau.",
  },
  {
    title: "Right to Request Settlement in Writing",
    text: "Any negotiated settlement should be confirmed in writing before payment, to ensure the agreed terms are honored.",
  },
  {
    title: "Right to Financial Privacy",
    text: "Personal and financial information shared with a platform or lender should be handled securely and not disclosed to unauthorized third parties.",
  },
];

export default function KnowYourRights() {
  return (
    <div className="dashboard">
      <h1>Know Your Rights</h1>
      <p className="section-subtitle">
        General borrower-rights guidance to help you navigate debt settlement discussions
        confidently. This is educational information, not legal advice.
      </p>
      <div className="grid grid-2">
        {RIGHTS.map((r) => (
          <Card key={r.title} title={r.title}>
            <p>{r.text}</p>
          </Card>
        ))}
      </div>
    </div>
  );
}
