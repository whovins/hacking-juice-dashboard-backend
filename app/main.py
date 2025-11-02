# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import get_settings, Settings, settings
from .core.logging import setup_logging
from .core.errors import register_exception_handlers
from .core.health import router as health_router
from .core.rate_limit import limiter, RateLimitMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from app.apps.auth.api import router as auth_router
from app.apps.settings.api import router as settings_router
from app.core.observability import configure_tracing

def create_app() -> FastAPI:
    settings: Settings = get_settings()
    setup_logging(env=settings.APP_ENV)

    app = FastAPI(title="Threat Intel API", version="0.1.0")

    # middlewares
    app.add_middleware(
    CORSMiddleware,
        allow_origins=settings.cors_origins, 
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RateLimitMiddleware)  # 파라미터 없이
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # observability & errors
    configure_tracing(app, settings)
    register_exception_handlers(app)

    # routers
    app.include_router(health_router)

    @app.on_event("startup")
    async def on_startup() -> None:
        # TODO: readiness 초기화 등
        pass

    @app.on_event("shutdown")
    async def on_shutdown() -> None:
        pass

    app.include_router(auth_router)
    app.include_router(settings_router)

    return app
