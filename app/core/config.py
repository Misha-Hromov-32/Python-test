from functools import lru_cache
from pathlib import Path

from pydantic import Field

try:
    from pydantic_settings import BaseSettings, SettingsConfigDict

    _USE_V2 = True
except ImportError:
    from pydantic import BaseSettings

    SettingsConfigDict = None
    _USE_V2 = False


class Settings(BaseSettings):
    app_name: str = "FastAPI"
    description: str = "FastAPI на порту 8165"
    upload_dir: Path = Path("uploads")
    posters_dir: Path = Path("static/posters")
    descriptions_dir: Path = Path("uploads/descriptions")
    static_dir: Path = Path("static")
    database_path: Path = Path("users.db")
    jwt_secret: str = Field("change-me-in-production", env="JWT_SECRET")
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 2

    if _USE_V2:
        model_config = SettingsConfigDict(
            env_file=".env",
            env_file_encoding="utf-8",
        )
    else:
        class Config:
            env_file = ".env"
            env_file_encoding = "utf-8"


def ensure_directories(settings: "Settings") -> None:
    settings.static_dir.mkdir(exist_ok=True, parents=True)
    settings.upload_dir.mkdir(exist_ok=True, parents=True)
    settings.posters_dir.mkdir(exist_ok=True, parents=True)
    settings.descriptions_dir.mkdir(exist_ok=True, parents=True)


@lru_cache
def get_settings() -> Settings:
    return Settings()

