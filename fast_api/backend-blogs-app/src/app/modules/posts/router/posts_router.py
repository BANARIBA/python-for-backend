from math import ceil
from typing import List, Union, Literal
from fastapi import APIRouter, Query, Body, HTTPException, status, Path
from src.app.modules.posts.schemas import PostCreate, PostUpdate, PostPublic, PostSummary, PaginationPost

BLOG_POSTS = [
    {
        "id": 1,
        "title": "Comentario Uno",
        "content": "Comentario Uno",
    },
    {
        "id": 2,
        "title": "Comentario Dos",
        "content": "Comentario Dos",
    },
    {
        "id": 3,
        "title": "Comentario Tres",
        "content": "Comentario Tres",
    },
    {
        "id": 4,
        "title": "Comentario Cuatro",
        "content": "Comentario Cuatro",
    },
    {
        "id": 5,
        "title": "Comentario Cinco",
        "content": "Comentario Cinco",
    },
    {
        "id": 6,
        "title": "Comentario Seis",
        "content": "Comentario Seis",
    },
    {
        "id": 7,
        "title": "Comentario Siete",
        "content": "Comentario Siete",
    },
]

post_router = APIRouter(
    prefix='/posts',
    tags=['Posts'],
)

# http://127.0.0.1:8000/api/posts/2 || http://127.0.0.1:3500/api/posts/1?not_include_content=True
@post_router.get("/{post_id}", response_model=Union[PostPublic, PostSummary], response_description="Comentario encontrado")
def get_post(
    post_id: int = Path(..., ge=1, title="Identificador del comentario", description="valor entero, debe ser mayor a 1"),
    not_include_content: bool | None = Query(
        title="not_include_content", 
        default=None, 
        description="Bandera para incluir el campo content en la respuesta"
    ),
):
    for post in BLOG_POSTS:
        if post["id"] == post_id:
            if not not_include_content:
                return post
            else:
                return {
                    "id": post["id"],
                    "title": post["title"],
                }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Comentario no Encontrado",
        headers=None,
    )
    

# http://127.0.0.1:8000/api/posts?search=Comentario Uno&limit=2&offset=60&order_by=id&direction=asc
@post_router.get("/", response_model=PaginationPost)
def get_all_posts(
    search: str | None = Query(
        title="title", 
        default=None, 
        description="Texto para buscar por titulo del comentario",
        alias="search",
        min_length=3,
        max_length=50,
        # pattern=r"^[a-zA-Z]+$",
    ),
    per_page: int = Query(default=10, ge=1, le=50, description="Numero de resultados por pagina [1 a 50]"),
    page: int = Query(default=1, ge=1, description="Elementos a saltar antes de empezar a paginar"),
    order_by: Literal["id", "title"] = Query(default="id", description="Campo de Ordernamiento por default id"),
    direction: Literal["asc", "desc"] = Query(default="desc", description="Tipo de ordenamiento, ascendente o descendente"),
):
    results = BLOG_POSTS
    if search:
        results = [post for post in results if search.lower() == post["title"].lower()]

    total = len(results)
    total_pages = ceil(total/per_page) if total > 0 else 0

    if total_pages == 0:
        current_page = 1
    else:
        current_page = min(page, total_pages)

    results = sorted(results, key=lambda post: post[order_by], reverse=(direction=="desc"))

    if total_pages == 0:
        items = []
    else:
        start = (current_page - 1) * per_page
        items = results[start: start + per_page]

    has_prev = current_page > 1
    has_next = current_page < total_pages if total_pages > 0 else False

    return PaginationPost(
        page=current_page,
        per_page=per_page,
        total_pages=total_pages,
        total=total,
        has_prev=has_prev,
        has_next=has_next,
        order_by=order_by,
        direction=direction,
        search=search,
        items=items,
    )

# http://127.0.0.1:8000/api/post
'''
    {
        "title": "Comentario 3",
        "content": "Contenido 3"
    }
'''
@post_router.post("/", response_model=PostPublic, response_description="Comentario creado en el blog")
def create_post(
    post: PostCreate = Body(...)
):
    new_id: int = BLOG_POSTS[-1]["id"] + 1 if BLOG_POSTS else 1
    new_post = { 
        "id": new_id, 
        "title": post.title, 
        "content": post.content, 
        "tags": [tag.model_dump() for tag in post.tags], 
        "author": post.author.model_dump() if post.author else None,
    }
    BLOG_POSTS.append(new_post)
    return new_post


# http://127.0.0.1:8000/api/post/6
'''
    {
        "title": "Comentario 3 Modificado",
        "content": "Contenido 3 Modificado"
    }
'''
@post_router.patch(
    "/{post_id}", 
    response_model=PostPublic,
    response_description="Comentario en el blog actualizado",
    response_model_exclude_none=True
)
def update_post(post_id: int, data: PostUpdate = Body(...)):
    for post in BLOG_POSTS:
        if post["id"] == post_id:
            playload = data.model_dump(exclude_unset=True)
            if "title" in playload: post["title"] = playload["title"]
            if "content" in playload: post["content"] = playload["content"]
            return post
        
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="No se encontro el comentario", 
        headers=None
    )

# http://127.0.0.1:8000/api/post/5
@post_router.delete("/{post_id}")
def delete_post(post_id: int):
    for index, post in enumerate(BLOG_POSTS):
        if post["id"] == post_id:
            BLOG_POSTS.pop(index)
            return {
                "message": f"Comentario {post_id} eliminado"
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Comentario no encontrado",
        headers=None,
    )
