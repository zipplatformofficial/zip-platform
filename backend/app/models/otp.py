"""OTP (One-Time Password) model for email and phone verification"""
import enum
from sqlalchemy import Column, String, Integer, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class OTPType(str, enum.Enum):
    """OTP types"""
    EMAIL_VERIFICATION = "email_verification"
    PHONE_VERIFICATION = "phone_verification"
    PASSWORD_RESET = "password_reset"
    TWO_FACTOR_AUTH = "two_factor_auth"


class OTP(BaseModel):
    """OTP model for verification codes"""

    __tablename__ = "otps"

    # User
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # OTP Details
    code = Column(String(6), nullable=False)  # 6-digit code
    type = Column(Enum(OTPType), nullable=False)

    # Verification target (email or phone)
    email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)

    # Status
    is_used = Column(Boolean, default=False, nullable=False)
    is_expired = Column(Boolean, default=False, nullable=False)

    # Expiry (stored as ISO datetime string)
    expires_at = Column(String(50), nullable=False)

    # Attempts tracking
    verification_attempts = Column(Integer, default=0, nullable=False)
    max_attempts = Column(Integer, default=3, nullable=False)

    # Relationships
    user = relationship("User")

    def __repr__(self):
        return f"<OTP {self.type} for user {self.user_id}>"
