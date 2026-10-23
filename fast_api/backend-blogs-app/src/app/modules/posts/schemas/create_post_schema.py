from pydantic import BaseModel, Field, field_validator
from typing import Optional, List

from .tag_schema import Tag
from .author_schema import Author

class PostCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100, description="Titulo del comentario del blog", examples=["Titulo del comentario de pruebas"])
    content: Optional[str] = Field(default=None, min_length=10, description="Contenido del comentario del blog", examples=["Contenido del comentario del blog de pruebas"])
    tags: List[Tag] = Field(default_factory=list)
    author: Optional[Author] = None

    @field_validator("title")
    @classmethod
    def not_allowed_titles(cls, value: str) -> str:
        if "spam" in value.lower():
            raise ValueError("El titulo no puede contener la palabra spam")
        return value
