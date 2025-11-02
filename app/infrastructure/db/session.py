from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

from app.core.config import settings

Base = declarative_base()

_engine: AsyncEngine | None = None
_sessionmaker: async_sessionmaker[AsyncSession] | None = None


def get_engine() -> AsyncEngine:
    global _engine, _sessionmaker
    if _engine is None:
        _engine = create_async_engine(
            settings.PG_DSN, pool_pre_ping=True, future=True
        )
        _sessionmaker = async_sessionmaker(
            _engine, expire_on_commit=False, autoflush=False, autocommit=False
        )
    return _engine


def get_sessionmaker() -> async_sessionmaker[AsyncSession]:
    global _sessionmaker
    if _sessionmaker is None:
        get_engine()
    return _sessionmaker  # type: ignore[return-value]


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    maker = get_sessionmaker()
    async with maker() as s:
        yield s


# alembic/env.py나 스크립트에서 직접 세션메이커가 필요할 때 사용
async_session = get_sessionmaker()