# migrations/env.py
from __future__ import annotations

from logging.config import fileConfig
from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.config import get_settings
from app.infrastructure.db import models

Base = models.Base

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata
PG_DSN = get_settings().PG_DSN  # postgresql+asyncpg://...


def run_migrations_offline() -> None:
    """
    오프라인 모드 (SQL만 생성)에서 마이그레이션 실행.
    """
    context.configure(
        url=PG_DSN,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        # JSON 기본값 비교 때문에 에러 나서 False 로 설정
        compare_server_default=False,
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """
    온라인 모드에서 실제 DB에 마이그레이션 실행.
    """
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        # 여기도 False 로 꺼줍니다.
        compare_server_default=False,
        render_as_batch=False,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    connectable: AsyncEngine = create_async_engine(
        PG_DSN,
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as conn:
        await conn.run_sync(do_run_migrations)
    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio
    asyncio.run(run_migrations_online())
