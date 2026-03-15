from fastapi import FastAPI

BLOG_POSTS: list[dict[str, str | int]] = [
  {"id": 1, "title": "Primer post"},
  {"id": 2, "title": "Segundo post"},
  {"id": 3, "title": "Tercer post"},
  {"id": 4, "title": "Cuarto post"},
]

app: FastAPI = FastAPI(title="Mini blog")

@app.get("/")
def home():
  return { 'message': 'Bienvenidos al mini blog' }

@app.get("/posts")
def list_posts():
  return {
    "data": BLOG_POSTS
  }