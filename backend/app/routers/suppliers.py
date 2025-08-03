from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from ..config.database import get_db
from ..models.user import User
from ..models.supplier import Supplier
from ..schemas.supplier import SupplierCreate, SupplierUpdate, Supplier as SupplierSchema
from ..utils.security import get_current_active_user

router = APIRouter()


@router.get("/", response_model=List[SupplierSchema])
async def list_suppliers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lista fornecedores da empresa do usuário logado"""
    suppliers = db.query(Supplier).filter(
        Supplier.company_id == current_user.company_id
    ).offset(skip).limit(limit).all()
    
    return suppliers


@router.get("/{supplier_id}", response_model=SupplierSchema)
async def get_supplier(
    supplier_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Retorna um fornecedor específico"""
    supplier = db.query(Supplier).filter(
        Supplier.id == supplier_id,
        Supplier.company_id == current_user.company_id
    ).first()
    
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found"
        )
    
    return supplier


@router.post("/", response_model=SupplierSchema)
async def create_supplier(
    supplier_data: SupplierCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Cria um novo fornecedor"""
    # Verificar se o documento já existe na empresa
    existing_supplier = db.query(Supplier).filter(
        Supplier.document == supplier_data.document,
        Supplier.company_id == current_user.company_id
    ).first()
    
    if existing_supplier:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Supplier with this document already exists"
        )
    
    # Criar novo fornecedor
    db_supplier = Supplier(
        **supplier_data.dict(),
        company_id=current_user.company_id
    )
    
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    
    return db_supplier


@router.put("/{supplier_id}", response_model=SupplierSchema)
async def update_supplier(
    supplier_id: UUID,
    supplier_data: SupplierUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Atualiza um fornecedor"""
    supplier = db.query(Supplier).filter(
        Supplier.id == supplier_id,
        Supplier.company_id == current_user.company_id
    ).first()
    
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found"
        )
    
    # Verificar se o novo documento já existe (se foi alterado)
    if supplier_data.document and supplier_data.document != supplier.document:
        existing_supplier = db.query(Supplier).filter(
            Supplier.document == supplier_data.document,
            Supplier.company_id == current_user.company_id,
            Supplier.id != supplier_id
        ).first()
        
        if existing_supplier:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Supplier with this document already exists"
            )
    
    # Atualizar campos
    update_data = supplier_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(supplier, field, value)
    
    db.commit()
    db.refresh(supplier)
    
    return supplier


@router.delete("/{supplier_id}")
async def delete_supplier(
    supplier_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Deleta um fornecedor"""
    supplier = db.query(Supplier).filter(
        Supplier.id == supplier_id,
        Supplier.company_id == current_user.company_id
    ).first()
    
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found"
        )
    
    db.delete(supplier)
    db.commit()
    
    return {"message": "Supplier deleted successfully"}

