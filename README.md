# FinRelief AI — AI Powered Debt Relief & Financial Recovery Platform

FinRelief AI is a full-stack web platform that helps borrowers understand their
financial health, predicts realistic loan settlement amounts, and uses
Google's Gemini API (with an automatic rule-based fallback) to generate
personalized negotiation strategies and lender-ready settlement letters.

**Author:** Sivamanikanta Maddineni
**Student ID:** AP24110010763
**Email:** sivamanikanta_maddineni@srmap.edu.in

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React.js + Vite, Axios, React Router, Recharts |
| Backend | FastAPI (Python 3.10+) |
| Database | SQLite via SQLAlchemy ORM (swappable for PostgreSQL) |
| Authentication | JWT (python-jose) + Werkzeug password hashing |
| AI | Google Gemini API, with a deterministic rule-based fallback engine |

## Repository Structure

This repository is organized by project phase, following the FinRelief AI
development lifecycle, with all runnable source code under
`Programmes and Codes/`:

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
└── Programmes and Codes/
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

## Getting Started

### 1. Backend (FastAPI)

```bash
cd "Programmes and Codes/backend"
python -m venv venv
venv\Scripts\activate            # Windows
# source venv/bin/activate       # macOS/Linux

pip install -r requirements.txt
copy .env.example .env           # Windows: copy, macOS/Linux: cp
# Edit .env and add your GEMINI_API_KEY (optional — falls back gracefully without it)

uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`, with interactive docs
at `http://localhost:8000/docs`.

Optional: seed demo data so the dashboard isn't empty on first run:

```bash
python ../scripts/seed_demo_data.py
```

Demo login: `demo@finrelief.ai` / `Demo@1234`

### 2. Frontend (React + Vite)

```bash
cd "Programmes and Codes/frontend"
npm install
cp .env.example .env             # points VITE_API_BASE_URL at the backend
npm run dev
```

The dashboard will be available at `http://localhost:5173`.

## Core Features

- **Secure authentication** — JWT-based sessions with Werkzeug password hashing.
- **Loan management** — add, list, and prioritize loans (High / Medium / Low).
- **Financial health engine** — EMI-to-income ratio, debt-to-income ratio,
  monthly surplus, and an overall financial health score.
- **Settlement prediction** — data-driven settlement percentage and
  recommended payoff amount per loan.
- **AI negotiation strategy & letters** — Gemini-generated (or rule-based
  fallback) negotiation strategy, lender letter, and plain-language summary.
- **History** — a running log of every AI-generated negotiation package.
- **Know Your Rights** — general borrower-rights and financial-guidance reference.

## Database Design

See `Requirement Analysis/Data Flow Diagram.pdf` and the ER model summary
below. Five entities: `Users`, `Loans`, `Financial_Profiles`,
`Settlement_Records`, and `AI_History`, related as:

- `Users (1) — (M) Loans`
- `Users (1) — (1) Financial_Profiles`
- `Users (1) — (M) Settlement_Records`
- `Users (1) — (M) AI_History`
- `Loans (1) — (M) Settlement_Records`

## Notes on the AI Integration

If `GEMINI_API_KEY` is not set (or the Gemini API call fails for any reason),
`ai_engine.py` automatically switches to a deterministic, rule-based
generator so the negotiation-letter feature keeps working offline or during
API outages — matching the "Fallback Logic Implementation" requirement.

## License

This project was built as an academic project deliverable. Feel free to
fork and extend it for learning purposes.
