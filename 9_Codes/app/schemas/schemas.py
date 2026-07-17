"""Pydantic request/response schemas used for input validation."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


# ---------- Auth ----------
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    user_id: int
    name: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---------- Loans ----------
class LoanCreate(BaseModel):
    loan_type: str
    loan_amount: float
    outstanding_amount: float
    interest_rate: float
    due_date: datetime


class LoanOut(LoanCreate):
    loan_id: int
    user_id: int

    class Config:
        from_attributes = True


# ---------- Financial Profile ----------
class FinancialProfileCreate(BaseModel):
    monthly_income: float
    monthly_expenses: float
    existing_debts: float = 0.0


class FinancialProfileOut(FinancialProfileCreate):
    profile_id: int
    user_id: int
    financial_health_score: float

    class Config:
        from_attributes = True


# ---------- Settlement ----------
class SettlementOut(BaseModel):
    settlement_id: int
    user_id: int
    loan_id: int
    settlement_prediction: Optional[str]
    recommended_amount: Optional[float]
    priority_level: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# ---------- AI History ----------
class NegotiationRequest(BaseModel):
    loan_id: int
    lender_name: str = "Lender"
    tone: str = "professional"


class AIHistoryOut(BaseModel):
    history_id: int
    user_id: int
    negotiation_strategy: Optional[str]
    settlement_letter: Optional[str]
    ai_response: Optional[str]
    generated_at: datetime

    class Config:
        from_attributes = True
