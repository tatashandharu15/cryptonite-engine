from redis.asyncio import Redis

from infrastructure.config.settings import get_settings


def create_redis_client() -> Redis:
    settings = get_settings()
    return Redis.from_url(settings.REDIS_URL, decode_responses=True)
