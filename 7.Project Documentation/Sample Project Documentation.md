*FinRelief AI — AI Powered Debt Relief & Financial Recovery Platform*

# Sample Project Documentation
*Reference documentation summary*

---

## Project Name

FinRelief AI — AI Powered Debt Relief & Financial Recovery Platform

## Author

Sivamanikanta Maddineni (AP24110010763) — sivamanikanta_maddineni@srmap.edu.in

## Purpose

To give individual borrowers a self-serve, AI-assisted way to understand their financial health, predict realistic loan settlements, and generate professional negotiation letters, without requiring a paid financial advisor.

## Entities (ER Model)

- Users — borrower accounts (user_id PK).
- Loans — loan records per borrower (loan_id PK, user_id FK).
- Financial_Profiles — one profile per borrower (profile_id PK, user_id FK, unique).
- Settlement_Records — settlement predictions per loan (settlement_id PK, user_id FK, loan_id FK).
- AI_History — AI-generated negotiation content (history_id PK, user_id FK).

## API Surface

- /auth/register, /auth/login
- /loans/ (GET, POST), /loans/priority, /loans/{id} (DELETE)
- /financial/profile (POST), /financial/metrics (GET)
- /settlement/predict/{loan_id} (POST), /settlement/ (GET)
- /negotiation/generate (POST)
- /history/ (GET)

## Related Documents

See `Requirement Analysis/Data Flow Diagram.md` for the full data flow and `Project Design Phase/Solution Architecture.md` for the system architecture.

---

*Prepared by Sivamanikanta Maddineni | AP24110010763 | sivamanikanta_maddineni@srmap.edu.in*
