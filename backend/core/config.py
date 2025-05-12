from enum import Enum
from functools import lru_cache
from typing import Any, Optional

from pydantic import BaseSettings, Field, PostgresDsn, RedisDsn, validator


class EnvironmentType(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TEST = "test"


class BaseConfig(BaseSettings):
    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


class Config(BaseConfig):
    # Application
    LOG_LEVEL: str = Field(default="DEBUG", env="LOG_LEVEL")
    DEBUG: bool = Field(default=False, env="DEBUG")
    DEFAULT_LOCALE: str = Field(default="en_US", env="DEFAULT_LOCALE")
    ENVIRONMENT: EnvironmentType = Field(
        default=EnvironmentType.DEVELOPMENT, env="ENVIRONMENT"
    )
    RELEASE_VERSION: str = Field(default="0.1", env="RELEASE_VERSION")

    # Database
    DATABASE_URL: str =Field(default="postgresql://username:password@localhost:5432/db-local", env="DATABASE_URL")

    # Redis
    REDIS_URL: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")

    # Security
    API_KEY: str = Field(default="test-api-key", env="API_KEY")
    SECRET_KEY: str = Field(default="super-secret-key", env="SECRET_KEY")
    JWT_ALGORITHM: str = Field(default="HS256", env="JWT_ALGORITHM")
    JWT_EXPIRE_MINUTES: int = Field(default=60 * 24, env="JWT_EXPIRE_MINUTES")
    class Config(BaseConfig.Config):
        env_prefix = ""


@lru_cache()
def get_config() -> Config:
    """
    Get config instance with caching.
    Usage: config = get_config()
    """
    return Config()


# Create config instance
config: Config = get_config()
