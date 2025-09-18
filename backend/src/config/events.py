import typing

import fastapi
import loguru
from src.common.log import MyLogger
from src.repository.events import (dispose_db_connection,
                                   initialize_db_connection,
                                   initialize_redis_connection,
                                   initialize_kafka_producer,
                                   dispose_redis_connection,
                                   dispose_kafka_producer)
from src.config.manager import settings

def execute_backend_server_event_handler(backend_app: fastapi.FastAPI) -> typing.Any:
    async def launch_backend_server_events() -> None:
        MyLogger().configure_logger()
        #await initialize_db_connection(backend_app=backend_app)
        if settings.ENABLE_REDIS:
            await initialize_redis_connection(backend_app=backend_app)
        if settings.ENABLE_KAFKA:
            await initialize_kafka_producer(backend_app=backend_app)

    return launch_backend_server_events


def terminate_backend_server_event_handler(backend_app: fastapi.FastAPI) -> typing.Any:
    @loguru.logger.catch
    async def stop_backend_server_events() -> None:
        await dispose_db_connection(backend_app=backend_app)
        if settings.ENABLE_REDIS:
            await dispose_redis_connection(backend_app=backend_app)
        if settings.ENABLE_KAFKA:
            await dispose_kafka_producer(backend_app=backend_app)

    return stop_backend_server_events
