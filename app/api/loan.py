from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.schemas.loan import LoanRequest, LoanResponse
from app.services.loan_service import create_loan_application

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