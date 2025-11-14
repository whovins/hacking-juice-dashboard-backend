from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.session import Base


class FeedCursor(Base):
    __tablename__ = "feed_cursor"

    # 소스 이름 (nvd, cisa_kev, rss_xxx 등) — PK
    source: Mapped[str] = mapped_column(String(64), primary_key=True)

    # 커서 값 (예: last_modified ISO 문자열, ID, 페이지 토큰 등)
    cursor: Mapped[str] = mapped_column(String(255), nullable=False)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
