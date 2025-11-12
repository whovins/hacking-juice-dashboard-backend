from __future__ import annotations

import enum
import uuid 
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Column, String, DateTime, text
import sqlalchemy as sa
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

class UserSetting(Base):
    __tablename__ = "user_settings"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    ui_theme = Column(String(16), nullable=False, server_default="light")
    notify_email = Column(sa.Boolean, nullable=False, server_default=sa.text("true"))
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=text("now()"))

