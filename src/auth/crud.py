from datetime import datetime

from src.database import blacklisted_token_collection


async def add_blacklisted_token(data: dict):
    blacklisted_token = await blacklisted_token_collection.insert_one(data)
    new_blacklisted_token = await retrieve_blacklisted_token_by_id(blacklisted_token.inserted_id)
    return new_blacklisted_token


async def retrieve_blacklisted_token_by_id(blacklisted_token_id: str):
    return await blacklisted_token_collection.find_one({"_id": blacklisted_token_id})


async def retrieve_blacklisted_token(blacklisted_token: str):
    return await blacklisted_token_collection.find_one({"token": blacklisted_token})


async def cleanup_expired_tokens():
    result = await blacklisted_token_collection.delete_many({"expires_at": {"$lt": datetime.now()}})
    return result.deleted_count
