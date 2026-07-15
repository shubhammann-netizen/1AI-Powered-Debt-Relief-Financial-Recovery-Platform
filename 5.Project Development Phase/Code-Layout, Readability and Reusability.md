*FinRelief AI — AI Powered Debt Relief & Financial Recovery Platform*

# Code Layout, Readability and Reusability
*Code organization principles applied in FinRelief AI*

---

## Modular Backend Layout

The backend/app package separates concerns into single-responsibility modules: database.py (connection/session), models.py (ORM schema), schemas.py (I/O validation), auth.py (security), financial_engine.py, settlement_engine.py, and ai_engine.py (business logic), and a routers/ package exposing one router file per feature area.

## Reusability

- financial_engine.py functions (calculate_financial_metrics, classify_stress_level, analyze_loan_priority, sort_loans_by_priority, simulate_repayment_timeline) are pure functions that accept ORM objects and can be reused by any router or script (e.g. seed_demo_data.py).
- ai_engine.py exposes a single generate_negotiation_package() function so the Gemini-vs-fallback decision is made in one place, not duplicated across routers.
- Frontend Card and Navbar components are reused across every dashboard page instead of duplicating layout markup.
- api/axios.js centralizes JWT attachment and 401 handling so every page's API calls share the same authenticated client instead of reimplementing headers per request.

## Readability Conventions

- Every backend module opens with a docstring explaining its responsibility and, where relevant, which user story it implements.
- Pydantic schemas are named consistently (XCreate / XOut / XIn) to make request vs. response types immediately clear.
- CSS uses named custom properties (--bg-primary, --accent, etc.) instead of hard-coded colors scattered through component styles.

---

*Prepared by Sivamanikanta Maddineni | AP24110010763 | sivamanikanta_maddineni@srmap.edu.in*
