from __future__ import annotations

import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    DateTime,
    Enum,
    Float,
    String,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.session import Base


class IOCType(str, enum.Enum):
    ipv4 = "ipv4"
    ipv6 = "ipv6"
    domain = "domain"
    url = "url"
    hash = "hash"
    email = "email"
    cve = "cve"
    other = "other"


class IOCIndex(Base):
    __tablename__ = "ioc_index"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    ioc: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    ioc_type: Mapped[IOCType] = mapped_column(
        Enum(
            IOCType,
            name="ioc_type",
            native_enum=True,
            create_constraint=False,
        ),
        nullable=False,
        index=True,
    )

    first_seen: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    last_seen: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    # 어떤 소스에서, 몇 번 나왔는지 요약
    # 예: {"sources": {"nvd": 10, "kev": 3}, "refs": ["..."]}
    sources: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)

    # 단순 점수 (0~100 등, KEV/EPSS/VT 기반)
    score: Mapped[float] = mapped_column(Float, nullable=True)
