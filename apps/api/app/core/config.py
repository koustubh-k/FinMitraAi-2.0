
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
    
    market_data_provider: str = "yahoo,duckduckgo"
    
    alpha_vantage_api_key: str | None = None
    finnhub_api_key: str | None = None
    fmp_api_key: str | None = None
    tavily_api_key: str | None = None
    serper_api_key: str | None = None
    marketaux_api_key: str | None = None
    exa_api_key: str | None = None
    firecrawl_api_key: str | None = None
    linkup_api_key: str | None = None

    model_config = SettingsConfigDict(
        env_file=(".env", "../.env", "../../.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()
