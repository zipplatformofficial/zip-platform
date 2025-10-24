"""Notification schemas"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class NotificationResponse(BaseModel):
    """Notification response schema"""
    id: int
    user_id: int
    title: str
    message: str
    type: str
    channels: List[str]
    is_read: bool
    read_at: Optional[datetime] = None
    created_at: datetime
    metadata: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 123,
                "title": "Booking Confirmed",
                "message": "Your maintenance booking #BK12345 has been confirmed",
                "type": "BOOKING",
                "channels": ["in_app", "push", "email"],
                "is_read": False,
                "read_at": None,
                "created_at": "2025-01-15T10:30:00Z",
                "metadata": {
                    "booking_ref": "BK12345",
                    "service_type": "maintenance"
                }
            }
        }


class NotificationCreate(BaseModel):
    """Create notification request"""
    title: str = Field(..., min_length=1, max_length=200)
    message: str = Field(..., min_length=1, max_length=1000)
    type: str = Field(default="INFO")
    channels: List[str] = Field(default=["in_app"])
    metadata: Optional[Dict[str, Any]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Special Offer",
                "message": "Get 20% off your next service booking!",
                "type": "PROMOTION",
                "channels": ["in_app", "push"],
                "metadata": {
                    "promo_code": "SAVE20"
                }
            }
        }


class NotificationPreferences(BaseModel):
    """User notification preferences"""
    email_enabled: bool = True
    sms_enabled: bool = True
    push_enabled: bool = True
    booking_notifications: bool = True
    payment_notifications: bool = True
    order_notifications: bool = True
    promotional_notifications: bool = True

    class Config:
        json_schema_extra = {
            "example": {
                "email_enabled": True,
                "sms_enabled": True,
                "push_enabled": True,
                "booking_notifications": True,
                "payment_notifications": True,
                "order_notifications": True,
                "promotional_notifications": False
            }
        }


class FCMTokenUpdate(BaseModel):
    """Update FCM device token"""
    fcm_token: str = Field(..., min_length=10, description="Firebase Cloud Messaging device token")

    class Config:
        json_schema_extra = {
            "example": {
                "fcm_token": "dXYz1234567890abcdefghijklmnop"
            }
        }


class UnreadCountResponse(BaseModel):
    """Unread notification count"""
    count: int

    class Config:
        json_schema_extra = {
            "example": {
                "count": 5
            }
        }
