from __future__ import annotations

import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    DateTime,
    Enum,
    Float,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.session import Base


class EventSeverity(str, enum.Enum):
    info = "info"
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class Event(Base):
    __tablename__ = "events"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    ts: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )

    source: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(64), nullable=False, index=True)

    severity: Mapped[EventSeverity] = mapped_column(
        Enum(
            EventSeverity,
            name="event_severity",
            native_enum=True,
            create_constraint=False,
        ),
        nullable=False,
        default=EventSeverity.info,
        index=True,
    )

    score: Mapped[float] = mapped_column(Float, nullable=True)

    title: Mapped[str] = mapped_column(String(512), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=True)

    # IOC 목록, 예: {"ipv4": ["1.2.3.4"], "cve": ["CVE-2024-1234"], ...}
    iocs: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)

    # 태그 배열, 예: ["nvd", "cisa_kev", "ransomware"]
    tags: Mapped[list[str]] = mapped_column(
        ARRAY(String(64)),
        nullable=False,
        default=list,
    )

    raw: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)

    hash_key: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)
