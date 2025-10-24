"""Car rental schemas"""
from typing import Optional, Dict, Any, List
from datetime import datetime, date
from pydantic import BaseModel, Field
from app.models.rental import RentalBookingStatus as RentalStatus


# Rental Vehicle Schemas
class RentalVehicleBase(BaseModel):
    """Base rental vehicle schema"""
    make: str
    model: str
    year: int = Field(ge=1900, le=2100)
    license_plate: str
    color: Optional[str] = None
    fuel_type: str
    transmission: str
    seating_capacity: Optional[int] = Field(None, ge=1, le=50)
    daily_rate: float = Field(gt=0)
    vehicle_type: str = "car"  # Default value
    vin: Optional[str] = None
    features: Optional[List[str]] = None
    is_available: bool = True


class RentalVehicleCreate(RentalVehicleBase):
    """Create rental vehicle schema"""
    photos: Optional[List[str]] = []  # Default to empty array
    description: Optional[str] = None


class RentalVehicleUpdate(BaseModel):
    """Update rental vehicle schema"""
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = Field(None, ge=1900, le=2100)
    color: Optional[str] = None
    fuel_type: Optional[str] = None
    transmission: Optional[str] = None
    seats: Optional[int] = Field(None, ge=1, le=50)
    daily_rate: Optional[float] = Field(None, gt=0)
    weekly_rate: Optional[float] = Field(None, gt=0)
    monthly_rate: Optional[float] = Field(None, gt=0)
    features: Optional[List[str]] = None
    images: Optional[List[str]] = None
    status: Optional[str] = None
    is_available: Optional[bool] = None


class RentalVehicleResponse(BaseModel):
    """Rental vehicle response schema"""
    id: int
    make: str
    model: str
    year: int
    license_plate: str
    color: Optional[str] = None
    fuel_type: str
    transmission: str
    seating_capacity: Optional[int] = None
    daily_rate: float
    vehicle_type: str
    vin: Optional[str] = None
    features: Optional[List[str]] = None
    photos: Optional[List[str]] = None
    description: Optional[str] = None
    is_available: bool
    average_rating: float = 0.0
    total_rentals: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Rental Booking Schemas
class RentalBookingBase(BaseModel):
    """Base rental booking schema"""
    vehicle_id: int
    start_date: date
    end_date: date
    pickup_location: Dict[str, Any]
    dropoff_location: Dict[str, Any]


class RentalBookingCreate(RentalBookingBase):
    """Create rental booking schema"""
    driver_license_number: str
    additional_drivers: Optional[List[Dict[str, str]]] = None
    insurance_option: Optional[str] = None


class RentalBookingUpdate(BaseModel):
    """Update rental booking schema"""
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    pickup_location: Optional[Dict[str, Any]] = None
    dropoff_location: Optional[Dict[str, Any]] = None
    status: Optional[RentalStatus] = None


class RentalBookingResponse(RentalBookingBase):
    """Rental booking response schema"""
    id: int
    customer_id: int
    booking_number: str
    status: RentalStatus
    total_days: int
    daily_rate: float
    total_price: float
    security_deposit: float
    insurance_cost: Optional[float]
    driver_license_number: str
    additional_drivers: Optional[List[Dict[str, str]]]
    picked_up_at: Optional[datetime]
    returned_at: Optional[datetime]
    actual_return_date: Optional[date]
    late_fee: Optional[float]
    damage_fee: Optional[float]
    customer_rating: Optional[int]
    customer_feedback: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RentalBookingStatusUpdate(BaseModel):
    """Rental booking status update schema"""
    status: RentalStatus


class RentalBookingRating(BaseModel):
    """Rental booking rating schema"""
    rating: int = Field(ge=1, le=5)
    feedback: Optional[str] = None


# Vehicle Inspection Schemas
class VehicleInspectionCreate(BaseModel):
    """Create vehicle inspection schema"""
    booking_id: int
    inspection_type: str  # pickup or return
    odometer_reading: int = Field(ge=0)
    fuel_level: int = Field(ge=0, le=100)
    exterior_condition: str
    interior_condition: str
    tire_condition: str
    damages: Optional[List[Dict[str, Any]]] = None
    photos: Optional[List[str]] = None
    notes: Optional[str] = None


class VehicleInspectionResponse(BaseModel):
    """Vehicle inspection response schema"""
    id: int
    booking_id: int
    inspector_id: int
    inspection_type: str
    odometer_reading: int
    fuel_level: int
    exterior_condition: str
    interior_condition: str
    tire_condition: str
    damages: Optional[List[Dict[str, Any]]]
    photos: Optional[List[str]]
    notes: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
