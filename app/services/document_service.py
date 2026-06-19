from sqlalchemy.orm import Session
from app.models.document import Document


def get_user_documents(db: Session, user_id: int):
    return (
        db.query(Document)
        .filter(Document.user_id == user_id)
        .order_by(Document.created_at.desc())
        .all()
    )