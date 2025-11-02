from __future__ import annotations
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # ---- app ----
    APP_ENV: str = "dev"
    API_HOST: str = "127.0.0.1"
    API_PORT: int = 8000
    APP_NAME: str = "threat-intel-api" 

    # ---- deps ----
    PG_DSN: str = "postgresql+asyncpg://app:pass@localhost:5432/app"
    REDIS_URL: str = "redis://localhost:6379/0"
    OS_URL: str = "http://localhost:9200"

    # ---- auth ----
    JWT_PRIVATE_KEY: str = "dev-key"
    JWT_PUBLIC_KEY: str = "dev-key"
    JWT_TTL_MIN: int = 30
    JWT_REFRESH_TTL_MIN: int = 10080

    # ---- web/CORS ----
    # 문자열로 받고 property에서 리스트로 변환
    CORS_ORIGINS: str = "http://localhost:5173"
    @property
    def cors_origins(self) -> list[str]:
        v = self.CORS_ORIGINS
        return [s.strip() for s in v.split(",") if s.strip()] if v else []

    # ---- observability ----
    OTEL_EXPORTER_OTLP_ENDPOINT: str | None = None
    OTEL_SAMPLER_RATIO: float = 1.0 

    model_config = SettingsConfigDict(
        env_file=("ops/env/.env.local", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
