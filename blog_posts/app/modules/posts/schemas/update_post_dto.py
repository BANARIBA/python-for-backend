from uuid import UUID

from typing import Optional

from pydantic import BaseModel, Field

class UpdatePostDto(BaseModel):
    title: Optional[str] = Field(None)
    content: Optional[str] = Field(None)
    author_id: Optional[UUID] = Field(None)