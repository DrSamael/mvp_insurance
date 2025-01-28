from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.exceptions import INVALID_LOGIN_DATA_EXCEPTION, CREDENTIALS_INVALID_EXCEPTION
from src.users.schemas import UserTokens, UserOut
from src.users.crud import retrieve_user_by_email
from .utils import verify_password, create_token, add_blacklist_token
from .deps import get_current_user, validate_refresh_token, get_user_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post('/login', response_model=UserTokens)
async def login(data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await retrieve_user_by_email(data.username)
    if user is None:
        raise INVALID_LOGIN_DATA_EXCEPTION

    hashed_pass = user['password']
    if not await verify_password(data.password, hashed_pass):
        raise INVALID_LOGIN_DATA_EXCEPTION

    return {
        "access_token": await create_token(user['_id'], None, "access_token"),
        "refresh_token": await create_token(user['_id'], None, "refresh_token")
    }


@router.get("/refresh-token", response_model=UserTokens)
async def refresh_access_token(current_user: UserOut = Depends(validate_refresh_token),
                               token: str = Depends(get_user_token)):
    await add_blacklist_token(token, current_user["_id"])

    return {
        "access_token": await create_token(current_user['_id'], None, 'access_token'),
        "refresh_token": await create_token(current_user['_id'], None, 'refresh_token')
    }


@router.get('/me', summary="Get details of currently logged in user", response_model=UserOut)
async def get_me(current_user: UserOut = Depends(get_current_user)):
    return current_user


@router.get("/logout")
async def logout(current_user: UserOut = Depends(validate_refresh_token), token: str = Depends(get_user_token)):
    try:
        await add_blacklist_token(token, current_user["_id"])
        return {"detail": "Successfully logged out"}
    except:
        raise CREDENTIALS_INVALID_EXCEPTION

