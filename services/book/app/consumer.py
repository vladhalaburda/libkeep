import asyncio
import json
from aiokafka import AIOKafkaConsumer, ConsumerRebalanceListener
import logging

from services.book import insert_user_book

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

async def process_stream(msg):
    try:
        print(msg.value)
        data = json.loads(msg.value.decode("utf-8"))
        if data.get("event") == "user_created":
            body = data.get("body")
            if body:
                created_id = body.get("id")
                if created_id:
                    await insert_user_book(created_id)
                else:
                    logger.warning("Missing 'id' in 'body'")
            else:
                logger.warning("Missing 'body' in message")
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON: {msg.value()}")
    except Exception as e:
        logger.error(f"Error processing message: {e}", exc_info=True)

async def start_streaming():
    consumer = AIOKafkaConsumer(
        'user-events',
        bootstrap_servers='kafka:9092',
        group_id="book-service-group",
        session_timeout_ms=30000,
        heartbeat_interval_ms=10000,
        max_poll_interval_ms=300000,
    )

    try:
        await consumer.start()
        logger.info("Kafka consumer started.")

        async for msg in consumer:
            await process_stream(msg)

    except asyncio.CancelledError:
        logger.info("Streaming cancelled")
    except KeyboardInterrupt:
        logger.info("Streaming stopped")
    except Exception as e:
        logger.error(f"Error in consumer: {e}", exc_info=True)
    finally:
        await consumer.stop()
        logger.info("Kafka consumer stopped.")


if __name__ == "__main__":
    logger.info("Consumer was started")
    asyncio.run(start_streaming())
























# import asyncio
# import json
# from aiokafka import AIOKafkaConsumer
# import logging

# from services.book import insert_user_book

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)

# async def process_stream(msg):
#     try:
#         data = json.loads(msg.value().decode("utf-8"))
#         if data.get("event") == "user_created":
#             body = data.get("body").value().decode("utf-8")
#             created_id = body.get("id")
#             await insert_user_book(created_id)
    
    
#     except Exception as e:
#         pass

# async def start_streaming():
#     consumer = AIOKafkaConsumer(
#         'user-events',
#         bootstrap_servers='kafka:9092', '''                   
#         group_id="book-service-group"
#     )
    
#     await consumer.start()
#     logger.info("Kafka consumer started.")

#     try:
#         async for msg in consumer:
#             await process_stream(msg)

#     except asyncio.CancelledError:
#         logger.info("Streaming cancelled")
#     except KeyboardInterrupt:
#         logger.info("Streaming stopped")
#     finally:
#         await consumer.stop()
#         logger.info("Kafka consumer stopped.")

# # Запуск стриминга
# if __name__ == "__main__":
#     logger.info("Consumer was started")
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(start_streaming())
