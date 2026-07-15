"""
models.py
SQLAlchemy ORM models implementing the FinRelief AI ER diagram:

    Users (1) ----- (M) Loans
    Users (1) ----- (1) Financial_Profiles
    Users (1) ----- (M) Settlement_Records
    Users (1) ----- (M) AI_History
    Loans (1) ----- (M) Settlement_Records
"""

from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)  # stored as a Werkzeug hash
    created_at = Column(DateTime, default=datetime.utcnow)

    loans = relationship("Loan", back_populates="owner", cascade="all, delete-orphan")
    financial_profile = relationship(
        "FinancialProfile",
        back_populates="owner",
        uselist=False,
        cascade="all, delete-orphan",
    )
    settlement_records = relationship(
        "SettlementRecord", back_populates="owner", cascade="all, delete-orphan"
    )
    ai_history = relationship(
        "AIHistory", back_populates="owner", cascade="all, delete-orphan"
    )


class Loan(Base):
    __tablename__ = "loans"

    loan_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    loan_type = Column(String(80), nullable=False)
    loan_amount = Column(Float, nullable=False)
    outstanding_amount = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=False)
    due_date = Column(DateTime, nullable=False)

    owner = relationship("User", back_populates="loans")
    settlement_records = relationship("SettlementRecord", back_populates="loan")


class FinancialProfile(Base):
    __tablename__ = "financial_profiles"
    __table_args__ = (UniqueConstraint("user_id", name="uq_profile_user"),)

    profile_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    monthly_income = Column(Float, nullable=False)
    monthly_expenses = Column(Float, nullable=False)
    existing_debts = Column(Float, nullable=False)
    financial_health_score = Column(Float, default=0.0)

    owner = relationship("User", back_populates="financial_profile")


class SettlementRecord(Base):
    __tablename__ = "settlement_records"

    settlement_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    loan_id = Column(Integer, ForeignKey("loans.loan_id"), nullable=False)
    settlement_prediction = Column(String(50), nullable=False)
    recommended_amount = Column(Float, nullable=False)
    priority_level = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="settlement_records")
    loan = relationship("Loan", back_populates="settlement_records")


class AIHistory(Base):
    __tablename__ = "ai_history"

    history_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    negotiation_strategy = Column(String, nullable=True)
    settlement_letter = Column(String, nullable=True)
    ai_response = Column(String, nullable=True)
    generated_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="ai_history")
