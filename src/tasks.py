from fastapi_utils.tasks import repeat_every
from src.auth.crud import cleanup_expired_tokens


def register_tasks(app):
    @app.on_event("startup")
    @repeat_every(seconds=86400)
    async def scheduled_cleanup():
        deleted_count = await cleanup_expired_tokens()
        print(f"Blacklisted tokens cleanup task completed. Deleted {deleted_count} expired tokens.")
