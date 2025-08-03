from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from decimal import Decimal
from datetime import datetime
from ..config.database import get_db
from ..models.user import User
from ..models.financial import (
    FinancialAccount, FinancialTransaction, FinancialCategory, 
    CostCenter, TransactionStatus
)
from ..models.integrations import TaxSimulation, TaxRegime
from ..schemas.financial import (
    FinancialAccountCreate, FinancialAccountUpdate, FinancialAccount as FinancialAccountSchema,
    FinancialTransactionCreate, FinancialTransactionUpdate, FinancialTransaction as FinancialTransactionSchema,
    FinancialCategoryCreate, FinancialCategoryUpdate, FinancialCategory as FinancialCategorySchema,
    CostCenterCreate, CostCenterUpdate, CostCenter as CostCenterSchema,
    TaxSimulationCreate, TaxSimulation as TaxSimulationSchema
)
from ..utils.security import get_current_active_user

router = APIRouter()

# Rotas para Contas Financeiras
@router.get("/accounts/", response_model=List[FinancialAccountSchema])
async def list_accounts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lista contas financeiras da empresa"""
    accounts = db.query(FinancialAccount).filter(
        FinancialAccount.company_id == current_user.company_id
    ).all()
    return accounts


@router.post("/accounts/", response_model=FinancialAccountSchema)
async def create_account(
    account_data: FinancialAccountCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Cria nova conta financeira"""
    db_account = FinancialAccount(
        **account_data.dict(),
        company_id=current_user.company_id
    )
    
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    
    return db_account


