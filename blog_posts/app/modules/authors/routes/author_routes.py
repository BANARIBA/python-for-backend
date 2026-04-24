from datetime import date
from uuid import UUID

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query, Path

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.modules.authors.schemas import AuthorResponse, CreateAuthorDto, UpdateAuthortDto, AuthorsResponse, FindAuthorsDto
from app.modules.authors.repositories import AuthorRepository
from app.core.database.database import get_db_connection

author_router = APIRouter(prefix="/authors", tags=["Authors"])
       
@author_router.get(
    "",
    response_model=AuthorsResponse, 
    response_description="Listado de autores registrados"
)
def find_all_by(
    term: Optional[str] = Query(
        default=None,
        deprecated=True,
        description="Campo que busca por nombre o email, se encuentra deprecado",
    ),
    name: Optional[str] = Query(
        default=None,
        description="Campo para buscar autores por nombre",
        min_length=1,
        max_length=150,
    ),
    email: Optional[str] = Query(
        default=None,
        description="Campo para buscar autores por email",
        min_length=1,
        max_length=150,
    ),
    is_active: Optional[bool] = Query(
        default=None,
        description="Campo de busqueda de autores por estado, activos o inactivos",
    ),
    init_created_date: Optional[date] = Query(
        default=None,
        description="Fecha inicial de busqueda de registros",
    ),
    end_created_date: Optional[date] = Query(
        default=None,
        description="Fecha final de busqueda de registros",
    ),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    get_db_connection: Session = Depends(get_db_connection),
):
    author_repository = AuthorRepository(get_db_connection)
    find_authors_dto =  FindAuthorsDto(
        email=email,
        name=name,
        is_active=is_active,
        init_created_date=init_created_date,
        end_created_date=end_created_date,
        page=page,
        limit=limit,
    )
    return author_repository.find_all_by(find_authors_dto)

@author_router.get(
    "/{id}",
    response_model=AuthorResponse,
    response_description="Autor encontrado",
)
def find_one_by(
    id: UUID = Path(
        ...,
        title="id del autor",
        description="Identificador uuid del autor",
        examples=['4AC9D94D-AEFC-415C-92AD-0DBC513B621F'],
    ),
    get_db_connetion: Session = Depends(get_db_connection),
) -> AuthorResponse:
    author_repository = AuthorRepository(get_db_connetion)
    try:
        author = author_repository.find_one_by(id)
        if not author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El autor no fue encontrado"
            )
        return AuthorResponse.model_validate(author, from_attributes=True)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ha ocurrido un error al obtener el autor"
        )

@author_router.post("", response_model=AuthorResponse, response_description="Autor creado con exito")
def create(
    createAuthorDto: CreateAuthorDto,
    get_db_connection: Session = Depends(get_db_connection),
):
    author_repository = AuthorRepository(get_db_connection)
    try:
        author = author_repository.create(createAuthorDto)
        return author
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El autor ya se encuentra registrado")
    except SQLAlchemyError as e:
        print(f"Ha ocurrido un error al crear el autor: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ha ocurrido un error al crear el autor")


@author_router.patch(
    "/{id}",
    response_model=AuthorResponse,
    response_description="Retorno del autor actualizado",
)
def update(
    id: UUID,
    update_post_dto: UpdateAuthortDto,
    get_db_connection: Session = Depends(get_db_connection),
):
    author_repository = AuthorRepository(get_db_connection)
    exists_author = author_repository.find_one_by(id)
    if not exists_author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Autor no encontrado",
        )
    try:
        author = update_post_dto.model_dump(exclude_unset=True)
        updated_post = author_repository.update(exists_author, author)
        get_db_connection.commit()
        get_db_connection.refresh(updated_post)
        return AuthorResponse.model_validate(updated_post, from_attributes=True)
    except IntegrityError as e:
        get_db_connection.rollback()
        print(f"Error al actualizar el autor, {e}")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya se encuentra un autor registrado")
    except SQLAlchemyError as e:
        get_db_connection.rollback()
        print(f"Error al actualizar el autor")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ha ocurrido un error al actualizar el autor")
        
@author_router.delete(
    "/{id}",
    response_model=AuthorResponse,
    response_description="Eliminacion de un autor, se inactiva",
)
def delete(
    id: UUID,
    get_db_connection: Session = Depends(get_db_connection),
):
    author_repository = AuthorRepository(get_db_connection)
    try:
        exists_author =  author_repository.find_one_by(id)
        if not exists_author:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El autor no fue encontrado")
        deleted_author = author_repository.delete(exists_author)
        return AuthorResponse.model_validate(deleted_author, from_attributes=True)
    except SQLAlchemyError as e:
        print(f"Ha ocurrido un error al eliminar el autor: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ha ocurrido un error al eliminar el autor")
    
@author_router.patch(
    "/reactivate/{id}",
    response_model=AuthorResponse,
    response_description="Autor reactivado"
)
def reactivate(
    id: UUID,
    get_db_connection: Session = Depends(get_db_connection),
):
    author_repository = AuthorRepository(get_db_connection)
    try:
        exists_author = author_repository.find_one_by(id)
        if not exists_author:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Autor no encontrado")
        reactivated_author = author_repository.reactivate(exists_author)
        return AuthorResponse.model_validate(reactivated_author, from_attributes=True)
    except SQLAlchemyError as e:
        print(f"Ha ocurrido un error al reactivar el autor: {e}")