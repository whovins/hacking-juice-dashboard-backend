from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    APP_ENV: str = "dev"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    PG_DSN: str
    REDIS_URL: str
    OS_URL: str
    JWT_PRIVATE_KEY: str
    JWT_PUBLIC_KEY: str
    JWT_TTL_MIN: int = 30
    JWT_REFRESH_TTL_MIN: int = 60 * 24 * 7
    CORS_ORIGINS: str = "http://localhost:5173"
    OTEL_EXPORTER_OTLP_ENDPOINT: str | None = None
    RATE_LIMIT_DEFAULT: str = "100/min"


    ILM_POLICY_DAYS_HOT: int = 7
    ILM_POLICY_DAYS_WARM: int = 30
    ILM_POLICY_DAYS_DELETE: int = 180


    DEDUP_TTL_DAYS: int = 14
    SUPPRESS_DEFAULT_HOURS: int = 24


    @property
    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]


    model_config = {"env_file": "ops/env/.env.example", "extra": "ignore"}


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()