from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from decimal import Decimal
from ..config.database import get_db
from ..models.user import User
from ..models.financial import FinancialTransaction, TransactionType, TransactionStatus
from ..models.customer import Customer
from ..models.supplier import Supplier
from ..models.invoice import Invoice
from ..models.billing import Billing
from ..utils.security import get_current_active_user

router = APIRouter()


@router.get("/kpis")
async def get_dashboard_kpis(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Retorna KPIs financeiros para o dashboard"""
    
    # Período atual (mês atual)
    now = datetime.now()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    
    # Período anterior (mês anterior)
    start_of_prev_month = (start_of_month - timedelta(days=1)).replace(day=1)
    end_of_prev_month = start_of_month - timedelta(days=1)
    
    company_id = current_user.company_id
    
    # Receitas do mês atual
    current_income = db.query(func.sum(FinancialTransaction.amount)).filter(
        and_(
            FinancialTransaction.company_id == company_id,
            FinancialTransaction.type == TransactionType.INCOME,
            FinancialTransaction.status == TransactionStatus.PAID,
            FinancialTransaction.payment_date >= start_of_month,
            FinancialTransaction.payment_date <= end_of_month
        )
    ).scalar() or Decimal('0')
    
    # Receitas do mês anterior
    prev_income = db.query(func.sum(FinancialTransaction.amount)).filter(
        and_(
            FinancialTransaction.company_id == company_id,
            FinancialTransaction.type == TransactionType.INCOME,
            FinancialTransaction.status == TransactionStatus.PAID,
            FinancialTransaction.payment_date >= start_of_prev_month,
            FinancialTransaction.payment_date <= end_of_prev_month
        )
    ).scalar() or Decimal('0')
    
    # Despesas do mês atual
    current_expenses = db.query(func.sum(FinancialTransaction.amount)).filter(
        and_(
            FinancialTransaction.company_id == company_id,
            FinancialTransaction.type == TransactionType.EXPENSE,
            FinancialTransaction.status == TransactionStatus.PAID,
            FinancialTransaction.payment_date >= start_of_month,
            FinancialTransaction.payment_date <= end_of_month
        )
    ).scalar() or Decimal('0')
    
    # Despesas do mês anterior
    prev_expenses = db.query(func.sum(FinancialTransaction.amount)).filter(
        and_(
            FinancialTransaction.company_id == company_id,
            FinancialTransaction.type == TransactionType.EXPENSE,
            FinancialTransaction.status == TransactionStatus.PAID,
            FinancialTransaction.payment_date >= start_of_prev_month,
            FinancialTransaction.payment_date <= end_of_prev_month
        )
    ).scalar() or Decimal('0')
    
    # Lucro líquido
    current_profit = current_income - current_expenses
    prev_profit = prev_income - prev_expenses
    
    # Margem líquida
    current_margin = (current_profit / current_income * 100) if current_income > 0 else Decimal('0')
    prev_margin = (prev_profit / prev_income * 100) if prev_income > 0 else Decimal('0')
    
    # Contas a receber (pendentes)
    accounts_receivable = db.query(func.sum(FinancialTransaction.amount)).filter(
        and_(
            FinancialTransaction.company_id == company_id,
            FinancialTransaction.type == TransactionType.INCOME,
            FinancialTransaction.status == TransactionStatus.PENDING
        )
    ).scalar() or Decimal('0')
    
    # Contas a pagar (pendentes)
    accounts_payable = db.query(func.sum(FinancialTransaction.amount)).filter(
        and_(
            FinancialTransaction.company_id == company_id,
            FinancialTransaction.type == TransactionType.EXPENSE,
            FinancialTransaction.status == TransactionStatus.PENDING
        )
    ).scalar() or Decimal('0')
    
    # Fluxo de caixa projetado (próximos 30 dias)
    next_30_days = now + timedelta(days=30)
    
    projected_income = db.query(func.sum(FinancialTransaction.amount)).filter(
        and_(
            FinancialTransaction.company_id == company_id,
            FinancialTransaction.type == TransactionType.INCOME,
            FinancialTransaction.status == TransactionStatus.PENDING,
            FinancialTransaction.due_date <= next_30_days
        )
    ).scalar() or Decimal('0')
    
    projected_expenses = db.query(func.sum(FinancialTransaction.amount)).filter(
        and_(
            FinancialTransaction.company_id == company_id,
            FinancialTransaction.type == TransactionType.EXPENSE,
            FinancialTransaction.status == TransactionStatus.PENDING,
            FinancialTransaction.due_date <= next_30_days
        )
    ).scalar() or Decimal('0')
    
    projected_cash_flow = projected_income - projected_expenses
    
    # Contadores
    total_customers = db.query(func.count(Customer.id)).filter(
        Customer.company_id == company_id
    ).scalar() or 0
    
    total_suppliers = db.query(func.count(Supplier.id)).filter(
        Supplier.company_id == company_id
    ).scalar() or 0
    
    total_invoices = db.query(func.count(Invoice.id)).filter(
        Invoice.company_id == company_id
    ).scalar() or 0
    
    total_billings = db.query(func.count(Billing.id)).filter(
        Billing.company_id == company_id
    ).scalar() or 0
    
    # Calcular variações percentuais
    def calculate_variation(current, previous):
        if previous == 0:
            return 100 if current > 0 else 0
        return float((current - previous) / previous * 100)
    
    return {
        "financial_kpis": {
            "revenue": {
                "current": float(current_income),
                "previous": float(prev_income),
                "variation": calculate_variation(current_income, prev_income)
            },
            "expenses": {
                "current": float(current_expenses),
                "previous": float(prev_expenses),
                "variation": calculate_variation(current_expenses, prev_expenses)
            },
            "profit": {
                "current": float(current_profit),
                "previous": float(prev_profit),
                "variation": calculate_variation(current_profit, prev_profit)
            },
            "margin": {
                "current": float(current_margin),
                "previous": float(prev_margin),
                "variation": float(current_margin - prev_margin)
            },
            "accounts_receivable": float(accounts_receivable),
            "accounts_payable": float(accounts_payable),
            "projected_cash_flow": float(projected_cash_flow)
        },
        "counters": {
            "customers": total_customers,
            "suppliers": total_suppliers,
            "invoices": total_invoices,
            "billings": total_billings
        },
        "period": {
            "current_month": start_of_month.strftime("%Y-%m"),
            "previous_month": start_of_prev_month.strftime("%Y-%m")
        }
    }

