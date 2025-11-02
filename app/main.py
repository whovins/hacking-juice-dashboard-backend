# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import get_settings, Settings
from .core.logging import setup_logging
from .core.errors import register_exception_handlers
from .core.health import router as health_router
from .core.rate_limit import limiter, RateLimitMiddleware
from .core.observability import configure_tracing
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from .core.rate_limit import limiter, RateLimitMiddleware

def create_app() -> FastAPI:
    settings: Settings = get_settings()
    setup_logging(env=settings.APP_ENV)

    application = FastAPI(title="Threat Intel API", version="0.1.0")

    # middlewares
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.add_middleware(RateLimitMiddleware)  # 파라미터 없이
    application.state.limiter = limiter
    application.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # observability & errors
    configure_tracing(application, settings)
    register_exception_handlers(application)

    # routers
    application.include_router(health_router)

    @application.on_event("startup")
    async def on_startup() -> None:
        # TODO: readiness 초기화 등
        pass

    @application.on_event("shutdown")
    async def on_shutdown() -> None:
        pass

    return application
