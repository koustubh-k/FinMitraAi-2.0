from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "FinMitra"
    environment: str = "development"
    
    database_url: str = "postgresql+psycopg://finmitra:finmitra@localhost:5432/finmitra"
    redis_url: str = "redis://localhost:6379/0"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
