import asyncio
import json
from aiokafka import AIOKafkaConsumer
import logging

from services.user import create_user
from models.user import UserCreate

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

async def process_stream(msg):
    pass

async def start_streaming():
    consumer = AIOKafkaConsumer(
        'user-events',  # Тема
        bootstrap_servers='kafka:9092',
        group_id="user-service-group"
    )
    
    await consumer.start()
    logger.info("Kafka consumer started.")

    try:
        async for msg in consumer:
            await process_stream(msg)

    except asyncio.CancelledError:
        logger.info("Streaming cancelled")
    except KeyboardInterrupt:
        logger.info("Streaming stopped")
    finally:
        await consumer.stop()
        logger.info("Kafka consumer stopped.")

# Запуск стриминга
if __name__ == "__main__":
    logger.info("Consumer was started")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_streaming())
