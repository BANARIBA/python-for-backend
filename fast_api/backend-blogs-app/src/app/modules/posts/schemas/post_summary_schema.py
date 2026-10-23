from pydantic import BaseModel

class PostSummary(BaseModel):
    id: int
    title: str