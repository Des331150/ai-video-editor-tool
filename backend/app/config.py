from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/ai_video_editor"
    storage_path: str = str(Path(__file__).resolve().parent.parent / "storage")

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


settings = Settings()
