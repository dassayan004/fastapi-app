import secrets
from typing import Any, List
from urllib.parse import urlparse
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # Use top level .env file (one level above ./backend/)
        env_file="./.env",
        env_ignore_empty=True,
        extra="ignore",
    )
    # App settings
    app_name: str = "FastAPI CORE"
    SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    # Database settings
    DATABASE_URL: str

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        tmpPostgres = urlparse(self.DATABASE_URL)
        return f"postgresql+asyncpg://{tmpPostgres.username}:{tmpPostgres.password}@{tmpPostgres.hostname}{tmpPostgres.path}"


appSetting = Settings()
