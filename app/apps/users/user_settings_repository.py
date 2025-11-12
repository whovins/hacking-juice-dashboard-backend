from __future__ import annotations

from typing import Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.users.models import UserSetting


class UserSettingsRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_user_id(self, user_id: str | UUID) -> Optional[UserSetting]:
        stmt = select(UserSetting).where(UserSetting.user_id == UUID(str(user_id)))
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()
    
    async def create(self, *, user_id: str | UUID, ui_theme: str = "light", notify_email: dict | None = None) -> UserSetting:
        s = UserSetting(user_id=UUID(str(user_id)), ui_theme=ui_theme, notify_email=notify_email or {})
        self.session.add(s)
        await self.session.flush()
        return s
        
    async def upsert(self, *, user_id: str | UUID, ui_theme: str | None = None, notify_email: dict | None = None) -> UserSetting:
        s = await self.get_by_user_id(user_id)
        if s:
            if ui_theme is not None:
                s.ui_theme = ui_theme
            if notify_email is not None:
                s.notify_email = notify_email
            await self.session.flush()
            return s
        return await self.create(user_id=user_id, ui_theme=ui_theme or "light", notify_email=notify_email or {})