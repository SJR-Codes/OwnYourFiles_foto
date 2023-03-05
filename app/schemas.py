import uuid

from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass

#OYF code from here on... dragons, perhaps...
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

#classes for images
class ImageBase(BaseModel):
    filename: str

class ImageCreate(ImageBase):
    pass

class Image(ImageBase):
    id: str
    filename: str

    class Config:
        orm_mode = True


#END OYF code