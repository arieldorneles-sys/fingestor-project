import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.config.database import get_db, Base
from app.models.user import User
from app.models.company import Company
from app.models.plan import Plan
from app.models.customer import Customer
from app.utils.security import get_password_hash

# Configurar banco de dados de teste
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_customers.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def authenticated_user(test_db):
    # Criar plano
    plan = Plan(
        name="Plano Teste",
        price=99.90,
        max_users=5,
        max_companies=1,
        max_invoices=100,
        max_billings=100
    )
    test_db.add(plan)
    test_db.commit()
    
    # Criar empresa
    company = Company(
        name="Empresa Teste",
        document="12345678000195",
        email="empresa@teste.com",
        plan_id=plan.id
    )
    test_db.add(company)
    test_db.commit()
    
    # Criar usuário
    user = User(
        email="usuario@teste.com",
        first_name="Usuario",
        last_name="Teste",
        hashed_password=get_password_hash("senha123"),
        company_id=company.id,
        is_active=True
    )
    test_db.add(user)
    test_db.commit()
    
    # Fazer login e obter token
    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": user.email,
            "password": "senha123"
        }
    )
    token = login_response.json()["access_token"]
    
    return {
        "user": user,
        "company": company,
        "token": token,
        "headers": {"Authorization": f"Bearer {token}"}
    }

def test_create_customer(setup_database, authenticated_user):
    """Teste de criação de cliente"""
    customer_data = {
        "name": "Cliente Teste",
        "document": "12345678901",
        "email": "cliente@teste.com",
        "phone": "(11) 99999-9999",
        "address": "Rua Teste, 123"
    }
    
    response = client.post(
        "/api/v1/customers/",
        json=customer_data,
        headers=authenticated_user["headers"]
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == customer_data["name"]
    assert data["document"] == customer_data["document"]
    assert data["email"] == customer_data["email"]
    assert "id" in data

def test_list_customers(setup_database, authenticated_user):
    """Teste de listagem de clientes"""
    # Criar cliente primeiro
    customer_data = {
        "name": "Cliente Lista",
        "document": "98765432100",
        "email": "lista@teste.com"
    }
    
    client.post(
        "/api/v1/customers/",
        json=customer_data,
        headers=authenticated_user["headers"]
    )
    
    # Listar clientes
    response = client.get(
        "/api/v1/customers/",
        headers=authenticated_user["headers"]
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert any(customer["name"] == "Cliente Lista" for customer in data)

def test_get_customer_by_id(setup_database, authenticated_user):
    """Teste de obtenção de cliente por ID"""
    # Criar cliente primeiro
    customer_data = {
        "name": "Cliente ID",
        "document": "11122233344",
        "email": "id@teste.com"
    }
    
    create_response = client.post(
        "/api/v1/customers/",
        json=customer_data,
        headers=authenticated_user["headers"]
    )
    customer_id = create_response.json()["id"]
    
    # Buscar cliente por ID
    response = client.get(
        f"/api/v1/customers/{customer_id}",
        headers=authenticated_user["headers"]
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == customer_id
    assert data["name"] == customer_data["name"]

def test_update_customer(setup_database, authenticated_user):
    """Teste de atualização de cliente"""
    # Criar cliente primeiro
    customer_data = {
        "name": "Cliente Original",
        "document": "55566677788",
        "email": "original@teste.com"
    }
    
    create_response = client.post(
        "/api/v1/customers/",
        json=customer_data,
        headers=authenticated_user["headers"]
    )
    customer_id = create_response.json()["id"]
    
    # Atualizar cliente
    update_data = {
        "name": "Cliente Atualizado",
        "email": "atualizado@teste.com"
    }
    
    response = client.put(
        f"/api/v1/customers/{customer_id}",
        json=update_data,
        headers=authenticated_user["headers"]
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["email"] == update_data["email"]
    assert data["document"] == customer_data["document"]  # Não alterado

def test_delete_customer(setup_database, authenticated_user):
    """Teste de exclusão de cliente"""
    # Criar cliente primeiro
    customer_data = {
        "name": "Cliente Deletar",
        "document": "99988877766",
        "email": "deletar@teste.com"
    }
    
    create_response = client.post(
        "/api/v1/customers/",
        json=customer_data,
        headers=authenticated_user["headers"]
    )
    customer_id = create_response.json()["id"]
    
    # Deletar cliente
    response = client.delete(
        f"/api/v1/customers/{customer_id}",
        headers=authenticated_user["headers"]
    )
    
    assert response.status_code == 200
    
    # Verificar se foi deletado
    get_response = client.get(
        f"/api/v1/customers/{customer_id}",
        headers=authenticated_user["headers"]
    )
    assert get_response.status_code == 404

def test_create_customer_duplicate_document(setup_database, authenticated_user):
    """Teste de criação de cliente com documento duplicado"""
    customer_data = {
        "name": "Cliente 1",
        "document": "12312312312",
        "email": "cliente1@teste.com"
    }
    
    # Criar primeiro cliente
    client.post(
        "/api/v1/customers/",
        json=customer_data,
        headers=authenticated_user["headers"]
    )
    
    # Tentar criar segundo cliente com mesmo documento
    customer_data2 = {
        "name": "Cliente 2",
        "document": "12312312312",  # Mesmo documento
        "email": "cliente2@teste.com"
    }
    
    response = client.post(
        "/api/v1/customers/",
        json=customer_data2,
        headers=authenticated_user["headers"]
    )
    
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

def test_unauthorized_access(setup_database):
    """Teste de acesso não autorizado"""
    response = client.get("/api/v1/customers/")
    assert response.status_code == 401

