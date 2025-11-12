from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.apps.users.models import Role, User

class UsersRepo:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def find_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_by_id(self, user_id: str) -> Optional[User]:
        stmt = select(User).where(User.id == user_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def create_user(self, *, email: str, password: str, role: Role) -> User:
        user = User(email=email, password=password, role=role)
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return User
