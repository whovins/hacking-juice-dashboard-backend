from typing import Callable
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# 전역 리미터 (라우트 데코레이터에서 사용)
limiter = Limiter(key_func=get_remote_address)

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:  # type: ignore[override]
        # slowapi는 app.state.limiter 를 참조함
        request.app.state.limiter = limiter
        try:
            response = await call_next(request)
        except RateLimitExceeded as exc:
            # 표준 에러 응답(JSON, 429)
            return _rate_limit_exceeded_handler(request, exc)
        return response
