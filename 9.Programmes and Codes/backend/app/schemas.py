"""
schemas.py
Pydantic models used by FastAPI to validate incoming requests and shape
outgoing JSON responses. Keeping these separate from the SQLAlchemy models
(models.py) follows the API layering described in the Financial Engine /
API Development stories.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# ---------- Auth ----------

class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(..., min_length=6)


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
    loan_amount: float = Field(..., gt=0)
    outstanding_amount: float = Field(..., ge=0)
    interest_rate: float = Field(..., ge=0)
    due_date: datetime


class LoanOut(BaseModel):
    loan_id: int
    loan_type: str
    loan_amount: float
    outstanding_amount: float
    interest_rate: float
    due_date: datetime

    class Config:
        from_attributes = True


# ---------- Financial Profile ----------

class FinancialProfileIn(BaseModel):
    monthly_income: float = Field(..., gt=0)
    monthly_expenses: float = Field(..., ge=0)
    existing_debts: float = Field(..., ge=0)


class FinancialProfileOut(BaseModel):
    profile_id: int
    monthly_income: float
    monthly_expenses: float
    existing_debts: float
    financial_health_score: float

    class Config:
        from_attributes = True


class FinancialMetricsOut(BaseModel):
    emi_to_income_ratio: float
    debt_to_income_ratio: float
    monthly_surplus: float
    total_outstanding_debt: float
    stress_level: str
    financial_health_score: float


# ---------- Settlement ----------

class SettlementOut(BaseModel):
    settlement_id: int
    loan_id: int
    settlement_prediction: str
    recommended_amount: float
    priority_level: str
    created_at: datetime

    class Config:
        from_attributes = True


# ---------- AI Negotiation ----------

class NegotiationRequest(BaseModel):
    loan_id: int
    lender_name: Optional[str] = "the lender"
    tone: Optional[str] = "professional"


class NegotiationOut(BaseModel):
    history_id: int
    negotiation_strategy: str
    settlement_letter: str
    ai_response: str
    generated_at: datetime

    class Config:
        from_attributes = True
