from fastapi import FastAPI, HTTPException
from aiokafka import AIOKafkaProducer
from motor.motor_asyncio import AsyncIOMotorClient
from loguru import logger
import json, os

from pydantic import EmailStr

from services.user import create_user, UserCreate
from services.user import get_user_by_email

app = FastAPI()

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
MONGO_URI = "mongodb://172.27.132.179:27017/"
DATABASE_NAME = "user_db"

# Создаем Kafka-продюсера
producer: AIOKafkaProducer | None = None
client: AsyncIOMotorClient = None
db = None

@app.on_event("startup")
async def startup():
    # Подключение к Kafka
    global producer
    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )
    await producer.start()
    logger.info("Kafka producer started")

    # Подключение к MongoDB
    global client, db
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DATABASE_NAME]
    logger.info("MongoDB connected")


@app.on_event("shutdown")
async def shutdown():
    await producer.stop()

@app.post("/users/")
async def create_user_endpoint(user: UserCreate):
    print("\n\n")
    logger.info("Request to create user")
    print(client)
    try:
        created_user = await create_user(user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка создания пользователя: {str(e)}")

    if not created_user:
        raise HTTPException(status_code=500, detail="Не удалось создать пользователя")
    
    event = {
        "event": "user_created",
        "body": {"id": created_user.id, "email": created_user.email, "username": created_user.username}
    }
    await producer.send("user-events", value=event)
    return {"id": created_user.id}


@app.get("/users/get_by_email/")
async def by_email_endpoint(email: EmailStr):
    try:
        user = await get_user_by_email(email)
    except:
         raise HTTPException(status_code=500, detail="Не удалось найти пользоватлеля")
    
    event = {
        "event": "search_user_by_email",
        "body": {"email": str(email)}
    }
    await producer.send("user-events", value=event)
    return {"user": user}