from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.core.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    file_name = Column(String(255))
    file_path = Column(String(500)) 
    file_type = Column(String(50))

    created_at = Column(DateTime, default=datetime.utcnow)