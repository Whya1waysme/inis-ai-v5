from __future__ import annotations

import os
from typing import List, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: Optional[str] = None
    higgsfield_api_key: Optional[str] = None
    higgsfield_api_url: Optional[str] = None
    cors_origins: List[str] = []
    log_level: str = "INFO"
    openai_model: str = "gpt-4o-mini"
    environment: str = "development"

    model_config = SettingsConfigDict(
        case_sensitive=False,
    )


def _parse_cors_from_env(default: List[str] | None = None) -> List[str]:
    cors_env = os.getenv("CORS_ORIGINS")
    if not cors_env:
        return default or []
    return [o.strip() for o in cors_env.split(",") if o.strip()]


def load_settings() -> Settings:
    settings = Settings()
    # Allow comma-separated CORS in env
    if not settings.cors_origins:
        settings.cors_origins = _parse_cors_from_env(settings.cors_origins)
    return settings


settings = load_settings()
