from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from datetime import timedelta
from uuid import UUID

from app.core.database import get_db_connection
from app.modules.users.repositories import UserRepository
from app.modules.users.models import User
from app.modules.users.schemas import CreateUserDto, UserResponse
from app.modules.auth.schemas import SignInDto, TokenResponse
from app.modules.auth.utils import AuthHelpers

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@auth_router.post("/new-account", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def new_account(dto: CreateUserDto, db: Session = Depends(get_db_connection)):
    repo = UserRepository(db)
    
    # Verificar duplicados
    if repo.find_by_email(dto.email):
        raise HTTPException(status_code=400, detail="El correo electrónico ya existe")
    
    # Hashear contraseña antes de guardar
    hashed_pw = AuthHelpers.hash_password(dto.password)
    
    new_user = User(
        complete_name=dto.complete_name,
        email=dto.email,
        password=hashed_pw,
        is_active=True
    )
    
    return repo.create(new_user)

@auth_router.post("/sign-in", response_model=TokenResponse)
def sign_in(dto: SignInDto, db: Session = Depends(get_db_connection)):
    repo = UserRepository(db)
    user = repo.find_by_email(dto.email)
    
    # Verificación de identidad
    if not user or not AuthHelpers.verify_password(dto.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Email o contraseña incorrectos"
        )
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Usuario inactivo")

    # Generación de tokens (1 hora cada uno)
    access_token = AuthHelpers.create_token({"sub": str(user.id)}, timedelta(hours=1))
    refresh_token = AuthHelpers.create_token({"sub": str(user.id)}, timedelta(hours=1))
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@auth_router.post("/refresh-token", response_model=TokenResponse)
def refresh(
    # El frontend envía el refresh_token en el body
    token: str = Body(..., embed=True), 
    db: Session = Depends(get_db_connection)
):
    # Decodificar el token para ver a quién pertenece
    payload = AuthHelpers.decode_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Token inválido o sesión expirada permanentemente"
        )
    
    user_id = payload.get("sub")
    
    # Opcional: Verificar que el usuario aún exista y esté activo
    repo = UserRepository(db)
    user = repo.find_one_by(UUID(user_id))
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Usuario no autorizado, no existe o se encuentra inactivo, hablar con el administrador")

    # Generar un nuevo par de tokens
    new_access = AuthHelpers.create_token({"sub": user_id}, timedelta(hours=1))
    new_refresh = AuthHelpers.create_token({"sub": user_id}, timedelta(hours=1))
    
    return {
        "access_token": new_access,
        "refresh_token": new_refresh,
        "token_type": "bearer"
    }