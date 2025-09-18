import fastapi
import loguru
from sqlalchemy import event
from sqlalchemy.dialects.postgresql.asyncpg import \
    AsyncAdapt_asyncpg_connection
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSessionTransaction
from sqlalchemy.pool.base import _ConnectionRecord
from src.repository.database import async_db
from src.repository.redis import async_redis
from src.repository.kafka import kafka_manager
# from src.repository.table import Base


if async_db is not None:
    @event.listens_for(target=async_db.async_engine.sync_engine, identifier="connect")
    def inspect_db_server_on_connection(
        db_api_connection: AsyncAdapt_asyncpg_connection, connection_record: _ConnectionRecord
    ) -> None:
        loguru.logger.info(f"New DB API Connection ---\n {db_api_connection}")
        loguru.logger.info(f"Connection Record ---\n {connection_record}")

    @event.listens_for(target=async_db.async_engine.sync_engine, identifier="close")
    def inspect_db_server_on_close(
        db_api_connection: AsyncAdapt_asyncpg_connection, connection_record: _ConnectionRecord
    ) -> None:
        loguru.logger.info(f"Closing DB API Connection ---\n {db_api_connection}")
        loguru.logger.info(f"Closed Connection Record ---\n {connection_record}")

async def initialize_db_tables(connection: AsyncConnection) -> None:
    loguru.logger.info("Database Table Creation --- Initializing . . .")

    # await connection.run_sync(Base.metadata.drop_all)
    # await connection.run_sync(Base.metadata.create_all)

    loguru.logger.info("Database Table Creation --- Successfully Initialized!")

async def initialize_db_connection(backend_app: fastapi.FastAPI) -> None:
    if async_db is None:
        loguru.logger.warning("Database Connection --- Skipped (async_db is None)")
        return

    loguru.logger.info("Database Connection --- Establishing . . .")

    backend_app.state.db = async_db

    async with backend_app.state.db.async_engine.begin() as connection:
        await initialize_db_tables(connection=connection)

    loguru.logger.info("Database Connection --- Successfully Established!")

async def dispose_db_connection(backend_app: fastapi.FastAPI) -> None:
    if async_db is None:
        loguru.logger.warning("Database Connection --- Skipped (async_db is None)")
        return

    loguru.logger.info("Database Connection --- Disposing . . .")

    # await backend_app.state.db.async_engine.dispose()

    loguru.logger.info("Database Connection --- Successfully Disposed!")

async def initialize_redis_connection(backend_app: fastapi.FastAPI) -> None:
    loguru.logger.info("Redis Connection --- Establishing . . .")

    backend_app.state.redis = await async_redis.get_redis()

    loguru.logger.info("Redis Connection --- Successfully Established!")

async def dispose_redis_connection(backend_app: fastapi.FastAPI) -> None:
    loguru.logger.info("Redis Connection --- Disposing . . .")

    await backend_app.state.redis.close()

    loguru.logger.info("Redis Connection --- Successfully Disposed!")

async def initialize_kafka_producer(backend_app: fastapi.FastAPI) -> None:
    loguru.logger.info("Kafka Producer --- Establishing . . .")

    backend_app.state.kafka_producer = await kafka_manager.get_producer()

    loguru.logger.info("Kafka Producer --- Successfully Established!")

async def dispose_kafka_producer(backend_app: fastapi.FastAPI) -> None:
    loguru.logger.info("Kafka Producer --- Disposing . . .")

    await backend_app.state.kafka_producer.stop()

    loguru.logger.info("Kafka Producer --- Successfully Disposed!")
