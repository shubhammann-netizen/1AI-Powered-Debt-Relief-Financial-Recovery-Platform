"""
seed_demo_data.py
Convenience script for the "Project Demo Planning" / demonstration phase.
Populates the local SQLite database with one demo borrower, a few loans,
and a financial profile, so the dashboard has data to show immediately
after cloning the repository.

Usage (from the backend/ directory, with the virtual environment active):
    python ../scripts/seed_demo_data.py
"""

import sys
import os
from datetime import datetime, timedelta

# Allow running this script from the scripts/ folder while importing the
# backend "app" package.
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.database import SessionLocal, Base, engine  # noqa: E402
from app.models import User, Loan, FinancialProfile  # noqa: E402
from app.auth import hash_password  # noqa: E402
from app.financial_engine import calculate_financial_metrics  # noqa: E402

Base.metadata.create_all(bind=engine)


def run():
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == "demo@finrelief.ai").first()
        if existing:
            print("Demo user already exists (demo@finrelief.ai). Skipping seed.")
            return

        user = User(
            name="Demo Borrower",
            email="demo@finrelief.ai",
            password=hash_password("Demo@1234"),
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        loans = [
            Loan(
                user_id=user.user_id,
                loan_type="Credit Card",
                loan_amount=5000,
                outstanding_amount=4200,
                interest_rate=24.0,
                due_date=datetime.utcnow() - timedelta(days=45),
            ),
            Loan(
                user_id=user.user_id,
                loan_type="Personal Loan",
                loan_amount=12000,
                outstanding_amount=9800,
                interest_rate=14.5,
                due_date=datetime.utcnow() - timedelta(days=10),
            ),
            Loan(
                user_id=user.user_id,
                loan_type="Auto Loan",
                loan_amount=18000,
                outstanding_amount=15000,
                interest_rate=9.0,
                due_date=datetime.utcnow() + timedelta(days=20),
            ),
        ]
        db.add_all(loans)

        profile = FinancialProfile(
            user_id=user.user_id,
            monthly_income=3200,
            monthly_expenses=2100,
            existing_debts=29000,
        )
        db.add(profile)
        db.commit()

        metrics = calculate_financial_metrics(profile, loans)
        profile.financial_health_score = metrics["financial_health_score"]
        db.commit()

        print("Seeded demo user: demo@finrelief.ai / Demo@1234")
        print(f"Financial health score: {profile.financial_health_score}")
    finally:
        db.close()


if __name__ == "__main__":
    run()
