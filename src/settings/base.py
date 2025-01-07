from enum import Enum

from pydantic_settings import BaseSettings


class AppEnvTypes(Enum):
    dev: str = 'dev'
    test: str = 'test'
    qa: str = 'qa'
    staging: str = 'staging'
    production: str = 'production'


class BaseAppSettings(BaseSettings):
    environment: AppEnvTypes = AppEnvTypes.dev
