from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from app.apps.users.models import Role

class UserOut(BaseModel):
    id: str
    email: EmailStr
    role: Role

    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    role: Role = Role.viewer

    model_config = ConfigDict(from_attributes=True)
    

class UserUpdateIn(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)
    role: Optional[Role] = None
    model_config = ConfigDict(from_attributes=True)

class PageUsers(BaseModel):
    items: list[UserOut]
    total: int
    page: int
    size: int
    model_config = ConfigDict(from_attributes=True)

class UserSettingsOut(BaseModel):
    user_id: str
    ui_theme: str
    notify_email: dict

    model_config = ConfigDict(from_attributes=True)

class UserSettingsIn(BaseModel):
    ui_theme: Optional[str] = None
    notify_email: Optional[dict] = None
    model_config = ConfigDict(from_attributes=True)
