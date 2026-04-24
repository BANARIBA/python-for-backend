from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db_connection
from app.modules.users.repositories import UserRepository
from app.modules.users.schemas import UserResponse, UsersResponse, UpdateUserDto, FindUsersDto
from app.modules.auth.utils import AuthHelpers

user_router = APIRouter(prefix="/users", tags=["Users"])

@user_router.get("", response_model=UsersResponse)
def find_all_by(
    params: FindUsersDto = Depends(), 
    db: Session = Depends(get_db_connection)
):
    repo = UserRepository(db)
    result = repo.find_all_by(params)
    return {
        "data": result["data"],
        "meta": {
            "page": params.page,
            "limit": params.limit,
            "total": result["total"],
            "total_pages": (result["total"] + params.limit - 1) // params.limit
        }
    }

@user_router.get("/{id}", response_model=UserResponse)
def find_one_by(id: UUID, db: Session = Depends(get_db_connection)):
    repo = UserRepository(db)
    user = repo.find_one_by(id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@user_router.patch("/{id}", response_model=UserResponse)
def update(
    id: UUID, 
    dto: UpdateUserDto, 
    db: Session = Depends(get_db_connection)
):
    repo = UserRepository(db)
    user = repo.find_one_by(id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    data = dto.model_dump(exclude_unset=True)
    
    # Si el update incluye password, hay que hashearlo
    if "password" in data:
        data["password"] = AuthHelpers.hash_password(data["password"])
        
    return repo.update(user, data)

@user_router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete(id: UUID, db: Session = Depends(get_db_connection)):
    repo = UserRepository(db)
    user = repo.find_one_by(id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    repo.delete(user)
    return {"message": "Usuario desactivado exitosamente"}

@user_router.patch("/reactivate/{id}", response_model=UserResponse)
def reactivate(id: UUID, db: Session = Depends(get_db_connection)):
    repo = UserRepository(db)
    user = repo.find_one_by(id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Lógica de reactivación
    fields = {"is_active": True, "deleted_at": None}
    return repo.update(user, fields)