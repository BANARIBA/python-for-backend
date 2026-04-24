import os

POST_DB_PASSWORD: str = os.getenv('POST_DB_PASSWORD', '-$PilotoDePruebas$-')
POST_DB_USER: str = os.getenv('POST_DB_USER', 'desarrollo')
POST_DB_NAME: str = os.getenv('POST_DB_NAME', 'posts_db_development')
POST_DB_HOST: str = os.getenv('POST_DB_HOST','localhost\\SQLEXPRESS')
POST_DB_PORT: int = int(os.getenv('POST_DB_PORT', 1433))
                        