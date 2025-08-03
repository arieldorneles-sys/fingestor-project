#!/usr/bin/env python3
"""
Script para criar dados de exemplo no banco de dados
"""

from sqlalchemy.orm import sessionmaker
from app.config.database import engine
from app.models.plan import Plan
from app.models.company import Company
from app.models.user import User, UserRole
from app.models.customer import Customer
from app.models.supplier import Supplier
from app.models.financial import FinancialAccount, FinancialCategory, CostCenter, AccountType, CategoryType
import uuid
from decimal import Decimal

# Criar sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

def create_sample_data():
    """Cria dados de exemplo para desenvolvimento"""
    
    # Criar planos
    basic_plan = Plan(
        name="Básico",
        max_invoices=50,
        max_billings=100,
        max_companies=1,
        price=Decimal("29.90"),
        features=["dashboard", "financeiro", "clientes"]
    )
    
    pro_plan = Plan(
        name="Profissional",
        max_invoices=200,
        max_billings=500,
        max_companies=3,
        price=Decimal("79.90"),
        features=["dashboard", "financeiro", "clientes", "nfe", "boletos"]
    )
    
    premium_plan = Plan(
        name="Premium",
        max_invoices=1000,
        max_billings=2000,
        max_companies=10,
        price=Decimal("149.90"),
        features=["dashboard", "financeiro", "clientes", "nfe", "boletos", "integracao_contabil", "simulacao_impostos"]
    )
    
    db.add_all([basic_plan, pro_plan, premium_plan])
    db.commit()
    
    # Criar empresa de exemplo
    company = Company(
        name="Empresa Exemplo Ltda",
        cnpj="12345678000195",
        address="Rua das Flores, 123 - Centro - São Paulo/SP",
        phone="(11) 99999-9999",
        email="contato@empresaexemplo.com.br",
        plan_id=pro_plan.id
    )
    
    db.add(company)
    db.commit()
    
    # Criar usuário administrador
    admin_user = User(
        email="admin@empresaexemplo.com.br",
        password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # senha: admin123
        first_name="Administrador",
        last_name="Sistema",
        is_active=True,
        is_superuser=True,
        role=UserRole.ADMIN,
        company_id=company.id
    )
    
    # Criar usuário da empresa
    company_user = User(
        email="usuario@empresaexemplo.com.br",
        password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # senha: admin123
        first_name="João",
        last_name="Silva",
        is_active=True,
        is_superuser=False,
        role=UserRole.COMPANY_USER,
        company_id=company.id
    )
    
    db.add_all([admin_user, company_user])
    db.commit()
    
    # Criar contas financeiras
    bank_account = FinancialAccount(
        company_id=company.id,
        name="Banco do Brasil - CC",
        type=AccountType.BANK,
        balance=Decimal("15000.00")
    )
    
    cash_account = FinancialAccount(
        company_id=company.id,
        name="Caixa",
        type=AccountType.CASH,
        balance=Decimal("500.00")
    )
    
    db.add_all([bank_account, cash_account])
    db.commit()
    
    # Criar categorias financeiras
    categories = [
        FinancialCategory(company_id=company.id, name="Vendas", type=CategoryType.INCOME),
        FinancialCategory(company_id=company.id, name="Serviços", type=CategoryType.INCOME),
        FinancialCategory(company_id=company.id, name="Aluguel", type=CategoryType.EXPENSE),
        FinancialCategory(company_id=company.id, name="Salários", type=CategoryType.EXPENSE),
        FinancialCategory(company_id=company.id, name="Fornecedores", type=CategoryType.EXPENSE),
        FinancialCategory(company_id=company.id, name="Marketing", type=CategoryType.EXPENSE),
    ]
    
    db.add_all(categories)
    db.commit()
    
    # Criar centros de custo
    cost_centers = [
        CostCenter(company_id=company.id, name="Administrativo"),
        CostCenter(company_id=company.id, name="Vendas"),
        CostCenter(company_id=company.id, name="Operacional"),
    ]
    
    db.add_all(cost_centers)
    db.commit()
    
    # Criar clientes de exemplo
    customers = [
        Customer(
            company_id=company.id,
            name="Cliente ABC Ltda",
            document="98765432000187",
            address="Av. Paulista, 1000 - Bela Vista - São Paulo/SP",
            phone="(11) 88888-8888",
            email="contato@clienteabc.com.br"
        ),
        Customer(
            company_id=company.id,
            name="João da Silva",
            document="12345678901",
            address="Rua das Palmeiras, 456 - Jardins - São Paulo/SP",
            phone="(11) 77777-7777",
            email="joao@email.com"
        ),
        Customer(
            company_id=company.id,
            name="Empresa XYZ S.A.",
            document="11223344000155",
            address="Rua Comercial, 789 - Centro - Rio de Janeiro/RJ",
            phone="(21) 66666-6666",
            email="financeiro@empresaxyz.com.br"
        ),
    ]
    
    db.add_all(customers)
    db.commit()
    
    # Criar fornecedores de exemplo
    suppliers = [
        Supplier(
            company_id=company.id,
            name="Fornecedor 123 Ltda",
            document="55667788000199",
            address="Rua Industrial, 321 - Distrito Industrial - São Paulo/SP",
            phone="(11) 55555-5555",
            email="vendas@fornecedor123.com.br"
        ),
        Supplier(
            company_id=company.id,
            name="Distribuidora Alpha",
            document="99887766000144",
            address="Av. dos Fornecedores, 654 - Zona Norte - São Paulo/SP",
            phone="(11) 44444-4444",
            email="comercial@alpha.com.br"
        ),
    ]
    
    db.add_all(suppliers)
    db.commit()
    
    print("✅ Dados de exemplo criados com sucesso!")
    print("\n📊 Resumo dos dados criados:")
    print(f"- {len([basic_plan, pro_plan, premium_plan])} planos")
    print(f"- 1 empresa: {company.name}")
    print(f"- 2 usuários (admin@empresaexemplo.com.br e usuario@empresaexemplo.com.br)")
    print(f"- 2 contas financeiras")
    print(f"- {len(categories)} categorias financeiras")
    print(f"- {len(cost_centers)} centros de custo")
    print(f"- {len(customers)} clientes")
    print(f"- {len(suppliers)} fornecedores")
    print("\n🔑 Credenciais de acesso:")
    print("Email: admin@empresaexemplo.com.br")
    print("Senha: admin123")
    print("\nEmail: usuario@empresaexemplo.com.br")
    print("Senha: admin123")

if __name__ == "__main__":
    create_sample_data()
    db.close()

