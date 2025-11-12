from __future__ import annotations

import enum
import uuid 
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, String, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import  String, DateTime
# import sqlalchemy as sa
from app.infrastructure.db.session import Base

class Role(str, enum.Enum):
    viewer = "viewer"
    analyst = "analyst"
    manager = "manager"
    admin = "admin"

class User(Base):
    
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[Role] = mapped_column(
        Enum(Role, name="user_role", native_enum=True, create_constraint=False),
        nullable=False,
        default=Role.viewer
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

class UserSetting(Base):
    __tablename__ = "user_settings"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, unique=True, index=True)
    ui_theme: Mapped[str] = mapped_column(String(32), nullable=False, server_default="light")
    notify_email: Mapped[dict] = mapped_column(JSON, nullable=False, server_default='{}')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

