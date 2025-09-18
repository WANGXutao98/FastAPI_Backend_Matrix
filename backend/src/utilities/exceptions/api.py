from fastapi import HTTPException, status
from loguru import logger
from src.utilities.messages.exceptions.api.base import (demo_api_error_test,
                                                        entity_dose_not_exist,
                                                        entity_key_duplicate,
                                                        unknown_error_internal)


class APIException(HTTPException):
    code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = unknown_error_internal()

    def __init__(self, message=None, code=None):
        if code is not None:
            self.code = code
        if message is not None:
            self.message += message

        super().__init__(status_code=status.HTTP_200_OK, detail=message)


class DemoTestException(APIException):
    code = -13000
    message = demo_api_error_test()


class APIEntityDoesNotExist(APIException):
    code = -13001
    message = entity_dose_not_exist()


class APIEntityKeyDuplicate(APIException):
    code = -13002
    message = entity_key_duplicate()


class AilabAuthServerInternalError(APIException):
    code = -13200
    message = "ailab auth server internal error!"


class APIDatasetAppGroupNotMatch(APIException):
    code = -13300
    message = "Evaluation Task`s App Group is not match with Dataset`s!"




class CeleryOperationError(APIException):
    code = -13500
    message = "celery error!"
