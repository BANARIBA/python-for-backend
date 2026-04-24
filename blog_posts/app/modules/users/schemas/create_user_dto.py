from pydantic import BaseModel, EmailStr

class CreateUserDto(BaseModel):
    complete_name: str
    email: EmailStr
    password: str