from uuid import UUID
from datetime import datetime

from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from app.modules.authors.schemas import AuthorResponse

class PostResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    title: str
    content: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    
    author: AuthorResponse
    
class PostsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    data: List[PostResponse]
    meta: dict