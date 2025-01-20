from fastapi import APIRouter, HTTPException, status
from typing import List

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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
