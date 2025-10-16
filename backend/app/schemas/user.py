"""User schemas"""
from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, validator
from app.models.user import UserRole, UserType


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    phone: str
    full_name: str


class UserCreate(UserBase):
    """User registration schema"""
    password: str = Field(..., min_length=8)
    user_type: Optional[UserType] = UserType.INDIVIDUAL

    # Optional corporate fields
    company_name: Optional[str] = None
    company_registration: Optional[str] = None

    # Optional location
    location: Optional[Dict[str, Any]] = None

    @validator("password")
    def validate_password(cls, v):
        """Validate password strength"""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one digit")
        if not any(char.isupper() for char in v):
            raise ValueError("Password must contain at least one uppercase letter")
        return v

    @validator("phone")
    def validate_phone(cls, v):
        """Validate Ghana phone number format"""
        # Remove spaces and dashes
        phone = v.replace(" ", "").replace("-", "")

        # Check if it starts with valid Ghana prefixes
        if not (phone.startswith("233") or phone.startswith("0")):
            raise ValueError("Phone number must be a valid Ghana number")

        # Normalize to international format
        if phone.startswith("0"):
            phone = "233" + phone[1:]

        if len(phone) != 12:  # 233XXXXXXXXX
            raise ValueError("Phone number must be 10 digits (excluding country code)")

        return phone


class UserLogin(BaseModel):
    """User login schema"""
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """User update schema"""
    full_name: Optional[str] = None
    phone: Optional[str] = None
    profile_photo: Optional[str] = None
    location: Optional[Dict[str, Any]] = None
    saved_addresses: Optional[List[Dict[str, Any]]] = None
    notification_preferences: Optional[Dict[str, Any]] = None
    language_preference: Optional[str] = None

    # Corporate fields
    company_name: Optional[str] = None
    company_registration: Optional[str] = None


class UserResponse(UserBase):
    """User response schema"""
    id: str
    role: UserRole
    user_type: Optional[UserType]
    is_active: bool
    is_verified: bool
    email_verified: bool
    phone_verified: bool
    profile_photo: Optional[str]
    location: Optional[Dict[str, Any]]
    saved_addresses: Optional[List[Dict[str, Any]]]
    company_name: Optional[str]
    average_rating: float
    total_ratings: int
    loyalty_points: int
    referral_code: Optional[str]
    language_preference: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserInDB(UserResponse):
    """User in database (includes password hash)"""
    password_hash: str
