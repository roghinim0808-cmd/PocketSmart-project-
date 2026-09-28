from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    app_name: str = "PocketSmart AI"
    secret_key: str = "dev-secret-change-me"
    database_url: str = "sqlite:///./data/pocketsmart.db"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.8-flash"
    access_token_expire_minutes: int = 120
    upload_dir: str = "uploads"
    max_upload_mb: int = 5
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
