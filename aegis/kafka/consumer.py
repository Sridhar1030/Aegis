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

            logger.info("=" * 60)
            logger.info(f"PIPELINE RESULT for {result.get('pr_id')}")
            logger.info("=" * 60)
            logger.info(f"  Replay Latency:    {result.get('replay_latency_delta')}s")
            logger.info(f"  Similar Failures:  {result.get('similar_failures')}")
            logger.info(f"  Risk Score:        {result.get('risk_score')}")
            logger.info(f"  Risk Reasoning:    {result.get('risk_reasoning')}")
            logger.info(f"  Anomaly Detected:  {result.get('anomaly_detected')}")
            if result.get("anomaly_detected"):
                logger.warning("  >>> ROLLBACK TRIGGERED <<<")
            else:
                logger.info("  >>> DEPLOYMENT APPROVED <<<")
            logger.info("=" * 60)
    except KeyboardInterrupt:
        logger.info("Shutting down consumer...")
    finally:
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(consume())
