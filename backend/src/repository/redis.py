from src.config.manager import settings
# from aioredis import Redis
from redis.asyncio import Redis

class AsyncRedis:
    def __init__(self):
        self.redis_uri = f"redis://{settings.DB_REDIS_HOST}:{settings.DB_REDIS_PORT}"
        self.redis = Redis.from_url(
            self.redis_uri,
            password=settings.DB_REDIS_PASSWORD,
            db=settings.DB_REDIS_DB,
            encoding="utf-8",
            decode_responses=True
        )

    async def get_redis(self):
        return self.redis
    
async_redis: AsyncRedis = AsyncRedis()