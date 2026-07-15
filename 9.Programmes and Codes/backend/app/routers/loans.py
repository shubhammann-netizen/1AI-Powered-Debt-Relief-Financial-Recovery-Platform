"""
routers/loans.py
CRUD-style endpoints for a borrower's loan portfolio, backed by SQLAlchemy
ORM (Loan model). Also exposes the priority-sorted view of the portfolio.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Loan, User
from ..schemas import LoanCreate, LoanOut
from ..auth import get_current_user
from ..financial_engine import sort_loans_by_priority, analyze_loan_priority

router = APIRouter(prefix="/loans", tags=["Loans"])


@router.post("/", response_model=LoanOut, status_code=201)
def create_loan(
    payload: LoanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    loan = Loan(user_id=current_user.user_id, **payload.dict())
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan


@router.get("/", response_model=List[LoanOut])
def list_loans(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return db.query(Loan).filter(Loan.user_id == current_user.user_id).all()


@router.get("/priority")
def list_loans_by_priority(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    loans = db.query(Loan).filter(Loan.user_id == current_user.user_id).all()
    sorted_loans = sort_loans_by_priority(loans)
    return [
        {
            "loan_id": loan.loan_id,
            "loan_type": loan.loan_type,
            "outstanding_amount": loan.outstanding_amount,
            "priority_level": analyze_loan_priority(loan),
        }
        for loan in sorted_loans
    ]


@router.delete("/{loan_id}", status_code=204)
def delete_loan(
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
    db.delete(loan)
    db.commit()
    return None
