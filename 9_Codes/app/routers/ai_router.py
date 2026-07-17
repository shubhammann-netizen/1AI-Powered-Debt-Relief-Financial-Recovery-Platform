from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import Loan, SettlementRecord, AIHistory, User
from app.schemas.schemas import NegotiationRequest, AIHistoryOut
from app.core.auth import get_current_user
from app.core.ai_engine import generate_negotiation_strategy, generate_negotiation_letter

router = APIRouter(prefix="/api/ai", tags=["AI Negotiation"])


@router.post("/negotiate", response_model=AIHistoryOut, status_code=201)
def negotiate(req: NegotiationRequest, db: Session = Depends(get_db),
              current_user: User = Depends(get_current_user)):
    loan = db.query(Loan).filter(
        Loan.loan_id == req.loan_id, Loan.user_id == current_user.user_id
    ).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    settlement = db.query(SettlementRecord).filter(
        SettlementRecord.loan_id == loan.loan_id
    ).order_by(SettlementRecord.created_at.desc()).first()

    recommended_amount = settlement.recommended_amount if settlement else loan.outstanding_amount * 0.7
    priority = settlement.priority_level if settlement else "Medium"

    strategy = generate_negotiation_strategy(
        loan_type=loan.loan_type,
        outstanding_amount=loan.outstanding_amount,
        recommended_amount=recommended_amount,
        priority_level=priority,
    )
    letter = generate_negotiation_letter(
        lender_name=req.lender_name,
        loan_type=loan.loan_type,
        outstanding_amount=loan.outstanding_amount,
        recommended_amount=recommended_amount,
        tone=req.tone,
    )

    history = AIHistory(
        user_id=current_user.user_id,
        negotiation_strategy=strategy,
        settlement_letter=letter,
        ai_response=f"Strategy and letter generated for loan #{loan.loan_id}",
    )
    db.add(history)
    db.commit()
    db.refresh(history)
    return history


@router.get("/history", response_model=List[AIHistoryOut])
def get_history(db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    return db.query(AIHistory).filter(
        AIHistory.user_id == current_user.user_id
    ).order_by(AIHistory.generated_at.desc()).all()
