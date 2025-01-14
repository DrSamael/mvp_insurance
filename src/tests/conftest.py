import os
import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient


def pytest_configure():
    os.environ['ENVIRONMENT'] = 'test'
    os.environ['DATABASE_NAME'] = 'mvp_insurance_db_test'


@pytest_asyncio.fixture(autouse=True)
async def cleanup_test_database():
    yield

    if os.getenv('ENVIRONMENT') == "test":
        mongo_uri = os.getenv("DATABASE_URI", "mongodb://localhost:27017")
        client = AsyncIOMotorClient(mongo_uri)
        test_db_name = os.getenv('DATABASE_NAME')

        await client.drop_database(test_db_name)
