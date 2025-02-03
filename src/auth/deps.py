from typing import Union, Any

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from src.exceptions import (CREDENTIALS_INVALID_EXCEPTION, TOKEN_BLACKLISTED_EXCEPTION, ROLE_PERMISSION_EXCEPTION,
                            USER_NOT_FOUND_EXCEPTION)
from src.users.crud import retrieve_user
from src.users.schemas import UserOut
from src.users.enums import UserRoles
from .utils import validate_token, check_blacklist_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    token_data = await validate_token(token, 'access_token')
    user: Union[dict[str, Any], None] = await retrieve_user(token_data['sub'])

    if user is None:
        raise CREDENTIALS_INVALID_EXCEPTION
    return user


async def validate_refresh_token(refresh_token: str = Depends(oauth2_scheme)):
    token_data = await validate_token(refresh_token, 'refresh_token')
    if await check_blacklist_token(refresh_token):
        raise TOKEN_BLACKLISTED_EXCEPTION

    user: Union[dict[str, Any], None] = await retrieve_user(token_data["sub"])

    if user is None:
        raise CREDENTIALS_INVALID_EXCEPTION
    return user


async def get_user_token(token: str = Depends(oauth2_scheme)):
    return token


async def admin_role_required(current_user: UserOut = Depends(get_current_user)):
    if current_user['role'] not in [UserRoles.super_admin, UserRoles.insurance_company_admin,
                                    UserRoles.insurance_agent]:
        raise ROLE_PERMISSION_EXCEPTION
    return current_user


async def check_user_presence(user_id: str):
    user = await retrieve_user(user_id)
    if not user:
        raise USER_NOT_FOUND_EXCEPTION
    return user
