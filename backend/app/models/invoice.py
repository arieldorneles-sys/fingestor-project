from sqlalchemy import Column, String, DateTime, Enum, ForeignKey, Numeric, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from ..config.database import Base


class InvoiceType(str, enum.Enum):
    NFE = "nfe"  # Nota Fiscal Eletrônica
    NFSE = "nfse"  # Nota Fiscal de Serviços Eletrônica


class InvoiceStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    CANCELLED = "cancelled"


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    type = Column(Enum(InvoiceType), nullable=False)
    number = Column(String, nullable=False)
    series = Column(String, nullable=False)
    issue_date = Column(DateTime(timezone=True), nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=True)
    supplier_id = Column(UUID(as_uuid=True), ForeignKey("suppliers.id"), nullable=True)
    status = Column(Enum(InvoiceStatus), default=InvoiceStatus.PENDING)
    xml_url = Column(String, nullable=True)
    pdf_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    company = relationship("Company", back_populates="invoices")
    customer = relationship("Customer", back_populates="invoices")
    supplier = relationship("Supplier", back_populates="invoices")

