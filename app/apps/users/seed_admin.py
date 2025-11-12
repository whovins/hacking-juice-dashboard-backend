from __future__ import annotations
import asyncio
from sqlalchemy import select
from passlib.hash import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession


from app.infrastructure.db.session import get_sessionmaker
from app.infrastructure.db.models import User, UserSetting, Role
from app.apps.users.repository import UsersRepo
from app.core.security import hash_password


ADMIN_EMAIL = "admin@admin.com"
ADMIN_PASSWORD = "Admin!23456"


async def main():
    maker = get_sessionmaker()
    async with maker() as session:
        repo = UsersRepo(session)
        email = ADMIN_EMAIL.strip().lower()

        exist = await repo.find_by_email(email)
        if exist:
            print("admin exists:", email)
            return

        user = await repo.create_user(email=email, password=hash_password(ADMIN_PASSWORD), role=Role.admin)

        await session.commit()
        print("seeded:", user.email)


if __name__ == "__main__":
    asyncio.run(main())
