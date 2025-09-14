from __future__ import annotations

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl
from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = "development"
    secret_key: str
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7

    database_url: str
    redis_url: str

    openai_api_key: str | None = None
    embeddings_provider: str = "openai"

    sentry_dsn: str | None = None
    otel_exporter_otlp_endpoint: str | None = None

    cors_origins: List[AnyHttpUrl] = []


@lru_cache()
def get_settings() -> Settings:
    return Settings()  # type: ignore[arg-type]


settings = get_settings()

