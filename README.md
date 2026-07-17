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
FinReliefAI-Project/
├── README.md                          <- you are here
├── Brainstorming & Ideation/           <- ideation & problem framing docs
├── Requirement Analysis/               <- customer journey, DFD, requirements, stack
├── Project Design Phase/               <- problem-solution fit & architecture
├── Project Planning Phase/             <- sprint/task planning
├── Project Development Phase/          <- code layout & feature-completion notes
├── Project Testing/                    <- performance & QA testing notes
├── Project Documentation/              <- executables list & sample docs
├── Project Demonstration/              <- demo planning & scalability notes
└── Codes/
    ├── backend/                        <- FastAPI application (source of truth for the API)
    │   ├── app/
    │   │   ├── main.py                 <- FastAPI app & router registration
    │   │   ├── database.py             <- SQLAlchemy engine/session
    │   │   ├── models.py               <- ORM models (Users, Loans, Financial_Profiles, ...)
    │   │   ├── schemas.py              <- Pydantic request/response schemas
    │   │   ├── auth.py                 <- JWT + password hashing
    │   │   ├── financial_engine.py     <- EMI/DTI ratios, stress level, loan priority
    │   │   ├── settlement_engine.py    <- settlement % and priority prediction
    │   │   ├── ai_engine.py            <- Gemini negotiation generator + fallback
    │   │   └── routers/                <- auth, loans, financial, settlement, negotiation, history
    │   ├── requirements.txt
    │   └── .env.example
    ├── frontend/                       <- React + Vite dashboard
    │   ├── src/
    │   │   ├── pages/                  <- Login, Register, Dashboard, Settlement Predictor,
    │   │   │                              Negotiation Email, Know Your Rights, History
    │   │   ├── components/             <- Navbar, Card
    │   │   ├── api/axios.js            <- JWT-aware Axios instance
    │   │   └── styles/index.css        <- dark-themed UI
    │   ├── package.json
    │   └── .env.example
    └── scripts/
        └── seed_demo_data.py           <- populates demo borrower/loans for a quick demo
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
