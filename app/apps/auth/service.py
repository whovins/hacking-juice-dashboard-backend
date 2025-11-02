from passlib.hash import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession
from app.apps.users.repository import UsersRepo
from app.core.security import issue_tokens
from fastapi import HTTPException

class AuthService:
    def __init__(self, s: AsyncSession):
        self.users = UsersRepo(s)
    async def login(self, email: str, password: str):
        u = await self.users.find_by_email(email.strip().lower())
        if not u or not bcrypt.verify(password, u.password_hash):
            raise HTTPException(status_code=401, detail="invalid_credentials")
        return issue_tokens(str(u.id), u.role.value)
