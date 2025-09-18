import json
import time
from datetime import datetime
from json import JSONDecodeError
from typing import Awaitable, Callable, Dict, List, Tuple

from loguru import logger
from src.utilities.authorize.paas_auth import g_paas_auth
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, StreamingResponse
from starlette.types import Message, Scope


class RequestWithBody(Request):
    """Creation of new request with body"""

    def __init__(self, scope: Scope, body: bytes) -> None:
        super().__init__(scope, self._receive)
        self._body = body
        self._body_returned = False

    async def _receive(self) -> Message:
        if self._body_returned:
            return {"type": "http.disconnect"}
        self._body_returned = True
        return {"type": "http.request", "body": self._body, "more_body": False}


class CustomLoggingMiddleware(BaseHTTPMiddleware):
    """
    Use of custom middleware since reading the request body and the response consumes the bytestream.
    Hence this approach to basically generate a new request/response when we read the attributes for logging.
    """

    @classmethod
    async def dispatch(cls, request: Request, call_next: Callable[[Request], Awaitable[StreamingResponse]]) -> Response:
        logger.info(
            f"{'*'*30} request start!!!!!{'*'*30} [Method: {request.method}] [Request: {request.url}] [Client: {request.client}]"
        )
        start_time = time.time()
        request_body_bytes = await request.body()

        # user = await g_paas_auth.get_login_user(request)
        user = {
            "user_fullname": "lynnlchen(陈凌)",
            "user_id": 1,
            "user_name": "lynnlchen",
            "user_type": "tof4",
            "user_uuid": "tof4_60567",
        }
        request.state.user_name = user["user_name"]

        request_with_body = RequestWithBody(request.scope, request_body_bytes)
        response = await call_next(request_with_body)
        response_content_bytes, response_headers, response_status = await cls._get_response_params(response)
        try:
            req_body = json.loads(request_body_bytes)
        except JSONDecodeError:
            req_body = ""
        except UnicodeDecodeError:
            logger.exception("Invalid JSON data: non-UTF-8 encoding")
            req_body = ""

        try:
            rsp_body = json.loads(response_content_bytes)
        except JSONDecodeError:
            rsp_body = ""
        except UnicodeDecodeError:
            logger.exception("Invalid JSON data: non-UTF-8 encoding")
            rsp_body = ""

        end_time = time.time()

        logger.info(
            f"{'*'*30}request finish!!!!!{'*'*30} [User: {request.state.user_name}] [Method: {request.method}] [Request: {request.url}] [Request_Body: {req_body}] [Status_code: {response.status_code}] [Response: {rsp_body if len(rsp_body) < 1000 else rsp_body[:1000]}] [Total_cost: {end_time - start_time:.2f} seconds] "
        )
        return Response(response_content_bytes, response_status, response_headers)

    @staticmethod
    async def _get_response_params(
        response: StreamingResponse,
    ) -> Tuple[bytes, Dict[str, str], int]:
        """Getting the response parameters of a response and create a new response."""
        response_byte_chunks: List[bytes] = []
        response_status: List[int] = []
        response_headers: List[Dict[str, str]] = []

        async def send(message: Message) -> None:
            if message["type"] == "http.response.start":
                response_status.append(message["status"])
                response_headers.append({k.decode("utf8"): v.decode("utf8") for k, v in message["headers"]})
            else:
                response_byte_chunks.append(message["body"])

        await response.stream_response(send)
        content = b"".join(response_byte_chunks)
        return (content, response_headers[0], response_status[0])
