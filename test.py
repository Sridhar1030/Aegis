# kafka_test.py
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import asyncio

async def main():
    producer = AIOKafkaProducer(bootstrap_servers="localhost:9092")
    await producer.start()

    await producer.send_and_wait("pr.created", b"test-event")

    consumer = AIOKafkaConsumer(
        "pr.created",
        bootstrap_servers="localhost:9092",
        group_id="test"
    )
    await consumer.start()

    async for msg in consumer:
        print(msg.value)
        break

    await producer.stop()
    await consumer.stop()

asyncio.run(main())