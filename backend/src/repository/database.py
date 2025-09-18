import pydantic
from sqlalchemy.ext.asyncio import AsyncEngine as SQLAlchemyAsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession as SQLAlchemyAsyncSession
from sqlalchemy.ext.asyncio import \
    async_sessionmaker as sqlalchemy_async_sessionmaker
from sqlalchemy.ext.asyncio import \
    create_async_engine as create_sqlalchemy_async_engine
from sqlalchemy.pool import Pool as SQLAlchemyPool
from sqlalchemy.pool import QueuePool as SQLAlchemyQueuePool
from src.config.manager import settings

class AsyncPostgresDatabase:
    def __init__(self):
        self.postgres_uri: pydantic.PostgresDsn = pydantic.PostgresDsn(
            url=f"{settings.DB_POSTGRES_SCHEMA}://{settings.DB_POSTGRES_USERNAME}:{settings.DB_POSTGRES_PASSWORD}@{settings.DB_POSTGRES_HOST}:{settings.DB_POSTGRES_PORT}/{settings.DB_POSTGRES_NAME}",
        )
        self.async_engine: SQLAlchemyAsyncEngine = create_sqlalchemy_async_engine(
            url=self.set_async_db_uri,
            echo=settings.IS_DB_ECHO_LOG,
            pool_size=settings.DB_POOL_SIZE,
            max_overflow=settings.DB_POOL_OVERFLOW,
            poolclass=SQLAlchemyQueuePool,
            pool_pre_ping=True,
        )
        self.async_session: SQLAlchemyAsyncSession = sqlalchemy_async_sessionmaker(
            bind=self.async_engine, autoflush=False, expire_on_commit=False
        )
        self.pool: SQLAlchemyPool = self.async_engine.pool

    @property
    def set_async_db_uri(self) -> str:
        """
        Set the synchronous database driver into asynchronous version by utilizing AsyncPG:

            `postgresql://` => `postgresql+asyncpg://`
        """
        return str(self.postgres_uri)
class AsyncMySQLDatabase:
    def __init__(self):
        self.mysql_uri: pydantic.MySQLDsn = pydantic.MySQLDsn(
            url=f"{settings.DB_MYSQL_SCHEMA}://{settings.DB_MYSQL_USERNAME}:{settings.DB_MYSQL_PASSWORD}@{settings.DB_MYSQL_HOST}:{settings.DB_MYSQL_PORT}/{settings.DB_MYSQL_NAME}",
        )
        self.async_engine: SQLAlchemyAsyncEngine = create_sqlalchemy_async_engine(
            url=self.set_async_db_uri,
            echo=settings.IS_DB_ECHO_LOG,
            pool_size=settings.DB_POOL_SIZE,
            max_overflow=settings.DB_POOL_OVERFLOW,
            poolclass=SQLAlchemyQueuePool,
            pool_pre_ping=True,
        )
        self.async_session: SQLAlchemyAsyncSession = sqlalchemy_async_sessionmaker(
            bind=self.async_engine, autoflush=False, expire_on_commit=False
        )
        self.pool: SQLAlchemyPool = self.async_engine.pool

    @property
    def set_async_db_uri(self) -> str:
        return str(self.mysql_uri)

async_postgres_db: AsyncPostgresDatabase = AsyncPostgresDatabase()
async_mysql_db: AsyncMySQLDatabase = AsyncMySQLDatabase()

if settings.ENABLE_POSTGRES :
    async_db = async_postgres_db
elif settings.ENABLE_MYSQL :
    async_db = async_mysql_db
else:
    async_db = None