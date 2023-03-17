from fastapi import Depends, FastAPI

#db create is done in run_once.py
#from app.db import User, create_db_and_tables
from app.db import User
from app.schemas import UserCreate, UserRead, UserUpdate
from app.users import auth_backend, current_active_user, fastapi_users, current_superuser

app = FastAPI()

#CORS
from fastapi.middleware.cors import CORSMiddleware
""" origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8000",
] """
#allow all origins for testing
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=[60*60]
)


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
from fastapi.responses import Response
from app import oyf_crud, schemas, db
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings
from uuid import uuid4
from datetime import datetime
from PIL import Image
import pathlib
import aiofiles
from io import BytesIO
import base64

photo_responses = {200: {"content": {"image/jpg": {}}}}

@app.get("/photos/", response_model=list[schemas.Photo], dependencies=[Depends(current_active_user)], tags=[settings.app_name])
async def read_photos(
        skip: int = 0, limit: int = 100, 
        db: AsyncSession = Depends(db.get_async_session)
    ):
    photos = await oyf_crud.get_photos(db, skip=skip, limit=limit)
    #print(categories)
    return photos

#@app.get("/photos/{id}", response_model=schemas.Photo, dependencies=[Depends(current_active_user)], tags=[settings.app_name])
@app.get("/photos/{id}", dependencies=[Depends(current_active_user)], tags=[settings.app_name])
async def read_photo(
        #id: UUID, 
        id: str,
        db: AsyncSession = Depends(db.get_async_session)
    ):
    photo = await oyf_crud.get_photo(db, photo_id=id)
    #print(category)
    if photo is None:
        raise HTTPException(status_code=404, detail="Photo not found")

    #TODO: better think this thoroughly, make sure we are not implementing caping holes into filesystem security
    #filen = "mid_" + id + ".jpg"
    filepath = settings.img_path
    filen = f"{filepath}mid_{id}.jpg"
    with open(filen, 'rb') as in_file:
        content = in_file.read()
    
    #TODO: deal with async stuff later
    #async with aiofiles.open(filen, 'r') as in_file:
    #    content = await in_file.read()  # async read
        #await out_file.write(content)  # async write
        #content = in_file.read(1024*1024)  # async read chunk #TODO: does chunk size matter? yes, but how much?
    #print(content)
    img = {"image": base64.b64encode(content).decode('utf-8')}
    #print(img)
    return img
    #return Response(content=filtered_image.getvalue(), media_type="image/jpeg")

""" @app.post("/photos/", response_model=schemas.Photo, dependencies=[Depends(current_superuser)], tags=[settings.app_name])
async def create_photo(
        photo: schemas.PhotoCreate, 
        db: AsyncSession = Depends(db.get_async_session)
    ):
    photo = await oyf_crud.create_photo(db=db, photo=photo)
    
    return photo """

@app.post("/upload/", response_model=schemas.Photo, dependencies=[Depends(current_superuser)], tags=[settings.app_name])
#@app.post("/upload/", responses=photo_responses, response_class=Response, dependencies=[Depends(current_superuser)], tags=[settings.app_name])
async def create_photo(
        upfile: UploadFile,
        #photo: schemas.PhotoCreate, 
        db: AsyncSession = Depends(db.get_async_session),
        
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
    
    #photo.filetype = upfile.content_type #original type #TODO: for what??
    #photo.filesize = os.stat(out_file.name).st_size #out_file.tell() #original filesize #TODO: for what?? really worth importing os just for this
    #photo.image_width = original_image.width
    #photo.image_height = original_image.height
    photo.image_time = exifdata.get('DateTimeOriginal', datetime.now()) #original timestamp if found
    photo.created = datetime.now() #photo uploaded timestamp
    
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

    #TODO: explain this after figuring out and remember to comment code when written...
    #why not PILLOW .tobytes()
    #https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.tobytes
    filtered_image = BytesIO()
    original_image.save(filtered_image, "JPEG")
    filtered_image.seek(0)

    #insert thumbnail into db as BLOB
    photo.thumbnail = base64.b64encode(filtered_image.getvalue()).decode('utf-8')

    photo = await oyf_crud.create_photo(db=db, photo=photo)

    #original_image.close()

    #return Response(content=filtered_image.getvalue(), media_type="image/jpeg")

    #return StreamingResponse(filtered_image, media_type="image/jpeg")

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