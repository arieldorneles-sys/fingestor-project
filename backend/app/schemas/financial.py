from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime, date
from uuid import UUID
from decimal import Decimal
from ..models.financial import AccountType, TransactionType, TransactionStatus, CategoryType


class FinancialAccountBase(BaseModel):
    name: str
    type: AccountType
    balance: Optional[Decimal] = Decimal('0')


class FinancialAccountCreate(FinancialAccountBase):
    company_id: UUID


class FinancialAccountUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[AccountType] = None
    balance: Optional[Decimal] = None


class FinancialAccountInDB(FinancialAccountBase):
    id: UUID
    company_id: UUID
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class FinancialAccount(FinancialAccountInDB):
    pass


class FinancialCategoryBase(BaseModel):
    name: str
    type: CategoryType


class FinancialCategoryCreate(FinancialCategoryBase):
    company_id: UUID


class FinancialCategoryUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[CategoryType] = None


class FinancialCategoryInDB(FinancialCategoryBase):
    id: UUID
    company_id: UUID
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class FinancialCategory(FinancialCategoryInDB):
    pass


class CostCenterBase(BaseModel):
    name: str


class CostCenterCreate(CostCenterBase):
    company_id: UUID


class CostCenterUpdate(BaseModel):
    name: Optional[str] = None


class CostCenterInDB(CostCenterBase):
    id: UUID
    company_id: UUID
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class CostCenter(CostCenterInDB):
    pass


class FinancialTransactionBase(BaseModel):
    description: str
    amount: Decimal
    due_date: date
    type: TransactionType
    account_id: UUID
    category_id: Optional[UUID] = None
    cost_center_id: Optional[UUID] = None
    is_recurring: Optional[bool] = False
    
    @validator('amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Amount must be greater than zero')
        return v


class FinancialTransactionCreate(FinancialTransactionBase):
    company_id: UUID


class FinancialTransactionUpdate(BaseModel):
    description: Optional[str] = None
    amount: Optional[Decimal] = None
    due_date: Optional[date] = None
    payment_date: Optional[date] = None
    status: Optional[TransactionStatus] = None
    account_id: Optional[UUID] = None
    category_id: Optional[UUID] = None
    cost_center_id: Optional[UUID] = None
    
    @validator('amount')
    def validate_amount(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Amount must be greater than zero')
        return v


class FinancialTransactionInDB(FinancialTransactionBase):
    id: UUID
    company_id: UUID
    payment_date: Optional[date]
    status: TransactionStatus
    recurrence_id: Optional[UUID]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class FinancialTransaction(FinancialTransactionInDB):
    account: Optional[FinancialAccount] = None
    category: Optional[FinancialCategory] = None
    cost_center: Optional[CostCenter] = None


class TaxSimulationBase(BaseModel):
    revenue: Decimal
    tax_regime: str  # 'simples_nacional' ou 'lucro_presumido'
    
    @validator('revenue')
    def validate_revenue(cls, v):
        if v <= 0:
            raise ValueError('Revenue must be greater than zero')
        return v
    
    @validator('tax_regime')
    def validate_tax_regime(cls, v):
        if v not in ['simples_nacional', 'lucro_presumido']:
            raise ValueError('Tax regime must be simples_nacional or lucro_presumido')
        return v


class TaxSimulationCreate(TaxSimulationBase):
    company_id: UUID


class TaxSimulationInDB(TaxSimulationBase):
    id: UUID
    company_id: UUID
    simulated_taxes: dict
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class TaxSimulation(TaxSimulationInDB):
    pass

