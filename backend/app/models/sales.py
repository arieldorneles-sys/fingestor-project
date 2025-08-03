from sqlalchemy import Column, String, DateTime, Enum, ForeignKey, Numeric, Date, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from ..config.database import Base


class SaleOrderStatus(str, enum.Enum):
    DRAFT = "draft"
    PENDING = "pending"
    APPROVED = "approved"
    CANCELLED = "cancelled"


class RecurrenceType(str, enum.Enum):
    FINANCIAL_TRANSACTION = "financial_transaction"
    SALE_CONTRACT = "sale_contract"


class RecurrenceFrequency(str, enum.Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class SaleOrder(Base):
    __tablename__ = "sale_orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    order_number = Column(String, nullable=False)
    issue_date = Column(Date, nullable=False)
    total_amount = Column(Numeric(15, 2), nullable=False)
    status = Column(Enum(SaleOrderStatus), default=SaleOrderStatus.DRAFT)
    items = Column(JSON, nullable=True)  # Lista de itens do pedido
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    company = relationship("Company", back_populates="sale_orders")
    customer = relationship("Customer", back_populates="sale_orders")
    items_detail = relationship("SaleOrderItem", back_populates="sale_order")


class SaleOrderItem(Base):
    __tablename__ = "sale_order_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sale_order_id = Column(UUID(as_uuid=True), ForeignKey("sale_orders.id"), nullable=False)
    product_service = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(15, 2), nullable=False)
    total_price = Column(Numeric(15, 2), nullable=False)

    # Relationships
    sale_order = relationship("SaleOrder", back_populates="items_detail")


class Recurrence(Base):
    __tablename__ = "recurrences"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    type = Column(Enum(RecurrenceType), nullable=False)
    frequency = Column(Enum(RecurrenceFrequency), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    next_occurrence = Column(Date, nullable=False)
    details = Column(JSON, nullable=True)  # Detalhes específicos da recorrência
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    company = relationship("Company", back_populates="recurrences")
    transactions = relationship("FinancialTransaction", back_populates="recurrence")

