import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class AppSettings(BaseSettings):
    database_name: str = os.getenv("DATABASE_NAME")
    database_uri: str = os.getenv("DATABASE_URI")

    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY")
    jwt_refresh_secret_key: str = os.getenv("JWT_REFRESH_SECRET_KEY")
    algorithm: str = os.getenv("ALGORITHM")
    access_token_expire_minutes: str = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_minutes: str = os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES")
    refresh_token_remember_expire_minutes: str = os.getenv("REFRESH_TOKEN_REMEMBER_EXPIRE_MINUTES")

    blacklisted_token_cleanup_interval: str = os.getenv("BLACKLISTED_TOKEN_CLEANUP_INTERVAL")
