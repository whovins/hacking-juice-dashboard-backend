from __future__ import annotations

import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    DateTime,
    Enum,
    String,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.session import Base
from app.apps.events.models import EventSeverity


class AlertStatus(str, enum.Enum):
    open = "open"
    ack = "ack"
    closed = "closed"


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    rule_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        index=True,
    )

    ts: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )

    severity: Mapped[EventSeverity] = mapped_column(
        Enum(
            EventSeverity,
            name="alert_severity",
            native_enum=True,
            create_constraint=False,
        ),
        nullable=False,
        default=EventSeverity.medium,
        index=True,
    )

    # 엔티티(주요 대상) — 예: host/IP/user/IOC 값 등
    entity: Mapped[str] = mapped_column(String(255), nullable=True, index=True)

    # 룰 매칭 결과(이벤트 목록, 집계 값 등)
    matches: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)

    status: Mapped[AlertStatus] = mapped_column(
        Enum(
            AlertStatus,
            name="alert_status",
            native_enum=True,
            create_constraint=False,
        ),
        nullable=False,
        default=AlertStatus.open,
        index=True,
    )

    # 담당자(선택), 이메일 또는 이름
    assignee: Mapped[str | None] = mapped_column(String(255), nullable=True)
