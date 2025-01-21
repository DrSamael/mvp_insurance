from typing import Union, Any

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from src.exceptions import CREDENTIALS_INVALID_EXCEPTION
from src.users.crud import retrieve_user
from .utils import validate_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    token_data = await validate_token(token, 'access_token')
    user: Union[dict[str, Any], None] = await retrieve_user(token_data['sub'])

    if user is None:
        raise CREDENTIALS_INVALID_EXCEPTION
    return user
