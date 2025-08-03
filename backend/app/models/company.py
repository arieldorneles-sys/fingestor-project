from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from ..config.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    cnpj = Column(String(14), unique=True, index=True, nullable=False)
    address = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    plan_id = Column(String(36), ForeignKey("plans.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    users = relationship("User", back_populates="company")
    plan = relationship("Plan", back_populates="companies")
    customers = relationship("Customer", back_populates="company")
    suppliers = relationship("Supplier", back_populates="company")
    financial_accounts = relationship("FinancialAccount", back_populates="company")
    financial_transactions = relationship("FinancialTransaction", back_populates="company")
    financial_categories = relationship("FinancialCategory", back_populates="company")
    cost_centers = relationship("CostCenter", back_populates="company")
    invoices = relationship("Invoice", back_populates="company")
    billings = relationship("Billing", back_populates="company")
    sale_orders = relationship("SaleOrder", back_populates="company")
    recurrences = relationship("Recurrence", back_populates="company")
    bank_reconciliations = relationship("BankReconciliation", back_populates="company")
    accounting_integrations = relationship("AccountingIntegration", back_populates="company")
    tax_simulations = relationship("TaxSimulation", back_populates="company")
