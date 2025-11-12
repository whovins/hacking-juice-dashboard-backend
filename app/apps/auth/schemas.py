from pydantic import BaseModel, EmailStr

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class MeOut(BaseModel):
    id: str
    email: EmailStr
    role: str

class TokenPairOut(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshIn(BaseModel):
    refresh_token: str
