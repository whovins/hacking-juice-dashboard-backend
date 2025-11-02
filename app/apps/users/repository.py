from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.infrastructure.db.models import User

class UsersRepo:
    def __init__(self, s: AsyncSession): self.s = s
    async def find_by_email(self, email: str) -> User | None:
        res = await self.s.execute(select(User).where(User.email == email))
        return res.scalars().first()
    async def get_by_id(self, uid) -> User | None:
        res = await self.s.execute(select(User).where(User.id == uid))
        return res.scalars().first()
