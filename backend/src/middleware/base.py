from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class MyBaseHTTPMiddleware(BaseHTTPMiddleware):
    async def __call__(self, scope, receive, send):
        try:
            await super().__call__(scope, receive, send)
        except RuntimeError as exc:
            logger.exception(str(exc))
            if str(exc) == "No response returned.":
                request = Request(scope, receive=receive)
                if await request.is_disconnected():
                    logger.warning(str(exc))
                    return
            raise

    async def dispatch(self, request, call_next):
        raise NotImplementedError()
