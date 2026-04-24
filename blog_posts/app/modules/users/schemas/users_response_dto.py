from uuid import UUID
from datetime import datetime

from typing import Optional, List

from pydantic import BaseModel, ConfigDict

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

class UsersResponse(BaseModel):
    data: List[UserResponse]
    meta: dict