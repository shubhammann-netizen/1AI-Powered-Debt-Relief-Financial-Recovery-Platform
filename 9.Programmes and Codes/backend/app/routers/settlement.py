"""
routers/settlement.py
Generates and stores settlement predictions for a specific loan, and lists
past predictions for the dashboard's Settlement Predictor page.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Loan, FinancialProfile, SettlementRecord, User
from ..schemas import SettlementOut
from ..auth import get_current_user
from ..settlement_engine import predict_settlement

router = APIRouter(prefix="/settlement", tags=["Settlement Prediction"])


@router.post("/predict/{loan_id}", response_model=SettlementOut)
def predict(
    loan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    loan = (
        db.query(Loan)
        .filter(Loan.loan_id == loan_id, Loan.user_id == current_user.user_id)
        .first()
    )
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    profile = (
        db.query(FinancialProfile)
        .filter(FinancialProfile.user_id == current_user.user_id)
        .first()
    )
    if not profile:
        raise HTTPException(
            status_code=400, detail="Create a financial profile before predicting settlements"
        )

    result = predict_settlement(loan, profile)

    record = SettlementRecord(
        user_id=current_user.user_id,
        loan_id=loan.loan_id,
        settlement_prediction=result["settlement_prediction"],
        recommended_amount=result["recommended_amount"],
        priority_level=result["priority_level"],
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/", response_model=List[SettlementOut])
def list_settlements(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return (
        db.query(SettlementRecord)
        .filter(SettlementRecord.user_id == current_user.user_id)
        .order_by(SettlementRecord.created_at.desc())
        .all()
    )
