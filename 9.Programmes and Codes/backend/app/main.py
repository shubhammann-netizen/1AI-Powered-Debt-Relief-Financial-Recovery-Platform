"""
main.py
FinRelief AI - AI Powered Debt Relief & Financial Recovery Platform
FastAPI application entry point. Wires up CORS, database table creation,
and all feature routers.

Run locally with:
    uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routers import auth_routes, loans, financial, settlement, negotiation, history

# Create all tables on startup (SQLite dev database)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FinRelief AI",
    description="AI Powered Debt Relief & Financial Recovery Platform API",
    version="1.0.0",
)

# Allow the Vite dev server (and any origin in development) to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(loans.router)
app.include_router(financial.router)
app.include_router(settlement.router)
app.include_router(negotiation.router)
app.include_router(history.router)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "service": "FinRelief AI API", "version": "1.0.0"}
