import logging
from typing import AsyncIterator

from elasticsearch import AsyncElasticsearch

from core.config import ELASTIC_HOST, ELASTIC_PORT

logger = logging.getLogger(__name__)


class ElasticClient:
    _client: AsyncElasticsearch | None = None

    @classmethod
    async def get_client(cls) -> AsyncElasticsearch:
        """Возвращает клиента, создавая его при первом вызове."""
        if cls._client is None:
            cls._client = AsyncElasticsearch(
                hosts=[{"host": ELASTIC_HOST, "port": ELASTIC_PORT, "scheme": "http"}]
            )
            logger.info("Elasticsearch client created")
        return cls._client

    @classmethod
    async def close(cls) -> None:
        """Закрывает клиент."""
        if cls._client is not None:
            await cls._client.close()
            logger.info("Elasticsearch closed")
            cls._client = None


async def get_elastic() -> AsyncIterator[AsyncElasticsearch]:
    """FastAPI dependency: возвращает клиента Elasticsearch."""
    yield await ElasticClient.get_client()
