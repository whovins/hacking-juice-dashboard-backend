FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# 시스템 빌드 툴 (argon2, psycopg 계열 등을 대비)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements-dev.txt ./
RUN pip install -U pip setuptools wheel && \
    pip install -r requirements.txt

# dev 이미지를 따로 쓰고 싶으면 아래 라인을 주석 해제
# RUN pip install -r requirements-dev.txt

COPY . .

# alembic/autogenerate 사용시 로컬타임존 이슈 최소화
ENV TZ=UTC

EXPOSE 8000

# 엔트리포인트에서 마이그레이션 → 앱 기동
ENTRYPOINT ["bash", "ops/entrypoint.api.sh"]
