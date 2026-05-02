from fastapi import APIRouter
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import asyncio
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("aegis.webhook")

router = APIRouter()
producer = None

async def get_producer():
    global producer
    if not producer:
        producer = AIOKafkaProducer(bootstrap_servers="localhost:9092")
        await producer.start()
    return producer

async def consume_pr_events():
    consumer = AIOKafkaConsumer(
        "pr.created",
        bootstrap_servers="localhost:9092",
        group_id="aegis-logger",
    )
    await consumer.start()
    logger.info("Kafka consumer started on 'pr.created'")
    try:
        async for msg in consumer:
            payload = json.loads(msg.value.decode())
            logger.info(f"[pr.created] offset={msg.offset} payload={payload}")
    finally:
        await consumer.stop()

@router.on_event("startup")
async def start_consumer():
    asyncio.create_task(consume_pr_events())

@router.post("/github")
async def github_webhook(data: dict):
    p = await get_producer()
    await p.send_and_wait("pr.created", json.dumps(data).encode())
    return {"status": "sent"}