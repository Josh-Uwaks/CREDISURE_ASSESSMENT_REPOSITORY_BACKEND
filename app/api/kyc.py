from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.kyc import KYCRequest, KYCResponse
from app.services.kyc_service import create_kyc
from app.core.database import SessionLocal
from app.core.deps import get_current_user

router = APIRouter(prefix="/kyc", tags=["KYC"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=KYCResponse)
def submit_kyc(
    payload: KYCRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Only authenticated users can submit KYC
    create_kyc(db, current_user["user_id"], payload)

    return {
        "message": "KYC submitted successfully",
        "kyc_status": "pending"
    }