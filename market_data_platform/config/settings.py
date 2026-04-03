from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    app_env: str = 'dev'
    log_level: str = 'INFO'
    database_url: str = 'sqlite:///./market_data.db'
    raw_data_path: Path = Path('./data/raw')
    staging_data_path: Path = Path('./data/staging')
    curated_data_path: Path = Path('./data/curated')
    export_data_path: Path = Path('./data/exports')
    sources_config_path: Path = Path('./config/sources.yaml')
    api_host: str = '0.0.0.0'
    api_port: int = 8000


@lru_cache
def get_settings() -> Settings:
    return Settings()
