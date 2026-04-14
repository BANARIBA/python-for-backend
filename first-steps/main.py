import os
from math import ceil
from typing import Union, Optional, Literal, List

from fastapi import FastAPI, Query, HTTPException, Path
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase

from classes.post import PostPublic, PostCreate, PostUpdate, PostSumary, PaginationPost
from data.posts import BLOG_POSTS

'''INICIO CONEXION A LA BASE DE DATOS'''
POST_DB_PASSWORD: str = os.getenv('POST_DB_PASSWORD', '-$PilotoDePruebas$-')
POST_DB_USER: str = os.getenv('POST_DB_USER', 'desarrollo')
POST_DB_NAME: str = os.getenv('POST_DB_NAME', 'test_db')
POST_DB_HOST: str = os.getenv('POST_DB_HOST', '10.30.3.204')
POST_DB_PORT: str = os.getenv('POST_DB_PORT', '1433')

connection_url = URL.create(
    "mssql+pyodbc",
    username=POST_DB_USER,
    password=POST_DB_PASSWORD,
    host=POST_DB_HOST,
    port=POST_DB_PORT,
    database=POST_DB_NAME,
    query={
        "driver": "ODBC Driver 18 for SQL Server",
        "TrustServerCertificate": "yes",
    },
)

engine = create_engine(
  connection_url, 
  echo=True, # hace que las query sql se vean en la terminal
  future=True, # para usar ultimas caracteristicas
)

LOCAL_SESSION = sessionmaker(
  bind=engine, # Motor a conectarse
  autocommit=False, # Que los commit no se hagan automaticos,
  autoflush=False,
  class_=Session
)

class Base(DeclarativeBase):
  pass

try:
    with engine.connect() as conn:
      result = conn.execute(text("SELECT 1 AS ok"))
      row = result.fetchone()
      print("Conexión exitosa:", row.ok)
except Exception as e:
  print("Error de conexión:", e)
'''FIN CONEXION A LA BASE DE DATOS'''

app: FastAPI = FastAPI(title="Mini blog")

@app.get("/")
def home():
  return { 'message': 'Bienvenidos al mini blog' }

# http://localhost:8000/posts?query=????
@app.get(
  "/posts",
  response_model=PaginationPost,
  response_description="Listado de comentarios"
)
def list_posts(
  text: Optional[str] = Query(
    default=None,
    deprecated=True,
    description="Texto para buscar por titulo del post, este parametro esta deprecado, usar search en su lugar",
  ),
  query: Optional[str] = Query(
    default=None, 
    description="Texto para buscar por titulo del post",
    alias="search",# Con la url puedo usar query o search, es increible esto
    min_length=3,
    max_length=50,
    pattern=r"^[\w\sáéíóúÁÉÍÓÚÜü-]+$"
  ),
  per_page: int = Query(
    10,
    ge=1, # mayor o igual
    le=50,  # menor o igual
    description="Numero de resultados entre [1-50]"
  ),
  page: int = Query(
    1,
    ge=1, # mayor o igual
    description="Elementos a saltar antes de enviar la lista de comentarios"
  ),
  order_by: Literal["id", "title"] = Query(
    "id", description="Campo de ordenamiento"
  ),
  direction: Literal["asc", "desc"] = Query(
    "asc", description="Direccion de ordenamiento"
  )
):
  results = BLOG_POSTS
  if query:
    # List comprenhension
    results = [post for post in results if query.lower() in post["title"].lower()]
    # For tradicional
    '''for post in BLOG_POSTS:
      if query.lower() in post["title"].lower():
        results.append(post)'''
        
  total = len(results)
  total_pages = ceil(total / per_page) if total > 0 else 0
  if total_pages == 0:
    current_page = 1
  else:
    current_page= min(page, total_pages)
    
  results = sorted(results, key=lambda post: post[order_by], reverse=(direction == "desc"))
  
  if total_pages == 0:
    items= []
  else:
    start = (current_page - 1) * per_page # page 1 => (1-1)*10, 2=>(2-1)*10 es el offset
    items = results[start: start + per_page]
  
  has_prev = current_page > 0
  has_next = current_page < total_pages if total_pages  > 0 else False
  
  raise HTTPException(status_code=200, detail={
    "page": page,
    "per_page": per_page,
    "total": len(BLOG_POSTS),
    "total_pages": total_pages,
    "has_prev": has_prev,
    "has_next": has_next,
    "search": query,
    "order_by": order_by,
    "direction": direction,
    "items": items
  })
  
# http://localhost:8000/posts/1
@app.get(
  "/posts/{post_id}",
  response_model=Union[PostPublic, PostSumary],
  response_description="Comentario encontrado"
)
def get_post(
  post_id: int=Path(
    ...,
    ge=1,
    title="Id del comentario",
    description="Identificador entero del comentario, debe ser mayor o igual a 1",
    examples=[1]
  ),
  query: bool | None = Query(default=True, description="Incluir el contenido del post True=Si, False=No")
):
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
  
@app.get('/posts/by/tags', response_model=List[PostPublic])
def get_posts_by_tags(
  tags: List[str] = Query(
    ...,
    min_length=2,
    description="Una o mas etiquetas para filtrar los comentarios, minimo 2 caracteres por etiqueta ejemplo: ?tags=python&tags=fastapi",
  ),
):
  lower_tags: list[str] = [tag.lower() for tag in tags]
  return [
    post for post in BLOG_POSTS
    if any(lower_tag["name"].lower() in lower_tags for lower_tag in post.get("tags", []))
  ]

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
