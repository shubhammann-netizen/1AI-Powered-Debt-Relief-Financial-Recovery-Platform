# FinRelief AI — AI Powered Debt Relief & Financial Recovery Platform

FinRelief AI helps borrowers understand their financial health, predicts
realistic loan settlement outcomes, and generates AI-powered negotiation
strategies and lender-specific letters — all through a secure, responsive
full-stack web application.

## Team
| Name | Roll Number | Email |
|------|-------------|-------|
| G Suresh Yadav | AP24122230018 | suresh_gandu@srmap.edu.in |
| Shubham Mann | AP24110011487 | Shubham_mann@srmap.edu.in |

## Tech Stack
- **Frontend:** React.js, Vite, React Router, Axios, Recharts
- **Backend:** Python 3.11+, FastAPI, Uvicorn
- **Database:** SQLAlchemy ORM + SQLite (dev) / PostgreSQL-ready
- **AI:** Google Gemini API with a rule-based fallback engine
- **Auth:** JWT (python-jose) + Werkzeug password hashing

## Project Structure
```
FinReliefAI/
├── app/                          # FastAPI backend
│   ├── main.py                   # App entrypoint
│   ├── database.py               # SQLAlchemy engine/session
│   ├── models/                   # ORM models (ER diagram entities)
│   ├── schemas/                  # Pydantic request/response schemas
│   ├── core/                     # Business logic
│   │   ├── auth.py               # JWT + password hashing
│   │   ├── financial_engine.py   # EMI/DTI ratios, stress classification
│   │   ├── settlement_engine.py  # Settlement prediction logic
│   │   └── ai_engine.py          # Gemini integration + fallback
│   └── routers/                  # REST API endpoints
├── frontend/                     # React + Vite frontend
│   └── src/
│       ├── pages/                # Login, Dashboard, Predictor, etc.
│       ├── api/client.js         # Axios instance with JWT interceptor
│       └── App.jsx               # App shell & navigation
├── docs/                         # Full project documentation
│   ├── 01_Brainstorming_and_Ideation/
│   ├── 02_Requirement_Analysis/
│   ├── 03_Project_Design_Phase/
│   ├── 04_Project_Planning_Phase/
│   ├── 05_Project_Development_Phase/
│   ├── 06_Project_Testing/
│   ├── 07_Project_Documentation/
│   └── 08_Project_Demonstration/
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## ER Diagram Summary
Five entities: **Users**, **Loans**, **Financial_Profiles**,
**Settlement_Records**, **AI_History**.
- Users → Loans: 1‑to‑Many
- Users → Financial_Profiles: 1‑to‑1
- Users → Settlement_Records: 1‑to‑Many
- Users → AI_History: 1‑to‑Many
- Loans → Settlement_Records: 1‑to‑Many

Full details in `docs/03_Project_Design_Phase/Solution Architecture.md`.

## Getting Started

### 1. Backend Setup
```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
cp .env.example .env         # then fill in JWT_SECRET_KEY and GEMINI_API_KEY

uvicorn app.main:app --reload
```
Backend runs at `http://localhost:8000` — interactive API docs at `/docs`.

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Frontend runs at `http://localhost:5173`.

### 3. Try It Out
1. Register a borrower account.
2. Add one or more loans.
3. Submit your financial profile to see health metrics on the Dashboard.
4. Run a Settlement Prediction on any loan.
5. Generate an AI Negotiation Strategy & Letter (works with or without a
   Gemini API key — falls back to a rule-based engine automatically).

## Key Features
- Secure JWT authentication with hashed passwords
- Multi-loan portfolio tracking
- Real-time financial health metrics & repayment timeline simulation
- AI-driven settlement prediction with priority ranking
- Gemini-powered negotiation strategy & letter generation with automatic
  rule-based fallback
- Dark-themed, responsive dashboard with data visualizations
- Full historical audit trail of AI-generated content
- Borrower Rights & Financial Guidance reference page

## License
This project was developed for academic purposes as part of a full-stack
AI application development program.
