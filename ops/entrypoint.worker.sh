#!/usr/bin/env bash
set -euo pipefail

# DB/Redis/OS 대기
bash ops/entrypoint.api.sh true >/dev/null 2>&1 || true

# Dramatiq 워커 기동
exec python -m app.workers.worker
