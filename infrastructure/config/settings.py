from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_DSN: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/cryptonite"
    )
    NEO4J_DSN: str = Field(default="neo4j://neo4j:password@localhost:7687")
    REDIS_URL: str = Field(default="redis://localhost:6379/0")
    CELERY_BROKER: str = Field(default="redis://localhost:6379/1")
    CELERY_BACKEND: str = Field(default="redis://localhost:6379/2")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
