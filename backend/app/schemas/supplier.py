from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime
from uuid import UUID
from ..utils.validators import validate_document, validate_email, validate_phone


class SupplierBase(BaseModel):
    name: str
    document: str
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    
    @validator('document')
    def validate_document_format(cls, v):
        if not validate_document(v):
            raise ValueError('Invalid CPF/CNPJ format')
        return v
    
    @validator('email')
    def validate_email_format(cls, v):
        if v and not validate_email(v):
            raise ValueError('Invalid email format')
        return v
    
    @validator('phone')
    def validate_phone_format(cls, v):
        if v and not validate_phone(v):
            raise ValueError('Invalid phone format')
        return v


class SupplierCreate(SupplierBase):
    company_id: UUID


class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    document: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    
    @validator('document')
    def validate_document_format(cls, v):
        if v and not validate_document(v):
            raise ValueError('Invalid CPF/CNPJ format')
        return v
    
    @validator('email')
    def validate_email_format(cls, v):
        if v and not validate_email(v):
            raise ValueError('Invalid email format')
        return v
    
    @validator('phone')
    def validate_phone_format(cls, v):
        if v and not validate_phone(v):
            raise ValueError('Invalid phone format')
        return v


class SupplierInDB(SupplierBase):
    id: UUID
    company_id: UUID
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class Supplier(SupplierInDB):
    pass

