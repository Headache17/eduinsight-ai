"""EduInsight AI — Configuration"""
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "dev-secret-key-never-use-in-production-32chars"
    DATABASE_URL: str = "postgresql+asyncpg://eduinsight:devpassword123@localhost:5432/eduinsight"
    REDIS_URL: str = "redis://:devredis123@localhost:6379/0"
    JWT_ALGORITHM : str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    BCRYPT_ROUNDS: int = 10
    LOGIN_MAX_ATTEMPTS: int = 5
    LOGIN_LOCKOUT_MINUTES: int = 30
    OTP_EXPIRY_MINUTES: int = 10
    OTP_MAX_ATTEMPTS: int = 3
    MFA_TOKEN_EXPIRE_MINUTES: int = 5
    AWS_REGION: str = "ap-south-1"
    AWS_S3_BUCKET: str = "eduinsight-dev-uploads"
    ENABLE_AI_INSIGHTS: bool = True

settings = Settings()
