import os

class Settings:
    MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://172.27.132.179:27017")
    DB_NAME = os.getenv("DB_NAME", "libkeep")

settings = Settings()