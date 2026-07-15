"""
financial_engine.py
Implements the Financial Engine Module story:
  - EMI & Debt-to-Income Ratio Calculation
  - Financial Stress Level Classification
  - Loan Priority Analysis
  - Priority-Based Loan Sorting
  - Debt Repayment Timeline Simulation
"""

from typing import List, Dict
from datetime import datetime

from .models import Loan, FinancialProfile


def calculate_financial_metrics(profile: FinancialProfile, loans: List[Loan]) -> Dict:
    """
    Calculates EMI ratio, debt-to-income ratio, monthly surplus, total
    outstanding debt, and an overall financial health score using the
    borrower's income, expenses, and loan portfolio.
    """
    total_outstanding_debt = sum(loan.outstanding_amount for loan in loans)

    # Approximate a monthly EMI obligation per loan (simple amortization proxy)
    def approx_emi(loan: Loan) -> float:
        months_remaining = max((loan.due_date - datetime.utcnow()).days // 30, 1)
        monthly_rate = (loan.interest_rate / 100) / 12
        principal = loan.outstanding_amount
        if monthly_rate == 0:
            return principal / months_remaining
        emi = (principal * monthly_rate * (1 + monthly_rate) ** months_remaining) / (
            ((1 + monthly_rate) ** months_remaining) - 1
        )
        return emi

    total_emi = sum(approx_emi(loan) for loan in loans) if loans else 0.0

    emi_to_income_ratio = round(
        (total_emi / profile.monthly_income) * 100 if profile.monthly_income else 0, 2
    )
    debt_to_income_ratio = round(
        (total_outstanding_debt / (profile.monthly_income * 12)) * 100
        if profile.monthly_income
        else 0,
        2,
    )
    monthly_surplus = round(
        profile.monthly_income - profile.monthly_expenses - total_emi, 2
    )

    stress_level = classify_stress_level(emi_to_income_ratio)

    # Financial health score: 100 minus a weighted penalty for high ratios,
    # floored at 0 and capped at 100.
    penalty = (emi_to_income_ratio * 0.6) + (debt_to_income_ratio * 0.2)
    financial_health_score = max(0.0, min(100.0, round(100 - penalty, 2)))

    return {
        "emi_to_income_ratio": emi_to_income_ratio,
        "debt_to_income_ratio": debt_to_income_ratio,
        "monthly_surplus": monthly_surplus,
        "total_outstanding_debt": round(total_outstanding_debt, 2),
        "stress_level": stress_level,
        "financial_health_score": financial_health_score,
    }


def classify_stress_level(emi_to_income_ratio: float) -> str:
    """Classifies debt stress into Low, Medium, or High based on EMI ratio."""
    if emi_to_income_ratio < 30:
        return "Low"
    elif emi_to_income_ratio < 50:
        return "Medium"
    return "High"


def analyze_loan_priority(loan: Loan) -> str:
    """
    Assigns a priority level (High / Medium / Low) to a loan based on
    overdue duration, interest rate, and EMI burden.
    """
    days_overdue = (datetime.utcnow() - loan.due_date).days
    score = 0

    if days_overdue > 60:
        score += 3
    elif days_overdue > 0:
        score += 2

    if loan.interest_rate >= 18:
        score += 2
    elif loan.interest_rate >= 10:
        score += 1

    if loan.outstanding_amount >= 0.5 * loan.loan_amount:
        score += 1

    if score >= 4:
        return "High"
    elif score >= 2:
        return "Medium"
    return "Low"


def sort_loans_by_priority(loans: List[Loan]) -> List[Loan]:
    """Sorts loans according to financial urgency (High -> Medium -> Low)."""
    order = {"High": 0, "Medium": 1, "Low": 2}
    return sorted(loans, key=lambda loan: order.get(analyze_loan_priority(loan), 3))


def simulate_repayment_timeline(
    outstanding_amount: float,
    interest_rate: float,
    monthly_payment: float,
    max_months: int = 60,
) -> List[Dict]:
    """
    Simulates month-by-month balance reduction given a fixed monthly
    payment, returning a timeline capped at max_months for safety.
    """
    timeline = []
    balance = outstanding_amount
    monthly_rate = (interest_rate / 100) / 12
    month = 0

    while balance > 0 and month < max_months:
        interest_charge = balance * monthly_rate
        principal_payment = max(monthly_payment - interest_charge, 0)
        balance = max(balance - principal_payment, 0)
        month += 1
        timeline.append(
            {
                "month": month,
                "remaining_balance": round(balance, 2),
                "principal_paid": round(principal_payment, 2),
                "interest_paid": round(interest_charge, 2),
            }
        )
        if principal_payment <= 0:
            break  # payment doesn't even cover interest, stop simulating

    return timeline