@router.put("/accounts/{account_id}", response_model=FinancialAccountSchema)
async def update_account(
    account_id: UUID,
    account_data: FinancialAccountUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Atualiza conta financeira"""
    account = db.query(FinancialAccount).filter(
        FinancialAccount.id == account_id,
        FinancialAccount.company_id == current_user.company_id
    ).first()
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    update_data = account_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(account, field, value)
    
    db.commit()
    db.refresh(account)
    
    return account


@router.delete("/accounts/{account_id}")
async def delete_account(
    account_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Deleta conta financeira"""
    account = db.query(FinancialAccount).filter(
        FinancialAccount.id == account_id,
        FinancialAccount.company_id == current_user.company_id
    ).first()
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    db.delete(account)
    db.commit()
    
    return {"message": "Account deleted successfully"}


# Rotas para Transações Financeiras
@router.get("/transactions/", response_model=List[FinancialTransactionSchema])
async def list_transactions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lista transações financeiras da empresa"""
    transactions = db.query(FinancialTransaction).filter(
        FinancialTransaction.company_id == current_user.company_id
    ).offset(skip).limit(limit).all()
    
    return transactions


@router.post("/transactions/", response_model=FinancialTransactionSchema)
async def create_transaction(
    transaction_data: FinancialTransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Cria nova transação financeira"""
    db_transaction = FinancialTransaction(
        **transaction_data.dict(),
        company_id=current_user.company_id
    )
    
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    
    return db_transaction


@router.put("/transactions/{transaction_id}", response_model=FinancialTransactionSchema)
async def update_transaction(
    transaction_id: UUID,
    transaction_data: FinancialTransactionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Atualiza transação financeira"""
    transaction = db.query(FinancialTransaction).filter(
        FinancialTransaction.id == transaction_id,
        FinancialTransaction.company_id == current_user.company_id
    ).first()
    
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    update_data = transaction_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(transaction, field, value)
    
    db.commit()
    db.refresh(transaction)
    
    return transaction


@router.delete("/transactions/{transaction_id}")
async def delete_transaction(
    transaction_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Deleta transação financeira"""
    transaction = db.query(FinancialTransaction).filter(
        FinancialTransaction.id == transaction_id,
        FinancialTransaction.company_id == current_user.company_id
    ).first()
    
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    db.delete(transaction)
    db.commit()
    
    return {"message": "Transaction deleted successfully"}


@router.post("/transactions/{transaction_id}/pay")
async def pay_transaction(
    transaction_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Marca transação como paga"""
    transaction = db.query(FinancialTransaction).filter(
        FinancialTransaction.id == transaction_id,
        FinancialTransaction.company_id == current_user.company_id
    ).first()
    
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    transaction.status = TransactionStatus.PAID
    transaction.payment_date = datetime.now().date()
    
    db.commit()
    db.refresh(transaction)
    
    return transaction


# Rotas para Categorias
@router.get("/categories/", response_model=List[FinancialCategorySchema])
async def list_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lista categorias financeiras da empresa"""
    categories = db.query(FinancialCategory).filter(
        FinancialCategory.company_id == current_user.company_id
    ).all()
    return categories


@router.post("/categories/", response_model=FinancialCategorySchema)
async def create_category(
    category_data: FinancialCategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Cria nova categoria financeira"""
    db_category = FinancialCategory(
        **category_data.dict(),
        company_id=current_user.company_id
    )
    
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    
    return db_category


# Rotas para Centros de Custo
@router.get("/cost_centers/", response_model=List[CostCenterSchema])
async def list_cost_centers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lista centros de custo da empresa"""
    cost_centers = db.query(CostCenter).filter(
        CostCenter.company_id == current_user.company_id
    ).all()
    return cost_centers


@router.post("/cost_centers/", response_model=CostCenterSchema)
async def create_cost_center(
    cost_center_data: CostCenterCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Cria novo centro de custo"""
    db_cost_center = CostCenter(
        **cost_center_data.dict(),
        company_id=current_user.company_id
    )
    
    db.add(db_cost_center)
    db.commit()
    db.refresh(db_cost_center)
    
    return db_cost_center


# Simulação de Impostos
@router.post("/taxes/simulate", response_model=TaxSimulationSchema)
async def simulate_taxes(
    simulation_data: TaxSimulationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Simula impostos para regime tributário"""
    
    def calculate_simples_nacional(revenue: Decimal) -> dict:
        """Calcula impostos do Simples Nacional"""
        # Tabela simplificada do Simples Nacional 2024
        if revenue <= 180000:
            rate = Decimal('0.06')  # 6%
        elif revenue <= 360000:
            rate = Decimal('0.112')  # 11.2%
        elif revenue <= 720000:
            rate = Decimal('0.135')  # 13.5%
        elif revenue <= 1800000:
            rate = Decimal('0.16')  # 16%
        elif revenue <= 3600000:
            rate = Decimal('0.21')  # 21%
        else:
            rate = Decimal('0.33')  # 33%
        
        total_tax = revenue * rate
        
        return {
            "regime": "Simples Nacional",
            "annual_revenue": float(revenue),
            "tax_rate": float(rate * 100),
            "total_tax": float(total_tax),
            "net_income": float(revenue - total_tax),
            "monthly_tax": float(total_tax / 12),
            "breakdown": {
                "simples_nacional": float(total_tax)
            }
        }
    
    def calculate_lucro_presumido(revenue: Decimal) -> dict:
        """Calcula impostos do Lucro Presumido"""
        # Presunção de lucro de 8% para comércio e 32% para serviços
        presumed_profit_rate = Decimal('0.32')  # Assumindo serviços
        presumed_profit = revenue * presumed_profit_rate
        
        # IRPJ: 15% sobre o lucro presumido + 10% sobre o que exceder R$ 240.000
        irpj_base = min(presumed_profit, Decimal('240000'))
        irpj = irpj_base * Decimal('0.15')
        
        if presumed_profit > 240000:
            irpj += (presumed_profit - Decimal('240000')) * Decimal('0.10')
        
        # CSLL: 9% sobre o lucro presumido
        csll = presumed_profit * Decimal('0.09')
        
        # PIS: 0.65% sobre o faturamento
        pis = revenue * Decimal('0.0065')
        
        # COFINS: 3% sobre o faturamento
        cofins = revenue * Decimal('0.03')
        
        total_tax = irpj + csll + pis + cofins
        
        return {
            "regime": "Lucro Presumido",
            "annual_revenue": float(revenue),
            "presumed_profit": float(presumed_profit),
            "total_tax": float(total_tax),
            "net_income": float(revenue - total_tax),
            "monthly_tax": float(total_tax / 12),
            "breakdown": {
                "irpj": float(irpj),
                "csll": float(csll),
                "pis": float(pis),
                "cofins": float(cofins)
            }
        }
    
    # Calcular impostos baseado no regime
    if simulation_data.tax_regime == "simples_nacional":
        simulated_taxes = calculate_simples_nacional(simulation_data.revenue)
    else:
        simulated_taxes = calculate_lucro_presumido(simulation_data.revenue)
    
    # Salvar simulação no banco
    db_simulation = TaxSimulation(
        company_id=current_user.company_id,
        revenue=simulation_data.revenue,
        tax_regime=TaxRegime(simulation_data.tax_regime),
        simulated_taxes=simulated_taxes
    )
    
    db.add(db_simulation)
    db.commit()
    db.refresh(db_simulation)
    
    return db_simulation


@router.get("/taxes/simulations/", response_model=List[TaxSimulationSchema])
async def list_tax_simulations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lista simulações de impostos da empresa"""
    simulations = db.query(TaxSimulation).filter(
        TaxSimulation.company_id == current_user.company_id
    ).offset(skip).limit(limit).all()
    
    return simulations

