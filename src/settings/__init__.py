from .base import BaseAppSettings
from .dev import DevAppSettings
from .qa import QaAppSettings
from .staging import StagingAppSettings
from .production import ProductionAppSettings
from .test import TestAppSettings


def get_settings():
    env = BaseAppSettings().environment

    if env.value == "qa":
        return QaAppSettings()
    elif env.value == 'staging':
        return StagingAppSettings()
    elif env.value == 'production':
        return ProductionAppSettings()
    elif env.value == 'test':
        return TestAppSettings()
    return DevAppSettings()


settings = get_settings()
