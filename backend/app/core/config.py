"""Application configuration"""
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, Field


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

    # CORS - stored as string
    ALLOWED_ORIGINS: str = "*"

    def get_cors_origins(self) -> List[str]:
        """Parse CORS origins from comma-separated string"""
        if "," in self.ALLOWED_ORIGINS:
            return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
        return [self.ALLOWED_ORIGINS]

    # File Upload
    MAX_FILE_SIZE: int = 5242880  # 5MB
    UPLOAD_DIR: str = "uploads"

    # Payment Gateway - Paystack
    PAYSTACK_SECRET_KEY: Optional[str] = None
    PAYSTACK_PUBLIC_KEY: Optional[str] = None
    PAYSTACK_WEBHOOK_SECRET: Optional[str] = None
    PAYSTACK_CALLBACK_URL: Optional[str] = None

    # SMS - Hubtel
    HUBTEL_CLIENT_ID: Optional[str] = None
    HUBTEL_CLIENT_SECRET: Optional[str] = None
    HUBTEL_API_KEY: Optional[str] = None
    HUBTEL_SENDER_ID: str = "ZIP"

    # Email
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAIL_FROM: str = "noreply@zipghana.com"

    # Firebase Cloud Messaging
    FIREBASE_SERVER_KEY: Optional[str] = None
    FIREBASE_CREDENTIALS_PATH: Optional[str] = None

    # AWS S3
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_S3_BUCKET_NAME: Optional[str] = None
    AWS_S3_REGION: str = "us-east-1"
    AWS_S3_CDN_URL: Optional[str] = None

    # Cloudinary
    CLOUDINARY_CLOUD_NAME: Optional[str] = None
    CLOUDINARY_API_KEY: Optional[str] = None
    CLOUDINARY_API_SECRET: Optional[str] = None
    CLOUDINARY_FOLDER: str = "zip-platform"  # Folder to organize uploads

    # Admin
    ADMIN_EMAIL: str = "admin@zipghana.com"
    ADMIN_DEFAULT_PASSWORD: str = "ChangeMe123!"

    # Geolocation
    GOOGLE_MAPS_API_KEY: Optional[str] = None

    # Commission Rates
    VENDOR_COMMISSION_RATE: float = 0.12
    TECHNICIAN_COMMISSION_RATE: float = 0.10

    # Verification - Smile ID
    SMILE_ID_PARTNER_ID: Optional[str] = None
    SMILE_ID_API_KEY: Optional[str] = None
    SMILE_ID_CALLBACK_URL: Optional[str] = None
    SMILE_ID_ENVIRONMENT: str = "sandbox"  # sandbox or production

    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    model_config = SettingsConfigDict(
        env_file = ".env",
        case_sensitive = True,
        extra = "ignore"
    )


# Create global settings instance
settings = Settings()
