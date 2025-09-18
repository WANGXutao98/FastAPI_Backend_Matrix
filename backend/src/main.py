import fastapi
import uvicorn
from fastapi.exceptions import HTTPException, RequestValidationError
from loguru import logger
from src.api.endpoints import router as api_endpoint_router
from src.config.events import (execute_backend_server_event_handler,
                               terminate_backend_server_event_handler)
from src.config.manager import business_settings, settings
from src.middleware import register_middleware
from src.utilities.exceptions.base import (my_http_exception_handler,
                                           my_unhandled_exception
                                           )


def initialize_backend_application() -> fastapi.FastAPI:
    logger.info(settings.__dict__)
    logger.info(business_settings)

    app = fastapi.FastAPI(**settings.set_backend_app_attributes)  # type: ignore

    register_middleware(app)

    app.add_event_handler(
        "startup",
        execute_backend_server_event_handler(backend_app=app),
    )
    app.add_event_handler(
        "shutdown",
        terminate_backend_server_event_handler(backend_app=app),
    )

    app.include_router(router=api_endpoint_router, prefix=settings.API_PREFIX)

    app.add_exception_handler(Exception, my_unhandled_exception)
    app.add_exception_handler(HTTPException, my_http_exception_handler)

    return app


backend_app: fastapi.FastAPI = initialize_backend_application()

if __name__ == "__main__":
    uvicorn.run(
        app="main:backend_app",
        host=settings.BACKEND_SERVER_HOST,
        port=settings.BACKEND_SERVER_PORT,
        reload=settings.DEBUG,
        workers=settings.BACKEND_SERVER_WORKERS,
        log_level=settings.LOGGING_LEVEL,
    )
