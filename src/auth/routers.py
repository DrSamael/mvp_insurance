from typing import Annotated, Union, Any

from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm

from src.exceptions import INVALID_LOGIN_DATA_EXCEPTION, USER_NOT_FOUND_EXCEPTION
from src.users.schemas import UserTokens, UserOut
from src.users.crud import retrieve_user_by_email, retrieve_user
from .utils import verify_password, create_token
from .deps import get_current_user, validate_token

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
async def refresh_access_token(request: Request):
    refresh_token = request.headers.get('refresh-token')
    token_data = await validate_token(refresh_token, 'refresh_token')
    user: Union[dict[str, Any], None] = await retrieve_user(token_data['sub'])

    if user is None:
        raise USER_NOT_FOUND_EXCEPTION

    return {
        "access_token": await create_token(user['_id'], None, 'access_token'),
        "refresh_token": await create_token(user['_id'], None, 'refresh_token')
    }


@router.get('/me', summary="Get details of currently logged in user", response_model=UserOut)
async def get_me(current_user: UserOut = Depends(get_current_user)):
    return current_user
