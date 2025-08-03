from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Any # Importar Any para o tipo de retorno do bypass

from ..config.database import get_db
from ..config.settings import settings
from ..models.user import User
from ..schemas.user import UserLogin, Token, UserCreate, User as UserSchema
from ..utils.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    get_current_active_user # Manter esta importação para uso em produção
)

router = APIRouter()

# --- INÍCIO DA MODIFICAÇÃO PARA DESENVOLVIMENTO ---

# Esta é uma dependência MOCK para desenvolvimento.
# Ela SEMPRE retorna um usuário "logado" para bypassar a autenticação.
# REMOVA OU COMENTE ESTA FUNÇÃO E SEU USO EM PRODUÇÃO!
async def get_current_user_dev_bypass() -> Any:
    """
    Retorna um objeto de usuário simulado para bypassar a autenticação em desenvolvimento.
    Ajuste os campos para corresponder ao seu modelo de usuário (User) se necessário.
    """
    return User(
        id=999, # ID fictício para o usuário de desenvolvimento
        email="dev.user@fingestor.com",
        first_name="Desenvolvedor",
        last_name="Teste",
        is_active=True,
        is_superuser=True,
        role="admin", # Defina uma role que permita acesso às funcionalidades
        company_id=1 # Defina um company_id se for necessário para o seu modelo
        # Adicione outros campos que seu modelo User espera e que são essenciais para o funcionamento
    )

# --- FIM DA MODIFICAÇÃO PARA DESENVOLVIMENTO ---


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Endpoint de login"""
    user = db.query(User).filter(User.email == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserSchema)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """Endpoint de registro de usuário"""
    # Verificar se o email já existe
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Criar novo usuário
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        password=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        is_active=user_data.is_active,
        role=user_data.role,
        company_id=user_data.company_id
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


@router.get("/me", response_model=UserSchema)
async def read_users_me(
    # current_user: User = Depends(get_current_active_user) # Comente esta linha
    current_user: Any = Depends(get_current_user_dev_bypass) # Use a função de bypass para desenvolvimento
):
    """Retorna informações do usuário logado"""
    return current_user


@router.post("/refresh", response_model=Token)
async def refresh_token(
    # current_user: User = Depends(get_current_active_user) # Comente esta linha
    current_user: Any = Depends(get_current_user_dev_bypass) # Use a função de bypass para desenvolvimento
):
    """Atualiza o token JWT"""
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": current_user["email"]}, expires_delta=access_token_expires # Use current_user["email"]
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
