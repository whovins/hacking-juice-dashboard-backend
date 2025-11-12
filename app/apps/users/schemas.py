from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field
from app.apps.users.models import Role

class UserOut(BaseModel):
    id: str
    email: EmailStr
    role: Role

    model_config = {"from_attributes": True}

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    role: Role = Role.viewer
