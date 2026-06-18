from app.models.loan_application import LoanApplication


def create_loan_application(db, user_id: int, payload):
    loan = LoanApplication(
        user_id=user_id,
        assessment_id=payload.assessment_id,
        amount=payload.amount,
        purpose=payload.purpose,
        term_months=payload.term_months
    )

    db.add(loan)
    db.commit()
    db.refresh(loan)

    return loan