from typing import Optional

from pydantic import Field, BaseModel
    
class UpdateAuthortDto(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=150)
    email: Optional[str] = Field(None)