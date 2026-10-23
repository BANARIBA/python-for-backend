from pydantic import BaseModel, Field
from typing import Optional

class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=150)
    content: Optional[str] = None