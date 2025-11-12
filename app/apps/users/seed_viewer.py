from __future__ import annotations
import asyncio


from app.infrastructure.db.session import get_sessionmaker
from app.infrastructure.db.models import Role
from app.apps.users.repository import UsersRepo
from app.core.security import hash_password


TEST_EMAIL = "test@test.com"
TEST_PASSWORD = "Test!23456"


async def main():
    maker = get_sessionmaker()
    async with maker() as session:
        repo = UsersRepo(session)
        email = TEST_EMAIL.strip().lower()

        exist = await repo.get_by_email(email)
        if exist:
            print("admin exists:", email)
            return

        user = await repo.create_user(email=email, password=hash_password(TEST_PASSWORD), role=Role.viewer)

        await session.commit()
        print("seeded:", user.email)


if __name__ == "__main__":
    asyncio.run(main())
