from bson import ObjectId
from core.config import books_collection, user_books_collection
from models.book import BookCreate, BookUpdate, BookInDB
from loguru import logger

async def create_book(book: BookCreate) -> BookInDB:
    book_data = book.dict()
    result = await books_collection.insert_one(book_data)
    return BookInDB(id=str(result.inserted_id), **book_data)

async def get_book(book_id: str) -> BookInDB:
    book = await books_collection.find_one({"_id": ObjectId(book_id)})
    if book:
        return BookInDB(id=str(book["_id"]), **book)
    return None

async def get_books():
    books = await books_collection.find().to_list(100)
    return [BookInDB(id=str(book["_id"]), **book) for book in books]

async def update_book(book_id: str, book_update: BookUpdate) -> bool:
    # КОСТЫЛЬ!!!!
    update_data = {k: v for k, v in book_update.dict().items() if v is not None}
    if not update_data:
        return False
    result = await books_collection.update_one({"_id": ObjectId(book_id)}, {"$set": update_data})
    return result.modified_count > 0

async def delete_book(book_id: str) -> bool:
    result = await books_collection.delete_one({"_id": ObjectId(book_id)})
    return result.deleted_count > 0


async def insert_user_book(user_id: str):
    logger.info("Was init book list for user")
    result = await user_books_collection.insert_one({"user_id": user_id, "books": []})
    return result.inserted_id

async def delete_user_book(user_id: str) -> bool:
    result = await user_books_collection.delete_many({"user_id": user_id})
    return result.deleted_count > 0