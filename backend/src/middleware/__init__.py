from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI
from src.config.manager import settings
from src.middleware.exception import ExceptionHandlerMiddleware
from src.middleware.logging import CustomLoggingMiddleware
from starlette.middleware.cors import CORSMiddleware


def register_middleware(app: FastAPI) -> None:
    # cors
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=settings.IS_ALLOWED_CREDENTIALS,
        allow_methods=settings.ALLOWED_METHODS,
        allow_headers=settings.ALLOWED_HEADERS,
        expose_headers=["X-Request-ID"],
    )
    app.add_middleware(CustomLoggingMiddleware)
    app.add_middleware(ExceptionHandlerMiddleware)

    # ASGI Correlation
    app.add_middleware(CorrelationIdMiddleware, header_name="X-Request-ID")
