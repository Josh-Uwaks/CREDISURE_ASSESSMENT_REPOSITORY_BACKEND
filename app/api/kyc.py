from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.kyc import KYCRequest, KYCResponse, KYCStatusResponse
from app.services.kyc_service import create_kyc, get_kyc_status
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

# -------------------------
# GET KYC STATUS
# -------------------------
@router.get("/status", response_model=KYCStatusResponse)
def kyc_status(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user_id = current_user["user_id"]

    kyc = get_kyc_status(db, user_id)

    if not kyc:
        return {
            "exists": False,
            "status": "not_submitted"
        }

    return {
        "exists": True,
        "status": kyc.kyc_status,
        "submitted_at": kyc.created_at,
        "updated_at": kyc.updated_at,
        "full_name": f"{kyc.first_name} {kyc.last_name}"
    }