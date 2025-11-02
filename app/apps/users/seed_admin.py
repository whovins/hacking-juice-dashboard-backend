import asyncio
from sqlalchemy import select
from passlib.hash import bcrypt

from app.infrastructure.db.session import get_sessionmaker
from app.infrastructure.db.models import User, UserSetting, Role


ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "Admin!23456"


async def main():
    maker = get_sessionmaker()
    async with maker() as s:
        email = ADMIN_EMAIL.strip().lower()

        exist = (await s.execute(select(User).where(User.email == email))).scalars().first()
        if exist:
            print("admin exists")
            return

        u = User(email=email, password_hash=bcrypt.hash(ADMIN_PASSWORD), role=Role.admin)
        s.add(u)
        await s.flush()
        s.add(UserSetting(user_id=u.id))
        await s.commit()
        print("seeded:", email)


if __name__ == "__main__":
    asyncio.run(main())
