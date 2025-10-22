from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="APP_", extra="ignore"
    )

    PROJECT_NAME: str = "digital-twin"
    DESCRIPTION: str = "A digital twin for professional communication use"
    VERSION: str = "0.1.0"
    LICENSE: dict[str, str] = {
        "name": "MIT License",
        "url": "http://opensource.org/licenses/MIT",
    }

    API_V1_STR: str = "/api/v1"

    DATABASE_URL: str = "sqlite:///:memory:"

    SECRET_KEY: str = ""
    ALGORITHM: str = ""
    GOOGLE_API_KEY: str = ""
    JWT_EXPIRE_MINUTES: int = 30

    OPENWEATHER_API_KEY: str = ""


settings = Settings()

