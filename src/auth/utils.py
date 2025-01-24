from typing import Union, Any, Literal
from datetime import datetime, timedelta, timezone

import jwt
import bcrypt

from src.settings import settings
from src.exceptions import TOKEN_EXPIRE_EXCEPTION, CREDENTIALS_INVALID_EXCEPTION

TokenType = Literal["access_token", "refresh_token"]


async def get_hashed_password(plain_password: str):
    hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')


async def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


async def create_token(user_id: Union[str, Any], expires_delta: int = None, token_type: TokenType = None):
    secret_key, expire_minutes = await define_token_params(token_type)
    if expires_delta is not None:
        expires_delta = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
    else:
        expires_delta = datetime.now(timezone.utc) + timedelta(minutes=float(expire_minutes))

    to_encode = {"exp": expires_delta, "sub": str(user_id)}
    encoded_jwt = jwt.encode(to_encode, secret_key, settings.algorithm)
    return encoded_jwt


async def define_token_params(token_type: TokenType = None):
    token_config = {
        'access_token': {
            'secret_key': settings.jwt_secret_key,
            'expire_minutes': settings.access_token_expire_minutes
        },
        'refresh_token': {
            'secret_key': settings.jwt_refresh_secret_key,
            'expire_minutes': settings.refresh_token_expire_minutes
        }
    }
    return token_config[token_type]['secret_key'], token_config[token_type]['expire_minutes']


async def decode_access_token(access_token):
    return jwt.decode(access_token, settings.jwt_secret_key, settings.algorithm)


async def decode_refresh_token(refresh_token):
    return jwt.decode(refresh_token, settings.jwt_refresh_secret_key, settings.algorithm)


async def validate_token(token: str, token_type: TokenType):
    try:
        decode_token_function = {
            'access_token': decode_access_token,
            'refresh_token': decode_refresh_token
        }
        return await decode_token_function[token_type](token)

    except jwt.exceptions.ExpiredSignatureError:
        raise TOKEN_EXPIRE_EXCEPTION
    except jwt.exceptions.InvalidTokenError:
        raise CREDENTIALS_INVALID_EXCEPTION
