"""
AI Negotiation Strategy Engine
--------------------------------
Generates personalised settlement strategies and lender-specific
negotiation letters using Google Gemini. If GEMINI_API_KEY is missing
or the API call fails, a rule-based fallback engine produces a
deterministic result so the platform keeps working end-to-end.
"""
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

_gemini_ready = False
if GEMINI_API_KEY:
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        _gemini_ready = True
    except Exception:
        _gemini_ready = False


def _fallback_strategy(loan_type: str, outstanding_amount: float,
                        recommended_amount: float, priority_level: str) -> str:
    return (
        f"Rule-based negotiation strategy for a {loan_type}:\n"
        f"1. Open by acknowledging the debt of Rs.{outstanding_amount:,.2f} "
        f"and your intent to resolve it in good faith.\n"
        f"2. Propose a one-time settlement of Rs.{recommended_amount:,.2f}, "
        f"citing financial hardship.\n"
        f"3. Given the {priority_level.lower()} priority of this account, "
        f"request a written confirmation before making any payment.\n"
        f"4. If rejected, propose a short-term structured payment plan as an alternative."
    )


def _fallback_letter(lender_name: str, loan_type: str, outstanding_amount: float,
                      recommended_amount: float) -> str:
    return (
        f"Dear {lender_name},\n\n"
        f"I am writing regarding my {loan_type} account with an outstanding balance "
        f"of Rs.{outstanding_amount:,.2f}. Due to financial hardship, I am unable to "
        f"repay the full amount at this time. I would like to propose a one-time "
        f"settlement of Rs.{recommended_amount:,.2f} to close this account in full.\n\n"
        f"I would appreciate a written response confirming this arrangement. "
        f"Thank you for your understanding and cooperation.\n\n"
        f"Sincerely,\nBorrower"
    )


def generate_negotiation_strategy(loan_type: str, outstanding_amount: float,
                                   recommended_amount: float, priority_level: str,
                                   financial_summary: str = "") -> str:
    if not _gemini_ready:
        return _fallback_strategy(loan_type, outstanding_amount,
                                   recommended_amount, priority_level)
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = (
            f"Act as a debt negotiation advisor. Create a concise, professional "
            f"negotiation strategy (numbered steps) for a borrower with a "
            f"{loan_type} of outstanding amount Rs.{outstanding_amount:,.2f}. "
            f"Recommended settlement amount is Rs.{recommended_amount:,.2f}. "
            f"Priority level: {priority_level}. Financial summary: {financial_summary}."
        )
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return _fallback_strategy(loan_type, outstanding_amount,
                                   recommended_amount, priority_level)


def generate_negotiation_letter(lender_name: str, loan_type: str,
                                 outstanding_amount: float,
                                 recommended_amount: float,
                                 tone: str = "professional") -> str:
    if not _gemini_ready:
        return _fallback_letter(lender_name, loan_type, outstanding_amount,
                                 recommended_amount)
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = (
            f"Write a {tone} settlement negotiation letter addressed to "
            f"'{lender_name}' regarding a {loan_type} with an outstanding "
            f"balance of Rs.{outstanding_amount:,.2f}, proposing a one-time "
            f"settlement of Rs.{recommended_amount:,.2f}. Keep it under 200 words."
        )
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return _fallback_letter(lender_name, loan_type, outstanding_amount,
                                 recommended_amount)
