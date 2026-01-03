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
    
    # Redis
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_USERNAME: str
    REDIS_PASSWORD: str
    REDIS_DB: int
    
    # Logging
    LOG_LEVEL: str  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

