from typing import Optional

from pydantic import EmailStr, BaseModel

class FindUsersDto(BaseModel):
    page: int = 1
    limit: int = 10
    complete_name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None