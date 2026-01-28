from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки приложения"""

    PROJECT_NAME: str
    VERSION: str
    API_PREFIX: str

    # Database
    DATABASE_URL: str

    # Security
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int

    # Admin credentials for auto-role assignment
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str

    # Redis (при REDIS_ENABLED=false токены хранятся в БД, подключение не создаётся)
    REDIS_ENABLED: bool = False
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_USERNAME: str = "default"
    REDIS_PASSWORD: str = ""
    REDIS_DB: int = 0

    # Logging
    LOG_LEVEL: str  # DEBUG, INFO, WARNING, ERROR, CRITICAL

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
