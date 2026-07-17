from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import Loan, FinancialProfile, SettlementRecord, User
from app.schemas.schemas import SettlementOut
from app.core.auth import get_current_user
from app.core.settlement_engine import predict_settlement

router = APIRouter(prefix="/api/settlements", tags=["Settlements"])


@router.post("/predict/{loan_id}", response_model=SettlementOut, status_code=201)
def predict(loan_id: int, db: Session = Depends(get_db),
            current_user: User = Depends(get_current_user)):
    loan = db.query(Loan).filter(
        Loan.loan_id == loan_id, Loan.user_id == current_user.user_id
    ).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    profile = db.query(FinancialProfile).filter(
        FinancialProfile.user_id == current_user.user_id
    ).first()
    health_score = profile.financial_health_score if profile else 50.0

    overdue_months = max(0, (datetime.utcnow() - loan.due_date).days // 30)

    result = predict_settlement(
        outstanding_amount=loan.outstanding_amount,
        overdue_months=overdue_months,
        loan_type=loan.loan_type,
        financial_health_score=health_score,
    )

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
def list_settlements(db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    return db.query(SettlementRecord).filter(
        SettlementRecord.user_id == current_user.user_id
    ).all()
