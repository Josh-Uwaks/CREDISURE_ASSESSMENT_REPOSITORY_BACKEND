import os
import logging
import warnings

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import engine, Base

# =========================
# API ROUTERS (clean imports)
# =========================
from app.api.auth import router as auth_router
from app.api.assessment import router as assessment_router
from app.api.documents import router as documents_router
from app.api.kyc import router as kyc_router
from app.api.loan import router as loan_router

# =========================
# MODELS (ensure metadata load)
# =========================
from app.models import *

# =========================
# ENV CONFIG
# =========================
ENV = os.getenv("ENV", "development")

# =========================
# LOGGING CLEANUP
# =========================
logging.getLogger("passlib").setLevel(logging.ERROR)

warnings.filterwarnings(
    "ignore",
    message=".*bcrypt version.*"
)

# =========================
# FASTAPI APP INIT
# =========================
app = FastAPI(
    title="CrediSure API",
    description="CrediSure Credit Intelligence Platform API",
    version="1.0.0"
)

# =========================
# CORS CONFIG
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        # production frontend URL goes here
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# =========================
# DATABASE INIT (SAFE)
# =========================
# Only auto-create tables in development
Base.metadata.create_all(bind=engine)

# =========================
# REGISTER ROUTES
# =========================
app.include_router(auth_router)
app.include_router(assessment_router)
app.include_router(documents_router)
app.include_router(kyc_router)
app.include_router(loan_router)

# =========================
# HEALTH ROUTES
# =========================
@app.get("/")
async def root():
    return {"message": "CrediSure API is running"}


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "environment": ENV
    }