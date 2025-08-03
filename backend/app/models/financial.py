from sqlalchemy import Column, String, Boolean, DateTime, Enum, ForeignKey, Numeric, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from ..config.database import Base


class AccountType(str, enum.Enum):
    BANK = "bank"
    CASH = "cash"


class TransactionType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"


class TransactionStatus(str, enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    OVERDUE = "overdue"


class CategoryType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"


class FinancialAccount(Base):
    __tablename__ = "financial_accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    name = Column(String, nullable=False)
    type = Column(Enum(AccountType), nullable=False)
    balance = Column(Numeric(15, 2), default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    company = relationship("Company", back_populates="financial_accounts")
    transactions = relationship("FinancialTransaction", back_populates="account")


class FinancialCategory(Base):
    __tablename__ = "financial_categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    name = Column(String, nullable=False)
    type = Column(Enum(CategoryType), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    company = relationship("Company", back_populates="financial_categories")
    transactions = relationship("FinancialTransaction", back_populates="category")


class CostCenter(Base):
    __tablename__ = "cost_centers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    company = relationship("Company", back_populates="cost_centers")
    transactions = relationship("FinancialTransaction", back_populates="cost_center")


class FinancialTransaction(Base):
    __tablename__ = "financial_transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    account_id = Column(UUID(as_uuid=True), ForeignKey("financial_accounts.id"), nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    description = Column(String, nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    due_date = Column(Date, nullable=False)
    payment_date = Column(Date, nullable=True)
    status = Column(Enum(TransactionStatus), default=TransactionStatus.PENDING)
    category_id = Column(UUID(as_uuid=True), ForeignKey("financial_categories.id"), nullable=True)
    cost_center_id = Column(UUID(as_uuid=True), ForeignKey("cost_centers.id"), nullable=True)
    is_recurring = Column(Boolean, default=False)
    recurrence_id = Column(UUID(as_uuid=True), ForeignKey("recurrences.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    company = relationship("Company", back_populates="financial_transactions")
    account = relationship("FinancialAccount", back_populates="transactions")
    category = relationship("FinancialCategory", back_populates="transactions")
    cost_center = relationship("CostCenter", back_populates="transactions")
    recurrence = relationship("Recurrence", back_populates="transactions")

