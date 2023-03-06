"""
* Own Your Files - Photos 03.03.2023
* oyf_models.py
* description
* MIT License
* Copyright (c) 2023 SJR-Codes / Samu Reinikainen / samu.reinikainen@gmail.com
"""

from sqlalchemy.orm import DeclarativeMeta, declarative_base, sessionmaker
from app.config import settings

DATABASE_URL = settings.database_url

Base: DeclarativeMeta = declarative_base()

from sqlalchemy import Column, ForeignKey, String, Integer, DateTime, CHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import UUID
import uuid as uuid_pkg

class OYF_Photo(Base):
    __tablename__ = "photo"
    #TODO: figure out sqlAchemys UUID type, since only sqlite supported for now this is fine
    id = Column( #UUID(hex),
        String(36),
        #UUID,
        #TODO: re-invent some more beautiful hack in here
        default=str(uuid_pkg.uuid4),
        primary_key=True,
        index=True,
        nullable=False)
    filename = Column(String(100))
    filetype = Column(String(5))
    filesize = Column(Integer)
    image_width = Column(Integer)
    image_height = Column(Integer)
    image_time = Column(DateTime)
    created = Column(DateTime, default=func.now())
    category_id = Column(Integer, ForeignKey("category.id"))
    category = relationship("OYF_Category") #, back_populates="")
    #TODO: need for backpopulate categories here?

class OYF_Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)