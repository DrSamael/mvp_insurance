from fastapi import APIRouter, Depends
from typing import List

from src.exceptions import INVALID_LOGIN_DATA_EXCEPTION
from src.auth.deps import admin_role_required, check_user_presence
from .schemas import UserOut, UserUpdate
from .crud import retrieve_users, update_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[UserOut])
async def list_users():
    return await retrieve_users()


@router.get("/{user_id}", response_model=UserOut)
async def show_user(user: UserOut = Depends(check_user_presence)):
    return user


@router.patch("/{user_id}", response_model=UserOut,
              dependencies=[Depends(admin_role_required), Depends(check_user_presence)])
async def edit_user(user_id: str, data: UserUpdate):
    updated_user = await update_user(user_id, data.model_dump(exclude_unset=True))
    if updated_user is None:
        raise INVALID_LOGIN_DATA_EXCEPTION
    return updated_user
