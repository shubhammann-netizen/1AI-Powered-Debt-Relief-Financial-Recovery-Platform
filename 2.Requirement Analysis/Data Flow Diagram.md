*FinRelief AI — AI Powered Debt Relief & Financial Recovery Platform*

# Data Flow Diagram
*Level 0/1 data flow for the FinRelief AI platform*

---

## External Entities

- Borrower (via React frontend)
- Google Gemini API (external AI service)

## Level 0 — Context

Borrower <-> React Frontend <-> FastAPI Backend <-> SQLite Database, with the FastAPI Backend making an outbound call to the Google Gemini API for negotiation content generation (falling back to a local rule-based generator on failure).

## Level 1 Process — Authentication

Borrower credentials -> /auth/register or /auth/login -> Users table (Werkzeug password hash) -> JWT access token returned to frontend -> stored and attached to every subsequent request via Axios interceptors.

## Level 1 Process — Loan & Financial Profile Management

Borrower input -> /loans and /financial/profile endpoints -> validated via Pydantic schemas -> persisted to Loans and Financial_Profiles tables -> Financial Engine recalculates metrics -> returned to the Dashboard.

## Level 1 Process — Settlement Prediction

Loan + Financial_Profile data -> Settlement Engine (settlement_engine.py) -> settlement percentage, recommended amount, and priority level computed -> stored in Settlement_Records -> returned to the Settlement Predictor page.

## Level 1 Process — AI Negotiation

Loan + Financial_Profile + Settlement data -> ai_engine.py -> Gemini API call (or rule-based fallback) -> negotiation_strategy, settlement_letter, ai_response -> stored in AI_History -> returned to the Negotiation Email and History pages.

## Referenced Diagram

See the entity-relationship structure in the ER Diagram summary referenced from the project workspace (FinRelief ER Diagram).

---

*Prepared by Sivamanikanta Maddineni | AP24110010763 | sivamanikanta_maddineni@srmap.edu.in*
