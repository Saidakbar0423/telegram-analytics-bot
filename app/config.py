import os
from pathlib import Path
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Telegram
    TELEGRAM_API_ID: int
    TELEGRAM_API_HASH: str
    BOT_TOKEN: str
    ADMIN_ID: int
    MONITORED_GROUPS: str = "@testgroup"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/telegram_analytics"
    DB_USER: str = "user"
    DB_PASSWORD: str = "password"
    DB_NAME: str = "telegram_analytics"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Parser
    PARSER_BATCH_SIZE: int = 100
    PARSER_INTERVAL_SECONDS: int = 300
    MAX_FLOOD_WAIT_SECONDS: int = 60
    PARSER_ENABLED: bool = True

    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_WORKERS: int = 4

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    LOG_FORMAT: str = "json"

    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True

    @property
    def monitored_groups_list(self) -> list[str]:
        """Convert comma-separated groups to list"""
        return [g.strip() for g in self.MONITORED_GROUPS.split(",")]

    @property
    def is_production(self) -> bool:
        """Check if running in production"""
        return self.ENVIRONMENT == "production"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# Create project directories
def create_directories():
    """Create necessary directories if they don't exist"""
    directories = ["logs", "data", "migrations"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)


# Initialize
settings = get_settings()
create_directories()