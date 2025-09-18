import traceback
import uuid
from typing import Union

from fastapi import Request, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.openapi.constants import REF_PREFIX
from fastapi.openapi.utils import validation_error_response_definition
from loguru import logger
from pydantic import ValidationError
from src.utilities.ipaddress.ip_address import IpAddress
from src.utilities.messages.exceptions.api.base import unknown_error_internal
from starlette.responses import JSONResponse


async def my_unhandled_exception(request: Request, exc: HTTPException) -> JSONResponse:
    logger.error("my_unhandled_exception called")

    # err_msg = traceback.format_exc()
    logger.exception(exc)
    return await my_http_exception_handler(request, exc)


async def my_http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    status_code = status.HTTP_200_OK
    message = exc.message if hasattr(exc, "message") else unknown_error_internal()
    default_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    if hasattr(exc, "status_code"):
        status_code = exc.status_code
        default_code = exc.status_code
    if hasattr(exc, "detail"):
        message = exc.detail

    if not hasattr(exc, "code"):
        logger.exception(exc)

    return JSONResponse(
        status_code=status_code,
        content={
            "retCode": exc.code if hasattr(exc, "code") else default_code,
            "retMsg": message,
            "clientIp": IpAddress.get_client_ip(request),
        },
    )


validation_error_response_definition["properties"] = {
    "errors": {
        "title": "Errors",
        "type": "array",
        "items": {"$ref": "{0}ValidationError".format(REF_PREFIX)},
    },
}
