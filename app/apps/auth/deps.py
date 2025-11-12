from __future__ import annotations

from typing import Iterable, Callable

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.session import get_session
from app.core.jwt import decode_jwt
from app.apps.users.repository import UsersRepo
from app.apps.users.models import Role

async def cur_user(
        request: Request,
        session: AsyncSession = Depends(get_session)
):
    auth_header = request.headers.get("authorization") or request.headers.get("Authorization")
    if not auth_header or not auth_header.lower().startswith("bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="missing_token"
        )
    
    token = auth_header.split(" ", 1)[1].strip()
    try:
        payload = decode_jwt(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid_token"
        )
    if payload.get("typ") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid_token_type"
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid_token"
        )
    
    repo = UsersRepo(session)
    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="user_not_found"
        )
    
    return user

    
def require_roles(*roles: Iterable[Role]) -> Callable:
    allowed = {r.value if isinstance(r, Role) else str(r) for r in roles}

    async def _checker(user=Depends(cur_user)):
        if allowed and user.role.name not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="forbidden"
            )
        return user
    return _checker