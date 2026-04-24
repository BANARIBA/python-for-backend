
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Path

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.modules.posts.schemas import FindPostsDto, CreatePostDto, UpdatePostDto, PostResponse, PostsResponse
from app.core.database.database import get_db_connection
from app.modules.authors.repositories import AuthorRepository
from app.modules.posts.repositories import PostRepository

post_router = APIRouter(prefix="/posts", tags=["Posts"])

@post_router.get(
    "",
    response_model=PostsResponse,
    response_description="Listado de comentarios encontrados",
)
def find_all_by(find_posts_dto: FindPostsDto = Depends(), get_db_connetion: Session = Depends(get_db_connection)):
    post_repository = PostRepository(get_db_connetion)
    return post_repository.find_all_by(find_posts_dto)

@post_router.get(
    "/{id}",
    response_model=PostResponse,
    response_description="Comentario encontrado",
)
def find_one_by(
    id: UUID = Path(
        ...,
        title="Id del comentario a buscar",
        description="Id del comentario, debe ser uuid",
        examples=['4AC9D94D-AEFC-415C-92AD-0DBC513B621F'],
    ),
    get_db_connection: Session = Depends(get_db_connection),
):
    post_repository = PostRepository(get_db_connection)
    try:
        exists_post = post_repository.find_one_by(id)
        if not exists_post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El comentario no fue encontrado")
        return PostResponse.model_validate(exists_post, from_attributes=True)
    except SQLAlchemyError as e:
        print(f"Ha ocurrido un error al obtener el comentario: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ha ocurrido un error al buscar el comentario")
    
@post_router.post(
    "",
    response_model=PostResponse,
    response_description="Comentario creado",    
)
def create(
    create_post_dto: CreatePostDto,
    get_db_connection: Session = Depends(get_db_connection),
):
    author_repository = AuthorRepository(get_db_connection)
    post_repository = PostRepository(get_db_connection)
    try:
        exists_author = author_repository.find_one_by(create_post_dto.author_id)
        if not exists_author:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El autor no fue encontrado")
        if exists_author.is_active == False:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El autor se encuentra inactivo")
        new_post = post_repository.create(create_post_dto, exists_author)
        return PostResponse.model_validate(new_post, from_attributes=True)
    
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El comentario ya se encuentra registrado")
    except SQLAlchemyError as e:
        print(f"Ha ocurrido un error al crear el comentario")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ha ocurrido un error al crear el comentario")
    
@post_router.patch(
    "/{id}",
    response_model=PostResponse,
    response_description="Comentario actualizado",
)
def update(
    id: UUID,
    update_post_dto: UpdatePostDto,
    get_db_connection: Session = Depends(get_db_connection),
):
    post_repository = PostRepository(get_db_connection)
    author_repository = AuthorRepository(get_db_connection)
    try:
        fields_to_update = update_post_dto.model_dump(exclude_unset=True)
        exists_post = post_repository.find_one_by(id)
        if not exists_post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El comentario no fue encontrado")
        if update_post_dto.author_id:
            exists_author = author_repository.find_one_by(update_post_dto.author_id)
            if not exists_author:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El autor no fue encontrado")
            if exists_author.is_active == False:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El autor se encuentra inactivo")
        updated_post = post_repository.update(exists_post, fields_to_update)
        return PostResponse.model_validate(updated_post, from_attributes=True)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ya hay un comentario registrado")
    except SQLAlchemyError as e:
        print(f"Ha ocurrido un error al actualizar el comentario: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ha ocurrido un error al actualizar el comentario")
    
@post_router.delete(
    "/{id}",
    response_model=PostResponse,
    response_description="Comentario eliminado",
)
def delete(
    id: UUID,
    get_db_connection: Session = Depends(get_db_connection),
):
    post_repository = PostRepository(get_db_connection)
    try:
        exist_post = post_repository.find_one_by(id)
        if not exist_post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comentario no encontrado")
        deleted = post_repository.delete(exist_post)
        return PostResponse.model_validate(deleted, from_attributes=True)
    except SQLAlchemyError as e:
        print(f"Ha ocurrido un error al eliminar el comentario: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ha ourrido un error al eliminar el comentario")
    
@post_router.patch(
    "/reactivate/{id}",
    response_model=PostResponse,
    response_description="Comentario reactivado",
)
def reactivate(
    id: UUID,
    get_db_connection: Session = Depends(get_db_connection),
):
    post_repository = PostRepository(get_db_connection)
    try:
        exists_post = post_repository.find_one_by(id)
        if not exists_post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El comentario no fue encontrado")
        reactivated = post_repository.reactivate(exists_post)
        return PostResponse.model_validate(reactivated, from_attributes=True)
    except SQLAlchemyError as e:
        print(f"Ha ocurrido un error al reactivar el comentario")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ha ocurrido un error al reactivar el comentario")