from pydantic import BaseModel, EmailStr


class RegistrationSchema(BaseModel):
    email: EmailStr
    password: str


class AuthSchema(BaseModel):
    email: EmailStr
    password: str
