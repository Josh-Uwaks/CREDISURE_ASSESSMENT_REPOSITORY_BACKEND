from pydantic import BaseModel


class AssessmentRequest(BaseModel):
    monthly_income: float
    monthly_expense: float
    existing_loans: float


class AssessmentResult(BaseModel):
    credit_score: int
    rating: str
    risk_level: str


class AssessmentResponse(BaseModel):
    user_id: int
    assessment: AssessmentResult