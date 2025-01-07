from motor.motor_asyncio import AsyncIOMotorClient

from src.settings import settings

client = AsyncIOMotorClient(settings.database_uri)
db = client[settings.database_name]
