from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeMeta, declarative_base, sessionmaker
from app.config import settings

DATABASE_URL = settings.database_url

Base: DeclarativeMeta = declarative_base()


class User(SQLAlchemyBaseUserTableUUID, Base):
    pass


engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

#TODO: move this to own "module"
# OYF code
from sqlalchemy import Column, ForeignKey, String, Integer, DateTime, CHAR, TEXT
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid as uuid_pkg
#from sqlalchemy.dialects.sqlite import BLOB

class OYF_Photo(Base):
    __tablename__ = "photo"
    #TODO: figure out sqlAchemys UUID type, since only sqlite supported for now this is fine
    id = Column(
        CHAR(36),
        default=uuid_pkg.uuid4,
        primary_key=True,
        index=True,
        nullable=False)
    filename = Column(String(100))
    #filetype = Column(String(5))
    #filesize = Column(Integer)
    #image_width = Column(Integer)
    #image_height = Column(Integer)
    image_time = Column(DateTime) 
    created = Column(DateTime, default=func.now())
    category_id = Column(Integer, ForeignKey("category.id"))
    category = relationship("OYF_Category") #, back_populates="")
    thumbnail = Column(TEXT)
    #thumbnail = Column(BLOB)
    #TODO: need for backpopulate categories here?

    def __repr__(self):
        #TODO: think representer for photo
        return f"Photo(id={self.id!r}, filename={self.filename!r})"

class OYF_Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)

    def __repr__(self):
        return f"Category(id={self.id!r}, title={self.title!r})"

# END OYF code

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
