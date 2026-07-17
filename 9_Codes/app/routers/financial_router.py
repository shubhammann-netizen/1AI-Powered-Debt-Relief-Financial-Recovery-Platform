from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import FinancialProfile, Loan, User
from app.schemas.schemas import FinancialProfileCreate, FinancialProfileOut
from app.core.auth import get_current_user
from app.core.financial_engine import (
    calculate_ratios, classify_stress_level, financial_health_score,
    simulate_repayment_timeline,
)

router = APIRouter(prefix="/api/financial-profile", tags=["Financial Profile"])


@router.post("/", response_model=FinancialProfileOut, status_code=201)
def upsert_profile(profile_in: FinancialProfileCreate, db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    total_outstanding = sum(
        l.outstanding_amount for l in
        db.query(Loan).filter(Loan.user_id == current_user.user_id).all()
    )
    ratios = calculate_ratios(profile_in.monthly_income, profile_in.monthly_expenses,
                               total_outstanding)
    score = financial_health_score(
        ratios["emi_to_income_ratio"], ratios["debt_to_income_ratio"],
        ratios["monthly_surplus"]
    )

    profile = db.query(FinancialProfile).filter(
        FinancialProfile.user_id == current_user.user_id
    ).first()

    if profile:
        profile.monthly_income = profile_in.monthly_income
        profile.monthly_expenses = profile_in.monthly_expenses
        profile.existing_debts = profile_in.existing_debts
        profile.financial_health_score = score
    else:
        profile = FinancialProfile(
            user_id=current_user.user_id,
            monthly_income=profile_in.monthly_income,
            monthly_expenses=profile_in.monthly_expenses,
            existing_debts=profile_in.existing_debts,
            financial_health_score=score,
        )
        db.add(profile)

    db.commit()
    db.refresh(profile)
    return profile


@router.get("/", response_model=FinancialProfileOut)
def get_profile(db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    profile = db.query(FinancialProfile).filter(
        FinancialProfile.user_id == current_user.user_id
    ).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Financial profile not found")
    return profile


@router.get("/metrics")
def get_metrics(db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    profile = db.query(FinancialProfile).filter(
        FinancialProfile.user_id == current_user.user_id
    ).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Financial profile not found")

    total_outstanding = sum(
        l.outstanding_amount for l in
        db.query(Loan).filter(Loan.user_id == current_user.user_id).all()
    )
    ratios = calculate_ratios(profile.monthly_income, profile.monthly_expenses,
                               total_outstanding)
    stress = classify_stress_level(ratios["emi_to_income_ratio"])
    timeline = simulate_repayment_timeline(total_outstanding, ratios["monthly_surplus"])

    return {
        **ratios,
        "financial_stress_level": stress,
        "financial_health_score": profile.financial_health_score,
        "total_outstanding_debt": total_outstanding,
        "repayment_timeline_projection": timeline,
    }
