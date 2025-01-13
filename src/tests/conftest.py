import os
import asyncio
import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient


def pytest_configure():
    os.environ['ENVIRONMENT'] = 'test'
    os.environ['DATABASE_NAME'] = 'mvp_insurance_db_test'


@pytest_asyncio.fixture(scope="session")
def event_loop():
    """Create an event loop for the session scope."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def cleanup_test_database():
    yield

    if os.getenv('ENVIRONMENT') == "test":
        mongo_uri = os.getenv("DATABASE_URI", "mongodb://localhost:27017")
        client = AsyncIOMotorClient(mongo_uri)
        test_db_name = os.getenv('DATABASE_NAME')

        await client.drop_database(test_db_name)
