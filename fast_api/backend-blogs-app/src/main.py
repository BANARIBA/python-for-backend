from fastapi import FastAPI, APIRouter
from src.app.modules.posts.router import post_router

app = FastAPI(
    title="Aplicacion de Blogs Backend",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

blog_api_router = APIRouter(prefix="/api")

# http://127.0.0.1:8000/api
@blog_api_router.get("/")
def index():
    return {"message": "Blogs API App is running!"}

blog_api_router.include_router(post_router)

app.include_router(blog_api_router)