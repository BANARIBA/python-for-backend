from pydantic import Field, BaseModel

class CreateAuthorDto(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    email: str = Field(min_length=1, max_length=150)