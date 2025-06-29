# app/core/config.py
from pydantic_settings import BaseSettings  # <== yangilangan import

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    CHANNEL: str = "fmb920_data"

    class Config:
        env_file = ".env"

settings = Settings()
