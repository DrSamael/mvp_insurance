import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class AppSettings(BaseSettings):
    database_name: str = os.getenv("DATABASE_NAME")
    database_uri: str = os.getenv("DATABASE_URI")
