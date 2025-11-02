#!/usr/bin/env bash
set -euo pipefail

# (선택) 의존 서비스 대기 블록은 유지해도 됩니다

# 마이그레이션 잠시 비활성
# alembic upgrade head || true

exec uvicorn app.main:create_app --factory --host 0.0.0.0 --port 8000