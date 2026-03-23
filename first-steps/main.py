from fastapi import FastAPI, Query, Body, HTTPException

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
@app.get("/posts")
def list_posts(query: str | None = Query(default=None, description="Texto para buscar por titulo del post")):
  if query:
    # List comprenhension
    results = [post for post in BLOG_POSTS if query.lower() in post["title"].lower()]
    # For tradicional
    '''for post in BLOG_POSTS:
      if query.lower() in post["title"].lower():
        results.append(post)'''
    return {
      "data": results,
      "query": query,
    }
  return {
    "data": BLOG_POSTS
  }
  
# http://localhost:8000/posts/1
@app.get("/posts/{post_id}")
def get_post(post_id: int, query: bool | None = Query(default=True, description="Incluir el contenido del post True=Si, False= No")):
  for post in BLOG_POSTS:
    if post["id"] == post_id:
      if query and query == True:
        return {
          "data": post
        }
      else:
        return {
          "data": {
            "id": post["id"],
            "title": post["title"],
          }
        }
  return {
    "error": "post no encontrado"
  }

@app.post("/posts")
def create_post(post: dict = Body(...)):
  if "title" not in post or "content" not in post:
    return {
      "error": "Titulo y contenido son requeridos"
    }
  if not str(post["title"]).strip():
    return {
      "error": "Titulo no puede estar vacio"
    }
  new_id:int = BLOG_POSTS[-1]["id"] + 1 if BLOG_POSTS else 1
  new_post = {
    "id": new_id,
    "title": post["title"],
    "content": post["content"]
  }
  BLOG_POSTS.append(new_post)
  return {
    "message": "Comentario creado",
    "data": new_post
  }
  
@app.put("/posts/{post_id}")
def update_port(post_id: int, data: dict = Body(...)):
  for post in BLOG_POSTS:
    if post["id"] == post_id:
      if "title" in data: post["title"] = data["title"]
      if "content" in data: post["content"] = data["content"]
      return {
        "message": "Comentario actualizado",
        "data": post,
      }
    raise HTTPException(status_code=404, detail="Comentario no encontrado")
  
@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
  for index, post in enumerate(BLOG_POSTS):
    if post["id"] == post_id:
      BLOG_POSTS.pop(index)
      raise HTTPException(status_code=200, detail="Comentario eliminado")
    raise HTTPException(status_code=404, detail="Comentario no encontrado")