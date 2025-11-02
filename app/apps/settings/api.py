from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.session import get_session
from app.core.security import current_user_claims
from app.apps.settings.schemas import SettingOut, SettingUpdate
from app.apps.settings.repository import SettingsRepo

router = APIRouter(prefix="/v1/settings", tags=["settings"])

@router.get("", response_model=SettingOut)
async def get_settings(claims=Depends(current_user_claims), s: AsyncSession = Depends(get_session)):
    repo = SettingsRepo(s)
    row = await repo.get_by_user(claims["sub"])
    if not row:
        row = await repo.upsert(claims["sub"])
    return {"ui_theme": row.ui_theme, "notify_email": row.notify_email}

@router.put("", response_model=SettingOut)
async def update_settings(body: SettingUpdate, claims=Depends(current_user_claims), s: AsyncSession = Depends(get_session)):
    repo = SettingsRepo(s)
    row = await repo.upsert(claims["sub"], ui_theme=body.ui_theme, notify_email=body.notify_email)
    return {"ui_theme": row.ui_theme, "notify_email": row.notify_email}
