from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.assessment import AssessmentRequest, AssessmentResponse
from app.services.assessment_service import calculate_credit_score
from app.core.deps import get_current_user
from app.core.database import get_db
from app.models.assessment import Assessment

router = APIRouter(prefix="/assessment", tags=["Assessment"])


@router.post("/", response_model=AssessmentResponse)
def assess_credit(
    payload: AssessmentRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    result = calculate_credit_score(
        monthly_income=payload.monthly_income,
        monthly_expense=payload.monthly_expense,
        existing_loans=payload.existing_loans
    )

    # ------------------------
    # SAVE TO DATABASE
    # ------------------------
    assessment = Assessment(
        user_id=current_user["user_id"],
        monthly_income=payload.monthly_income,
        monthly_expense=payload.monthly_expense,
        existing_loans=payload.existing_loans,
        credit_score=result["credit_score"],
        rating=result["rating"],
        risk_level=result["risk_level"]
    )

    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    return {
        "user_id": current_user["user_id"],
        "assessment": result
    }

# ------------------------
# HISTORY (PROTECTED ROUTE)
# ------------------------
@router.get("/history")
def get_history(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    records = db.query(Assessment).filter(
        Assessment.user_id == current_user["user_id"]
    ).all()

    return [
        {
            "id": r.id,
            "credit_score": r.credit_score,
            "rating": r.rating,
            "risk_level": r.risk_level,
            "created_at": r.created_at
        }
        for r in records
    ]