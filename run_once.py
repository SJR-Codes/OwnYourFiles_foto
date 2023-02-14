"""
* Own Your Files - Photos 07.02.2023
* run_once.py
* Create necessary things, admin user etc.
* MIT License
* Copyright (c) 2023 SJR-Codes / Samu Reinikainen / samu.reinikainen@gmail.com
"""

if __name__ == "__main__":
    user_name = input("Enter email for admin user: ")
    passwd1 = input("Enter password for admin user: ")
    passwd2 = input("Enter password again for admin user: ")

    #for quick testing
    """     user_name = "asd@asd.fo"
        passwd1 = "asd"
        passwd2 = "asd"
    """
    if len(user_name) < 6 and passwd1 != passwd2:
        print('Oh, please. Try again. Relax!')
        exit()

    #create secret to encode reset password & verification token.
    import secrets
    secret = secrets.token_hex(64)

    #create .env file
    with open(".env", "w") as f:
        f.write('APP_NAME="Own Your Files - Photos"\n')
        f.write('APP_VERSION="0.0.1"\n')
        f.write(f'ADMIN_EMAIL="{user_name}"\n')
        f.write('DATABASE_URL="sqlite+aiosqlite:///./test.db"\n')
        f.write(f'SECRET="{secret}"\n')

    import contextlib
    #TODO: think. Does this really need to be asynchronous, like really.
    import asyncio

    from app.db import create_db_and_tables
    async def create_db():
        await create_db_and_tables()

    from app.db import get_async_session, get_user_db, engine
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
        #except ValidationError:
        #    print(f"{email} is not valid email")

    #create db and table
    asyncio.run(create_db())
    print("DB & tables created")
    asyncio.run(create_user(user_name, passwd1, True))
    print("Admin user created")


