from pydantic import BaseModel, EmailStr

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class MeOut(BaseModel):
    id: str
    email: EmailStr
    role: str

class RefreshIn(BaseModel):
    refresh_token: str
