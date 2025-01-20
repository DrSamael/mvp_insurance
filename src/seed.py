import asyncio
from datetime import datetime

from src.users.crud import retrieve_user_by_email, add_user
from src.users.enums import UserRoles

AdminUserData = {
    "email": "superadmin@user.com",
    "password": "123123",
    "first_name": "super-admin",
    "last_name": "super-admin",
    "role": UserRoles.super_admin,
    "created_at": datetime.now(),
    "updated_at": datetime.now()
}


async def create_admin_user():
    if await is_admin_user_present(): return

    await add_user(AdminUserData)
    print("Admin user created successfully")


async def is_admin_user_present():
    if await retrieve_user_by_email("superadmin@user.com"):
        print("Admin user already exists. No new user created")
        return True
    return False


if __name__ == "__main__":
    asyncio.run(create_admin_user())
