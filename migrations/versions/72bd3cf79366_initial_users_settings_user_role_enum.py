# migrations/versions/<rev>_initial.py
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "72bd3cf79366"
down_revision = None
branch_labels = None
depends_on = None

# 모델과 동일한 이름, 수동 생성
user_role = postgresql.ENUM("viewer","analyst","manager","admin", name="user_role", create_type=False)

def _has_table(conn, name: str) -> bool:
    insp = sa.inspect(conn)
    return insp.has_table(name)

def upgrade() -> None:
    conn = op.get_bind()

    # 1) ENUM 타입 없으면 생성
    op.execute("""
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT 1 FROM pg_type t
            JOIN pg_namespace n ON n.oid = t.typnamespace
            WHERE t.typname = 'user_role'
        ) THEN
            CREATE TYPE user_role AS ENUM ('viewer','analyst','manager','admin');
        END IF;
    END$$;
    """)

    # 2) users 테이블 없으면 생성
    if not _has_table(conn, "users"):
        op.create_table(
            "users",
            sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
            sa.Column("email", sa.String(length=255), nullable=False, unique=True),
            sa.Column("password_hash", sa.String(length=255), nullable=False),
            sa.Column("role", user_role, nullable=False, server_default="viewer"),
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        )
        op.create_index("ix_users_email", "users", ["email"], unique=True)

    # 3) user_settings 테이블 없으면 생성
    if not _has_table(conn, "user_settings"):
        op.create_table(
            "user_settings",
            sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
            sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False),
            sa.Column("ui_theme", sa.String(length=16), server_default="light", nullable=False),
            sa.Column("notify_email", sa.Boolean(), server_default=sa.text("true"), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        )

def downgrade() -> None:
    # 역순 제거(존재할 때만)
    conn = op.get_bind()
    if _has_table(conn, "user_settings"):
        op.drop_table("user_settings")
    if _has_table(conn, "users"):
        op.drop_index("ix_users_email", table_name="users")
        op.drop_table("users")
    op.execute("""
    DO $$
    BEGIN
        IF EXISTS (
            SELECT 1 FROM pg_type t
            JOIN pg_namespace n ON n.oid = t.typnamespace
            WHERE t.typname = 'user_role'
        ) THEN
            DROP TYPE user_role;
        END IF;
    END$$;
    """)
