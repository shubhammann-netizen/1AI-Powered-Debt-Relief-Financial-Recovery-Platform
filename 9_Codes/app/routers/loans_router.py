from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import Loan, User
from app.schemas.schemas import LoanCreate, LoanOut
from app.core.auth import get_current_user

router = APIRouter(prefix="/api/loans", tags=["Loans"])


@router.post("/", response_model=LoanOut, status_code=201)
def create_loan(loan_in: LoanCreate, db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    loan = Loan(user_id=current_user.user_id, **loan_in.dict())
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan


@router.get("/", response_model=List[LoanOut])
def list_loans(db: Session = Depends(get_db),
               current_user: User = Depends(get_current_user)):
    return db.query(Loan).filter(Loan.user_id == current_user.user_id).all()


@router.get("/{loan_id}", response_model=LoanOut)
def get_loan(loan_id: int, db: Session = Depends(get_db),
             current_user: User = Depends(get_current_user)):
    loan = db.query(Loan).filter(
        Loan.loan_id == loan_id, Loan.user_id == current_user.user_id
    ).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan


@router.delete("/{loan_id}", status_code=204)
def delete_loan(loan_id: int, db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    loan = db.query(Loan).filter(
        Loan.loan_id == loan_id, Loan.user_id == current_user.user_id
    ).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    db.delete(loan)
    db.commit()
