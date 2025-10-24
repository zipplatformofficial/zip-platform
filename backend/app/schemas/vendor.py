"""Vendor schemas"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from decimal import Decimal


class VendorRegister(BaseModel):
    """Vendor registration request"""
    # Business Info
    business_name: str = Field(..., min_length=2, max_length=200)
    business_registration_number: str = Field(..., min_length=5, max_length=50)

    # Contact Info
    contact_person: str = Field(..., min_length=2, max_length=200)
    email: EmailStr
    phone: str = Field(..., pattern=r"^\+?233\d{9}$|^0\d{9}$")
    password: str = Field(..., min_length=8)

    # Location
    address: str = Field(..., min_length=5)

    # Documents
    ghana_card_number: Optional[str] = Field(None, min_length=10, max_length=20)

    class Config:
        json_schema_extra = {
            "example": {
                "business_name": "Accra Auto Parts Ltd",
                "business_registration_number": "BN-12345678",
                "contact_person": "Kofi Asante",
                "email": "vendor@example.com",
                "phone": "+233244123456",
                "password": "SecurePass123!",
                "address": "123 Spintex Road, Accra",
                "ghana_card_number": "GHA-987654321-0"
            }
        }


class VendorProfileUpdate(BaseModel):
    """Update vendor profile"""
    business_name: Optional[str] = Field(None, min_length=2, max_length=200)
    contact_person: Optional[str] = Field(None, min_length=2, max_length=200)
    address: Optional[str] = None
    phone: Optional[str] = Field(None, pattern=r"^\+?233\d{9}$|^0\d{9}$")
    description: Optional[str] = Field(None, max_length=1000)


class VendorResponse(BaseModel):
    """Vendor profile response"""
    id: int
    user_id: int
    business_name: str
    business_registration_number: str
    contact_person: str
    address: str
    rating: Optional[Decimal] = None
    total_sales: int
    is_verified: bool
    description: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class VendorAnalytics(BaseModel):
    """Vendor analytics/dashboard"""
    total_revenue: Decimal
    pending_payout: Decimal
    total_orders: int
    pending_orders: int
    completed_orders: int
    this_month_revenue: Decimal
    this_month_orders: int
    total_products: int
    active_products: int
    average_rating: Optional[Decimal] = None

    class Config:
        json_schema_extra = {
            "example": {
                "total_revenue": 125400.50,
                "pending_payout": 12500.00,
                "total_orders": 245,
                "pending_orders": 8,
                "completed_orders": 220,
                "this_month_revenue": 8500.00,
                "this_month_orders": 15,
                "total_products": 45,
                "active_products": 42,
                "average_rating": 4.5
            }
        }


class PayoutRequest(BaseModel):
    """Request payout"""
    amount: Decimal = Field(..., gt=0, description="Amount to withdraw")
    bank_account_number: str = Field(..., min_length=10, max_length=20)
    bank_code: str = Field(..., description="Bank code from Paystack")
    account_name: str = Field(..., min_length=2)

    class Config:
        json_schema_extra = {
            "example": {
                "amount": 5000.00,
                "bank_account_number": "0123456789",
                "bank_code": "GH180101",
                "account_name": "Accra Auto Parts Ltd"
            }
        }
