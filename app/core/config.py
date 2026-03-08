from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    APP_NAME: str = "FastAPI AI"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False


settings = Settings()
