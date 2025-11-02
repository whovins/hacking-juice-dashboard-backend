from redis.asyncio import Redis
from ...core.config import get_settings


_settings = get_settings()
redis = Redis.from_url(_settings.REDIS_URL, decode_responses=True)