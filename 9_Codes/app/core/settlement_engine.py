"""
Settlement Prediction System
-----------------------------
Calculates optimal settlement percentages and risk categories for a loan
based on outstanding amount, overdue months, loan type, and the
borrower's financial health score.
"""
from typing import Dict


LOAN_TYPE_BASE_DISCOUNT = {
    "credit_card": 0.45,
    "personal_loan": 0.35,
    "medical_loan": 0.50,
    "auto_loan": 0.20,
    "education_loan": 0.15,
    "other": 0.30,
}


def predict_settlement(outstanding_amount: float, overdue_months: int,
                        loan_type: str, financial_health_score: float) -> Dict:
    """
    Returns a dict with:
      - settlement_prediction: "Likely" / "Possible" / "Unlikely"
      - recommended_amount: suggested settlement figure
      - priority_level: High / Medium / Low
    """
    base_discount = LOAN_TYPE_BASE_DISCOUNT.get(loan_type.lower().replace(" ", "_"), 0.30)

    # More overdue months + lower financial health => lender more willing to settle
    overdue_factor = min(overdue_months / 24, 1.0) * 0.20
    health_factor = (100 - financial_health_score) / 100 * 0.15

    total_discount = min(base_discount + overdue_factor + health_factor, 0.70)
    recommended_amount = round(outstanding_amount * (1 - total_discount), 2)

    if total_discount >= 0.45:
        prediction = "Likely"
    elif total_discount >= 0.25:
        prediction = "Possible"
    else:
        prediction = "Unlikely"

    if overdue_months > 6 or financial_health_score < 40:
        priority = "High"
    elif overdue_months > 2 or financial_health_score < 65:
        priority = "Medium"
    else:
        priority = "Low"

    return {
        "settlement_prediction": prediction,
        "recommended_amount": recommended_amount,
        "priority_level": priority,
        "discount_percentage": round(total_discount * 100, 2),
    }
