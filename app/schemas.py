import uuid

from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass

#OYF code from here on... dragons, perhaps...
from datetime import datetime
from pydantic import BaseModel

#classes for categories
class CategoryBase(BaseModel):
    title: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        orm_mode = True

#classes for photos
class PhotoBase(BaseModel):
    filename: str

class PhotoCreate(PhotoBase):
    pass

class Photo(PhotoBase):
    id: str
    filetype: str
    filesize: int
    image_width: int
    image_height: int
    image_time: datetime
    created: datetime
    #category: Category

    class Config:
        orm_mode = True

#END OYF code