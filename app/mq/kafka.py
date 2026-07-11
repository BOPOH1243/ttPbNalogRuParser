import json
from aiokafka import AIOKafkaProducer
from app.config import settings

producer: AIOKafkaProducer | None = None

async def start_kafka():
    global producer
    producer = AIOKafkaProducer(
        bootstrap_servers=settings.KAFKA_BOOTSTRAP
    )
    await producer.start()

async def stop_kafka():
    if producer:
        await producer.stop()

async def send_kafka(data: dict):
    await producer.send_and_wait(
        settings.KAFKA_TOPIC,
        json.dumps(
            data,
            ensure_ascii=False
        ).encode()
    )