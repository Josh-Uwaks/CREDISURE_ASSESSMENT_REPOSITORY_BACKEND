from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.schemas.loan import LoanRequest, LoanResponse
from app.services.loan_service import create_loan_application, get_user_loans

router = APIRouter(prefix="/loans", tags=["Loans"])


@router.post("/", response_model=LoanResponse)
def apply_for_loan(
    payload: LoanRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    loan = create_loan_application(
        db,
        current_user["user_id"],
        payload
    )

    return loan

@router.get("/", response_model=List[LoanResponse])
def get_loans(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    loans = get_user_loans(db, current_user["user_id"])
    return loans