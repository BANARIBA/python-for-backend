from uuid import UUID

from pydantic import BaseModel, Field

class CreatePostDto(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    content: str = Field(min_length=1, max_length=255)
    author_id: UUID = Field()
    