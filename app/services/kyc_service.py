from sqlalchemy.orm import Session
from app.models.kyc import KYCRecord


def create_kyc(db, user_id, payload):
    kyc = KYCRecord(
        user_id=user_id,
        first_name=payload.first_name,
        middle_name=payload.middle_name,
        last_name=payload.last_name,
        title=payload.title,
        gender=payload.gender,
        date_of_birth=payload.dob,
        address=payload.address,
        mobile_number=payload.mobile_no,
        country=payload.country,
        state=payload.state,
        city=payload.city,
        postal_code=payload.postal_code,
        id_type=payload.id_type,
        id_number=payload.id_number,
    )

    db.add(kyc)
    db.commit()
    db.refresh(kyc)

    return kyc

def get_kyc_status(db: Session, user_id: int):
    return db.query(KYCRecord).filter(
        KYCRecord.user_id == user_id
    ).first()