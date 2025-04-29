from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.routers import router

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis

from prometheus_fastapi_instrumentator import Instrumentator

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url("redis://redis:6379/", encoding="utf-8", decode_responses=True)
    try:
        await redis.ping()
        print("Redis connection established")
    except Exception as e:
        print(f"Failed to connect to Redis: {e}")
        raise e
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield
app = FastAPI(lifespan=lifespan)
app.include_router(router)

instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"]
)

instrumentator.instrument(app).expose(app)