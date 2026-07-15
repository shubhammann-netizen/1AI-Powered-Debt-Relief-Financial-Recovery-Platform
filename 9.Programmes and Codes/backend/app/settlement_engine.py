"""
settlement_engine.py
Implements the Settlement Prediction System story: calculates optimal
settlement percentages and risk categories per loan by analyzing
outstanding amount, overdue months, loan type, and the borrower's
financial profile.
"""

from datetime import datetime
from typing import Dict

from .models import Loan, FinancialProfile

# Baseline settlement percentage by loan type (industry-style heuristics
# used as a starting point before adjustments)
BASE_SETTLEMENT_PCT = {
    "credit card": 45,
    "personal loan": 55,
    "auto loan": 65,
    "medical debt": 40,
    "student loan": 70,
    "mortgage": 75,
}


def predict_settlement(loan: Loan, profile: FinancialProfile) -> Dict:
    """Returns settlement_prediction, recommended_amount, and priority_level."""
    months_overdue = max((datetime.utcnow() - loan.due_date).days // 30, 0)

    base_pct = BASE_SETTLEMENT_PCT.get(loan.loan_type.lower(), 55)

    # More overdue months and lower financial health -> lower settlement ask
    overdue_adjustment = min(months_overdue * 1.5, 20)
    health_adjustment = (
        (50 - profile.financial_health_score) * 0.2
        if profile.financial_health_score < 50
        else 0
    )

    settlement_pct = max(base_pct - overdue_adjustment - health_adjustment, 20)
    settlement_pct = min(settlement_pct, 90)

    recommended_amount = round(loan.outstanding_amount * (settlement_pct / 100), 2)

    if settlement_pct <= 40:
        prediction = "High likelihood of settlement approval"
    elif settlement_pct <= 60:
        prediction = "Moderate likelihood of settlement approval"
    else:
        prediction = "Requires strong negotiation leverage"

    if months_overdue > 6 or profile.financial_health_score < 35:
        priority_level = "High"
    elif months_overdue > 2 or profile.financial_health_score < 60:
        priority_level = "Medium"
    else:
        priority_level = "Low"

    return {
        "settlement_prediction": prediction,
        "recommended_amount": recommended_amount,
        "priority_level": priority_level,
        "settlement_percentage": round(settlement_pct, 2),
        "months_overdue": months_overdue,
    }
