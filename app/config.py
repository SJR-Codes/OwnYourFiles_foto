"""
* Own Your Files - Photos 07.02.2023
* config.py
* Config/settings file
* MIT License
* Copyright (c) 2023 SJR-Codes / Samu Reinikainen / samu.reinikainen@gmail.com
"""
from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "Default generic API"
    app_version: str = "0.0.0"
    admin_email: str = "admin@example.com"
    database_url: str
    secret: str = "Just something to be overidden"

    #override above variables from .env-file. See .env_example
    class Config:
        env_file = ".env"

#cache the function so we don't read .env-file from filesystem on every call
@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()