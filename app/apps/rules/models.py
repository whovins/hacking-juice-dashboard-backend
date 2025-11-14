from __future__ import annotations

import enum
import uuid

from sqlalchemy import (
    Boolean,
    Enum,
    Integer,
    String,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.session import Base
from app.apps.events.models import EventSeverity


class Rule(Base):
    __tablename__ = "rules"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(1024), nullable=True)

    # OpenSearch 쿼리 문자열 (DSL JSON or KQL 등)
    query: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)

    # 윈도우(초 단위), 예: 3600 = 1시간
    window_sec: Mapped[int] = mapped_column(Integer, nullable=False, default=3600)

    # 임계치 (윈도우 내 이벤트 개수, score 합 등)
    threshold: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    severity: Mapped[EventSeverity] = mapped_column(
        Enum(
            EventSeverity,
            name="rule_severity",
            native_enum=True,
            create_constraint=False,
        ),
        nullable=False,
        default=EventSeverity.medium,
    )

    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    # 알림/액션 정의 (email/telegram/webhook 등)
    actions: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)

    # 같은 키로 일정 시간 동안 suppress (초 단위)
    suppress_for_sec: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
