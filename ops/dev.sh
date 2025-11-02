#!/usr/bin/env bash
# Portable dev runner: works on macOS bash 3.2 (no `wait -n`)
set -euo pipefail

# 1) 로컬 env 자동 로드
if [ -f "ops/env/.env.local" ]; then
  set -a; source ops/env/.env.local; set +a
fi

# 2) API + 워커 동시 실행 (핫리로드/오토워치)
uvicorn app.main:create_app --factory --reload &
UV_PID=$!
dramatiq app.workers.worker --watch app &
WK_PID=$!

cleanup() {
  kill "$UV_PID" "$WK_PID" 2>/dev/null || true
}
trap cleanup INT TERM EXIT

# 3) 양쪽 중 하나가 종료될 때까지 대기 (wait -n 대체 루프)
while :; do
  if ! kill -0 "$UV_PID" 2>/dev/null; then
    wait "$UV_PID" || true
    break
  fi
  if ! kill -0 "$WK_PID" 2>/dev/null; then
    wait "$WK_PID" || true
    break
  fi
  sleep 0.5
done
