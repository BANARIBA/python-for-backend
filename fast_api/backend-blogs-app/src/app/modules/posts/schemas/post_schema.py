from pydantic import BaseModel, Field
from typing import List, Optional

from .tag_schema import Tag
from .author_schema import Author

class PostBase(BaseModel):
    title: str
    content: str
    tags: Optional[List[Tag]] = Field(default_factory=list)
    author: Optional[Author] = None