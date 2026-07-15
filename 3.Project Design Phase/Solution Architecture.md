*FinRelief AI — AI Powered Debt Relief & Financial Recovery Platform*

# Solution Architecture
*System architecture and component interaction*

---

## Architecture Style

A classic three-tier web architecture: a React.js single-page frontend, a FastAPI REST backend, and a SQLite relational database, with an external call from the backend to the Google Gemini API.

## Component Breakdown

- Frontend (React + Vite): renders the Login, Register, Dashboard, Settlement Predictor, Negotiation Email, Know Your Rights, and History pages; communicates with the backend exclusively over HTTPS/JSON via Axios.
- Backend (FastAPI): exposes REST endpoints grouped by router — auth_routes, loans, financial, settlement, negotiation, history — each backed by Pydantic schemas for validation.
- Financial Engine: pure-Python module computing EMI/DTI ratios, stress level, and loan priority from ORM objects.
- Settlement Engine: pure-Python module computing settlement percentage and priority from loan type, overdue duration, and financial health score.
- AI Engine: wraps the Gemini API call; on any failure (missing key, quota, network error, malformed response) it transparently falls back to a deterministic rule-based generator.
- Database (SQLite via SQLAlchemy): five tables — Users, Loans, Financial_Profiles, Settlement_Records, AI_History — related as described in the ER Diagram.

## Security Architecture

Passwords are hashed with Werkzeug before storage. All protected endpoints require a valid JWT bearer token (120-minute expiry), verified via a FastAPI dependency (get_current_user) on every request.

## Deployment View

The backend can be containerized and deployed behind any ASGI server (uvicorn/gunicorn); the frontend builds to static assets deployable to any static host or CDN; SQLite can be swapped for PostgreSQL by changing DATABASE_URL only.

---

*Prepared by Sivamanikanta Maddineni | AP24110010763 | sivamanikanta_maddineni@srmap.edu.in*
