from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.v1 import films
from db.elastic import ElasticClient, logger
from db.redis import redis_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up")

    yield

    logger.info("Shutting down")
    await redis_client.close()
    await ElasticClient.close()


app = FastAPI(
    # title=config.PROJECT_NAME,
    title="Read-only API для онлайн-кинотеатра",
    docs_url="/api/openapi",
    openapi_url="/api/open",
    description="Информация о фильмах, жанрах и людях, участвовавших в создании произведения",
    lifespan=lifespan,
)

app.include_router(films.router, prefix="/api/v1/films", tags=["films"])
