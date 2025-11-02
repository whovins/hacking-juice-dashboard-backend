from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.session import get_session
from app.apps.auth.schemas import LoginIn, MeOut, RefreshIn
from app.apps.auth.service import AuthService
from app.core.security import current_user_claims, verify, issue_tokens

router = APIRouter(prefix="/v1/auth", tags=["auth"])

@router.post("/login")
async def login(body: LoginIn, s: AsyncSession = Depends(get_session)):
    svc = AuthService(s)
    return await svc.login(body.email, body.password)

from app.apps.users.repository import UsersRepo
@router.get("/me", response_model=MeOut)
async def me(claims: dict = Depends(current_user_claims), s: AsyncSession = Depends(get_session)):
    u = await UsersRepo(s).get_by_id(claims["sub"])
    return {"id": str(u.id), "email": u.email, "role": u.role.value}

@router.post("/refresh")
async def refresh(body: RefreshIn):
    claims = verify(body.refresh_token)
    if claims.get("typ") != "refresh":
        raise HTTPException(status_code=401, detail="invalid_token_type")
    return issue_tokens(claims["sub"], claims["role"])
