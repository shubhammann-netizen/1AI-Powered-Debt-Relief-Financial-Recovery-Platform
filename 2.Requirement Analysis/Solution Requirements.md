*FinRelief AI — AI Powered Debt Relief & Financial Recovery Platform*

# Solution Requirements
*Functional and non-functional requirements*

---

## Functional Requirements

- Borrowers can register and log in securely (FR-1).
- Borrowers can create, view, and delete loan records (FR-2).
- Borrowers can create/update a single financial profile per account (FR-3).
- System computes EMI-to-income ratio, debt-to-income ratio, monthly surplus, and a financial health score from loan + profile data (FR-4).
- System classifies each loan's negotiation priority as High/Medium/Low (FR-5).
- System predicts a settlement percentage and recommended amount per loan (FR-6).
- System generates an AI negotiation strategy, settlement letter, and summary per loan, using Gemini or a rule-based fallback (FR-7).
- System stores and displays a history of all AI-generated negotiation packages (FR-8).
- System provides static borrower-rights and financial-guidance content (FR-9).

## Non-Functional Requirements

- Security: passwords hashed with Werkzeug; all protected routes require a valid JWT (120-minute expiry).
- Availability: negotiation-letter generation must not fail even if the Gemini API key is missing or the API call errors out (fallback engine).
- Performance: SQLite configured with check_same_thread=False to support concurrent requests during development.
- Usability: a responsive, dark-themed interface usable on desktop and mobile.
- Portability: the SQLAlchemy data layer allows swapping SQLite for PostgreSQL or another RDBMS with minimal code changes.

---

*Prepared by Sivamanikanta Maddineni | AP24110010763 | sivamanikanta_maddineni@srmap.edu.in*
