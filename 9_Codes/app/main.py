"""
FinRelief AI - AI Powered Debt Relief & Financial Recovery Platform
Backend entrypoint (FastAPI).

Run with:
    uvicorn app.main:app --reload
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import (
    auth_router, loans_router, financial_router, settlement_router, ai_router
)

# Create all tables on startup (SQLite dev convenience; use Alembic for prod)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FinRelief AI",
    description="AI Powered Debt Relief & Financial Recovery Platform API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(loans_router.router)
app.include_router(financial_router.router)
app.include_router(settlement_router.router)
app.include_router(ai_router.router)


@app.get("/")
def root():
    return {
        "message": "FinRelief AI backend is running",
        "docs": "/docs",
    }


@app.get("/api/health")
def health_check():
    return {"status": "ok"}
