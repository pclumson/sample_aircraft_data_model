from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings."""
    app_name: str = "Aircraft Component Data Model"
    debug: bool = False
    database_url: str = "sqlite:///aircraft_data.db"
    allowed_origins: List[str] = ["*"]

    class Config:
        env_file = ".env"


settings = Settings()
