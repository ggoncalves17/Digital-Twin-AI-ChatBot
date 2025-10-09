from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="APP_")

    PROJECT_NAME: str = "digital-twin"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

settings = Settings()

