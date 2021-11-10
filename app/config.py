from typing import Set
from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_HOSTNAME: str
    DATABASE_PORT: str
    DATABASE_NAME: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    SECRET_KEY: str
    HASHING_ALGO: str
    JWT_TOKEN_EXPIRY_MINS: int

    class Config:
        env_file = ".env"

settings = Settings()