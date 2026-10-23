from pydantic import BaseModel, Field, EmailStr

class Author(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="Nombre del autor del comentario")
    email: EmailStr