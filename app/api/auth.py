from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.auth import RegisterSchema, LoginSchema
from app.core.database import get_db
from app.services.auth_service import register_user, authenticate_user

router = APIRouter(prefix="/auth", tags=["Auth"])


# ------------------------
# REGISTER
# ------------------------
@router.post("/register")
def register(payload: RegisterSchema, db: Session = Depends(get_db)):
    user = register_user(
        db,
        email=payload.email,
        password=payload.password
    )

    return {
        "message": "User created successfully",
        "user_id": user.id,
        "email": user.email
    }


# ------------------------
# LOGIN
# ------------------------
@router.post("/login")
def login(payload: LoginSchema, db: Session = Depends(get_db)):
    token = authenticate_user(
        db,
        email=payload.email,
        password=payload.password
    )

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return {
        "access_token": token,
        "token_type": "bearer"
    }