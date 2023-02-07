"""
* Own Your Files - Photos 07.02.2023
* run_once.py
* Create necessary things, admin user etc.
* MIT License
* Copyright (c) 2023 SJR-Codes / Samu Reinikainen / samu.reinikainen@gmail.com
"""

import contextlib

from app.db import get_async_session, get_user_db
from app.schemas import UserCreate
from app.users import get_user_manager
from fastapi_users.exceptions import UserAlreadyExists

get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(email: str, password: str, is_superuser: bool = False):
    try:
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    user = await user_manager.create(
                        UserCreate(
                            email=email, password=password, is_superuser=is_superuser
                        )
                    )
                    print(f"User created {user}")
    except UserAlreadyExists:
        print(f"User {email} already exists")
    except ValidationError:
        print(f"{email} is not valid email")


import asyncio

if __name__ == "__main__":
    user_name = input("Enter email for admin user: ")
    passwd1 = input("Enter password for admin user: ")
    passwd2 = input("Enter password again for admin user: ")

    if len(user_name) > 6 and passwd1 == passwd2:
        asyncio.run(create_user(user_name, passwd1, True))
    else:
        print('Please, try again. Relax!')