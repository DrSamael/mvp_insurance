from .app import AppSettings


class DevAppSettings(AppSettings):
    debug: bool = True
    title: str = 'MVP Insurance application'
