import json
import aio_pika

from app.config import settings

connection = None
channel = None

async def connect_rabbit():
    global connection, channel
    connection = await aio_pika.connect_robust(
        settings.RABBIT_URL
    )
    channel = await connection.channel()


async def send_status(data: dict):
    queue = await channel.declare_queue(
        settings.RABBIT_STATUS_QUEUE
    )

    await channel.default_exchange.publish(
        aio_pika.Message(
            json.dumps(
                data,
                ensure_ascii=False
            ).encode()
        ),
        routing_key=queue.name
    )



async def consume(callback):
    queue = await channel.declare_queue(
        settings.RABBIT_REQUEST_QUEUE
    )
    async with queue.iterator() as iterator:
        async for message in iterator:
            async with message.process():
                body = json.loads(
                    message.body
                )
                await callback(body)