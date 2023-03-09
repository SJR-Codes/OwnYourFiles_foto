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

#testing route, to be removed or renamed
@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}

#OYF routes
from fastapi import HTTPException, UploadFile
from app import oyf_crud, oyf_models, schemas, db
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings
from uuid import UUID, uuid4
from datetime import datetime
from PIL import Image
import pathlib
import aiofiles
import os

@app.get("/photos/{id}", response_model=schemas.Photo, dependencies=[Depends(current_active_user)], tags=[settings.app_name])
async def read_photo(
        #id: UUID, 
        id: str,
        db: AsyncSession = Depends(db.get_async_session)
    ):
    photo = await oyf_crud.get_photo(db, photo_id=id)
    #print(category)
    if photo is None:
        raise HTTPException(status_code=404, detail="Photo not found")
    return photo

@app.post("/photos/", response_model=schemas.Photo, dependencies=[Depends(current_superuser)], tags=[settings.app_name])
async def create_photo(
        photo: schemas.PhotoCreate, 
        db: AsyncSession = Depends(db.get_async_session)
    ):
    photo = await oyf_crud.create_photo(db=db, photo=photo)
    
    return photo

@app.post("/upload/", response_model=schemas.Photo, dependencies=[Depends(current_superuser)], tags=[settings.app_name])
async def create_photo(
        upfile: UploadFile,
        #photo: schemas.PhotoCreate, 
        db: AsyncSession = Depends(db.get_async_session)
    ):

    photo = schemas.Photo
    photo.id = str(uuid4())
    photo.filename = upfile.filename #original filename

    #TODO: groove this func
    #TODO: funcing async awaits, figure out blocking functions
    #TODO: might be "easiest" to spawn separate process for mangling image in background

    #save file into img_path using UUID as filename
    filepath = settings.img_path
    save_filename = f"{photo.id}.jpg"
    
    #save original file as is but with uuid filename
    #tmp = await upfile.read()
    #get the file extension
    file_extension = pathlib.Path(photo.filename).suffix
    orig_filename = f"{filepath}orig_{photo.id}{file_extension}"

    #remove blocking code
    #with open(orig_filename, "wb") as f:
    #    f.write(tmp)

    #handle file save asynchronously
    async with aiofiles.open(orig_filename, 'wb') as out_file:
        #content = await upfile.read()  # async read
        #await out_file.write(content)  # async write
        while content := await upfile.read(1024*1024):  # async read chunk #TODO: does chunk size matter? yes, but how much?
            await out_file.write(content)  # async write chunk
    #TODO: perhaps check shutil way...
    
    #TODO: these should be done in subprocess... if we are okay with not returning image right away...
    #user uploads image, gets "image uploaded", does she upload more or should processed image be returned straight away?
    #we have saved original into filesystem above so could just spawn mangle_image(orig_filename) into subprocess
    #pros: not blocking process with possibly huge file mangling
    #cons: user doesn't get processed image back right after upload -> redirect and hope subprocess has done it's magic
    
    original_image = Image.open(upfile.file)

    exifdata = original_image.getexif()
    
    photo.filetype = upfile.content_type #original type #TODO: for what??
    photo.filesize = os.stat(out_file.name).st_size #out_file.tell() #original filesize #TODO: for what?? really worth importing os just for this
    photo.image_width = original_image.width
    photo.image_height = original_image.height
    photo.image_time = exifdata.get('DateTimeOriginal', datetime.now()) #original timestamp if found
    photo.created = datetime.now() #photo uploaded timestamp

    photo = await oyf_crud.create_photo(db=db, photo=photo)
    
    #save full size, optimized, in jpg format
    original_image.save(f"{filepath}{save_filename}", 'jpeg', optimize=True)

    #TODO: list(dict(size,prefix)) -> loop function to create images
    #save midnail
    mid_size = (1080,1080)
    original_image.thumbnail(mid_size)
    original_image.save(f"{filepath}mid_{save_filename}", 'jpeg', optimize=True)

    #save thumbnail
    thmb_size = (161,161)
    original_image.thumbnail(thmb_size)
    original_image.save(f"{filepath}thmb_{save_filename}", 'jpeg', optimize=True)

    original_image.close()

    return photo

@app.post("/categories/", response_model=schemas.Category, dependencies=[Depends(current_superuser)], tags=[settings.app_name])
async def create_category(
        category: schemas.CategoryCreate, 
        db: AsyncSession = Depends(db.get_async_session)
    ):
    category = await oyf_crud.create_category(db=db, category=category)
    
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