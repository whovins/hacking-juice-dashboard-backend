from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.session import get_session
from app.apps.users.service import UserService
from app.apps.users.schemas import UserCreate, UserOut, UserUpdateIn, PageUsers
from app.apps.auth.deps import require_roles,  cur_user
from app.apps.users.models import Role

router = APIRouter(prefix="/v1/users", tags=["users"])

@router.post("", response_model=UserOut, dependencies=[Depends(require_roles(Role.admin))])
async def create_user(body: UserCreate):
    svc = UserService()
    u = await svc.create_user(email=body.email, password=body.password, role=body.role)
    return u

@router.get("/{user_id}", response_model=UserOut, dependencies=[Depends(require_roles(Role.admin))])
async def get_user(user_id: str = Path(...)):
    svc = UserService()
    u = await svc.get_user(user_id)
    print("DEBUG user type:", type(u), "user:", u)
    return u

@router.get("", response_model=PageUsers, dependencies=[Depends(require_roles(Role.admin))])
async def list_user(page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=200), q: str | None = Query(None)):
    svc = UserService()
    items, total = await svc.list_user(page=page, size=size, query=q)
    print("DEBUG items types:", [type(x) for x in items])
    return {"items": items, "total": total, "page": page, "size": size}

async def update_user():
    pass

async def delete_user():
    pass

