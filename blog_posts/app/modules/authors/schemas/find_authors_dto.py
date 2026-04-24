from datetime import date

from typing import Optional

from pydantic import Field, BaseModel

class FindAuthorsDto(BaseModel):
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=10, ge=1)
    name: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None
    init_created_date: Optional[date] = None
    end_created_date: Optional[date] = None