from app.modules.authors.routes import author_router
from app.modules.posts.routes import post_router
from app.modules.auth.routes import auth_router

__all__ = [
    'author_router',
    'post_router',
    'auth_router',
]