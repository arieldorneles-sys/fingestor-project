from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Numeric, Enum, Date, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from ..config.database import Base


class ReconciliationStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class FileType(str, enum.Enum):
    OFX = "ofx"
    XLSX = "xlsx"


class ExportType(str, enum.Enum):
    SPED = "sped"
    DRE = "dre"


class TaxRegime(str, enum.Enum):
    SIMPLES_NACIONAL = "simples_nacional"
    LUCRO_PRESUMIDO = "lucro_presumido"


class BankReconciliation(Base):
    __tablename__ = "bank_reconciliations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    account_id = Column(String(36), ForeignKey("financial_accounts.id"), nullable=False)
    file_type = Column(Enum(FileType), nullable=False)
    file_url = Column(String, nullable=False)
    status = Column(Enum(ReconciliationStatus), default=ReconciliationStatus.PENDING)
    reconciled_transactions = Column(JSON, nullable=True)
    unreconciled_transactions = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    company = relationship("Company", back_populates="bank_reconciliations")
    account = relationship("FinancialAccount")


class AccountingIntegration(Base):
    __tablename__ = "accounting_integrations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    accountant_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    export_type = Column(Enum(ExportType), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    file_url = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    company = relationship("Company", back_populates="accounting_integrations")
    accountant = relationship("User")


class TaxSimulation(Base):
    __tablename__ = "tax_simulations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    revenue = Column(Numeric(15, 2), nullable=False)
    tax_regime = Column(Enum(TaxRegime), nullable=False)
    simulated_taxes = Column(JSON, nullable=False)  # Detalhes dos impostos simulados
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    company = relationship("Company", back_populates="tax_simulations")
