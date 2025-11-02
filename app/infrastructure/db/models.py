from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import text
import uuid
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password_hash: Mapped[str]
    role: Mapped[str] = mapped_column(server_default=text("'viewer'"))
    created_at: Mapped[datetime] = mapped_column(server_default=text("now()"))
