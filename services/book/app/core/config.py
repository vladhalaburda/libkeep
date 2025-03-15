from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://172.27.132.179:27017")
DB_NAME = "libkeep"

client = AsyncIOMotorClient(MONGO_URL)
database = client[DB_NAME]

books_collection = database["books"]
user_books_collection = database['user_books']