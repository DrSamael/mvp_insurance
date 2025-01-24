from fastapi import APIRouter
from typing import List

from src.exceptions import USER_NOT_FOUND_EXCEPTION
from .schemas import UserOut
from .crud import retrieve_users, retrieve_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[UserOut])
async def list_users():
    return await retrieve_users()


@router.get("/{user_id}", response_model=UserOut)
async def show_user(user_id: str):
    user = await retrieve_user(user_id)
    if user is None:
        raise USER_NOT_FOUND_EXCEPTION
    return user
