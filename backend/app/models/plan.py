from sqlalchemy import Column, String, Integer, Numeric, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from ..config.database import Base

class Plan(Base):
    __tablename__ = "plans"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    max_invoices = Column(Integer, nullable=False)
    max_billings = Column(Integer, nullable=False)
    max_companies = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    features = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    companies = relationship("Company", back_populates="plan")
