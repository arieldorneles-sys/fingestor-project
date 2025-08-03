from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime
from uuid import UUID
from ..models.user import UserRole


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool = True
    role: UserRole = UserRole.COMPANY_USER


class UserCreate(UserBase):
    password: str
    company_id: Optional[UUID] = None
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[UserRole] = None
    company_id: Optional[UUID] = None


class UserInDB(UserBase):
    id: UUID
    is_superuser: bool
    company_id: Optional[UUID]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class User(UserInDB):
    pass


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None

