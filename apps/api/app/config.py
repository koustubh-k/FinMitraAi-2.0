from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "FinMitra 2.0"
    ENVIRONMENT: str = "development"
    API_V1_STR: str = "/api/v1"
    API_PORT: int = 8000
    HOST: str = "0.0.0.0"
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"

    # Database & Persistence (Host PG: 5433, Host Redis: 6380)
    DATABASE_URL: str = "postgresql+asyncpg://finmitra_user:finmitra_password@localhost:5433/finmitra_db"
    REDIS_URL: str = "redis://localhost:6380/0"

    # Future Providers (Placeholders)
    GROQ_API_KEY: str = ""
    OPENROUTER_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    ALPHAVANTAGE_API_KEY: str = ""
    FINNHUB_API_KEY: str = ""

    # Observability
    LANGCHAIN_TRACING_V2: bool = False
    LANGCHAIN_API_KEY: str = ""
    LANGCHAIN_PROJECT: str = "finmitra-2.0"

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin]

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
