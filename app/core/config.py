from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    APP_NAME: str = "FastAPI AI"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    POSTGRES_USER: str = "user"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "dbname"

    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/dbname"


settings = Settings()
