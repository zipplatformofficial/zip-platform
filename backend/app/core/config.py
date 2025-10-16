"""Application configuration"""
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, validator


class Settings(BaseSettings):
    """Application settings"""

    # Application
    APP_NAME: str = "ZIP Automobile Service Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"

    # API
    API_V1_PREFIX: str = "/api/v1"

    # Database
    DATABASE_URL: PostgresDsn

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    ALLOWED_ORIGINS: List[str] = ["*"]

    @validator("ALLOWED_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v

    # File Upload
    MAX_FILE_SIZE: int = 5242880  # 5MB
    UPLOAD_DIR: str = "uploads"

    # Payment Gateway
    MTN_MOMO_API_KEY: Optional[str] = None
    VODAFONE_CASH_API_KEY: Optional[str] = None
    AIRTELTIGO_MONEY_API_KEY: Optional[str] = None

    # SMS
    SMS_API_KEY: Optional[str] = None
    SMS_SENDER_ID: str = "ZIP"

    # Email
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAIL_FROM: str = "noreply@zipghana.com"

    # Admin
    ADMIN_EMAIL: str = "admin@zipghana.com"
    ADMIN_DEFAULT_PASSWORD: str = "ChangeMe123!"

    # Geolocation
    GOOGLE_MAPS_API_KEY: Optional[str] = None

    # Commission Rates
    VENDOR_COMMISSION_RATE: float = 0.12
    TECHNICIAN_COMMISSION_RATE: float = 0.10

    # Verification
    GHANA_CARD_VERIFICATION_API: Optional[str] = None

    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()
