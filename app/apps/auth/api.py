from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.session import get_session
from app.apps.auth.schemas import LoginIn, MeOut, RefreshIn, TokenPairOut
from app.apps.auth.service import AuthService
from app.apps.auth.deps import cur_user, require_roles
from app.apps.users.schemas import UserOut
from app.apps.users.models import Role

router = APIRouter(prefix="/v1/auth", tags=["auth"])

@router.post("/login", response_model=TokenPairOut)
async def login(body: LoginIn, session: AsyncSession = Depends(get_session)):
    service = AuthService(session)
    access_token, refresh_token, _user = await service.login(email=body.email, password=body.password)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }

@router.post("/refresh", response_model=TokenPairOut)
async def refresh(
    body: RefreshIn,
    session: AsyncSession = Depends(get_session)
):
    service = AuthService(session)
    access_token, refresh_token, _user = await service.refresh(refresh_token=body.refresh_token)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


@router.get("/me", response_model=MeOut)
async def me(user=Depends(cur_user)):
    return user

@router.get("/admin/check", dependencies=[Depends(require_roles(Role.admin))])
async def admin_check():
    return {"ok": True}
