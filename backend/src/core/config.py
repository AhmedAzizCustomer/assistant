"""Application configuration."""
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""

    # App Configuration
    app_name: str = "AI Personal Assistant"
    environment: str = "development"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    secret_key: str

    # AI API Keys
    anthropic_api_key: str
    openai_api_key: str
    default_ai_provider: str = "anthropic"
    claude_model: str = "claude-3-5-sonnet-20241022"
    openai_model: str = "gpt-4-turbo-preview"

    # Gmail Configuration
    gmail_client_id: Optional[str] = None
    gmail_client_secret: Optional[str] = None

    # Outlook Configuration
    outlook_client_id: Optional[str] = None
    outlook_client_secret: Optional[str] = None

    # Google Calendar Configuration
    google_calendar_client_id: Optional[str] = None
    google_calendar_client_secret: Optional[str] = None

    # Database
    database_url: str

    # CORS
    frontend_url: str = "http://localhost:3000"

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
