*FinRelief AI — AI Powered Debt Relief & Financial Recovery Platform*

# Coding & Solution
*Summary of the implemented solution*

---

## Backend Implementation

Implemented with FastAPI and SQLAlchemy. Endpoints are grouped under /auth, /loans, /financial, /settlement, /negotiation, and /history, all documented automatically at /docs via FastAPI's OpenAPI integration.

## Financial Engine Logic

calculate_financial_metrics() estimates a monthly EMI per loan from its outstanding balance, interest rate, and remaining term, sums these across the borrower's loan portfolio, and derives the EMI-to-income ratio, debt-to-income ratio, monthly surplus, and a 0-100 financial health score.

## Settlement Engine Logic

predict_settlement() starts from a loan-type baseline settlement percentage, then reduces it based on months overdue and a low financial health score (both of which typically strengthen the borrower's negotiating position), clamped to a 20%-90% realistic range.

## AI Negotiation Logic

generate_negotiation_package() first attempts a Gemini API call with a structured prompt requesting a JSON response (strategy, letter, summary); on any exception it calls the deterministic fallback generator so the feature never hard-fails.

## Frontend Implementation

Built with React function components and hooks (useState, useEffect). Each dashboard page fetches its own data via the shared Axios client and renders it inside reusable Card components with a consistent dark theme.

---

*Prepared by Sivamanikanta Maddineni | AP24110010763 | sivamanikanta_maddineni@srmap.edu.in*
