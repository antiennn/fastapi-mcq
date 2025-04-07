import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DB_USERNAME: str = os.getenv("DB_USERNAME", "")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_HOST: str = os.getenv("DB_HOST", "")
    DB_NAME: str = os.getenv("DB_NAME", "")
    DB_PORT: str = os.getenv("DB_PORT", "")

    ADMIN_USERNAME_BACKEND: str = os.getenv("ADMIN_USERNAME_BACKEND", "")
    ADMIN_PASSWORD_BACKEND: str = os.getenv("ADMIN_PASSWORD_BACKEND", "")
    ADMIN_SECRET_KEY: str = os.getenv("ADMIN_SECRET_KEY", "")

    class Config:
        env_file: str = "/.env"


settings = Settings()
