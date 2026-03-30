from fastapi import FastAPI, Query, HTTPException
from typing import List, Union

from classes.post import PostPublic, PostCreate, PostUpdate, PostSumary

BLOG_POSTS = [
  {"id": 1, "title": "Primer post", "content": "Contenido del 1 post"},
  {"id": 2, "title": "Segundo post", "content": "Contenido del 2 post"},
  {"id": 3, "title": "Tercer post", "content": "Contenido del 3 post"},
  {"id": 4, "title": "Cuarto post", "content": "Contenido del 4 post"},
]

app: FastAPI = FastAPI(title="Mini blog")

@app.get("/")
def home():
  return { 'message': 'Bienvenidos al mini blog' }

# http://localhost:8000/posts?query=????
@app.get(
  "/posts",
  response_model=List[PostPublic],
  response_description="Listado de comentarios"
)
def list_posts(query: str | None = Query(default=None, description="Texto para buscar por titulo del post")):
  if query:
    # List comprenhension
    results = [post for post in BLOG_POSTS if query.lower() in post["title"].lower()]
    # For tradicional
    '''for post in BLOG_POSTS:
      if query.lower() in post["title"].lower():
        results.append(post)'''
    raise HTTPException(status_code=200, detail=results)
  raise HTTPException(status_code=200, detail=BLOG_POSTS)
  
# http://localhost:8000/posts/1
@app.get(
  "/posts/{post_id}",
  response_model=Union[PostPublic, PostSumary],
  response_description="Comentario encontrado"
)
def get_post(post_id: int, query: bool | None = Query(default=True, description="Incluir el contenido del post True=Si, False=No")):
  for post in BLOG_POSTS:
    if post["id"] == post_id:
      if query and query == True:
        raise HTTPException(status_code=200, detail=post)
      else:
        raise HTTPException(status_code=200, detail={
          "id": post["id"],
          "title": post["title"],
        })
  raise HTTPException(status_code=404, detail={
    "error": "post no encontrado"
  })

@app.post(
  "/posts",
  response_model=PostPublic,
  response_description="Comentario creado"
)
def create_post(post: PostCreate):
  new_post_id: int = BLOG_POSTS[-1]["id"] + 1 if BLOG_POSTS else 1
  new_post = {
    "id": new_post_id,
    "title": post.title,
    "content": post.content,
    "tags": [tag.model_dump() for tag in post.tags],
    "author": post.author.model_dump() if post.author else None,
  }
  BLOG_POSTS.append(new_post)
  raise HTTPException(status_code=201, detail=new_post)
  
@app.put(
  "/posts/{post_id}",
  response_model=PostPublic,
  response_description="Comentario actualizado"
)
def update_post(post_id: int, data: PostUpdate):
  for post in BLOG_POSTS:
    if post["id"] == post_id:
      playload = data.model_dump(exclude_unset=True)
      if "title" in playload: post["title"] = playload["title"]
      if "content" in playload: post["content"] = playload["content"]
      raise HTTPException(status_code=200, detail=post)
    raise HTTPException(status_code=404, detail={ "error": "Comentario no encontrado" })
  
@app.delete(
  "/posts/{post_id}",
  response_model=str,
  response_description="Detalle del comentario ha eliminar"
)
def delete_post(post_id: int):
  for index, post in enumerate(BLOG_POSTS):
    if post["id"] == post_id:
      BLOG_POSTS.pop(index)
      raise HTTPException(status_code=200, detail=post)
    raise HTTPException(status_code=404, detail={ "error": "Comentario no encontrado" })