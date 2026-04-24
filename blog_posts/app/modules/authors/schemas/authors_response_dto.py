from uuid import UUID
from datetime import datetime

from typing import Optional, List

from pydantic import ConfigDict, EmailStr, BaseModel

class AuthorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: str
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    
class AuthorsResponse(BaseModel):
    data: List[AuthorResponse]
    meta: dict