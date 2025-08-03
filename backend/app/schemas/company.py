from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime
from uuid import UUID
from ..utils.validators import validate_cnpj


class CompanyBase(BaseModel):
    name: str
    cnpj: str
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    
    @validator('cnpj')
    def validate_cnpj_format(cls, v):
        if not validate_cnpj(v):
            raise ValueError('Invalid CNPJ format')
        return v


class CompanyCreate(CompanyBase):
    plan_id: UUID


class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    plan_id: Optional[UUID] = None
    is_active: Optional[bool] = None


class CompanyInDB(CompanyBase):
    id: UUID
    plan_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class Company(CompanyInDB):
    pass


class CompanyWithPlan(Company):
    plan: Optional[dict] = None

