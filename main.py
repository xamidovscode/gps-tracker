import asyncio

from fastapi import FastAPI
from app.api.routes import router
from app.services.redis_listner import listen_to_redis
from app.services.tcp_handler import start
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_listen = asyncio.create_task(listen_to_redis())
    redis_send = asyncio.create_task(start())

    print("Redis listener started.")

    yield

    redis_listen.cancel()
    redis_send.cancel()

    try:
        await redis_listen
    except asyncio.CancelledError:
        print("Redis listener stopped.")

    try:
        await start
    except asyncio.CancelledError:
        print("Another worker to‘xtadi.")

app = FastAPI(lifespan=lifespan)
app.include_router(router)
