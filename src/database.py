from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_URI = os.getenv("DATABASE_URI", "mongodb://mongo:27017")

client = AsyncIOMotorClient(DATABASE_URI)
db = client[DATABASE_NAME]
