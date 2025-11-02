from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class AppError(Exception):
    def __init__(self, title: str, status: int = 400, detail: str | None = None) -> None:
        self.title = title
        self.status = status
        self.detail = detail or title




def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def _app_error(_: Request, exc: AppError):
        return JSONResponse(
            status_code=exc.status,
            content={
            "type": "about:blank",
            "title": exc.title,
            "status": exc.status,
            "detail": exc.detail,
            },
        )