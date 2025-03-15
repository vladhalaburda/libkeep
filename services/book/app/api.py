from aiokafka import AIOKafkaProducer
from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from loguru import logger

import os, json

from services.book import get_books, create_book, get_book, update_book, delete_book
from models.book import BookInDB, BookCreate, BookUpdate

app = FastAPI()

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
MONGO_URI = "mongodb://172.27.132.179:27017/"
DATABASE_NAME = "user_db"

producer: AIOKafkaProducer | None = None
client: AsyncIOMotorClient = None
db = None

@app.on_event("startup")
async def startup():
    global producer
    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )
    await producer.start()
    logger.info("Kafka producer started")

    global client, db
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DATABASE_NAME]
    logger.info("MongoDB connected")

@app.on_event("shutdown")
async def shutdown():
    await producer.stop()


@app.post("/", response_model=BookInDB)
async def create_book_endpoint(book: BookCreate):
    try:
        created_book = await create_book(book)
    except Exception as e:
        raise HTTPException(500, "Is not available")

    event = {
        "event": "created_book",
        "body": {"book_id": created_book.id}
    }
    await producer.send("book-events", value=event)

    return created_book

@app.get("/{book_id}", response_model=BookInDB)
async def get_book_endpoint(book_id: str):
    book = await get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.get("/", response_model=list[BookInDB])
async def get_books_endpoint():
    return await get_books()

@app.put("/{book_id}", response_model=bool)
async def update_book_endpoint(book_id: str, book_update: BookUpdate):
    if await update_book(book_id, book_update):
        return True
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/{book_id}", response_model=bool)
async def delete_book_endpoint(book_id: str):
    if await delete_book(book_id):
        return True
    raise HTTPException(status_code=404, detail="Book not found")