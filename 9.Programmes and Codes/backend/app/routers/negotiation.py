"""
routers/negotiation.py
Triggers AI-powered negotiation strategy and settlement letter generation
for a given loan, storing the result in AI_History for later review on the
History page.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Loan, FinancialProfile, User, AIHistory
from ..schemas import NegotiationRequest, NegotiationOut
from ..auth import get_current_user
from ..settlement_engine import predict_settlement
from ..ai_engine import generate_negotiation_package

router = APIRouter(prefix="/negotiation", tags=["AI Negotiation"])


@router.post("/generate", response_model=NegotiationOut)
def generate_negotiation(
    payload: NegotiationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    loan = (
        db.query(Loan)
        .filter(Loan.loan_id == payload.loan_id, Loan.user_id == current_user.user_id)
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
            status_code=400, detail="Create a financial profile before generating a negotiation"
        )

    settlement = predict_settlement(loan, profile)
    package = generate_negotiation_package(
        loan=loan,
        profile=profile,
        settlement=settlement,
        borrower_name=current_user.name,
        lender_name=payload.lender_name or "the lender",
        tone=payload.tone or "professional",
    )

    history = AIHistory(
        user_id=current_user.user_id,
        negotiation_strategy=package["negotiation_strategy"],
        settlement_letter=package["settlement_letter"],
        ai_response=package["ai_response"],
    )
    db.add(history)
    db.commit()
    db.refresh(history)
    return history
