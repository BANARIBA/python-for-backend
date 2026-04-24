from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session

from app.core.config import POST_DB_HOST, POST_DB_NAME, POST_DB_PASSWORD, POST_DB_USER

DATABASE_URL: str = (
    f"mssql+pyodbc://{POST_DB_USER}:{POST_DB_PASSWORD}@{POST_DB_HOST}"
    f"/{POST_DB_NAME}?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes&Encrypt=yes"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=True, # Ver querys sql
    future=True # Ultimas funionalidades
)

session_local = sessionmaker(
    bind=engine,
    autocommit=False, # El commit lo haremos en cada repositorio
    autoflush=False, # Ejecuta el sql sin hacer commitm, tenemos control total
    class_=Session
)

def get_db_connection():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
    
# Actia como catalogo donde mappea todas las tablas o clases model creadas   
class Base(DeclarativeBase):
    pass