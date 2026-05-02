import asyncio
import json
import logging
import os
import sys

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "../../.env"))

from aiokafka import AIOKafkaConsumer
from agents.graph import graph

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(message)s",
)
logger = logging.getLogger("aegis.consumer")


async def consume():
    consumer = AIOKafkaConsumer(
        "pr.created",
        bootstrap_servers="localhost:9092",
        group_id="aegis-pipeline",
        auto_offset_reset="latest",
    )
    await consumer.start()
    logger.info("Consumer started — listening on 'pr.created'")

    try:
        async for msg in consumer:
            payload = json.loads(msg.value.decode())
            logger.info(f"Received event: {payload}")

            result = graph.invoke(payload)

            logger.info(f"Pipeline result:")
            logger.info(f"  PR ID:           {result.get('pr_id')}")
            logger.info(f"  Latency Delta:   {result.get('replay_latency_delta')}")
            logger.info(f"  Risk Score:      {result.get('risk_score')}")
            logger.info(f"  Risk Reasoning:  {result.get('risk_reasoning')}")
    except KeyboardInterrupt:
        logger.info("Shutting down consumer...")
    finally:
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(consume())
