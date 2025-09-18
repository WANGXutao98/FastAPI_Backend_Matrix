import traceback

from fastapi import Request, status
from loguru import logger
from src.middleware.base import MyBaseHTTPMiddleware
from src.utilities.messages.exceptions.api.base import unknown_error_internal
from starlette.responses import JSONResponse


class ExceptionHandlerMiddleware(MyBaseHTTPMiddleware):
    @staticmethod
    async def dispatch(request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            if not hasattr(e, "code"):
                logger.exception(e)
            status_code = e.status_code if hasattr(e, "status_code") else status.HTTP_500_INTERNAL_SERVER_ERROR
            return JSONResponse(
                status_code=status_code,
                content={
                    "retCode": e.code if hasattr(e, "code") else status_code,
                    "retMsg": e.detail if hasattr(e, "detail") else unknown_error_internal(),
                    "debugError": e.__class__.__name__,
                    "debugMsg": e.args,
                },
            )
