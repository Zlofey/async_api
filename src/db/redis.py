import logging
from typing import AsyncIterator

import redis.asyncio as redis

from core.config import REDIS_HOST, REDIS_PORT

logger = logging.getLogger(__name__)


class RedisClient:
    """Обертка для Redis с ленивым созданием клиента."""

    _client: redis.Redis | None = None

    async def get_client(self) -> redis.Redis:
        """Лениво создает и возвращает клиента Redis."""
        if self._client is None:
            self._client = redis.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
            )
            # Пробуем пинг, но не падаем, если Redis недоступен
            try:
                await self._client.ping()
                logger.info("Redis connected")
            except Exception as e:
                logger.warning("Redis not available: %s", e)
        return self._client

    async def close(self) -> None:
        """Закрывает клиент."""
        if self._client is not None:
            await self._client.close()
            logger.info("Redis closed")
            self._client = None


redis_client = RedisClient()


async def get_redis() -> AsyncIterator[redis.Redis]:
    """FastAPI dependency: возвращает клиента Redis."""
    yield await redis_client.get_client()
