import enum
import sqlalchemy as sa
from sqlalchemy import Column, String, DateTime, text
from sqlalchemy.dialects.postgresql import UUID
from app.infrastructure.db.session import Base
import uuid

class Role(str, enum.Enum):
    viewer="viewer"; analyst="analyst"; manager="manager"; admin="admin"

role_enum = sa.Enum(Role, name="user_role", create_type=False)

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(role_enum, nullable=False, server_default="viewer")
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=text("now()"))

class UserSetting(Base):
    __tablename__ = "user_settings"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    ui_theme = Column(String(16), nullable=False, server_default="light")
    notify_email = Column(sa.Boolean, nullable=False, server_default=sa.text("true"))
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=text("now()"))
