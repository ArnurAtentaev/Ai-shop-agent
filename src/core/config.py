import os
from dotenv import load_dotenv

from pydantic_settings import BaseSettings
from pydantic import EmailStr

load_dotenv(".env")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_DB = os.getenv("PG_DB")
PG_PORT_SERVICE = os.getenv("PG_PORT_SERVICE")
email_support = os.getenv("SUPPORT_EMAIL")
phone_support = os.getenv("SUPPORT_PHONE")


class DataBaseSettings(BaseSettings):
    db_url: str = (
        f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@postgres_db:{PG_PORT_SERVICE}/shop"
    )
    db_echo: bool = False


class SupportSettings(BaseSettings):
    SUPPORT_EMAIL: EmailStr = email_support
    SUPPORT_PHONE: str = phone_support


db_settings = DataBaseSettings()
support_settings = SupportSettings()
