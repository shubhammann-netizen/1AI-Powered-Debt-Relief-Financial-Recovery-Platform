"""
routers/financial.py
Endpoints for creating/updating a borrower's financial profile and fetching
computed financial health metrics (EMI ratio, DTI ratio, surplus, stress
level) used by the dashboard visualizations.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import FinancialProfile, Loan, User
from ..schemas import FinancialProfileIn, FinancialProfileOut, FinancialMetricsOut
from ..auth import get_current_user
from ..financial_engine import calculate_financial_metrics

router = APIRouter(prefix="/financial", tags=["Financial Profile"])


@router.post("/profile", response_model=FinancialProfileOut)
def upsert_profile(
    payload: FinancialProfileIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile = (
        db.query(FinancialProfile)
        .filter(FinancialProfile.user_id == current_user.user_id)
        .first()
    )
    if profile is None:
        profile = FinancialProfile(user_id=current_user.user_id, **payload.dict())
        db.add(profile)
    else:
        profile.monthly_income = payload.monthly_income
        profile.monthly_expenses = payload.monthly_expenses
        profile.existing_debts = payload.existing_debts

    loans = db.query(Loan).filter(Loan.user_id == current_user.user_id).all()
    metrics = calculate_financial_metrics(profile, loans)
    profile.financial_health_score = metrics["financial_health_score"]

    db.commit()
    db.refresh(profile)
    return profile


@router.get("/metrics", response_model=FinancialMetricsOut)
def get_metrics(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    profile = (
        db.query(FinancialProfile)
        .filter(FinancialProfile.user_id == current_user.user_id)
        .first()
    )
    if profile is None:
        return FinancialMetricsOut(
            emi_to_income_ratio=0,
            debt_to_income_ratio=0,
            monthly_surplus=0,
            total_outstanding_debt=0,
            stress_level="Low",
            financial_health_score=0,
        )

    loans = db.query(Loan).filter(Loan.user_id == current_user.user_id).all()
    metrics = calculate_financial_metrics(profile, loans)
    return FinancialMetricsOut(**metrics)
