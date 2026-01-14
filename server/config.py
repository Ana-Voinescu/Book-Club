"""
Configuration settings for the Book Club API.
Loads environment variables from .env file.
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    # Database
    DATABASE_URL: str = "sqlite:///./bookclub.db"

    # Application
    APP_NAME: str = "Book Club API"
    DEBUG: bool = True

    # Security
    SECRET_KEY: str = "change-this-secret-key"
    SESSION_COOKIE_NAME: str = "bookclub_session"

    # CORS - origins that can access the API
    ALLOWED_ORIGINS: str = "http://localhost:5500,http://127.0.0.1:5500"

    # Server
    HOST: str = "127.0.0.1"
    PORT: int = 8000

    class Config:
        env_file = ".env"
        case_sensitive = False

    def get_allowed_origins(self) -> List[str]:
        """Convert comma-separated origins string to list."""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]


# Create a global settings instance
settings = Settings()
