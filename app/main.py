import asyncio

from fastapi import FastAPI

from app.api.routes import router
from app.mq.kafka import start_kafka
from app.mq.rabbit import connect_rabbit, consume
from app.service import process_search

app = FastAPI()

app.include_router(router)

async def rabbit_worker():
    async def handler(msg):
        await process_search(
            msg["search_string"]
        )
    await consume(handler)

@app.on_event("startup")
async def startup():
    await connect_rabbit()
    await start_kafka()
    asyncio.create_task(
        rabbit_worker()
    )