"""
ai_engine.py
Implements the AI Negotiation Strategy Engine and Fallback Logic stories:
  - Analyzes the borrower's financial profile and loan data
  - Generates a personalized settlement strategy and negotiation letter
    using the Google Gemini API when GEMINI_API_KEY is configured
  - Falls back to a deterministic, rule-based generator when the API key
    is missing or the API call fails, so the platform stays usable offline
"""

import os
from typing import Dict

from dotenv import load_dotenv

from .models import Loan, FinancialProfile

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

_gemini_model = None
if GEMINI_API_KEY:
    try:
        import google.generativeai as genai

        genai.configure(api_key=GEMINI_API_KEY)
        _gemini_model = genai.GenerativeModel("gemini-1.5-flash")
    except Exception:
        # Any import/config failure quietly disables Gemini and keeps the
        # rule-based fallback engine active instead of crashing the app.
        _gemini_model = None


def generate_negotiation_package(
    loan: Loan,
    profile: FinancialProfile,
    settlement: Dict,
    borrower_name: str,
    lender_name: str = "the lender",
    tone: str = "professional",
) -> Dict:
    """
    Returns a dict with negotiation_strategy, settlement_letter, and
    ai_response. Tries Gemini first, falls back to rule-based logic.
    """
    if _gemini_model is not None:
        try:
            return _generate_with_gemini(
                loan, profile, settlement, borrower_name, lender_name, tone
            )
        except Exception:
            # API failure (quota, network, invalid key, etc.) - fall back
            pass

    return _generate_with_fallback(
        loan, profile, settlement, borrower_name, lender_name
    )


def _generate_with_gemini(
    loan: Loan,
    profile: FinancialProfile,
    settlement: Dict,
    borrower_name: str,
    lender_name: str,
    tone: str,
) -> Dict:
    prompt = f"""
You are a financial negotiation assistant helping a borrower settle a debt.

Borrower: {borrower_name}
Lender: {lender_name}
Loan type: {loan.loan_type}
Outstanding amount: {loan.outstanding_amount}
Interest rate: {loan.interest_rate}%
Monthly income: {profile.monthly_income}
Monthly expenses: {profile.monthly_expenses}
Financial health score (0-100): {profile.financial_health_score}
Recommended settlement amount: {settlement['recommended_amount']}
Settlement percentage of balance: {settlement.get('settlement_percentage')}%

Write a JSON object with exactly these three keys:
"negotiation_strategy": a short paragraph outlining the negotiation approach,
"settlement_letter": a {tone} letter to the lender proposing the settlement,
"ai_response": a one-paragraph plain-language summary for the borrower.
Return ONLY the JSON object, no markdown formatting.
"""
    response = _gemini_model.generate_content(prompt)
    text = response.text.strip()

    import json

    text = text.replace("```json", "").replace("```", "").strip()
    data = json.loads(text)

    return {
        "negotiation_strategy": data["negotiation_strategy"],
        "settlement_letter": data["settlement_letter"],
        "ai_response": data["ai_response"],
    }


def _generate_with_fallback(
    loan: Loan,
    profile: FinancialProfile,
    settlement: Dict,
    borrower_name: str,
    lender_name: str,
) -> Dict:
    """Deterministic, rule-based generator used when Gemini is unavailable."""
    strategy = (
        f"Given a {settlement['priority_level'].lower()}-priority {loan.loan_type} "
        f"with {settlement.get('months_overdue', 0)} month(s) overdue, open with an offer of "
        f"{settlement['recommended_amount']:.2f} (about {settlement.get('settlement_percentage', 0):.0f}% "
        f"of the outstanding balance). Emphasize documented financial hardship, propose a lump-sum "
        f"or short installment plan, and request written confirmation that the account will be "
        f"reported as 'settled' rather than left in default."
    )

    letter = f"""Dear {lender_name},

I am writing regarding my {loan.loan_type} account with an outstanding balance of
{loan.outstanding_amount:.2f}. Due to a change in my financial circumstances, my
current monthly surplus does not allow me to continue payments at the original
terms.

After reviewing my finances, I would like to propose a settlement of
{settlement['recommended_amount']:.2f} to resolve this account in full. I am able to
pay this amount as a lump sum / short installment plan (please advise your
preferred option) upon written confirmation that this settlement will close the
account and be reported accordingly to the credit bureaus.

I value this relationship and would appreciate the opportunity to resolve this
matter amicably and promptly.

Sincerely,
{borrower_name}"""

    ai_response = (
        f"Based on your {loan.loan_type} balance and financial profile, a settlement "
        f"of around {settlement['recommended_amount']:.2f} "
        f"({settlement.get('settlement_percentage', 0):.0f}% of the outstanding amount) looks "
        f"achievable. This loan has been flagged as {settlement['priority_level']} priority — "
        f"consider negotiating this one first. A draft letter has been generated for you below."
    )

    return {
        "negotiation_strategy": strategy,
        "settlement_letter": letter,
        "ai_response": ai_response,
    }
