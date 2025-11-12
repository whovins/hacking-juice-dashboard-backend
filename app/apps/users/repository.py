from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional, Sequence, Tuple
from app.apps.users.models import Role, User

class UsersRepo:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_by_id(self, user_id: str) -> Optional[User]:
        stmt = select(User).where(User.id == user_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()
    
    async def list(self, *, page: int = 1, size: int = 10, query: str | None = None) -> tuple[Sequence[User], int]:
        stmt = select(User)
        if query:
            q = f"%{query}%"
            stmt = stmt.where(User.email.ilike(q))
        total_stmt = select(func.count()).select_from(stmt.subquery())

        stmt = stmt.order_by(User.created_at.desc()).offset((page - 1) * size).limit(size)
        res = await self.session.execute(stmt)
        items = res.scalar().all()
        total_res = await self.session.execute(total_stmt)
        total = total_res.scalar_one()
        return items, int(total)

    async def create_user(self, *, email: str, password: str, role: Role) -> User:
        user = User(email=email, password=password, role=role)
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return User

    async def update():
        pass

    async def delete():
        pass