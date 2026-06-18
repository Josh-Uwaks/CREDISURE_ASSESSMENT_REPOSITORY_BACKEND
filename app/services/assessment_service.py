def calculate_credit_score(monthly_income: float, monthly_expense: float, existing_loans: float):
    """
    Simple rule-based credit scoring algorithm.

    This simulates how a basic credit risk engine evaluates users
    using income, expenses, and existing debt.

    In a real system, this would be replaced with:
    - ML models
    - Historical credit data
    - Bank transaction analysis
    """

    # Prevent division errors and invalid financial input
    if monthly_income <= 0:
        return {
            "credit_score": 0,
            "rating": "Poor",
            "risk_level": "High Risk"
        }

    # Calculate financial pressure ratios
    # Higher ratios = higher financial risk
    expense_ratio = monthly_expense / monthly_income
    debt_ratio = existing_loans / monthly_income

    # Start from a perfect base score (best-case scenario)
    score = 850

    # Reduce score based on spending behavior
    # More expenses relative to income = higher risk
    score -= expense_ratio * 300

    # Reduce score based on debt burden
    # More existing loans = lower creditworthiness
    score -= debt_ratio * 200

    # Ensure score stays within valid credit range
    score = max(300, min(850, int(score)))

    # Map score to risk categories (business interpretation layer)
    if score >= 750:
        rating = "Very Good"
        risk = "Low Risk"
    elif score >= 650:
        rating = "Good"
        risk = "Medium Risk"
    elif score >= 550:
        rating = "Fair"
        risk = "High Risk"
    else:
        rating = "Poor"
        risk = "Very High Risk"

    # Final structured output for API response
    return {
        "credit_score": score,
        "rating": rating,
        "risk_level": risk
    }