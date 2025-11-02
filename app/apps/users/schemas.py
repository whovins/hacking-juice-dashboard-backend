from pydantic import BaseModel, EmailStr
from enum import Enum

class Role(str, Enum):
    viewer="viewer"; analyst="analyst"; manager="manager"; admin="admin"

class UserOut(BaseModel):
    id: str
    email: EmailStr
    role: Role
