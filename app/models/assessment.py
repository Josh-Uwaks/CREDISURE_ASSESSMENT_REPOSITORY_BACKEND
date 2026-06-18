from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from datetime import datetime
from app.core.database import Base


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    monthly_income = Column(Float, nullable=False)
    monthly_expense = Column(Float, nullable=False)
    existing_loans = Column(Float, nullable=False)

    credit_score = Column(Integer, nullable=False)
    rating = Column(String(50), nullable=False)
    risk_level = Column(String(50), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)