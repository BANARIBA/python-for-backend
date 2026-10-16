from fastapi import FastAPI, APIRouter, Query

app = FastAPI(
    title="Aplicacion de Blogs Backend",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

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

blog_api_router = APIRouter(prefix="/api")

# http://127.0.0.1:8000/api
@blog_api_router.get("/")
def index():
    return {"message": "Blogs API App is running!"}

# http://127.0.0.1:8000/api/posts/2
@blog_api_router.get("/posts/{post_id}")
def get_post(
    post_id: int
):
    res: dict | None = None
    for post in BLOG_POSTS:
        if post["id"] == post_id:
            return {
                "status": 200,
                "data": post,
            }

    return {
        "status": 404,
        "data": "Post not found",
    }
    

# http://127.0.0.1:8000/api/posts?query=Comentario Uno
@blog_api_router.get("/posts")
def get_all_posts(
    query: str | None = Query(title="title", default=None, description="Texto para buscar por titulo del comentario"),
):
    print(query)
    if query:
        results = [post for post in BLOG_POSTS if query.lower() == post["title"].lower()]
        # for post in BLOG_POSTS:
        #     if query.lower() in post["title"].lower():
        #         results.append(post)

        return {
            "data": results,
            "query": query,
        }

    return {
        "status": 200,
        "data": BLOG_POSTS,
    }

app.include_router(blog_api_router)