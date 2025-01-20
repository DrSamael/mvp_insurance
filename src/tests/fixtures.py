import pytest_asyncio
from bson import ObjectId
from faker import Faker
from httpx import AsyncClient, ASGITransport

from src.main import app
from src.database import db
from src.database import user_collection
from src.users.enums import UserRoles

fake = Faker()


@pytest_asyncio.fixture(scope='function', autouse=True)
async def clear_test_db():
    for collection_name in await db.list_collection_names():
        await db[collection_name].delete_many({})


@pytest_asyncio.fixture(scope='function')
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


def generate_user_data(role: UserRoles = UserRoles.super_admin) -> dict:
    return {
        "_id": ObjectId(),
        "email": fake.ascii_free_email(),
        "password": "123123",
        "first_name": fake.first_name_male(),
        "last_name": fake.last_name_male(),
        "role": role
    }


@pytest_asyncio.fixture(scope='function')
async def test_user():
    user_data = generate_user_data()
    await user_collection.insert_one(user_data)
    yield user_data


@pytest_asyncio.fixture(scope='function')
async def test_users_list():
    users_data = [generate_user_data() for _ in range(3)]
    await user_collection.insert_many(users_data)
    yield users_data
