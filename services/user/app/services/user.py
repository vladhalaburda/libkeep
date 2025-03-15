import bcrypt
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient
from models.user import UserCreate, UserInDB, UserOut
from core.config import settings
from pydantic import EmailStr
from loguru import logger

client = AsyncIOMotorClient(settings.MONGODB_URL)
logger.info("Mongo client")
print(client)

db = client[settings.DB_NAME]
users_collection = db.users


async def get_user_by_email(email: EmailStr) -> Optional[UserInDB]:
    user_data = await users_collection.find_one({"email": email})
    if user_data:
        return UserInDB(**user_data)


async def create_user(user: UserCreate) -> UserOut:
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())


    user_in_db = UserInDB(
        email = user.email,
        username = user.username,
        hashed_password = hashed_password.decode("utf-8")
    )
    result = await users_collection.insert_one(user_in_db.model_dump())


    return UserOut(
        id = str(result.inserted_id),
        email = user_in_db.email,
        username = user_in_db.username
    )


async def authenticate_user(email: EmailStr, password: str) -> Optional[UserInDB]:
    user = await get_user_by_email(email)
    if user and bcrypt.checkpw(password.encode("utf-8"), user.hashed_password.encode("utf-8")):
        return user
    return None


async def update_user(email: EmailStr, updated_data: dict) -> Optional[UserOut]:
    result = await users_collection.update_one({"email": email}, {"$set": updated_data})
    if result.modified_count > 0:
        user = await get_user_by_email(email)
        return UserOut(
            id=str(user.id),
            email=user.email,
            username=user.username
        )
    return None

async def delete_user(email: EmailStr) -> bool:
    result = await users_collection.delete_one({"email": email})
    return result.deleted_count > 0