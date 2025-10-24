"""Technician schemas"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class TechnicianRegister(BaseModel):
    """Technician registration request"""
    # Personal Info
    full_name: str = Field(..., min_length=2, max_length=200)
    email: EmailStr
    phone: str = Field(..., pattern=r"^\+?233\d{9}$|^0\d{9}$")
    password: str = Field(..., min_length=8)

    # Professional Info
    specializations: List[str] = Field(..., min_items=1, description="Service types (oil_change, tire_repair, etc.)")
    years_of_experience: int = Field(..., ge=0, le=50)

    # Location
    address: str = Field(..., min_length=5)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)

    # Documents
    ghana_card_number: str = Field(..., min_length=10, max_length=20)

    class Config:
        json_schema_extra = {
            "example": {
                "full_name": "Kwame Mensah",
                "email": "kwame@example.com",
                "phone": "+233244123456",
                "password": "SecurePass123!",
                "specializations": ["oil_change", "tire_repair", "brake_service"],
                "years_of_experience": 5,
                "address": "123 Ring Road, Accra",
                "latitude": 5.6037,
                "longitude": -0.1870,
                "ghana_card_number": "GHA-123456789-0"
            }
        }


class TechnicianProfileUpdate(BaseModel):
    """Update technician profile"""
    specializations: Optional[List[str]] = None
    years_of_experience: Optional[int] = Field(None, ge=0, le=50)
    address: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    bio: Optional[str] = Field(None, max_length=500)


class TechnicianResponse(BaseModel):
    """Technician profile response"""
    id: int
    user_id: int
    specializations: List[str]
    years_of_experience: int
    rating: Optional[Decimal] = None
    total_jobs: int
    is_available: bool
    is_verified: bool
    address: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    bio: Optional[str] = None
    certifications: Optional[List[str]] = None
    created_at: datetime

    class Config:
        from_attributes = True


class TechnicianEarnings(BaseModel):
    """Technician earnings summary"""
    total_earnings: Decimal
    pending_payout: Decimal
    completed_jobs: int
    this_month_earnings: Decimal
    this_month_jobs: int
    average_rating: Optional[Decimal] = None

    class Config:
        json_schema_extra = {
            "example": {
                "total_earnings": 5420.50,
                "pending_payout": 850.00,
                "completed_jobs": 45,
                "this_month_earnings": 1200.00,
                "this_month_jobs": 8,
                "average_rating": 4.7
            }
        }


class AvailabilityUpdate(BaseModel):
    """Update availability status"""
    is_available: bool

    class Config:
        json_schema_extra = {
            "example": {
                "is_available": True
            }
        }
