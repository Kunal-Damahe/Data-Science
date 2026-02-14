"""Application configuration and environment settings."""

from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Centralized application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Multi-Modal Compliance QA Pipeline"
    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    # --- API keys and observability ---
    google_api_key: str = Field(default="", alias="GOOGLE_API_KEY")
    langsmith_api_key: str = Field(default="", alias="LANGSMITH_API_KEY")
    langsmith_tracing: bool = Field(default=True, alias="LANGSMITH_TRACING")
    langsmith_project: str = Field(default="compliance-qa", alias="LANGSMITH_PROJECT")

    # --- Model and embedding config ---
    gemini_chat_model: str = "gemini-1.5-pro"
    gemini_embedding_model: str = "models/embedding-001"
    whisper_model_size: str = "base"

    # --- Processing params ---
    frame_extract_every_n_seconds: int = 3
    max_frames_for_ocr: int = 30

    # --- Storage paths ---
    data_dir: Path = Path("data")
    upload_dir: Path = Path("data/uploads")
    audio_dir: Path = Path("data/audio")
    frame_dir: Path = Path("data/frames")
    vector_store_dir: Path = Path("data/vector_store")
    compliance_rules_path: Path = Path("data/compliance_rules.txt")

    # --- Optional dependencies ---
    redis_url: Optional[str] = None
    database_url: Optional[str] = None


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached settings object."""

    settings = Settings()
    for directory in [
        settings.data_dir,
        settings.upload_dir,
        settings.audio_dir,
        settings.frame_dir,
        settings.vector_store_dir,
    ]:
        directory.mkdir(parents=True, exist_ok=True)
    return settings
