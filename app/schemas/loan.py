from pydantic import BaseModel
from typing import Optional


class LoanRequest(BaseModel):
    amount: float
    purpose: Optional[str] = None
    term_months: int
    assessment_id: Optional[int] = None


class LoanResponse(BaseModel):
    id: int
    amount: float
    purpose: Optional[str]
    term_months: int
    application_status: str

    class Config:
        from_attributes = True