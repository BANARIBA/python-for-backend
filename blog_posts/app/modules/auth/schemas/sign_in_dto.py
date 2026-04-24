from pydantic import BaseModel, EmailStr

class SignInDto(BaseModel):
    email: EmailStr
    password: str