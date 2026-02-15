import os
from dotenv import load_dotenv

from pydantic_settings import BaseSettings
from pydantic import EmailStr

load_dotenv(".env")
DATABASE_CONNECTION = os.getenv("DATABASE_CONNECTION")
email_support = os.getenv("SUPPORT_EMAIL")
phone_support = os.getenv("SUPPORT_PHONE")


class DataBaseSettings(BaseSettings):
    db_url: str = DATABASE_CONNECTION
    db_echo: bool = False


class SupportSettings(BaseSettings):
    SUPPORT_EMAIL: EmailStr = email_support
    SUPPORT_PHONE: str = phone_support


db_settings = DataBaseSettings()
support_settings = SupportSettings()
