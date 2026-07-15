"""
routers/history.py
Read-only endpoint listing a borrower's past AI-generated negotiation
strategies and settlement letters, powering the History page.
"""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import AIHistory, User
from ..schemas import NegotiationOut
from ..auth import get_current_user

router = APIRouter(prefix="/history", tags=["AI History"])


@router.get("/", response_model=List[NegotiationOut])
def list_history(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return (
        db.query(AIHistory)
        .filter(AIHistory.user_id == current_user.user_id)
        .order_by(AIHistory.generated_at.desc())
        .all()
    )
