
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "FinMitra"
    environment: str = "development"
    log_level: str = "INFO"
    
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    database_url: str = "postgresql+psycopg://finmitra:finmitra@localhost:5432/finmitra"
    redis_url: str = "redis://localhost:6379/0"

    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30

    model_config = SettingsConfigDict(
        env_file=(".env", "../.env", "../../.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()
