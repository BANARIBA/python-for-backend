from pydantic import BaseModel, Field

class Tag(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="Nombre de etiquetas")