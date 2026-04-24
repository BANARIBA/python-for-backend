from dotenv import load_dotenv

from fastapi import FastAPI

from app.core.database.database import engine, Base
from app.core.database import load_models
from app.app_routes import author_router, post_router, auth_router

load_dotenv()

def create_app() -> FastAPI:
    # Inicializar app
    app: FastAPI = FastAPI(title="Blog Posts")
    
    # Sincroniza todo modelo o tabla creada con la base de datos
    Base.metadata.create_all(bind=engine)
    
    # Cargando rutas
    app.include_router(author_router)
    app.include_router(post_router)
    app.include_router(auth_router, prefix='/api')
    
    return app

app = create_app()
