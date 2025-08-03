from sqlalchemy import Column, String, DateTime, Enum, ForeignKey, Numeric, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from ..config.database import Base


class BillingStatus(str, enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"


class Billing(Base):
    __tablename__ = "billings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    due_date = Column(Date, nullable=False)
    barcode = Column(String, nullable=True)
    digitable_line = Column(String, nullable=True)
    status = Column(Enum(BillingStatus), default=BillingStatus.PENDING)
    payment_date = Column(Date, nullable=True)
    external_id = Column(String, nullable=True)  # ID na API externa
    pdf_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    company = relationship("Company", back_populates="billings")
    customer = relationship("Customer", back_populates="billings")

