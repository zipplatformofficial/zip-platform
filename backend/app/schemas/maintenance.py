"""Maintenance service schemas"""
from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.maintenance import ServiceBookingStatus as BookingStatus


# Maintenance Service Schemas
class MaintenanceServiceBase(BaseModel):
    """Base maintenance service schema"""
    name: str
    description: Optional[str] = None
    service_type: str
    base_price: float = Field(gt=0)
    estimated_duration: Optional[int] = None  # minutes


class MaintenanceServiceCreate(MaintenanceServiceBase):
    """Create maintenance service schema"""
    pass


class MaintenanceServiceUpdate(BaseModel):
    """Update maintenance service schema"""
    name: Optional[str] = None
    description: Optional[str] = None
    service_type: Optional[str] = None
    base_price: Optional[float] = Field(None, gt=0)
    estimated_duration: Optional[int] = None
    is_active: Optional[bool] = None


class MaintenanceServiceResponse(MaintenanceServiceBase):
    """Maintenance service response schema"""
    id: int
    is_active: bool
    icon: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Technician Schemas
class TechnicianBase(BaseModel):
    """Base technician schema"""
    bio: Optional[str] = None
    specializations: Optional[list[str]] = None
    years_of_experience: Optional[int] = Field(None, ge=0)


class TechnicianCreate(TechnicianBase):
    """Create technician schema"""
    user_id: int


class TechnicianUpdate(BaseModel):
    """Update technician schema"""
    bio: Optional[str] = None
    specializations: Optional[list[str]] = None
    years_of_experience: Optional[int] = Field(None, ge=0)
    is_available: Optional[bool] = None
    is_verified: Optional[bool] = None


class TechnicianResponse(TechnicianBase):
    """Technician response schema"""
    id: int
    user_id: int
    is_available: bool
    is_verified: bool
    average_rating: float
    total_ratings: int
    total_jobs_completed: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Service Booking Schemas
class ServiceBookingBase(BaseModel):
    """Base service booking schema"""
    service_id: int
    vehicle_id: int
    scheduled_date: datetime
    location: Dict[str, Any]
    notes: Optional[str] = None


class ServiceBookingCreate(ServiceBookingBase):
    """Create service booking schema"""
    pass


class ServiceBookingUpdate(BaseModel):
    """Update service booking schema"""
    scheduled_date: Optional[datetime] = None
    location: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None
    status: Optional[BookingStatus] = None


class ServiceBookingResponse(ServiceBookingBase):
    """Service booking response schema"""
    id: int
    customer_id: int
    technician_id: Optional[int]
    status: BookingStatus
    final_price: Optional[float]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    customer_rating: Optional[int]
    customer_feedback: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BookingStatusUpdate(BaseModel):
    """Booking status update schema"""
    status: BookingStatus
    notes: Optional[str] = None


class BookingRating(BaseModel):
    """Booking rating schema"""
    rating: int = Field(ge=1, le=5)
    feedback: Optional[str] = None
