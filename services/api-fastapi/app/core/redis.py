import redis
from app.core.config import settings

_redis_client: redis.Redis | None = None

def get_redis_client() -> redis.Redis:
    """Obtiene o crea una conexión Redis (singleton lazy)."""
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5,
        )
    return _redis_client
