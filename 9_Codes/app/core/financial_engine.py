"""
Financial Engine Module
------------------------
Implements the borrower financial health calculations described in
Epic 2 / Story 2 of the project workflow:
  - EMI-to-income and debt-to-income ratio calculation
  - Financial stress level classification
  - Loan priority analysis and sorting
  - Simple monthly repayment timeline simulation
"""
from typing import List, Dict


def calculate_ratios(monthly_income: float, monthly_expenses: float,
                      total_outstanding: float) -> Dict[str, float]:
    """Return EMI-to-income and debt-to-income ratios (as percentages)."""
    if monthly_income <= 0:
        return {"emi_to_income_ratio": 0.0, "debt_to_income_ratio": 0.0,
                "monthly_surplus": 0.0}

    monthly_surplus = monthly_income - monthly_expenses
    # Assume ~3% of outstanding debt is the effective monthly obligation
    estimated_emi = total_outstanding * 0.03
    emi_ratio = round((estimated_emi / monthly_income) * 100, 2)
    dti_ratio = round((total_outstanding / (monthly_income * 12)) * 100, 2)

    return {
        "emi_to_income_ratio": emi_ratio,
        "debt_to_income_ratio": dti_ratio,
        "monthly_surplus": round(monthly_surplus, 2),
    }


def classify_stress_level(emi_ratio: float) -> str:
    """Classify borrower stress level based on EMI ratio."""
    if emi_ratio < 30:
        return "Low"
    elif emi_ratio < 55:
        return "Medium"
    return "High"


def financial_health_score(emi_ratio: float, dti_ratio: float,
                            monthly_surplus: float) -> float:
    """Composite 0-100 score: higher is healthier."""
    score = 100 - (emi_ratio * 0.4) - (dti_ratio * 0.4)
    if monthly_surplus < 0:
        score -= 15
    return round(max(0.0, min(100.0, score)), 2)


def loan_priority(loan: dict) -> str:
    """
    Assign High / Medium / Low priority based on overdue duration,
    interest rate, and outstanding balance.
    `loan` expects keys: interest_rate, outstanding_amount, overdue_days
    """
    score = 0
    if loan.get("overdue_days", 0) > 60:
        score += 2
    elif loan.get("overdue_days", 0) > 15:
        score += 1

    if loan.get("interest_rate", 0) > 18:
        score += 2
    elif loan.get("interest_rate", 0) > 10:
        score += 1

    if loan.get("outstanding_amount", 0) > 100000:
        score += 1

    if score >= 4:
        return "High"
    elif score >= 2:
        return "Medium"
    return "Low"


def sort_loans_by_priority(loans: List[dict]) -> List[dict]:
    """Sort loans descending by urgency (High -> Medium -> Low)."""
    priority_rank = {"High": 3, "Medium": 2, "Low": 1}
    for loan in loans:
        loan["priority_level"] = loan_priority(loan)
    return sorted(loans, key=lambda x: priority_rank[x["priority_level"]], reverse=True)


def simulate_repayment_timeline(outstanding_amount: float, monthly_surplus: float,
                                 months: int = 12) -> List[float]:
    """
    Simulate month-by-month balance reduction assuming the borrower applies
    their entire monthly surplus toward the outstanding balance.
    """
    timeline = []
    balance = outstanding_amount
    monthly_payment = max(monthly_surplus, 0)
    for _ in range(months):
        balance = max(0.0, balance - monthly_payment)
        timeline.append(round(balance, 2))
        if balance == 0:
            break
    return timeline
