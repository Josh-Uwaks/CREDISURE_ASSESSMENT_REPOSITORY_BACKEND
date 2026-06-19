import os
import uuid
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas.document import DocumentResponse
from app.services.document_service import get_user_documents
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.document import Document

router = APIRouter(prefix="/upload", tags=["Documents"])

# =========================
# STORAGE PATH (INSIDE APP)
# =========================

APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(APP_DIR, "storage", "uploads")

# create folder if it doesn't exist
os.makedirs(UPLOAD_DIR, exist_ok=True)


# =========================
# UPLOAD ENDPOINT
# =========================
@router.post("/")
def upload_statement(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # prevent filename conflicts
    filename = f"{uuid.uuid4()}_{file.filename}"

    file_path = os.path.join(UPLOAD_DIR, filename)

    # save file
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    # save to DB
    document = Document(
        user_id=current_user["user_id"],
        file_name=file.filename,
        file_path=file_path,
        file_type=file.content_type
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return {
        "message": "File uploaded successfully",
        "document_id": document.id,
        "file_name": document.file_name
    }

@router.get("/", response_model=List[DocumentResponse])
def get_documents(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_user_documents(db, current_user["user_id"])