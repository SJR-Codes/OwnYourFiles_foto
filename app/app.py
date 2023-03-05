from fastapi import Depends, FastAPI

#db create is done in run_once.py
#from app.db import User, create_db_and_tables
from app.db import User
from app.schemas import UserCreate, UserRead, UserUpdate
from app.users import auth_backend, current_active_user, fastapi_users, current_superuser

app = FastAPI()

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}

#done in run_once.py
#@app.on_event("startup")
#async def on_startup():
    # Not needed if you setup a migration system like Alembic
#    await create_db_and_tables()

#TODO: routes
from fastapi import HTTPException
from app import oyf_crud, oyf_models, schemas, db
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings

@app.post("/categories/", response_model=schemas.Category, dependencies=[Depends(current_superuser)], tags=[settings.app_name])
async def create_category(
        category: schemas.CategoryCreate, 
        db: AsyncSession = Depends(db.get_async_session)
    ):
    category = await oyf_crud.create_category(db=db, category=category)
    #if db_user:
    #    raise HTTPException(status_code=400, detail="Email already registered")
    return category


@app.get("/categories/", response_model=list[schemas.Category], dependencies=[Depends(current_active_user)], tags=[settings.app_name])
async def read_categories(
        skip: int = 0, limit: int = 100, 
        db: AsyncSession = Depends(db.get_async_session)
    ):
    categories = await oyf_crud.get_categories(db, skip=skip, limit=limit)
    #print(categories)
    return categories


@app.get("/categories/{id}", response_model=schemas.Category, dependencies=[Depends(current_active_user)], tags=[settings.app_name])
async def read_category(
        id: int, 
        db: AsyncSession = Depends(db.get_async_session)
    ):
    category = await oyf_crud.get_category(db, category_id=id)
    #print(category)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category