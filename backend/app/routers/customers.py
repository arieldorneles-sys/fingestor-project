from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from ..config.database import get_db
from ..models.user import User
from ..models.customer import Customer
from ..schemas.customer import CustomerCreate, CustomerUpdate, Customer as CustomerSchema
from ..utils.security import get_current_active_user

router = APIRouter()


@router.get("/", response_model=List[CustomerSchema])
async def list_customers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lista clientes da empresa do usuário logado"""
    customers = db.query(Customer).filter(
        Customer.company_id == current_user.company_id
    ).offset(skip).limit(limit).all()
    
    return customers


@router.get("/{customer_id}", response_model=CustomerSchema)
async def get_customer(
    customer_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Retorna um cliente específico"""
    customer = db.query(Customer).filter(
        Customer.id == customer_id,
        Customer.company_id == current_user.company_id
    ).first()
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    return customer


@router.post("/", response_model=CustomerSchema)
async def create_customer(
    customer_data: CustomerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Cria um novo cliente"""
    # Verificar se o documento já existe na empresa
    existing_customer = db.query(Customer).filter(
        Customer.document == customer_data.document,
        Customer.company_id == current_user.company_id
    ).first()
    
    if existing_customer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Customer with this document already exists"
        )
    
    # Criar novo cliente
    db_customer = Customer(
        **customer_data.dict(),
        company_id=current_user.company_id
    )
    
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    
    return db_customer


@router.put("/{customer_id}", response_model=CustomerSchema)
async def update_customer(
    customer_id: UUID,
    customer_data: CustomerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Atualiza um cliente"""
    customer = db.query(Customer).filter(
        Customer.id == customer_id,
        Customer.company_id == current_user.company_id
    ).first()
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    # Verificar se o novo documento já existe (se foi alterado)
    if customer_data.document and customer_data.document != customer.document:
        existing_customer = db.query(Customer).filter(
            Customer.document == customer_data.document,
            Customer.company_id == current_user.company_id,
            Customer.id != customer_id
        ).first()
        
        if existing_customer:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Customer with this document already exists"
            )
    
    # Atualizar campos
    update_data = customer_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(customer, field, value)
    
    db.commit()
    db.refresh(customer)
    
    return customer


@router.delete("/{customer_id}")
async def delete_customer(
    customer_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Deleta um cliente"""
    customer = db.query(Customer).filter(
        Customer.id == customer_id,
        Customer.company_id == current_user.company_id
    ).first()
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    db.delete(customer)
    db.commit()
    
    return {"message": "Customer deleted successfully"}

