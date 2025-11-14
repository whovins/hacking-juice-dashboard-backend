
from __future__ import annotations

from app.infrastructure.db.session import Base

from app.apps.users.models import User, Role, UserSetting


# 각 앱의 models를 import해서 Base.metadata에 등록만 한다 (side-effect)
import app.apps.users.models     # noqa: F401
import app.apps.events.models    # noqa: F401
import app.apps.ioc.models       # noqa: F401
import app.apps.rules.models     # noqa: F401
import app.apps.alerts.models    # noqa: F401
import app.apps.audit.models     # noqa: F401
import app.apps.ingest.models    # noqa: F401

__all__ = [
    "Base",
    "User",
    "Role",
    "UserSetting"
]

