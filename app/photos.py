"""
* Own Your Files - Photos 08.02.2023
* photos.py
* Photos handler module for Own Your Files core
* MIT License
* Copyright (c) 2023 SJR-Codes / Samu Reinikainen / samu.reinikainen@gmail.com
"""

from app.config import settings

from fastapi import Depends, FastAPI, File, Form, UploadFile
from pydantic import BaseModel
from app.db import User
from app.users import auth_backend, current_active_user, fastapi_users, current_superuser

app = FastAPI()

#allow file upload only to superusers

@app.post("/fileup/")
async def create_file(
    user: User = Depends(current_superuser),
    fileb: UploadFile = File(description="A file read as UploadFile"), 
    category = Form(), tags = Form(),
):
    return {
        "file_size": len(fileb),
        "category": category,
        "tags": tags,
        "fileb_content_type": fileb.content_type,
    }