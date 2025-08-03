from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from ..config.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    name = Column(String, nullable=False)
    document = Column(String, nullable=False)  # CPF/CNPJ
    address = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    company = relationship("Company", back_populates="customers")
    invoices = relationship("Invoice", back_populates="customer")
    billings = relationship("Billing", back_populates="customer")
    sale_orders = relationship("SaleOrder", back_populates="customer")
