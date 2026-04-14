from typing import Optional, List, Literal

from pydantic import BaseModel, Field, field_validator, EmailStr
from fastapi import HTTPException

class Tag(BaseModel):
  name: str = Field(..., min_length=2, max_length=30, description="Nombre de la etiqueta")
  
class Author(BaseModel):
  name: str = Field(..., min_length=3, max_length=150, description="Nombre del autor quien creo el comentario")
  email: EmailStr = Field(..., description="Email de quien creo el comentario")

class PostBase(BaseModel):
  title: str
  content: Optional[str] = "Sin contenido"
  tags: Optional[List[Tag]] = Field(default_factory=list) # Crea una lista vacia por defecto [] 
  author: Optional[Author] = None
  
class PostCreate(BaseModel):
  title: str = Field(
    ...,
    min_length=3,
    max_length=100,
    description="Titulo del post, minimo 3 caracteres y maximo 100 caracteres",
    examples=["Mi primer post con fast api"]
  )
  content: Optional[str] = Field(
    default="Contenido no disponible",
    min_length=10,
    description="Contenido del post, minimo 10 caracteres",
    examples=["Contenido del primer post con fast api"],
  )
  tags: List[Tag] = Field(default_factory=list) # Crea una lista vacia por defecto [] 
  author: Optional[Author] = None
  
  @field_validator("title")
  @classmethod
  def not_allowed_title(cls, value: str) -> str:
    if "spam" in value.lower():
      raise HTTPException(status_code=400, detail="Titulo no valido por que es una palabra no permitida 'spam'")
    return value

class PostUpdate(BaseModel):
  title: Optional[str] = Field(None, min_length=3, max_length=100)
  content: Optional[str] = None
  
class PostPublic(PostBase):
  id: int

class PostSumary(BaseModel):
  id: int
  content: str
  
class PaginationPost(BaseModel):
  page: int
  per_page: int
  total: int
  total_pages:int
  search: Optional[str] = None
  order_by: Literal["id", "title"]
  direction: Literal["asc", "desc"]
  items: List[PostPublic]
  has_prev: bool
  has_next: bool
