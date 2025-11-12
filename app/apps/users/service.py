from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.users.repository import UsersRepo
from app.apps.users.user_settings_repository import UserSettingsRepo
from app.core.security import hash_password
from app.apps.users.models import Role
from app.infrastructure.db.session import get_sessionmaker

class UserService:
    def __init__(self, session_maker=None) -> None:
        self._maker = session_maker or get_sessionmaker()
    
    async def create_user(self, *, email: str, password: str, role: Role):
        async with self._maker() as session:
            repo = UsersRepo(session)
            email_norm = email.strip().lower()
            existting = await repo.get_by_email(email_norm)
            if existting:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="email exist")
            hashed = hash_password(password)
            u = await repo.create_user(email=email_norm, password=hashed, role=role)
            await session.commit()
            return u
        
    async def get_user(self, user_id: str):
        async with self._maker() as session:
            repo = UsersRepo(session)
            u = await repo.get_by_id(user_id)
            if not u: 
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
            return u

    async def list_user(self, *, page: int = 1, size: int = 10, query: str | None = None):
        async with self._maker() as session:
            repo = UsersRepo(session)
            items, total = await repo.list(page=page, size=size, query=query)
            return items, total
        

    async def update_user():
        pass
    
    async def delete_user():
        pass
    
   

class SettingService:
    def __init__(self, session_maker=None) -> None:
        self._maker = session_maker or get_sessionmaker()
    async def get_settings(self, user_id: str):
        async with self._maker() as session:
            repo = UserSettingsRepo(session)
            s = await repo.get_by_user_id(user_id)
            return s
    async def update_settings(self, user_id: str, payload: dict):
        async with self._maker() as session:
            repo = UserSettingsRepo(session)
            s = repo.upsert(user_id=user_id, ui_theme=payload.get("ui_theme"), notify_email=payload.get("notify_email"))
            await session.commit()
            return s