from typing import Optional

from pydantic import BaseModel
from datetime import date, datetime

class KYCRequest(BaseModel):
    first_name: str
    middle_name: str | None = None
    last_name: str

    title: str | None = None
    gender: str | None = None
    dob: date | None = None

    address: str | None = None
    mobile_no: str | None = None

    country: str | None = None
    state: str | None = None
    city: str | None = None
    postal_code: str | None = None

    id_type: str | None = None
    id_number: str | None = None


class KYCResponse(BaseModel):
    message: str
    kyc_status: str


class KYCStatusResponse(BaseModel):
    exists: bool
    status: str
    submitted_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    full_name: Optional[str] = None