import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.config.database import get_db, Base
from app.models.user import User
from app.models.company import Company
from app.models.plan import Plan
from app.utils.security import get_password_hash

# Configurar banco de dados de teste
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
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
def test_plan(test_db):
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
    test_db.refresh(plan)
    return plan

@pytest.fixture
def test_company(test_db, test_plan):
    company = Company(
        name="Empresa Teste",
        document="12345678000195",
        email="empresa@teste.com",
        plan_id=test_plan.id
    )
    test_db.add(company)
    test_db.commit()
    test_db.refresh(company)
    return company

@pytest.fixture
def test_user(test_db, test_company):
    user = User(
        email="usuario@teste.com",
        first_name="Usuario",
        last_name="Teste",
        hashed_password=get_password_hash("senha123"),
        company_id=test_company.id,
        is_active=True
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user

def test_register_user(setup_database, test_plan, test_company):
    """Teste de registro de usuário"""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "novo@usuario.com",
            "password": "senha123",
            "first_name": "Novo",
            "last_name": "Usuario",
            "company_id": str(test_company.id)
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "novo@usuario.com"
    assert data["first_name"] == "Novo"
    assert "id" in data

def test_login_user(setup_database, test_user):
    """Teste de login de usuário"""
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": test_user.email,
            "password": "senha123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(setup_database):
    """Teste de login com credenciais inválidas"""
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "usuario@inexistente.com",
            "password": "senhaerrada"
        }
    )
    assert response.status_code == 401

def test_get_current_user(setup_database, test_user):
    """Teste de obtenção do usuário atual"""
    # Fazer login primeiro
    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": test_user.email,
            "password": "senha123"
        }
    )
    token = login_response.json()["access_token"]
    
    # Testar endpoint protegido
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user.email
    assert data["first_name"] == test_user.first_name

def test_protected_route_without_token(setup_database):
    """Teste de acesso a rota protegida sem token"""
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401

def test_protected_route_with_invalid_token(setup_database):
    """Teste de acesso a rota protegida com token inválido"""
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer token_invalido"}
    )
    assert response.status_code == 401

