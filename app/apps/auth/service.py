from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.users.repository import UsersRepo
from app.core.security import verify_password
from app.core.jwt import issue_access_refresh, decode_jwt

from fastapi import HTTPException, status

class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.users = UsersRepo(session)
    async def login(self, *, email: str, password: str):
        email = email.strip().lower()
        user = await self.users.get_by_email(email)
        if not user or not verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid_credentials"
            )
        
        access_token, refresh_token = issue_access_refresh(sub=str(user.id), role=user.role.name)
        return access_token, refresh_token, user
    
    async def refresh(self, *, refresh_token: str): 
        try: 
            payload = decode_jwt(refresh_token)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid_token"
            )
        
        if payload.get("typ") != "refresh":
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
        
        user = await self.users.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="user_not_found"
            )
        
        access_token, new_refresh_token = issue_access_refresh(sub=str(user.id), role=user.role.name)
        return access_token, new_refresh_token, user
