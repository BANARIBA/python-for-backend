from uuid import UUID
from datetime import date

from pydantic import BaseModel, Field

from typing import Optional

class FindPostsDto(BaseModel):
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=10, ge=1)
    title: Optional[str] = Field(None)
    content: Optional[str] = Field(None)
    author: Optional[UUID] = Field(None)
    is_active: Optional[bool]= Field(None)
    init_created_date: Optional[date] = Field(None)
    end_created_date: Optional[date] = Field(None)