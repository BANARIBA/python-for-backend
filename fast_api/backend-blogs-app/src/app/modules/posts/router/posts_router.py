from typing import List, Union
from fastapi import APIRouter, Query, Body, HTTPException, status, Path
from src.app.modules.posts.schemas import PostCreate, PostUpdate, PostPublic, PostSummary

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
    

# http://127.0.0.1:8000/api/posts?query=Comentario Uno
@post_router.get("/", response_model=List[PostPublic])
def get_all_posts(
    query: str | None = Query(
        title="title", 
        default=None, 
        description="Texto para buscar por titulo del comentario"
    ),
):
    if query:
        results = [post for post in BLOG_POSTS if query.lower() == post["title"].lower()]
        # for post in BLOG_POSTS:
        #     if query.lower() in post["title"].lower():
        #         results.append(post)

        return results

    return BLOG_POSTS

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
