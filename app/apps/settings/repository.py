from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.infrastructure.db.models import UserSetting

class SettingsRepo:
    def __init__(self, s: AsyncSession): self.s = s
    async def get_by_user(self, uid):
        res = await self.s.execute(select(UserSetting).where(UserSetting.user_id==uid))
        return res.scalars().first()
    async def upsert(self, uid, ui_theme=None, notify_email=None):
        row = await self.get_by_user(uid)
        if not row:
            row = UserSetting(user_id=uid)
            self.s.add(row)
            await self.s.flush()
        if ui_theme is not None: row.ui_theme = ui_theme
        if notify_email is not None: row.notify_email = notify_email
        await self.s.commit()
        return row
