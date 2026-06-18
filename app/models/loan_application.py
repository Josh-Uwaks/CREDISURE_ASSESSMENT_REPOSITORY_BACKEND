from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, TIMESTAMP, Enum
from sqlalchemy.sql import func
from app.core.database import Base


class LoanApplication(Base):
    __tablename__ = "loan_applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=True)

    amount = Column(DECIMAL(15, 2), nullable=False)
    purpose = Column(String(255))
    term_months = Column(Integer, nullable=False)

    application_status = Column(
        Enum("pending", "approved", "rejected", name="loan_status"),
        default="pending"
    )

    created_at = Column(TIMESTAMP, server_default=func.now())