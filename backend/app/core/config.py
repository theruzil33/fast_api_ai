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

    # JWT
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # Initial user created on startup (leave empty to skip)
    INITIAL_USER_USERNAME: str = ""
    INITIAL_USER_PASSWORD: str = ""


settings = Settings()
