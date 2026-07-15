*FinRelief AI — AI Powered Debt Relief & Financial Recovery Platform*

# Project Executable Files
*How to run FinRelief AI locally*

---

## Backend Entry Point

Programmes and Codes/backend/app/main.py — run with `uvicorn app.main:app --reload` from inside the backend/ directory (after installing requirements.txt into an activated virtual environment).

## Frontend Entry Point

Programmes and Codes/frontend/src/main.jsx — run with `npm install` followed by `npm run dev` from inside the frontend/ directory.

## Supporting Script

Programmes and Codes/scripts/seed_demo_data.py — optional script that seeds a demo borrower (demo@finrelief.ai / Demo@1234) with sample loans and a financial profile so the dashboard is populated on first run.

## Configuration Files

- backend/.env.example — copy to .env and set JWT_SECRET_KEY, GEMINI_API_KEY, and DATABASE_URL.
- frontend/.env.example — copy to .env and set VITE_API_BASE_URL to the backend URL.

## Full Instructions

See the root README.md for the complete step-by-step setup for both the backend and frontend.

---

*Prepared by Sivamanikanta Maddineni | AP24110010763 | sivamanikanta_maddineni@srmap.edu.in*
