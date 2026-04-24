from typing import Optional

from pydantic import EmailStr, BaseModel

class UpdateUserDto(BaseModel):
    complete_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None